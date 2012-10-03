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
        if self.smpl is not None:
            dbapi.delete_sample(self.smpl)
        if self.ds is not None:
            dbapi.delete_datasource(self.ds)
        if self.agent is not None:
            dbapi.delete_agent(self.agent)
        if self.user is not None:
            dbapi.delete_user(self.user)
        
    def test_user_creation(self):
        self.user = dbapi.create_user(self.username, self.password)
        self.assertGreater(self.user, 0, "test_user_creation uid>0")
    
    def test_user_duplicate(self):
        self.user = dbapi.create_user(self.username, self.password)
        self.assertRaises(exceptions.AlreadyExistingUserError, dbapi.create_user, self.username, self.password)

    def test_user_not_found(self):
        self.assertRaises(exceptions.NotFoundUserError, dbapi.User, self.username)
        
    def test_agent_creation(self):
        self.user = dbapi.create_user(self.username, self.password)
        self.agent = dbapi.create_agent(self.username, self.agentname, self.password)
        self.assertGreater(self.agent, 0, "test_agent_creation aid>0")
    

    
        
if __name__ == '__main__':
    unittest.main()
