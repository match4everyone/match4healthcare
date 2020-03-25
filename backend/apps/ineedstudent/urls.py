from django.urls import path

from . import views

urlpatterns = [
    path('students/<countrycode>/<plz>/<int:distance>', views.list_by_plz, name='list_by_plz'),
    path('hospitals/<countrycode>/<plz>', views.hospital_list, name='hospital_list'),
    path('hospital_registration', views.hospital_registration, name='hospital_registration'),
    path('hospital_map', views.hospital_overview, name='hopsital_map'),
    path('hospital_view/<str:uuid>/', views.hospital_view, name='hospital_view')
]
