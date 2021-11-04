import json
import logging
from django.test import TransactionTestCase,TestCase
from django.test.testcases import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline
from mentorship.models import MentorshipRequest,MentorshipRequestStatus,Mentorship,MentorshipStatus


class Only_Involved_Mentee_Can_Delete_Mentorship_Req(TestCase):
    # Set up the mentor and mentee through which we will do the mentor profile testing.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_mentee= next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
            cls.login_mentee2= next(user for user in users_data if user['email'] ==  'karan17058@iiitd.ac.in')
            cls.login_mentor = next(user for user in users_data if user['email'] ==  'ananya17020@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        # log in the mentor and mentee and get the logged in user object
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
       
        # get the mentor object for the logged in user
        self.mentor = CustomUser.objects.get(email=self.login_mentor['email']).mentor

        # get the uid for all designation types
        accepted_types = []
        mentee_desig = MenteeDesignation.objects.all()
        for des in mentee_desig.iterator():
            accepted_types.append(des.uid)

        deptt_uid=self.mentor.department.uid
        disc_uid=self.mentor.discipline.uid
        desig_uid=self.mentor.designation.uid

        self.data = {
            'accepted_mentee_types': accepted_types,  #adding all since randomly mentee gets any
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
        }
         # Making mentor available to take mentorship request from all types of mentees
        response = self.client.patch(f'/api/mentor/mentor/{self.mentor.uid}/', data=self.data, content_type='application/json', follow=True)
        self.client.logout()

        #logging in the mentee to send the mentor a mentorship request
        self.client.login(email=self.login_mentee['email'], password=self.login_mentee['password'])
        self.mentee = CustomUser.objects.get(email=self.login_mentee['email']).mentee

        request_data = {
            "mentor": self.mentor.uid,
            "mentee": self.mentee.uid,
            "statement_of_purpose": "Trial",
            "expectations": "Trial",
            "commitment": "Trial",
        }

        response = self.client.post(f'/api/mentorship/request/', data=request_data)
        self.client.logout()

        self.mentorship_req=MentorshipRequest.objects.get(mentor=self.mentor,mentee=self.mentee)
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_PENDING) 

    def test_involved_mentee_can_delete(self):
        self.client.login(email=self.login_mentee['email'], password=self.login_mentee['password'])
        mentorship_req_uid = self.mentorship_req.uid
        response = self.client.delete(f'/api/mentorship/request/{mentorship_req_uid}/')
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(self.mentorship_req,MentorshipRequest.objects.all())
        self.client.logout()

    def test_uninvolved_mentee_cannot_delete(self):
        # Logging in as different mentee
        self.client.login(email=self.login_mentee2['email'], password=self.login_mentee2['password'])
        mentorship_req_uid = self.mentorship_req.uid
        response = self.client.delete(f'/api/mentorship/request/{mentorship_req_uid}/')
    
        self.mentorship_req.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertIn(self.mentorship_req,MentorshipRequest.objects.all())
        self.client.logout()
