import json
import logging

from django.test import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import Mentor, MentorDepartment, MentorDesignation, MentorDiscipline


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
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mentor_updates_different_profile(self):
        """ tests the response when mentor updates a different mentor's profile """
        m_user = CustomUser.objects.get(email='ananya17020@iiitd.ac.in')
        m_uid = m_user.mentor.uid
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_updates_invalid_profile(self):
        """ tests the response when mentor updates an invalid profile """
        m_uid = "abcdef"
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mentor_updates_mentee_profile(self):
        """ tests the response when mentor updates a mentee's profile """
        m_user = CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        m_uid = m_user.mentee.uid
        response = self.client.put(f'/api/mentee/mentee/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)