'''
operation.py

This file contains classes and functions related with message operations 
(operation=actions generated by successfully procesed messages)

We associate message operations with auth operations, so that we can
update user resource utilization and control access based on this

'''

import json
import uuid
from komlog.komfig import logger
from komlog.komimc import api as msgapi
from komlog.komlibs.auth import operations as authoperations
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.general.validation import arguments
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.interface.websocket.protocol.v1 import errors, exceptions
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Operation

def process_operation(operation):
    if not isinstance(operation, modop.WSIFaceOperation):
        raise exceptions.BadParametersException(error=errors.E_IWSPV1PO_ROA_IOT)
    if operation.oid not in _operation_funcs:
        raise exceptions.OperationValidationException(error=errors.E_IWSPV1PO_ROA_ONF)
    return _operation_funcs[operation.oid](operation)

def _process_operation_new_datasource(operation):
    if authupdate.update_resources(operation=operation.auth_operation, params=operation.params):
        message=messages.UpdateQuotesMessage(operation=operation.auth_operation, params=operation.params)
        msgapi.send_message(message)
        message=messages.NewDSWidgetMessage(uid=operation.uid,did=operation.did)
        msgapi.send_message(message)
        message=messages.UserEventMessage(uid=operation.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, parameters={'did':operation.did.hex})
        msgapi.send_message(message)
        return True
    else:
        return False

_operation_funcs = {
    Operation.NEW_DATASOURCE:_process_operation_new_datasource,
}
