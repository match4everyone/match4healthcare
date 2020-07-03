from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import mpld3

from .db_stats import DataBaseStats

matplotlib.use("agg")


@login_required
@staff_member_required
def view_statistics(request):
    stats = DataBaseStats(length_history_days=14)

    count_stats = stats.all_stats()
    graphs = stats.all_graphs()

    stats_with_plot = []
    for name, history in graphs:
        (x, y) = history
        fig, ax = plt.subplots()
        ax.plot(x, y, "ks-", mec="w", mew=5, ms=17)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title(name)
        fig_html = mpld3.fig_to_html(fig)
        stats_with_plot.append((name, fig_html))

    return render(
        request, "database_stats.html", {"count_statistics": count_stats, "graphs": stats_with_plot}
    )
