from django.test import TestCase


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
