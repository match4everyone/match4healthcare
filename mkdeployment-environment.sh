#!/bin/bash -e
TOOLS="$(pwd)/tools"
GOROOT="${TOOLS}/go-dist"
SERVERHOME="$(pwd)/m4h-server"
PREDEPLOY_BRANCH="malte-test-predeploy"
DEPLOY_BRANCH="production"
REPO="git@github.com:match4healthcare/match4healthcare.git"
GITHUB_SECRET="$(tr -dc 'a-z0-9!A-Z(-_=+)' < /dev/urandom | head -c50)"

OK="\t\e[32mOK\e[0m"
ERROR="\t\e[31mERROR\e[0m"

export GOPATH="${TOOLS}/go-build"
export GOCACHE="${TOOLS}/go-cache"
export PATH="${PATH}:${GOROOT}/go/bin:${TOOLS}/bin"

echo -n "Deleting old directories: \"${TOOLS}\" \"${SERVERHOME}-deploy\" \"${SERVERHOME}-predeploy\""

rm -rf "${TOOLS}"                \
       "${SERVERHOME}-deploy"    \
       "${SERVERHOME}-predeploy" \
        && echo -e $OK || { echo -e "$ERROR"; exit 1; }

echo -n "(Re)creating empty directories"
mkdir -p "${GOROOT}" "${GOPATH}" "${GOCACHE}" && echo -e $OK || { echo -e "$ERROR"; exit 1; }

echo -n "Downloading and installing golang"
curl -s https://dl.google.com/go/go1.14.1.linux-amd64.tar.gz |tar -xzC "${GOROOT}" && echo -e $OK || { echo -e "$ERROR"; exit 1; }

go get github.com/adnanh/webhook && echo -e "Webhook-Installation\t$OK" || { echo -e "Webhook-Installation\t$ERROR"; exit 1; }
git clone -q -b "${PREDEPLOY_BRANCH}" --depth 1 "${REPO}" "${SERVERHOME}-predeploy" && echo -e "Git Clone ${PREDEPLOY_BRANCH} -> ${SERVERHOME}-predeploy\t$OK" || { echo -e "Git Clone\t$ERROR"; exit 1; }
git clone -q -b "${DEPLOY_BRANCH}"    --depth 1 "${REPO}" "${SERVERHOME}-deploy"    && echo -e "Git Clone ${DEPLOY_BRANCH}    -> ${SERVERHOME}-deploy \t\t$OK" || { echo -e "Git Clone\t$ERROR"; exit 1; }

echo "Creating Config files and folders"
ln -s "${GOPATH}/bin/webhook" "${TOOLS}"
mkdir -p "${TOOLS}/webhooks/github"
cat > "${TOOLS}/webhooks/hooks.json" <<EOF
[
  {
    "id": "deploy",
    "execute-command": "${TOOLS}/webhooks/github/deploy.sh",
    "command-working-directory": "${SERVERHOME}-deploy",
    "response-message": "Executing deploy script...",
    "include-command-output-in-response": true,
    "include-command-output-in-response-on-error": true,
    "pass-arguments-to-command": [
      {
        "source": "payload",
        "name": "ref"
      }
    ],
    "trigger-rule": {
      "match": {
        "type": "payload-hash-sha1",
        "secret": "${GITHUB_SECRET}",
        "parameter": {
          "source": "header",
          "name": "X-Hub-Signature"
        }
      }
    }
  }
]
EOF

function generate_env_file(){
ENV_FILE="${TOOLS}/webhooks/github/${1}.env"
cat > "${ENV_FILE}" <<EOF
SECRET_KEY="$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)"
POSTGRES_DB="${1}"
POSTGRES_USER="m4hc"
POSTGRES_PASSWORD="$( tr -dc 'a-z0-9!_=+)' < /dev/urandom | head -c10 )"
CURRENT_UID=$(id -u):$(id -g)
EOF
}

generate_env_file "${PREDEPLOY_BRANCH}"
generate_env_file "${DEPLOY_BRANCH}"

cat > "${TOOLS}/webhooks/github/deploy.sh" <<EOF
#!/bin/bash -ex

# Extract Branch from argument ref ("refs/heads/branch-name")
export BRANCH="\${1##*/}"
export ENV_FILE="${TOOLS}/webhooks/github/\${BRANCH}.env"

if [ "\$BRANCH" == "$PREDEPLOY_BRANCH" ]; then
    echo "Predeploy Branch - Call Mirror Database script"
    "${TOOLS}/webhooks/github/cp-db-from-deploy-to-predeploy.sh"
    echo "Set backend port to 8020"
    export BACKEND_PORT=8020
    echo "Switch working dir to ${SERVERHOME}-predeploy"
    cd "${SERVERHOME}-predeploy"
elif [ "\$BRANCH" == "$DEPLOY_BRANCH" ]; then
    echo "Deploy Branch Set backend port to 8020"
    export BACKEND_PORT=8020
    echo "Switch working dir to ${SERVERHOME}-deploy"
    cd "${SERVERHOME}-deploy"
else    
    echo "Branch not relevant for this system, abort deployment"
fi

source "${ENV_FILE}"
env

git fetch --all
git checkout --force "origin/\${BRANCH}"

cp "${TOOLS}/webhooks/github/\${BRANCH}.env" "./prod.env"
docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml up --build -d

docker exec --env PYTHONPATH="/match4healthcare-backend:$PYTHONPATH" "\${BRANCH}-backend" django-admin makemessages
docker exec --env PYTHONPATH="/match4healthcare-backend:$PYTHONPATH" "\${BRANCH}-backend" django-admin compilemessages
docker exec "\${BRANCH}-backend" python3 manage.py migrate
docker exec "\${BRANCH}-backend" python3 manage.py collectstatic --no-input
EOF

cat > "${TOOLS}/webhooks/github/cp-db-from-deploy-to-predeploy.sh" <<EOF
#!/bin/bash -e
echo "Now we would copy prod DB to predeploy instance"
EOF

chmod +x "${TOOLS}/webhooks/github/"*.sh
echo -e "Finished preparations\n\nStarting webhookd using the following command:"
echo -e "${TOOLS}/webhook -hooks ${TOOLS}/webhooks/hooks.json -ip 0.0.0.0 -verbose\n"
echo -e "Please remember to set GitHub secret to ${GITHUB_SECRET}\n"
"${TOOLS}/webhook" -hooks "${TOOLS}/webhooks/hooks.json" -ip "0.0.0.0" -verbose

