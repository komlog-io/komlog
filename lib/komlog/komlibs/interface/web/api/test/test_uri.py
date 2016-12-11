import unittest
import uuid
from base64 import b64encode, b64decode
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.auth import passport, permissions
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import agent as agentapi
from komlog.komlibs.interface.web.api import datasource as datasourceapi
from komlog.komlibs.interface.web.api import uri as uriapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komfig import logging
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.auth import permissions


pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')

class InterfaceWebApiUriTest(unittest.TestCase):
    ''' komlibs.interface.web.api.uri tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.uri_user'
        self.password = 'password'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
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
        agentname='test_komlibs.interface.web.api.uri_agent'
        version='test library vX.XX'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        agents_info=agentapi.get_agents_config_request(passport=self.passport)
        self.agents=agents_info.data
        aid = response.data['aid']
        cookie = {'user':self.username, 'sid':uuid.uuid4().hex, 'aid':aid, 'pv':1, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        self.agent_passport = passport.get_agent_passport(cookie)

    def test_get_uri_request_failure_invalid_passport(self):
        ''' get_uri_request should fail if passport is invalid '''
        passports=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
            ('a','tuple'),
            {'set'},
            {'a':'dict'},
            uuid.uuid4(),
            23.32,
        ]
        for psp in passports:
            response=uriapi.get_uri_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uri_request_failure_invalid_uri(self):
        ''' get_uri_request should fail if uri is invalid '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uris=[234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
                ' spacesatbeggining',
                'spacesatend ',
                'three...consecutive.points',
                '.beginswithpoint',
                'endswith.',
                'containsspecialchar$',
                'endswith\t',
                '\nbeginwithnewline',
                'endswith\n',
                ]
        for uri in uris:
            response=uriapi.get_uri_request(passport=psp, uri=uri)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uri_request_failure_user_not_found(self):
        ''' get_uri_request should fail if user does not exist on system '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        response=uriapi.get_uri_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.error, Errors.OK.value)
        self.assertEqual(response.data, {})

    def test_get_uri_request_failure_uri_not_found(self):
        ''' get_uri_request should fail if uri does not exist '''
        psp = self.passport
        uri='test_get_uri_request_failure_uri_not_found'
        response=uriapi.get_uri_request(passport=psp, uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_uri_request_success_without_uri(self):
        ''' get_uri_request should succeed and return uri structure from uid root node '''
        psp = self.passport
        response=uriapi.get_uri_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)

    def test_get_uri_request_success_with_uri(self):
        ''' get_uri_request should succeed and return requested uri and adjacent nodes '''
        psp = self.agent_passport
        uri='test_komlibs.interface.web'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uri_request(passport=psp,uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)

    def test_get_uri_request_failure_with_relative_uri(self):
        ''' get_uri_request should fail relative uris not supported '''
        psp = self.agent_passport
        uri='test_komlibs.interface.web.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        uri='test_komlibs.interface.web.datasource..datasource..web..interface'
        response=uriapi.get_uri_request(passport=psp,uri=uri)
        self.assertEqual(response.error, Errors.E_IWAUR_GUR_IUR.value)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uri_request_failure_global_uri_user_does_not_exist(self):
        ''' get_uri_request should fail if we try to access a non existent global uri '''
        psp = self.agent_passport
        uri='test_get_uri_request_failure_global_uri_user_does_not_exist:uri'
        response=uriapi.get_uri_request(passport=psp,uri=uri)
        self.assertEqual(response.error, autherrors.E_ARA_AGU_RE.value)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_uri_request_failure_global_uri_not_shared(self):
        username = 'test_get_uri_request_failure_global_uri_not_shared'
        password = 'password'
        email=username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp= passport.get_user_passport(cookie)
        agentname='agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
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
        agents_info=agentapi.get_agents_config_request(passport=psp)
        agents=agents_info.data
        aid = response.data['aid']
        cookie = {'user':username, 'sid':uuid.uuid4().hex, 'aid':aid, 'pv':1, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        agent_passport = passport.get_agent_passport(cookie)
        uri=username+':'+'not_shared_uri'
        psp = self.agent_passport
        response=uriapi.get_uri_request(passport=psp,uri=uri)
        self.assertEqual(response.error, autherrors.E_ARA_AGU_RE.value)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_uri_request_failure_global_uri_shared_but_non_existing(self):
        username = 'test_get_uri_request_failure_global_uri_shared_but_non_existing'
        password = 'password'
        email=username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp= passport.get_user_passport(cookie)
        agentname='agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
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
        agents_info=agentapi.get_agents_config_request(passport=psp)
        agents=agents_info.data
        aid = response.data['aid']
        cookie = {'user':username, 'sid':uuid.uuid4().hex, 'aid':aid, 'pv':1, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        agent_passport = passport.get_agent_passport(cookie)
        shared_uri='shared_uri'
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=agent_passport.uid, dest_uid=self.passport.uid,uri=shared_uri, perm=permissions.CAN_READ))
        requested_uri=username+':shared_uri.does_not_exist'
        psp = self.agent_passport
        response=uriapi.get_uri_request(passport=psp,uri=requested_uri)
        self.assertEqual(response.error, Errors.E_IWAUR_GUR_URINF.value)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_uri_request_success_global_uri(self):
        username = 'test_get_uri_request_success_global_uri'
        password = 'password'
        email=username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp= passport.get_user_passport(cookie)
        agentname='agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
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
        agents_info=agentapi.get_agents_config_request(passport=psp)
        agents=agents_info.data
        aid = response.data['aid']
        cookie = {'user':username, 'sid':uuid.uuid4().hex, 'aid':aid, 'pv':1, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        agent_passport = passport.get_agent_passport(cookie)
        shared_uri='shared_uri.datasource'
        response = datasourceapi.new_datasource_request(passport=agent_passport, datasourcename=shared_uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=agent_passport.uid, dest_uid=self.passport.uid,uri=shared_uri, perm=permissions.CAN_READ))
        requested_uri=username+':'+shared_uri
        psp = self.passport
        response=uriapi.get_uri_request(passport=psp,uri=requested_uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['children'],[])
        self.assertEqual(response.data['name'],'shared_uri.datasource')
        self.assertEqual(response.data['type'],'d')

    def test_share_uri_request_failure_invalid_passport(self):
        ''' share_uri_request should fail if passport is invalid '''
        passports=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
            ('a','tuple'),
            {'set'},
            {'a':'dict'},
            uuid.uuid4(),
            23.32,
        ]
        uri='uri'
        users=['user1','user2','user3']
        for psp in passports:
            response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_SUR_IPSP.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_share_uri_request_failure_invalid_uri(self):
        ''' share_uri_request should fail if uri is invalid '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uris=[234234,
            'with spaces',
            'withspecialcharacterslike\t',
            'or\ncharacter',
            ' spacesatbeggining',
            'spacesatend ',
            'three...consecutive.points',
            '.beginswithpoint',
            'endswith.',
            'containsspecialchar$',
            'endswith\t',
            '\nbeginwithnewline',
            'endswith\n',
            'global:uri',
            'relative..uri',
        ]
        users=['user1','user2','user3']
        for uri in uris:
            response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_SUR_IURI.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_share_uri_request_failure_invalid_users(self):
        ''' share_uri_request should fail if users is not a list '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uri='local.uri'
        userss=[None,1,132,33.33,-1231,tuple(),dict(),set(),'username',uuid.uuid4(),uuid.uuid1()]
        for users in userss:
            response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_SUR_IUSERS.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_share_uri_request_failure_invalid_user_item(self):
        ''' share_uri_request should fail if a users item is not a valid username '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uri='local.uri'
        invalid_users=[None,1,132,33.33,-1231,tuple(),dict(),set(),'username not valid',uuid.uuid4(),uuid.uuid1()]
        for user in invalid_users:
            users=['user1','user2','user3']
            users.append(user)
            response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_SUR_IUSER.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_share_uri_request_failure_no_users_to_share(self):
        ''' share_uri_request should fail if request has no users to share to '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uri='local.uri'
        users=[]
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.error, Errors.E_IWAUR_SUR_NUSER.value)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_share_uri_request_failure_non_existent_uri(self):
        ''' share_uri_request should fail if uri does not exist '''
        username='test_share_uri_request_failure_non_existent_uri'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        psp = passport.Passport(uid=uuid.UUID(response.data['uid']),sid=uuid.uuid4())
        uri='non_existent_uri'
        users=['user1']
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.error, Errors.E_IWAUR_SUR_URINF.value)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_share_uri_request_failure_non_existent_dest_user(self):
        ''' share_uri_request should fail if dest_user does not exist '''
        username='test_share_uri_request_failure_non_existent_dest_user'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        uri='uris.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=['non_existent_user']
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.error, gesterrors.E_GUA_GUID_UNF.value)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_share_uri_request_success(self):
        ''' share_uri_request should succeed '''
        username='test_share_uri_request_success'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        ds_uri='uris.datasource'
        uri='uris'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
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
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)

    def test_unshare_uri_request_failure_invalid_passport(self):
        ''' unshare_uri_request should fail if passport is invalid '''
        passports=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
            ('a','tuple'),
            {'set'},
            {'a':'dict'},
            uuid.uuid4(),
            23.32,
        ]
        uri='uri'
        users=['user1','user2','user3']
        for psp in passports:
            response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_USUR_IPSP.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_unshare_uri_request_failure_invalid_uri(self):
        ''' unshare_uri_request should fail if uri is invalid '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uris=[234234,
            'with spaces',
            'withspecialcharacterslike\t',
            'or\ncharacter',
            ' spacesatbeggining',
            'spacesatend ',
            'three...consecutive.points',
            '.beginswithpoint',
            'endswith.',
            'containsspecialchar$',
            'endswith\t',
            '\nbeginwithnewline',
            'endswith\n',
            'global:uri',
            'relative..uri',
        ]
        users=['user1','user2','user3']
        for uri in uris:
            response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_USUR_IURI.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_unshare_uri_request_failure_invalid_users(self):
        ''' unshare_uri_request should fail if users is not a list '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uri='local.uri'
        userss=[1,132,33.33,-1231,tuple(),dict(),set(),'username',uuid.uuid4(),uuid.uuid1()]
        for users in userss:
            response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_USUR_IUSERS.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_unshare_uri_request_failure_invalid_user_item(self):
        ''' unshare_uri_request should fail if a users item is not a valid username '''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        uri='local.uri'
        invalid_users=[None,1,132,33.33,-1231,tuple(),dict(),set(),'username not valid',uuid.uuid4(),uuid.uuid1()]
        for user in invalid_users:
            users=['user1','user2','user3']
            users.append(user)
            response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=users)
            self.assertEqual(response.error, Errors.E_IWAUR_USUR_IUSER.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_unshare_uri_request_failure_non_existent_uri(self):
        ''' unshare_uri_request should fail if uri does not exist '''
        username='test_unshare_uri_request_failure_non_existent_uri'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        psp = passport.Passport(uid=uuid.UUID(response.data['uid']),sid=uuid.uuid4())
        uri='non_existent_uri'
        response=uriapi.unshare_uri_request(passport=psp, uri=uri)
        self.assertEqual(response.error, Errors.E_IWAUR_USUR_URINF.value)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_unshare_uri_request_success_non_shared_previously_no_user_specified(self):
        ''' unshare_uri_request should succeed even if uri was not shared previously '''
        username='test_unshare_uri_request_success_non_shared_previously_no_user_specified'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        ds_uri='uris.datasource'
        uri='uris'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        response=uriapi.unshare_uri_request(passport=psp, uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})

    def test_unshare_uri_request_success_non_shared_previously_non_existent_users_specified(self):
        ''' unshare_uri_request should succeed even if uri was not shared previously '''
        username='test_unshare_uri_request_success_non_shared_previously_non_existent_users_specified'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        uri='uris.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'non_existent_user1',username+'non_existent_user2']
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})

    def test_unshare_uri_request_success_non_shared_previously_existent_users_specified(self):
        ''' unshare_uri_request should succeed even if uri was not shared previously '''
        username='test_unshare_uri_request_success_non_shared_previously_existent_users_specified'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        uri='uris.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'dest_1',username+'dest_2',username+'dest_3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
            uid = uuid.UUID(response.data['uid'])
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {})
        self.assertEqual(users_checked,3)

    def test_unshare_uri_request_success_shared_previously_no_user_specified(self):
        ''' unshare_uri_request should succeed removing the share completely '''
        username='test_unshare_uri_request_success_shared_previously_no_user_specified'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        uri='uris.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'dest_1',username+'dest_2',username+'dest_3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(users))
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response=uriapi.unshare_uri_request(passport=psp, uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {})
        self.assertEqual(users_checked,3)

    def test_unshare_uri_request_success_shared_previously_user_specified(self):
        ''' unshare_uri_request should succeed removing the share from the specified users '''
        username='test_unshare_uri_request_success_shared_previously_user_specified'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        uri='uris.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'dest_1',username+'dest_2',username+'dest_3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(users))
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        specified_users=users[0:1]
        specified_uid=dest_uids[0:1]
        keep_share_users=users[1:]
        keep_share_uid=dest_uids[1:]
        response=uriapi.unshare_uri_request(passport=psp, uri=uri,users=specified_users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(keep_share_users))
        users_checked=0
        for dest_uid in specified_uid:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {})
        self.assertEqual(users_checked,1)
        users_checked=0
        for dest_uid in keep_share_uid:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,2)

    def test_unshare_uri_request_success_shared_previously_non_existent_user_specified(self):
        ''' unshare_uri_request should keep the share to non specified users '''
        username='test_unshare_uri_request_success_shared_previously_non_existent_user_specified'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        uri='uris.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'dest_1',username+'dest_2',username+'dest_3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(users))
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        non_existent=[username+'non_existent1',username+'non_existent2']
        response=uriapi.unshare_uri_request(passport=psp, uri=uri, users=non_existent)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(users))
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)

    def test_get_uris_shared_request_failure_invalid_passport(self):
        ''' get_uris_shared_request should fail if passport is invalid '''
        passports=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
            ('a','tuple'),
            {'set'},
            {'a':'dict'},
            uuid.uuid4(),
            23.32,
        ]
        for psp in passports:
            response=uriapi.get_uris_shared_request(passport=psp)
            self.assertEqual(response.error, Errors.E_IWAUR_GUSR_IPSP.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uris_shared_request_success_no_shares(self):
        ''' get_uris_shared_request should succeed, returning an empty dict if no data is shared'''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        response=uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})

    def test_get_uris_shared_request_success_one_share(self):
        ''' get_uris_shared_request should succeed returning the shares '''
        username='test_get_uris_shared_request_success_one_share'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        ds_uri='uris.datasource'
        uri='uris'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(users))
        for dest_uid in dest_uids:
            perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertIsNotNone(perm)
            self.assertEqual(perm.uid, uid)
            self.assertEqual(perm.dest_uid, dest_uid)
            self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
            self.assertEqual(perm.uri,uri)

    def test_get_uris_shared_request_success_some_shares(self):
        ''' get_uris_shared_request should succeed returning the shares '''
        username='test_get_uris_shared_request_success_some_shares'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        ds_uri='uris.datasources.thisone'
        uris=['uris','uris.datasources']
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        for uri in uris:
            response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(username in response.data)
            self.assertEqual(len(response.data.keys()),1)
            self.assertEqual(sorted(response.data[username]),sorted(uris))
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uris[0] in response.data)
        self.assertTrue(uris[1] in response.data)
        self.assertEqual(len(response.data.keys()),2)
        self.assertEqual(sorted(response.data[uris[0]]),sorted(users))
        self.assertEqual(sorted(response.data[uris[1]]),sorted(users))
        for dest_uid in dest_uids:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
                self.assertIsNotNone(perm)
                self.assertEqual(perm.uid, uid)
                self.assertEqual(perm.dest_uid, dest_uid)
                self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                self.assertEqual(perm.uri,uri)

    def test_get_uris_shared_request_success_some_shares_one_user_left_system(self):
        ''' get_uris_shared_request should succeed returning the shares and updating shares if one user has left the system in the mean time '''
        username='test_get_uris_shared_request_success_some_shares_one_user_left_system'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        ds_uri='uris.datasources.thisone'
        uris=['uris','uris.datasources']
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        for uri in uris:
            response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(username in response.data)
            self.assertEqual(len(response.data.keys()),1)
            self.assertEqual(sorted(response.data[username]),sorted(uris))
        self.assertEqual(users_checked,3)
        #now for some reason one user leaves the system
        psp = passport.Passport(uid=dest_uids[0],sid=uuid.uuid4())
        response = userapi.delete_user_request(passport=psp)
        if response.status==status.WEB_STATUS_RECEIVED:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        #check nothing has happened yet to the shares
        for dest_uid in dest_uids:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
                self.assertIsNotNone(perm)
                self.assertEqual(perm.uid, uid)
                self.assertEqual(perm.dest_uid, dest_uid)
                self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                self.assertEqual(perm.uri,uri)
                perm = cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
                self.assertIsNotNone(perm)
                self.assertEqual(perm.uid, dest_uid)
                self.assertEqual(perm.owner_uid, uid)
                self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                self.assertEqual(perm.uri,uri)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uris[0] in response.data)
        self.assertTrue(uris[1] in response.data)
        self.assertEqual(len(response.data.keys()),2)
        self.assertEqual(sorted(response.data[uris[0]]),sorted(users[1:]))
        self.assertEqual(sorted(response.data[uris[1]]),sorted(users[1:]))
        for dest_uid in dest_uids[1:]:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
                self.assertIsNotNone(perm)
                self.assertEqual(perm.uid, uid)
                self.assertEqual(perm.dest_uid, dest_uid)
                self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                self.assertEqual(perm.uri,uri)
        for uri in uris:
            perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uids[0], uri=uri)
            self.assertIsNone(perm)
            perm = cassapiperm.get_user_shared_uris_with_me(uid=dest_uids[0])
            self.assertEqual(perm,[])

    def test_get_uris_shared_with_me_request_failure_invalid_passport(self):
        ''' get_uris_shared_with_me_request should fail if passport is invalid '''
        passports=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
            ('a','tuple'),
            {'set'},
            {'a':'dict'},
            uuid.uuid4(),
            23.32,
        ]
        for psp in passports:
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.error, Errors.E_IWAUR_GUSWMR_IPSP.value)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uris_shared_with_me_request_success_no_shares(self):
        ''' get_uris_shared_with_me_request should succeed, returning an empty dict if no data is shared'''
        psp = passport.Passport(uid=uuid.uuid4(),sid=uuid.uuid4())
        response=uriapi.get_uris_shared_with_me_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {})

    def test_get_uris_shared_with_me_request_success_one_share(self):
        ''' get_uris_shared_with_me_request should succeed returning the shares '''
        username='test_get_uris_shared_with_me_request_success_one_share'
        password='password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
        uid = uuid.UUID(response.data['uid'])
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
        psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
        ds_uri='uris.datasource'
        uri='uris'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(response.data, {username:[uri]})
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uri in response.data)
        self.assertEqual(len(response.data.keys()),1)
        self.assertEqual(sorted(response.data[uri]),sorted(users))
        for dest_uid in dest_uids:
            perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
            self.assertIsNotNone(perm)
            self.assertEqual(perm.uid, uid)
            self.assertEqual(perm.dest_uid, dest_uid)
            self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
            self.assertEqual(perm.uri,uri)

    def test_get_uris_shared_with_me_request_success_some_shares(self):
        ''' get_uris_shared_request should succeed returning the shares '''
        username='test_get_uris_shared_with_me_request_success_some_shares'
        owner_ids=[]
        for i in range(0,10):
            user=username+str(i)
            password='password'
            email =user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
            owner_ids.append(uuid.UUID(response.data['uid']))
            uid = uuid.UUID(response.data['uid'])
            psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
            psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
            ds_uri='uris.datasources.thisone'
            uris=['uris','uris.datasources']
            response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
            if response.status==status.WEB_STATUS_OK:
                msgs=response.unrouted_messages
                while len(msgs)>0:
                    for msg in msgs:
                        msgs.remove(msg)
                        msgresponse=msgapi.process_message(msg)
                        for msg2 in msgresponse.unrouted_messages:
                            msgs.append(msg2)
                        self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        for uid in owner_ids:
            psp = passport.Passport(uid=uid,sid=uuid.uuid4())
            for uri in uris:
                response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
                self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(len(response.data.keys()),10)
            for i in range(0,10):
                user=username+str(i)
                self.assertTrue(user in response.data)
                self.assertEqual(sorted(response.data[user]),sorted(uris))
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uris[0] in response.data)
        self.assertTrue(uris[1] in response.data)
        self.assertEqual(len(response.data.keys()),2)
        self.assertEqual(sorted(response.data[uris[0]]),sorted(users))
        self.assertEqual(sorted(response.data[uris[1]]),sorted(users))
        for dest_uid in dest_uids:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
                self.assertIsNotNone(perm)
                self.assertEqual(perm.uid, uid)
                self.assertEqual(perm.dest_uid, dest_uid)
                self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                self.assertEqual(perm.uri,uri)

    def test_get_uris_shared_with_me_request_success_some_shares_one_user_left_system(self):
        ''' get_uris_shared_request should succeed returning the shares and updating shares if one user has left the system in the mean time '''
        username='test_get_uris_shared_with_me_request_success_some_shares_one_user_left_system'
        owner_ids=[]
        for i in range(0,10):
            user=username+str(i)
            password='password'
            email =user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
            owner_ids.append(uuid.UUID(response.data['uid']))
            uid = uuid.UUID(response.data['uid'])
            psp = passport.Passport(uid=uid,sid=uuid.uuid4())
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
            psp = passport.Passport(uid=uid,aid=aid,pv=1,sid=uuid.uuid4())
            ds_uri='uris.datasources.thisone'
            uris=['uris','uris.datasources']
            response = datasourceapi.new_datasource_request(passport=psp, datasourcename=ds_uri)
            if response.status==status.WEB_STATUS_OK:
                msgs=response.unrouted_messages
                while len(msgs)>0:
                    for msg in msgs:
                        msgs.remove(msg)
                        msgresponse=msgapi.process_message(msg)
                        for msg2 in msgresponse.unrouted_messages:
                            msgs.append(msg2)
                        self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        users=[username+'_dest1',username+'_dest2',username+'_dest3']
        dest_uids=[]
        for user in users:
            password='password'
            email = user+'@komlog.org'
            response = userapi.new_user_request(username=user, password=password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            dest_uids.append(uuid.UUID(response.data['uid']))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        for uid in owner_ids:
            psp = passport.Passport(uid=uid,sid=uuid.uuid4())
            for uri in uris:
                response=uriapi.share_uri_request(passport=psp, uri=uri, users=users)
                self.assertEqual(response.status, status.WEB_STATUS_OK)
        users_checked=0
        for dest_uid in dest_uids:
            users_checked+=1
            psp = passport.Passport(uid=dest_uid,sid=uuid.uuid4())
            response=uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(len(response.data.keys()),10)
            for i in range(0,10):
                user=username+str(i)
                self.assertTrue(user in response.data)
                self.assertEqual(sorted(response.data[user]),sorted(uris))
        self.assertEqual(users_checked,3)
        psp = passport.Passport(uid=uid,sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(uris[0] in response.data)
        self.assertTrue(uris[1] in response.data)
        self.assertEqual(len(response.data.keys()),2)
        self.assertEqual(sorted(response.data[uris[0]]),sorted(users))
        self.assertEqual(sorted(response.data[uris[1]]),sorted(users))
        for dest_uid in dest_uids:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
                self.assertIsNotNone(perm)
                self.assertEqual(perm.uid, uid)
                self.assertEqual(perm.dest_uid, dest_uid)
                self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                self.assertEqual(perm.uri,uri)
        #now some users leave system (owner1 and dest1)
        for uid in (dest_uids[0],owner_ids[0]):
            psp = passport.Passport(uid=uid,sid=uuid.uuid4())
            response = userapi.delete_user_request(passport=psp)
            if response.status==status.WEB_STATUS_RECEIVED:
                msgs=response.unrouted_messages
                while len(msgs)>0:
                    for msg in msgs:
                        msgs.remove(msg)
                        msgresponse=msgapi.process_message(msg)
                        for msg2 in msgresponse.unrouted_messages:
                            msgs.append(msg2)
                        self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
            response = userapi.get_user_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        #check perms stay the same right now for users
        for owner in owner_ids:
            for dest in dest_uids:
                for uri in uris:
                    perm = cassapiperm.get_user_shared_uri_perm(uid=owner, dest_uid=dest, uri=uri)
                    self.assertIsNotNone(perm)
                    self.assertEqual(perm.uid, owner)
                    self.assertEqual(perm.dest_uid, dest)
                    self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                    self.assertEqual(perm.uri,uri)
                    perm = cassapiperm.get_user_shared_uri_with_me_perm(uid=dest, owner_uid=owner, uri=uri)
                    self.assertIsNotNone(perm)
                    self.assertEqual(perm.uid, dest)
                    self.assertEqual(perm.owner_uid, owner)
                    self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                    self.assertEqual(perm.uri,uri)
        #now make get_uris_shared_with_me requests and see how perms are updated
        for dest in dest_uids[1:]:
            psp = passport.Passport(uid=dest,sid=uuid.uuid4())
            response = uriapi.get_uris_shared_with_me_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertEqual(len(response.data.keys()),9)
            for i in range(1,10):
                user=username+str(i)
                self.assertTrue(user in response.data)
                self.assertEqual(sorted(response.data[user]),sorted(uris))
        for owner in owner_ids[1:]:
            psp = passport.Passport(uid=owner,sid=uuid.uuid4())
            response = uriapi.get_uris_shared_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(uris[0] in response.data)
            self.assertTrue(uris[1] in response.data)
            self.assertEqual(len(response.data.keys()),2)
            self.assertEqual(sorted(response.data[uris[0]]),sorted(users[1:]))
            self.assertEqual(sorted(response.data[uris[1]]),sorted(users[1:]))
        psp = passport.Passport(uid=dest_uids[0],sid=uuid.uuid4())
        response = uriapi.get_uris_shared_with_me_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data,{})
        psp = passport.Passport(uid=owner_ids[0],sid=uuid.uuid4())
        response = uriapi.get_uris_shared_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data,{})
        for owner in owner_ids[1:]:
            for dest in dest_uids[1:]:
                for uri in uris:
                    perm = cassapiperm.get_user_shared_uri_perm(uid=owner, dest_uid=dest, uri=uri)
                    self.assertIsNotNone(perm)
                    self.assertEqual(perm.uid, owner)
                    self.assertEqual(perm.dest_uid, dest)
                    self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                    self.assertEqual(perm.uri,uri)
                    perm = cassapiperm.get_user_shared_uri_with_me_perm(uid=dest, owner_uid=owner, uri=uri)
                    self.assertIsNotNone(perm)
                    self.assertEqual(perm.uid, dest)
                    self.assertEqual(perm.owner_uid, owner)
                    self.assertEqual(perm.perm, permissions.CAN_READ|permissions.CAN_SNAPSHOT)
                    self.assertEqual(perm.uri,uri)
        for dest in dest_uids:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=owner_ids[0],dest_uid=dest,uri=uri)
                self.assertIsNone(perm)
                perm = cassapiperm.get_user_shared_uri_with_me_perm(uid=dest, owner_uid=owner_ids[0], uri=uri)
                self.assertIsNone(perm)
        for owner in owner_ids:
            for uri in uris:
                perm = cassapiperm.get_user_shared_uri_perm(uid=owner,dest_uid=dest_uids[0],uri=uri)
                self.assertIsNone(perm)
                perm = cassapiperm.get_user_shared_uri_with_me_perm(uid=dest_uids[0], owner_uid=owner, uri=uri)
                self.assertIsNone(perm)

