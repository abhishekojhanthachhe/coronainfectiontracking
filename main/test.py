from turtle import clear
from app import app
import unittest
import os
import sys
import string
import random
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
# import tempfile


class FlaskTestCase(unittest.TestCase):
    # Note that this test cases depend on your computer as well as well.

    def test_index_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type="html/text")
        self.assertIn(b'index', response.data)

    # # The login is successful for a user

    def test_user_login_successful(self):
        tester = app.test_client(self)
        response = tester.post(
            '/user_log', data=dict(username="adm1n", password="adm1n"), follow_redirects=True)
        self.assertIn(b'user_log', response.data)

    # # # # The login is not successful because of incorrect credentials
    def test_place_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/place_log', data=dict(username="wrong", password="right"), follow_redirects=True)
        self.assertIn(b'place_login', response.data)

    # # # # The login being successful
    def test_place_login_successful(self):
        tester = app.test_client(self)
        response = tester.post(
            '/place_log', data=dict(username="jac", password="jac"), follow_redirects=True)
        self.assertIn(b'place_login', response.data)

    def test_user(self):
        tester = app.test_client(self)
        response = tester.get('/user_login', content_type="html/text")
        self.assertIn(b'user_login', response.data)

    def test_place(self):
        tester = app.test_client(self)
        response = tester.get('/place_page', content_type="html/text")
        self.assertIn(b'place_page', response.data)

    def test_user_reg(self):
        tester = app.test_client(self)
        response = tester.get('/user_registration',
                              content_type="html/text")
        self.assertIn(b'user_registration', response.data)

    def test_place_login_successful(self):
        tester = app.test_client(self)
        response = tester.post(
            '/place_login', data=dict(username="jacobs", password="jacobs"), follow_redirects=True)
        self.assertIn(b'place_login', response.data)

    def test_user_login_successful(self):
        tester = app.test_client(self)
        response = tester.post(
            '/user_login', data=dict(username="jacobs", password="jacobs"), follow_redirects=True)
        self.assertIn(b'visitor_log', response.data)


# The login is successful because of correct credentials
    def test_user_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/user_login', data=dict(username="User", password="54321"), follow_redirects=True)
        self.assertIn(b'Invalid Credentials!', response.data)

    # The login is not successful because of incorrect credentials
    def test_user_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/user_login', data=dict(username="wrong", password="right"), follow_redirects=True)
        self.assertIn(b'Invalid Credentials!', response.data)
    
    # The login is successful because correct credentials
    def test_place_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/place_login', data=dict(username="12345", password="12345"), follow_redirects=True)
        self.assertIn(b'Invalid Credentials!', response.data)

    # The login is not successful because of incorrect credentials
    def test_place_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/place_login', data=dict(username="wrong1", password="wrong"), follow_redirects=True)
        self.assertIn(b'Invalid Credentials!', response.data)

    # User registration opens freely
    def test_place_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/register_place_page', content_type="html/text")
        self.assertIn(b'Place Register', response.data)

    # The login is successful because of correct credentials
    def test_place_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/login_place', data=dict(username="Place", password="qwerty"), follow_redirects=True)
        self.assertIn(b'Invalid Credentials!', response.data)

    # The login is not successful because of incorrect credentials
    def test_place_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/login_place', data=dict(username="wrong", password="wrongbut2nd"), follow_redirects=True)
        self.assertIn(b'Invalid Credentials!', response.data)


if __name__ == '__main__':
    unittest.main()