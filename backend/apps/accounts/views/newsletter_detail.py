import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.text import format_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import View

from apps.accounts.forms import NewsletterEditForm, NewsletterViewForm, TestMailForm
from apps.accounts.modelss import LetterApprovedBy, Newsletter, NewsletterState

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class NewsletterDetailView(View):
    def post(self, request, uuid):
        nl = Newsletter.objects.get(uuid=uuid)

        form, nl = self.switch_newsletter(nl, request.user, request, post=request.POST, get=None)
        return self.rendered_form(request, uuid, form, nl)

    def get(self, request, uuid):
        nl = Newsletter.objects.get(uuid=uuid)

        if "email" in request.GET:
            email = request.GET.get("email")
            nl.send_testmail_to(email)
            messages.add_message(
                request, messages.INFO, _("Eine Test Email wurde an %s versendet." % email)
            )

        form, nl = self.switch_newsletter(nl, request.user, request, post=None, get=request.GET)

        return self.rendered_form(request, uuid, form, nl)

    def rendered_form(self, request, uuid, form, nl):
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

    def switch_newsletter(self, nl, user, request, post=None, get=None):
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
                    return self.switch_newsletter(nl, user, request, post=None, get=None)

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
                    return self.switch_newsletter(nl, user, request, post=None, get=None)
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
                    return self.switch_newsletter(nl, user, request, post=None, get=None)
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
                    self.switch_newsletter(nl, user, request, post=None, get=None)

            form = NewsletterViewForm(instance=nl)

        elif nl_state == NewsletterState.READY_TO_SEND:
            if get is not None:
                if "sendNewsletter" in get:
                    nl.send(user)
                    nl.save()
                    messages.add_message(
                        request, messages.INFO, _("Der Newsletter wurde versendet.")
                    )
                    self.switch_newsletter(nl, user, request)
                if "unFreezeNewsletter" in get:
                    nl.unfreeze()
                    nl.save()
                    messages.add_message(
                        request, messages.INFO, _("Der Newsletter kann wieder bearbeitet werden."),
                    )
                    return self.switch_newsletter(nl, user, request, post=None, get=None)

            form = NewsletterViewForm(instance=nl)

        elif nl_state == NewsletterState.SENT:
            form = NewsletterViewForm(instance=nl)
        else:
            raise Http404

        return form, nl
