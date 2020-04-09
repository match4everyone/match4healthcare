from django.apps import apps as camelot_apps
from django.core.checks import register, Error, Warning
from django.core.checks import Tags as DjangoTags
from django.conf import settings


class Tags(DjangoTags):
    mail_tag = 'mails'


@register(Tags.mail_tag)
def check_numpy_is_installed(app_configs=None, **kwargs):
    "Check that django-taggit is installed when usying myapp."
    errors = []

    try:
        if settings.SENDGRID_API_KEY:
            import http.client
            import json

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
            assert res.status == 200

    except AttributeError:
        errors.append(
            Warning(
                "Sendgrid API key not found.",
                hint=("Either you are in development and using another backend, then this is fine. "
                      "Otherwise, check if you have your API key for SENDGRID at the right place."),
                id='mails.W001',
            )
        )

    except AssertionError:
        errors.append(
            Error(
                "You want to use Sendgrid, but sending a mail in sandbox mode fails.",
                hint=("Your API key might be invalid, something is up with sendgrid... go check it!"),
                id='mails.E001',
            )
        )

    return errors
