import unittest
import uuid
import json
from base64 import b64decode, b64encode
from komlog.komlibs.auth import operations
from komlog.komlibs.auth import passport
from komlog.komlibs.auth import errors as autherrors
from komlog.komlibs.gestaccount import errors as gesterrors
from komlog.komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlog.komlibs.interface.web.api import login as loginapi 
from komlog.komlibs.interface.web.api import user as userapi 
from komlog.komlibs.interface.web.api import agent as agentapi 
from komlog.komlibs.interface.web.api import datasource as datasourceapi 
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web import status, exceptions, errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komlibs.interface.imc.model import messages
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi


class InterfaceWebApiDatasourceTest(unittest.TestCase):
    ''' komlibs.interface.web.api.datasource tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.datasource_user'
        self.password = 'password'
        agentname='test_komlibs.interface.web.api.datasource_agent'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            response, cookie = loginapi.login_request(username=self.username, password=self.password)
            self.passport = passport.get_user_passport(cookie)
            response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
            aid = response.data['aid']
            cookie = {'user':self.username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
            self.agent_passport = passport.get_agent_passport(cookie)
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==self.passport.uid and msg.params['aid']==self.agent_passport.aid):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            datasourcename='datasource'
            response = datasourceapi.new_datasource_request(passport=self.agent_passport, datasourcename=datasourcename)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==self.agent_passport.uid and msg.params['aid']==self.agent_passport.aid and msg.params['did']==uuid.UUID(response.data['did'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if not msg:
                    break
                if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==self.agent_passport.uid:
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
                if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==self.agent_passport.uid: 
                    rescontrol.process_message_RESAUTH(message=msg)
                else:
                    msgapi.send_message(msg)
                    count+=1
                    if count>=100:
                        break
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        self.passport = passport.get_user_passport(cookie)
        response = agentapi.get_agents_config_request(passport=self.passport)
        self.agents = response.data

    def test_get_datasource_config_request_success(self):
        ''' get_datasource_config_request should succeed returning the datasource config '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        response = datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('datasourcename' in response.data)
        self.assertTrue('aid' in response.data)
        self.assertTrue('did' in response.data)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
        self.assertEqual(self.agents[0]['aid'], response.data['aid'])

    def test_get_datasource_config_request_failure_invalid_passport(self):
        ''' get_datasource_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        did=uuid.uuid4().hex
        for psp in passports:
            response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_config_request_failure_invalid_did(self):
        ''' get_datasource_config_request should fail if did is invalid '''
        dids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4()]
        psp = passport.Passport(uid=uuid.uuid4())
        for did in dids:
            response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_config_request_failure_non_existent_username(self):
        ''' get_datasource_config_request should fail if username does not exist '''
        psp = passport.Passport(uid=uuid.uuid4())
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSC_RE)

    def test_get_datasource_config_request_failure_non_existent_datasource(self):
        ''' get_datasource_config_request should fail if datasource does not exist '''
        psp = self.passport
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSC_RE)

    def test_get_datasource_config_request_failure_no_permission_over_this_datasource(self):
        ''' get_datasource_config_request should fail if user does not have permission over datasource '''
        new_username = 'test_get_datasource_config_request_failure_no_permission_over_datasource_user'
        password = 'password'
        new_email = new_username+'@komlog.org'
        response = userapi.new_user_request(username=new_username, password=password, email=new_email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response, cookie = loginapi.login_request(username=new_username, password = password)
        psp = passport.get_user_passport(cookie)
        did = self.agents[0]['dids'][0]
        response= datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSC_RE)

    def test_get_datasources_config_request_success(self):
        ''' get_datasources_config_request should succeed if username exists and return the datasources config '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie ={'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_agent_passport(cookie)
        datasourcename='test_get_datasource_config_request_success_datasource_ds'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==psp.uid and msg.params['aid']==psp.aid and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid:
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
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid: 
                rescontrol.process_message_RESAUTH(message=msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = datasourceapi.get_datasources_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response2.data)>=2) #the one created at setup too
        found=0
        for datasource in response2.data:
            if datasource['did']==response.data['did']:
                found+=1
        self.assertEqual(found,1)

    def test_get_datasources_config_request_failure_invalid_passport(self):
        ''' get_datasources_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=datasourceapi.get_datasources_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasources_config_request_failure_non_existent_username(self):
        ''' get_datasources_config_request should fail if username does not exist '''
        psp = passport.Passport(uid=uuid.uuid4())
        response=datasourceapi.get_datasources_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasources_config_request_success_no_datasources(self):
        ''' get_datasources_config_request should succeed but should return an empty array '''
        username = 'test_get_datasources_config_success_no_datasources'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response, cookie = loginapi.login_request(username=username, password=password)
        psp = passport.get_user_passport(cookie)
        response2=datasourceapi.get_datasources_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_upload_datasource_data_request_success(self):
        ''' upload_datasource_data should store content on a file and return a received status code '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie ={'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_agent_passport(cookie)
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)


    def test_upload_datasource_data_request_failure_invalid_passport(self):
        ''' upload_datasource_data should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        did=uuid.uuid4().hex
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        for psp in passports:
            response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_did(self):
        ''' upload_datasource_data should fail if did is invalid'''
        psp = passport.Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        dids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4()]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        for did in dids:
            response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_content(self):
        ''' upload_datasource_data should fail if content is invalid '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie ={'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_agent_passport(cookie)
        contents=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),uuid.uuid4()]
        did=self.agents[0]['dids'][0]
        destination='/tmp/'
        for content in contents:
            response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)


    def test_upload_datasource_data_request_failure_invalid_destination_no_string(self):
        ''' upload_datasource_data should fail if destination is invalid '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie ={'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_agent_passport(cookie)
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destinations=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),uuid.uuid4()]
        for destination in destinations:
            response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_upload_datasource_data_request_failure_invalid_destination_os_error(self):
        ''' upload_datasource_data should fail if destination is invalid '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie ={'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_agent_passport(cookie)
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destinations=['/root','/home/notfounddir']
        for destination in destinations:
            response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
            self.assertEqual(response.status, status.WEB_STATUS_INTERNAL_ERROR)

    def test_upload_datasource_data_request_failure_non_existent_user(self):
        ''' upload_datasource_data should fail if user does not exists '''
        psp = passport.Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp'
        response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ATDSD_RE)

    def test_upload_datasource_data_request_failure_non_existent_agent(self):
        ''' upload_datasource_data should fail if agent does not exists '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp'
        response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ATDSD_ANF)

    def test_upload_datasource_data_request_failure_non_existent_datasource(self):
        ''' upload_datasource_data should fail if datasource does not exists '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie ={'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_agent_passport(cookie)
        did=uuid.uuid4().hex
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp'
        response=datasourceapi.upload_datasource_data_request(passport=psp, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ATDSD_RE)

    def test_upload_datasource_data_request_failure_user_no_permission_over_datasource(self):
        ''' upload_datasource_data should store content on a file and return a received status code '''
        username='test_upload_datasource_data_request_failure_user_no_permission_over_datasource'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response, cookie = loginapi.login_request(username=username, password=password)
        psp = passport.get_user_passport(cookie)
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='v'
        response = agentapi.new_agent_request(passport=psp, agentname=username+'_agent', pubkey=pubkey, version=version)
        aid = response.data['aid']
        cookie = {'user':username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        agent_passport = passport.get_agent_passport(cookie)
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        response=datasourceapi.upload_datasource_data_request(passport=agent_passport, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ATDSD_RE)

    def test_upload_datasource_data_request_success_different_agent_but_from_the_same_user(self):
        ''' upload_datasource_data should store content if the agent uploading data belongs to the datasource user '''
        psp = self.passport
        agentname='test_upload_datasource_data_request_success_different_agent_but_from_the_same_user_agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        aid=response.data['aid']
        cookie = {'user':self.username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        agent_passport = passport.get_agent_passport(cookie)
        did=self.agents[0]['dids'][0]
        content='Datasource Content upload_datasource_data_request_success 0 1 2 3 4'
        destination='/tmp/'
        response=datasourceapi.upload_datasource_data_request(passport=agent_passport, did=did, content=content, destination=destination)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)

    def test_update_datasource_config_request_success(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_success'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(passport=psp, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(datasourceinfo.status, status.WEB_STATUS_OK)
        self.assertEqual(datasourceinfo.data['did'],did)
        self.assertEqual(datasourceinfo.data['datasourcename'],new_datasourcename)

    def test_update_datasource_config_request_failure_invalid_did(self):
        ''' update_datasource_config should fail if did is invalid '''
        psp = passport.Passport(uid=uuid.uuid4())
        dids=[None, 2342342, uuid.uuid4(), '2342342','234 234 223 ','stringwithñ',{'a','dict'},['a','list'],('a','tuple'),json.dumps('jsonstring')]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        for did in dids:
            response=datasourceapi.update_datasource_config_request(passport=psp,did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_passport(self):
        ''' update_datasource_config should fail if passport is invalid'''
        did=self.agents[0]['dids'][0]
        passports=[None, 2342342, uuid.uuid4(), '234 234 223 ','stringwithñ',{'a','dict'},['a','list'],('a','tuple'),json.dumps('jsonstring')]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        for psp in passports:
            response=datasourceapi.update_datasource_config_request(passport=psp,did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_data_type(self):
        ''' update_datasource_config should fail if data is invalid '''
        psp = passport.Passport(uid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        datas=[None, 2342342, uuid.uuid4(), '2342342','234 234 223 ','stringwithñ',['a','list'],('a','tuple'),json.dumps('jsonstring')]
        for data in datas:
            response=datasourceapi.update_datasource_config_request(passport=psp,did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_data_content(self):
        ''' update_datasource_config should fail if data is invalid '''
        psp = passport.Passport(uid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        datas=[{'a':'dict'},]
        for datasourcename in [None, 234234, 23423.234234, ['a','list'],{'a':'dict'},('a','tuple'),'Invalid\tdatasourcename','Invalid\n','ÑÑnovalid']:
            datas.append({'datasourcename':datasourcename})
        for data in datas:
            response=datasourceapi.update_datasource_config_request(passport=psp,did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_non_existent_user(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        psp =passport.Passport(uid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(passport=psp, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDSC_RE)

    def test_update_datasource_config_request_failure_non_existent_did(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        psp = passport.Passport(uid=uuid.uuid4())
        did=uuid.uuid4().hex
        new_datasourcename='test_update_datasource_config_failure_non_existent_did'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(passport=psp, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDSC_RE)

    def test_update_datasource_config_request_failure_no_permission_over_datasource(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        username='test_update_datasource_config_request_failure_no_permission_over_datasource'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response, cookie = loginapi.login_request(username=username, password=password)
        psp = passport.get_user_passport(cookie)
        did=self.agents[0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_failure_no_permission_over_ds'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(passport=psp, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_datasource_request_success(self):
        ''' new_datasource_request should succeed if parameters exists, and user has permission '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie = {'user':self.username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp= passport.get_agent_passport(cookie)
        datasourcename='test_new_datasource_request_success'
        response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==psp.uid and msg.params['aid']==psp.aid and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid:
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
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid: 
                rescontrol.process_message_RESAUTH(message=msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        datasourceinfo=datasourceapi.get_datasource_config_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourceinfo.status, status.WEB_STATUS_OK)
        self.assertEqual(datasourceinfo.data['did'],response.data['did'])
        self.assertEqual(datasourceinfo.data['datasourcename'],datasourcename)
        self.assertEqual(datasourceinfo.data['aid'],aid)

    def test_new_datasource_request_failure_invalid_username(self):
        ''' new_datasource_request should fail if username is invalid '''
        passports=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        datasourcename='test_new_datasource_request_failure'
        for psp in passports:
            response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_request_failure_invalid_aid(self):
        ''' new_datasource_request should fail if passport passed only contains the user '''
        psp=passport.Passport(uid=uuid.uuid4())
        datasourcename='test_new_datasource_request_failure'
        response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_AQA_ANDS_IA)

    def test_new_datasource_request_failure_invalid_datasourcename(self):
        ''' new_datasource_request should fail if datasourcename is invalid '''
        datasourcenames=[None, 234234, 23423.02342, 'Datasource Name ÑÑ', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        psp = passport.Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        for datasourcename in datasourcenames:
            response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_request_failure_no_permission_over_agent(self):
        ''' new_datasource_request should fail if user has no permission over this agent '''
        username='test_new_datasource_request_failure_no_permission_over_agent'
        password='temporal'
        email=username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response, cookie = loginapi.login_request(username=username, password=password)
        psp= passport.get_user_passport(cookie)
        psp.aid=uuid.UUID(self.agents[0]['aid'])
        datasourcename='test_new_datasource_request_failure_no_permission_over_agent'
        response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ANDS_RE)

    def test_get_datasource_data_request_failure_invalid_passport(self):
        ''' get_datasource_data_request should fail if username is invalid '''
        passports=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        did=uuid.uuid4().hex
        for psp in passports:
            response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_data_request_failure_invalid_did(self):
        ''' get_datasource_data_request should fail if did is invalid '''
        dids=[None, 234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername',uuid.uuid4()]
        psp = passport.Passport(uid=uuid.uuid4())
        for did in dids:
            response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_data_request_failure_invalid_tid(self):
        ''' get_datasource_data_request should fail if tid is invalid '''
        tids=[234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername',uuid.uuid4()]
        psp=passport.Passport(uid=uuid.uuid4())
        did=uuid.uuid4().hex
        for tid in tids:
            response=datasourceapi.get_datasource_data_request(passport=psp, did=did, tid=tid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWADS_GDSDR_IT)

    def test_get_datasource_data_request_failure_non_existent_datasource(self):
        ''' get_datasource_data_request should fail if datasource does not exist '''
        psp = self.passport
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_datasource_data_request_failure_non_existent_username(self):
        ''' get_datasource_data_request should fail if user does not exist '''
        psp = passport.Passport(uid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSD_RE)

    def test_get_datasource_data_request_data_not_found(self):
        ''' get_datasource_data should return a 404 error indicating no data was found '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasource_data_request_success(self):
        ''' get_datasource_data should return last mapped data '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['did'],did)
        self.assertEqual(response.data['ts'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response.data['variables'],[(28,1),(30,1),(32,1)])
        self.assertEqual(response.data['content'],content)
        self.assertEqual(response.data['datapoints'],[])

    def Notest_delete_datasource_request_failure_invalid_passport(self):
        ''' delete_datasource_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        did=uuid.uuid4().hex
        for psp in passports:
            response=datasourceapi.delete_datasource_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def Notest_delete_datasource_request_failure_invalid_did(self):
        ''' delete_datasource_request should fail if did is invalid '''
        dids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = passport.Passport(uid=uuid.uuid4())
        for did in dids:
            response=datasourceapi.delete_datasource_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

