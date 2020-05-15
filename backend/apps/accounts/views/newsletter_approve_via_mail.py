import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView

from apps.accounts.modelss import LetterApprovedBy, Newsletter

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class ApproveNewsletterTextRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        nl = get_object_or_404(Newsletter, uuid=kwargs["uuid"])
        approval = get_object_or_404(LetterApprovedBy, newsletter=nl, user=self.request.user)
        if approval.approval_code == int(kwargs["token"]):
            approval.did_see_email = True
            approval.save()
            messages.add_message(self.request, messages.INFO, _("Dein Approval ist nun gültig."))
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                _(
                    "Der Link ist nicht mehr gültig. Versuch dir eine nochmal neue "
                    "Mail zu schicken (approve den Text nochmals)."
                ),
            )

        self.url = "/accounts/view_newsletter/" + str(kwargs["uuid"])
        return super().get_redirect_url(*args, **kwargs)
