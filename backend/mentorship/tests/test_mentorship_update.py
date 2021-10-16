import json
import logging

from django.test import TestCase
from rest_framework import status
from mentorship.models import Mentorship, MentorshipRequest
from mentee.models import MenteeDesignation
from users.models import CustomUser

class MentorshipFinishTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_mentee1 = next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
            cls.login_mentor1 = next(user for user in users_data if user['email'] ==  'prince17080@iiitd.ac.in')
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

        self.data = {
            'status': 3,
            'start_date': '16/10/2021',
            'end_date': '16/12/2021'
        }

    def test_update_mentorship_put(self):
        self.client.login(email=self.login_mentor1['email'], password=self.login_mentor1['password'])
        res = self.client.put(f'/api/mentorship/mentorship/{self.mentorship.uid}/', data=self.data, follow=True, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentorship_patch(self):
        self.client.login(email=self.login_mentor1['email'], password=self.login_mentor1['password'])
        res = self.client.patch(f'/api/mentorship/mentorship/{self.mentorship.uid}/', data=self.data, follow=True, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_mentorship_post(self):
        self.client.login(email=self.login_mentor1['email'], password=self.login_mentor1['password'])
        res = self.client.post(f'/api/mentorship/mentorship/{self.mentorship.uid}/', data=self.data, follow=True, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_405_FORBIDDEN)