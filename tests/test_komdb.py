from komdb import api as dbapi
from komdb import exceptions

import unittest, random, string



class KomdbFunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.username = 'tUser'+''.join(random.choice(string.digits) for x in range(6))
        self.password = self.username
        self.agentname = 'tAgent'+''.join(random.choice(string.digits) for x in range(6))
        self.dsname = 'tDs'+''.join(random.choice(string.digits) for x in range(6))
        self.user = None
        self.agent = None
        self.ds = None
        self.smpl = None
        
    def tearDown(self):
        self.username = None
        self.password = None
        self.agentname = None
        self.dsname = None
        dbapi.delete_sample(self.smpl)
        dbapi.delete_datasource(self.ds)
        dbapi.delete_agent(self.agent)
        dbapi.delete_user(self.user)
        
    def test_user_creation(self):
        self.user = dbapi.create_user(self.username, self.password)
        self.assertGreater(self.user, 0, "test_user_creation uid>0")
    
    def test_user_duplicate(self):
        self.user = dbapi.create_user(self.username, self.password)
        self.assertRaises(exceptions.AlreadyExistingAgentError, dbapi.create_user(self.username, self.password))

    def test_user_not_found(self):
        user = dbapi.User(self.username)
        self.assertRaises(exceptions.NotFoundUserError, user)
        
if __name__ == '__main__':
    unittest.main()
