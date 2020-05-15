from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("thanks", TemplateView.as_view(template_name="thanks.html"), name="thanks"),
    path("successful_mail", views.EmailToStudentSuccessView.as_view(), name="success"),
    # path('students_testing/<countrycode>/<plz>/<int:distance>', views.student_list_view, name='student_list_view'),
    path(
        "send_mail_student/<id_list>",
        views.send_mail_student_id_list,
        name="send_mail_student_id_list",
    ),
    path("view_student/<uuid>", views.view_student, name="view_student"),
]
