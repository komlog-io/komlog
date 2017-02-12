import unittest
import uuid
import json
from komlog.komfig import logging
from base64 import b64decode, b64encode
from komlog.komcass.api import interface as cassapiiface
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.resources import update as resupdate
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import agent as agentapi
from komlog.komlibs.interface.web.api import datasource as datasourceapi
from komlog.komlibs.interface.web.api import uri as uriapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komlibs.interface.imc.model import messages
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi

pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')

class InterfaceWebApiDatasourceTest(unittest.TestCase):
    ''' komlibs.interface.web.api.datasource tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.datasource_user'
        self.password = 'password'
        agentname='test_komlibs.interface.web.api.datasource_agent'
        version='test library vX.XX'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            for msg in response.unrouted_messages:
                if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                    code = msg.code
                    userapi.confirm_user_request(email=email, code=code)
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
            response = loginapi.login_request(username=self.username, password=self.password)
            cookie=getattr(response, 'cookie',None)
            self.passport = passport.get_user_passport(cookie)
            response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
            aid = response.data['aid']
            cookie = passport.AgentCookie(aid=uuid.UUID(aid), pv=1, sid=uuid.uuid4(), seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
            self.agent_passport = passport.get_agent_passport(cookie)
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
            datasourcename='datasource'
            response = datasourceapi.new_datasource_request(passport=self.agent_passport, datasourcename=datasourcename)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        self.passport = passport.get_user_passport(cookie)
        response = agentapi.get_agents_config_request(passport=self.passport)
        self.agents = response.data

    def test_get_datasource_config_request_success(self):
        ''' get_datasource_config_request should succeed returning the datasource config '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        response = datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('datasourcename' in response.data)
        self.assertTrue('aid' in response.data)
        self.assertTrue('did' in response.data)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response.data['aid']), uuid.UUID))
        self.assertEqual(self.agents[0]['aid'], response.data['aid'])

    def test_get_datasource_config_request_success_remote_datasource(self):
        ''' get_datasource_config_request should succeed, returning datasource info
            indicating global uri if datasource owner is different from the one who
            requested the info. '''
        username='test_get_datasource_config_request_success_remote_datasource'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.UserPassport(uid=uid,sid=uuid.uuid4())
        agentname='agent'
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=psp, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        aid = uuid.UUID(response.data['aid'])
        psp = passport.UserPassport(uid=uid,sid=uuid.uuid4())
        ds_uri='uris.datapoint'
        uri='uris'
        datasource=gestdatasourceapi.create_datasource(uid=uid, aid=aid,datasourcename=ds_uri)
        did=datasource['did']
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        response=datasourceapi.get_datasource_config_request(passport=psp,did=did.hex)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['did'],did.hex)
        self.assertEqual(response.data['datasourcename'],ds_uri)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            for msg in response.unrouted_messages:
                if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                    code = msg.code
                    userapi.confirm_user_request(email=email, code=code)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
            uid = uuid.UUID(response.data['uid'])
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.UserPassport(uid=dest_uid,sid=uuid.uuid4())
            response=datasourceapi.get_datasource_config_request(passport=psp,did=did.hex)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data['did'],did.hex)
            self.assertEqual(response.data['datasourcename'],':'.join((username,ds_uri)))
        self.assertEqual(users_checked,3)

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
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        for did in dids:
            response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_config_request_failure_non_existent_username(self):
        ''' get_datasource_config_request should fail if username does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSC_RE.value)

    def test_get_datasource_config_request_failure_non_existent_datasource(self):
        ''' get_datasource_config_request should fail if datasource does not exist '''
        psp = self.passport
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSC_RE.value)

    def test_get_datasource_config_request_failure_no_permission_over_this_datasource(self):
        ''' get_datasource_config_request should fail if user does not have permission over datasource '''
        username = 'test_get_datasource_config_request_failure_no_permission_over_datasource_user'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        response = loginapi.login_request(username=username, password = password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        did = self.agents[0]['dids'][0]
        response= datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSC_RE.value)

    def test_get_datasources_config_request_success(self):
        ''' get_datasources_config_request should succeed if username exists and return the datasources config '''
        username=self.username
        aid=self.agents[0]['aid']
        cookie = passport.AgentCookie(aid=uuid.UUID(aid), pv=1, sid=uuid.uuid4(), seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
        psp = passport.get_agent_passport(cookie)
        datasourcename='test_get_datasource_config_request_success_datasource_ds'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        cookie = passport.UserCookie(user=username, sid=uuid.uuid4(), seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
        psp= passport.get_user_passport(cookie)
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
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response=datasourceapi.get_datasources_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_datasources_config_request_success_no_datasources(self):
        ''' get_datasources_config_request should succeed but should return an empty array '''
        username = 'test_get_datasources_config_success_no_datasources'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        response2=datasourceapi.get_datasources_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

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
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
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
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        datas=[None, 2342342, uuid.uuid4(), '2342342','234 234 223 ','stringwithñ',['a','list'],('a','tuple'),json.dumps('jsonstring')]
        for data in datas:
            response=datasourceapi.update_datasource_config_request(passport=psp,did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_invalid_data_content(self):
        ''' update_datasource_config should fail if data is invalid '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        datas=[{'a':'dict'},]
        for datasourcename in [None, 234234, 23423.234234, ['a','list'],{'a':'dict'},('a','tuple'),'Invalid\tdatasourcename','Invalid\n','ÑÑnovalid']:
            datas.append({'datasourcename':datasourcename})
        for data in datas:
            response=datasourceapi.update_datasource_config_request(passport=psp,did=did, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datasource_config_request_failure_non_existent_user(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        psp =passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        new_datasourcename='test_update_datasource_config_request_failure'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(passport=psp, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDSC_RE.value)

    def test_update_datasource_config_request_failure_non_existent_did(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=uuid.uuid4().hex
        new_datasourcename='test_update_datasource_config_failure_non_existent_did'
        data={'datasourcename':new_datasourcename}
        response=datasourceapi.update_datasource_config_request(passport=psp, did=did, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDSC_RE.value)

    def test_update_datasource_config_request_failure_no_permission_over_datasource(self):
        ''' update_datasource_config should succeed if user and did exists, user have permission and datasourcename parameter is passed '''
        username='test_update_datasource_config_request_failure_no_permission_over_datasource'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
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
        cookie = passport.AgentCookie(aid=uuid.UUID(aid),pv=1,  sid=uuid.uuid4(), seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
        psp= passport.get_agent_passport(cookie)
        datasourcename='test_new_datasource_request_success'
        response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']),uuid.UUID))
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        cookie = passport.UserCookie(user=username, sid=uuid.uuid4(), seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
        psp= passport.get_user_passport(cookie)
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

    def test_new_datasource_request_failure_invalid_datasourcename(self):
        ''' new_datasource_request should fail if datasourcename is invalid '''
        datasourcenames=[None, 234234, 23423.02342, 'Datasource Name ÑÑ', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername']
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        for datasourcename in datasourcenames:
            response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_request_failure_no_permission_over_agent(self):
        ''' new_datasource_request should fail if user has no permission over this agent '''
        username='test_new_datasource_request_failure_no_permission_over_agent'
        password='temporal'
        email=username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        uid = uuid.UUID(response.data['uid'])
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.unrouted_messages:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        cookie = passport.AgentCookie(aid=uuid.UUID(self.agents[0]['aid']),sid=uuid.uuid4(), pv=1, seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
        psp= passport.get_agent_passport(cookie)
        psp.uid = uid
        datasourcename='test_new_datasource_request_failure_no_permission_over_agent'
        response=datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ANDS_RE.value)

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
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        for did in dids:
            response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datasource_data_request_failure_invalid_tid(self):
        ''' get_datasource_data_request should fail if tid is invalid '''
        tids=[234234, 23423.02342, 'UserName', {'a':'dict'},['a','list'],('a','tuple'),'a\ninvalid\tusername',uuid.uuid4()]
        psp=passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=uuid.uuid4().hex
        for tid in tids:
            response=datasourceapi.get_datasource_data_request(passport=psp, did=did, tid=tid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWADS_GDSDR_IT.value)

    def test_get_datasource_data_request_failure_non_existent_datasource(self):
        ''' get_datasource_data_request should fail if datasource does not exist '''
        psp = self.passport
        did=uuid.uuid4().hex
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_datasource_data_request_failure_non_existent_username(self):
        ''' get_datasource_data_request should fail if user does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDSD_RE.value)

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

    def test_get_datasource_data_request_failure_date_requested_less_than_interval_bound_limit(self):
        ''' get_datasource_data_request should fail if date requested is less than the date set
            in the deny interface '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 4 5 6'
        date=timeuuid.uuid1(seconds=1000)
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        seq=timeuuid.get_custom_sequence(date)
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_ALLOWED)
        self.assertEqual(response.error, autherrors.E_AQA_AGDSD_IBE.value)
        self.assertEqual(response.data, {'error':autherrors.E_AQA_AGDSD_IBE.value})
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_get_datasource_data_request_failure_date_requested_empty_but_last_processed_less_than_interval_bound_limit(self):
        ''' get_datasource_data_request should fail if date requested is less than the date set
            in the deny interface '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 4 5 6'
        date=timeuuid.uuid1(seconds=1000)
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=5000)
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_ALLOWED)
        self.assertEqual(response.error, Errors.E_IWADS_GDSDR_LDBL.value)
        self.assertEqual(response.data, {'error':Errors.E_IWADS_GDSDR_LDBL.value})
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_get_datasource_data_request_failure_date_requested_empty_but_limit_is_in_the_future(self):
        ''' get_datasource_data_request should fail if date set in the interval bounds limit is in the future '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 4 5 6'
        date=timeuuid.uuid1(seconds=1000)
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.HIGHEST_TIME_UUID
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_ALLOWED)
        self.assertEqual(response.error, Errors.E_IWADS_GDSDR_ADIF.value)
        self.assertEqual(response.data, {'error':Errors.E_IWADS_GDSDR_ADIF.value})
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_get_datasource_data_request_success_date_requested_empty_but_last_processed_after_than_interval_bound_limit(self):
        ''' get_datasource_data_request should succeed if date requested is empty and date retrieved is after than the date set in the deny interface '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 4 5 6'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=100)
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_get_datasource_data_request_failure_interval_bound_set_and_data_requested_after_limit_does_not_exist(self):
        ''' get_datasource_data_request should fail if date requested is after limit, but does not exist '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 4 5 6'
        date=timeuuid.uuid1(seconds=5000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=4000)
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        seq=timeuuid.get_custom_sequence(date)
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GDA_GMDD_DDNF.value)
        self.assertEqual(response.data, {'error':gesterrors.E_GDA_GMDD_DDNF.value})
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_get_datasource_data_request_success_interval_bound_set_and_data_requested_after_limit_does_exist(self):
        ''' get_datasource_data_request should succeed if date requested is after limit, and data exists '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        content='get_datasource_data content 4 5 6'
        date=timeuuid.uuid1(seconds=5000)
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=4000)
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        response=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_delete_datasource_request_failure_invalid_passport(self):
        ''' delete_datasource_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        did=uuid.uuid4().hex
        for psp in passports:
            response=datasourceapi.delete_datasource_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWADS_DDSR_IPSP.value)

    def test_delete_datasource_request_failure_invalid_did(self):
        ''' delete_datasource_request should fail if did is invalid '''
        dids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        for did in dids:
            response=datasourceapi.delete_datasource_request(passport=psp, did=did)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWADS_DDSR_ID.value)

