from datetime import datetime
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.ineedstudent.models import Hospital
from apps.mapview.utils import plzs


def validate_semester(value):
    if value < 0:
        raise ValidationError(_("Semester darf nicht negativ sein"))
    else:
        return value


def validate_checkbox(value):
    pass
    # TODO: Remove in a manner that does not brake migrations!!! # noqa: T003


# class Bezahlung(models.IntegerChoices):
EGAL = 0
# TODO: im form ändern zu radio # noqa: T003
BEZAHLUNG = 1
UNENTGELTLICH = 2
DARF_NICHT_BEZAHLT_WERDEN = 3
BEZAHLUNG_CHOICES = (
    (UNENTGELTLICH, _("Ich freue mich über eine Vergütung, helfe aber auch ohne")),
    (BEZAHLUNG, _("Ich benötige eine Vergütung")),
    (DARF_NICHT_BEZAHLT_WERDEN, _("Ich möchte ohne Bezahlung helfen")),
)

NUR_BEZAHLUNG = 1
NUR_UNENTGELTLICH = 2
BEZAHLUNG_CHOICES_Filter = (
    (NUR_BEZAHLUNG, _("Helfende müssen eine Vergütung annehmen.")),
    (NUR_UNENTGELTLICH, _("Wir können keine Vergütung anbieten.")),
)


CHECKBOX_CHOICES = [
    ("unknown", _("egal")),
    ("true", _("muss")),
    # ('false', _('darf nicht')),
]


# class Verfuegbarkeiten(models.IntegerChoices):
TEN = 1
TWENTY = 2
THIRTY = 3
FOURTY = 4
VERFUEGBARKEIT_CHOICES = (
    (TEN, _("10h pro Woche")),
    (TWENTY, _("20h pro Woche")),
    (THIRTY, _("30h pro Woche")),
    (FOURTY, _("40h pro Woche")),
)


class Ampel(models.IntegerChoices):
    ROT = 1
    GELB = 2
    GRUEN = 3


# class Umkreise(models.IntegerChoices):
LESSTEN = 1
LESSTWENTY = 2
LESSFOURTY = 3
MOREFOURTY = 4
UMKREIS_CHOICES = (
    (LESSTEN, _("<10 km")),
    (LESSTWENTY, _("<20 km")),
    (LESSFOURTY, _("<40 km")),
    (MOREFOURTY, _(">40 km")),
)
COUNTRY_CODE_CHOICES = [
    ("DE", _("Deutschland")),
    ("AT", _("Österreich")),
]


class Student(models.Model):

    # Database stuff
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    countrycode = models.CharField(max_length=2, choices=COUNTRY_CODE_CHOICES, default="DE",)
    # Allgemeines

    # vorerkrankungen
    # Berufserfahrung

    # TODO: add more validators! # noqa: T003

    # Bezahlung

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    name_first = models.CharField(max_length=50, default="")
    name_last = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=100, blank=True, default="")

    plz = models.CharField(max_length=5, null=True)
    umkreis = models.IntegerField(choices=UMKREIS_CHOICES, null=True, blank=False)
    availability_start = models.DateField(null=True, default=datetime.now)

    braucht_bezahlung = models.IntegerField(
        choices=BEZAHLUNG_CHOICES, default=UNENTGELTLICH
    )  # RADIO BUTTONS IM FORM!

    zeitliche_verfuegbarkeit = models.IntegerField(
        choices=VERFUEGBARKEIT_CHOICES, null=True, blank=False
    )

    datenschutz_zugestimmt = models.BooleanField(default=False, validators=[validate_checkbox])
    einwilligung_datenweitergabe = models.BooleanField(
        default=False, validators=[validate_checkbox]
    )
    einwilligung_agb = models.BooleanField(default=False, validators=[validate_checkbox])

    sonstige_qualifikationen = models.CharField(max_length=200, blank=True, default="keine")
    unterkunft_gewuenscht = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)

    # Metadata
    class Meta:
        ordering = ["plz"]

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""  # noqa: D401
        return self.user.email

    def clean(self):
        if self.plz not in plzs[self.countrycode]:
            raise ValidationError(
                str(self.plz) + str(_(" ist keine Postleitzahl in ")) + self.countrycode
            )


"""Add stufff to model"""
wunschorte = [
    "arzt",
    "gesundheitsamt",
    "krankenhaus",
    "pflege",
    "rettungsdienst",
    "labor",
    "apotheke",
    "ueberall",
]
wunschorte_prefix = "wunsch_ort"
for w in wunschorte:
    Student.add_to_class(
        "%s_%s" % (wunschorte_prefix.lower(), w.lower()), models.BooleanField(default=False),
    )

# class MedstudAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
VORKLINIK = 1
KLINIK = 2
PJ = 3
ASSIST = 4
FACH = 5
MEDSTUD_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (VORKLINIK, _("Vorklinischer Teil")),
    (KLINIK, _("Klinischer Teil")),
    (PJ, _("Praktisches Jahr")),
    (ASSIST, _("Assistenzarzt")),
    (FACH, _("Facharzt")),
)


# class ZahnstudAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
VORKLINIK = 1
KLINIK = 2
ABGESCHLOSSEN = 3
ZAHNSTUD_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (VORKLINIK, _("Vorklinischer Teil")),
    (KLINIK, _("Klinischer Teil")),
    (ABGESCHLOSSEN, _("Abgeschlossen")),
)


# class MFAAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
JAHR_1 = 1
JAHR_2 = 2
JAHR_3 = 3
BERUFSTAETIG = 4
MFA_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (JAHR_1, _("1. Jahr")),
    (JAHR_2, _("2. Jahr")),
    (JAHR_3, _("3. Jahr")),
    (BERUFSTAETIG, _("Berufstätig")),
)

# class Ergotherapieauszubildende*r(models.IntegerChoices):
KEINE_ANGABE = 0
IN_AUSBILDUNG = 1
BERUFSTAETIG = 2
ERGOTHERAPIE_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (IN_AUSBILDUNG, _("In Ausbildung")),
    (BERUFSTAETIG, _("Berufstätig")),
)


# class Psychologie/Psychotherapeut(models.IntegerChoices):
KEINE_ANGABE = 0
STUDIUM = 1
IN_AUSBILDUNG = 2
BERUFSTAETIG = 3
PSYCHO_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (STUDIUM, _("Studium")),
    (IN_AUSBILDUNG, _("In Ausbildung")),
    (BERUFSTAETIG, _("Berufstätig")),
)


# class NOTFALLSANIAbschnitt(models.IntegerChoices):
KEINE_ANGABE = 0
JAHR_1 = 1
JAHR_2 = 2
BERUFSTAETIG = 4
NOTFALLSANI_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (JAHR_1, _("1. Jahr")),
    (JAHR_2, _("2. Jahr")),
    (BERUFSTAETIG, _("Berufstätig")),
)
KEINE_ANGABE = 0
ERFAHR = 1
AUSBID_ABGESCHLOSSEN = 2
BETREU_CHOICES = (
    (KEINE_ANGABE, _("Keine Angabe")),
    (ERFAHR, _("Lediglich Erfahrungen")),
    (AUSBID_ABGESCHLOSSEN, _("Abgeschlossene Ausbildung")),
)


AUSBILDUNGS_TYPEN = {
    "MEDSTUD": {
        "abschnitt": (
            models.IntegerField,
            {"choices": MEDSTUD_CHOICES, "default": KEINE_ANGABE, "null": True},
        ),
        "famulaturen_anaesthesie": (models.BooleanField, {"default": False}),
        "famulaturen_chirurgie": (models.BooleanField, {"default": False}),
        "famulaturen_innere": (models.BooleanField, {"default": False}),
        "famulaturen_intensiv": (models.BooleanField, {"default": False}),
        "famulaturen_notaufnahme": (models.BooleanField, {"default": False}),
        "famulaturen_allgemeinmedizin": (models.BooleanField, {"default": False}),
        "empty_3": None,
        "anerkennung_noetig": (models.BooleanField, {"default": False}),
    },
    "MFA": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "MTLA": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "MTA": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "OTA": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "ATA": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "NOTFALLSANI": {
        "abschnitt": (
            models.IntegerField,
            {"choices": NOTFALLSANI_CHOICES, "default": 0, "null": True},
        ),
    },
    "PFLEGE": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "ERGOTHERAPIE": {
        "abschnitt": (
            models.IntegerField,
            {"choices": ERGOTHERAPIE_CHOICES, "default": 0, "null": True},
        ),
    },
    "PSYCHO": {
        "abschnitt": (
            models.IntegerField,
            {"choices": PSYCHO_CHOICES, "default": 0, "null": True},
        ),
    },
    "SANI": {},
    "HEBAMME": {},
    "FSJ": {},
    "ZAHNI": {
        "abschnitt": (
            models.IntegerField,
            {"choices": ZAHNSTUD_CHOICES, "default": 0, "null": True},
        ),
    },
    "PHYSIO": {
        "abschnitt": (models.IntegerField, {"choices": MFA_CHOICES, "default": 0, "null": True},),
    },
    "KINDERBETREUNG": {
        "ausgebildet_abschnitt": (
            models.IntegerField,
            {"choices": BETREU_CHOICES, "default": 0, "null": True},
        ),
    },
}

AUSBILDUNGS_IDS = dict(zip(AUSBILDUNGS_TYPEN.keys(), range(len(AUSBILDUNGS_TYPEN))))

AUSBILDUNGS_DETAIL_COLUMNS = []
for ausbildungs_typ, felder in AUSBILDUNGS_TYPEN.items():

    # types
    a_typ = "ausbildung_typ_%s" % ausbildungs_typ.lower()
    Student.add_to_class(a_typ, models.BooleanField(default=False))

    for key, field in felder.items():
        if "empty" in key:
            continue
        a_typ_kind = "ausbildung_typ_%s_%s" % (ausbildungs_typ.lower(), key.lower())
        AUSBILDUNGS_DETAIL_COLUMNS.append(a_typ_kind)
        Student.add_to_class(a_typ_kind, field[0](**field[1]))

# Generate Fields for translation
# print("{%s:_('')}"% ": _(''),".join(["'%s'" % c for c in columns]))

AUSBILDUNGS_TYPEN_COLUMNS = [
    "ausbildung_typ_%s" % ausbildungs_typ.lower() for ausbildungs_typ in AUSBILDUNGS_TYPEN
]


class EmailGroup(models.Model):
    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="", max_length=10000)
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)


# emails that hospitals send to students
class EmailToSend(models.Model):

    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="", max_length=10000)
    was_sent = models.BooleanField(default=False)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    send_date = models.DateTimeField(null=True)

    email_group = models.ForeignKey(EmailGroup, on_delete=models.CASCADE, null=True, blank=True)


# emails that students send to hospitals
class EmailToHospital(models.Model):

    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="", max_length=10000)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    send_date = models.DateTimeField(null=True)
