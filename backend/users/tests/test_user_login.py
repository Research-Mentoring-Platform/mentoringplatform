import logging
import unittest
from django.test.testcases import TestCase
from users.models import CustomUser

Test_User_1 = {
    'username' : 'test_user1',
    'email' : 'hello@gmail.com',
    'first_name' : 'test_mentor',
    'password':'pass4321',
    'last_name' : 'last_name',
    'date_of_birth': '2001-08-07',
    'is_mentor': True,
    'email_verified' : True
}
Test_User_2 = {
    'username' : 'test_user2',
    'email' : 'hello123@gmail.com',
    'first_name' : 'test_mentee',
    'password':'pass4321',
    'last_name' : 'last_name',
    'date_of_birth': '2001-08-07',
    'is_mentee': True,
    'email_verified' : True
}
Test_User_3= {
    'username':'test_user3',
    'password':'pass4321',
    'email':'hello456@gmail.com',
    'first_name':'unverify_test_mentor',
    'last_name':'last_name',
    'date_of_birth':'2001-08-07',
    'is_mentor':True
}
Test_User_4 ={
    'username':'test_user4',
    'password':'pass4321',
    'email':'hello789@gmail.com',
    'first_name':'unverify_test_mentee',
    'last_name':'last_name',
    'date_of_birth':'2001-08-07',
    'is_mentee':True
}
class LoginTestCases(TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        cls.test_mentor=CustomUser(**Test_User_1)
        cls.test_mentor.set_password(Test_User_1['password'])
        cls.test_mentor.save()
        tc=unittest.TestCase()
        tc.assertNotEqual(cls.test_mentor.password,"pass4321")
        cls.test_mentee=CustomUser(**Test_User_2)
        cls.test_mentee.set_password(Test_User_2['password'])
        cls.test_mentee.save()
        tc.assertNotEqual(cls.test_mentee.password,"pass4321")
        cls.unverified_test_mentor=CustomUser(**Test_User_3)
        cls.unverified_test_mentor.set_password(Test_User_3['password'])
        cls.unverified_test_mentor.save()
        tc.assertNotEqual(cls.unverified_test_mentor.password,"pass4321")
        cls.unverified_test_mentee=CustomUser(**Test_User_4)
        cls.unverified_test_mentee.set_password(Test_User_4['password'])
        cls.unverified_test_mentee.save()
        tc.assertNotEqual(cls.unverified_test_mentee.password,"pass4321")
        super().setUpClass()
       

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        LoginTestCases.test_mentor.delete()
        LoginTestCases.test_mentee.delete()
        LoginTestCases.unverified_test_mentor.delete()
        LoginTestCases.unverified_test_mentee.delete()    
        return super().tearDownClass()
    
    def test_verified_mentor_login(self):
        data={
            'email' : self.test_mentor.email, 
            'password' : 'pass4321'
        }
        response=self.client.post('/api/users/token/',data=data)
        self.assertEqual(response.status_code,200) 

    def test_verified_mentee_login(self):
        data={
            'email' : self.test_mentee.email,
            'password' : 'pass4321'
        }
        response=self.client.post('/api/users/token/',data=data)
        self.assertEqual(response.status_code,200) 
        
    def test_unverified_mentor_login(self):
        data={
            'email' : self.unverified_test_mentor.email,
            'password' : 'pass4321'
        }
        response=self.client.post('/api/users/token/',data=data)
        self.assertEqual(response.status_code,400) 
        
    def test_unverified_mentee_login(self):
        data={
            'email' : self.unverified_test_mentee.email,
            'password' : 'pass4321'
        }
        response=self.client.post('/api/users/token/',data=data)
        self.assertEqual(response.status_code,400)

    def test_invalid_credentials(self):
        data={
            'email' : 'reeshabh17086@iiitd.ac.in',
            'password' : 'apass4321'
        }
        response=self.client.post('/api/users/token/',data=data)
        self.assertEqual(response.status_code,401) 
        
    def test_non_existing_account_login(self):
        data={
            'email' : 'random_unregistered@iiithyderabad.ac.in',
            'password' : 'randompass'
        }
        response=self.client.post('/api/users/token/',data=data)
        self.assertEqual(response.status_code,401)
