import unittest
import uuid
from komfig import logger
from komimc import bus, routing
from komimc import api as msgapi
from komlibs.interface.imc.model import messages
from komlibs.interface.websocket.protocol.v1 import errors, exceptions
from komlibs.interface.websocket.protocol.v1.processing import operation
from komlibs.interface.websocket.protocol.v1.model import operation as modop


class InterfaceWebSocketProtocolV1ProcessingOperationTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.processing.operation tests '''

    def test_process_operation_failure_invalid_operation_type(self):
        ''' the process_operation should fail if operation parameter is not a valid object '''
        operations=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}]
        for op in operations:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                resp=operation.process_operation(operation=op)
            self.assertEqual(cm.exception.error, errors.E_IWSPV1PO_ROA_IOT)

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
        self.assertEqual(cm.exception.error, errors.E_IWSPV1PO_ROA_ONF)
        operation._operation_funcs=original_funcs

    def test_process_operation_new_datasource_success(self):
        ''' the process_operation_new_datasource function should succeed and send the corresponding messages '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        op=modop.NewDatasourceOperation(uid=uid, aid=aid, did=did)
        self.assertTrue(operation.process_operation(operation=op))
        message_expected={messages.UPDATE_QUOTES_MESSAGE:1,messages.NEW_DS_WIDGET_MESSAGE:1,messages.USER_EVENT_MESSAGE:1}
        message_retrieved={}
        for msg_type in routing.MESSAGE_TO_ADDRESS_MAPPING.keys():
            msg_addr=routing.get_address(type=msg_type, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    message_retrieved[msg.type] = message_retrieved.get(msg.type,0) + 1
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
        self.assertEqual(message_retrieved, message_expected)

