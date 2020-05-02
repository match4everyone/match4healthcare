from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .db_stats import DataBaseStats

@login_required
@staff_member_required
def view_statistics(request):
    stats = DataBaseStats()
    return render(request, 'database_stats.html', {'statistics': stats.all_stats()})