import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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
    stats_with_plot = []
    for name, count, history in stats.all_stats():
        if not history == (None, None):
            (x, y) = history
            fig, ax = plt.subplots()
            ax.plot(x, y, "ks-", mec="w", mew=5, ms=17)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_title(name)
            fig_html = mpld3.fig_to_html(fig)
            stats_with_plot.append((name, count, fig_html))
        else:
            stats_with_plot.append((name, count, None))
    return render(request, "database_stats.html", {"statistics": stats_with_plot})
