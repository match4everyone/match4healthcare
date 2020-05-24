from datetime import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from apps.accounts.models import User
from apps.accounts.src.notifications import send_password_set_email

logger = logging.getLogger(__name__)


@login_required
def validate_email(request):
    if not request.user.validated_email:
        request.user.validated_email = True
        request.user.email_validation_date = datetime.now()
        request.user.save()
    return HttpResponseRedirect("login_redirect")


def resend_validation_email(request, email):
    if request.user.is_anonymous:
        if not User.objects.get(username=email).validated_email:
            send_password_set_email(
                email=email,
                host=request.META["HTTP_HOST"],
                template="registration/password_set_email_.html",
                subject_template="registration/password_reset_email_subject.txt",
            )
            return HttpResponseRedirect("/accounts/password_reset/done")
    return HttpResponseRedirect("/")
