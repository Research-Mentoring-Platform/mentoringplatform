import json
import logging
from django.test import TransactionTestCase,TestCase
from django.test.testcases import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline


class CorrectlyUpdatingMentorProfileTestCase(TestCase):
    # Set up the mentor through which we will do the mentor profile testing.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_user = next(user for user in users_data if user['email'] ==  'prince17080@iiitd.ac.in')
        logging.disable(logging.CRITICAL)
   
    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        # log in the mentor and get the logged in user object
        self.client.login(email=self.login_user['email'], password=self.login_user['password'])

        # get the mentor object for the logged in user
        self.mentor = CustomUser.objects.get(email=self.login_user['email']).mentor

        # get the mentor designation, department and discipline uids
        desig_uid = MentorDesignation.objects.get(label='Industry Researcher').uid
        deptt_uid = MentorDepartment.objects.get(label='Computer Science and Design').uid
        disc_uid= MentorDiscipline.objects.get(label='Human-Computer Interaction').uid

    
        # construct a profile data object which contains all the mentor fields to be modified
        self.data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
            'specialization': 'lorem ipsum',
            'expected_min_mentorship_duration': 2,
            'expected_max_mentorship_duration': 4,
            'is_accepting_mentorship_requests': False
        }


    def test__invalid_discipline(self):
        # checking invalid discipline uid shouldn't work.

        temp=self.data['discipline']
        self.data['discipline']="Random-0----2"
        m_uid = self.mentor.uid
        mentor = Mentor.objects.get(uid=m_uid)
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.data['discipline']=temp
        # self.assertNotEqual(mentor.discipline.uid, self.data['discipline'])

    def test__invalid_designation(self):
        temp=self.data['designation']
        self.data['designation']="Random-0----2"
        m_uid = self.mentor.uid
        mentor = Mentor.objects.get(uid=m_uid)
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.data['designation']=temp
        # self.assertNotEqual(mentor.designation.uid, self.data['designation']) 

    def test__invalid_department(self):
       
        temp=self.data['department']
        self.data['department']="Random-0----2"
        m_uid = self.mentor.uid
        mentor = Mentor.objects.get(uid=m_uid)
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.data['department']=temp
        # self.assertNotEqual(mentor.department.uid, self.data['department']) 

    def test_exactmaxlength_specialization(self):
        # try passing exact 256 length in specialization

        temp=self.data['specialization']
        self.data['specialization']="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis,."
        m_uid = self.mentor.uid
        mentor = Mentor.objects.get(uid=m_uid)
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 200)
        mentor.refresh_from_db()
        # self.assertEqual(mentor.specialization, self.data['specialization'])
        self.data['specialization']=temp
    
    def test_abovemaxlength_specialization(self):
        # try passing more than 256 characters  in specialization

        temp=self.data['specialization']
        self.data['specialization']="Extraword Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis,."
        m_uid = self.mentor.uid
        mentor = Mentor.objects.get(uid=m_uid)
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 400)
        # self.assertNotEqual(mentor.specialization, self.data['specialization'])
        self.data['specialization']=temp
        # self.assertEqual(mentor.specialization, self.data['specialization'])
    
     
    