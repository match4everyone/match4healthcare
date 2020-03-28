from django.test import TestCase, Client
from apps.iamstudent.models import Student, AUSBILDUNGS_TYPEN_COLUMNS
from apps.ineedstudent.models import Hospital
from apps.accounts.models import User
from django.contrib import auth

import numpy as np

def generate_random_student(countrycode="DE", plz="14482", i=0):
    m = str(i) + "student@email.de"
    pwd = User.objects.make_random_password()
    kwd = dict(zip(AUSBILDUNGS_TYPEN_COLUMNS,np.random.choice([True,False],size=len(AUSBILDUNGS_TYPEN_COLUMNS))))

    u = User.objects.create(username=m, email=m, is_student=True)
    u.set_password(pwd)
    s = Student.objects.create(user=u,
                               plz=plz,
                               availability_start='{}-{:02d}-{:02d}'.format(2020,3,23),
                               **kwd
                            )
    u.save()
    s.save()
    return m, pwd

def generate_random_hospital(countrycode="DE", plz="14482", i=0):
    m = str(i) + "hospital@email.de"
    pwd = User.objects.make_random_password()
    u = User.objects.create(username=m, email=m, is_hospital=True)
    u.set_password(pwd)
    s = Hospital.objects.create(user=u,
                               plz=plz,
                               ansprechpartner='XY',
                                sonstige_infos='yeaah'
                                )
    u.save()
    s.save()
    return m, pwd


class UrlEndpointTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_http_get_endpoints(self):
        assert self.client.get('/', {}).status_code == 200
        assert self.client.get('/about/', {}).status_code == 200
        assert self.client.get('/impressum/', {}).status_code == 200
        assert self.client.get('/dataprotection/', {}).status_code == 200
        assert self.client.get('/legal-questions/', {}).status_code == 200

        # Mapview
        assert self.client.get('/mapview/', {}).status_code == 200

        # Accounts
        assert self.client.get('/accounts/signup_student', {}).status_code == 200
        assert self.client.get('/accounts/signup_hospital', {}).status_code == 200
        assert self.client.get('/accounts/password_reset/', {}).status_code == 200
        assert self.client.get('/accounts/login/', {}).status_code == 200

        # TODO Remove /ineedstudent/hospital_registration

    def test_student(self):
        student_email, student_password = generate_random_student()
        assert self.client.post('/accounts/logout/', {}).status_code == 200

        response = self.client.post('/accounts/password_reset', {
            "email": student_email
        }, follow=True)
        #print(response.redirect_chain)
        assert response.status_code == 200
        #TODO why does this not redirect to /accounts/password_reset/done

        response = self.client.post('/accounts/validate_email', {
            "email": student_email
        }, follow=True)
        assert "/accounts/login" in response.redirect_chain[0][0]
        assert response.status_code == 200


        response = self.client.post('/accounts/login/', {
            "username": student_email,
            "password": student_password,
        }, follow=True)
        assert auth.get_user(self.client).username == student_email

        assert Student.objects.get(user__email=student_email).user.validated_email == False
        response = self.client.post('/accounts/validate_email', {
            "email": student_email
        }, follow=True)
        assert response.status_code == 200
        assert Student.objects.get(user__email=student_email).user.validated_email


        response = self.client.post('/accounts/password_change', {
            "email": student_email,
            "new_password1": student_password,
            "new_password2": student_password
        }, follow=True)
        #print(response.redirect_chain)
        assert response.status_code == 200
        #TODO why does this not redirect to /accounts/password_change/done

        assert self.client.get('/mapview/', {}).status_code == 200
        #TODO Test Detailansicht for a hospital!

        #TODO this doesnt work right now w/ backend error
        #response = self.client.get('/accounts/profile_redirect', follow=True)
        #print(response.redirect_chain)
        #assert self.client.get('/accounts/profile_student/', {}).status_code == 200

        assert self.client.get('/accounts/logout/', {}).status_code == 200
        assert auth.get_user(self.client).is_anonymous

        response = self.client.post('/accounts/login/', {
            "username": student_email,
            "password": student_password,
        }, follow=True)
        assert auth.get_user(self.client).username == student_email

        assert self.client.get('/accounts/delete_me_ask', {}).status_code == 200
        assert self.client.get('/accounts/delete_me', {}).status_code == 200

        response = self.client.post('/accounts/login/', {
            "username": student_email,
            "password": student_password,
        }, follow=True)
        assert auth.get_user(self.client).is_anonymous

        #TODO: Test ineedstudent/hospitals/countrycode/plz
        #TODO: Test ineedstudent/hopsital_view

    def test_hospital(self):
        hospital_email, hospital_password = generate_random_hospital()

        assert self.client.post('/accounts/logout/', {}).status_code == 200

        response = self.client.post('/accounts/password_reset', {
            "email": hospital_email
        }, follow=True)
        #print(response.redirect_chain)
        assert response.status_code == 200
        #TODO why does this not redirect to /accounts/password_reset/done

        response = self.client.post('/accounts/validate_email', {
            "email": hospital_email
        }, follow=True)
        assert "/accounts/login" in response.redirect_chain[0][0]
        assert response.status_code == 200


        response = self.client.post('/accounts/login/', {
            "username": hospital_email,
            "password": hospital_password,
        }, follow=True)
        assert auth.get_user(self.client).username == hospital_email

        assert Hospital.objects.get(user__email=hospital_email).user.validated_email == False
        response = self.client.post('/accounts/validate_email', {
            "email": hospital_email
        }, follow=True)
        assert response.status_code == 200
        assert Hospital.objects.get(user__email=hospital_email).user.validated_email


        response = self.client.post('/accounts/password_change', {
            "email": hospital_email,
            "new_password1": hospital_password,
            "new_password2": hospital_password
        }, follow=True)
        #print(response.redirect_chain)
        assert response.status_code == 200
        #TODO why does this not redirect to /accounts/password_change/done

        assert self.client.get('/mapview/', {}).status_code == 200
        #TODO Test Detailansicht for a hospital!

        #TODO this doesnt work right now w/ backend error
        response = self.client.get('/accounts/profile_redirect', follow=True)
        assert response.status_code == 200
        assert "profile_hospital" in response.redirect_chain[0][0]
        assert self.client.get('/accounts/profile_hospital', {}).status_code == 200

        assert self.client.get('/accounts/logout/', {}).status_code == 200
        assert auth.get_user(self.client).is_anonymous

        response = self.client.post('/accounts/login/', {
            "username": hospital_email,
            "password": hospital_password,
        }, follow=True)
        assert auth.get_user(self.client).username == hospital_email

        assert self.client.get('/accounts/delete_me_ask', {}).status_code == 200
        assert self.client.get('/accounts/delete_me', {}).status_code == 200

        response = self.client.post('/accounts/login/', {
            "username": hospital_email,
            "password": hospital_password,
        }, follow=True)
        assert auth.get_user(self.client).is_anonymous

        response = self.client.get("/ineedstudent/students/DE/14482/0", follow=True)
        #TODO: Why is this a redirect?

        #TODO: Test ineedstudent/hospitals/countrycode/plz
        #TODO: Test ineedstudent/hopsital_view


    def test_admin(self):
        # TODO: Test approving of hospitals etc.
        pass
