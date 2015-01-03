import unittest
import uuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api
from komlibs.gestaccount import exceptions
from komcass.model.orm import datasource as ormdatasource

class GestaccountDatasourceApiTest(unittest.TestCase):
    ''' komlog.gestaccount.datasource.api tests '''

    def setUp(self):
        username='test_gestaccount.datasource.api_user'
        password='password'
        email='test_gestaccount.datasource.api_user@komlog.org'
        self.user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_gestaccount.datasource.api_agent'
        pubkey='pubkey'
        version='Test Version'
        self.agent=agentapi.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)

    def test_create_datasource_non_existent_user(self):
        ''' create_datasource should fail if user is not found in system '''
        username='test_user_non_existent_datasource_creation'
        aid=uuid.uuid4()
        datasourcename='Datasource Name'
        self.assertRaises(exceptions.UserNotFoundException, api.create_datasource,username=username, aid=aid, datasourcename=datasourcename ) 

    def test_create_datasource_non_existent_agent(self):
        ''' create_datasource should fail if agent is not found in system '''
        username=self.user.username
        aid=uuid.uuid4()
        datasourcename='test_create_datasource_non_existent_agent'
        self.assertRaises(exceptions.AgentNotFoundException, api.create_datasource,username=username, aid=aid, datasourcename=datasourcename ) 

    def test_create_datasource_success(self):
        ''' create_datasource should succeed if user and agent exist '''
        username=self.user.username
        aid=self.agent.aid
        datasourcename='test_create_datasource_success'
        datasource=api.create_datasource(username=username, aid=aid, datasourcename=datasourcename) 
        self.assertIsInstance(datasource, ormdatasource.Datasource)

    def test_get_last_processed_datasource_data_non_existent_datasource(self):
        ''' get_last_processed_datasource_data should fail if did is not in system '''
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.get_last_processed_datasource_data, did=did)
    
    def test_upload_datasource_data_non_existent_datasource(self):
        ''' upload_datasource_data should fail if did is not in system '''
        did=uuid.uuid4()
        content='sadfa'
        dest_dir=''
        self.assertRaises(exceptions.DatasourceNotFoundException, api.upload_datasource_data, did=did, content=content, dest_dir=dest_dir)

    def test_get_datasource_config_non_existent_datasource(self):
        ''' get_datasource_config should fail if did is not in system '''
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.get_datasource_config, did=did)

    def test_get_datasource_config_success(self):
        ''' get_datasource_config should succeed if datasource exists '''
        username=self.user.username
        aid=self.agent.aid
        datasourcename='test_get_datasource_config_success'
        datasource=api.create_datasource(username=username, aid=aid, datasourcename=datasourcename) 
        data=api.get_datasource_config(did=datasource.did)
        self.assertIsInstance(data, dict)

    def test_get_datasources_config_non_existent_username(self):
        ''' get_datasource_config should fail if user is not in system '''
        username='test_get_datasources_config_non_existent_username'
        self.assertRaises(exceptions.UserNotFoundException, api.get_datasources_config, username=username)

    def test_get_datasources_config_success(self):
        ''' get_datasources_config should succeed if user exists '''
        username=self.user.username
        data=api.get_datasources_config(username=username)
        self.assertIsInstance(data, list)

    def test_update_datasource_config_data_with_no_datasourcename(self):
        ''' update_datasource_config should fail if data has no ds_name key'''
        did=uuid.uuid4()
        data={'key':'value'}
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, data=data)

    def test_update_datasource_config_data_with_empty_datasourcename(self):
        ''' update_datasource_config should fail if data has empty ds_name'''
        did=uuid.uuid4()
        data={'ds_name':None}
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, data=data)

    def test_update_datasource_config_data_with_invalid_datasourcename(self):
        ''' update_datasource_config should fail if data has invalid ds_name'''
        did=uuid.uuid4()
        data={'ds_name':2342321434}
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, data=data)

    def test_update_datasource_config_non_existent_datasource(self):
        ''' update_datasource_config should fail if datasource is not in system '''
        did=uuid.uuid4()
        data={'ds_name':'test_update_datasource_config_with_invalid_datasourcename'}
        self.assertRaises(exceptions.DatasourceNotFoundException, api.update_datasource_config, did=did, data=data)

    def test_update_datasource_config_success(self):
        ''' update_datasource_config should succeed if datasource exists '''
        username=self.user.username
        aid=self.agent.aid
        datasourcename='test_update_datasource_config_success'
        datasource=api.create_datasource(username=username, aid=aid, datasourcename=datasourcename) 
        data={'ds_name':'test_update_datasource_config_success_after_update'}
        self.assertTrue(api.update_datasource_config(did=datasource.did, data=data))

