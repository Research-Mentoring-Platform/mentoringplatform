import json
import logging

from django.test import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline


class MentorProfileUpdateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # select a mentor from the test_users.json list to login for tests
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

    def test_mentor_updates_own_profile(self):
        """ tests the response when mentor updates own profile """
        m_uid = self.mentor.uid
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        mentor = Mentor.objects.get(uid=m_uid)

        self.assertEqual(mentor.about_self, self.data['about_self'])
        self.assertEqual(mentor.department.uid, self.data['department'])
        self.assertEqual(mentor.discipline.uid, self.data['discipline'])
        self.assertEqual(mentor.designation.uid, self.data['designation'])
        self.assertEqual(mentor.specialization, self.data['specialization'])
        self.assertEqual(mentor.expected_min_mentorship_duration, self.data['expected_min_mentorship_duration'])
        self.assertEqual(mentor.expected_max_mentorship_duration, self.data['expected_max_mentorship_duration'])
        self.assertEqual(mentor.is_accepting_mentorship_requests, self.data['is_accepting_mentorship_requests'])

    def test_mentor_updates_different_profile(self):
        """ tests the response when mentor updates a different mentor's profile """
        m_user = CustomUser.objects.get(email='ananya17020@iiitd.ac.in')
        m_uid = m_user.mentor.uid
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        diff_mentor = Mentor.objects.get(uid=m_uid)
        self.assertNotEqual(diff_mentor.about_self, self.data['about_self'])
        if m_user.mentor.department.uid != self.data['department']:
            self.assertNotEqual(diff_mentor.department.uid, self.data['department'])
        if m_user.mentor.discipline.uid != self.data['discipline']:
            self.assertNotEqual(diff_mentor.discipline.uid, self.data['discipline'])
        if m_user.mentor.designation.uid != self.data['designation']:
            self.assertNotEqual(diff_mentor.designation.uid, self.data['designation'])
        self.assertNotEqual(diff_mentor.specialization, self.data['specialization'])
        if m_user.mentor.expected_min_mentorship_duration != self.data['expected_min_mentorship_duration']:
            self.assertNotEqual(diff_mentor.expected_min_mentorship_duration, self.data['expected_min_mentorship_duration'])
        if m_user.mentor.expected_max_mentorship_duration != self.data['expected_max_mentorship_duration']:
            self.assertNotEqual(diff_mentor.expected_max_mentorship_duration, self.data['expected_max_mentorship_duration'])
        if m_user.mentor.is_accepting_mentorship_requests != self.data['is_accepting_mentorship_requests']:
            self.assertNotEqual(diff_mentor.is_accepting_mentorship_requests, self.data['is_accepting_mentorship_requests'])


    def test_mentor_updates_invalid_profile(self):
        """ tests the response when mentor updates an invalid profile """
        m_uid = "abcdef"
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mentor_updates_mentee_profile(self):
        """ tests the response when mentor updates a mentee's profile """
        m_user = CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        m_uid = m_user.mentee.uid
        mentee_data = {
            'about_self': self.data['about_self'],
            'department': MenteeDepartment.objects.get(label='Computer Science and Design').uid,
            'discipline': MenteeDiscipline.objects.get(label='Operating Systems').uid,
            'designation': MenteeDesignation.objects.get(label='MTech').uid,
            'specialization': 'lorem ipsum',
        }
        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=mentee_data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mentee = Mentee.objects.get(uid=m_uid)
        self.assertNotEqual(mentee.about_self, mentee_data['about_self'])
        if m_user.mentee.department.uid != self.data['department']:
            self.assertNotEqual(mentee.department.uid, mentee_data['department'])
        if m_user.mentee.discipline.uid != self.data['discipline']:
            self.assertNotEqual(mentee.discipline.uid, mentee_data['discipline'])
        if m_user.mentee.designation.uid != self.data['designation']:
            self.assertNotEqual(mentee.designation.uid, mentee_data['designation'])
        self.assertNotEqual(mentee.specialization, mentee_data['specialization'])