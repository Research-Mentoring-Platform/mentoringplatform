from django.test import TestCase
import logging
from .test_data import *

class RegistrationTestCases(TestCase):
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

    def test_user_both_mentor_and_mentee(self):
        data1=VALID_USER_DATA.copy()
        data1['is_mentor']= True
        data1['is_mentee']= False
        response = self.client.post('/api/users/user/', data=data1)
        data1['is_mentor'] = False
        data1['is_mentee'] = True
        response = self.client.post('/api/users/user/', data=data1)
        self.assertEqual(response.status_code, 400)

    def test_user_already_registered(self):
        response = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        response = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        self.assertEqual(response.status_code, 400)

    def test_multiple_user_register_valid(self):
        response1 = self.client.post('/api/users/user/', data=VALID_USER_DATA)
        response2 = self.client.post('/api/users/user/', data=VALID_USER_DATA2)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_user_weak_password(self):
        data = VALID_USER_DATA.copy()
        data['password']= 'pass'
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_user_invalid_email(self):
        data = VALID_USER_DATA.copy()
        data['email']= 'email'
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_user_invalid_date_of_birth(self):
        data = VALID_USER_DATA.copy()
        data['date_of_birth']= '2010-09-07'
        response = self.client.post('/api/users/user/', data=data)
        self.assertEqual(response.status_code, 400)