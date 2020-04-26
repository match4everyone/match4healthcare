from django.views.generic import CreateView
from django.shortcuts import render
from . import models
from .forms import StudentEvaluationForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def student_evaluation(request):
    if request.method == 'POST':
        form_info = StudentEvaluationForm(request.POST)

        if form_info.is_valid():
            form_info.save()
            return HttpResponseRedirect(reverse('evaluation_completed'))

    else:
        form_info = StudentEvaluationForm()
        context = {
            'form_info': form_info,
        }
    form_info.helper.form_tag = False
    return render(request, 'evaluation/studentevaluation_form.html', context)


def evaluation_completed(request):
    return render(request, 'evaluation/evaluation_completed.html')
