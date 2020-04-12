from django import forms
from django.shortcuts import render
from . import models


class StudentEvaluationForm(forms.ModelForm):
    model = models.StudentEvaluation
