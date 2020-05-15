import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import format_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView

from apps.ineedstudent.models import Hospital

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class DeleteHospitalRedirect(RedirectView):
    url = "/accounts/approve_hospitals"

    def get_redirect_url(self, *args, **kwargs):
        h = get_object_or_404(Hospital, uuid=kwargs["uuid"])
        logger.info(
            "Delete Hospital %s.", kwargs["uuid"], extra={"request": self.request},
        )
        name = h.user
        h.delete()
        text = format_lazy(_("Du hast die Institution mit user '{name}' gelöscht."), name=name)
        messages.add_message(self.request, messages.INFO, text)
        return super().get_redirect_url(*args, **kwargs)
