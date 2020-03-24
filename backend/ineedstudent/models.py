from django.db import models
import uuid
from datetime import datetime
from iamstudent.models import validate_plz
from accounts.models import User

# Create your models here.
class Hospital(models.Model):
    """A typical class defining a model, derived from the Model class."""

    ## Datenbankfeatures
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    ## Kontaktdaten
    email = models.EmailField(unique=True)
    sonstige_infos = models.TextField(default='')
    ansprechpartner = models.CharField(max_length=100,default='')
    telefon = models.CharField(max_length=100,default='')
    firmenname = models.CharField(max_length=100,default='')
    plz = models.CharField(max_length=5, null=True, validators=[validate_plz])

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ['email']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.email
"""
class JobRequirement(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    hospital = models.CharField(max_length=100, blank=True)


    muss_krankenpflege = models.BooleanField(default=False)

    class Meta:
        ordering = ['uuid']
        
"""