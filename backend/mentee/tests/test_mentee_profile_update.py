import json
import logging

from django.test import TestCase
from rest_framework import status
from users.models import CustomUser
from mentee.models import Mentee

class MenteeProfileUpdateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_user = next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        x = self.client.login(email=self.login_user['email'], password=self.login_user['password'])
        self.user = CustomUser.objects.get(email=self.login_user['email'])
        print(self.user.mentee)

    def test_mentee_updates_own_profile(self):
        pass
