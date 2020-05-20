from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.gzip import gzip_page

from apps.mapview.src.map import get_ttl_hash, prepare_students


# Should be safe against BREACH attack because we don't have user input in reponse body
@gzip_page
def index(request):
    locations_and_number = prepare_students(ttl_hash=get_ttl_hash())
    template = loader.get_template("mapview/map.html")
    context = {
        "locations": list(locations_and_number.values()),
        "mapbox_token": settings.MAPBOX_TOKEN,
    }
    return HttpResponse(template.render(context, request))
