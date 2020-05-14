import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class StaffProfileView(TemplateView):
    template_name = "staff_profile.html"
