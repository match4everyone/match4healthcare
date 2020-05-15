import datetime
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import format_lazy
from django.utils.translation import gettext as _

from apps.accounts.decorator import hospital_required
from apps.iamstudent.forms import EmailToSendForm
from apps.iamstudent.models import EmailGroup, EmailToSend, Student

logger = logging.getLogger(__name__)


@login_required
@hospital_required
def send_mail_student_id_list(request, id_list):
    id_list = id_list.split("_")

    max_emails = request.user.hospital.leftover_emails_for_today()
    if max_emails < len(id_list):
        pass
        # do something

    hospital = request.user.hospital
    message = format_lazy(
        _(
            "Liebe(r) Helfende(r),\n\n"
            "Wir sind... \n"
            "Wir suchen...\n\n"
            "Meldet euch baldmöglichst!\n\nBeste Grüße,\n{ansprechpartner}\n\nTel: {telefon}\nEmail: {email}"
        ),
        ansprechpartner=hospital.ansprechpartner,
        telefon=hospital.telefon,
        email=hospital.user.email,
    )

    initial = {"subject": _("Ein Ort braucht Deine Hilfe"), "message": message}
    form = EmailToSendForm(initial=initial)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = EmailToSendForm(request.POST, initial=initial)

        if form.is_valid():

            hospital_message = form.cleaned_data["message"]

            subject = form.cleaned_data["subject"]

            email_group = EmailGroup.objects.create(
                subject=subject, message=hospital_message, hospital=request.user.hospital,
            )

            for student_id in id_list:
                student = Student.objects.get(user_id=student_id)

                new_message = format_lazy(
                    _(
                        "Hallo {first_name} {last_name},\n\n "
                        "wir haben folgende Nachricht von {firmenname} für dich. "
                        "Falls du keine Nachrichten mehr erhalten möchtest, deaktiviere dein "
                        "Konto bitte hier: https://match4healthcare.de/accounts/change_activation"
                        "\n\nDein Match4Healthcare Team"
                        "\n----------------------------\n"
                        "{hospital_message}"
                    ),
                    first_name=student.name_first,
                    last_name=student.name_last,
                    firmenname=request.user.hospital.firmenname,
                    hospital_message=hospital_message,
                )

                mail = EmailToSend.objects.create(
                    student=student,
                    hospital=request.user.hospital,
                    message=new_message,
                    subject="[match4healthcare] " + subject,
                    email_group=email_group,
                )
                mail.save()

            if request.user.hospital.is_approved:
                send_mails_for(request.user.hospital)

            return HttpResponseRedirect("/iamstudent/successful_mail")

    return render(
        request,
        "send_mail_hospital.html",
        {"form": form, "ids": "_".join(id_list), "n": len(id_list)},
    )


def send_mails_for(hospital):
    emails = EmailToSend.objects.filter(hospital=hospital, was_sent=False)
    if len(emails) == 0:
        return None

    # inform the hospital about sent emails via
    sent_emailgroups = []

    for m in emails:

        if m.email_group_id not in sent_emailgroups:
            sent_emailgroups.append(m.email_group_id)
            text = m.email_group.message
            send_mail(
                _("[match4healthcare] Sie haben gerade potentielle Helfer*innen kontaktiert"),
                ("Hallo %s,\n\n" % hospital.ansprechpartner)
                + (
                    "Sie haben potentielle Helfer*innen mit der folgenden Nachricht kontaktiert. "
                    "Diese Mails wurden gerade abgesendet."
                    "\n\nLiebe Grüße,\nIhr match4healthcare Team\n\n=============\n\n"
                )
                + text,
                settings.NOREPLY_MAIL,
                [hospital.user.email],
            )

        if m.subject and m.message and m.student.user.email:
            try:
                send_mail(m.subject, m.message, settings.NOREPLY_MAIL, [m.student.user.email])
                # TODO: muss noch asynchron werden ...celery? # noqa: T003
                m.send_date = datetime.datetime.now()
                m.was_sent = True
                m.save()

            except BadHeaderError:
                # Do not show error message to malicous actor
                # Do not send the email
                logger.warning(
                    "Email with email_group_id %s to Students from Hospital %s could not be sent due to a BadHeaderError",
                    str(m.email_group_id),
                    str(hospital.user.email),
                )
