from django.test import TestCase, Client
from apps.iamstudent.models import Student, AUSBILDUNGS_TYPEN_COLUMNS
from apps.ineedstudent.models import Hospital
from apps.accounts.models import User
from django.contrib import auth

import numpy as np

def generate_random_student(countrycode="DE", plz="14482", i=0, validated_email=False):
    m = str(i) + "student@email.de"
    pwd = User.objects.make_random_password()
    kwd = dict(zip(AUSBILDUNGS_TYPEN_COLUMNS,np.random.choice([True,False],size=len(AUSBILDUNGS_TYPEN_COLUMNS))))

    u = User.objects.create(username=m, email=m, is_student=True, validated_email=validated_email)
    u.set_password(pwd)
    s = Student.objects.create(user=u,
                               countrycode=countrycode,
                               plz=plz,
                               availability_start='{}-{:02d}-{:02d}'.format(2020,3,23),
                               **kwd
                            )
    u.save()
    s.save()
    return m, pwd, s.uuid

def generate_random_hospital(countrycode="DE", plz="14482", i=0, datenschutz_zugestimmt=True, validated_email=False):
    m = str(i) + "hospital@email.de"
    pwd = User.objects.make_random_password()
    u = User.objects.create(username=m, email=m, is_hospital=True, validated_email=validated_email)
    u.set_password(pwd)
    s = Hospital.objects.create(user=u,
                               countrycode=countrycode,
                               plz=plz,
                               ansprechpartner='XY',
                               sonstige_infos='yeaah',
                               datenschutz_zugestimmt=datenschutz_zugestimmt,                            
                               einwilligung_datenweitergabe=True,
                            )
    u.save()
    s.save()
    return m, pwd, s.uuid

def generate_staff_user(i=0):
    m = str(i) + "staff@email.de"
    pwd = User.objects.make_random_password()
    u = User.objects.create_superuser(username=m, email=m)
    u.set_password(pwd)
    u.save()
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

    def test_count_url(self):
        generate_random_student(validated_email=True)
        response = self.client.get('/accounts/count', {})
        assert response.status_code == 200
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'facility_count': 0, 'user_count': 1}
        )

        generate_random_hospital(validated_email=True)
        response = self.client.get('/accounts/count', {})
        assert response.status_code == 200
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'facility_count': 1, 'user_count': 1}
        )



    def test_student(self):
        student_email, student_password, _ = generate_random_student()
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

        response = self.client.get('/accounts/profile_redirect', follow=True)
        assert "profile_student" in response.redirect_chain[0][0]
        assert self.client.get('/accounts/profile_student', {}).status_code == 200

        assert self.client.get('/accounts/logout/', {}).status_code == 200
        assert auth.get_user(self.client).is_anonymous

        response = self.client.post('/accounts/login/', {
            "username": student_email,
            "password": student_password,
        }, follow=True)
        assert auth.get_user(self.client).username == student_email

        # Test view list of studens without being logged in as student. Should redirect!
        response = self.client.get("/ineedstudent/students/DE/14482/0", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200

        # Test admin view when logged in as student. Should redirect
        response = self.client.get("/accounts/approve_hospitals", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200

        m1, p1, uuid1 = generate_random_hospital("DE", "14482", 1337)
        m2, p2, uuid2 = generate_random_hospital("DE", "10115", 1234)
        m3, p3, uuid3 = generate_random_hospital("AT", "4020", 420)
        response = self.client.get('/ineedstudent/hospital_view/' + str(uuid1) + "/")
        assert response.status_code == 200

        response = self.client.get('/ineedstudent/hospitals/DE/14482')
        assert response.status_code == 200

        assert self.client.get('/accounts/delete_me_ask', {}).status_code == 200
        assert self.client.get('/accounts/delete_me', {}).status_code == 200


        response = self.client.post('/accounts/login/', {
            "username": student_email,
            "password": student_password,
        }, follow=True)
        assert auth.get_user(self.client).is_anonymous

        # Only available to logged in users, should redirect
        response = self.client.get('/ineedstudent/hospital_view/' + str(uuid1) + "/", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200

        # Only available to logged in users, should redirect
        response = self.client.get('/ineedstudent/hospitals/DE/14482', follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200

    def test_hospital(self):
        hospital_email, hospital_password, uuid = generate_random_hospital()

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

        # Test view list of students with being logged in as hospital. Should work!
        response = self.client.get("/ineedstudent/students/DE/14482/0", follow=True)
        assert response.status_code == 200
        assert len(response.redirect_chain) == 0


        # Test admin view when logged in as hospital. Should redirect
        response = self.client.get("/accounts/approve_hospitals", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200


        response = self.client.get('/ineedstudent/hospital_view/' + str(uuid) + "/")
        assert response.status_code == 200

        response = self.client.get('/ineedstudent/hospitals/DE/14482')
        assert response.status_code == 200

        m1, p1, uuid1 = generate_random_student("DE", "14482", 1337, validated_email=True)
        m2, p2, uuid2 = generate_random_student("DE", "10115", 1234, validated_email=True)
        m3, p3, uuid3 = generate_random_student("DE", "10115", 12345, validated_email=False)
        m4, p4, uuid4 = generate_random_student("AT", "4020", 420, validated_email=True)
        response = self.client.get('/ineedstudent/students/DE/14482/0')

        assert "1 Helfer*innen" in str(response.content)
        assert response.status_code == 200

        response = self.client.get('/ineedstudent/students/DE/14482/50')
        assert "2 Helfer*innen" in str(response.content)
        assert response.status_code == 200

        assert self.client.get('/accounts/delete_me_ask', {}).status_code == 200
        assert self.client.get('/accounts/delete_me', {}).status_code == 200

        response = self.client.post('/accounts/login/', {
            "username": hospital_email,
            "password": hospital_password,
        }, follow=True)
        assert auth.get_user(self.client).is_anonymous

        # Test view list of studens without being logged in. Should redirect!
        response = self.client.get("/ineedstudent/students/DE/14482/0", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200

        # Test admin view as logged out user. Should redirect
        response = self.client.get("/accounts/approve_hospitals", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200

        hospital_email, hospital_password, uuid = generate_random_hospital(datenschutz_zugestimmt=False, i=9999)
        response = self.client.post('/accounts/login/', {
            "username": hospital_email,
            "password": hospital_password,
        }, follow=True)
        assert Hospital.objects.get(user__email=hospital_email).datenschutz_zugestimmt == False
        assert "zustimmung" in response.redirect_chain[1][0]
        assert auth.get_user(self.client).username == hospital_email

        response = self.client.post('/ineedstudent/zustimmung', {
            "datenschutz_zugestimmt": True,
            "einwilligung_datenweitergabe": True,
        }, follow=True)
        assert response.status_code == 200
        assert "login_redirect" in response.redirect_chain[0][0]
        assert Hospital.objects.get(user__email=hospital_email).datenschutz_zugestimmt == True

    def test_sudent_individual_view(self):
        staff_email, staff_password = generate_staff_user()
        hospital_email, hospital_password, hospital_uuid = generate_random_hospital()
        student_email, student_password, student_uuid = generate_random_student()

        response = self.client.post('/accounts/login/', {
            "username": student_email,
            "password": student_password,
        }, follow=True)
        response = self.client.get('/iamstudent/view_student/' + str(student_uuid), follow=True)
        assert response.status_code == 200
        assert "/accounts/profile_student" in response.redirect_chain[0][0]

        # TOOD: test which emails can be seen here!
        response = self.client.post('/accounts/login/', {
            "username": staff_email,
            "password": staff_password,
        }, follow=True)
        response = self.client.get('/iamstudent/view_student/' + str(student_uuid))
        assert response.status_code == 200

        # TOOD: test which emails can be seen here!
        response = self.client.post('/accounts/login/', {
            "username": hospital_email,
            "password": hospital_password,
        }, follow=True)
        response = self.client.get('/iamstudent/view_student/' + str(student_uuid))
        assert response.status_code == 200




    def test_admin(self):
        staff_email, staff_password = generate_staff_user()

        assert self.client.post('/accounts/logout/', {}).status_code == 200

        response = self.client.post('/accounts/password_reset', {
            "email": staff_email
        }, follow=True)
        #print(response.redirect_chain)
        assert response.status_code == 200
        #TODO why does this not redirect to /accounts/password_reset/done

        response = self.client.post('/accounts/login/', {
            "username": staff_email,
            "password": staff_password,
        }, follow=True)
        assert auth.get_user(self.client).username == staff_email

        response = self.client.post('/accounts/password_change', {
            "email": staff_email,
            "new_password1": staff_password,
            "new_password2": staff_password
        }, follow=True)
        #print(response.redirect_chain)
        assert response.status_code == 200
        #TODO why does this not redirect to /accounts/password_change/done

        assert self.client.get('/mapview/', {}).status_code == 200
        #TODO Test Detailansicht for a hospital!

        response = self.client.get('/accounts/profile_redirect', follow=True)
        assert response.status_code == 200
        assert "approve_hospitals" in response.redirect_chain[0][0]

        response = self.client.get('/accounts/approve_hospitals', follow=True)
        assert response.status_code == 200

        assert self.client.get('/accounts/logout/', {}).status_code == 200
        assert auth.get_user(self.client).is_anonymous

        response = self.client.post('/accounts/login/', {
            "username": staff_email,
            "password": staff_password,
        }, follow=True)
        assert auth.get_user(self.client).username == staff_email

        # Test view list of studens witbeing logged in as staff user
        # Current behavior: Should redirect!
        # TODO: discuss what the behavior of this should be!
        response = self.client.get("/ineedstudent/students/DE/14482/0", follow=True)
        assert "login" in response.redirect_chain[0][0]
        assert response.status_code == 200


        assert self.client.get('/accounts/delete_me_ask', {}).status_code == 200
        assert self.client.get('/accounts/delete_me', {}).status_code == 200

        response = self.client.post('/accounts/login/', {
            "username": staff_email,
            "password": staff_password,
        }, follow=True)
        assert auth.get_user(self.client).is_anonymous

        response = self.client.get("/ineedstudent/students/DE/14482/0", follow=True)
