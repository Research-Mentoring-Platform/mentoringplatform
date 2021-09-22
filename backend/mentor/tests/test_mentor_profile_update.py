from mentor.models import Mentor
from users.models import CustomUser
import logging, json
from django.test import TestCase
from rest_framework import status

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
        # log in the mentor
        self.client.login(email= self.login_user['email'], password=self.login_user['password'])

        # get list of all mentors in the database
        res = self.client.get('/api/mentor/mentor', follow=True)
        self.mentors = json.loads(res.content)
        self.user = CustomUser.objects.get(email=self.login_user['email'])

        # get the mentor object with the same user uid as the logged in user
        for mentor in self.mentors:
            if str(mentor['user']) == str(self.user.uid):
                self.mentor = mentor

        # get list of all mentor designations
        res = self.client.get('/api/mentor/designation', format='json', follow=True)
        self.designation = str(json.loads(res.content)[0]['uid'])

        # get list of all mentor departments
        res = self.client.get('/api/mentor/department', format='json', follow=True)
        self.department = str(json.loads(res.content)[1]['uid'])

        # get list of all mentor disciplines
        res = self.client.get('/api/mentor/discipline', format='json', follow=True)
        self.discipline = str(json.loads(res.content)[14]['uid'])

        # construct a profile data object which contains all the mentor fields to be modified
        self.data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': self.department,      # mandatory field
            'discipline': self.discipline,      # mandatory field
            'designation': self.designation,    # mandatory field
            'specialization': 'lorem ipsum',
            'expected_min_mentorship_duration': 2,
            'expected_max_mentorship_duration': 4,
            'is_accepting_mentorship_requests': False
        }

    def test_mentor_updates_own_profile(self):
        """ tests the response when mentor updates own profile """
        m_uid = self.mentor['uid']
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mentor_updates_different_profile(self):
        """ tests the response when mentor updates a different mentor's profile """
        m_uid = str(self.mentors[1]['uid'])
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_updates_invalid_profile(self):
        """ tests the response when mentor updates an invalid profile """
        m_uid = "abcdef"
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
