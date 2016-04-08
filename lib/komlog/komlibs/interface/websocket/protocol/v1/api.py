'''

This file implement the v1 api of the websocket protocol

'''

from komlog.komlibs.interface.websocket.protocol.v1 import status, exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import message as procmsg
from komlog.komlibs.interface.websocket.protocol.v1.model.response import Response
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Message



@exceptions.ExceptionHandler
def process_message(passport, message):
    try:
        return _processing_funcs[message['action']](passport, message)
    except KeyError:
        return Response(status=status.PROTOCOL_ERROR, error=Errors.E_IWSPV1A_PM_IA.value, reason='unsupported action')

_processing_funcs = {
    Message.SEND_DS_DATA:procmsg._process_send_ds_data,
}

