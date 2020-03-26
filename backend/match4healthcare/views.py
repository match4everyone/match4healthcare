from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home(request):
    context = {}
    template = loader.get_template('home.html')

    return HttpResponse(template.render(context, request))

def about(request):

    context = {}
    template = loader.get_template('about.html')

    return HttpResponse(template.render(context, request))

def impressum(request):
    context = {}
    template = loader.get_template('impressum.html')

    return HttpResponse(template.render(context, request))

def dataprotection(request):
    context = {}
    template = loader.get_template('dataprotection.html')

    return HttpResponse(template.render(context, request))
