# adapted from: https://gist.github.com/jcinis/2866253
from random import choice
from string import ascii_lowercase, digits
from .models import User
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.forms import PasswordResetForm

from django.conf import settings

def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):

    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username



def send_password_set_email(email, host, subject_template, template='registration/password_set_email_.html'):
    form = PasswordResetForm({'email': email})
    logger.debug("Sending Password reset to", email)
    if form.is_valid():
        form.save(
            subject_template_name=subject_template,
            html_email_template_name=template,
            domain_override=host,
            from_email=settings.NOREPLY_MAIL,
            use_https=True,
        )
        logger.debug("Sent!")
    else:
        logger.warn("Email to " + str(email) + " not sent because form is invalid")
