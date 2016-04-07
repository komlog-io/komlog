import unittest
import time
import uuid
from komlog.komfig import logging
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.interface.websocket import api
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions, status
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation, message
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import response as modresp
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Message


class InterfaceWebSocketApiTest(unittest.TestCase):
    ''' komlibs.interface.websocket.api tests '''

    def test_process_message_failure_message_without_version_field(self):
        ''' process_message should fail if message has no version field '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        psp = Passport(uid,aid)
        msg={'action':1}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSA_PM_IVA)

    def test_process_message_failure_message_without_action_field(self):
        ''' process_message should fail if message has no action field '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        psp = Passport(uid,aid)
        msg={'v':1}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSA_PM_IVA)

    def test_process_message_failure_invalid_version(self):
        ''' process_message should fail if version is invalid '''
        versions=['\tadas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        psp = Passport(uid,aid)
        msg={'v':None,'action':'send_ds_data','payload':{'data':'data'}}
        for version in versions:
            msg['v']=version
            resp=api.process_message(passport=psp, message=msg)
            self.assertTrue(isinstance(resp, modresp.Response))
            self.assertEqual(resp.status, status.PROTOCOL_ERROR)
            self.assertEqual(resp.error, Errors.E_IWSA_PM_IVA)

    def test_process_message_failure_invalid_action(self):
        ''' process_message should fail if action is invalid '''
        actions=[None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        psp = Passport(uid,aid)
        msg={'v':1,'action':None,'payload':{'data':'data'}}
        for action in actions:
            msg['action']=action
            resp=api.process_message(passport=psp, message=msg)
            self.assertTrue(isinstance(resp, modresp.Response))
            self.assertEqual(resp.status, status.PROTOCOL_ERROR)
            self.assertEqual(resp.error, Errors.E_IWSA_PM_IVA)

    def test_process_message_failure_invalid_passport(self):
        ''' process_message should fail if passport is invalid '''
        passports=['\tadas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        msg={'v':1,'action':'send_ds_data','payload':{'data':'data'}}
        for psp in passports:
            resp=api.process_message(passport=psp, message=msg)
            self.assertTrue(isinstance(resp, modresp.Response))
            self.assertEqual(resp.status, status.INTERNAL_ERROR)
            self.assertEqual(resp.error, Errors.E_IWSA_PM_IPSP)

    def test_process_message_failure_invalid_message_payload(self):
        ''' process_message should fail if message payload is invalid '''
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        psp = Passport(uid,aid)
        msg={'v':1,'action':'send_ds_data','payload':{'data':'data'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_process_message_failure_unsupported_protocol_version(self):
        ''' process_message should fail if protocol version is not known '''
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        psp = Passport(uid,aid)
        msg={'v':100000000000,'action':'send_ds_data','payload':{'data':'data'}}
        resp=api.process_message(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSA_PM_UPV)

