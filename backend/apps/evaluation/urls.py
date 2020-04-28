from django.urls import path

from . import views

urlpatterns = [
    # path for Student-Evaluations
    path('student/', views.student_evaluation, name='student_evaluation'),
    # path for Institution-Evaluations
    path('institution/', views.institution_evaluation, name='institution_evaluation'),
    # evaluation complete
    path('completed/', views.evaluation_completed, name='evaluation_completed')
]