import json
import logging

from users.models import CustomUser
from mentor.models import  Mentor
from mentee.models import Mentee,MenteeDesignation
from mentorship.models import MentorshipRequest,Mentorship, MentorshipRequestStatus
from django.test.testcases import TestCase

class mentorship_rejection(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('config/test_users.json') as f:
            user_data=json.load(f)['users']
            cls.login_mentor=next(user for user in user_data if user['email']=='shaurya17104@iiitd.ac.in')
            cls.login_mentee=next(user for user in user_data if user['email']=='reeshabh17086@iiitd.ac.in')
        logging.disable(logging.CRITICAL)
        return super().setUpClass()


    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self):
        #Login Mentor and add accepted types
        self.client.login(email=self.login_mentor['email'],password=self.login_mentor['password'])
        self.mentor=CustomUser.objects.get(email=self.login_mentor['email']).mentor
        
        accepted_mentee_types=[des.uid for des in MenteeDesignation.objects.all()]
    
        deptt_uid=self.mentor.department.uid
        disc_uid=self.mentor.discipline.uid
        desig_uid=self.mentor.designation.uid
        self.data = {
            'accepted_mentee_types': accepted_mentee_types,  
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
        }
        
        response = self.client.patch(f'/api/mentor/mentor/{self.mentor.uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code,200)
        self.client.logout()

        #Login Mentee and make mentorship request
        self.client.login(email=self.login_mentee['email'],password=self.login_mentee['password'])
        self.mentee=CustomUser.objects.get(email=self.login_mentee['email']).mentee

        request_data= {
            "mentor": self.mentor.uid,
            "mentee": self.mentee.uid,
            "statement_of_purpose": "Bazinga",
            "expectations": "Bazinga",
            "commitment": "Bazinga",
        }

        response=self.client.post(f'/api/mentorship/request/',data=request_data)
        self.assertEqual(response.status_code,201)
        self.mentorship_request=MentorshipRequest.objects.get(mentor=self.mentor,mentee=self.mentee)
        self.client.logout()
        

    def test_rejected_without_reject_reason(self):
        #Login mentor and reject the mentorship without reject reason
        self.client.login(email=self.login_mentor['email'],password=self.login_mentor['password'])
        respond_data={
            'accepted':False,
            'reject_reason':' '
        }
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_request.uid}/respond/', data=respond_data, follow=True)
        self.assertEqual(response.status_code,400)
    
    def test_accepted_with_reject_reason(self):
        #Login mentor again and accept the mentorship with reject reason
        self.client.login(email=self.login_mentor['email'],password=self.login_mentor['password'])
        respond_data={
            'accepted':True,
            'reject_reason':'Bazinga! Now we are Even :D'
        }
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_request.uid}/respond/', data=respond_data, follow=True)
        self.assertEqual(response.status_code,400)
    




        