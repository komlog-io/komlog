from komdb import api as dbapi

import unittest

class KomdbFunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.username = 'testUser'
        self.password = 'testUser'
    def tearDown(self):
        self.username = None
        self.password = None
    def test_user_creation(self):
        uid = dbapi.create_user(self.username, self.password)
        self.assertGreater(uid, 0, "test_user_creation uid>0")

if __name__ == '__main__':
    unittest.main()
