from django.db import models
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError
from mapview.utils import plzs
from django.utils.translation import gettext as _
from accounts.models import User


def validate_semester(value):
    if value < 0:
        raise ValidationError(_("Semester darf nicht negativ sein"))
    else:
        return value

def validate_plz(value):
    if value not in plzs:
        raise ValidationError(_('Dies ist keine Postleitzahl in Deutschland.'))
    else:
        return value

class Student(models.Model):
    """A typical class defining a model, derived from the Model class."""

    class Bezahlung(models.IntegerChoices):
        UNENTGELTLICH = 1
        MINIJOB = 2
        VOLLZEIT = 3

    class Ampel(models.IntegerChoices):
        ROT = 1
        GELB = 2
        GRUEN = 3

    ## Database stuff
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    #Allgemeines

    # vorerkrankungen
    # Berufserfahrung

    # Bezahlung

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    plz = models.CharField(max_length=5, null=True, validators=[validate_plz])
    email = models.EmailField(unique=True)

    semester = models.IntegerField(null=True, validators=[validate_semester])
    immatrikuliert = models.BooleanField(default=False)
    availability_start = models.DateField(null=True)

    braucht_bezahlung = models.IntegerField(choices=Bezahlung.choices, default=Bezahlung.UNENTGELTLICH)

    ba_arzt = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_krankenpflege = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_pflegehilfe = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_anaesthesiepflege = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_intensivpflege = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_ota = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_mfa = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_mta_lta = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_rta = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_rettungssanitaeter = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_kinderbetreuung = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_hebamme = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_sprechstundenhilfe = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    ba_labortechnische_assistenz = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)

    ba_famulatur = models.CharField(max_length=100,default='')
    ba_pflegepraktika = models.CharField(max_length=100,default='')
    ba_fsj_krankenhaus = models.CharField(max_length=100,default='')

    skill_coronascreening = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_pflegeunterstuetzung = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_transportdienst = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_kinderbetreuung = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_labortaetigkeiten = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_drkblutspende = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_hotline = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_abstriche = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_patientenpflege = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_patientenlagerung = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_opassistenz = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_blutentnahmedienst = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_anrufe = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_infektionsnachverfolgung = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_patientenaufnahme = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_edvkenntnisse = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_zugaengelegen = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_arztbriefeschreiben = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_blutkulturenabnehmen = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_infusionenmischen = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_ekgschreiben = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_ultraschall = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_bgas = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)
    skill_beatmungsgeraetebedienen = models.IntegerField(choices=Ampel.choices, default=Ampel.ROT)

    # Metadata
    class Meta:
        ordering = ['email']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.email

import django_filters
from django import forms
from django.db import models

class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = {
            'semester': ['lt', 'gt'],
            'ba_arzt': ['isnull']
        }
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
