from rest_framework.test import APITestCase

from .models import CustomUser


class UserTestCase(APITestCase):
    def setUp(self):
        CustomUser.objects.create_user("bruce.wayne@dc.com", "0111111111", "bruce.wayne", "123 abc st")

    def test_send_forgot_password_email(self):
        response = self.client.post('/accounts/password/forgot/',
                                    data={"email": "bruce.wayne@dc.com"},
                                    HTTP_HOST='example.com')
        self.assertEqual(response.data, {"message": 'Email has been sent to your email address. '
                                                    'Please check its inbox to continue resetting password.'})