import logging

from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from apps.accounts.decorator import hospital_required
from apps.ineedstudent.tables import ContactedTable

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class HospitalDashboardView(TemplateView):

    template_name = "hospital_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # tabelle kontaktierter Studis
        values = ["student", "registration_date", "message", "subject"]
        qs = self.request.user.hospital.emailtosend_set.all().values(
            *values, is_activated=models.F("student__is_activated")
        )
        kontaktiert_table = ContactedTable(qs)

        context["already_contacted"] = len(qs) > 0
        context["has_posting"] = self.request.user.hospital.appears_in_map
        context["posting_text"] = self.request.user.hospital.sonstige_infos
        context["kontaktiert_table"] = kontaktiert_table
