from django.urls import path, register_converter

from apps.iamstudent.views import student_list_view

from . import converters, views

register_converter(converters.DecimalPointFloatConverter, "float")


urlpatterns = [
    path("students/<countrycode>/<plz>/<float:distance>", student_list_view, name="list_by_plz",),
    # path('students_testing/<countrycode>/<plz>/<int:distance>', views.student_list_view, name='student_list_view'),
    path("hospitals/<countrycode>/<plz>", views.hospital_list, name="hospital_list"),
    path("hospital_map", views.hospital_overview, name="hopsital_map"),
    path("hospital_view/<str:uuid>/", views.hospital_view, name="hospital_view"),
    path("hospital_dashboard", views.hospital_dashboard, name="hospital_dashboard"),
    path("change_posting", views.change_posting, name="change_posting"),
]
