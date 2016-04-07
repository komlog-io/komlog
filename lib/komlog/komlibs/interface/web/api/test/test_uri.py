import unittest
import uuid
from base64 import b64encode, b64decode
from komlog.komlibs.auth import operations
from komlog.komlibs.auth import passport
from komlog.komlibs.auth import errors as autherrors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi 
from komlog.komlibs.interface.web.api import agent as agentapi 
from komlog.komlibs.interface.web.api import datasource as datasourceapi 
from komlog.komlibs.interface.web.api import uri as uriapi 
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komfig import logging


class InterfaceWebApiUriTest(unittest.TestCase):
    ''' komlibs.interface.web.api.uri tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.uri_user'
        self.password = 'password'
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        self.passport = passport.get_user_passport(cookie)
        agentname='test_komlibs.interface.web.api.uri_agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
        agents_info=agentapi.get_agents_config_request(passport=self.passport)
        self.agents=agents_info.data
        aid = response.data['aid']
        cookie = {'user':self.username, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
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
        psp = passport.Passport(uid=uuid.uuid4())
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
            response=uriapi.get_uri_request(passport=psp, uri=uri)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_uri_request_failure_user_not_found(self):
        ''' get_uri_request should fail if user does not exist on system '''
        psp = passport.Passport(uid=uuid.uuid4())
        response=uriapi.get_uri_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.error, None)
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

    def test_get_uri_request_success_with_relative_uri(self):
        ''' get_uri_request should succeed and return requested uri and adjacent nodes '''
        psp = self.agent_passport
        uri='test_komlibs.interface.web.datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        uri='test_komlibs.interface.web.datasource..datasource..web..interface'
        response=uriapi.get_uri_request(passport=psp,uri=uri)
        self.assertEqual(response.status, status.WEB_STATUS_OK)

