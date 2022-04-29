import json
import logging

from users.models import CustomUser
from mentor.models import  Mentor
from mentee.models import Mentee,MenteeDesignation
from mentorship.models import MentorshipRequest,Mentorship, MentorshipRequestStatus
from django.test.testcases import TestCase

class mentee_view_only_involved_mentorships(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('config/test_users.json') as f:
            user_data=json.load(f)['users']
            cls.login_mentor1=next(user for user in user_data if user['email']=='prince17080@iiitd.ac.in')
            cls.login_mentor2=next(user for user in user_data if user['email']=='shaurya17104@iiitd.ac.in')
            cls.login_mentee1=next(user for user in user_data if user['email']=='reeshabh17086@iiitd.ac.in')
            cls.login_mentee2=next(user for user in user_data if user['email']=='karan17058@iiitd.ac.in')
        logging.disable(logging.CRITICAL)


        
        return super().setUpClass()


    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()
    
    def setUp(self) -> None:
        '''
        Mentorship 1: Mentor 1 -> Mentee 1
        Mentorship 2: Mentor 1 -> Mentee 2
        Mentorship 3: Mentor 2 -> Mentee 2    
        ''' 
        #Login Mentor 1 and add accepted types
        self.client.login(email=self.login_mentor1['email'],password=self.login_mentor1['password'])
        self.mentor1=CustomUser.objects.get(email=self.login_mentor1['email']).mentor
    
        accepted_mentee_types=[des.uid for des in MenteeDesignation.objects.all()]
    
        deptt_uid=self.mentor1.department.uid
        disc_uid=self.mentor1.discipline.uid
        desig_uid=self.mentor1.designation.uid
        self.data = {
            'accepted_mentee_types': accepted_mentee_types,  
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
        }
        
        response = self.client.patch(f'/api/mentor/mentor/{self.mentor1.uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code,200)
        self.client.logout()


        #Login Mentor 2 and add accepted types
        self.client.login(email=self.login_mentor2['email'],password=self.login_mentor2['password'])
        self.mentor2=CustomUser.objects.get(email=self.login_mentor2['email']).mentor
    
        accepted_mentee_types=[des.uid for des in MenteeDesignation.objects.all()]
    
        deptt_uid=self.mentor2.department.uid
        disc_uid=self.mentor2.discipline.uid
        desig_uid=self.mentor2.designation.uid
        self.data = {
            'accepted_mentee_types': accepted_mentee_types,  
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
        }
        
        response = self.client.patch(f'/api/mentor/mentor/{self.mentor2.uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code,200)
        self.client.logout()



        #Login Mentee 1
        self.client.login(email=self.login_mentee1['email'],password=self.login_mentee1['password'])
        self.mentee1=CustomUser.objects.get(email=self.login_mentee1['email']).mentee

        request_data1 = {
            "mentor": self.mentor1.uid,
            "mentee": self.mentee1.uid,
            "statement_of_purpose": "Bazinga",
            "expectations": "Bazinga",
            "commitment": "Bazinga",
        }


        response=self.client.post(f'/api/mentorship/request/',data=request_data1)
        self.assertEqual(response.status_code,201)
        self.mentorship_request1=MentorshipRequest.objects.get(mentor=self.mentor1,mentee=self.mentee1)
        
        self.assertEqual(self.mentorship_request1.status,MentorshipRequestStatus.REQUEST_PENDING)
        self.client.logout()

        

        #Login Mentee 2
        self.client.login(email=self.login_mentee2['email'],password=self.login_mentee2['password'])
        self.mentee2=CustomUser.objects.get(email=self.login_mentee2['email']).mentee

        request_data2 = {
            "mentor": self.mentor1.uid,
            "mentee": self.mentee2.uid,
            "statement_of_purpose": "Bazinga",
            "expectations": "Bazinga",
            "commitment": "Bazinga",
        }


        response=self.client.post(f'/api/mentorship/request/',data=request_data2)
        self.assertEqual(response.status_code,201)
        self.mentorship_request2=MentorshipRequest.objects.get(mentor=self.mentor1,mentee=self.mentee2)
        self.assertEqual(self.mentorship_request2.status,MentorshipRequestStatus.REQUEST_PENDING)
        
        request_data3= {
            "mentor": self.mentor2.uid,
            "mentee": self.mentee2.uid,
            "statement_of_purpose": "Bazinga",
            "expectations": "Bazinga",
            "commitment": "Bazinga",
        }


        response=self.client.post(f'/api/mentorship/request/',data=request_data3)
        self.assertEqual(response.status_code,201)
        self.mentorship_request3=MentorshipRequest.objects.get(mentor=self.mentor2,mentee=self.mentee2)
        self.assertEqual(self.mentorship_request3.status,MentorshipRequestStatus.REQUEST_PENDING)
        
        
        self.client.logout()
        
        
        #Login mentor 1 again and accept the mentorships
        self.client.login(email=self.login_mentor1['email'],password=self.login_mentor1['password'])
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_request1.uid}/respond/', data={'accepted':True}, follow=True)
        self.assertEqual(response.status_code,200)
        
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_request2.uid}/respond/', data={'accepted':True}, follow=True)
        self.assertEqual(response.status_code,200)
        
        
        
        self.mentorship1=Mentorship.objects.get(mentor=self.mentor1,mentee=self.mentee1)
        self.mentorship2=Mentorship.objects.get(mentor=self.mentor1,mentee=self.mentee2)
        
        self.client.logout()

        #Login mentor 2 again and accept the mentorship
        self.client.login(email=self.login_mentor2['email'],password=self.login_mentor2['password'])
        response = self.client.post(f'/api/mentorship/request/{self.mentorship_request3.uid}/respond/', data={'accepted':True}, follow=True)
        self.assertEqual(response.status_code,200)

        self.mentorship3=Mentorship.objects.get(mentor=self.mentor2,mentee=self.mentee2)
        self.client.logout()

        return super().setUp()

    def test_mentee_view_involved_mentorships(self):
        #Login as mentee1 and view mentorships
        self.client.login(email=self.login_mentee1['email'],password=self.login_mentee1['password'])
        response=self.client.get(f'/api/mentorship/mentorship/')
        self.assertTrue(response.status_code,200)
        
        mentorship_uids=[res['uid'] for res in response.json()]
        self.assertTrue(str(self.mentorship1.uid) in mentorship_uids)
        self.assertFalse(str(self.mentorship2.uid) in mentorship_uids)
        self.assertFalse(str(self.mentorship3.uid) in mentorship_uids)
        
        self.client.logout()

        #Login as mentee2 and view mentorships
        self.client.login(email=self.login_mentee2['email'],password=self.login_mentee2['password'])
        response=self.client.get(f'/api/mentorship/mentorship/')
        self.assertTrue(response.status_code,200)
        
        mentorship_uids=[res['uid'] for res in response.json()]
        self.assertFalse(str(self.mentorship1.uid) in mentorship_uids)
        self.assertTrue(str(self.mentorship2.uid) in mentorship_uids)
        self.assertTrue(str(self.mentorship3.uid) in mentorship_uids)
        
        self.client.logout()

    def test_mentor_view_involved_mentorships(self):
        #Login as mentor1 and view mentorships
        self.client.login(email=self.login_mentor1['email'],password=self.login_mentor1['password'])
        response=self.client.get(f'/api/mentorship/mentorship/')
        self.assertTrue(response.status_code,200)
        
        mentorship_uids=[res['uid'] for res in response.json()]
        self.assertTrue(str(self.mentorship1.uid) in mentorship_uids)
        self.assertTrue(str(self.mentorship2.uid) in mentorship_uids)
        self.assertFalse(str(self.mentorship3.uid) in mentorship_uids)
        
        self.client.logout()

        #Login as mentor2 and view mentorships
        self.client.login(email=self.login_mentor2['email'],password=self.login_mentor2['password'])
        response=self.client.get(f'/api/mentorship/mentorship/')
        self.assertTrue(response.status_code,200)
        
        mentorship_uids=[res['uid'] for res in response.json()]
        self.assertFalse(str(self.mentorship1.uid) in mentorship_uids)
        self.assertFalse(str(self.mentorship2.uid) in mentorship_uids)
        self.assertTrue(str(self.mentorship3.uid) in mentorship_uids)
        
        self.client.logout()


