'''
Created on 29/09/2012

@author: jcazor
'''
import unittest, random, string
from komdb import api as dbapi
from komws import checkws, authws, procws
from komws import exceptions as wsex
from datetime import datetime


class komwsFunctionalTestCase(unittest.TestCase):


    def setUp(self):
        self.username = 'tUser'+''.join(random.choice(string.digits) for x in range(6))
        self.password = self.username
        self.agentname = 'tAgent'+''.join(random.choice(string.digits) for x in range(6))
        self.dsname = 'tDs'+''.join(random.choice(string.digits) for x in range(6))
        self.filecontent = "komws Functional TestCase"
        self.date = datetime.utcnow()
        self.uid = None
        self.aid = None
        self.did = None
        self.smpl = None

    def tearDown(self):
        self.username = None
        self.password = None
        self.agentname = None
        self.dsname = None
        dbapi.delete_sample(self.smpl)
        dbapi.delete_datasource(self.did)
        dbapi.delete_agent(self.aid)
        dbapi.delete_user(self.uid)


    def test_wsUploadSample_checkws_OK(self):
        """
        Fill in data structure and call checking
        """
        self.aid = 0
        self.did = 0
        
        data = {'username':self.username,'password':self.password,
                'agentid':self.aid,'datasourceid':self.did,'date':self.date,
                'filecontent':self.filecontent}
        
        self.assertTrue(checkws.wsupload_sample(data))

    def test_wsUploadSample_checkws_invalid_data(self):
        """
        Fill in data structure without one field and call checking
        """
        self.aid = 0
        self.did = 0
        
        data = {'password':self.password,
                'agentid':self.aid,'datasourceid':self.did,'date':self.date,
                'filecontent':self.filecontent}
        
        self.assertRaises(wsex.InvalidData, checkws.wsupload_sample(data))
        
    
    def test_wsUploadSample_authws_OK(self):
        """
        Authentication implies data to exist on DB, so, 
        first: create user, agent and datasource
        second: fill in data structure 
        third: call authws for authentication
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        self.did = dbapi.create_datasource(self.aid, self.dsname)
        
        data = {'username':self.username, 'password':self.password,
                'agentid':self.aid, 'datasourceid':self.did,
                'date':self.date, 'filecontent':self.filecontent}
              
        self.assertTrue(authws.wsupload_sample(data))
        
    def test_wsUploadSample_authws_authentication_error(self):
        """
        In this case, we use a faked datasourceid
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        
        data = {'username':self.username, 'password':self.password,
                'agentid':self.aid, 'datasourceid':0,
                'date':self.date, 'filecontent':self.filecontent}
              
        self.assertRaises(wsex.AuthenticationError, authws.wsupload_sample(data))
        

    
    def test_wsUploadSample_procws_OK(self):
        """
        Processing implies data to exist on DB, so, 
        first: create user, agent and datasource
        second: fill in data structure 
        third: call procws for authentication
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        self.did = dbapi.create_datasource(self.aid, self.dsname)
        
        data = {'username':self.username, 'password':self.password,
                'agentid':self.aid, 'datasourceid':self.did,
                'date':self.date, 'filecontent':self.filecontent}
              
        self.assertTrue(procws.wsupload_sample(data))

    def test_wsUploadSample_procws_processing_error(self):
        """
        In this case, we use a nonexistent datasourceid        
        """
        
        data = {'username':self.username, 'password':self.password,
                'agentid':self.aid, 'datasourceid':0,
                'date':self.date, 'filecontent':self.filecontent}
              
        self.assertRaises(wsex.ProcessingError, procws.wsupload_sample(data))

        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()