import unittest
import time
import uuid
from komlog.komfig import logging
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.gestaccount import errors as gesterrors
from komlog.komlibs.interface.websocket.protocol.v1 import errors, exceptions, status, api
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation, message
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import response as modresp
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Message


class InterfaceWebSocketProtocolV1ApiTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.api tests '''

    def Notest_process_message_failure_non_existent_action(self):
        ''' process_message should fail if action is invalid '''
        action=999999999999
        psp = Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        msg={'action':action}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, errors.E_IWSPV1A_PM_IA)

    def Notest_process_message_failure_message_without_action_field(self):
        ''' process_message should fail if message has no action field '''
        psp = Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        msg={'v':1}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, errors.E_IWSPV1A_PM_IA)

    def Notest_process_message_failure_invalid_message_payload(self):
        ''' process_message should fail if message payload is invalid '''
        psp = Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'data':'data'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, errors.E_IWSPV1MM_SDDM_IPL)

    def test_process_message_failure_username_not_found(self):
        ''' process_message should fail if username is not found '''
        psp = Passport(uid=uuid.uuid4(), aid=uuid.uuid4())
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'content':'content', 'uri':'uri'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED) #E_ARA_ANDS_RE

