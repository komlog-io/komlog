import unittest
import uuid
import json
from base64 import b64encode, b64decode
from komlibs.auth import operations
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.api import agent as agentapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.web import status, exceptions
from komlibs.interface.imc.api import rescontrol
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.crypto import crypto
from komlibs.gestaccount.agent import states
from komimc import bus, routing
from komimc import api as msgapi


class InterfaceWebApiAgentTest(unittest.TestCase):
    ''' komlibs.interface.web.api.agent tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        username = 'test_komlibs.interface.web.api.agent_user'
        response=userapi.get_user_config_request(username=username)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username+'@komlog.org'
            response = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            response2 = userapi.get_user_config_request(username=username)
            self.assertEqual(response2.status, status.WEB_STATUS_OK)
            response=userapi.get_user_config_request(username=username)
        self.userinfo=response.data

    def test_new_agent_request_success(self):
        ''' new_agent_request should succeed if arguments are valid and return the agent id '''
        username=self.userinfo['username']
        agentname='test_new_agent_request_success'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
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
        #msg UPDQUO received OK

    def test_new_agent_request_failure_invalid_username(self):
        ''' new_agent_request should fail if username is invalid '''
        usernames=[None, 23423422, 23423.2342, {'a':'dict'},['a','list'],json.dumps('username'),'Username','userñame','user name','\tusername']
        agentname='test_new_agent_request_failure_invalid_username'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        for username in usernames:
            response=agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_invalid_agentname(self):
        ''' new_agent_request should fail if agentname is invalid '''
        agentnames=[None, 23423422, 23423.2342, {'a':'dict'},['a','list'],json.dumps('username'),'userñame','user\nname','\tusername']
        username='test_new_agent_request_failure_invalid_agentname'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        for agentname in agentnames:
            response=agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_invalid_pubkey(self):
        ''' new_agent_request should fail if pubkey is invalid '''
        pubkeys=[None, 23423422, 23423.2342, {'a':'dict'},['a','list']]
        agentname='test_new_agent_request_failure_invalid_pubkey'
        username='test_new_agent_request_failure_invalid_pubkey'
        version='test library vX.XX'
        for pubkey in pubkeys:
            response=agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_invalid_version(self):
        ''' new_agent_request should fail if version is invalid '''
        versions=[None, 23423422, 23423.2342, {'a':'dict'},['a','list'],json.dumps('username'),'userñame','user\nname','\tusername']
        agentname='test_new_agent_request_failure_invalid_version'
        username='test_new_agent_request_failure_invalid_version'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        for version in versions:
            response=agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_non_existent_user(self):
        ''' new_agent_request should fail if user does not exists '''
        username='test_new_agent_request_failure_non_existent_user'
        agentname='test_new_agent_request_failure_non_existent_user'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response=agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_new_agent_request_failure_agent_already_exists(self):
        ''' new_agent_request should succeed if arguments are valid and return the agent id '''
        username=self.userinfo['username']
        agentname='test_new_agent_request_failure_agent_already_exists'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
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
        #msg UPDQUO received OK
        response2 = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response2.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_agent_config_request_success(self):
        ''' get_agent_config_request should succeed if agent exists and return the agent config '''
        username=self.userinfo['username']
        agentname='test_get_agent_config_request_success'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
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
        response2 = agentapi.get_agent_config_request(username=username, aid=response.data['aid'])
        self.assertTrue(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data['aid'],response.data['aid'])
        self.assertEqual(response2.data['agentname'],agentname)
        self.assertEqual(response2.data['state'], states.ACTIVE)
        self.assertEqual(response2.data['version'], version)

    def test_get_agent_config_request_failure_invalid_username(self):
        ''' get_agent_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        aid=uuid.uuid4().hex
        for username in usernames:
            response=agentapi.get_agent_config_request(username=username, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_agent_config_request_failure_invalid_aid(self):
        ''' get_agent_config_request should fail if aid is invalid '''
        aids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_get_agent_config_request_failure_invalid_aid'
        for aid in aids:
            response=agentapi.get_agent_config_request(username=username, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_agent_config_request_failure_non_existent_username(self):
        ''' get_agent_config_request should fail if username does not exist '''
        username='test_get_agent_config_request_failure_non_existent_username'
        aid=uuid.uuid4().hex
        response=agentapi.get_agent_config_request(username=username, aid=aid)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_agent_config_request_failure_non_existent_agent(self):
        ''' get_agent_config_request should fail if agent does not exist '''
        username=self.userinfo['username']
        aid=uuid.uuid4().hex
        response=agentapi.get_agent_config_request(username=username, aid=aid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_agent_config_request_failure_no_permission_over_this_agent(self):
        ''' get_agent_config_request should fail if user does not have permission over the agent '''
        username=self.userinfo['username']
        agentname='test_get_agent_config_request_failure_no_permission_over_this_agent'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
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
        #msg UPDQUO received OK
        username2 = 'test_get_agent_config_failure_no_permission_over_this_agent_user'
        password = 'password'
        email2 = username2+'@komlog.org'
        response2 = userapi.new_user_request(username=username2, password=password, email=email2)
        self.assertTrue(isinstance(response2, webmodel.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        response3 = agentapi.get_agent_config_request(username=username2, aid=response.data['aid'])
        self.assertTrue(response3.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_agents_config_request_success(self):
        ''' get_agents_config_request should succeed if username exists and return the agents config '''
        username=self.userinfo['username']
        agentname1='test_get_agents_config_request_success_1'
        pubkey1 = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response1 = agentapi.new_agent_request(username=username, agentname=agentname1, pubkey=pubkey1, version=version)
        self.assertTrue(isinstance(response1, webmodel.WebInterfaceResponse))
        self.assertEqual(response1.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response1.data['aid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response1.data['aid'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        agentname2='test_get_agents_config_request_success_2'
        pubkey2 = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response2 = agentapi.new_agent_request(username=username, agentname=agentname2, pubkey=pubkey2, version=version)
        self.assertTrue(isinstance(response2, webmodel.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response2.data['aid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response2.data['aid'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        response3 = agentapi.get_agents_config_request(username=username)
        self.assertTrue(response3.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response3.data)>=2)
        agent_seen=0
        for reg in response3.data:
            if reg['aid']==response1.data['aid']:
                agent_seen+=1
                self.assertEqual(reg['agentname'],agentname1)
                self.assertEqual(reg['state'], states.ACTIVE)
                self.assertEqual(reg['version'], version)
            elif reg['aid']==response2.data['aid']:
                agent_seen+=1
                self.assertEqual(reg['agentname'],agentname2)
                self.assertEqual(reg['state'], states.ACTIVE)
                self.assertEqual(reg['version'], version)
        self.assertEqual(agent_seen,2)

    def test_get_agents_config_request_failure_invalid_username(self):
        ''' get_agents_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for username in usernames:
            response=agentapi.get_agents_config_request( username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_agents_config_request_failure_non_existent_username(self):
        ''' get_agents_config_request should fail if username does not exist '''
        username='test_get_agents_config_request_failure_non_existent_username'
        response=agentapi.get_agents_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_agents_config_request_success_no_agents(self):
        ''' get_agents_config_request should succeed but should return an empty array '''
        username = 'test_get_agents_config_success_no_agents'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response2=agentapi.get_agents_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_update_agent_config_request_success(self):
        ''' update_agent_config_request should succeed if agent exists and the new conf is set '''
        username=self.userinfo['username']
        agentname='test_update_agent_config_request_success'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
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
        new_agentname=agentname+'_new'
        data={'agentname':new_agentname}
        response2 = agentapi.update_agent_config_request(username=username, aid=response.data['aid'], data=data)
        self.assertTrue(response2.status, status.WEB_STATUS_OK)
        response3 = agentapi.get_agent_config_request(username=username, aid=response.data['aid'])
        self.assertTrue(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['aid'],response.data['aid'])
        self.assertEqual(response3.data['agentname'],new_agentname)
        self.assertEqual(response3.data['state'], states.ACTIVE)
        self.assertEqual(response3.data['version'], version)

    def test_update_agent_config_request_failure_invalid_username(self):
        ''' update_agent_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        aid=uuid.uuid4().hex
        data={'agentname':'test_update_agent_config_request_failure'}
        for username in usernames:
            response=agentapi.update_agent_config_request(username=username, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_aid(self):
        ''' update_agent_config_request should fail if aid is invalid '''
        aids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(),'23234234hasdfasdfASDFASDF']
        username=self.userinfo['username']
        data={'agentname':'test_update_agent_config_request_failure'}
        for aid in aids:
            response=agentapi.update_agent_config_request(username=username, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_data(self):
        ''' update_agent_config_request should fail if data is invalid '''
        datas=[None, 32423, 023423.23423,['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(),'23234234hasdfasdfASDFASDF']
        aid=uuid.uuid4().hex
        username=self.userinfo['username']
        for data in datas:
            response=agentapi.update_agent_config_request(username=username, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_data_keys(self):
        ''' update_agent_config_request should fail if data is invalid '''
        aid=uuid.uuid4().hex
        username=self.userinfo['username']
        keys=[234234, 0234234234.023423234,('a','tuple'),'string',None]
        new_agentname='test_update_agent_config_request_failure'
        for key in keys:
            data={key:new_agentname}
            response=agentapi.update_agent_config_request(username=username, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_data_new_agentname(self):
        ''' update_agent_config_request should fail if data is invalid '''
        agentnames=[None, 32423, 023423.23423,['a','list'],('a','tuple'),'user\nname','userñame', uuid.uuid4(),'23234234\thasdfasdfASDFASDF']
        aid=uuid.uuid4().hex
        username=self.userinfo['username']
        for name in agentnames:
            data={'agentname':name}
            response=agentapi.update_agent_config_request(username=username, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_non_existent_agent(self):
        ''' update_agent_config_request should fail if agent does not exists '''
        username=self.userinfo['username']
        aid=uuid.uuid4().hex
        data={'agentname':'new_agentname'}
        response=agentapi.update_agent_config_request(username=username, aid=aid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_agent_request_failure_invalid_username(self):
        ''' delete_agent_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        aid=uuid.uuid4().hex
        for username in usernames:
            response=agentapi.delete_agent_request(username=username, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_agent_request_failure_invalid_aid(self):
        ''' delete_agent_request should fail if aid is invalid '''
        aids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_agent_request_failure_invalid_aid'
        for aid in aids:
            response=agentapi.delete_agent_request(username=username, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

