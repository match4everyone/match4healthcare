import logging

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from apps.accounts.decorator import hospital_required

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class EmailToStudentSuccessView(TemplateView):

    template_name = "emails_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["not_registered"] = not self.request.user.hospital.is_approved
        return context
