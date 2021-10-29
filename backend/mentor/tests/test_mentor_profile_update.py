import json, uuid, logging, random

from django.db.models import Q
from django.test import TestCase
from rest_framework import status
from users.models import CustomUser
from mentor.models import MentorDepartment, MentorDesignation, MentorDiscipline
from mentee.models import MenteeDepartment, MenteeDesignation, MenteeDiscipline


class MentorProfileUpdateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # select a mentor from the test_users.json list to login for tests
        with open('config/test_users.json') as f:
            users_data = json.load(f)['users']
            cls.login_user = next(user for user in users_data if user['email'] == 'prince17080@iiitd.ac.in')
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        # log in the mentor and get the logged in user object
        self.client.login(email=self.login_user['email'], password=self.login_user['password'])

        # get the mentor object for the logged in user
        self.mentor = CustomUser.objects.get(email=self.login_user['email']).mentor

        # get a designation, department, discipline that are different from the mentor's values
        desig_uid = next(d for d in list(MentorDesignation.objects.all()) if d.uid != self.mentor.designation).uid
        deptt_uid = next(d for d in list(MentorDepartment.objects.all()) if d.uid != self.mentor.department).uid
        disc_uid = next(d for d in list(MentorDiscipline.objects.all()) if d.uid != self.mentor.discipline).uid

        # construct a profile data object which contains all the mentor fields to be modified
        self.data = {
            'about_self': 'Fugiat ad id ut ullamco commodo irure duis reprehenderit reprehenderit irure non in ex Lorem.',
            'department': deptt_uid,        # mandatory field
            'discipline': disc_uid,         # mandatory field
            'designation': desig_uid,       # mandatory field
            'specialization': 'lorem ipsum',
        }

    def test_mentor_updates_own_profile(self):
        """ tests the response when mentor updates own profile """
        m_uid = self.mentor.uid

        # mentor's data before the PATCH request
        prev_data = {
            'about_self': self.mentor.about_self,
            'department': self.mentor.department.uid,
            'designation': self.mentor.designation.uid,
            'discipline': self.mentor.discipline.uid,
            'specialization': self.mentor.specialization,
        }

        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mentor.refresh_from_db()

        self.assertEqual(self.mentor.about_self, prev_data['about_self'])
        self.assertEqual(self.mentor.department.uid, prev_data['department'])
        self.assertEqual(self.mentor.discipline.uid, prev_data['discipline'])
        self.assertEqual(self.mentor.designation.uid, prev_data['designation'])
        self.assertEqual(self.mentor.specialization, prev_data['specialization'])

    def test_mentor_updates_different_profile(self):
        """ tests the response when mentor updates a different mentor's profile """
        m_user = CustomUser.objects.get(email='ananya17020@iiitd.ac.in')
        diff_mentor = m_user.mentor

        # mentor's data before the PATCH request
        prev_data = {
            'about_self': diff_mentor.about_self,
            'department': diff_mentor.department.uid,
            'designation': diff_mentor.designation.uid,
            'discipline': diff_mentor.discipline.uid,
            'specialization': diff_mentor.specialization,
        }

        response = self.client.patch(f'/api/mentor/mentor/{diff_mentor.uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        diff_mentor.refresh_from_db()

        self.assertEqual(diff_mentor.about_self, prev_data['about_self'])
        self.assertEqual(diff_mentor.department.uid, prev_data['department'])
        self.assertEqual(diff_mentor.discipline.uid, prev_data['discipline'])
        self.assertEqual(diff_mentor.designation.uid, prev_data['designation'])
        self.assertEqual(diff_mentor.specialization, prev_data['specialization'])

    def test_mentor_updates_invalid_profile(self):
        """ tests the response when mentor updates an invalid profile """
        m_uid = uuid.uuid4()
        response = self.client.patch(f'/api/mentor/mentor/{m_uid}/', data=self.data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mentor_updates_mentee_profile(self):
        """ tests the response when mentor updates a mentee's profile """
        m_user = CustomUser.objects.get(email='karan17058@iiitd.ac.in')
        mentee = m_user.mentee
        m_uid = mentee.uid

        # mentee's data before the PATCH request
        prev_data = {
            'about_self': mentee.about_self,
            'department': mentee.department.uid,
            'discipline': mentee.discipline.uid,
            'designation': mentee.designation.uid,
            'specialization': mentee.specialization,
        }

        # get a designation, department, discipline that are different from the mentee's values
        desig_uid = next(d for d in list(MenteeDesignation.objects.all()) if d.uid != mentee.designation).uid
        deptt_uid = next(d for d in list(MenteeDepartment.objects.all()) if d.uid != mentee.department).uid
        disc_uid = next(d for d in list(MenteeDepartment.objects.all()) if d.uid != mentee.discipline).uid

        mentee_data = {
            'about_self': self.data['about_self'],
            'department': deptt_uid,
            'discipline': disc_uid,
            'designation': desig_uid,
            'specialization': 'lorem ipsum',
        }

        response = self.client.patch(f'/api/mentee/mentee/{m_uid}/', data=mentee_data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        mentee.refresh_from_db()

        self.assertEqual(mentee.about_self, prev_data['about_self'])
        self.assertEqual(mentee.department.uid, prev_data['department'])
        self.assertEqual(mentee.discipline.uid, prev_data['discipline'])
        self.assertEqual(mentee.designation.uid, prev_data['designation'])
        self.assertEqual(mentee.specialization, prev_data['specialization'])
