from django.test import TransactionTestCase
import logging
from users.models import CustomUser, ForgotPasswordToken
from unittest.mock import patch

USER_DATA = {
    'username': 'username',
    'password': 'oldpass@1234',
    'email': 'name@abc.de',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'date_of_birth': '2001-08-07',
    'is_mentor': True,
    'is_mentee': False,
}

USER_NEW_PASSWORD_DATA = {
    'token': '',
    'new_password': 'newpass@1234'
}

USER_OLD_PASSWORD = 'oldpass@1234'


class ForgotPasswordTestCases(TransactionTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        self.client.post('/api/users/user/', data=USER_DATA)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])

    def test_user_generate_forgot_password_token_invalid_email(self):
        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': 'invalidemail@abc.def'})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ForgotPasswordToken.objects.filter(user=self.user).exists())

    def test_user_forgot_password_new_password_same_as_old_password(self):
        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': USER_DATA['email']})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForgotPasswordToken.objects.filter(user=self.user).exists())
        token_object = ForgotPasswordToken.objects.get(user=self.user)

        response = self.client.post('/api/users/user/forgot-password/',
                                    data={'token': token_object.token,
                                          'new_password': USER_OLD_PASSWORD})
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])
        self.assertTrue(self.user.check_password(USER_OLD_PASSWORD))

    def test_user_forgot_password_new_password_weak(self):
        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': USER_DATA['email']})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForgotPasswordToken.objects.filter(user=self.user).exists())
        token_object = ForgotPasswordToken.objects.get(user=self.user)

        response = self.client.post('/api/users/user/forgot-password/',
                                    data={'token': token_object.token,
                                          'new_password': 'pass'})
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])
        self.assertTrue(self.user.check_password(USER_OLD_PASSWORD))

    def test_user_forgot_password_old_authentication_token(self):
        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': USER_DATA['email']})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForgotPasswordToken.objects.filter(user=self.user).exists())
        old_token_object = ForgotPasswordToken.objects.get(user=self.user)

        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': USER_DATA['email']})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForgotPasswordToken.objects.filter(user=self.user).exists())
        new_token_object = ForgotPasswordToken.objects.get(user=self.user)

        USER_NEW_PASSWORD_DATA['token'] = old_token_object.token
        response = self.client.post('/api/users/user/forgot-password/',
                                    data=USER_NEW_PASSWORD_DATA)
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])
        self.assertTrue(self.user.check_password(USER_OLD_PASSWORD))

        USER_NEW_PASSWORD_DATA['token'] = new_token_object.token
        response = self.client.post('/api/users/user/forgot-password/', data=USER_NEW_PASSWORD_DATA)
        self.assertEqual(response.status_code, 200)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])
        self.assertTrue(self.user.check_password(USER_NEW_PASSWORD_DATA['new_password']))

    @patch('users.models.ForgotPasswordToken.is_expired')
    def test_user_forgot_password_expired_token(self, mock_is_expired):
        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': USER_DATA['email']})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForgotPasswordToken.objects.filter(user=self.user).exists())
        token_object = ForgotPasswordToken.objects.get(user=self.user)
        mock_is_expired.is_expired.return_value = True
        USER_NEW_PASSWORD_DATA['token'] = token_object.token

        response = self.client.post('/api/users/user/forgot-password/', data=USER_NEW_PASSWORD_DATA)
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])
        self.assertTrue(self.user.check_password(USER_OLD_PASSWORD))

    def test_user_forgot_password_valid_workflow(self):
        response = self.client.post('/api/users/user/forgot-password-token/',
                                    data={'email': USER_DATA['email']})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ForgotPasswordToken.objects.filter(user=self.user).exists())
        token_object = ForgotPasswordToken.objects.get(user=self.user)
        USER_NEW_PASSWORD_DATA['token'] = token_object.token

        response = self.client.post('/api/users/user/forgot-password/', data=USER_NEW_PASSWORD_DATA)
        self.assertEqual(response.status_code, 200)
        self.user = CustomUser.objects.get(username=USER_DATA['username'])
        self.assertTrue(self.user.check_password(USER_NEW_PASSWORD_DATA['new_password']))
