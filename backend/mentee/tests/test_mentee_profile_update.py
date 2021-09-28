import json
import logging

from django.test import TestCase
from rest_framework import status
from users.models import CustomUser
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline

class MenteeProfileUpdateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_user = next(user for user in users_data if user['email'] ==  'reeshabh17086@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        # log in the mentee and get the logged in user object
        self.client.login(email=self.login_user['email'], password=self.login_user['password'])

        # get the mentee object for the logged in user
        self.mentee = CustomUser.objects.get(email=self.login_user['email']).mentee

        # get the mentee designation, department and discipline uids
        desig_uid = MenteeDesignation.objects.get(label='Industry Researcher').uid
        deptt_uid = MenteeDepartment.objects.get(label='Computer Science and Design').uid
        disc_uid= MenteeDiscipline.objects.get(label='Human-Computer Interaction').uid

        # # construct a profile data object which contains all the mentee fields to be modified
        self.data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
            'specialization': 'lorem ipsum',
        }

    def test_mentee_updates_own_profile(self):
        """ tests the response when mentee updates own profile """
        m_uid = self.mentee.uid
        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mentee = Mentee.objects.get(uid=m_uid)
        self.assertEqual(mentee.about_self, self.data['about_self'])
        self.assertEqual(mentee.department.uid, self.data['department'])
        self.assertEqual(mentee.discipline.uid, self.data['discipline'])
        self.assertEqual(mentee.designation.uid, self.data['designation'])
        self.assertEqual(mentee.specialization, self.data['specialization'])

    def test_mentee_updates_different_profile(self):
        """ tests the response when mentee updates a different mentee's profile """
        m_user = CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        m_uid = m_user.mentee.uid
        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        diff_mentee = Mentee.objects.get(uid=m_uid)
        self.assertNotEqual(diff_mentee.about_self, self.data['about_self'])
        if m_user.mentee.department.uid != self.data['department']:
            self.assertNotEqual(diff_mentee.department.uid, self.data['department'])
        if m_user.mentee.discipline.uid != self.data['discipline']:
            self.assertNotEqual(diff_mentee.discipline.uid, self.data['discipline'])
        if m_user.mentee.designation.uid != self.data['designation']:
            self.assertNotEqual(diff_mentee.designation.uid, self.data['designation'])
        self.assertNotEqual(diff_mentee.specialization, self.data['specialization'])

    def test_mentee_updates_invalid_profile(self):
        """ tests the response when mentee updates an invalid profile """
        m_uid = "abcdef"
        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mentee_updates_mentor_profile(self):
        """ tests the response when mentee updates a mentor's profile """
        m_user = CustomUser.objects.get(email='shaurya17104@iiitd.ac.in')
        m_uid = m_user.mentor.uid
        mentor_data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': MentorDepartment.objects.get(label='Computer Science and Design').uid,
            'discipline': MentorDiscipline.objects.get(label='Human-Computer Interaction').uid,
            'designation': MentorDesignation.objects.get(label='Industry Researcher').uid,
            'specialization': 'lorem ipsum'
        }
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=mentor_data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mentor = Mentor.objects.get(uid=m_uid)
        self.assertNotEqual(mentor.about_self, mentor_data['about_self'])
        if m_user.mentor.department.uid != mentor_data['department']:
            self.assertNotEqual(mentor.department.uid, mentor_data['department'])
        if m_user.mentor.designation.uid != mentor_data['designation']:
            self.assertNotEqual(mentor.designation.uid, mentor_data['designation'])
        if m_user.mentor.discipline.uid != mentor_data['discipline']:
            self.assertNotEqual(mentor.discipline.uid, mentor_data['discipline'])
        self.assertNotEqual(mentor.specialization, mentor_data['specialization'])
