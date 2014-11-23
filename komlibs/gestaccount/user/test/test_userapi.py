import unittest
from komlibs.gestaccount.user import api

class GestaccountUserApiTest(unittest.TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.email = 'test_user@komlog.org'

    def test_create_user(self):
        user = api.create_user(username=self.username, password=self.password, email=self.email)
        self.assertEqual(self.username, user.username)
        self.assertEqual(api.get_hpassword(user.uid,self.password), user.password)
        self.assertEqual(self.email, user.email)

