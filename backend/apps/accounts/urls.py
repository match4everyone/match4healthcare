from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

from . import generate_users

urlpatterns = [
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done_.html'),name='password_change_done'),
    path('password_change',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form_.html'),name='password_change_form'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_.html', from_email=settings.NOREPLY_MAIL),name='password_reset_form'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_.html'),name='password_reset_done'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_.html'),name='password_reset_complete_'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm_.html',
        post_reset_login=True,
        success_url='/accounts/validate_email'
      ) , name='password_reset_confirm_'),
    path('resend_validation_email/<email>', views.resend_validation_email,name='resend_validation_email'),
    path('login/', views.CustomLoginView.as_view(template_name='registration/login.html'),name='login'),
    path('', include('django.contrib.auth.urls')),
    path('validate_email', views.validate_email, name='validate_email'),
    path('profile_redirect', views.profile_redirect, name='profile_redirect'),
    path('login_redirect', views.login_redirect, name='login_redirect'),
    path('delete_me_ask', views.delete_me_ask, name='delete_me_ask'),
    path('delete_me', views.delete_me, name='delete_me'),
    path('signup_student', views.student_signup, name='student_signup'),
    path('signup_hospital', views.hospital_signup, name='hospital_signup'),
    path('profile_student', views.edit_student_profile, name='edit_student_profile'),
    path('profile_hospital', views.edit_hospital_profile, name='edit_hospital_profile'),
    path('approve_hospitals', views.approve_hospitals, name='approve_hospitals'),
    path('change_hospital_approval/<str:uuid>/', views.change_hospital_approval, name='change_hospital_approval'),
    path('delete_hospital/<str:uuid>/', views.delete_hospital, name='delete_hospitall'),
    path('count', views.UserCountView.as_view(), name='count'),
    path('change_activation',views.change_activation_ask,name='activate_student_ask'),
    path('change_activation_confirm',views.change_activation,name='activate_student'),
    path('view_newsletter/<uuid>', views.view_newsletter, name='view_newsletter'),
    path('new_newsletter', views.new_newsletter, name='new_newsletter'),
    path('list_newsletter', views.list_newsletter, name='list_newsletter'),
    path('did_see_newsletter/<uuid>/<token>', views.did_see_newsletter, name='did_see_newsletter'),
    path('profile_staff', views.staff_profile, name='staff_profile'),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns.append(path('add_data',generate_users.populate_db))
