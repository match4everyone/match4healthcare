from django.contrib.auth.decorators import login_required#
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import pandas as pd
import datetime
from django.conf import settings
from apps.iamstudent.models import EmailToSend
from django.core.mail import send_mail
import logging
logger = logging.getLogger("django")


@login_required
@staff_member_required
def resend_emailtosend(request):

    startup_time = datetime.datetime(year=2020, month=4, day=8, hour=7, minute=51)
    startup_time_minus_24h = datetime.datetime(year=2020, month=4, day=7, hour=7, minute=51)
    end_time = datetime.datetime(year=2020, month=4, day=8, hour=23, minute=31)

    really_send = 'reallySend' in  request.GET
    logger.warning("Start Process of resending!")
    if not really_send:
        logger.warning("TESTMODE NOT REALLY SENDING MAILS")

    mails_definitely_send = EmailToSend.objects.filter(
        # From begin of when it didnt work
        registration_date__gte=startup_time,
        # To end of when it didnt work
        registration_date__lte=end_time,
        hospital__is_approved=True
    )

    for mail in mails_definitely_send:
        if not mail.was_sent:
            logger.warning("From Hospital: %s %s to Student: %s with subject: %s from %s" %
                           (mail.hospital.name, mail.hospital.user.email, mail.student.user.email, mail.subject,
                            str(mail.registration_date)))
            if really_send:
                resend_mail(mail)
        else:
            logger.warning("WARNING ALREADY SENT!!! From Hospital: %s %s to Student: %s with subject: %s from %s" %
                           (mail.hospital.name, mail.hospital.user.email, mail.student.user.email, mail.subject,
                            str(mail.registration_date)))

    logger.warning("\n\n\n=====================================================================\n\n\n")

    mails_maybe_send = EmailToSend.objects.filter(
        # From day before it didnt work
        registration_date__gte=startup_time_minus_24h,
        # To begin of when it didnt work
        registration_date__lte=startup_time,
        hospital__is_approved=True,
        was_sent=False,
    )
    df = pd.read_csv("apps/accounts/sendgriddump.csv", parse_dates=["processed"])[["processed", "subject", "email"]]
    ind = (df["processed"] > startup_time_minus_24h) & (df["processed"] < startup_time)
    sendgriddump = df[ind]
    logger.warning(str(len(df)) + " " + str(len(sendgriddump)))

    for mail in mails_maybe_send:
        if not mail.was_sent:
            # check if theyre in the csv dump from sendgrid
            filtered = sendgriddump[sendgriddump["email"] == mail.user.email]
            filtered = filtered[filtered["subject"].str.contains(mail.subject)]

            if len(filtered)==0:
                # if theyre not in sendgrid, they have not been sent
                logger.warning("From Hospital: %s %s to Student: %s with subject: %s from %s" %
                               (mail.hospital.name, mail.hospital.user.email, mail.student.user.email, mail.subject, str(mail.registration_date)))
                if really_send:
                    resend_mail(mail)

            elif len(filtered)>1:
                logger.warning("WARNING POSSIBLE DUPLICATE! From Hospital: %s %s to Student: %s with subject: %s from %s" %
                               (mail.hospital.name, mail.hospital.user.email, mail.student.user.email, mail.subject, str(mail.registration_date)))

    return HttpResponse(200)


def resend_mail(mail):
    try:
        send_mail(mail.subject,
                  mail.message,
                  settings.NOREPLY_MAIL,
                  [mail.student.user.email]
        )
    except:
        logger.warning("COULD NOT SEND! From Hospital: %s %s to Student: %s with subject: %s from %s" %
                       (mail.hospital.name, mail.hospital.user.email, mail.student.user.email, mail.subject,
                        str(mail.registration_date)))
