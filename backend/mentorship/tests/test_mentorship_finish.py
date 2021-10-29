import json
import logging

from django.test import TestCase
from rest_framework import status
from mentorship.models import Mentorship, MentorshipRequest, MentorshipStatus
from mentee.models import MenteeDesignation
from users.models import CustomUser

class MentorshipFinishTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_mentee1 = next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
            cls.login_mentee2 = next(user for user in users_data if user['email'] ==  'karan17058@iiitd.ac.in')
            cls.login_mentor1 = next(user for user in users_data if user['email'] ==  'prince17080@iiitd.ac.in')
            cls.login_mentor2 = next(user for user in users_data if user['email'] ==  'shaurya17104@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        """ create a Mentorship object for login_mentor1 and login_mentee1 """

        # login as mentor and update accepted_mentee_types to include all MenteeDesginations
        self.client.login(email=self.login_mentor1['email'], password=self.login_mentor1['password'])
        self.mentor = CustomUser.objects.get(email=self.login_mentor1['email']).mentor

        accepted_types = []
        mentee_desig = MenteeDesignation.objects.all()
        for des in mentee_desig.iterator():
            accepted_types.append(des.uid)

        deptt_uid = self.mentor.department.uid
        disc_uid = self.mentor.discipline.uid
        desig_uid = self.mentor.designation.uid

        mentor_data = {
            'accepted_mentee_types': accepted_types,
            'department': deptt_uid,
            'designation': desig_uid,
            'discipline': disc_uid
        }

        res = self.client.patch(f'/api/mentor/mentor/{self.mentor.uid}/', data=mentor_data, content_type='application/json', follow=True)
        self.client.logout()

        # login as mentee and send a mentorship request to the mentor
        self.client.login(email=self.login_mentee1['email'], password=self.login_mentee1['password'])
        self.mentee = CustomUser.objects.get(email=self.login_mentee1['email']).mentee

        request_data = {
            "mentor": self.mentor.uid,
            "mentee": self.mentee.uid,
            "statement_of_purpose": "lorem ipsum",
            "expectations": "lorem ipsum",
            "commitment": "lorem ipsum",
        }

        res = self.client.post('/api/mentorship/request/', data=request_data)
        self.mentorship_req = MentorshipRequest.objects.get(mentor=self.mentor,mentee=self.mentee)
        self.client.logout()

        # login as mentor and accept the mentorship request
        self.client.login(email=self.login_mentor1['email'], password=self.login_mentor1['password'])
        res = self.client.post(f'/api/mentorship/request/{self.mentorship_req.uid}/respond/', data={'accepted': True}, follow=True)
        self.mentorship = Mentorship.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.client.logout()

    def test_mentee_finishes_own_mentorship(self):
        """ tests response when a mentee finishes their own mentorship """
        self.client.login(email=self.login_mentee1['email'], password=self.login_mentee1['password'])
        res = self.client.post(f'/api/mentorship/mentorship/{self.mentorship.uid}/finish/', data={}, content_type='application/json', follow=True)
        m_obj = Mentorship.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(m_obj.status, MentorshipStatus['FINISHED'])

    def test_mentor_finishes_own_mentorship(self):
        """ tests response when a mentor finishes their own mentorship """
        self.client.login(email=self.login_mentor1['email'], password=self.login_mentor1['password'])
        res = self.client.post(f'/api/mentorship/mentorship/{self.mentorship.uid}/finish/', data={}, content_type='application/json', follow=True)
        m_obj = Mentorship.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(m_obj.status, MentorshipStatus['FINISHED'])

    def test_mentee_finishes_other_mentorship(self):
        """ tests response when a mentee finishes a different mentee's mentorship """
        self.client.login(email=self.login_mentee2['email'], password=self.login_mentee2['password'])
        res = self.client.post(f'/api/mentorship/mentorship/{self.mentorship.uid}/finish/', data={}, content_type='application/json', follow=True)
        m_obj = Mentorship.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(m_obj.status, MentorshipStatus['ONGOING'])

    def test_mentor_finishes_other_mentorship(self):
        """ tests response when a mentor finishes a different mentor's mentorship """
        self.client.login(email=self.login_mentor2['email'], password=self.login_mentor2['password'])
        res = self.client.post(f'/api/mentorship/mentorship/{self.mentorship.uid}/finish/', data={}, content_type='application/json', follow=True)
        m_obj = Mentorship.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(m_obj.status, MentorshipStatus['ONGOING'])
