'''

This file implement the v1 api of the websocket protocol

'''

from komlibs.interface.websocket.protocol.v1 import status, exceptions, errors
from komlibs.interface.websocket.protocol.v1.processing import message as procmsg
from komlibs.interface.websocket.protocol.v1.model.response import Response
from komlibs.interface.websocket.protocol.v1.model.types import Message



@exceptions.ExceptionHandler
def process_message(passport, message):
    try:
        return _processing_funcs[message['action']](passport, message)
    except KeyError:
        return Response(status=status.PROTOCOL_ERROR, error=errors.E_IWSPV1A_PM_IA, reason='unsupported action')

_processing_funcs = {
    Message.SEND_DS_DATA:procmsg._process_send_ds_data,
}

