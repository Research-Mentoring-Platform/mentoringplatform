from mentor.models import Mentor
from users.models import CustomUser
import logging, json
from django.test import TestCase
from rest_framework import status

class MentorProfileUpdateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        data = {
            'email': 'prince17080@iiitd.ac.in',
            'password': 'pass4321'
        }
        self.client.login(**data)

        res = self.client.get('/api/mentor/mentor', follow=True)
        self.mentors = json.loads(res.content)
        self.user = CustomUser.objects.get(email=data['email'])
        for mentor in self.mentors:
            if str(mentor['user']) == str(self.user.uid):
                self.mentor = mentor

        res = self.client.get('/api/mentor/designation', format='json', follow=True)
        self.designation = str(json.loads(res.content)[0]['uid'])

        res = self.client.get('/api/mentor/department', format='json', follow=True)
        self.department = str(json.loads(res.content)[1]['uid'])

        res = self.client.get('/api/mentor/discipline', format='json', follow=True)
        self.discipline = str(json.loads(res.content)[14]['uid'])

        self.data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': self.department,
            'discipline': self.discipline,
            'designation': self.designation,
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
