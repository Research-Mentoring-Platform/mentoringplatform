import json
import logging

from django.test import TestCase
from rest_framework import status
from users.models import CustomUser
from mentee.models import Mentee, MenteeDepartment, MenteeDesignation, MenteeDiscipline

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
        response = self.client.put(f'/api/mentee/mentee/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mentee_updates_different_profile(self):
        """ tests the response when mentee updates a different mentee's profile """
        m_user = CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        m_uid = m_user.mentee.uid
        response = self.client.put(f'/api/mentee/mentee/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentee_updates_invalid_profile(self):
        """ tests the response when mentee updates an invalid profile """
        m_uid = "abcdef"
        response = self.client.put(f'/api/mentee/mentee/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)