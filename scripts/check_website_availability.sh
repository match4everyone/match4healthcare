#!/usr/bin/env bash

# ======================================================================================
# title			:  check_website_basic.sh
# description	:  Checks if the website is up and can be served as well as
#				   whether Django throws an error while serving
# author       	:  Kevin Yuan
# date			:  28.03.2020
# version		:  1.0
# notes			:  This script is called by travis but should work locally too
# ======================================================================================

# Setting some colors
red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# Return variable
failed=False

# Site
URL=localhost:8000

# Log file location
ERR_LOG_PATH=backend/run/match4healthcare.json.error.log

# Execute command and print status
function test() {
	printf "${1}:\t"
	eval "$2"
	if [[ $? -eq 0 ]]; then
		printf "${grn}Pass\n${end}"
	else
		failed=True
		printf "${red}Failed\n${end}"
	fi
}


function check_website_up() {
	# Check if log file exists
	for i in $(seq 1 10); do
		# GET request to website and get http code fromkk server https://superuser.com/a/442395
		if [[  $(curl -s -o /dev/null -w "%{http_code}\n" $URL) -eq 200 ]]; then
    		break
		else
			if [[ i -eq 10 ]]; then
				printf "Website error code: $(curl -s -o /dev/null -w "%{http_code}\n" $URL)"
				return 1
			fi
		fi
		sleep 1
	done

}

function check_error_log_empty() {
	# Check if log file exists
	for i in $(seq 1 10); do
		if [ -f "$ERR_LOG_PATH" ]; then
    		break
		else
			if [[ i -eq 10 ]]; then
				printf "Log file not found\t"
				return 1
			fi
		fi
		sleep 1
	done

	curl --silent --output /dev/null localhost:8000
	sleep 5
	if [  -s "$ERR_LOG_PATH" ]; then
		printf "\n"
		cat "$ERR_LOG_PATH"
		printf "\n"
		return 1
	fi
}

test "Website reachable" "check_website_up"
test "Error log empty" "check_error_log_empty"

# If everything went well we exit with zero, else one
if [[ $failed = "True" ]]; then
	exit 1
else
	exit 0
fi