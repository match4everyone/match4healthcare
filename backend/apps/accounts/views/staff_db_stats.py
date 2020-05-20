import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.accounts.src.statistics import DataBaseStats

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class DBStatsView(View):
    def get(self, request):
        stats = DataBaseStats()
        return render(request, "database_stats.html", {"statistics": stats.all_stats()})
