from django.urls import path

from . import views

urlpatterns = [
    #path('student_registration', views.get_student, name='student_registration'),
    path('thanks', views.thx, name='thanks'),
    #path('send_mail_student', views.send_mail_student, name='send_mail_student'),
    path('successful_mail', views.successful_mail, name='success'),
    path('send_mail_student/<id_list>', views.send_mail_student_id_list, name='send_mail_student_id_list'),
]
