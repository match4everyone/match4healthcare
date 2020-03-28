from django.db import models
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError
from apps.mapview.utils import plzs
from django.utils.translation import gettext as _
from apps.accounts.models import User
from apps.ineedstudent.models import Hospital

def validate_semester(value):
    if value < 0:
        raise ValidationError(_("Semester darf nicht negativ sein"))
    else:
        return value


def validate_checkbox(value):
    pass
    # TODO: Remove in a manner that does not brake migrations!


#class Bezahlung(models.IntegerChoices):
EGAL = 0
# todo: im form ändern zu radio
BEZAHLUNG = 1
UNENTGELTLICH = 2
BEZAHLUNG_CHOICES = (
    (UNENTGELTLICH, _('Ich freue mich über eine Vergütung, helfe aber auch ohne')),
    (BEZAHLUNG, _('Ich benötige eine Vergütung')),
)

BEZAHLUNG_CHOICES_Filter = (
    (BEZAHLUNG, _('ja')),
    (UNENTGELTLICH, _('nein')),
)


CHECKBOX_CHOICES = [
            ('unknown', _('egal')),
            ('true', _('muss')),
            #('false', _('darf nicht')),
        ]


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
LESSTEN = 1
LESSTWENTY = 2
LESSFOURTY = 3
MOREFOURTY = 4
UMKREIS_CHOICES = (
    (LESSTEN, _('<10 km')),
    (LESSTWENTY, _('<20 km')),
    (LESSFOURTY, _('<40 km')),
        (MOREFOURTY, _('>40 km')),
)



class Student(models.Model):


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
    availability_start = models.DateField(null=True,default=datetime.now)

    braucht_bezahlung = models.IntegerField(choices=BEZAHLUNG_CHOICES,
                                            default=UNENTGELTLICH)  # RADIO BUTTONS IM FORM!

    zeitliche_verfuegbarkeit = models.IntegerField(choices=VERFUEGBARKEIT_CHOICES, null=True, blank=False)

    datenschutz_zugestimmt = models.BooleanField(default=False, validators=[validate_checkbox])
    einwilligung_datenweitergabe = models.BooleanField(default=False, validators=[validate_checkbox])

    sonstige_qualifikationen = models.CharField(max_length=200, blank=True, default='keine')
    unterkunft_gewuenscht = models.BooleanField(default=False)

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

class PersistenStudentFilterModel(models.Model):

    """
    Persistent Filtering for the Student List
    """

    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)


    ausbildung_typ_medstud_famulaturen_anaesthesie = models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown')
    ausbildung_typ_medstud_famulaturen_chirurgie =models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown')
    ausbildung_typ_medstud_famulaturen_innere = models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown')
    ausbildung_typ_medstud_famulaturen_intensiv = models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown')
    ausbildung_typ_medstud_famulaturen_notaufnahme = models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown')

    ausbildung_typ_medstud_anerkennung_noetig = models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown')




"""Add stufff to model"""
wunschorte = ['arzt', 'gesundheitsamt', 'krankenhaus', 'pflege', 'rettungsdienst', 'labor', 'apotheke','ueberall']
wunschorte_prefix = 'wunsch_ort'
for w in wunschorte:
    Student.add_to_class('%s_%s' % (wunschorte_prefix.lower(), w.lower()), models.BooleanField(default=False))

#class MedstudAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
VORKLINIK = 1
KLINIK = 2
PJ = 3
ASSIST = 4
FACH = 5
MEDSTUD_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (VORKLINIK, _('Vorklinischer Teil (1.-5. Semester)')),
    (KLINIK, _('Klinischer Teil (6.-10. Semester)')),
    (PJ, _('Praktisches Jahr')),
    (ASSIST, _('Assistenzarzt')),
    (FACH,_('Facharzt'))
)


#class ZahnstudAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
VORKLINIK = 1
KLINIK = 2
ABGESCHLOSSEN = 3
ZAHNSTUD_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (VORKLINIK, _('Vorklinischer Teil')),
    (KLINIK, _('Klinischer Teil')),
    (ABGESCHLOSSEN, _('Abgeschlossen'))
)


#class MFAAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
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
KEINE_ANGABE = 0
JAHR_1 = 1
JAHR_2 = 2
BERUFSTAETIG = 4
NOTFALLSANI_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (JAHR_1, _('1. Jahr')),
    (JAHR_2, _('2. Jahr')),
    (BERUFSTAETIG, _('Berufstätig'))
)
KEINE_ANGABE = 0
ERFAHR = 1
AUSBID_ABGESCHLOSSEN = 2
BETREU_CHOICES = (
    (KEINE_ANGABE, _('Keine Angabe')),
    (ERFAHR, _('Lediglich Erfahrungen')),
    (AUSBID_ABGESCHLOSSEN, _('Abgeschlossene Ausbildung'))
)


AUSBILDUNGS_TYPEN = {
    'MEDSTUD':
        {
            'abschnitt': (models.IntegerField, {'choices':MEDSTUD_CHOICES, 'default':KEINE_ANGABE,'null':True}),

            'famulaturen_anaesthesie': (models.BooleanField,{'default':False}),
            'famulaturen_chirurgie': (models.BooleanField,{'default':False}),
            'famulaturen_innere': (models.BooleanField,{'default':False}),
            'famulaturen_intensiv': (models.BooleanField,{'default':False}),
            'famulaturen_notaufnahme': (models.BooleanField,{'default':False}),
            'empty_3': None,
            'anerkennung_noetig':(models.BooleanField,{'default':False})
        },
    'MFA':
        {
            'abschnitt': (models.IntegerField, {'choices':MFA_CHOICES, 'default':0,'null':True}),
        },
    'MTLA':
        {
            'abschnitt': (models.IntegerField, {'choices':MFA_CHOICES, 'default':0,'null':True}),
        },
    'MTA': {
        'abschnitt': (models.IntegerField, {'choices':MFA_CHOICES, 'default':0,'null':True}),
    },
    'NOTFALLSANI': {
        'abschnitt': (models.IntegerField, {'choices':NOTFALLSANI_CHOICES, 'default':0,'null':True}),
    },
    'PFLEGE' :{
        'abschnitt':(models.IntegerField, {'choices':MFA_CHOICES, 'default':0,'null':True}),
    },
    'SANI': {

    },
    'HEBAMME': {

    },
    'FSJ': {

    },
    'ZAHNI': {
        'abschnitt': (models.IntegerField, {'choices':ZAHNSTUD_CHOICES, 'default':0,'null':True}),
    },
    'PHYSIO':{
        'abschnitt': (models.IntegerField, {'choices':MFA_CHOICES, 'default':0,'null':True}),
    },
    'KINDERBETREUNG': {
        'ausgebildet_abschnitt': (models.IntegerField, {'choices':BETREU_CHOICES, 'default':0,'null':True}),
    }
}

AUSBILDUNGS_IDS = dict(zip(AUSBILDUNGS_TYPEN.keys(), range(len(AUSBILDUNGS_TYPEN))))

AUSBILDUNGS_DETAIL_COLUMNS = []
for ausbildungs_typ, felder in AUSBILDUNGS_TYPEN.items():

    # types
    a_typ = 'ausbildung_typ_%s' % ausbildungs_typ.lower()
    Student.add_to_class(a_typ, models.BooleanField(default=False))
    PersistenStudentFilterModel.add_to_class(a_typ, models.CharField(max_length=10,choices=CHECKBOX_CHOICES,default='unknown'))

    for key, field in felder.items():
        if 'empty' in key:
            continue
        a_typ_kind = 'ausbildung_typ_%s_%s' % (ausbildungs_typ.lower(), key.lower())
        AUSBILDUNGS_DETAIL_COLUMNS.append(a_typ_kind)
        Student.add_to_class(a_typ_kind, field[0](**field[1]))
        # todo: switch type
        if 'abschnitt' == key:
            PersistenStudentFilterModel.add_to_class('%s_lt' % a_typ_kind ,field[0](**field[1]))#models.IntegerField(choices=ZAHNSTUD_CHOICES, default=0, null=True) )
            PersistenStudentFilterModel.add_to_class('%s_gt' % a_typ_kind ,field[0](**field[1]))#models.IntegerField(choices=ZAHNSTUD_CHOICES, default=0, null=True) )
        elif 'famulatu' in a_typ_kind or 'noetig' in a_typ_kind:
            pass
        else:
            PersistenStudentFilterModel.add_to_class(a_typ_kind, field[0](**field[1]))

# Generate Fields for translation
# print("{%s:_('')}"% ": _(''),".join(["'%s'" % c for c in columns]))

AUSBILDUNGS_TYPEN_COLUMNS = ['ausbildung_typ_%s' % ausbildungs_typ.lower() for ausbildungs_typ in AUSBILDUNGS_TYPEN]





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
