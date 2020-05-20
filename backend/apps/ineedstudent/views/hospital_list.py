import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.ineedstudent.models import Hospital
from apps.ineedstudent.tables import HospitalTable
from apps.mapview.src.map import plzs

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class HospitalListView(View):
    def get(self, request, countrycode, plz):

        if countrycode not in plzs or plz not in plzs[countrycode]:
            # TODO: niceren error werfen # noqa: T003
            return HttpResponse(
                "Postleitzahl: " + plz + " ist keine valide Postleitzahl in " + countrycode
            )

        lat, lon, ort = plzs[countrycode][plz]

        table = HospitalTable(
            Hospital.objects.filter(
                user__validated_email=True, is_approved=True, plz=plz, appears_in_map=True
            )
        )
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        context = {"countrycode": countrycode, "plz": plz, "ort": ort, "table": table}

        return render(request, "list_hospitals_by_plz.html", context)
