import logging
from types import ClassMethodDescriptorType
from django import setup
from django.test.testcases import TestCase
from users.models import CustomUser
from mentor.models import *
from mentee.models import *


class SearchMentorTestCases(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logging.disable(logging.CRITICAL)
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        logging.disable(logging.NOTSET)
        return super().tearDownClass()

    def setUp(self) -> None:
        self.client.login(email="karan17058@iiitd.ac.in", password="pass4321")
        user1=CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        user2=CustomUser.objects.get(email='prince17080@iiitd.ac.in')
        self.mentee=Mentee.objects.get(user=user1)
        self.mentor=Mentor.objects.get(user=user2)
        self.mentor.accepted_mentee_types.add(self.mentee.designation)
        return super().setUp()
    
    def test_mentor_search_full_name(self):
        response=self.client.get('/api/mentor/mentor/find_for_mentorship/?search=prince sachdeva')
        self.assertTrue(any(mentor['username']=='prince17080' for mentor in response.json()))
    
    def test_mentor_search_first_name(self):
        response=self.client.get('/api/mentor/mentor/find_for_mentorship/?search=prin')
        self.assertTrue(any(mentor['username']=='prince17080' for mentor in response.json()))

    def test_mentor_search_last_name(self):
        response=self.client.get('/api/mentor/mentor/find_for_mentorship/?search=sach')
        self.assertTrue(any(mentor['username']=='prince17080' for mentor in response.json()))

    def test_mentor_search_username(self):
        response=self.client.get('/api/mentor/mentor/find_for_mentorship/?search=prince1708')
        self.assertTrue(any(mentor['username']=='prince17080' for mentor in response.json()))

