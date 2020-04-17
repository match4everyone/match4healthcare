from django.views.generic import CreateView
from django.shortcuts import render
from . import models


class StudentEvaluationForm(CreateView):

    model = models.StudentEvaluation
    fields = '__all__'
