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


class Student(models.Model):
    """A typical class defining a model, derived from the Model class."""

    class Bezahlung(models.IntegerChoices):
        UNENTGELTLICH = 1
        BEZAHLUNG = 4

    class Verfuegbarkeiten(models.IntegerChoices):
        TEN = 1
        TWENTY = 2
        THIRTY = 3
        FOURTY = 4

    class Ampel(models.IntegerChoices):
        ROT = 1
        GELB = 2
        GRUEN = 3

    class Umkreise(models.IntegerChoices):
        LESSFIVE = 1
        LESSTEN = 2
        LESSTWENTY = 3
        MORETWENTY = 4

    class Ausbildungen(models.IntegerChoices):
        ARZT = 1
        MEDSTUD = 2
        MFA = 3
        MTA = 4
        MTLA = 5
        NOTFALLSANI = 6
        PFLEGESTUD = 7
        SANI = 8
        ZAHNI = 9
        KINDERBETREUUNG = 10
        SONSTIGE = 11

    class Arzttyp(models.IntegerChoices):
        ANAESTHESIE = 1
        CHIRURGIE = 2
        INNERE = 3
        INTENSIV = 4
        NOTAUFNAHME = 5
        ANDERE = 6
    
    class MedstudAbschnitt(models.IntegerChoices):
        VORKLINIK = 1
        KLINIK = 2
        PJ = 3

    ## Database stuff
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


    COUNTRY_CODE_CHOICES = [
        ("DE", 'Deutschland'),
        ("AT", 'Österreich'),
    ]
    countrycode = models.CharField(
        max_length=2,
        choices=COUNTRY_CODE_CHOICES,
        default="DE",
    )
    #Allgemeines

    # vorerkrankungen
    # Berufserfahrung

    # TODO add more validators!

    # Bezahlung

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    name_first = models.CharField(max_length=50, default='')
    name_last = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=100, blank=True, default='')

    plz = models.CharField(max_length=5, null=True)
    umkreis = models.IntegerField(choices=Umkreise.choices, null=True, blank=False)
    availability_start = models.DateField(null=True)

    wunsch_ort_arzt = models.BooleanField(default=False)
    wunsch_ort_gesundheitsamt = models.BooleanField(default=False)
    wunsch_ort_krankenhaus = models.BooleanField(default=False)
    wunsch_ort_pflege = models.BooleanField(default=False)
    wunsch_ort_rettungsdienst = models.BooleanField(default=False)
    wunsch_ort_labor = models.BooleanField(default=False)

    braucht_bezahlung = models.IntegerField(choices=Bezahlung.choices, default=Bezahlung.UNENTGELTLICH) # RADIO BUTTONS IM FORM!

    zeitliche_verfuegbarkeit = models.IntegerField(choices=Verfuegbarkeiten.choices, null=True, blank=False)

    vorausbildung_typ_krankenpflege = models.BooleanField(default=False)
    vorausbildung_typ_intensiv = models.BooleanField(default=False)
    vorausbildung_typ_innere = models.BooleanField(default=False)
    vorausbildung_typ_anaesthesie = models.BooleanField(default=False)
    vorausbildung_typ_pflege = models.BooleanField(default=False)
    vorausbildung_typ_rettungsdienst = models.BooleanField(default=False)
    vorausbildung_typ_hebamme = models.BooleanField(default=False)
    vorausbildung_typ_labor = models.BooleanField(default=False)
    vorausbildung_typ_verwaltunglogistik = models.BooleanField(default=False)
    vorausbildung_typ_fsjgesundheitswesen = models.BooleanField(default=False)
    vorausbildung_typ_blutentnahmedienst = models.BooleanField(default=False)
    vorausbildung_typ_kinderbetreuung = models.BooleanField(default=False)

    ausbildung_typ = models.IntegerField(choices=Ausbildungen.choices, null=True, blank=False)
    ausbildung_typ_sonstige = models.CharField(max_length=50, default='')

    ausbildung_arzt_typ = models.IntegerField(choices=Arzttyp.choices, null=True)
    ausbildung_arzt_typ_sonstige = models.CharField(max_length=50, default='')

    ausbildung_medstud_abschnitt = models.IntegerField(choices=MedstudAbschnitt.choices, null=True)
    ausbildung_medstud_famulaturen_anaesthesie = models.BooleanField(default=False)
    ausbildung_medstud_famulaturen_chirurgie = models.BooleanField(default=False)
    ausbildung_medstud_famulaturen_innere = models.BooleanField(default=False)
    ausbildung_medstud_famulaturen_intensiv = models.BooleanField(default=False)
    ausbildung_medstud_famulaturen_notaufnahme = models.BooleanField(default=False)

    ausbildung_medstud_anerkennung_noetig = models.BooleanField(default=False)


    ### TODO: 

    # ausbildung_mfa_details
    # ausbildung_mta_details
    # ausbildung_mtla_details
    # ausbildung_notfallsani_details
    # ausbildung_pflegestud_details
    # ausbildung_sani_details
    # ausbildung_zahni_details
    # ausbildung_kindebetreuung_details
    

    # Metadata
    class Meta:
        ordering = ['plz']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user.email

    def clean(self):
        if self.plz not in plzs[self.countrycode]:
            raise ValidationError(str(self.plz) + _(" ist keine Postleitzahl in ") + self.countrycode)

import django_filters
from django import forms
from django.db import models

class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = {}
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
