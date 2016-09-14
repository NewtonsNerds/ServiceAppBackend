from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser


class UserTestCase(APITestCase):
    def setUp(self):
        CustomUser.objects.create_user(email="ronak@newtonsit.com.au", mobile="0123232323",password="test12345",address="13 Larkin Street")

    def test_LoginUser(self):
        data = {"email": "ronak@newtonsit.com.au","password": "test12345"}
        response = self.client.post('/accounts/login/', data, format='json')
        self.assertEqual(response.data.get('email'),"ronak@newtonsit.com.au")
        self.assertEqual(response.data.get('mobile'),"0123232323")
        self.assertEqual(response.data.get('address'),"13 Larkin Street")

    def test_InvalidLoginUser(self):
        data = {"email": "ronak@newtonsit.com.au", "password": "test12341"}
        response = self.client.post('/accounts/login/', data, format='json')
        self.assertEqual(response.data, {
            "non_field_errors": [
                "Incorrect credentials. Please try again."
            ]
        })

    def test_InvalidLoginUser(self):
        data = {"email": "ronak@newtonsit.com.au", "password": "test12341"}
        response = self.client.post('/accounts/login/', data, format='json')
        self.assertEqual(response.data, {
            "non_field_errors": [
                "Incorrect credentials. Please try again."
            ]
        })

    def test_BlankInvalidLoginUser(self):
        data = {"email": "", "password": "test12341"}
        response = self.client.post('/accounts/login/', data, format='json')
        self.assertEqual(response.data, {
            "email": [
                "This field may not be blank."
            ]
        })

    def test_RegisterUser(self):
        data = {"email": "ronak_test1@newtonsit.com.au","password": "test12345","mobile": "1234567890","address": "larkin"}
        response = self.client.post('/accounts/register/', data, format='json')
        self.assertEqual(response.data.get('email'), "ronak_test1@newtonsit.com.au")
        self.assertEqual(response.data.get('mobile'), "1234567890")
        self.assertEqual(response.data.get('address'), "larkin")

    def test_InvalidRegisterUser(self):
        data = {"email": "ronak@newtonsit.com.au","password": "test12345","mobile": "1234567890","address": "larkin"}
        response = self.client.post('/accounts/register/', data, format='json')
        self.assertEqual(response.data, {
            "non_field_errors": [
                "This email is already exist"
            ]
        })

    def test_send_forgot_password_email(self):
        response = self.client.post('/accounts/password/forgot/',
                                    data={"email": "ronak@newtonsit.com.au"},
                                    HTTP_HOST='example.com')
        self.assertEqual(response.data, {"message": 'Email has been sent to your email address. '
                                                    'Please check its inbox to continue resetting password.'})
