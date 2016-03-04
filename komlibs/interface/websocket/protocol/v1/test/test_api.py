import unittest
import time
import uuid
from komfig import logger
from komlibs.gestaccount import errors as gesterrors
from komlibs.interface.websocket.protocol.v1 import errors, exceptions, status, api
from komlibs.interface.websocket.protocol.v1.processing import operation, message
from komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlibs.interface.websocket.protocol.v1.model import response as modresp
from komlibs.interface.websocket.protocol.v1.model import operation as modop
from komlibs.interface.websocket.protocol.v1.model import types


class InterfaceWebSocketProtocolV1ApiTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.api tests '''

    def test_process_message_failure_non_existent_action(self):
        ''' process_message should fail if action is invalid '''
        action=999999999999
        username='username'
        aid=uuid.uuid4().hex
        msg={'action':action}
        resp=api.process_message(username=username, aid=aid, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, errors.E_IWSPV1A_PM_IA)

    def test_process_message_failure_message_without_action_field(self):
        ''' process_message should fail if message has no action field '''
        username='username'
        aid=uuid.uuid4().hex
        msg={'v':1}
        resp=api.process_message(username=username, aid=aid, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, errors.E_IWSPV1A_PM_IA)

    def test_process_message_failure_invalid_username(self):
        ''' process_message should fail if username is invalid '''
        usernames=['\tadas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        aid=uuid.uuid4().hex
        msg={'v':1,'action':types.MESSAGE_POST_DATASOURCE_DATA,'payload':{'data':'data'}}
        for username in usernames:
            resp=api.process_message(username=username, aid=aid, message=msg)
            self.assertTrue(isinstance(resp, modresp.Response))
            self.assertEqual(resp.status, status.PROTOCOL_ERROR)
            self.assertEqual(resp.error, errors.E_IWSPV1PM_PPDD_IU)

    def test_process_message_failure_invalid_hex_aid(self):
        ''' process_message should fail if aid is invalid '''
        aids=['\tadas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        username='username'
        msg={'v':1,'action':types.MESSAGE_POST_DATASOURCE_DATA,'payload':{'data':'data'}}
        for aid in aids:
            resp=api.process_message(username=username, aid=aid, message=msg)
            self.assertTrue(isinstance(resp, modresp.Response))
            self.assertEqual(resp.status, status.PROTOCOL_ERROR)
            self.assertEqual(resp.error, errors.E_IWSPV1PM_PPDD_IHAID)

    def test_process_message_failure_invalid_message_payload(self):
        ''' process_message should fail if message payload is invalid '''
        username='username'
        aid=uuid.uuid4().hex
        msg={'v':1,'action':types.MESSAGE_POST_DATASOURCE_DATA,'payload':{'data':'data'}}
        resp=api.process_message(username=username, aid=aid, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, errors.E_IWSPV1MM_PDDM_IPL)

    def test_process_message_failure_username_not_found(self):
        ''' process_message should fail if username is not found '''
        username='username'
        aid=uuid.uuid4().hex
        msg={'v':1,'action':types.MESSAGE_POST_DATASOURCE_DATA,'payload':{'ts':time.time(),'content':'content', 'uri':'uri'}}
        resp=api.process_message(username=username, aid=aid, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.error, gesterrors.E_GUA_GUID_UNF)

