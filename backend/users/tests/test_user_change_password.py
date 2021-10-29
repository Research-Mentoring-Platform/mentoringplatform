from django.test import TransactionTestCase
import logging
from users.models import CustomUser

USER_DATA1 = {
    'username': 'username1',
    'password': 'oldpass@1234',
    'email': 'name1@abc.de',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'date_of_birth': '2001-08-07',
    'is_mentor': True,
    'is_mentee': False,
}

USER_DATA2 = {
    'username': 'username2',
    'password': 'oldpass@1234',
    'email': 'name2@abc.de',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'date_of_birth': '2001-08-07',
    'is_mentor': True,
    'is_mentee': False,
}

USER_PASSWORD_DATA = {
    'current_password': 'oldpass@1234',
    'new_password': 'newpass@1234'
}



class ChangePasswordTestCases(TransactionTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        self.client.post('/api/users/user/', data=USER_DATA1)
        self.user = CustomUser.objects.get(username=USER_DATA1['username'])
        self.user.email_verified = True
        self.user.save()
        response = self.client.login(email=USER_DATA1['email'], password=USER_DATA1['password'])
        self.assertTrue(response)

    def test_user_change_password_valid(self):
        response = self.client.post(f'/api/users/user/{self.user.uid}/change-password/',
                                    data=USER_PASSWORD_DATA)
        self.assertEqual(response.status_code, 200)
        self.user = CustomUser.objects.get(username=USER_DATA1['username'])
        self.assertTrue(self.user.check_password(USER_PASSWORD_DATA['new_password']))

    def test_user_change_password_invalid_user(self):
        self.client.post('/api/users/user/', data=USER_DATA2)
        self.user2 = CustomUser.objects.get(username=USER_DATA2['username'])
        response = self.client.login(email=USER_DATA2['email'],
                                     password=USER_DATA2['password'])  # login as another user
        self.assertTrue(response)
        self.user2.email_verified = True
        self.user2.save()

        response = self.client.post(f'/api/users/user/{self.user.uid}/change-password/',
                                    data=USER_PASSWORD_DATA)    # user2 trying to change password of user
        self.assertEqual(response.status_code, 403)
        self.user = CustomUser.objects.get(username=USER_DATA1['username'])
        self.assertTrue(self.user.check_password(USER_PASSWORD_DATA['current_password']))

    def test_user_change_password_new_password_same_as_current_password(self):
        response = self.client.post(f'/api/users/user/{self.user.uid}/change-password/',
                                    data={'current_password': USER_PASSWORD_DATA['current_password'],
                                          'new_password': USER_PASSWORD_DATA['current_password']})
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA1['username'])
        self.assertTrue(self.user.check_password(USER_PASSWORD_DATA['current_password']))

    def test_user_change_password_new_password_weak(self):
        response = self.client.post(f'/api/users/user/{self.user.uid}/change-password/',
                                    data={'current_password': USER_PASSWORD_DATA['current_password'],
                                          'new_password': 'pass'})
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA1['username'])
        self.assertTrue(self.user.check_password(USER_PASSWORD_DATA['current_password']))

    def test_user_change_password_invalid_current_password(self):
        response = self.client.post(f'/api/users/user/{self.user.uid}/change-password/',
                                    data={'current_password': 'wrong-current-password',
                                          'new_password': USER_PASSWORD_DATA['new_password']})
        self.assertEqual(response.status_code, 400)
        self.user = CustomUser.objects.get(username=USER_DATA1['username'])
        self.assertTrue(self.user.check_password(USER_PASSWORD_DATA['current_password']))
