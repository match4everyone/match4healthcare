from datetime import datetime
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _

from apps.accounts.decorator import student_required
from apps.accounts.modelss import Newsletter, User
from apps.accounts.utils import send_password_set_email
from apps.iamstudent.views import send_mails_for
from apps.ineedstudent.models import Hospital

logger = logging.getLogger(__name__)


@login_required
@staff_member_required
def change_hospital_approval(request, uuid):

    h = Hospital.objects.get(uuid=uuid)
    logger.info(
        "Set Hospital %s approval to %s", uuid, (not h.is_approved), extra={"request": request},
    )

    if not h.is_approved:
        h.is_approved = True
        h.approval_date = datetime.now()
        h.approved_by = request.user
    else:
        h.is_approved = False
        h.approval_date = None
        h.approved_by = None
    h.save()

    if h.is_approved:
        send_mails_for(h)

    return HttpResponseRedirect("/accounts/approve_hospitals")


@login_required
def delete_me(request):
    user = request.user
    logout(request)
    user.delete()
    return render(request, "deleted_user.html")


@login_required
def delete_me_ask(request):
    return render(request, "deleted_user_ask.html")


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


@login_required
@student_required
def change_activation_ask(request):
    return render(
        request, "change_activation_ask.html", {"is_activated": request.user.student.is_activated},
    )


@login_required
@student_required
def change_activation(request):
    s = request.user.student
    status = s.is_activated
    s.is_activated = not s.is_activated
    s.save()
    if status:
        messages.add_message(
            request,
            messages.INFO,
            _(
                "Du hast dein Profil erfolgreich deaktiviert, du kannst nun keine Anfragen mehr von Hilfesuchenden bekommen."
            ),
        )
    else:
        messages.add_message(
            request,
            messages.INFO,
            _(
                "Du hast dein Profil erfolgreich aktiviert, du kannst nun wieder von Hilfesuchenden kontaktiert werden."
            ),
        )
    return HttpResponseRedirect("profile_student")


@login_required
@staff_member_required
def new_newsletter(request):
    newsletter = Newsletter.objects.create()
    newsletter.letter_authored_by.add(request.user)
    newsletter.save()
    return HttpResponseRedirect("view_newsletter/" + str(newsletter.uuid))
