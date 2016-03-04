'''

This file implement the v1 api of the websocket protocol

'''

from komlibs.interface.websocket.protocol.v1 import status, exceptions, errors
from komlibs.interface.websocket.protocol.v1.processing import message as procmsg
from komlibs.interface.websocket.protocol.v1.model import response, types


@exceptions.ExceptionHandler
def process_message(username, aid, message):
    try:
        return _processing_funcs[message['action']](username, aid, message)
    except KeyError:
        return response.Response(status=status.PROTOCOL_ERROR, error=errors.E_IWSPV1A_PM_IA, reason='unsupported action')

_processing_funcs = {
    types.MESSAGE_POST_DATASOURCE_DATA:procmsg._process_post_datasource_data,
}

