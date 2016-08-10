'''

This file implement the v1 api of the websocket protocol

'''

import time
from komlog.komfig import logging
from komlog.komlibs.interface.websocket.protocol.v1 import status, exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import message as procmsg
from komlog.komlibs.interface.websocket.protocol.v1.model.response import Response
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Messages



def process_message(passport, message):
    try:
        return _processing_funcs[message['action']](passport, message)
    except KeyError:
        t=time.time()
        error=Errors.E_IWSPV1A_PM_IA
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.protocol.v1.api.process_message',error.name,str(t),str(t))))
        return Response(status=status.PROTOCOL_ERROR, error=error.value,reason='unsupported action')

_processing_funcs = {
    Messages.SEND_DS_DATA.value:procmsg._process_send_ds_data,
    Messages.SEND_DP_DATA.value:procmsg._process_send_dp_data,
    Messages.SEND_MULTI_DATA.value:procmsg._process_send_multi_data,
    Messages.HOOK_TO_URI.value:procmsg._process_hook_to_uri,
    Messages.UNHOOK_FROM_URI.value:procmsg._process_unhook_from_uri,
    Messages.REQUEST_DATA_INTERVAL.value:procmsg._process_request_data_interval,
}

