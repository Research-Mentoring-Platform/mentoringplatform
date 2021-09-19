from django.test import TestCase

from mentee.models import MenteeDiscipline
from mentorship.models import Mentorship
from users.models import CustomUser


class ExampleTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def test_example_case_1(self):
        self.assertEqual(1, 1)

    def test_example_case_2(self):
        self.assertNotEqual(1, 2)
