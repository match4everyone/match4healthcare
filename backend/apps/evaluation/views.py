from django.shortcuts import render
from .forms import StudentEvaluationForm, InstitutionEvaluationForm
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse, path


def student_evaluation(request):
    if request.method == 'POST':
        form_info = StudentEvaluationForm(request.POST)

        if form_info.is_valid():
            form_info.save()
            request.session['eval_completed'] = True
            request.session['eval_completed_referer'] = 'student'
            return HttpResponseRedirect(reverse('evaluation_completed'))

    else:
        form_info = StudentEvaluationForm(initial={})

    form_info.helper.form_tag = False
    return render(request, 'evaluation/studentevaluation_form.html', {'form_info': form_info})


def institution_evaluation(request):

    if request.method == 'POST':
        form_info = InstitutionEvaluationForm(request.POST)

        if form_info.is_valid():
            form_info.save()
            request.session['eval_completed'] = True
            request.session['eval_completed_referer'] = 'institution'
            return HttpResponseRedirect(reverse('evaluation_completed'))

    else:
        form_info = InstitutionEvaluationForm(initial={})

    form_info.helper.form_tag = False
    return render(request, 'evaluation/institutionevaluation_form.html', {'form_info': form_info})


def evaluation_completed(request):

    if request.session.get('eval_completed', False):
        del request.session['eval_completed']
        return render(request, 'evaluation/evaluation_completed.html')

    return HttpResponseRedirect('/')
