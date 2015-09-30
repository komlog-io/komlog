import unittest
import uuid
import json
from komlibs.auth import operations
from komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.api import agent as agentapi 
from komlibs.interface.web.api import datasource as datasourceapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions, errors
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.interface.imc.api import rescontrol
from komlibs.interface.imc.model import messages
from komimc import bus, routing
from komimc import api as msgapi


class InterfaceWebApiDatasourceTest(unittest.TestCase):
    ''' komlibs.interface.web.api.datasource tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        username = 'test_komlibs.interface.web.api.datasource_user'
        userresponse=userapi.get_user_config_request(username=username)
        if userresponse.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username+'@komlog.org'
            response = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            userresponse = userapi.get_user_config_request(username=username)
            self.assertEqual(userresponse.status, status.WEB_STATUS_OK)
            self.userinfo=userresponse.data
            agentname='test_komlibs.interface.web.api.datasource_agent'
            pubkey='TESTKOMLIBSINTERFACEWEBAPIDATASOURCEAGENT'
            version='test library vX.XX'
            response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
            aid=response.data['aid']
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response.data['aid'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response.data['aid'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_RESAUTH(msg)
            datasourcename='test_get_datasource_config_request_success_datasource'
            response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_RESAUTH(msg)
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if not msg:
                    break
                if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                    rescontrol.process_message_UPDQUO(msg)
                else:
                    msgapi.send_message(msg)
                    count+=1
                    if count>=100:
                        break
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if not msg:
                    break
                if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                    rescontrol.process_message_RESAUTH(msg)
                else:
                    msgapi.send_message(msg)
                    count+=1
                    if count>=100:
                        break
            userresponse=userapi.get_user_config_request(username=username)
        self.userinfo=userresponse.data

    def test_get_datasource_config_request_success(self):
        ''' get_datasource_config_request should succeed returning the datasource config '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        response = datasourceapi.get_datasource_config_request(username=username, did=did)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('datasourcename' in response.data)
        self.assertTrue('aid' in response.data)
        self.assertTrue('did' in response.data)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
        self.assertEqual(self.userinfo['agents'][0]['aid'], response.data['aid'])

    def test_get_datasource_config_request_failure_invalid_username(self):
        ''' get_datasource_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        did=uuid.uuid4().hex
        for username in usernames:
            response=datasourceapi.get_datasource_config_request(username=username, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_config_request_failure_invalid_did(self):
        ''' get_datasource_config_request should fail if did is invalid '''
        dids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4()]
        username='test_get_datasource_config_request_failure_invalid_did'
        for did in dids:
            response=datasourceapi.get_datasource_config_request(username=username, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_config_request_failure_non_existent_username(self):
        ''' get_datasource_config_request should fail if username does not exist '''
        username='test_get_datasource_config_request_failure_non_existent_username'
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_config_request(username=username, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasource_config_request_failure_non_existent_datasource(self):
        ''' get_datasource_config_request should fail if datasource does not exist '''
        username=self.userinfo['username']
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_config_request(username=username, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_datasource_config_request_failure_no_permission_over_this_datasource(self):
        ''' get_datasource_config_request should fail if user does not have permission over datasource '''
        new_username = 'test_get_datasource_config_request_failure_no_permission_over_datasource_user'
        password = 'password'
        new_email = new_username+'@komlog.org'
        response = userapi.new_user_request(username=new_username, password=password, email=new_email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        did=self.userinfo['agents'][0]['dids'][0]
        datasourceinfo = datasourceapi.get_datasource_config_request(username=new_username, did=did)
        self.assertEqual(datasourceinfo.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(datasourceinfo.data, None)

    def test_get_datasources_config_request_success(self):
        ''' get_datasources_config_request should succeed if username exists and return the datasources config '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_datasource_config_request_success_datasource_ds'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_RESAUTH(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                rescontrol.process_message_UPDQUO(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                rescontrol.process_message_RESAUTH(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = datasourceapi.get_datasources_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response2.data)>=2) #the one created at setup too
        found=0
        for datasource in response2.data:
            if datasource['did']==response.data['did']:
                found+=1
        self.assertEqual(found,1)

    def test_get_datasources_config_request_failure_invalid_username(self):
        ''' get_datasources_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for username in usernames:
            response=datasourceapi.get_datasources_config_request(username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasources_config_request_failure_non_existent_username(self):
        ''' get_datasources_config_request should fail if username does not exist '''
        username='test_get_datasources_config_request_failure_non_existent_username'
        response=datasourceapi.get_datasources_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasources_config_request_success_no_datasources(self):
        ''' get_datasources_config_request should succeed but should return an empty array '''
        username = 'test_get_datasources_config_success_no_datasources'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response2=datasourceapi.get_datasources_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_upload_datasource_data_request_success(self):
        ''' upload_datasource_data should store content on a file and return a received status code '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)


    def test_upload_datasource_data_request_failure_invalid_username(self):
        ''' upload_datasource_data should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        for username in usernames:
            response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_aid(self):
        ''' upload_datasource_data should fail if aid is invalid'''
        username=self.userinfo['username']
        aids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4()]
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        for aid in aids:
            response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_did(self):
        ''' upload_datasource_data should fail if did is invalid'''
        username=self.userinfo['username']
        dids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4()]
        aid=self.userinfo['agents'][0]['aid']
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        for did in dids:
            response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_content(self):
        ''' upload_datasource_data should fail if content is invalid '''
        username=self.userinfo['username']
        contents=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),uuid.uuid4()]
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        destination='/tmp/'
        for content in contents:
            response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_destination_no_string(self):
        ''' upload_datasource_data should fail if destination is invalid '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destinations=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),uuid.uuid4()]
        for destination in destinations:
            response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_upload_datasource_data_request_failure_invalid_destination_os_error(self):
        ''' upload_datasource_data should fail if destination is invalid '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destinations=['/root','/home/notfounddir']
        for destination in destinations:
            response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_INTERNAL_ERROR)

    def test_upload_datasource_data_request_failure_non_existent_user(self):
        ''' upload_datasource_data should fail if user does not exists '''
        username='test_upload_datasource_data_request_failure_non_existent_user'
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp'
        response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_upload_datasource_data_request_failure_non_existent_agent(self):
        ''' upload_datasource_data should fail if agent does not exists '''
        username=self.userinfo['username']
        aid=uuid.uuid4().hex
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp'
        response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_upload_datasource_data_request_failure_non_existent_datasource(self):
        ''' upload_datasource_data should fail if datasource does not exists '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        did=uuid.uuid4().hex
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp'
        response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_upload_datasource_data_request_failure_user_no_permission_over_datasource(self):
        ''' upload_datasource_data should store content on a file and return a received status code '''
        username='test_upload_datasource_data_request_failure_user_no_permission_over_datasource'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        aid=self.userinfo['agents'][0]['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_upload_datasource_data_request_failure_agent_no_permission_over_datasource(self):
        ''' upload_datasource_data should store content on a file and return a received status code '''
        username='test_upload_datasource_data_request_failure_agent_no_permission_over_datasource'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        agentname='test_upload_datasource_data_request_failure_agent_no_permission_over_datasource_agent'
        pubkey='TESTUPLOADDATASOURCEDATAREQUESTFAILURENOPERMISSIONAGENT'
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        username=self.userinfo['username']
        aid=response.data['aid']
        did=self.userinfo['agents'][0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        response=datasourceapi.upload_datasource_data_request(username=username, aid=aid, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_datasource_config_request_success(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_success'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_config_request(username=username, did=did)
        self.assertEqual(datasourceinfo.status, status.WEB_STATUS_OK)
        self.assertEqual(datasourceinfo.data['did'],did)
        self.assertEqual(datasourceinfo.data['datasourcename'],new_datasourcename)

    def test_update_datasource_config_request_failure_invalid_did(self):
        ''' update_datasource_config should fail if did is invalid '''
        username=self.userinfo['username']
        dids=[None, 2342342, uuid.uuid4(), '2342342','234 234 223 ','stringwithñ',{'a','dict'},['a','list'],('a','tuple'),json.dumps('jsonstring')]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        for did in dids:
            response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_username(self):
        ''' update_datasource_config should fail if username is invalid'''
        did=self.userinfo['agents'][0]['dids'][0]
        usernames=[None, 2342342, uuid.uuid4(), '234 234 223 ','stringwithñ',{'a','dict'},['a','list'],('a','tuple'),json.dumps('jsonstring')]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        for username in usernames:
            response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_data_type(self):
        ''' update_datasource_config should fail if data is invalid '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datas=[None, 2342342, uuid.uuid4(), '2342342','234 234 223 ','stringwithñ',['a','list'],('a','tuple'),json.dumps('jsonstring')]
        for data in datas:
            response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_data_content(self):
        ''' update_datasource_config should fail if data is invalid '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datas=[{'a':'dict'},]
        for datasourcename in [None, 234234, 23423.234234, ['a','list'],{'a':'dict'},('a','tuple'),'Invalid\tdatasourcename','Invalid\n','ÑÑnovalid']:
            datas.append({'datasourcename':datasourcename})
        for data in datas:
            response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_non_existent_user(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        username='test_update_datasource_config_request_failure_non_existent_user'
        did=self.userinfo['agents'][0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_update_datasource_config_request_failure_non_existent_did(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        username=self.userinfo['username']
        did=uuid.uuid4().hex
        new_datasourcename='test_update_datasource_config_failure_non_existent_did'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_datasource_config_request_failure_no_permission_over_datasource(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        username='test_update_datasource_config_request_failure_no_permission_over_datasource'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        did=self.userinfo['agents'][0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_failure_no_permission_over_ds'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(username=username, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_datasource_request_success(self):
        ''' new_datasource_request should succeed if parameters exists, and user has permission '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_new_datasource_request_success'
        response=datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_RESAUTH(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                rescontrol.process_message_UPDQUO(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                rescontrol.process_message_RESAUTH(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        datasourceinfo=datasourceapi.get_datasource_config_request(username=username, did=response.data['did'])
        self.assertEqual(datasourceinfo.status, status.WEB_STATUS_OK)
        self.assertEqual(datasourceinfo.data['did'],response.data['did'])
        self.assertEqual(datasourceinfo.data['datasourcename'],datasourcename)
        self.assertEqual(datasourceinfo.data['aid'],aid)

    def test_new_datasource_request_failure_invalid_username(self):
        ''' new_datasource_request should fail if username is invalid '''
        usernames=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_new_datasource_request_failure'
        for username in usernames:
            response=datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_request_failure_invalid_aid(self):
        ''' new_datasource_request should fail if aid is invalid '''
        username=self.userinfo['username']
        aids=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        datasourcename='test_new_datasource_request_failure'
        for aid in aids:
            response=datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_request_failure_invalid_datasourcename(self):
        ''' new_datasource_request should fail if datasourcename is invalid '''
        datasourcenames=[None, 234234, 23423.02342, 'Datasource Name ÑÑ', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        for datasourcename in datasourcenames:
            response=datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_request_failure_no_permission_over_agent(self):
        ''' new_datasource_request should fail if user has no permission over this agent '''
        username=self.userinfo['username']
        aid=uuid.uuid4().hex
        datasourcename='test_new_datasource_request_failure_no_permission_over_agent'
        response=datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_datasource_data_request_failure_invalid_username(self):
        ''' get_datasource_data_request should fail if username is invalid '''
        usernames=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        did=self.userinfo['agents'][0]['dids'][0]
        for username in usernames:
            response=datasourceapi.get_datasource_data_request(username=username, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_data_request_failure_invalid_did(self):
        ''' get_datasource_data_request should fail if did is invalid '''
        dids=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername',uuid.uuid4()]
        username=self.userinfo['username']
        for did in dids:
            response=datasourceapi.get_datasource_data_request(username=username, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_data_request_failure_invalid_tid(self):
        ''' get_datasource_data_request should fail if tid is invalid '''
        tids=[234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername',uuid.uuid4()]
        username=self.userinfo['username']
        did=uuid.uuid4().hex
        for tid in tids:
            response=datasourceapi.get_datasource_data_request(username=username, did=did, tid=tid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWADS_GDSDR_IT)

    def test_get_datasource_data_request_failure_non_existent_datasource(self):
        ''' get_datasource_data_request should fail if datasource does not exist '''
        username=self.userinfo['username']
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_datasource_data_request_failure_non_existent_username(self):
        ''' get_datasource_data_request should fail if user does not exist '''
        username='test_get_datasource_data_request_failure_non_existent_username'
        did=self.userinfo['agents'][0]['dids'][0]
        response=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasource_data_request_data_not_found(self):
        ''' get_datasource_data should return a 404 error indicating no data was found '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        response=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasource_data_request_success(self):
        ''' get_datasource_data should return last mapped data '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        content='get_datasource_data content 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        response=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['did'],did)
        self.assertEqual(response.data['ts'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response.data['variables'],[(28,1),(30,1),(32,1)])
        self.assertEqual(response.data['content'],content)
        self.assertEqual(response.data['datapoints'],[])

    def test_delete_datasource_request_failure_invalid_username(self):
        ''' delete_datasource_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        did=uuid.uuid4().hex
        for username in usernames:
            response=datasourceapi.delete_datasource_request(username=username, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datasource_request_failure_invalid_did(self):
        ''' delete_datasource_request should fail if did is invalid '''
        dids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_datasource_request_failure_invalid_did'
        for did in dids:
            response=datasourceapi.delete_datasource_request(username=username, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

