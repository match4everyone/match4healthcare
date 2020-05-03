from django.core.checks import register, Error, Warning
from django.core.checks import Tags as DjangoTags
from django.conf import settings
import http.client
import json
import os

ENVS = settings.ENVS


def register_check(tag, for_environments, exclude_if_travis=False, exclude_if_fork=False):
    if settings.THIS_ENV in for_environments:
        if not ((settings.IS_FORK and exclude_if_fork)
                or (settings.IS_TRAVIS and exclude_if_travis)):
            return register(tag)
    return lambda x: x


def does_sendgrid_sandbox_mail_work():
    conn = http.client.HTTPSConnection("api.sendgrid.com")

    payload = {"personalizations": [
        {
            "to": [{"email": "john.doe@example.com", "name": "John Doe"}],
            "subject": "Hello, World!"
        }],
        "content": [{"type": "text/plain", "value": "Heya!"}],
        "from": {"email": "sam.smith@example.com", "name": "Sam Smith"},
        "reply_to": {"email": "sam.smith@example.com", "name": "Sam Smith"},
        "mail_settings": {
            "sandbox_mode": {
                "enable": True
            }
        }
    }
    headers = {
        'authorization': "Bearer " + settings.SENDGRID_API_KEY,
        'content-type': "application/json"
    }

    conn.request("POST", "/v3/mail/send", json.dumps(payload), headers)

    res = conn.getresponse()
    # on success, sendgrid returns a 200 OK

    return res.status == 200


class Tags(DjangoTags):
    mail_tag = 'mails'
    env_tag = 'environment'


@register_check(Tags.env_tag, [ENVS.DEVELOPMENT, ENVS.PRODUCTION])
def check_slack_webhook(app_configs=None, **kwargs):
    errors = []
    if os.environ.get('SLACK_LOG_WEBHOOK') is None:
        errors.append(
            Warning(
                "No Slack Webhook for logging set.",
                hint=(
                    "Currently no logging to Slack Channels is configured.\n\t"
                    "This is not necessary, but recommended for production deployment. A key can be generated "
                    "using the documentation at:\n\t"
                    "https://slack.com/intl/en-at/help/articles/115005265063-Incoming-Webhooks-for-Slack\n\t"
                    "To use Slack Error notifications set the webhook in your environment using "
                    "'export SLACK_LOG_WEBHOOK=<<webhook URL>>="),
                id='env.E003',
            )
        )
    return errors


@register_check(Tags.env_tag, [ENVS.DEVELOPMENT, ENVS.PRODUCTION])
def check_secret_key(app_configs=None, **kwargs):
    errors = []
    if settings.SECRET_KEY is None:
        errors.append(
            Error(
                "Django secret key not found.",
                hint=(
                    "You have to set the django application secret key in you environment with "
                    "'export SECRET_KEY=<<yourKey>>'."),
                id='env.E002',
            )
        )
    return errors


@register_check(Tags.mail_tag, [ENVS.DEVELOPMENT])
def check_sendgrid_dev(app_configs=None, **kwargs):
    errors = []
    if settings.MAIL_RELAY_OPTION == 'sendgrid':
        if settings.SENDGRID_API_KEY is None:
            errors.append(
                Error("Sendgrid API key not found.",
                      hint=("Your are in development mode, and want to use the sendgrid backend. "
                            "We did not find an API key.\n"
                            "You have to set the Sendgrid API key in you environment with 'export "
                            "SENDGRID_API_KEY=<<yourKey>>'.\n"
                            "If you want to use another backend set 'MAIL_RELAY_OPTION' in the development"
                            " settings to another value, e.g. 'file'."),
                      id='mails.E003'))
        else:
            if not does_sendgrid_sandbox_mail_work():
                errors.append(
                    Error(
                        "You want to use Sendgrid, but sending a mail in sandbox mode fails.",
                        hint=("Your API key might be invalid, something is up with sendgrid... "
                              "go check it!"),
                        id='mails.E002',
                    )
                )
    return errors


@register_check(Tags.mail_tag, [ENVS.PRODUCTION], exclude_if_fork=True)
def check_sendgrid_prod(app_configs=None, **kwargs):
    errors = []
    if settings.SENDGRID_API_KEY is None:
        errors.append(
            Error(
                "Sendgrid API key not found.",
                hint=(
                    "You have to set the Sendgrid API key in you environment with 'export "
                    "SENDGRID_API_KEY=<<yourKey>>'."
                    "If thats "),
                id='mails.E001',
            ))
    else:
        if not does_sendgrid_sandbox_mail_work():
            errors.append(
                Error(
                    "You want to use Sendgrid, but sending a mail in sandbox mode fails.",
                    hint=("Your API key might be invalid, something is up with sendgrid... "
                          "go check it!"),
                    id='mails.E002',
                )
            )
    return errors
