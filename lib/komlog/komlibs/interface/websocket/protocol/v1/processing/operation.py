'''
operation.py

This file contains classes and functions related with message operations 
(operation=actions generated by successfully procesed messages)

We associate message operations with auth operations, so that we can
update user resource utilization and control access based on this

'''

import json
import uuid
from komlog.komfig import logging
from komlog.komimc import api as msgapi
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.general.validation import arguments
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.model.types import Operations
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop

def process_operation(operation):
    if not isinstance(operation, modop.WSIFaceOperation):
        raise exceptions.BadParametersException(error=Errors.E_IWSPV1PO_ROA_IOT)
    try:
        return _operation_funcs[operation.oid](operation)
    except KeyError:
        raise exceptions.OperationValidationException(error=Errors.E_IWSPV1PO_ROA_ONF)

def _process_operation_new_datasource(operation):
    if authupdate.update_resources(operation=operation.auth_operation, params=operation.params):
        msgs=[]
        msgs.append(messages.UpdateQuotesMessage(operation=operation.auth_operation, params=operation.params))
        msgs.append(messages.NewDSWidgetMessage(uid=operation.uid,did=operation.did))
        msgs.append(messages.UserEventMessage(uid=operation.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, parameters={'did':operation.did.hex}))
        return msgs
    else:
        raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PO_PONDS_EUR)

def _process_operation_new_user_datapoint(operation):
    if authupdate.update_resources(operation=operation.auth_operation, params=operation.params):
        msgs=[]
        msgs.append(messages.UpdateQuotesMessage(operation=operation.auth_operation, params=operation.params))
        msgs.append(messages.NewDPWidgetMessage(uid=operation.uid,pid=operation.pid))
        return msgs
    else:
        raise exceptions.OperationValidationException(error=Errors.E_IWSPV1PO_PONUDP_EUR)

def _process_operation_datasource_data_stored(operation):
    msgs=[]
    msgs.append(messages.UpdateQuotesMessage(operation=operation.auth_operation,params=operation.params))
    msgs.append(messages.GenerateTextSummaryMessage(did=operation.did,date=operation.date))
    msgs.append(messages.MapVarsMessage(did=operation.did,date=operation.date))
    return msgs

def _process_operation_datapoint_data_stored(operation):
    msgs=[]
    msgs.append(messages.UpdateQuotesMessage(operation=operation.auth_operation,params=operation.params))
    return msgs

_operation_funcs = {
    Operations.NEW_DATASOURCE:_process_operation_new_datasource,
    Operations.NEW_USER_DATAPOINT:_process_operation_new_user_datapoint,
    Operations.DATASOURCE_DATA_STORED:_process_operation_datasource_data_stored,
    Operations.DATAPOINT_DATA_STORED:_process_operation_datapoint_data_stored,
}

