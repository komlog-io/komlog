import unittest
import time
import uuid
import json
from komlog.komfig import logging
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import message
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Message


class InterfaceWebSocketProtocolV1ModelMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.model.message tests '''

    def test_new_SendDsDataMessage_failure_invalid_type(self):
        ''' the creation of a SendDsDataMessage object should fail if message is not a dict '''
        messages=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        for msg in messages:
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg )
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IMT)

    def test_new_SendDsDataMessage_failure_version_not_found(self):
        ''' the creation of a SendDsDataMessage object should fail if version is not found '''
        msg={'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'content':'content','uri':'valid.uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IMT)

    def test_new_SendDsDataMessage_failure_action_not_found(self):
        ''' the creation of a SendDsDataMessage object should fail if action is not found '''
        msg={'v':1,'payload':{'ts':time.time(),'content':'content','uri':'valid.uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IMT)

    def test_new_SendDsDataMessage_failure_payload_not_found(self):
        ''' the creation of a SendDsDataMessage object should fail if payload is not found '''
        msg={'v':1,'action':Message.SEND_DS_DATA.value}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IMT)

    def test_new_SendDsDataMessage_failure_invalid_version(self):
        ''' the creation of a SendDsDataMessage object should fail if version is not 1 '''
        versions=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':None,'action':Message.SEND_DS_DATA.value,'payload':{}}
        for version in versions:
            msg['v']=version
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IV)

    def test_new_SendDsDataMessage_failure_invalid_action(self):
        ''' the creation of a SendDsDataMessage object should fail if action is not Message.SEND_DS_DATA.value '''
        actions=['adas',None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':1,'action':None,'payload':{}}
        for action in actions:
            msg['action']=action
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IA)

    def test_new_SendDsDataMessage_failure_invalid_payload_no_uri(self):
        ''' the creation of a SendDsDataMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'content':'content'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_no_ts(self):
        ''' the creation of a SendDsDataMessage object should fail if payload has no ts field '''
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'uri':'valid.uri','content':'content'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_no_content(self):
        ''' the creation of a SendDsDataMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_uri(self):
        ''' the creation of a SendDsDataMessage object should fail if payload uri is invalid '''
        uris=[None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf']
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':None,'content':'content'}}
        for uri in uris:
            msg['payload']['uri']=uri
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_ts(self):
        ''' the creation of a SendDsDataMessage object should fail if payload ts is invalid '''
        tss=[None,-2,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf',{'a':'dict'}]
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':None,'uri':'uri','content':'content'}}
        for ts in tss:
            msg['payload']['ts']=ts
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_content(self):
        ''' the creation of a SendDsDataMessage object should fail if payload content is invalid '''
        contents=[None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),{'a':'dict'}]
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':'uri','content':None}}
        for content in contents:
            msg['payload']['content']=content
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDDM_IPL)

    def test_new_SendDsDataMessage_success(self):
        ''' the creation of a SendDsDataMessage object should succeed '''
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':'uri','content':'content'}}
        modmsg=message.SendDsDataMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.SendDsDataMessage))
        self.assertEqual(modmsg.payload,msg['payload'])
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,msg['action'])

