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


# Create your views here.

def list_by_plz(request, plz, distance):
    template = loader.get_template('list_by_plz.html')

    lat, lon, ort = plzs[plz]

    if distance==0:
        f = StudentFilter(request.GET, queryset=Student.objects.filter(plz=plz))
    else:
        close_plzs = get_plzs_close_to(plz, distance)
        f = StudentFilter(request.GET, queryset=Student.objects.filter(plz__in=close_plzs))

    context = {
        'plz': plz,
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





def hospital_overview(request):
    locations_and_number = prepare_students()
    template = loader.get_template('map_hospitals.html')
    context = {
        'locations': list(locations_and_number.values()),
    }
    return HttpResponse(template.render(context, request))


def prepare_students():
    students = Hospital.objects.all()
    locations_and_number = {}
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
                "ort": ort
            }
    return locations_and_number


def hospital_list(request, plz):
    lat, lon, ort = plzs[plz]

    table = HospitalTable(Hospital.objects.filter(plz=plz))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    context = {
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
