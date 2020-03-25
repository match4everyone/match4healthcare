from django.db import models
import uuid
from datetime import datetime

from apps.accounts.models import User
from django.core.exceptions import ValidationError
from apps.mapview.utils import plzs
from django.utils.translation import gettext as _


# Create your models here.
class Hospital(models.Model):
    """A typical class defining a model, derived from the Model class."""

    ## Datenbankfeatures
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

    ## Kontaktdaten
    #email = models.EmailField(unique=True)
    sonstige_infos = models.TextField(default='')
    ansprechpartner = models.CharField(max_length=100,default='')
    telefon = models.CharField(max_length=100,default='')
    firmenname = models.CharField(max_length=100,default='')
    plz = models.CharField(max_length=5, null=True)

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    # Metadata
    class Meta:
        ordering = ['registration_date']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.uuid

    def clean(self):
        if self.plz not in plzs[self.countrycode]:
            raise ValidationError(_(str(self.plz) + " ist keine Postleitzahl in " + self.countrycode))
