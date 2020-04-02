from django.contrib.auth.decorators import login_required
from .decorator import student_required, hospital_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

import logging
logger = logging.getLogger(__name__)

from .models import User

import datetime

from .utils import send_password_set_email
import time

@login_required
@staff_member_required
def resend_validation(request):
    really_send = 'reallySend' in  request.GET
    logger.warn("Start Process of resending!")
    if not really_send:
        logger.warn("TESTMODE NOT REALLY SENDING MAILS")
    timeout = 30  # seconds
    every_mail = 100

    startup_time = datetime.datetime(year=2020, month=4, day=2, hour=3, minute=33)
    end_time = datetime.datetime(year=2020, month=4, day=2, hour=19, minute=1)

    qs = User.objects.filter(validated_email=False,
                             date_joined__gt=startup_time,
                             date_joined__lt=end_time)

    for i, user in enumerate(qs):

        if i > 1 and i % every_mail == 0:
            logger.warn('Waiting %s seconds' % timeout)
            time.sleep(timeout)

        if user.is_student:
            if really_send:
                send_password_set_email(
                    email=user.email,
                    host=request.META['HTTP_HOST'],
                    template="registration/password_set_email_.html",
                    subject_template="registration/password_reset_email_subject.txt"
                )
            logger.warn('Resend validation to :' + user.email)

        if user.is_hospital:
            if really_send:
                send_password_set_email(
                    email=user.email,
                    host=request.META['HTTP_HOST'],
                    template="registration/password_set_email_hospital.html",
                    subject_template="registration/password_reset_email_subject.txt"
                )
            logger.warn('Resend validation to :' + user.email)
    logger.warn('ended process of resending')
    return HttpResponse('okaayy, done :*')
