from datetime import datetime
import uuid

from django.db import models
import django.forms as forms
import django_filters.fields as filter_fields

from apps.ineedstudent.models import Hospital

from .filters import StudentJobRequirementsFilter
from .models import *  # noqa: F401, F403
from .models import COUNTRY_CODE_CHOICES


class LocationFilterModel(models.Model):

    plz = models.CharField(max_length=5, null=True)
    distance = models.IntegerField(default=0)
    countrycode = models.CharField(max_length=2, choices=COUNTRY_CODE_CHOICES, default="DE",)
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)


class StudentListFilterModel(models.Model):

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    location = LocationFilterModel

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    name = models.CharField(max_length=100)


jrf = StudentJobRequirementsFilter()


for f_name, sjr_filter in jrf.base_filters.items():

    if type(sjr_filter.field) == forms.NullBooleanField:
        StudentListFilterModel.add_to_class(
            f_name, models.NullBooleanField(default=None, null=True)
        )
    elif type(sjr_filter.field) == forms.DecimalField:
        StudentListFilterModel.add_to_class(f_name, models.IntegerField(default=0))
    elif type(sjr_filter.field) == filter_fields.ChoiceField:
        StudentListFilterModel.add_to_class(
            f_name, models.IntegerField(default=0, choices=filter.field.choices)
        )
    elif type(sjr_filter.field) == forms.DateField:
        StudentListFilterModel.add_to_class(
            f_name, models.DateField(null=True, default=datetime.now)
        )
    else:
        raise ValueError(
            "I do not know what to do with field type '%s' for '%s'" % (type(filter.field), f_name)
        )
