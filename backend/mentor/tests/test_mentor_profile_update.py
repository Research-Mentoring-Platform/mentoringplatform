from users.models import CustomUser
import logging, random, json
from django.test import TestCase
from rest_framework import status


class MentorProfileUpdateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)


    @classmethod
    def tearDownClass(self):
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
        des = json.loads(res.content)
        self.designation = str(des[random.randint(0, len(des) - 1)]['uid'])

        res = self.client.get('/api/mentor/department', format='json', follow=True)
        deptt = json.loads(res.content)
        self.department = str(deptt[random.randint(0, len(deptt) - 1)]['uid'])

        res = self.client.get('/api/mentor/discipline', format='json', follow=True)
        disc = json.loads(res.content)
        self.discipline = str(disc[random.randint(0, len(disc) - 1)]['uid'])


    def test_mentor_updates_own_profile(self):
        """ tests that the mentor is updating their own profile only """
        data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': self.department,
            'discipline': self.discipline,
            'designation': self.designation,
            'specialization': 'lorem ipsum',
            'expected_min_mentorship_duration': 2,
            'expected_max_mentorship_duration': 4,
            'is_accepting_mentorship_requests': False
        }

        idx = random.randint(0, len(self.mentors) - 1)
        m_uid = str(self.mentors[idx]['uid'])
        response = self.client.put(f'/api/mentor/mentor/{m_uid}', data, content_type='application/json', follow=True)

        if m_uid == str(self.mentor['uid']):
            self.assertEquals(response.status_code, status.HTTP_200_OK)
        else:
            print(response.status_code)
            self.assertNotEquals(response.status_code, status.HTTP_200_OK)
