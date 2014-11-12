'''
Created on 29/09/2012

@author: jcazor
'''
import unittest, random, string
from komdb import api as dbapi
from komws import checkws, authws, procws
from komws import exceptions as wsex
from datetime import datetime

class dict2data(object):
    def __init__(self,dictionary):
        self.len = 0
        for k,v in list(dictionary.items()):
            setattr(self,k,v)
            self.len += 1
    
    def __len__(self):
        return self.len


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
        if self.smpl is not None:
            dbapi.delete_sample(self.smpl)
        if self.did is not None:
            dbapi.delete_datasource(self.did)
        if self.aid is not None:
            dbapi.delete_agent(self.aid)
        if self.uid is not None:
            dbapi.delete_user(self.uid)


    def test_wsUploadSample_checkws_OK(self):
        """
        Fill in data structure and call checking
        """
        aid = 0
        did = 0
        
        dictdata = {'username':self.username,'password':self.password,
                    'agentid':aid,'datasourceid':did,'date':self.date,
                    'filecontent':self.filecontent}
        
        data = dict2data(dictdata)
        self.assertTrue(checkws.wsupload_sample(data))

    def test_wsUploadSample_checkws_invalid_data(self):
        """
        Fill in data structure without one field and call checking
        """
        aid = 0
        did = 0
        
        dictdata = {'password':self.password,
                    'agentid':aid,'datasourceid':did,'date':self.date,
                    'filecontent':self.filecontent}
        
        data = dict2data(dictdata)
        self.assertRaises(wsex.InvalidData, checkws.wsupload_sample,data)
    
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
        
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.password, 'datasourceid':self.did,
                    'date':self.date, 'filecontent':self.filecontent}
        
        data = dict2data(dictdata)      
        self.assertTrue(authws.wsupload_sample(data))
        
    def test_wsUploadSample_authws_authentication_error(self):
        """
        In this case, we use a faked datasourceid
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.aid, 'datasourceid':0,
                    'date':self.date, 'filecontent':self.filecontent}
        
        data = dict2data(dictdata)      
        self.assertRaises(wsex.AuthenticationError, authws.wsupload_sample,data)
           
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
        
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.password, 'datasourceid':self.did,
                    'date':self.date, 'filecontent':self.filecontent}
        
        data = dict2data(dictdata)      
        self.assertTrue(procws.wsupload_sample(data))

    def test_wsUploadSample_procws_processing_error(self):
        """
        In this case, we use a nonexistent datasourceid        
        """
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.aid, 'datasourceid':0,
                    'date':self.date, 'filecontent':self.filecontent}
        
        data = dict2data(dictdata)      
        self.assertRaises(wsex.ProcessingError, procws.wsupload_sample,data)

    def test_wsdownload_config_checkws_OK(self):
        """
        Fill in data structure and call checking
        """
                
        dictdata = {'username':self.username,'password':self.password,
                    'agentid':self.agentname}
        
        data = dict2data(dictdata)
        self.assertTrue(checkws.wsdownload_config(data))

    def test_wsdownload_config_checkws_invalid_data(self):
        """
        Fill in data structure without one field and call checking
        """
         
        dictdata = {'password':self.password,
                    'agentid':self.agentname}
        
        data = dict2data(dictdata)
        self.assertRaises(wsex.InvalidData, checkws.wsdownload_config,data)

    def test_wsdownload_config_authws_OK(self):
        """
        Authentication implies data to exist on DB, so, 
        first: create user, agent and datasource
        second: fill in data structure 
        third: call authws for authentication
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.password}
        
        data = dict2data(dictdata)      
        self.assertTrue(authws.wsdownload_config(data))
        
    def test_wsdownload_config_authws_authentication_error(self):
        """
        In this case, we use a faked datasourceid
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.aid}
        
        data = dict2data(dictdata)      
        self.assertRaises(wsex.AuthenticationError, authws.wsdownload_config,data)
   
    def test_wsdownload_config_procws_OK(self):
        """
        Processing implies data to exist on DB, so, 
        first: create user, agent and datasource
        second: fill in data structure 
        third: call procws for authentication
        """
        self.uid = dbapi.create_user(self.username, self.password)
        self.aid = dbapi.create_agent(self.username, self.agentname, self.password)
        self.did = dbapi.create_datasource(self.aid, self.dsname)
        ds = dbapi.Datasource(self.did)
        ds_config = {'did':ds.did, 'sec':'*','min':'*','hour':'*','dom':'*','mon':'*','dow':'*','command':'*'}
        ds.setConfig(ds_config)
        
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':self.password}
        
        data = dict2data(dictdata) 
        configuration=[]
        configuration.append(ds_config)     
        self.assertEqual(procws.wsdownload_config(data),configuration)

    def test_wsdownload_config_procws_processing_error(self):
        """
        In this case, we use a nonexistent agentid        
        """
                
        dictdata = {'username':self.username, 'password':self.password,
                    'agentid':0}
        
        data = dict2data(dictdata)      
        self.assertRaises(wsex.ProcessingError, procws.wsupload_sample,data)
     
    
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(komwsFunctionalTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
