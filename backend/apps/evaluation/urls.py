from django.urls import path

from . import views

urlpatterns = [
    # path for Student-Evaluations
    path('student/', views.StudentEvaluationForm.as_view()),
    # path for Institution-Evaluations
    path('institution/', views.InstitutionEvaluationForm.as_view()),
]