import unittest
import uuid
import json
from base64 import b64encode, b64decode
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.interface.web.api import login as loginapi 
from komlog.komlibs.interface.web.api import user as userapi 
from komlog.komlibs.interface.web.api import agent as agentapi 
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.agent.states import *
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komfig import logging


class InterfaceWebApiAgentTest(unittest.TestCase):
    ''' komlibs.interface.web.api.agent tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        username = 'test_komlibs.interface.web.api.agent_user'
        password = 'password'
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response,'cookie',None)
        if response.status == status.WEB_STATUS_NOT_FOUND:
            email = username+'@komlog.org'
            creation = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(creation , webresp.WebInterfaceResponse))
            self.assertEqual(creation .status, status.WEB_STATUS_OK)
            for msg in creation.unrouted_messages:
                msgresponse=msgapi.process_message(msg)
            response = loginapi.login_request(username=username, password=password)
            cookie=getattr(response,'cookie',None)
        self.passport=passport.get_user_passport(cookie)

    def test_new_agent_request_success(self):
        ''' new_agent_request should succeed if arguments are valid and return the agent id '''
        agentname='test_new_agent_request_success'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
        self.assertEqual(len(response.unrouted_messages),2)
        for msg in response.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)

    def test_new_agent_request_failure_invalid_passport(self):
        ''' new_agent_request should fail if username is invalid '''
        passports=[None, 23423422, 23423.2342, {'a':'dict'},['a','list'],json.dumps('username'),'Username','userñame','user name','\tusername']
        agentname='test_new_agent_request_failure_invalid_username'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        for psp in passports:
            response=agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_invalid_agentname(self):
        ''' new_agent_request should fail if agentname is invalid '''
        agentnames=[None, 23423422, 23423.2342, {'a':'dict'},['a','list'],json.dumps('username'),'userñame','user\nname','\tusername']
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4(), aid=None)
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        for agentname in agentnames:
            response=agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_invalid_pubkey(self):
        ''' new_agent_request should fail if pubkey is invalid '''
        pubkeys=[None, 23423422, 23423.2342, {'a':'dict'},['a','list']]
        agentname='test_new_agent_request_failure_invalid_pubkey'
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4(), aid=None)
        version='test library vX.XX'
        for pubkey in pubkeys:
            response=agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_invalid_version(self):
        ''' new_agent_request should fail if version is invalid '''
        versions=[None, 23423422, 23423.2342, {'a':'dict'},['a','list'],json.dumps('username'),'userñame','user\nname','\tusername']
        agentname='test_new_agent_request_failure_invalid_version'
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4(), aid=None)
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        for version in versions:
            response=agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_agent_request_failure_non_existent_user(self):
        ''' new_agent_request should fail if user does not exists '''
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4(), aid=None)
        agentname='test_new_agent_request_failure_non_existent_user'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response=agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GAA_CRA_UNF.value)

    def test_new_agent_request_failure_agent_already_exists(self):
        ''' new_agent_request should succeed if arguments are valid and return the agent id '''
        psp = self.passport
        agentname='test_new_agent_request_failure_agent_already_exists'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response2.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_agent_config_request_success(self):
        ''' get_agent_config_request should succeed if agent exists and return the agent config '''
        psp=self.passport
        agentname='test_get_agent_config_request_success'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
        for msg in response.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = agentapi.get_agent_config_request(passport=psp, aid=response.data['aid'])
        self.assertTrue(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data['aid'],response.data['aid'])
        self.assertEqual(response2.data['agentname'],agentname)
        self.assertEqual(response2.data['state'], AgentStates.ACTIVE)
        self.assertEqual(response2.data['version'], version)

    def test_get_agent_config_request_failure_invalid_passport(self):
        ''' get_agent_config_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        aid=uuid.uuid4().hex
        for psp in passports:
            response=agentapi.get_agent_config_request(passport=psp, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_agent_config_request_failure_invalid_aid(self):
        ''' get_agent_config_request should fail if aid is invalid '''
        aids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp=passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        for aid in aids:
            response=agentapi.get_agent_config_request(passport=psp, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_agent_config_request_failure_non_existent_username(self):
        ''' get_agent_config_request should fail if username does not exist '''
        psp=passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        aid=uuid.uuid4().hex
        response=agentapi.get_agent_config_request(passport=psp, aid=aid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGAC_RE.value)

    def test_get_agent_config_request_failure_non_existent_agent(self):
        ''' get_agent_config_request should fail if agent does not exist '''
        psp=self.passport
        aid=uuid.uuid4().hex
        response=agentapi.get_agent_config_request(passport=psp, aid=aid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGAC_RE.value)

    def test_get_agent_config_request_failure_no_permission_over_this_agent(self):
        ''' get_agent_config_request should fail if user does not have permission over the agent '''
        psp=self.passport
        agentname='test_get_agent_config_request_failure_no_permission_over_this_agent'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        username2 = 'test_get_agent_config_failure_no_permission_over_this_agent_user'
        password = 'password'
        email2 = username2+'@komlog.org'
        response2 = userapi.new_user_request(username=username2, password=password, email=email2)
        self.assertTrue(isinstance(response2, webresp.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        for msg in response2.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
        response3 = loginapi.login_request(username=username2, password=password)
        cookie=getattr(response3,'cookie',None)
        psp2 = passport.get_user_passport(cookie)
        response3 = agentapi.get_agent_config_request(passport=psp2, aid=response.data['aid'])
        self.assertTrue(response3.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response3.error, autherrors.E_ARA_AGAC_RE.value)

    def test_get_agents_config_request_success(self):
        ''' get_agents_config_request should succeed if username exists and return the agents config '''
        psp = self.passport
        agentname1='test_get_agents_config_request_success_1'
        pubkey1 = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response1 = agentapi.new_agent_request(passport=psp, agentname=agentname1, pubkey=pubkey1, version=version)
        self.assertTrue(isinstance(response1, webresp.WebInterfaceResponse))
        self.assertEqual(response1.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response1.data['aid']), uuid.UUID))
        for msg in response1.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        agentname2='test_get_agents_config_request_success_2'
        pubkey2 = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response2 = agentapi.new_agent_request(passport=psp, agentname=agentname2, pubkey=pubkey2, version=version)
        self.assertTrue(isinstance(response2, webresp.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response2.data['aid']), uuid.UUID))
        for msg in response2.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response3 = agentapi.get_agents_config_request(passport=psp)
        self.assertTrue(response3.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response3.data)>=2)
        agent_seen=0
        for reg in response3.data:
            if reg['aid']==response1.data['aid']:
                agent_seen+=1
                self.assertEqual(reg['agentname'],agentname1)
                self.assertEqual(reg['state'], AgentStates.ACTIVE)
                self.assertEqual(reg['version'], version)
            elif reg['aid']==response2.data['aid']:
                agent_seen+=1
                self.assertEqual(reg['agentname'],agentname2)
                self.assertEqual(reg['state'], AgentStates.ACTIVE)
                self.assertEqual(reg['version'], version)
        self.assertEqual(agent_seen,2)

    def test_get_agents_config_request_failure_invalid_passport(self):
        ''' get_agents_config_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=agentapi.get_agents_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_agents_config_request_failure_non_existent_username(self):
        ''' get_agents_config_request should fail if username does not exist '''
        psp=passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response=agentapi.get_agents_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GAA_GASC_UNF.value)

    def test_get_agents_config_request_success_no_agents(self):
        ''' get_agents_config_request should succeed but should return an empty array '''
        username = 'test_get_agents_config_success_no_agents'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response,'cookie',None)
        psp = passport.get_user_passport(cookie)
        response2=agentapi.get_agents_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_update_agent_config_request_success(self):
        ''' update_agent_config_request should succeed if agent exists and the new conf is set '''
        psp = self.passport
        agentname='test_update_agent_config_request_success'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
        for msg in response.unrouted_messages:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        new_agentname=agentname+'_new'
        data={'agentname':new_agentname}
        response2 = agentapi.update_agent_config_request(passport=psp, aid=response.data['aid'], data=data)
        self.assertTrue(response2.status, status.WEB_STATUS_OK)
        response3 = agentapi.get_agent_config_request(passport=psp, aid=response.data['aid'])
        self.assertTrue(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['aid'],response.data['aid'])
        self.assertEqual(response3.data['agentname'],new_agentname)
        self.assertEqual(response3.data['state'], AgentStates.ACTIVE)
        self.assertEqual(response3.data['version'], version)

    def test_update_agent_config_request_failure_invalid_passport(self):
        ''' update_agent_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        aid=uuid.uuid4().hex
        data={'agentname':'test_update_agent_config_request_failure'}
        for psp in passports:
            response=agentapi.update_agent_config_request(passport=psp, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_aid(self):
        ''' update_agent_config_request should fail if aid is invalid '''
        aids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(),'23234234hasdfasdfASDFASDF']
        psp=passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        data={'agentname':'test_update_agent_config_request_failure'}
        for aid in aids:
            response=agentapi.update_agent_config_request(passport=psp, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_data(self):
        ''' update_agent_config_request should fail if data is invalid '''
        datas=[None, 32423, 023423.23423,['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(),'23234234hasdfasdfASDFASDF']
        aid=uuid.uuid4().hex
        psp = self.passport
        for data in datas:
            response=agentapi.update_agent_config_request(passport=psp, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_data_keys(self):
        ''' update_agent_config_request should fail if data is invalid '''
        aid=uuid.uuid4().hex
        psp = self.passport
        keys=[234234, 0234234234.023423234,('a','tuple'),'string',None]
        new_agentname='test_update_agent_config_request_failure'
        for key in keys:
            data={key:new_agentname}
            response=agentapi.update_agent_config_request(passport=psp, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_invalid_data_new_agentname(self):
        ''' update_agent_config_request should fail if data is invalid '''
        agentnames=[None, 32423, 023423.23423,['a','list'],('a','tuple'),'user\nname','userñame', uuid.uuid4(),'23234234\thasdfasdfASDFASDF']
        aid=uuid.uuid4().hex
        psp = self.passport
        for name in agentnames:
            data={'agentname':name}
            response=agentapi.update_agent_config_request(passport=psp, aid=aid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_agent_config_request_failure_non_existent_agent(self):
        ''' update_agent_config_request should fail if agent does not exists '''
        psp = self.passport
        aid=uuid.uuid4().hex
        data={'agentname':'new_agentname'}
        response=agentapi.update_agent_config_request(passport=psp, aid=aid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_agent_request_failure_invalid_passport(self):
        ''' delete_agent_request should fail if username is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        aid=uuid.uuid4().hex
        for psp in passports:
            response=agentapi.delete_agent_request(passport=psp, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_agent_request_failure_invalid_aid(self):
        ''' delete_agent_request should fail if aid is invalid '''
        aids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp=passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        for aid in aids:
            response=agentapi.delete_agent_request(passport=psp, aid=aid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

