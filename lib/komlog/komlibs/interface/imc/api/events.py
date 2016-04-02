'''

Events message definitions

'''

import uuid
from komlog.komfig import logger
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.events.api import user as usereventsapi
from komlog.komlibs.events.api import user_responses as userrespeventsapi
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.imc import status, exceptions


@exceptions.ExceptionHandler
def process_message_USEREV(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    uid=message.uid
    event_type=message.event_type
    parameters=message.parameters
    if usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_USEREVRESP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    uid=message.uid
    date=message.date
    parameters=message.parameters
    if userrespeventsapi.process_event_response(uid=uid, date=date, response_data=parameters):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

