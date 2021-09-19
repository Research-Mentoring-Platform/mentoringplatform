from django.test import TransactionTestCase
import logging
from users.models import CustomUser

VALID_USER_DATA = {
    'username': 'username',
    'password': 'pass@1234',
    'email': 'name@abc.de',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'date_of_birth': '2001-08-07',
    'is_mentor': True,
    'is_mentee': False,
}

VALID_USER_DATA2 = {
    'username': 'name',
    'password': 'pass@4321',
    'email': 'name@def.gh',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'date_of_birth': '2003-08-07',
    'is_mentor': False,
    'is_mentee': True,
}


class RegistrationTestCases(TransactionTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def test_user_valid(self):
        response = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomUser.objects.get(username=VALID_USER_DATA['username']))

    def test_user_both_mentor_and_mentee(self):
        data1 = VALID_USER_DATA.copy()
        data1['is_mentor'] = True
        data1['is_mentee'] = False
        response = self.client.post('/api/users/user/', data=data1)
        data1['is_mentor'] = False
        data1['is_mentee'] = True
        response = self.client.post('/api/users/user/', data=data1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_both_mentor_mentee_true(self):
        data = VALID_USER_DATA.copy()
        data['is_mentor'] = True
        data['is_mentee'] = True
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_both_mentor_mentee_false(self):
        data = VALID_USER_DATA.copy()
        data['is_mentor'] = False
        data['is_mentee'] = False
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_already_registered(self):
        response = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        response = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_multiple_user_register_valid(self):
        response1 = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        response2 = self.client.post('/api/users/user/', data=VALID_USER_DATA2)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(CustomUser.objects.get(username=VALID_USER_DATA['username']))
        self.assertTrue(CustomUser.objects.get(username=VALID_USER_DATA2['username']))

    def test_user_weak_password(self):
        data = VALID_USER_DATA.copy()
        data['password'] = 'pass'
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_invalid_email(self):
        data = VALID_USER_DATA.copy()
        data['email'] = 'email'
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_invalid_date_of_birth(self):
        data = VALID_USER_DATA.copy()
        data['date_of_birth'] = '2010-09-07'
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(CustomUser.objects.count(), 0)
