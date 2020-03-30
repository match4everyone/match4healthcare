from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from apps.mapview.utils import plzs
from apps.iamstudent.models import Student
from apps.ineedstudent.models import Hospital
from apps.ineedstudent.forms import HospitalForm

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from apps.mapview.utils import plzs, get_plzs_close_to
import django_tables2 as tables
from django_tables2 import TemplateColumn

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorator import student_required, hospital_required
from django.contrib.admin.views.decorators import staff_member_required

from functools import lru_cache
from apps.mapview.views import get_ttl_hash
import time
from apps.accounts.utils import send_password_set_email
from apps.ineedstudent.forms import HospitalFormZustimmung
from django.views.decorators.gzip import gzip_page


class StudentTable(tables.Table):
    info = TemplateColumn(template_name='info_button.html')
    checkbox = TemplateColumn(template_name='checkbox_studenttable.html')

    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        exclude = ['uuid','registration_date','id']
        fields = ['user']


# Should be safe against BREACH attack because we don't have user input in reponse body
@gzip_page
def hospital_overview(request):
    locations_and_number = prepare_hospitals(ttl_hash=get_ttl_hash(60))
    template = loader.get_template('map_hospitals.html')
    context = {
        'locations': list(locations_and_number.values()),
    }
    return HttpResponse(template.render(context, request))

@lru_cache(maxsize=1)
def prepare_hospitals(ttl_hash=None):
    hospitals = Hospital.objects.filter(user__validated_email=True, is_approved=True, appears_in_map=True)
    locations_and_number = {}
    for hospital in hospitals:
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
                "ort": ort
            }
    return locations_and_number

@login_required
def hospital_list(request, countrycode, plz):

    if countrycode not in plzs or plz not in plzs[countrycode]:
        # TODO: niceren error werfen
        return HttpResponse("Postleitzahl: " + plz + " ist keine valide Postleitzahl in " + countrycode)

    lat, lon, ort = plzs[countrycode][plz]

    table = HospitalTable(Hospital.objects.filter(user__validated_email=True, is_approved=True, plz=plz))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    context = {
        'countrycode': countrycode,
        'plz': plz,
        'ort': ort,
        'table': table}

    return render(request, "list_hospitals_by_plz.html", context)

@login_required
@hospital_required
def zustimmung(request):
    user = request.user
    h = Hospital.objects.get(user=user)
    if request.method == 'POST':
        form_info = HospitalFormZustimmung(request.POST, instance=h)

        if form_info.is_valid():
            h.save()
            return HttpResponseRedirect("/accounts/login_redirect")

    else:
        form_info = HospitalFormZustimmung()
    return render(request, 'zustimmung.html', {'form_info': form_info })

class HospitalTable(tables.Table):
    info = TemplateColumn(template_name='info_button.html')

    class Meta:
        model = Hospital
        template_name = "django_tables2/bootstrap4.html"
        fields = ['firmenname','ansprechpartner','telefon','plz']
        exclude = ['uuid','registration_date','id']

class ApprovalHospitalTable(HospitalTable):
    info = TemplateColumn(template_name='info_button.html')
    status = TemplateColumn(template_name='approval_button.html')
    delete = TemplateColumn(template_name='delete_button.html')
    class Meta:
        model = Hospital
        template_name = "django_tables2/bootstrap4.html"
        fields = ['firmenname','ansprechpartner','user','telefon','plz','user__validated_email']
        exclude = ['uuid','registration_date','id']

@login_required
def hospital_view(request,uuid):
    h = Hospital.objects.filter(uuid=uuid)[0]

    lat1, lon1, ort1 = plzs[h.countrycode][h.plz]
    context = {
        'hospital': h,
        'uuid': h.uuid,
        'ort': ort1,
    }
    if request.user.is_student:
        s = Student.objects.get(user=request.user)
        lat2, lon2, context["student_ort"] = plzs[s.countrycode][s.plz]
        context["distance"] = int(haversine(lon1, lat1, lon2, lat2))
        context["plz_student"] = s.plz
    return render(request, 'hospital_view.html', context)
