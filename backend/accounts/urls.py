from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup_student', views.student_signup, name='student_signup'),
    path('signup_hospital', views.hospital_signup, name='hospital_signup'),
    path('profile_student',views.edit_student_profile, name='edit_student_profile')
]
