import json
import logging
from django.test import TransactionTestCase,TestCase
from django.test.testcases import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline
from mentorship.models import MentorshipRequest,MentorshipRequestStatus


class OnlyInvolvedMentorCanRespondTest(TestCase):
    # Set up the mentor and mentee through which we will do the mentor profile testing.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_mentor = next(user for user in users_data if user['email'] ==  'shaurya17104@iiitd.ac.in')
            cls.login_mentee= next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
            cls.login_mentor2 = next(user for user in users_data if user['email'] ==  'ananya17020@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        # log in the mentor and mentee and get the logged in user object
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
       
        # get the mentor object for the logged in user
        self.mentor = CustomUser.objects.get(email=self.login_mentor['email']).mentor

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

        #Logging in the second mentor and making him available to get the mentorship request too
        self.client.login(email=self.login_mentor2['email'], password=self.login_mentor2['password'])
        self.mentor2 = CustomUser.objects.get(email=self.login_mentor2['email']).mentor

        # Making mentor2 available to take mentorship request from all types of mentees
        response = self.client.patch(f'/api/mentor/mentor/{self.mentor2.uid}/', data=self.data, content_type='application/json', follow=True)
        self.client.logout()


        #logging in the mentee to send the mentor a mentorship request to original mentor
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


    def test_involved_mentor_responds_accepted(self):
        #logging in the mentor to accept the request
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        mentorship_req_uid= self.mentorship_req.uid

        respond_data = {
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'status' : MentorshipRequestStatus.REQUEST_ACCEPTED ,#Accepting the request.,
            'accepted' : True   #added field to accept
        }

        response = self.client.post(f'/api/mentorship/request/{mentorship_req_uid}/respond/',data=respond_data ) 
        self.assertEqual(response.status_code, 200)     #Successfully accept mentorship request
        self.mentorship_req.refresh_from_db()
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_ACCEPTED)  #Successfully accept mentorship request in db too
        self.client.logout()



    def test_involved_mentor_responds_rejected(self):

        #logging in the mentor to reject the request
        self.client.login(email=self.login_mentor['email'], password=self.login_mentor['password'])
        mentorship_req_uid= self.mentorship_req.uid

        respond_data = {
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'status' : MentorshipRequestStatus.REQUEST_REJECTED ,#Rejecting the request.,
            'reject_reason' : " Rejecting to test rejection from involved mentor.",
            'accepted' : False   #added field to accept
        }

        response = self.client.post(f'/api/mentorship/request/{mentorship_req_uid}/respond/',data=respond_data ) 
        self.assertEqual(response.status_code, 200)     #Successfully Reject mentorship request
        self.mentorship_req.refresh_from_db()
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_REJECTED) 
        self.client.logout()


    def test_uninvolved_mentor_responds_rejected(self):
        
        #logging in as the mentor2 to try to reject the request
        self.client.login(email=self.login_mentor2['email'], password=self.login_mentor2['password'])
        mentorship_req_uid= self.mentorship_req.uid

        respond_data = {
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'status' : MentorshipRequestStatus.REQUEST_REJECTED ,#Rejecting the request.,
            'reject_reason' : " Rejecting to test rejection from involved mentor.",
            'accepted' : False   #added field to accept
        }

        response = self.client.post(f'/api/mentorship/request/{mentorship_req_uid}/respond/',data=respond_data ) 
        self.assertEqual(response.status_code, 403)     #Forbidden access
        self.mentorship_req.refresh_from_db()
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_PENDING)  #Request still pending
        self.client.logout()


    def test_uninvolved_mentor_responds_accepted(self):
        
        #logging in as the mentor2 to try to  accept the request
        self.client.login(email=self.login_mentor2['email'], password=self.login_mentor2['password'])
        mentorship_req_uid= self.mentorship_req.uid

        respond_data = {
            'mentor': self.mentor.uid,
            'mentee': self.mentee.uid,
            'status' : MentorshipRequestStatus.REQUEST_ACCEPTED ,#Rejecting the request.,
            'accepted' : True   #added field to accept
        }

        response = self.client.post(f'/api/mentorship/request/{mentorship_req_uid}/respond/',data=respond_data ) 
        self.assertEqual(response.status_code, 403)     #Forbidden access
        self.mentorship_req.refresh_from_db()
        self.assertEqual(self.mentorship_req.status,MentorshipRequestStatus.REQUEST_PENDING)  #Request still pending 
        self.client.logout()
