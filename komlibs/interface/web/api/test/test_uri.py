import unittest
import uuid
from komlibs.auth import operations
from komlibs.general.time import timeuuid
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.api import agent as agentapi 
from komlibs.interface.web.api import datasource as datasourceapi 
from komlibs.interface.web.api import uri as uriapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions
from komlibs.interface.imc.model import messages
from komlibs.interface.imc.api import rescontrol
from komimc import bus, routing
from komimc import api as msgapi
from komfig import logger


class InterfaceWebApiUriTest(unittest.TestCase):
    ''' komlibs.interface.web.api.uri tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        username = 'test_komlibs.interface.web.api.uri_user'
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
            agentname='test_komlibs.interface.web.api.uri_agent'
            pubkey='TESTKOMLIBSINTERFACEWEBAPIURIAGENT'
            version='test library vX.XX'
            response = agentapi.new_agent_request(username=self.userinfo['username'], agentname=agentname, pubkey=pubkey, version=version)
            aid=response.data['aid']
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
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
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
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
            datasourcename='test_komlibs.interface.web.api.uri_datasource'
            response = datasourceapi.new_datasource_request(username=self.userinfo['username'], aid=aid, datasourcename=datasourcename)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
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
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
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

    def test_get_uri_request_failure_invalid_username(self):
        ''' get_uri_request should fail if username is invalid '''
        usernames=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
                ' spacesatbeggining',
                'spacesatend ',
                'Capitals',
                'Two..consecutivepoints',
                '.beginswithpoint',
                'endswith.',
                'containsspecialchar$',
                'endswith\t',
                '\nbeginwithnewline',
                'endswith\n',
                '',
                ]
        for username in usernames:
            response=uriapi.get_uri_request(username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uri_request_failure_invalid_uri(self):
        ''' get_uri_request should fail if uri is invalid '''
        username=self.userinfo['username']
        uris=[234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
                ' spacesatbeggining',
                'spacesatend ',
                'Capitals',
                'Three...consecutive.points',
                '.beginswithpoint',
                'endswith.',
                'containsspecialchar$',
                'endswith\t',
                '\nbeginwithnewline',
                'endswith\n',
                ]
        for uri in uris:
            response=uriapi.get_uri_request(username=username, uri=uri)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uri_request_failure_user_not_found(self):
        ''' get_uri_request should fail if user does not exist on system '''
        username='test_get_uri_request_failure_user_not_found'
        response=uriapi.get_uri_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_uri_request_failure_uri_not_found(self):
        ''' get_uri_request should fail if uri does not exist '''
        username=self.userinfo['username']
        uri='test_get_uri_request_failure_uri_not_found'
        response=uriapi.get_uri_request(username=username, uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_uri_request_success_without_uri(self):
        ''' get_uri_request should succeed and return uri structure from uid root node '''
        username=self.userinfo['username']
        uid=self.userinfo['uid']
        response=uriapi.get_uri_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data['v']),6)
        self.assertEqual(len(response.data['e']),5)
        found=0
        for reg in response.data['v']:
            if reg['id']==uid:
                found+=1
        self.assertEqual(found,1)

    def test_get_uri_request_success_with_uri(self):
        ''' get_uri_request should succeed and return requested uri and adjacent nodes '''
        username=self.userinfo['username']
        uri='test_komlibs.interface.web'
        response=uriapi.get_uri_request(username=username,uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data['v']),6)
        self.assertEqual(len(response.data['e']),5)

    def test_get_uri_request_success_with_relative_uri(self):
        ''' get_uri_request should succeed and return requested uri and adjacent nodes '''
        username=self.userinfo['username']
        uri='test_komlibs.interface.web..web..interface'
        response=uriapi.get_uri_request(username=username,uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data['v']),6)
        self.assertEqual(len(response.data['e']),5)

