import matplotlib
import matplotlib.pyplot as plt
import mpld3
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .db_stats import DataBaseStats

matplotlib.use("agg")


@login_required
@staff_member_required
def view_statistics(request):
    stats = DataBaseStats()
    fig, ax = plt.subplots()
    ax.plot([3, 1, 4, 1, 5], "ks-", mec="w", mew=5, ms=20)
    fig_html = mpld3.fig_to_html(fig)
    return render(
        request, "database_stats.html", {"statistics": stats.all_stats(), "figures": [fig_html]}
    )
