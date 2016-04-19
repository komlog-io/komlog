import unittest
import uuid
import random
from komlog.komfig import logging
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto

class GestaccountDatasourceApiTest(unittest.TestCase):
    ''' komlog.gestaccount.datasource.api tests '''

    def setUp(self):
        username='test_gestaccount.datasource.api_user'
        password='password'
        email='test_gestaccount.datasource.api_user@komlog.org'
        try:
            uid=userapi.get_uid(username=username)
        except Exception:
            user=userapi.create_user(username=username, password=password, email=email)
            uid=user['uid']
        finally:
            self.user=userapi.get_user_config(uid=uid)
        agentname='test_gestaccount.datasource.api_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        try:
            self.agent=agentapi.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        except Exception:
            agents=agentapi.get_agents_config(uid=self.user['uid'])
            for agent in agents:
                if agent['agentname']==agentname:
                    self.agent=agent

    def test_create_datasource_non_existent_user(self):
        ''' create_datasource should fail if user is not found in system '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        datasourcename='datasource_name'
        self.assertRaises(exceptions.UserNotFoundException, api.create_datasource,uid=uid, aid=aid, datasourcename=datasourcename ) 

    def test_create_datasource_non_existent_agent(self):
        ''' create_datasource should fail if agent is not found in system '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        datasourcename='test_create_datasource_non_existent_agent'
        self.assertRaises(exceptions.AgentNotFoundException, api.create_datasource,uid=uid, aid=aid, datasourcename=datasourcename ) 

    def test_create_datasource_success(self):
        ''' create_datasource should succeed if user and agent exist '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_create_datasource_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        self.assertIsInstance(datasource, dict)
        self.assertEqual(datasource['aid'],aid)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)

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
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_config_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        data=api.get_datasource_config(did=datasource['did'], pids_flag=True)
        self.assertIsInstance(data, dict)
        self.assertEqual(datasource['aid'],aid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertEqual(len(data),5)

    def test_get_datasources_config_non_existent_username(self):
        ''' get_datasource_config should fail if user is not in system '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.get_datasources_config,uid=uid)

    def test_get_datasources_config_success(self):
        ''' get_datasources_config should succeed if user exists '''
        username='test_get_datasources_config_success_user'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_get_datasources_config_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        self.agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        data=api.get_datasources_config(uid=user['uid'])
        self.assertEqual(data, [])

    def test_update_datasource_config_data_with_empty_datasourcename(self):
        ''' update_datasource_config should fail if data has empty ds_name'''
        did=uuid.uuid4()
        datasourcename=None
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, datasourcename=datasourcename)

    def test_update_datasource_config_data_with_invalid_datasourcename(self):
        ''' update_datasource_config should fail if data has invalid ds_name'''
        did=uuid.uuid4()
        datasourcename=2342321434
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, datasourcename=datasourcename)

    def test_update_datasource_config_non_existent_datasource(self):
        ''' update_datasource_config should fail if datasource is not in system '''
        did=uuid.uuid4()
        datasourcename='test_update_datasource_config_with_invalid_datasourcename'
        self.assertRaises(exceptions.DatasourceNotFoundException, api.update_datasource_config, did=did, datasourcename=datasourcename)

    def test_update_datasource_config_success(self):
        ''' update_datasource_config should succeed if datasource exists '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_update_datasource_config_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        datasourcename='test_update_datasource_config_success_after_update'
        self.assertTrue(api.update_datasource_config(did=datasource['did'], datasourcename=datasourcename))

    def test_get_datasource_data_success(self):
        ''' store_datasource_data should should store the content successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='store_datasource_data content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, date=date)
        self.assertIsNotNone(data)
        self.assertEqual(data['did'], did)
        self.assertEqual(data['date'], date)
        self.assertEqual(data['content'], content)

    def test_get_datasource_data_non_existent_datasource(self):
        ''' get_datasource_data should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.get_datasource_data, did=did, date=date)

    def test_get_datasource_data_non_existent_data_at_this_date(self):
        ''' get_datasource_data should fail if there is no data '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='store_datasource_data content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.get_datasource_data, did=did, date=date)

    def test_generate_datasource_map_non_existent_datasource(self):
        ''' generate_datasource_map should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.generate_datasource_map, did=did, date=date)

    def test_generate_datasource_map_non_existent_data_at_given_time(self):
        ''' generate_datasource_map should fail if did does not exist '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_generate_datasource_map_non_existent_data_at_given_time'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.generate_datasource_map, did=datasource['did'], date=date)

    def test_generate_datasource_map_success(self):
        ''' generate_datasource_data should generate and store the map successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='generate_datasource_map content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, date=date)
        self.assertIsNotNone(data)
        self.assertEqual(data['did'], did)
        self.assertEqual(data['date'], date)
        self.assertEqual(data['content'], content)
        self.assertTrue(api.generate_datasource_map(did=did, date=date))

