from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from mapview.utils import plzs
from iamstudent.models import Student



def index(request):
    locations_and_number = prepare_students()
    template = loader.get_template('mapview/map.html')
    context = {
        'locations': list(locations_and_number.values()),
    }
    return HttpResponse(template.render(context, request))


def prepare_students():
    students = Student.objects.all()
    locations_and_number = {}
    i=0
    for student in students:
        plz = student.plz
        if plz in locations_and_number:
            locations_and_number[plz]["count"] += 1
        else:
            lat, lon, ort = plzs[plz]
            locations_and_number[plz] = {
                "plz": plz,
                "count": 1,
                "lat": lat,
                "lon": lon,
                "ort": ort,
                "i": i,
            }
            i+=1
    return locations_and_number
