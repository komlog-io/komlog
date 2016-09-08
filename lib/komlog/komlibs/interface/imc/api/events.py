'''

Events message definitions

'''

import uuid
from komlog.komfig import logging
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.events.api import user as usereventsapi
from komlog.komlibs.events.api import user_responses as userrespeventsapi
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.imc.model import messages, responses


@exceptions.ExceptionHandler
def process_message_USEREV(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    uid=message.uid
    event_type=message.event_type
    parameters=message.parameters
    if usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters):
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAE_USEREV_ECE
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_USEREVRESP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    uid=message.uid
    date=message.date
    parameters=message.parameters
    if userrespeventsapi.process_event_response(uid=uid, date=date, response_data=parameters):
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAE_USEREVRESP_EPER
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

