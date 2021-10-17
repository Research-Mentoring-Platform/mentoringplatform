import json
import logging

from django.test import TestCase
from mentorship.models import Mentorship, MentorshipRequest
from mentee.models import MenteeDesignation
from users.models import CustomUser


class MentorshipCreateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_mentee = next(user for user in users_data if user['email'] == 'reeshabh17086@iiitd.ac.in')
            cls.login_mentor = next(user for user in users_data if user['email'] == 'prince17080@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        # login as mentor and update accepted_mentee_types to include all MenteeDesginations
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        self.mentor = CustomUser.objects.get(email=self.login_mentor['email']).mentor

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
        res = self.client.patch(f'/api/mentor/mentor/{self.mentor.uid}/', data=mentor_data,
                                content_type='application/json', follow=True)
        self.client.logout()

        # login as mentee
        self.client.login(email=self.login_mentee['email'], password=self.login_mentee['password'])
        self.mentee = CustomUser.objects.get(email=self.login_mentee['email']).mentee

        # mentorship request data
        self.request_data = {
            "mentor": self.mentor.uid,
            "mentee": self.mentee.uid,
            "statement_of_purpose": "lorem ipsum",
            "expectations": "lorem ipsum",
            "commitment": "lorem ipsum",
        }

    def test_mentorship_request_sent_and_accepted(self):
        # mentee sends a mentorship request to the mentor
        response = self.client.post('/api/mentorship/request/', data=self.request_data)
        self.mentorship_req = MentorshipRequest.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.client.logout()

        # login as mentor and accept the mentorship request
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_req.uid}/respond/',
                                    data={'accepted': True},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Mentorship.objects.filter(mentor=self.mentor, mentee=self.mentee).exists())
        self.client.logout()

    def test_mentorship_request_sent_and_pending(self):
        response = self.client.post('/api/mentorship/request/', data=self.request_data)
        self.mentorship_req = MentorshipRequest.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.client.logout()
        self.assertFalse(Mentorship.objects.filter(mentor=self.mentor, mentee=self.mentee).exists())
        self.client.logout()

    def test_mentorship_request_sent_and_rejected(self):
        response = self.client.post('/api/mentorship/request/', data=self.request_data)
        self.mentorship_req = MentorshipRequest.objects.get(mentor=self.mentor, mentee=self.mentee)
        self.client.logout()

        # login as mentor and reject the mentorship request
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_req.uid}/respond/',
                                    data={'reject': True, 'reject_reason': 'xyz'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Mentorship.objects.filter(mentor=self.mentor, mentee=self.mentee).exists())
        self.client.logout()
