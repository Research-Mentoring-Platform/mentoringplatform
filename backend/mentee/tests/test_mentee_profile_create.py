from django.test import TransactionTestCase
import logging
from mentee.models import Mentee
from users.models import CustomUser

VALID_USER_DATA = {
    'username': 'name',
    'password': 'pass@4321',
    'email': 'name@def.gh',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'date_of_birth': '2003-08-07',
    'is_mentor': False,
    'is_mentee': True,
}

LOGIN_USER_DATA = {
    'email': 'name@def.gh',
    'password': 'pass@4321'
}


class MenteeProfileCreationTestCases(TransactionTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        self.client.post('/api/users/user/', data=VALID_USER_DATA)
        self.user = CustomUser.objects.get(username=VALID_USER_DATA['username'])

    def test_mentee_profile_not_created_after_registration(self):
        self.assertFalse(Mentee.objects.filter(user=self.user).exists())

    def test_mentee_profile_not_created_after_registration_and_email_verification(self):
        self.user.email_verified = True
        self.user.save()
        self.assertFalse(Mentee.objects.filter(user=self.user).exists())

    def test_mentee_profile_created_after_login(self):
        self.user.email_verified = True
        self.user.save()
        self.client.post('/api/users/token/', data=LOGIN_USER_DATA, follow=True)
        self.assertTrue(Mentee.objects.filter(user=self.user).exists())
