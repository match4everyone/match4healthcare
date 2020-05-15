from datetime import datetime
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView

from apps.iamstudent.views import send_mails_for
from apps.ineedstudent.models import Hospital

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class ChangeHospitalApprovalRedirect(RedirectView):
    url = "/accounts/approve_hospitals"

    def get_redirect_url(self, *args, **kwargs):
        h = get_object_or_404(Hospital, uuid=kwargs["uuid"])
        h = Hospital.objects.get(uuid=kwargs["uuid"])
        logger.info(
            "Set Hospital %s approval to %s",
            kwargs["uuid"],
            (not h.is_approved),
            extra={"request": self.request},
        )

        if not h.is_approved:
            h.is_approved = True
            h.approval_date = datetime.now()
            h.approved_by = self.request.user
        else:
            h.is_approved = False
            h.approval_date = None
            h.approved_by = None
        h.save()

        if h.is_approved:
            send_mails_for(h)
        return super().get_redirect_url(*args, **kwargs)
