from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('facilities', views.facilitiesJSON, name='facilitiesJSON'),
    path('supporters', views.supportersJSON, name='supportersJSON'),
]
