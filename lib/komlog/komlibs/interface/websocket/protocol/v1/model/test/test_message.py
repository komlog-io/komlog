import unittest
import time
import uuid
import json
from komlog.komfig import logging
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import message
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Messages


class InterfaceWebSocketProtocolV1ModelMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.model.message tests '''

    def test_new_SendDsDataMessage_failure_invalid_type(self):
        ''' the creation of a SendDsDataMessage object should fail if message is not a dict '''
        messages=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        for msg in messages:
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg )
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IMT)

    def test_new_SendDsDataMessage_failure_version_not_found(self):
        ''' the creation of a SendDsDataMessage object should fail if version is not found '''
        msg={'action':Messages.SEND_DS_DATA.value,'payload':{'ts':time.time(),'content':'content','uri':'valid.uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IMT)

    def test_new_SendDsDataMessage_failure_action_not_found(self):
        ''' the creation of a SendDsDataMessage object should fail if action is not found '''
        msg={'v':1,'payload':{'ts':time.time(),'content':'content','uri':'valid.uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IMT)

    def test_new_SendDsDataMessage_failure_payload_not_found(self):
        ''' the creation of a SendDsDataMessage object should fail if payload is not found '''
        msg={'v':1,'action':Messages.SEND_DS_DATA.value}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IMT)

    def test_new_SendDsDataMessage_failure_invalid_version(self):
        ''' the creation of a SendDsDataMessage object should fail if version is not 1 '''
        versions=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':None,'action':Messages.SEND_DS_DATA.value,'payload':{}}
        for version in versions:
            msg['v']=version
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IV)

    def test_new_SendDsDataMessage_failure_invalid_action(self):
        ''' the creation of a SendDsDataMessage object should fail if action is not Messages.SEND_DS_DATA.value '''
        actions=['adas',None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':1,'action':None,'payload':{}}
        for action in actions:
            msg['action']=action
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IA)

    def test_new_SendDsDataMessage_failure_invalid_payload_no_uri(self):
        ''' the creation of a SendDsDataMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'ts':time.time(),'content':'content'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_no_ts(self):
        ''' the creation of a SendDsDataMessage object should fail if payload has no ts field '''
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'valid.uri','content':'content'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_no_content(self):
        ''' the creation of a SendDsDataMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDsDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_uri(self):
        ''' the creation of a SendDsDataMessage object should fail if payload uri is invalid '''
        uris=[None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf']
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':None,'content':'content'}}
        for uri in uris:
            msg['payload']['uri']=uri
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_ts(self):
        ''' the creation of a SendDsDataMessage object should fail if payload ts is invalid '''
        tss=[None,-2,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf',{'a':'dict'}]
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'ts':None,'uri':'uri','content':'content'}}
        for ts in tss:
            msg['payload']['ts']=ts
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IPL)

    def test_new_SendDsDataMessage_failure_invalid_payload_content(self):
        ''' the creation of a SendDsDataMessage object should fail if payload content is invalid '''
        contents=[None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),{'a':'dict'}]
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':'uri','content':None}}
        for content in contents:
            msg['payload']['content']=content
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDsDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSDM_IPL)

    def test_new_SendDsDataMessage_success(self):
        ''' the creation of a SendDsDataMessage object should succeed '''
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'ts':time.time(),'uri':'uri','content':'content'}}
        modmsg=message.SendDsDataMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.SendDsDataMessage))
        self.assertEqual(modmsg.payload,msg['payload'])
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.SEND_DS_DATA)

    def test_new_SendDpDataMessage_failure_invalid_type(self):
        ''' the creation of a SendDpDataMessage object should fail if message is not a dict '''
        messages=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        for msg in messages:
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDpDataMessage(message=msg )
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IMT)

    def test_new_SendDpDataMessage_failure_version_not_found(self):
        ''' the creation of a SendDpDataMessage object should fail if version is not found '''
        msg={'action':Messages.SEND_DP_DATA.value,'payload':{'ts':time.time(),'content':'content','uri':'valid.uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDpDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IMT)

    def test_new_SendDpDataMessage_failure_action_not_found(self):
        ''' the creation of a SendDpDataMessage object should fail if action is not found '''
        msg={'v':1,'payload':{'ts':time.time(),'content':'content','uri':'valid.uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDpDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IMT)

    def test_new_SendDpDataMessage_failure_payload_not_found(self):
        ''' the creation of a SendDpDataMessage object should fail if payload is not found '''
        msg={'v':1,'action':Messages.SEND_DP_DATA.value}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDpDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IMT)

    def test_new_SendDpDataMessage_failure_invalid_version(self):
        ''' the creation of a SendDpDataMessage object should fail if version is not 1 '''
        versions=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':None,'action':Messages.SEND_DP_DATA.value,'payload':{}}
        for version in versions:
            msg['v']=version
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDpDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IV)

    def test_new_SendDpDataMessage_failure_invalid_action(self):
        ''' the creation of a SendDpDataMessage object should fail if action is not Messages.SEND_DP_DATA.value '''
        actions=['adas',None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':1,'action':None,'payload':{}}
        for action in actions:
            msg['action']=action
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDpDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IA)

    def test_new_SendDpDataMessage_failure_invalid_payload_no_uri(self):
        ''' the creation of a SendDpDataMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'ts':time.time(),'content':'content'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDpDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IPL)

    def test_new_SendDpDataMessage_failure_invalid_payload_no_ts(self):
        ''' the creation of a SendDpDataMessage object should fail if payload has no ts field '''
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'valid.uri','content':'content'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDpDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IPL)

    def test_new_SendDpDataMessage_failure_invalid_payload_no_content(self):
        ''' the creation of a SendDpDataMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'ts':time.time(),'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendDpDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IPL)

    def test_new_SendDpDataMessage_failure_invalid_payload_uri(self):
        ''' the creation of a SendDpDataMessage object should fail if payload uri is invalid '''
        uris=[None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf']
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'ts':time.time(),'uri':None,'content':'content'}}
        for uri in uris:
            msg['payload']['uri']=uri
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDpDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IPL)

    def test_new_SendDpDataMessage_failure_invalid_payload_ts(self):
        ''' the creation of a SendDpDataMessage object should fail if payload ts is invalid '''
        tss=[None,-2,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf',{'a':'dict'}]
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'ts':None,'uri':'uri','content':'content'}}
        for ts in tss:
            msg['payload']['ts']=ts
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDpDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IPL)

    def test_new_SendDpDataMessage_failure_invalid_payload_content(self):
        ''' the creation of a SendDpDataMessage object should fail if payload content is invalid '''
        contents=[None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),{'a':'dict'}]
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'ts':time.time(),'uri':'uri','content':None}}
        for content in contents:
            msg['payload']['content']=content
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendDpDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPDM_IPL)

    def test_new_SendDpDataMessage_success(self):
        ''' the creation of a SendDpDataMessage object should succeed '''
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'ts':time.time(),'uri':'uri','content':'content'}}
        modmsg=message.SendDpDataMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.SendDpDataMessage))
        self.assertEqual(modmsg.payload,msg['payload'])
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.SEND_DP_DATA)

    def test_new_SendMultiDataMessage_failure_invalid_type(self):
        ''' the creation of a SendMultiDataMessage object should fail if message is not a dict '''
        messages=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        for msg in messages:
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendMultiDataMessage(message=msg )
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IMT)

    def test_new_SendMultiDataMessage_failure_version_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if version is not found '''
        msg={'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time(),'uris':[]}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IMT)

    def test_new_SendMultiDataMessage_failure_action_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if action is not found '''
        msg={'v':1,'payload':{'ts':time.time(),'uris':[]}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IMT)

    def test_new_SendMultiDataMessage_failure_payload_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if payload is not found '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IMT)

    def test_new_SendMultiDataMessage_failure_invalid_version(self):
        ''' the creation of a SendMultiDataMessage object should fail if version is not 1 '''
        versions=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':None,'action':Messages.SEND_MULTI_DATA.value,'payload':{}}
        for version in versions:
            msg['v']=version
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendMultiDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IV)

    def test_new_SendMultiDataMessage_failure_invalid_action(self):
        ''' the creation of a SendMultiDataMessage object should fail if action is not Messages.SEND_MULTI_DATA.value '''
        actions=['adas',None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),Messages.SEND_DP_DATA.value, Messages.SEND_DS_DATA.value]
        msg={'v':1,'action':None,'payload':{}}
        for action in actions:
            msg['action']=action
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendMultiDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IA)

    def test_new_SendMultiDataMessage_failure_invalid_payload_no_ts(self):
        ''' the creation of a SendMultiDataMessage object should fail if payload has no ts field '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'uris':[{'uri':'uri','content':'content'}]}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_ts(self):
        ''' the creation of a SendMultiDataMessage object should fail if payload ts is invalid '''
        tss=[None,-2,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),'asd...asdf',{'a':'dict'}]
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':None,'uris':[{'uri':'a.uri','content':'content'}]}}
        for ts in tss:
            msg['payload']['ts']=ts
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendMultiDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_no_uris(self):
        '''the creation of a SendMultiDataMessage object should fail if payload has no uris field'''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_invalid_uris_type(self):
        '''the creation of a SendMultiDataMessage object should fail if payload uris is not list'''
        uris=[None,-2,1.1,{'set','a'},('a','tuple'),uuid.uuid4(),{'a':'dict'}]
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        for uri in uris:
            msg['payload']['uris']=uri
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.SendMultiDataMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_uris_length_0(self):
        ''' the creation of a SendMultiDataMessage object should fail if payload has no uris '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_item_uri_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if a payload item has no uri'''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'uri':'a.valid.uri','content':'content'},{'content':'content'}]
        msg['payload']['uris']=uris
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_items_uri_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if all payload items have no uri'''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'content':'content'},{'content':'content'}]
        msg['payload']['uris']=uris
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_item_uri_is_invalid(self):
        ''' the creation of a SendMultiDataMessage object should fail if a payload item uri is invalid'''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'uri':'in valid.uri','content':'content'},{'uri':'valid.uri','content':'content'}]
        msg['payload']['uris']=uris
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_item_content_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if a payload item has no content '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'uri':'a.valid.uri','content':'content'},{'uri':'another.uri'}]
        msg['payload']['uris']=uris
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_items_content_not_found(self):
        ''' the creation of a SendMultiDataMessage object should fail if all payload items have no content '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'uri':'a.valid.uri'},{'uri':'another.uri'}]
        msg['payload']['uris']=uris
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_failure_invalid_payload_item_content_is_invalid(self):
        ''' the creation of a SendMultiDataMessage object should fail if a payload item content is invalid'''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'uri':'valid.uri','content':'content'},{'uri':'valid.uri','content':4}]
        msg['payload']['uris']=uris
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.SendMultiDataMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTDM_IPL)

    def test_new_SendMultiDataMessage_success(self):
        ''' the creation of a SendMultiDataMessage object should succeed '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        uris=[{'uri':'valid.uri','content':'33232.2323'},{'uri':'valid.uri','content':'content'}]
        msg['payload']['uris']=uris
        modmsg=message.SendMultiDataMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.SendMultiDataMessage))
        self.assertEqual(modmsg.payload,msg['payload'])
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.SEND_MULTI_DATA)

    def test_new_SendMultiDataMessage_success_extra_fields_are_not_loaded(self):
        ''' the creation of a SendMultiDataMessage object should succeed and any extra (not valid) field received is not propagated '''
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':time.time()}}
        valid_uris=[{'uri':'valid.uri','content':'33232.2323'},{'uri':'valid.uri','content':'content'}]
        extra_uris=[{'uri':'valid.uri','content':'33232.2323','extra':'something'},{'uri':'valid.uri','content':'content','wtf':['something','we','dont','expect']}]
        msg['payload']['uris']=extra_uris
        modmsg=message.SendMultiDataMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.SendMultiDataMessage))
        self.assertEqual(modmsg.payload['ts'],msg['payload']['ts'])
        self.assertEqual(modmsg.payload['uris'],valid_uris)
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.SEND_MULTI_DATA)

    def test_new_HookToUriMessage_failure_invalid_type(self):
        ''' the creation of a HookToUriMessage object should fail if message is not a dict '''
        messages=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        for msg in messages:
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.HookToUriMessage(message=msg )
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IMT)

    def test_new_HookToUriMessage_failure_version_not_found(self):
        ''' the creation of a HookToUriMessage object should fail if version is not found '''
        msg={'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.HookToUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IMT)

    def test_new_HookToUriMessage_failure_action_not_found(self):
        ''' the creation of a HookToUriMessage object should fail if action is not found '''
        msg={'v':1,'payload':{'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.HookToUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IMT)

    def test_new_HookToUriMessage_failure_payload_not_found(self):
        ''' the creation of a HookToUriMessage object should fail if payload is not found '''
        msg={'v':1,'action':Messages.HOOK_TO_URI.value}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.HookToUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IMT)

    def test_new_HookToUriMessage_failure_invalid_version(self):
        ''' the creation of a HookToUriMessage object should fail if version is not 1 '''
        versions=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':None,'action':Messages.HOOK_TO_URI.value,'payload':{}}
        for version in versions:
            msg['v']=version
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.HookToUriMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IV)

    def test_new_HookToUriMessage_failure_invalid_action(self):
        ''' the creation of a HookToUriMessage object should fail if action is not Messages.HOOK_TO_URI.value '''
        actions=['adas',None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),Messages.SEND_DP_DATA.value, Messages.SEND_DS_DATA.value]
        msg={'v':1,'action':None,'payload':{}}
        for action in actions:
            msg['action']=action
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.HookToUriMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IA)

    def test_new_HookToUriMessage_failure_invalid_payload_no_uri(self):
        ''' the creation of a HookToUriMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uris':[{'uri':'uri','content':'content'}]}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.HookToUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IPL)

    def test_new_HookToUriMessage_failure_invalid_payload_invalid_uri_type(self):
        '''the creation of a HookToUriMessage object should fail if payload uri is not valid '''
        uris=[None,-2,1.1,{'set','a'},('a','tuple'),uuid.uuid4(),{'a':'dict'},'In valid Uri','']
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':None}}
        for uri in uris:
            msg['payload']['uri']=uri
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.HookToUriMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTUM_IPL)

    def test_new_HookToUriMessage_success(self):
        ''' the creation of a HookToUriMessage object should succeed '''
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri'}}
        modmsg=message.HookToUriMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.HookToUriMessage))
        self.assertEqual(modmsg.payload,msg['payload'])
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.HOOK_TO_URI)

    def test_new_HookToUriMessage_success_extra_fields_are_not_loaded(self):
        ''' the creation of a HookToUriMessage object should succeed and any extra (not valid) field received in payload is not propagated '''
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{}}
        valid_payload={'uri':'valid.uri'}
        extra_payload={'uri':'valid.uri','content':'33232.2323'}
        msg['payload']=extra_payload
        modmsg=message.HookToUriMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.HookToUriMessage))
        self.assertEqual(modmsg.payload,valid_payload)
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.HOOK_TO_URI)

    def test_new_UnHookFromUriMessage_failure_invalid_type(self):
        ''' the creation of a UnHookFromUriMessage object should fail if message is not a dict '''
        messages=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        for msg in messages:
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.UnHookFromUriMessage(message=msg )
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IMT)

    def test_new_UnHookFromUriMessage_failure_version_not_found(self):
        ''' the creation of a UnHookFromUriMessage object should fail if version is not found '''
        msg={'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.UnHookFromUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IMT)

    def test_new_UnHookFromUriMessage_failure_action_not_found(self):
        ''' the creation of a UnHookFromUriMessage object should fail if action is not found '''
        msg={'v':1,'payload':{'uri':'uri'}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.UnHookFromUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IMT)

    def test_new_UnHookFromUriMessage_failure_payload_not_found(self):
        ''' the creation of a UnHookFromUriMessage object should fail if payload is not found '''
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.UnHookFromUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IMT)

    def test_new_UnHookFromUriMessage_failure_invalid_version(self):
        ''' the creation of a UnHookFromUriMessage object should fail if version is not 1 '''
        versions=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4()]
        msg={'v':None,'action':Messages.UNHOOK_FROM_URI.value,'payload':{}}
        for version in versions:
            msg['v']=version
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.UnHookFromUriMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IV)

    def test_new_UnHookFromUriMessage_failure_invalid_action(self):
        ''' the creation of a UnHookFromUriMessage object should fail if action is not Messages.UNHOOK_FROM_URI.value '''
        actions=['adas',None,-2,1.1,1000000,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid4(),Messages.SEND_DP_DATA.value, Messages.SEND_DS_DATA.value]
        msg={'v':1,'action':None,'payload':{}}
        for action in actions:
            msg['action']=action
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.UnHookFromUriMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IA)

    def test_new_UnHookFromUriMessage_failure_invalid_payload_no_uri(self):
        ''' the creation of a UnHookFromUriMessage object should fail if payload has no uri field '''
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uris':[{'uri':'uri','content':'content'}]}}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message.UnHookFromUriMessage(message=msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IPL)

    def test_new_UnHookFromUriMessage_failure_invalid_payload_invalid_uri_type(self):
        '''the creation of a UnHookFromUriMessage object should fail if payload uri is not valid '''
        uris=[None,-2,1.1,{'set','a'},('a','tuple'),uuid.uuid4(),{'a':'dict'},'In valid Uri','']
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':None}}
        for uri in uris:
            msg['payload']['uri']=uri
            with self.assertRaises(exceptions.MessageValidationException) as cm:
                message.UnHookFromUriMessage(message=msg)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFUM_IPL)

    def test_new_UnHookFromUriMessage_success(self):
        ''' the creation of a UnHookFromUriMessage object should succeed '''
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri'}}
        modmsg=message.UnHookFromUriMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.UnHookFromUriMessage))
        self.assertEqual(modmsg.payload,msg['payload'])
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.UNHOOK_FROM_URI)

    def test_new_UnHookFromUriMessage_success_extra_fields_are_not_loaded(self):
        ''' the creation of a UnHookFromUriMessage object should succeed and any extra (not valid) field received in payload is not propagated '''
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{}}
        valid_payload={'uri':'valid.uri'}
        extra_payload={'uri':'valid.uri','content':'33232.2323'}
        msg['payload']=extra_payload
        modmsg=message.UnHookFromUriMessage(message=msg)
        self.assertTrue(isinstance(modmsg,message.UnHookFromUriMessage))
        self.assertEqual(modmsg.payload,valid_payload)
        self.assertEqual(modmsg.v,msg['v'])
        self.assertEqual(modmsg.action,Messages.UNHOOK_FROM_URI)

