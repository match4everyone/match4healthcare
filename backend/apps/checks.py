from django.apps import apps as camelot_apps
from django.core.checks import register, Error, Warning
from django.core.checks import Tags as DjangoTags
from django.conf import settings
import http.client
import json


def sendgrid_sandbox_mail_works():
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


@register(Tags.env_tag)
def check_env_variables_set(app_configs=None, **kwargs):
    """Check that all required environment variables (not belonging to emails) are set."""
    errors = []

    if settings.SECRET_KEY is None:
        errors.append(
            Error(
                "Django secret key not found.",
                hint=(
                    "You have to set the django application secret key in you environment with 'export SECRET_KEY=<<yourKey>>'."),
                id='env.E002',
            )
        )

    return errors


@register(Tags.mail_tag)
def check_send_mails(app_configs=None, **kwargs):
    """Check that we are actually able to send emails."""

    errors = []

    try:
        if settings.SENDGRID_API_KEY is None:
            errors.append(
                Error(
                    "Sendgrid API key not found.",
                    hint=(
                        "You have to set the Sendgrid API key in you environment with 'export SENDGRID_API_KEY=<<yourKey>>'."),
                    id='mails.E001',
                )
            )
        else:
            if not sendgrid_sandbox_mail_works():
                errors.append(
                    Error(
                        "You want to use Sendgrid, but sending a mail in sandbox mode fails.",
                        hint=("Your API key might be invalid, something is up with sendgrid... go check it!"),
                        id='mails.E002',
                    )
                )

    except AttributeError:
        # the user did not set a key at all and is in development, so we just mention that he's on a different backend.
        errors.append(
            Warning(
                "No SENDGRID API key.",
                hint=(
                    "That's okay if you are using another email backend. "
                    "If you do want to use the Sendgrid email backend, set the 'mail_relay_option' to sendgrid in 'development.py'"),
                id='env.E001',
            )
        )

    return errors
