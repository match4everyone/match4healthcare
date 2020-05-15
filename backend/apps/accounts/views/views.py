from datetime import datetime
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import format_lazy
from django.utils.translation import gettext as _

from apps.accounts.decorator import student_required
from apps.accounts.forms import NewsletterEditForm, NewsletterViewForm, TestMailForm
from apps.accounts.modelss import LetterApprovedBy, Newsletter, NewsletterState, User
from apps.accounts.utils import send_password_set_email
from apps.iamstudent.views import send_mails_for
from apps.ineedstudent.models import Hospital

logger = logging.getLogger(__name__)


@login_required
def profile_redirect(request):
    user = request.user

    if user.is_student:
        return HttpResponseRedirect("profile_student")

    elif user.is_hospital:
        h = Hospital.objects.get(user=user)
        if not h.datenschutz_zugestimmt or not h.einwilligung_datenweitergabe:
            return HttpResponseRedirect("/ineedstudent/zustimmung")
        return HttpResponseRedirect("profile_hospital")

    elif user.is_staff:
        return HttpResponseRedirect("profile_staff")

    else:
        # TODO: throw 404  # noqa: T003
        logger.warning(
            "User is unknown type, profile redirect not possible", extra={"request": request},
        )
        HttpResponse("Something wrong in database")


@login_required
def login_redirect(request):
    user = request.user

    if user.is_student:
        return HttpResponseRedirect("/mapview")

    elif user.is_hospital:
        h = Hospital.objects.get(user=user)
        if not h.datenschutz_zugestimmt or not h.einwilligung_datenweitergabe:
            return HttpResponseRedirect("/ineedstudent/zustimmung")
        return HttpResponseRedirect("/ineedstudent/hospital_dashboard")

    elif user.is_staff:
        return HttpResponseRedirect("approve_hospitals")

    else:
        # TODO: throw 404  # noqa: T003
        logger.warning(
            "User is unknown type, login redirect not possible", extra={"request": request},
        )
        HttpResponse("Something wrong in database")


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
@staff_member_required
def delete_hospital(request, uuid):
    h = Hospital.objects.get(uuid=uuid)
    logger.info(
        "Delete Hospital %s by %s", uuid, request.user, extra={"request": request},
    )
    name = h.user
    h.delete()
    text = format_lazy(_("Du hast die Institution mit user '{name}' gelöscht."), name=name)
    messages.add_message(request, messages.INFO, text)
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


def switch_newsletter(nl, user, request, post=None, get=None):
    nl_state = nl.sending_state()

    if nl_state == NewsletterState.BEING_EDITED:
        # an edit was made
        if post is not None:
            form = NewsletterEditForm(post, uuid=nl.uuid, instance=nl)

            if form.is_valid():
                form.save()
                nl.edit_meta_data(user)
                nl.save()
                messages.add_message(request, messages.INFO, _("Bearbeitungen gespeichert."))
                return switch_newsletter(nl, user, request, post=None, get=None)

        elif get is not None:
            # wants to freeze the form for review
            if "freezeNewsletter" in get:
                nl.freeze(user)
                nl.save()
                messages.add_message(
                    request,
                    messages.INFO,
                    _(
                        "Der Newsletter kann nun nicht mehr editiert werden. Andere Leute können ihn approven."
                    ),
                )
                return switch_newsletter(nl, user, request, post=None, get=None)
            else:
                # the form is a virgin
                form = NewsletterEditForm(uuid=nl.uuid, instance=nl)
        else:
            form = NewsletterEditForm(uuid=nl.uuid, instance=nl)

    elif nl_state == NewsletterState.UNDER_APPROVAL:
        if get is not None:
            if "unFreezeNewsletter" in get:
                nl.unfreeze()
                nl.save()
                messages.add_message(
                    request, messages.INFO, _("Der Newsletter kann wieder bearbeitet werden."),
                )
                return switch_newsletter(nl, user, request, post=None, get=None)
            elif "approveNewsletter" in get:
                # TODO: check that author cannot approve # noqa: T003
                nl.approve_from(user)
                nl.save()
                messages.add_message(
                    request,
                    messages.WARNING,
                    format_lazy(
                        _(
                            "Noch ist deine Zustimmung UNGÜLTIG. Du musst den Validierungslink in der dir gesendeten Mail ({mail}) anklicken."
                        ),
                        mail=user.email,
                    ),
                )
                approval = LetterApprovedBy.objects.get(newsletter=nl, user=request.user)
                nl.send_approval_mail(approval, host=request.META["HTTP_HOST"])
                switch_newsletter(nl, user, request, post=None, get=None)

        form = NewsletterViewForm(instance=nl)

    elif nl_state == NewsletterState.READY_TO_SEND:
        if get is not None:
            if "sendNewsletter" in get:
                nl.send(user)
                nl.save()
                messages.add_message(request, messages.INFO, _("Der Newsletter wurde versendet."))
                switch_newsletter(nl, user, request)
            if "unFreezeNewsletter" in get:
                nl.unfreeze()
                nl.save()
                messages.add_message(
                    request, messages.INFO, _("Der Newsletter kann wieder bearbeitet werden."),
                )
                return switch_newsletter(nl, user, request, post=None, get=None)

        form = NewsletterViewForm(instance=nl)

    elif nl_state == NewsletterState.SENT:
        form = NewsletterViewForm(instance=nl)
    else:
        from django.http import Http404

        raise Http404

    return form, nl


@login_required
@staff_member_required
def view_newsletter(request, uuid):
    # 404 if not there?
    nl = Newsletter.objects.get(uuid=uuid)

    if request.method == "GET" and "email" in request.GET:
        email = request.GET.get("email")
        nl.send_testmail_to(email)
        messages.add_message(
            request, messages.INFO, _("Eine Test Email wurde an %s versendet." % email)
        )

    post = request.POST if request.method == "POST" else None
    get = request.GET if request.method == "GET" else None

    form, nl = switch_newsletter(nl, request.user, request, post=post, get=get)

    # special view if person was the freezer

    context = {
        "form": form,
        "uuid": uuid,
        "newsletter_state": nl.sending_state(),
        "state_enum": NewsletterState,
        "mail_form": TestMailForm(),
        "already_approved_by_this_user": nl.has_been_approved_by(request.user),
        "required_approvals": nl.required_approvals(),
        "frozen_by": nl.frozen_by,
        "sent_by": nl.sent_by,
        "send_date": nl.send_date,
        "approvers": ", ".join([a.user.username for a in nl.letterapprovedby_set.all()]),
    }

    return render(request, "newsletter_edit.html", context)


@login_required
@staff_member_required
def new_newsletter(request):
    newsletter = Newsletter.objects.create()
    newsletter.letter_authored_by.add(request.user)
    newsletter.save()
    return HttpResponseRedirect("view_newsletter/" + str(newsletter.uuid))


@login_required
@staff_member_required
def did_see_newsletter(request, uuid, token):
    nl = Newsletter.objects.get(uuid=uuid)
    try:
        approval = LetterApprovedBy.objects.get(newsletter=nl, user=request.user)
        if approval.approval_code == int(token):
            approval.did_see_email = True
            approval.save()
            messages.add_message(request, messages.INFO, _("Dein Approval ist nun gültig."))
        else:
            return HttpResponse("Wrong code")
    except Exception:
        return HttpResponse("Not registered")
    return HttpResponseRedirect("/accounts/view_newsletter/" + str(uuid))
