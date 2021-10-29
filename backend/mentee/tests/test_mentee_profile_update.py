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
        self.client.login(email=self.login_user['email'], password=self.login_user['password'])

        # get the mentee object for the logged in user
        self.mentee = CustomUser.objects.get(email=self.login_user['email']).mentee

        # get a designation, department, discipline that are different from the mentee's values
        desig_uid = next(d for d in list(MenteeDesignation.objects.all()) if d.uid != self.mentee.designation).uid
        deptt_uid = next(d for d in list(MenteeDepartment.objects.all()) if d.uid != self.mentee.department).uid
        disc_uid = next(d for d in list(MenteeDepartment.objects.all()) if d.uid != self.mentee.discipline).uid

        # # construct a profile data object which contains all the mentee fields to be modified
        self.data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
            'specialization': 'lorem ipsum',
        }

    def tearDown(self):
        self.client.logout()

    def test_mentee_updates_own_profile(self):
        """ tests the response when mentee updates own profile """
        m_uid = self.mentee.uid

        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mentee.refresh_from_db()

        self.assertEqual(self.mentee.about_self, self.data['about_self'])
        self.assertEqual(self.mentee.department.uid, self.data['department'])
        self.assertEqual(self.mentee.discipline.uid, self.data['discipline'])
        self.assertEqual(self.mentee.designation.uid, self.data['designation'])
        self.assertEqual(self.mentee.specialization, self.data['specialization'])

    def test_mentee_updates_different_profile(self):
        """ tests the response when mentee updates a different mentee's profile """
        m_user = CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        diff_mentee = m_user.mentee
        m_uid = diff_mentee.uid

        # mentor's data before the PATCH request
        prev_data = {
            'about_self': diff_mentee.about_self,
            'department': diff_mentee.department.uid,
            'designation': diff_mentee.designation.uid,
            'discipline': diff_mentee.discipline.uid,
            'specialization': diff_mentee.specialization,
        }

        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        diff_mentee.refresh_from_db()

        self.assertEqual(diff_mentee.about_self, prev_data['about_self'])
        self.assertEqual(diff_mentee.department.uid, prev_data['department'])
        self.assertEqual(diff_mentee.discipline.uid, prev_data['discipline'])
        self.assertEqual(diff_mentee.designation.uid, prev_data['designation'])
        self.assertEqual(diff_mentee.specialization, prev_data['specialization'])

    def test_mentee_updates_invalid_profile(self):
        """ tests the response when mentee updates an invalid profile """
        m_uid = "abcdef"
        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mentee_updates_mentor_profile(self):
        """ tests the response when mentee updates a mentor's profile """
        m_user = CustomUser.objects.get(email='shaurya17104@iiitd.ac.in')
        mentor = m_user.mentor

        # mentee's data before the PATCH request
        prev_data = {
            'about_self': mentor.about_self,
            'department': mentor.department.uid,
            'discipline': mentor.discipline.uid,
            'designation': mentor.designation.uid,
            'specialization': mentor.specialization,
        }

        # get a designation, department, discipline that are different from the mentor's values
        desig_uid = next(d for d in list(MentorDesignation.objects.all()) if d.uid != mentor.designation).uid
        deptt_uid = next(d for d in list(MentorDepartment.objects.all()) if d.uid != mentor.department).uid
        disc_uid = next(d for d in list(MentorDepartment.objects.all()) if d.uid != mentor.discipline).uid


        mentor_data = {
            'about_self': self.data['about_self'],
            'department': deptt_uid,
            'discipline': disc_uid,
            'designation': desig_uid,
            'specialization': 'lorem ipsum',
        }

        response = self.client.patch(f'/api/mentor/mentor/{mentor.uid}/', data=mentor_data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        mentor.refresh_from_db()

        self.assertEqual(mentor.about_self, prev_data['about_self'])
        self.assertEqual(mentor.department.uid, prev_data['department'])
        self.assertEqual(mentor.discipline.uid, prev_data['discipline'])
        self.assertEqual(mentor.designation.uid, prev_data['designation'])
        self.assertEqual(mentor.specialization, prev_data['specialization'])

    def test_mentee_updates_restricted_field(self):
        """ tests the response when mentee updates their rating (restricted) """
        prev_rating = self.mentee.rating
        m_uid = self.mentee.uid
        data = {
            'rating': 10
        }
        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 403)
        self.mentee.refresh_from_db()
        self.assertEqual(self.mentee.rating, prev_rating)
