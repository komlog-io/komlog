import unittest
import time
import uuid
import pandas as pd
from komlog.komfig import logging
from komlog.komlibs.auth.passport import AgentPassport
from komlog.komlibs.interface.websocket import exceptions, status
from komlog.komlibs.interface.websocket.model import response
from komlog.komlibs.interface.websocket.model.types import Messages
from komlog.komlibs.interface.websocket.protocol.v1 import api
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation, message
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop


class InterfaceWebSocketProtocolV1ApiTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.api tests '''

    def test_process_message_failure_non_existent_action(self):
        ''' process_message should fail if action is invalid '''
        action=999999999999
        psp = AgentPassport(uid=uuid.uuid4(), aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'action':action, 'v':1, 'seq':uuid.uuid1().hex[0:20]}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1A_PM_IA)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(resp.ws_messages[0].action,Messages.GENERIC_RESPONSE)
        self.assertTrue(resp.ws_messages[0].status,status.PROTOCOL_ERROR)
        self.assertTrue(resp.ws_messages[0].error,Errors.E_IWSPV1A_PM_IA)
        self.assertTrue(resp.ws_messages[0].v,1)
        self.assertTrue(resp.ws_messages[0].irt,msg['seq'])

    def test_process_message_failure_invalid_message_payload_SEND_DS_DATA_message(self):
        ''' process_message should fail if message payload is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(), aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'seq':uuid.uuid1().hex[0:20], 'irt':None, 'action':Messages.SEND_DS_DATA.value,'payload':{'data':'data'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDSD_ELFD)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(resp.ws_messages[0].action,Messages.GENERIC_RESPONSE)
        self.assertTrue(resp.ws_messages[0].status,status.PROTOCOL_ERROR)
        self.assertTrue(resp.ws_messages[0].error,Errors.E_IWSPV1MM_SDSD_ELFD)
        self.assertTrue(resp.ws_messages[0].v,1)
        self.assertTrue(resp.ws_messages[0].irt,msg['seq'])

    def test_process_message_failure_invalid_message_payload_SEND_DP_DATA_message(self):
        ''' process_message should fail if message payload is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(), aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'seq':uuid.uuid1().hex[0:20], 'irt':None, 'action':Messages.SEND_DP_DATA.value,'payload':{'data':'data'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ELFD)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(resp.ws_messages[0].action,Messages.GENERIC_RESPONSE)
        self.assertTrue(resp.ws_messages[0].status,status.PROTOCOL_ERROR)
        self.assertTrue(resp.ws_messages[0].error,Errors.E_IWSPV1MM_SDPD_ELFD)
        self.assertTrue(resp.ws_messages[0].v,1)
        self.assertTrue(resp.ws_messages[0].irt,msg['seq'])

    def test_process_message_failure_invalid_message_payload_SEND_MULTI_DATA_message(self):
        ''' process_message should fail if message payload is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(), aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'seq':uuid.uuid1().hex[0:20], 'irt':None, 'action':Messages.SEND_MULTI_DATA.value,'payload':{'data':'data'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SMTD_ELFD)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(resp.ws_messages[0].action,Messages.GENERIC_RESPONSE)
        self.assertTrue(resp.ws_messages[0].status,status.PROTOCOL_ERROR)
        self.assertTrue(resp.ws_messages[0].error,Errors.E_IWSPV1MM_SMTD_ELFD)
        self.assertTrue(resp.ws_messages[0].v,1)
        self.assertTrue(resp.ws_messages[0].irt,msg['seq'])

    def test_process_message_failure_username_not_found(self):
        ''' process_message should fail if username is not found '''
        psp = AgentPassport(uid=uuid.uuid4(), aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'seq':uuid.uuid1().hex[0:20], 'irt':None, 'action':Messages.SEND_DS_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content', 'uri':'uri'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED) #E_ARA_ANDS_RE
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(resp.ws_messages[0].action,Messages.GENERIC_RESPONSE)
        self.assertTrue(resp.ws_messages[0].status,status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(resp.ws_messages[0].v,1)
        self.assertTrue(resp.ws_messages[0].irt,msg['seq'])

