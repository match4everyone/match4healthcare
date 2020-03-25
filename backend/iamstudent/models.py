from django.db import models
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError
from mapview.utils import plzs
from django.utils.translation import gettext as _
from accounts.models import User
from ineedstudent.models import Hospital

def validate_semester(value):
    if value < 0:
        raise ValidationError(_("Semester darf nicht negativ sein"))
    else:
        return value

def validate_checkbox(value):
    if value != True:
        raise ValidationError(_("You have to accept this"), code='invalid')
    else:
        return value


class Student(models.Model):

    #class Bezahlung(models.IntegerChoices):
    UNENTGELTLICH = 1
    BEZAHLUNG = 4
    BEZAHLUNG_CHOICES = (
        (UNENTGELTLICH, _('Ich freue mich über eine Vergütung, helfe aber auch ohne')),
        (BEZAHLUNG, _('Ich benötige eine Vergütung')),
    )

    #class Verfuegbarkeiten(models.IntegerChoices):
    TEN = 1
    TWENTY = 2
    THIRTY = 3
    FOURTY = 4
    VERFUEGBARKEIT_CHOICES = (
        (TEN, _('10h pro Woche')),
        (TWENTY, _('20h pro Woche')),
        (THIRTY, _('30h pro Woche')),
        (FOURTY, _('40h pro Woche')),
    )

    class Ampel(models.IntegerChoices):
        ROT = 1
        GELB = 2
        GRUEN = 3

    #class Umkreise(models.IntegerChoices):
    LESSFIVE = 1
    LESSTEN = 2
    LESSTWENTY = 3
    MORETWENTY = 4
    UMKREIS_CHOICES = (
        (LESSFIVE, _('<5 km')),
        (LESSTEN, _('<10 km')),
        (LESSTWENTY, _('<20 km')),
        (MORETWENTY, _('>20 km')),
    )

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
    # Allgemeines

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
    umkreis = models.IntegerField(choices=UMKREIS_CHOICES, null=True, blank=False)
    availability_start = models.DateField(null=True)

    braucht_bezahlung = models.IntegerField(choices=BEZAHLUNG_CHOICES,
                                            default=UNENTGELTLICH)  # RADIO BUTTONS IM FORM!

    zeitliche_verfuegbarkeit = models.IntegerField(choices=VERFUEGBARKEIT_CHOICES, null=True, blank=False)

    datenschutz_zugestimmt = models.BooleanField(default=False, validators=[validate_checkbox])
    einwilligung_datenweitergabe = models.BooleanField(default=False, validators=[validate_checkbox])

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


"""Add stufff to model"""
wunschorte = ['arzt', 'gesundheitsamt', 'krankenhaus', 'pflege', 'rettungsdienst', 'labor']
wunschorte_prefix = 'wunsch_ort'
for w in wunschorte:
    Student.add_to_class('%s_%s' % (wunschorte_prefix.lower(), w.lower()), models.BooleanField(default=False))

KEINE_ANGABE = 0
#class Arzttyp(models.IntegerChoices):
ANAESTHESIE = 1
CHIRURGIE = 2
INNERE = 3
INTENSIV = 4
NOTAUFNAHME = 5
ANDERE = 6
ARZT_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (ANAESTHESIE, _('Anästhesie')),
    (CHIRURGIE, _('Chirurgie')),
    (INNERE, _('Innere Medizin')),
    (INTENSIV, _('Intensivstation')),
    (NOTAUFNAHME, _('Notaufnahme'))
)


#class MedstudAbschnitt(models.IntegerChoices):
VORKLINIK = 1
KLINIK = 2
PJ = 3
MEDSTUD_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (VORKLINIK, _('Vorklinischer Teil (1.-5. Semester)')),
    (KLINIK, _('Klinischer Teil (6.-10. Semester)')),
    (PJ, _('Praktisches Jahr')),
)


#class ZahnstudAbschnitt(models.IntegerChoices):
VORKLINIK = 1
KLINIK = 2
ZAHNSTUD_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (VORKLINIK, _('Vorklinischer Teil')),
    (KLINIK, _('Klinischer Teil')),
)


#class MFAAbschnitt(models.IntegerChoices):
JAHR_1 = 1
JAHR_2 = 2
JAHR_3 = 3
BERUFSTAETIG = 4
MFA_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (JAHR_1, _('1. Jahr')),
    (JAHR_2, _('2. Jahr')),
    (JAHR_3, _('3. Jahr')),
    (BERUFSTAETIG, _('Berufstätig')),
)


#class NOTFALLSANIAbschnitt(models.IntegerChoices):

JAHR_1 = 1
JAHR_2 = 2
BERUFSTAETIG = 4
NOTFALLSANI_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (JAHR_1, _('1. Jahr')),
    (JAHR_2, _('2. Jahr')),
    (BERUFSTAETIG, _('Berufstätig'))
)


AUSBILDUNGS_TYPEN = {
    'ARZT':
        {
            'typ': models.IntegerField(choices=ARZT_CHOICES, default=0,null=True),
            #'sonstige': models.CharField(max_length=50, blank=True, default='')
        },
    'MEDSTUD':
        {
            'abschnitt': models.IntegerField(choices=MEDSTUD_CHOICES, null=True, default=0),
            'farmulaturen_anaesthesie': models.BooleanField(default=False),
            'famulaturen_chirurgie': models.BooleanField(default=False),
            'famulaturen_innere': models.BooleanField(default=False),
            'famulaturen_intensiv': models.BooleanField(default=False),
            'famulaturen_notaufnahme': models.BooleanField(default=False),
            'anerkennung_noetig': models.BooleanField(default=False)
        },
    'MFA':
        {
            'abschnitt': models.IntegerField(choices=MFA_CHOICES, default=0,null=True),
        },
    'MTLA':
        {
            'abschnitt': models.IntegerField(choices=MFA_CHOICES, default=0,null=True),
        },
    'MTA': {
        'abschnitt': models.IntegerField(choices=MFA_CHOICES, default=0, null=True),
    },
    'NOTFALLSANI': {
        'abschnitt': models.IntegerField(choices=NOTFALLSANI_CHOICES, default=0,null=True),
    },
    'PFLEGE' :{
        'abschnitt': models.IntegerField(choices=MFA_CHOICES, default=0, null=True),
    },
    'SANI': {

    },
    'HEBAMME': {

    },
    'FSJ': {

    },
    'ZAHNI': {
        'abschnitt': models.IntegerField(choices=ZAHNSTUD_CHOICES, default=0, null=True)
    },
    'PHYSIO':{
        'abschnitt': models.IntegerField(choices=MFA_CHOICES, default=0, null=True),
    },
    'KINDERBETREUNG': {
        'ausgebildet': models.BooleanField(default=False),
        'vorerfahrung': models.BooleanField(default=False),
    },
    'SONSTIGE': {
        'eintragen': models.CharField(max_length=200, blank=True, default='keine')
    },
}

AUSBILDUNGS_IDS = dict(zip(AUSBILDUNGS_TYPEN.keys(), range(len(AUSBILDUNGS_TYPEN))))

columns = []
for ausbildungs_typ, felder in AUSBILDUNGS_TYPEN.items():
    columns.append('ausbildung_typ_%s' % ausbildungs_typ.lower())
    Student.add_to_class('ausbildung_typ_%s' % ausbildungs_typ.lower(), models.BooleanField(default=False))
    for key, field in felder.items():
        columns.append('ausbildung_typ_%s_%s' % (ausbildungs_typ.lower(), key.lower()))
        Student.add_to_class('ausbildung_typ_%s_%s' % (ausbildungs_typ.lower(), key.lower()), field)
print("{%s:_('')}"% ": _(''),".join(["'%s'" % c for c in columns]))

"""End"""

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

class EmailToSend(models.Model):

    subject = models.CharField(max_length=200,default='')
    message = models.TextField(default='')
    was_sent = models.BooleanField(default=False)


    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
