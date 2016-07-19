import unittest
import time
import uuid
import json
import decimal
import pandas as pd
from komlog.komfig import logging
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import message
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Messages


class InterfaceWebSocketProtocolV1ModelMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.model.message tests '''

    def test_KomlogMessage_failure_direct_instantiation_not_allowed(self):
        ''' we cannot create a KomlogMessage object directly. we only are allowed to
            create one of its derived classes '''
        with self.assertRaises(TypeError) as cm:
            msg=message.KomlogMessage()
        self.assertEqual(str(cm.exception), '<KomlogMessage> cannot be instantiated directly')

    def test_SendDsData_version_cannot_be_modified(self):
        ''' if we create a new SendDsData message, the version param cannot be modified  '''
        msg=message.SendDsData()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.v=3
        self.assertEqual(str(cm.exception),'Version cannot be modified')

    def test_SendDsData_action_cannot_be_modified(self):
        ''' if we create a new SendDsData message, the action param cannot be modified  '''
        msg=message.SendDsData()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.action=3
        self.assertEqual(str(cm.exception),'Action cannot be modified')

    def test_SendDsData_with_no_params_does_not_have_attributes_and_cannot_serialize_to_dict(self):
        ''' if we create a new SendDsData message without params, it will has no attributes and
            to_dict function will fail '''
        msg=message.SendDsData()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertFalse(getattr(msg,'uri', False))
        self.assertFalse(getattr(msg,'ts', False))
        self.assertFalse(getattr(msg,'content', False))
        with self.assertRaises(AttributeError) as cm:
            msg.to_dict()

    def test_SendDsData_success_generating_serializable_dict(self):
        ''' SendDsData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDsData(uri='uri',ts=ts,content='content')
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_generating_serializable_dict_with_no_timezone_ts(self):
        ''' SendDsData.to_dict() method should generate a valid serializable dict '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts,tz='utc')
        msg=message.SendDsData(uri='uri',ts=ts,content='content')
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':ts2.isoformat(),'content':'content'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_loading_from_dict(self):
        ''' SendDsData.load_from_dict() method should generate a valid SendDsData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_loading_from_dict_with_no_timezone_ts(self):
        ''' SendDsData.load_from_dict() method should generate a valid SendDsData object '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts, tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':ts,'content':'content'}
        }
        msg=message.SendDsData.load_from_dict(dict_msg)
        dict_msg['payload']['ts']=ts2.isoformat()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.ts.timestamp(), ts2.timestamp())
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_failure_loading_from_dict_invalid_version(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':2,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_action(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_type(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':['uri','uri','ts',ts.isoformat(),'content','content']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'ari':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_ts_not_found(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','its':1,'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_content_not_found(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'contents':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'ñññinvalid uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_IURI)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_ts_invalid(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':'1','content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ITS)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_content_invalid(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':{'a':'dict'}}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ICNT)

    def test_SendDpData_with_no_params_does_not_have_attributes_and_cannot_serialize_to_dict(self):
        ''' if we create a new SendDpData message without params, it will has no attributes and
            to_dict function will fail '''
        msg=message.SendDpData()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertFalse(getattr(msg,'uri', False))
        self.assertFalse(getattr(msg,'ts', False))
        self.assertFalse(getattr(msg,'content', False))
        with self.assertRaises(AttributeError) as cm:
            msg.to_dict()

    def test_SendDpData_success_generating_serializable_dict(self):
        ''' SendDpData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDpData(uri='uri',ts=ts,content='33.33')
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_generating_serializable_dict_with_no_timezone_ts(self):
        ''' SendDpData.to_dict() method should generate a valid serializable dict '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts,tz='utc')
        msg=message.SendDpData(uri='uri',ts=ts,content='33.33')
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':ts2.isoformat(),'content':'33.33'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))


    def test_SendDpData_success_loading_from_dict(self):
        ''' SendDpData.load_from_dict() method should generate a valid SendDpData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_loading_from_dict_with_no_timezone_ts(self):
        ''' SendDpData.load_from_dict() method should generate a valid SendDpData object '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts,tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':ts,'content':'33.33'}
        }
        msg=message.SendDpData.load_from_dict(dict_msg)
        dict_msg['payload']['ts']=ts2.isoformat()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.ts.timestamp(), ts2.timestamp())
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_failure_loading_from_dict_invalid_version(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':2,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_action(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DS_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_type(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':['uri','uri','ts',ts.isoformat(),'content','33.33']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'ari':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_ts_not_found(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','its':1,'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_content_not_found(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'contents':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'ñññinvalid uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_IURI)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_ts_invalid(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':'1','content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ITS)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_content_invalid(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':{'a':'dict'}}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ICNT)

    def test_SendMultiData_with_no_params_does_not_have_attributes_and_cannot_serialize_to_dict(self):
        ''' if we create a new SendMultiData message without params, it will has no attributes and
            to_dict function will fail '''
        msg=message.SendMultiData()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertFalse(getattr(msg,'uris', False))
        self.assertFalse(getattr(msg,'ts', False))
        with self.assertRaises(AttributeError) as cm:
            msg.to_dict()

    def test_SendMultiData_success_generating_serializable_dict(self):
        ''' SendMultiData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendMultiData(uris=[{'uri':'uri','type':vertex.DATAPOINT,'content':decimal.Decimal('33.33')}],ts=ts)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.SEND_MULTI_DATA.value,'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_generating_serializable_dict_with_no_timezone_ts(self):
        ''' SendMultiData.to_dict() method should generate a valid serializable dict '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts, tz='utc')
        msg=message.SendMultiData(uris=[{'uri':'uri','type':vertex.DATAPOINT,'content':decimal.Decimal('33.33')}],ts=ts)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.SEND_MULTI_DATA.value,'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts2.isoformat()}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))


    def test_SendMultiData_success_loading_from_dict(self):
        ''' SendMultiData.load_from_dict() method should generate a valid SendMultiData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_loading_from_dict_with_no_timezone_ts(self):
        ''' SendMultiData.load_from_dict() method should generate a valid SendMultiData object '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts, tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts}
        }
        msg=message.SendMultiData.load_from_dict(dict_msg)
        dict_msg['payload']['ts']=ts2.isoformat()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.ts.timestamp(),ts2.timestamp())
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_failure_loading_from_dict_invalid_version(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':2,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_action(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_DP_DATA.value,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':['uri','uri','ts',ts.isoformat(),'content','33.33']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_not_found(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'aris':[{'uri':'uri','type':vertex.DATAPOINT, 'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_ts_not_found(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'its':1}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_invalid_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uris':{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'},'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_invalid_item_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uris':['string','other','trhee'],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_without_uri(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'},
                    {'content':'ds content'},
                ],
                'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_uri_invalid(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'},
                    {'uri':'Ñot valid','type':vertex.DATASOURCE,'content':'ds content'},
                ],
                'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_no_content(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT, 'content':'33.33'},
                    {'type':vertex.DATAPOINT, 'uri':'valid_uri'},
                ],
                'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_content_invalid(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'},
                    {'uri':'valid_uri','type':vertex.DATAPOINT,'content':'non dp content'},
                ],
                'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_no_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT, 'content':'33.33'},
                    {'uri':'valid_uri', 'content':'5'},
                ],
                'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_type_invalid(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'},
                    {'uri':'valid_uri','type':vertex.USER,'content':'content'},
                ],
                'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_ts_invalid(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'uris':[
                    {'uri':'uri','type':vertex.DATAPOINT, 'content':'33.33'},
                    {'uri':'valid_uri','type':vertex.DATASOURCE, 'content':'valid ds content'},
                ],
                'ts':'1'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ITS)

    def test_HookToUri_with_no_params_does_not_have_attributes_and_cannot_serialize_to_dict(self):
        ''' if we create a new HookToUri message without params, it will has no attributes and
            to_dict function will fail '''
        msg=message.HookToUri()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertFalse(getattr(msg,'uri', False))
        with self.assertRaises(AttributeError) as cm:
            msg.to_dict()

    def test_HookToUri_success_generating_serializable_dict(self):
        ''' HookToUri.to_dict() method should generate a valid serializable dict '''
        msg=message.HookToUri(uri='uri')
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_success_loading_from_dict(self):
        ''' HookToUri.load_from_dict() method should generate a valid HookToUri object '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.HOOK_TO_URI.value,
            'payload':{'uri':'uri'}
        }
        msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_failure_loading_from_dict_invalid_version(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':2,
            'action':Messages.HOOK_TO_URI.value,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_action(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_payload_type(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.HOOK_TO_URI.value,
            'payload':['uri','uri']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.HOOK_TO_URI.value,
            'payload':{'ari':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.HOOK_TO_URI.value,
            'payload':{'uri':['uri']}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_IURI)

    def test_UnHookFromUri_with_no_params_does_not_have_attributes_and_cannot_serialize_to_dict(self):
        ''' if we create a new UnHookFromUri message without params, it will has no attributes and
            to_dict function will fail '''
        msg=message.UnHookFromUri()
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertFalse(getattr(msg,'uri', False))
        with self.assertRaises(AttributeError) as cm:
            msg.to_dict()

    def test_UnHookFromUri_success_generating_serializable_dict(self):
        ''' UnHookFromUri.to_dict() method should generate a valid serializable dict '''
        msg=message.UnHookFromUri(uri='uri')
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(), {'v':message.VERSION,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_success_loading_from_dict(self):
        ''' UnHookFromUri.load_from_dict() method should generate a valid UnHookFromUri object '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.UNHOOK_FROM_URI.value,
            'payload':{'uri':'uri'}
        }
        msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.VERSION)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_failure_loading_from_dict_invalid_version(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':2,
            'action':Messages.UNHOOK_FROM_URI.value,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_action(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.HOOK_TO_URI.value,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_payload_type(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.UNHOOK_FROM_URI.value,
            'payload':['uri','uri']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.UNHOOK_FROM_URI.value,
            'payload':{'ari':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.VERSION,
            'action':Messages.UNHOOK_FROM_URI.value,
            'payload':{'uri':['uri']}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_IURI)

