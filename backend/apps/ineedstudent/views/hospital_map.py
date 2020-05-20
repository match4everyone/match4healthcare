from functools import lru_cache
import logging

from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from django.views.generic.base import TemplateView

from apps.ineedstudent.models import Hospital
from apps.mapview.src.map import plzs
from apps.mapview.views import get_ttl_hash

logger = logging.getLogger(__name__)


# Should be safe against BREACH attack because we don't have user input in reponse body
@method_decorator([gzip_page], name="dispatch")
class HospitalMapView(TemplateView):
    template_name = "map_hospitals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations_and_number = prepare_hospitals(ttl_hash=get_ttl_hash(60))
        context["locations"] = list(locations_and_number.values())
        return context


@lru_cache(maxsize=1)
def prepare_hospitals(ttl_hash=None):
    hospitals = Hospital.objects.filter(
        user__validated_email=True, is_approved=True, appears_in_map=True
    )
    locations_and_number = {}
    for hospital in hospitals:
        if len(hospital.sonstige_infos) != 0:
            cc = hospital.countrycode
            plz = hospital.plz
            key = cc + "_" + plz
            if key in locations_and_number:
                locations_and_number[key]["count"] += 1
                locations_and_number[key]["uuid"] = None
            else:
                lat, lon, ort = plzs[cc][plz]
                locations_and_number[key] = {
                    "uuid": hospital.uuid,
                    "countrycode": cc,
                    "plz": plz,
                    "count": 1,
                    "lat": lat,
                    "lon": lon,
                    "ort": ort,
                }
    return locations_and_number
