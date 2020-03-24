from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    #path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_student', views.student_signup, name='student_signup'),
    path('signup_hospital', views.hospital_signup, name='hospital_signup')
]
