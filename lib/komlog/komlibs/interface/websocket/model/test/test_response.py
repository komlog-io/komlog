import unittest
import time
import uuid
import json
from komlog.komfig import logging
from komlog.komlibs.general.time.timeuuid import TimeUUID
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.errors import Errors
from komlog.komlibs.interface.websocket.model import response
from komlog.komlibs.interface.websocket.model.types import Messages


class InterfaceWebSocketModelResponseTest(unittest.TestCase):
    ''' komlibs.interface.websocket.model.response tests '''

    def test_new_processing_result_success(self):
        ''' a new WSocketIfaceResponse object should be created '''
        resp=response.WSocketIfaceResponse(status=1, error=Errors.OK)
        self.assertTrue(isinstance(resp,response.WSocketIfaceResponse))
        self.assertEqual(resp.ws_messages,[])
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})

    def test_WSocketIfaceResponse_invalid_status(self):
        ''' WSocketIfaceResponse creation should fail if status is invalid '''
        with self.assertRaises(exceptions.ResponseValidationException) as cm:
            resp=response.WSocketIfaceResponse(status='invalid', error=Errors.OK)
        self.assertEqual(cm.exception.error, Errors.E_IWSMR_PR_IS)

    def test_WSocketIfaceResponse_success_setting_imc_messages(self):
        ''' when adding a msg to a WSocketIfaceResponse, the message should be added successfully to the imc_messages attributes '''
        dest='host'
        routed_messages=['message1','message2','message3','message4']
        unrouted_messages=['msg1','msg2','msg3','msg4']
        resp=response.WSocketIfaceResponse(status=1, error=Errors.OK)
        for msg in unrouted_messages:
            self.assertTrue(resp.add_imc_message(msg))
        for msg in routed_messages:
            self.assertTrue(resp.add_imc_message(msg, dest=dest))
        self.assertEqual(resp.imc_messages,{'routed':{dest:routed_messages},'unrouted':unrouted_messages})

    def test_WSocketIfaceResponse_success_setting_ws_messages(self):
        ''' when adding a msg to a WSocketIfaceResponse, the message should be added successfully to the ws_messages attributes '''
        ws_messages=['msg1','msg2','msg3','msg4']
        resp=response.WSocketIfaceResponse(status=1, error=Errors.OK)
        for msg in ws_messages:
            self.assertTrue(resp.add_ws_message(msg))
        self.assertEqual(resp.ws_messages,ws_messages)

    def test_GenericResponse_success(self):
        ''' a new GenericResponse object should be created '''
        resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason')
        self.assertTrue(isinstance(resp,response.GenericResponse))
        self.assertEqual(resp.status,1)
        self.assertEqual(resp.error,Errors.OK)
        self.assertEqual(resp.reason,'reason')
        self.assertEqual(resp.irt,None)
        self.assertEqual(resp.v,0)
        self.assertNotEqual(resp.seq,None)
        self.assertEqual(resp.action, Messages.GENERIC_RESPONSE)

    def test_GenericResponse_to_dict_success(self):
        ''' a new GenericResponse object should be created. and to_dict should succeed '''
        resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason', v=7, irt=TimeUUID())
        self.assertTrue(isinstance(resp,response.GenericResponse))
        self.assertEqual(resp.status,1)
        self.assertEqual(resp.error,Errors.OK)
        self.assertEqual(resp.reason,'reason')
        self.assertEqual(resp.v,7)
        expected_dict ={
            'action':Messages.GENERIC_RESPONSE.value,
            'v':7,
            'seq':resp.seq.hex,
            'irt':resp.irt.hex,
            'payload':{
                'status':1,
                'error':Errors.OK.value,
                'reason':'reason'
            }
        }
        self.assertEqual(expected_dict, resp.to_dict())

    def test_GenericResponse_failure_action_cannot_be_modified(self):
        ''' Trying to modify a GenericResponse action should fail '''
        resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason', v=7, irt=TimeUUID())
        with self.assertRaises(TypeError) as cm:
            resp.action='whatever'
        self.assertEqual(str(cm.exception), 'Action cannot be modified')

    def test_GenericResponse_failure_version_cannot_be_modified(self):
        ''' Trying to modify a GenericResponse version should fail '''
        resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason', v=7, irt=TimeUUID())
        with self.assertRaises(TypeError) as cm:
            resp.v=9
        self.assertEqual(str(cm.exception), 'Version cannot be modified')

    def test_GenericResponse_failure_invalid_version(self):
        ''' Should get an exception if GenericResponse version is invalid '''
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason', v='version', irt=TimeUUID())
        self.assertEqual(cm.exception.error, Errors.E_IWSMR_GR_IV)

    def test_GenericResponse_failure_sequence_cannot_be_modified(self):
        ''' Trying to modify a GenericResponse sequence should fail '''
        resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason', v=7, irt=TimeUUID())
        with self.assertRaises(TypeError) as cm:
            resp.seq=uuid.uuid1().hex[0:20]
        self.assertEqual(str(cm.exception), 'Sequence cannot be modified')

    def test_GenericResponse_failure_invalid_sequence(self):
        ''' Should get an exception if GenericResponse version is invalid '''
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            resp=response.GenericResponse(status=1,error=Errors.OK,reason='reason', v=1, irt=TimeUUID(), seq=uuid.uuid1())
        self.assertEqual(cm.exception.error, Errors.E_IWSMR_GR_ISEQ)

    def test_GenericResponse_failure_invalid_status(self):
        ''' Should get an exception if GenericResponse status is invalid '''
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            resp=response.GenericResponse(status='23',error=Errors.OK,reason='reason', v=1, irt=TimeUUID())
        self.assertEqual(cm.exception.error, Errors.E_IWSMR_GR_IS)

    def test_GenericResponse_failure_invalid_irt(self):
        ''' Should get an exception if GenericResponse irt is invalid '''
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            resp=response.GenericResponse(status=4000, error=Errors.OK, reason='reason', v=1, irt=uuid.uuid1())
        self.assertEqual(cm.exception.error, Errors.E_IWSMR_GR_IIRT)

