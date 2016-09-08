import unittest
import uuid
from komlog.komfig import logging
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop


class InterfaceWebSocketProtocolV1ProcessingOperationTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.processing.operation tests '''

    def test_process_operation_failure_invalid_operation_type(self):
        ''' the process_operation should fail if operation parameter is not a valid object '''
        operations=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}]
        for op in operations:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                resp=operation.process_operation(operation=op)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1PO_ROA_IOT)

    def test_process_operation_failure_operation_ID_not_found(self):
        ''' the process_operation should fail if operation parameter is not a valid object '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        op=modop.NewDatasourceOperation(uid=uid, aid=aid, did=did)
        original_funcs=operation._operation_funcs
        operation._operation_funcs={}
        with self.assertRaises(exceptions.OperationValidationException) as cm:
            resp=operation.process_operation(operation=op)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1PO_ROA_ONF)
        operation._operation_funcs=original_funcs

    def test_process_operation_new_datasource_success(self):
        ''' the process_operation_new_datasource function should succeed and send the corresponding messages '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        op=modop.NewDatasourceOperation(uid=uid, aid=aid, did=did)
        msgs=operation.process_operation(operation=op)
        message_expected={messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,messages.Messages.USER_EVENT_MESSAGE.value:1}
        message_retrieved={}
        for msg in msgs:
            try:
                message_retrieved[msg._type_.value]+=1
            except KeyError:
                message_retrieved[msg._type_.value]=1
        self.assertEqual(sorted(message_retrieved), sorted(message_expected))

    def test_process_operation_new_user_datapoint_success(self):
        ''' _process_operation_new_user_datapoint should succeed and send the corresponding messages '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        op=modop.NewUserDatapointOperation(uid=uid, aid=aid, pid=pid)
        msgs=operation.process_operation(operation=op)
        message_expected={messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,messages.Messages.UPDATE_QUOTES_MESSAGE.value:1}
        message_retrieved={}
        for msg in msgs:
            try:
                message_retrieved[msg._type_.value]+=1
            except KeyError:
                message_retrieved[msg._type_.value]=1
        self.assertEqual(sorted(message_retrieved), sorted(message_expected))

    def test_process_operation_datasource_data_stored_success(self):
        ''' _process_operation_datasource_data_stored should succeed and send the corresponding messages '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=uuid.uuid1()
        op=modop.DatasourceDataStoredOperation(uid=uid, did=did, date=date)
        msgs=operation.process_operation(operation=op)
        message_expected={messages.Messages.GENERATE_TEXT_SUMMARY_MESSAGE.value:1,
                          messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,
                          messages.Messages.MAP_VARS_MESSAGE.value:1}
        message_retrieved={}
        for msg in msgs:
            try:
                message_retrieved[msg._type_.value]+=1
            except KeyError:
                message_retrieved[msg._type_.value]=1
        self.assertEqual(sorted(message_retrieved), sorted(message_expected))

    def test_process_operation_datapoint_data_stored_success(self):
        ''' _process_operation_datapoint_data_stored should succeed and send the corresponding messages '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        date=uuid.uuid1()
        op=modop.DatapointDataStoredOperation(uid=uid, pid=pid, date=date)
        msgs=operation.process_operation(operation=op)
        message_expected={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,
        }
        message_retrieved={}
        for msg in msgs:
            try:
                message_retrieved[msg._type_.value]+=1
            except KeyError:
                message_retrieved[msg._type_.value]=1
        self.assertEqual(sorted(message_retrieved), sorted(message_expected))

