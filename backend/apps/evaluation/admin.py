from django.contrib import admin

from .models import InstitutionEvaluation, StudentEvaluation

admin.site.register(StudentEvaluation)
admin.site.register(InstitutionEvaluation)
