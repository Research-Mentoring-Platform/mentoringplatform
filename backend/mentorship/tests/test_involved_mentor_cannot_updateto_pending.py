import json
import logging
from django.test import TransactionTestCase,TestCase
from django.test.testcases import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline
from mentorship.models import MentorshipRequest,MentorshipRequestStatus,Mentorship,MentorshipStatus


class Involved_Mentor_Cannot_Update_To_Pending_Test(TestCase):
    # Set up the mentor and mentee through which we will do the mentor profile testing.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_mentee= next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
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
        Btech_uid = MenteeDesignation.objects.get(label='BTech').uid
        Mtech_uid = MenteeDesignation.objects.get(label='MTech').uid
        Faculty_uid = MenteeDesignation.objects.get(label='Faculty').uid
        Phd_uid = MenteeDesignation.objects.get(label='PhD').uid
        IndRes_uid = MenteeDesignation.objects.get(label='Industry Researcher').uid


        deptt_uid=self.mentor.department.uid
        disc_uid=self.mentor.discipline.uid
        desig_uid=self.mentor.designation.uid

        self.data = {
            'accepted_mentee_types': [Btech_uid,Mtech_uid,Faculty_uid,Phd_uid,IndRes_uid],  #adding all since randomly mentee gets any
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
        }
         # Making mentor available to take mentorship request from all types of mentees
        response = self.client.patch(f'/api/mentor/mentor/{self.mentor.uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 200)
       
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
        self.assertEqual(response.status_code, 201)

        self.mentorship_req=MentorshipRequest.objects.get(mentor=self.mentor,mentee=self.mentee)
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_PENDING) 

    
    def test_Involved_Mentor_Cannot_Update_To_Pending_If_Accepted(self):
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        mentorshipreq_uid= self.mentorship_req.uid

        respond_data={
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'status' : MentorshipRequestStatus.REQUEST_ACCEPTED ,#Accepting the request.,
            'accepted' : True   #added field to accept
        }

        response = self.client.post(f'/api/mentorship/request/{mentorshipreq_uid}/respond/',data=respond_data)
        self.assertEqual(response.status_code, 200)     #Successfully accept mentorship request
        self.mentorship_req.refresh_from_db()
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_ACCEPTED)  #Successfully accept mentorship request in db too
        respond_data={
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'uid':  mentorshipreq_uid,
            'status' : MentorshipRequestStatus.REQUEST_PENDING ,#trying to go back to pending 
        }
        response = self.client.post(f'/api/mentorship/request/{mentorshipreq_uid}/respond/',data=respond_data)
        self.assertEqual(response.status_code, 403)     #Cannot modify status of a non-pending mentorship request
        
        response = self.client.patch(f'/api/mentorship/request/{mentorshipreq_uid}/',data=respond_data)
        self.assertEqual(response.status_code, 403)  

        response = self.client.put(f'/api/mentorship/request/{mentorshipreq_uid}/',data=respond_data)
        self.assertEqual(response.status_code, 403)  
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_ACCEPTED)
        
    def test_Involved_Mentor_Cannot_Update_To_Pending_If_Rejected(self):
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        mentorshipreq_uid= self.mentorship_req.uid

        respond_data={
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'status' : MentorshipRequestStatus.REQUEST_REJECTED ,#Accepting the request.,
            'accepted' : False ,  #added field to accept
            'reject_reason' : "Rejecting for testing"
        }

        response = self.client.post(f'/api/mentorship/request/{mentorshipreq_uid}/respond/',data=respond_data)
        self.assertEqual(response.status_code, 200)     #Successfully accept mentorship request
        self.mentorship_req.refresh_from_db()
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_REJECTED)  #Successfully accept mentorship request in db too
        respond_data={
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'uid':  mentorshipreq_uid,
            'status' : MentorshipRequestStatus.REQUEST_PENDING ,#trying to go back to pending 
        }
        response = self.client.post(f'/api/mentorship/request/{mentorshipreq_uid}/respond/',data=respond_data)
        self.assertEqual(response.status_code, 403)     #Cannot modify status of a non-pending mentorship request
        
        response = self.client.patch(f'/api/mentorship/request/{mentorshipreq_uid}/',data=respond_data)
        self.assertEqual(response.status_code, 403)  

        response = self.client.put(f'/api/mentorship/request/{mentorshipreq_uid}/',data=respond_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_REJECTED)
    