import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.accounts.decorator import hospital_required
from apps.iamstudent.filters import StudentJobRequirementsFilter
from apps.iamstudent.models import LocationFilterModel, Student, StudentListFilterModel
from apps.iamstudent.tables import StudentTable
from apps.mapview.utils import get_plzs_close_to, plzs

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class StudentSelectionView(View):
    def get(self, request, countrycode, plz, distance):

        # remove parameters fro mthe get request that should not be taken into account
        request_filtered = self.clean_request(request)

        # only show validated students
        qs = Student.objects.filter(user__validated_email=True, is_activated=True)

        # filter by location
        countrycode = request.GET.get("countrycode", countrycode)
        plz = request.GET.get("plz", plz)
        distance = int(request.GET.get("distance", distance))

        if countrycode not in plzs or plz not in plzs[countrycode]:
            return HttpResponse(
                "Postleitzahl: " + plz + " ist keine valide Postleitzahl in " + countrycode
            )
        lat, lon, ort = plzs[countrycode][plz]
        if distance == 0:
            close_plzs = [plz]
        else:
            close_plzs = get_plzs_close_to(countrycode, plz, distance)
        qs = qs.filter(plz__in=close_plzs, countrycode=countrycode)

        # filter by job requirements
        filter_jobrequirements = StudentJobRequirementsFilter(request_filtered, queryset=qs)
        qs = filter_jobrequirements.qs

        # displayed table
        table = StudentTable(qs, hospital=request.user.hospital)

        # disable huge amounts of email sends
        max_mails = request.user.hospital.leftover_emails_for_today()
        enable_mail_send = filter_jobrequirements.qs.count() <= max_mails

        # special display to enable the fancy java script stuff and logic
        DISPLAY_filter_jobrequirements = StudentJobRequirementsFilter(
            request_filtered, display_version=True
        )

        context = {
            "plz": plz,
            "countrycode": countrycode,
            "ort": ort,
            "distance": distance,
            "table": table,
            "filter": DISPLAY_filter_jobrequirements,
            "n": qs.count(),
            "enable_mail": enable_mail_send,
            "max": max_mails,
            "email": request.user.email,
        }

        # saving logic

        uuid = request.GET.get("uuid", "")
        save_filter = request.GET.get("saveFilter", "false")
        filter_name = request.GET.get("filterName", "")

        if save_filter == "true" and filter_name != "":

            student_attr = self.clean_request_for_saving(request_filtered)
            loc = LocationFilterModel(plz=plz, distance=distance, countrycode=countrycode)
            loc.save()
            filter_model = StudentListFilterModel(
                **student_attr, name=filter_name, hospital=request.user.hospital
            )
            filter_model.location = loc
            filter_model.save()

            context["uuid"] = filter_model.uuid
            context["filter_name"] = filter_model.name
            context["filter_is_being_saved"] = True

        elif uuid != "":
            # update saved filter
            filter_model = StudentListFilterModel.objects.get(uuid=uuid)

            # update filter
            uuid_filter = str(filter_model.uuid)
            student_attr = self.clean_request_for_saving(request_filtered)
            qs = StudentListFilterModel.objects.filter(uuid=uuid_filter)
            qs.update(**student_attr)
            from django.db.models.fields import NOT_PROVIDED

            for r in qs:
                r.save()

            # reset all fields that have not been set to default
            filter_model = StudentListFilterModel.objects.get(uuid=uuid)
            for f in filter_model._meta.fields:
                if (
                    f.name not in ["uuid", "hospital", "location", "registration_date"]
                    and f.name not in student_attr
                ):
                    if f.default != NOT_PROVIDED:
                        setattr(filter_model, f.name, f.get_default())
            filter_model.save()

            # update location
            uuid_loc = str(filter_model.location.uuid)
            qs = LocationFilterModel.objects.filter(uuid=uuid_loc)
            qs.update(plz=plz, distance=distance, countrycode=countrycode)
            for r in qs:
                r.save()

            context["filter_name"] = filter_model.name
            context["uuid"] = filter_model.uuid
            context["filter_is_being_saved"] = True
        else:
            # user does not want to save filter
            context["filter_is_being_saved"] = False

        return render(request, "student_list_view.html", context)

    def clean_request(self, request):
        keys = list(request.GET.keys())
        request_filtered = request.GET.copy()
        for k in keys:
            if k.startswith("ausbildung_typ_") and k.count("_") > 2:
                # this is a subfield with the selection notenabled this should not be in the filter
                # possibly also solvable by javascript (do not send these hidden boxes at all))
                if not "_".join(k.split("_")[:3]) in request.GET:
                    request_filtered.pop(k)
        return request_filtered

    def clean_request_for_saving(self, request):
        student_attr = dict(request)
        for i in ["plz", "distance", "countrycode", "uuid", "saveFilter", "filterName"]:
            if i in request.keys():
                student_attr.pop(i)

        for i in list(student_attr.keys()):

            if type(student_attr[i]) == list:
                student_attr[i] = student_attr[i][0]

            if student_attr[i] == "":
                student_attr.pop(i)
            elif student_attr[i] == "true":
                student_attr[i] = True
            elif student_attr[i] == "false":
                student_attr[i] = False
        return student_attr
