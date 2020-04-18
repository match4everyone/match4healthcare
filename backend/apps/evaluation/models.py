from django.db import models
from django.utils.translation import gettext_lazy as _

VERY_GOOD = 1
GOOD = 2
AVERAGE = 3
BAD = 4
VERY_BAD = 5

LIKERT_CHOICES = (
    (VERY_GOOD, _('Sehr gut')),
    (GOOD, _('Gut')),
    (AVERAGE, _('Durchschnittlich')),
    (BAD, _('Schlecht')),
    (VERY_BAD, _('Sehr schlecht')),
)


# fields common to both, institutions and students
class BaseEvaluation(models.Model):
    overall_rating = models.IntegerField(choices=LIKERT_CHOICES, default=3, blank=True, null=True)

    registration_feedback = models.TextField(default='', blank=True, null=True)
    suggested_improvements = models.TextField(default='', blank=True, null=True)

    likelihood_recommendation = models.IntegerField(choices=LIKERT_CHOICES, default=3, blank=True, null=True)

    contact_mail = models.EmailField(blank=True, null=True)


# student-specific fields
class StudentEvaluation(BaseEvaluation):

    communication_with_institutions = models.TextField(blank=True, null=True)


INSTITUTION_HOSPITAL = 'hospital'
INSTITUTION_GENERAL_PRACTICE = 'general practice'
INSTITUTION_HEALTH_AUTHORITY = 'health authority'
INSTITUTION_EMS = 'emergency medical service'
INSTITUTION_OTHER = 'other'

INSTITUTION_CHOICES = [
    (INSTITUTION_HOSPITAL, _('Krankenhaus/Spital')),
    (INSTITUTION_GENERAL_PRACTICE, _('Arztpraxis')),
    (INSTITUTION_HEALTH_AUTHORITY, _('Gesundheitsamt')),
    (INSTITUTION_EMS, _('Rettungsdienst')),
    (INSTITUTION_OTHER, _('Andere')),
]


# institution-specific fields
class InstitutionEvaluation(BaseEvaluation):

    institution_type = models.CharField(max_length=30, choices=INSTITUTION_CHOICES, default=INSTITUTION_HOSPITAL)
