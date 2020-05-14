import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.ineedstudent.models import Hospital
from apps.ineedstudent.views import ApprovalHospitalTable

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class ApproveHospitalsView(View):
    template_name = "approve_hospitals.html"

    def get(self, request):
        table_approved = ApprovalHospitalTable(Hospital.objects.filter(is_approved=True))
        table_approved.prefix = "approved"
        table_approved.paginate(page=request.GET.get(table_approved.prefix + "page", 1), per_page=5)

        table_unapproved = ApprovalHospitalTable(Hospital.objects.filter(is_approved=False))
        table_unapproved.prefix = "unapproved"
        table_unapproved.paginate(
            page=request.GET.get(table_unapproved.prefix + "page", 1), per_page=5
        )

        return render(
            request,
            "approve_hospitals.html",
            {"table_approved": table_approved, "table_unapproved": table_unapproved},
        )
