import unittest
import time
import uuid
import json
import decimal
import pandas as pd
from komlog.komfig import logging
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.model.types import Messages
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import message


class InterfaceWebSocketProtocolV1ModelMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.model.message tests '''

    def test_MessagesVersionCatalog_failure_direct_instantiation_not_allowed(self):
        ''' we cannot create a MessagesVersionCatalog object directly. we only are allowed to
            create one of its derived classes '''
        with self.assertRaises(TypeError) as cm:
            msg=message.MessagesVersionCatalog()
        self.assertEqual(str(cm.exception), '<MessagesVersionCatalog> cannot be instantiated directly')

    def test_GenericResponse_version_cannot_be_modified(self):
        ''' if we create a new GenericResponse message, the version param cannot be modified  '''
        msg=message.GenericResponse(status=1,irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.GENERIC_RESPONSE)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.v=3
        self.assertEqual(str(cm.exception),'Version cannot be modified')

    def test_GenericResponse_action_cannot_be_modified(self):
        ''' if we create a new GenericResponse message, the action param cannot be modified  '''
        msg=message.GenericResponse(status=1,irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.GENERIC_RESPONSE)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.action=3
        self.assertEqual(str(cm.exception),'Action cannot be modified')

    def test_GenericResponse_seq_cannot_be_modified(self):
        ''' if we create a new GenericResponse message, the version param cannot be modified  '''
        msg=message.GenericResponse(status=1,irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.GENERIC_RESPONSE)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.seq=3
        self.assertEqual(str(cm.exception),'Sequence cannot be modified')

    def test_GenericResponse_success_generating_serializable_dict_with_irt(self):
        ''' GenericResponse.to_dict() method should generate a valid serializable dict '''
        msg=message.GenericResponse(status=1,irt=uuid.uuid1().hex[0:20])
        self.assertIsNotNone(msg.irt)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.GENERIC_RESPONSE)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.GENERIC_RESPONSE.value,'irt':msg.irt, 'seq':msg.seq, 'payload':{'status':1,'error':Errors.OK.value,'reason':None}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_version_cannot_be_modified(self):
        ''' if we create a new SendDsData message, the version param cannot be modified  '''
        msg=message.SendDsData(uri='uri',ts=pd.Timestamp('now',tz='utc'),content='ds_content')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.v=3
        self.assertEqual(str(cm.exception),'Version cannot be modified')

    def test_SendDsData_action_cannot_be_modified(self):
        ''' if we create a new SendDsData message, the action param cannot be modified  '''
        msg=message.SendDsData(uri='uri',ts=pd.Timestamp('now',tz='utc'),content='ds_content')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.action=3
        self.assertEqual(str(cm.exception),'Action cannot be modified')

    def test_SendDsData_seq_cannot_be_modified(self):
        ''' if we create a new SendDsData message, the seq param cannot be modified  '''
        msg=message.SendDsData(uri='uri',ts=pd.Timestamp('now',tz='utc'),content='ds_content')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertTrue(args.is_valid_message_sequence(msg.seq))
        self.assertEqual(msg.irt, None)
        self.assertFalse(getattr(msg,'payload', False))
        with self.assertRaises(TypeError) as cm:
            msg.seq=uuid.uuid1().hex[0:20]
        self.assertEqual(str(cm.exception),'Sequence cannot be modified')

    def test_SendDsData_success_generating_serializable_dict(self):
        ''' SendDsData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDsData(uri='uri',ts=ts,content='content')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DS_DATA.value,'irt':None, 'seq':msg.seq, 'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_generating_serializable_dict_with_no_timezone_ts(self):
        ''' SendDsData.to_dict() method should generate a valid serializable dict '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts,tz='utc')
        msg=message.SendDsData(uri='uri',ts=ts,content='content')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DS_DATA.value,'irt':None, 'seq':msg.seq, 'payload':{'uri':'uri','ts':ts2.isoformat(),'content':'content'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_generating_serializable_dict_with_global_uri(self):
        ''' SendDsData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDsData(uri='user:uri',ts=ts,content='content')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DS_DATA.value,'irt':None, 'seq':msg.seq, 'payload':{'uri':'user:uri','ts':ts.isoformat(),'content':'content'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_generating_serializable_dict_with_irt(self):
        ''' SendDsData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDsData(uri='user:uri',ts=ts,content='content', irt=uuid.uuid1().hex[0:20])
        self.assertIsNotNone(msg.irt)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DS_DATA.value,'irt':msg.irt, 'seq':msg.seq, 'payload':{'uri':'user:uri','ts':ts.isoformat(),'content':'content'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_loading_from_dict(self):
        ''' SendDsData.load_from_dict() method should generate a valid SendDsData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_loading_from_dict_with_no_timezone_ts(self):
        ''' SendDsData.load_from_dict() method should generate a valid SendDsData object '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts, tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts,'content':'content'}
        }
        msg=message.SendDsData.load_from_dict(dict_msg)
        dict_msg['payload']['ts']=ts2.isoformat()
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.ts.timestamp(), ts2.timestamp())
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_loading_from_dict_with_global_uri(self):
        ''' SendDsData.load_from_dict() method should generate a valid SendDsData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'my_user:uri','ts':ts.isoformat(),'content':'content'}
        }
        msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_success_loading_from_dict_with_non_none_irt(self):
        ''' SendDsData.load_from_dict() method should generate a valid SendDsData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{'uri':'my_user:uri','ts':ts.isoformat(),'content':'content'}
        }
        msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DS_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDsData_failure_loading_from_dict_invalid_version(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':2,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_action(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_non_seq(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_seq(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:10],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_SendDsData_failure_loading_from_dict_non_irt(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'eirt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_irt(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':'invalidirt',
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_type(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':['uri','uri','ts',ts.isoformat(),'content','content']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'ari':'uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_ts_not_found(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','its':1,'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_content_not_found(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'contents':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ELFD)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'ñññinvalid uri','ts':ts.isoformat(),'content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_IURI)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_ts_invalid(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':'1','content':'content'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ITS)

    def test_SendDsData_failure_loading_from_dict_invalid_payload_content_invalid(self):
        ''' SendDsData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':{'a':'dict'}}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDsData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDSD_ICNT)

    def test_SendDpData_success_generating_serializable_dict(self):
        ''' SendDpData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDpData(uri='uri',ts=ts,content='33.33')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DP_DATA.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_generating_serializable_dict_with_no_timezone_ts(self):
        ''' SendDpData.to_dict() method should generate a valid serializable dict '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts,tz='utc')
        msg=message.SendDpData(uri='uri',ts=ts,content='33.33')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DP_DATA.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'uri','ts':ts2.isoformat(),'content':'33.33'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_generating_serializable_dict_with_global_uri(self):
        ''' SendDpData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDpData(uri='user:uri',ts=ts,content='33.33')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DP_DATA.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'user:uri','ts':ts.isoformat(),'content':'33.33'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_generating_serializable_dict_with_irt(self):
        ''' SendDpData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendDpData(uri='user:uri',ts=ts,content='33.33', irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_DP_DATA.value,'seq':msg.seq, 'irt':msg.irt, 'payload':{'uri':'user:uri','ts':ts.isoformat(),'content':'33.33'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_loading_from_dict(self):
        ''' SendDpData.load_from_dict() method should generate a valid SendDpData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_loading_from_dict_with_no_timezone_ts(self):
        ''' SendDpData.load_from_dict() method should generate a valid SendDpData object '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts,tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts,'content':'33.33'}
        }
        msg=message.SendDpData.load_from_dict(dict_msg)
        dict_msg['payload']['ts']=ts2.isoformat()
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.ts.timestamp(), ts2.timestamp())
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_loading_from_dict_with_global_uri(self):
        ''' SendDpData.load_from_dict() method should generate a valid SendDpData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'the_user:uri','ts':ts.isoformat(),'content':'33.33'}
        }
        msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_success_loading_from_dict_with_irt(self):
        ''' SendDpData.load_from_dict() method should generate a valid SendDpData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{'uri':'the_user:uri','ts':ts.isoformat(),'content':'33.33'}
        }
        msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DP_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendDpData_failure_loading_from_dict_invalid_version(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':2,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_action(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_non_seq(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_seq(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:19],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_SendDpData_failure_loading_from_dict_non_irt(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'iirt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_irt(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':23,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_type(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':['uri','uri','ts',ts.isoformat(),'content','33.33']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'ari':'uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_ts_not_found(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','its':1,'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_content_not_found(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'contents':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ELFD)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'ñññinvalid uri','ts':ts.isoformat(),'content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_IURI)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_ts_invalid(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':'1','content':'33.33'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ITS)

    def test_SendDpData_failure_loading_from_dict_invalid_payload_content_invalid(self):
        ''' SendDpData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri','ts':ts.isoformat(),'content':{'a':'dict'}}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDpData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDPD_ICNT)

    def test_SendMultiData_success_generating_serializable_dict(self):
        ''' SendMultiData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendMultiData(uris=[{'uri':'uri','type':vertex.DATAPOINT,'content':decimal.Decimal('33.33')}],ts=ts)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_MULTI_DATA.value,'seq':msg.seq, 'irt':None, 'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_generating_serializable_dict_with_no_timezone_ts(self):
        ''' SendMultiData.to_dict() method should generate a valid serializable dict '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts, tz='utc')
        msg=message.SendMultiData(uris=[{'uri':'uri','type':vertex.DATAPOINT,'content':decimal.Decimal('33.33')}],ts=ts)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_MULTI_DATA.value,'seq':msg.seq, 'irt':None, 'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts2.isoformat()}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_generating_serializable_dict_with_global_uri(self):
        ''' SendMultiData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendMultiData(uris=[{'uri':'user1:uri','type':vertex.DATAPOINT,'content':decimal.Decimal('33.33')}],ts=ts)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_MULTI_DATA.value,'seq':msg.seq, 'irt':None, 'payload':{'uris':[{'uri':'user1:uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_generating_serializable_dict_with_irt(self):
        ''' SendMultiData.to_dict() method should generate a valid serializable dict '''
        ts=pd.Timestamp('now',tz='utc')
        msg=message.SendMultiData(uris=[{'uri':'user1:uri','type':vertex.DATAPOINT,'content':decimal.Decimal('33.33')}],ts=ts, irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.SEND_MULTI_DATA.value,'seq':msg.seq, 'irt':msg.irt, 'payload':{'uris':[{'uri':'user1:uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_loading_from_dict(self):
        ''' SendMultiData.load_from_dict() method should generate a valid SendMultiData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_loading_from_dict_with_no_timezone_ts(self):
        ''' SendMultiData.load_from_dict() method should generate a valid SendMultiData object '''
        ts='2016-07-18T17:15:00'
        ts2=pd.Timestamp(ts, tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts}
        }
        msg=message.SendMultiData.load_from_dict(dict_msg)
        dict_msg['payload']['ts']=ts2.isoformat()
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.ts.timestamp(),ts2.timestamp())
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_loading_from_dict_with_global_uri(self):
        ''' SendMultiData.load_from_dict() method should generate a valid SendMultiData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'user2:uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_success_loading_from_dict_with_irt(self):
        ''' SendMultiData.load_from_dict() method should generate a valid SendMultiData object '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{'uris':[{'uri':'user2:uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_MULTI_DATA)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_SendMultiData_failure_loading_from_dict_invalid_version(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':2,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_action(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DP_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_non_seq(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_seq(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':10,
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_SendMultiData_failure_loading_from_dict_non_irt(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'iirt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_irt(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':332,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':['uri','uri','ts',ts.isoformat(),'content','33.33']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_not_found(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'aris':[{'uri':'uri','type':vertex.DATAPOINT, 'content':'33.33'}],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_ts_not_found(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'}],'its':1}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_ELFD)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_invalid_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':{'uri':'uri','type':vertex.DATAPOINT,'content':'33.33'},'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_invalid_item_type(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uris':['string','other','trhee'],'ts':ts.isoformat()}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendMultiData.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SMTD_IURIS)

    def test_SendMultiData_failure_loading_from_dict_invalid_payload_uris_item_without_uri(self):
        ''' SendMultiData.load_from_dict() method should fail is passed argument is invalid '''
        ts=pd.Timestamp('now',tz='utc')
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
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

    def test_HookToUri_success_generating_serializable_dict(self):
        ''' HookToUri.to_dict() method should generate a valid serializable dict '''
        msg=message.HookToUri(uri='uri')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.HOOK_TO_URI.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_success_generating_serializable_dict_with_global_uri(self):
        ''' HookToUri.to_dict() method should generate a valid serializable dict '''
        msg=message.HookToUri(uri='user1:uri')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.HOOK_TO_URI.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'user1:uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_success_generating_serializable_dict_with_irt(self):
        ''' HookToUri.to_dict() method should generate a valid serializable dict '''
        msg=message.HookToUri(uri='user1:uri', irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.HOOK_TO_URI.value,'seq':msg.seq, 'irt':msg.irt, 'payload':{'uri':'user1:uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_success_loading_from_dict(self):
        ''' HookToUri.load_from_dict() method should generate a valid HookToUri object '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_success_loading_from_dict_with_global_uri(self):
        ''' HookToUri.load_from_dict() method should generate a valid HookToUri object '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'the_user:uri'}
        }
        msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_success_loading_from_dict_with_irt(self):
        ''' HookToUri.load_from_dict() method should generate a valid HookToUri object '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{'uri':'the_user:uri'}
        }
        msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.HOOK_TO_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_HookToUri_failure_loading_from_dict_invalid_version(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':2,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_action(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_non_seq(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.HOOK_TO_URI.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_seq(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:10],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_HookToUri_failure_loading_from_dict_non_irt(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'iirt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_irt(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':'hi',
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_HookToUri_failure_loading_from_dict_invalid_payload_type(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':['uri','uri']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'ari':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_ELFD)

    def test_HookToUri_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' HookToUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':['uri']}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.HookToUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_HTU_IURI)

    def test_UnHookFromUri_success_generating_serializable_dict(self):
        ''' UnHookFromUri.to_dict() method should generate a valid serializable dict '''
        msg=message.UnHookFromUri(uri='uri')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.UNHOOK_FROM_URI.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_success_generating_serializable_dict_with_global_uri(self):
        ''' UnHookFromUri.to_dict() method should generate a valid serializable dict '''
        msg=message.UnHookFromUri(uri='my_superuser:uri')
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.UNHOOK_FROM_URI.value,'seq':msg.seq, 'irt':None, 'payload':{'uri':'my_superuser:uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_success_generating_serializable_dict_with_irt(self):
        ''' UnHookFromUri.to_dict() method should generate a valid serializable dict '''
        msg=message.UnHookFromUri(uri='my_superuser:uri', irt=uuid.uuid1().hex[0:20])
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(), {'v':message.MessagesVersionCatalog._version_,'action':Messages.UNHOOK_FROM_URI.value,'seq':msg.seq, 'irt':msg.irt, 'payload':{'uri':'my_superuser:uri'}})
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_success_loading_from_dict(self):
        ''' UnHookFromUri.load_from_dict() method should generate a valid UnHookFromUri object '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_success_loading_from_dict_with_global_uri(self):
        ''' UnHookFromUri.load_from_dict() method should generate a valid UnHookFromUri object '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'root:uri'}
        }
        msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_success_loading_from_dict_with_irt(self):
        ''' UnHookFromUri.load_from_dict() method should generate a valid UnHookFromUri object '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{'uri':'root:uri'}
        }
        msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.UNHOOK_FROM_URI)
        self.assertEqual(msg.to_dict(),dict_msg)
        self.assertTrue(isinstance(json.dumps(msg.to_dict()),str))

    def test_UnHookFromUri_failure_loading_from_dict_invalid_version(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':2,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_action(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.HOOK_TO_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_no_seq(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.UNHOOK_FROM_URI.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_seq(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:10],
            'irt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_UnHookFromUri_failure_loading_from_dict_no_irt(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'iirt':None,
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_irt(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':1,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:10],
            'payload':{'uri':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_payload_type(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':['uri','uri']
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_payload_uri_not_found(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'ari':'uri'}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_ELFD)

    def test_UnHookFromUri_failure_loading_from_dict_invalid_payload_uri_invalid(self):
        ''' UnHookFromUri.load_from_dict() method should fail is passed argument is invalid '''
        dict_msg={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.UNHOOK_FROM_URI.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{'uri':['uri']}
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.UnHookFromUri.load_from_dict(dict_msg)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_UHFU_IURI)

    def test_RequestData_success(self):
        ''' Creating a RequestData object should succeed '''
        uri='valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        count=123
        msg=message.RequestData(uri=uri, start=start, end=end, count=count)
        self.assertTrue(isinstance(msg, message.RequestData))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.count, count)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.REQUEST_DATA)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':msg.seq,
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'count':count
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_RequestData_success_no_dates(self):
        ''' Creating a RequestData object should succeed '''
        uri='valid.uri'
        count=123
        msg=message.RequestData(uri=uri, count=count)
        self.assertTrue(isinstance(msg, message.RequestData))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, None)
        self.assertEqual(msg.end, None)
        self.assertEqual(msg.count, count)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.REQUEST_DATA)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':msg.seq,
            'irt':None,
            'payload':{
                'uri':uri,
                'start':None,
                'end':None,
                'count':count
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_RequestData_success_no_count(self):
        ''' Creating a RequestData object should succeed '''
        uri='valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        msg=message.RequestData(uri=uri, start=start, end=end)
        self.assertTrue(isinstance(msg, message.RequestData))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.count, None)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.REQUEST_DATA)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':msg.seq,
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'count':None
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_RequestData_success_with_global_uri(self):
        ''' Creating a RequestData object should succeed '''
        uri='remote_user:valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        count=123
        msg=message.RequestData(uri=uri, start=start, end=end, count=count)
        self.assertTrue(isinstance(msg, message.RequestData))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.count, count)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.REQUEST_DATA)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':msg.seq,
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'count':count
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_RequestData_success_with_irt(self):
        ''' Creating a RequestData object should succeed '''
        uri='remote_user:valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        count=123
        msg=message.RequestData(uri=uri, start=start, end=end, count=count, irt=uuid.uuid1().hex[0:20])
        self.assertTrue(isinstance(msg, message.RequestData))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.count, count)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.REQUEST_DATA)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':msg.seq,
            'irt':msg.irt,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'count':count
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_RequestData_failure_no_count_no_complete_interval(self):
        ''' Creating a RequestData object should fail if no count and no complete interval is passed'''
        uri='valid.uri'
        end=pd.Timestamp('now',tz='utc')
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, end=end)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ECOIN)

    def test_RequestData_failure_invalid_uri(self):
        ''' Creating a RequestData object fail if uri is invalid '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, start=start, end=end)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_IURI)

    def test_RequestData_failure_invalid_start(self):
        ''' Creating a RequestData object fail if start is invalid '''
        uri='valid.uri'
        start=timeuuid.uuid1()
        end=pd.Timestamp('now',tz='utc')
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, start=start, end=end)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ISTART)

    def test_RequestData_failure_invalid_end(self):
        ''' Creating a RequestData object fail if end is invalid '''
        uri='valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=time.time()
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, start=start, end=end)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_IEND)

    def test_RequestData_failure_invalid_count(self):
        ''' Creating a RequestData object fail if count is invalid '''
        uri='valid.uri'
        count=-1
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, count=count)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ICOUNT)

    def test_RequestData_failure_invalid_seq(self):
        ''' Creating a RequestData object fail if seq is invalid '''
        uri='valid.uri'
        seq=1
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, seq=seq)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_RequestData_failure_invalid_irt(self):
        ''' Creating a RequestData object fail if count is invalid '''
        uri='valid.uri'
        irt=1
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData(uri=uri, irt=irt)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_RequestData_failure_error_loading_from_dict_no_dict(self):
        ''' Creating a RequestData object should fail if msg is not a dict '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial=[{
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_no_version(self):
        ''' Creating a RequestData object should fail if v is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'va':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_no_action(self):
        ''' Creating a RequestData object should fail if action is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'theaction':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_no_seq(self):
        ''' Creating a RequestData object should fail if seq is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_invalid_seq(self):
        ''' Creating a RequestData object should fail if seq is invalid '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:30],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_RequestData_failure_error_loading_from_dict_no_irt(self):
        ''' Creating a RequestData object should fail if irt is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'iirt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_invalid_irt(self):
        ''' Creating a RequestData object should fail if irt is invalid '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':90,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_RequestData_failure_error_loading_from_dict_no_payload(self):
        ''' Creating a RequestData object should fail if payload is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'fayload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_invalid_version(self):
        ''' Creating a RequestData object should fail if version is not an int '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':[message.MessagesVersionCatalog._version_],
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_wrong_version(self):
        ''' Creating a RequestData object should fail if version is not the expected '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':9999999999999,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_invalid_action(self):
        ''' Creating a RequestData object should fail if action is invalid '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':[Messages.REQUEST_DATA.value],
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_wrong_action(self):
        ''' Creating a RequestData object should fail if action is not the expected '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DS_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_invalid_payload(self):
        ''' Creating a RequestData object should fail if payload is not a dict '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':[{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }]
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_payload_uri_not_found(self):
        ''' Creating a RequestData object should fail if payload uri is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'ari':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_payload_start_not_found(self):
        ''' Creating a RequestData object should fail if payload start is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'estart':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_payload_end_not_found(self):
        ''' Creating a RequestData object should fail if payload end is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'fin':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_failure_error_loading_from_dict_payload_count_not_found(self):
        ''' Creating a RequestData object should fail if payload count is not found '''
        uri='non valid uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'mount':33,
                'end':end.isoformat()
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_RQDT_ELFD)

    def test_RequestData_success_loading_from_dict(self):
        ''' Creating a RequestData object should succeed '''
        uri='valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':33,
                'end':end.isoformat()
            }
        }
        msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(msg.uri,uri)
        self.assertEqual(msg.start,start)
        self.assertEqual(msg.end,end)
        self.assertEqual(msg.count,33)

    def test_RequestData_success_loading_from_dict_with_global_uri(self):
        ''' Creating a RequestData object should succeed '''
        uri='the_remote_master:valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':None,
                'end':end.isoformat()
            }
        }
        msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(msg.uri,uri)
        self.assertEqual(msg.start,start)
        self.assertEqual(msg.end,end)
        self.assertEqual(msg.count,None)

    def test_RequestData_success_loading_from_dict_with_irt(self):
        ''' Creating a RequestData object should succeed '''
        uri='the_remote_master:valid.uri'
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'count':None,
                'end':end.isoformat()
            }
        }
        msg=message.RequestData.load_from_dict(serial)
        self.assertEqual(msg.uri,uri)
        self.assertEqual(msg.seq, serial['seq'])
        self.assertEqual(msg.irt, serial['irt'])
        self.assertEqual(msg.start,start)
        self.assertEqual(msg.end,end)
        self.assertEqual(msg.count,None)

    def test_SendDataInterval_success(self):
        ''' Creating a SendDataInterval object should succeed '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertTrue(isinstance(msg, message.SendDataInterval))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.data, data)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DATA_INTERVAL)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':msg.seq,
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_SendDataInterval_success_with_global_uri(self):
        ''' Creating a SendDataInterval object should succeed '''
        uri={'uri':'other_group:valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertTrue(isinstance(msg, message.SendDataInterval))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.data, data)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DATA_INTERVAL)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':msg.seq,
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_SendDataInterval_success_with_irt(self):
        ''' Creating a SendDataInterval object should succeed '''
        uri={'uri':'other_group:valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data, irt=uuid.uuid1().hex[0:20])
        self.assertTrue(isinstance(msg, message.SendDataInterval))
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end, end)
        self.assertEqual(msg.data, data)
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DATA_INTERVAL)
        expected_dict={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':msg.seq,
            'irt':msg.irt,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        self.assertEqual(msg.to_dict(), expected_dict)

    def test_SendDataInterval_failure_invalid_uri_type(self):
        ''' Creating a SendDataInterval object should fail if uri is not a dict '''
        uri=[{'uri':'valid.uri','type':vertex.DATAPOINT}]
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IURI)

    def test_SendDataInterval_failure_invalid_uri_dict_has_no_uri(self):
        ''' Creating a SendDataInterval object should fail if uri dict has no uri '''
        uri={'ari':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IURI)

    def test_SendDataInterval_failure_invalid_uri_dict_invalid_uri(self):
        ''' Creating a SendDataInterval object should fail if uri dict has invalid uri '''
        uri={'uri':'in valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IURI)

    def test_SendDataInterval_failure_invalid_uri_dict_has_no_type(self):
        ''' Creating a SendDataInterval object should fail if uri dict has no type '''
        uri={'uri':'valid.uri','taip':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IURI)

    def test_SendDataInterval_failure_invalid_uri_dict_has_invalid_type(self):
        ''' Creating a SendDataInterval object should fail if uri dict has invalid type '''
        uri={'uri':'valid.uri','type':vertex.WIDGET}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IURI)

    def test_SendDataInterval_failure_invalid_start(self):
        ''' Creating a SendDataInterval object should fail if start is invalid '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=timeuuid.uuid1()
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ISTART)

    def test_SendDataInterval_failure_invalid_end(self):
        ''' Creating a SendDataInterval object should fail if end is invalid '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=time.time()
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IEND)

    def test_SendDataInterval_failure_invalid_data_not_a_list(self):
        ''' Creating a SendDataInterval object should fail if data is not a list '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_data_not_item_tuple(self):
        ''' Creating a SendDataInterval object should fail if data has a non tuple item '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            [(pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'],
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_data_tuple_not_two_elements(self):
        ''' Creating a SendDataInterval object should fail if data has tuple without two items '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243','third'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_data_item0_not_isodate(self):
        ''' Creating a SendDataInterval object should fail if data an item[0] that is not an isodate '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            (time.time(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_data_item0_not_isodate_string(self):
        ''' Creating a SendDataInterval object should fail if data an item[0] isodate but not in string form '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            (pd.Timestamp('now',tz='utc')-pd.Timedelta('8m'),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_data_item0_not_tz_in_isodate_string(self):
        ''' Creating a SendDataInterval object should fail if data an item[0] isodate string without timezone '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_data_item1_not_a_string(self):
        ''' Creating a SendDataInterval object should fail if data an item[1] is not a string '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),243),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_IDATA)

    def test_SendDataInterval_failure_invalid_irt(self):
        ''' Creating a SendDataInterval object should fail if irt is invalid '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        irt=123
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data, irt=irt)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_SendDataInterval_failure_invalid_seq(self):
        ''' Creating a SendDataInterval object should fail if seq is invalid '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=(
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        )
        seq=9234
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval(uri=uri, start=start, end=end, data=data, seq=seq)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_SendDataInterval_failure_load_from_dict_failure_not_a_dict(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg is not a dict '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial=[{
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }]
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_failure_not_v(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has no version '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'vi':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_failure_no_action(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has no action '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'theaction':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_failure_no_seq(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has no seq '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'iseq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_failure_invalid_seq(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has invalid seq '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:10],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_ISEQ)

    def test_SendDataInterval_failure_load_from_dict_failure_no_irt(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has no irt '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'iirt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_failure_invalid_irt(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has invalid irt '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':12,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_MVC_IIRT)

    def test_SendDataInterval_failure_load_from_dict_failure_no_payload(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg has no payload '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'iipayload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_invalid_v(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg v is invalid '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':[message.MessagesVersionCatalog._version_],
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_wrong_v(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg v is not the expected '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_+1,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_invalid_action(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg action is invalid '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_wrong_action(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg action is not the expected '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.REQUEST_DATA.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_payload_not_a_dict(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg payload is not a dict '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':[{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }]
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_payload_without_uri(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg payload has no uri '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'iuri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_payload_without_start(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg payload has no start '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'estart':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_payload_without_end(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg payload has no end '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'theend':end.isoformat(),
                'data':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_failure_load_from_dict_payload_without_data(self):
        ''' Creating a SendDataInterval object from a dict should fail if msg payload has no data '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'idata':data,
            }
        }
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            msg=message.SendDataInterval.load_from_dict(serial)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MM_SDI_ELFD)

    def test_SendDataInterval_success_load_from_dict(self):
        ''' Creating a SendDataInterval object from a dict should succeed '''
        uri={'uri':'valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        msg=message.SendDataInterval.load_from_dict(serial)
        self.assertTrue(isinstance(msg, message.SendDataInterval))
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DATA_INTERVAL)
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end,end)
        self.assertEqual(msg.data,data)

    def test_SendDataInterval_success_load_from_dict_with_global_uri(self):
        ''' Creating a SendDataInterval object from a dict should succeed '''
        uri={'uri':'other_user:valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':None,
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        msg=message.SendDataInterval.load_from_dict(serial)
        self.assertTrue(isinstance(msg, message.SendDataInterval))
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DATA_INTERVAL)
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end,end)
        self.assertEqual(msg.data,data)

    def test_SendDataInterval_success_load_from_dict_with_irt(self):
        ''' Creating a SendDataInterval object from a dict should succeed '''
        uri={'uri':'other_user:valid.uri','type':vertex.DATAPOINT}
        start=pd.Timestamp('now',tz='utc')-pd.Timedelta('10m')
        end=pd.Timestamp('now',tz='utc')
        data=[
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('9m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('8m')).isoformat(),'223'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('7m')).isoformat(),'273.32'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('6m')).isoformat(),'243'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('5m')).isoformat(),'283'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('4m')).isoformat(),'223.44'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('3m')).isoformat(),'213'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('2m')).isoformat(),'743'),
            ((pd.Timestamp('now',tz='utc')-pd.Timedelta('1m')).isoformat(),'283'),
        ]
        serial={
            'v':message.MessagesVersionCatalog._version_,
            'action':Messages.SEND_DATA_INTERVAL.value,
            'seq':uuid.uuid1().hex[0:20],
            'irt':uuid.uuid1().hex[0:20],
            'payload':{
                'uri':uri,
                'start':start.isoformat(),
                'end':end.isoformat(),
                'data':data,
            }
        }
        msg=message.SendDataInterval.load_from_dict(serial)
        self.assertTrue(isinstance(msg, message.SendDataInterval))
        self.assertEqual(msg.v, message.MessagesVersionCatalog._version_)
        self.assertEqual(msg.action, Messages.SEND_DATA_INTERVAL)
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg.seq, serial['seq'])
        self.assertEqual(msg.irt, serial['irt'])
        self.assertEqual(msg.start, start)
        self.assertEqual(msg.end,end)
        self.assertEqual(msg.data,data)

