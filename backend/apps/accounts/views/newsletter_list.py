import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.accounts.models import Newsletter
from apps.accounts.tables import NewsletterTable

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class NewsletterListView(View):
    table = NewsletterTable
    query_set = Newsletter.objects.all().order_by("-registration_date")
    template = "newsletter_list.html"

    def get(self, request):
        context = {"table": self.table(self.query_set)}
        return render(request, self.template, context)
