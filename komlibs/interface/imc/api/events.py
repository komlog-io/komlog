'''

Events message definitions

'''

import uuid
from komfig import logger
from komlibs.general.validation import arguments as args
from komlibs.events.api import user as usereventsapi
from komlibs.events.model import types as eventstypes
from komlibs.interface.imc.model import messages, responses
from komlibs.interface.imc import status, exceptions


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

