from django.shortcuts import render
from django.template import loader
from iamstudent.models import Student
from django.http import HttpResponse

from mapview.utils import plzs
from iamstudent.models import Student, StudentFilter
from ineedstudent.models import Hospital
from ineedstudent.forms import HospitalForm

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from mapview.utils import plzs, get_plzs_close_to
import django_tables2 as tables
from django_tables2 import TemplateColumn

from django.http import HttpResponse, HttpResponseRedirect

from django.utils.translation import gettext as _

from functools import lru_cache
import time
from mapview.views import get_ttl_hash
from django.views.decorators.gzip import gzip_page


# Create your views here.

def list_by_plz(request, countrycode, plz, distance):
    template = loader.get_template('list_by_plz.html')

    if countrycode not in plzs or plz not in plzs[countrycode]:
        # TODO: niceren error werfen
        return HttpResponse(_("Postleitzahl: ") + plz + _(" ist keine valide Postleitzahl in ") + countrycode)

    lat, lon, ort = plzs[countrycode][plz]

    # TODO Consult with others how this should behave!
    if distance==0:
        f = StudentFilter(request.GET, queryset=Student.objects.filter(plz=plz, countrycode=countrycode))
    else:
        close_plzs = get_plzs_close_to(countrycode, plz, distance)
        f = StudentFilter(request.GET, queryset=Student.objects.filter(plz__in=close_plzs, countrycode=countrycode))

    context = {
        'plz': plz,
        'countrycode': countrycode,
        'ort': ort,
        'distance': distance,
        'filter': f,
    }

    return HttpResponse(template.render(context, request))


def hospital_registration(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HospitalForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return render(request, 'thanks_hospital.html')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = HospitalForm()

    return render(request, 'hospital.html', {'form': form})




# Should be safe against BREACH attack because we don't have user input in reponse body
@gzip_page
def hospital_overview(request):
    locations_and_number = prepare_hospitals(ttl_hash=get_ttl_hash(60))
    template = loader.get_template('map_hospitals.html')
    context = {
        'locations': list(locations_and_number.values()),
    }
    return HttpResponse(template.render(context, request))


@lru_cache()
def prepare_hospitals(ttl_hash=None):
    students = Hospital.objects.all()
    locations_and_number = {}
    for student in students:
        cc = student.countrycode
        plz = student.plz
        key = cc + "_" + plz
        if key in locations_and_number:
            locations_and_number[key]["count"] += 1
        else:
            lat, lon, ort = plzs[cc][plz]
            locations_and_number[key] = {
                "countrycode": cc,
                "plz": plz,
                "count": 1,
                "lat": lat,
                "lon": lon,
                "ort": ort
            }
    return locations_and_number


def hospital_list(request, countrycode, plz):

    if countrycode not in plzs or plz not in plzs[countrycode]:
        # TODO: niceren error werfen
        return HttpResponse(_("Postleitzahl: ") + plz + _(" ist keine valide Postleitzahl in ") + countrycode)
        
    lat, lon, ort = plzs[countrycode][plz]

    table = HospitalTable(Hospital.objects.filter(plz=plz))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    context = {
        'countrycode': countrycode,
        'plz': plz,
        'ort': ort,
        'table': table}

    return render(request, "list_hospitals_by_plz.html", context)


class HospitalTable(tables.Table):
    info = TemplateColumn(template_name='info_button.html')

    class Meta:
        model = Hospital
        template_name = "django_tables2/bootstrap4.html"
        fields = ['firmenname','ansprechpartner','telefon','plz']
        exclude = ['uuid','registration_date','id']

def hospital_view(request,uuid):
    h = Hospital.objects.filter(uuid=uuid)[0]
    return render(request, 'hospital_view.html', {'hospital': h})
