# adapted from: https://gist.github.com/jcinis/2866253
import logging

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm

logger = logging.getLogger("django")


def send_password_set_email(
    email, host, subject_template, template="registration/password_set_email_.html"
):
    form = PasswordResetForm({"email": email})
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
        logger.warning("Email to %s not sent because form is invalid", str(email))
