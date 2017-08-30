'''

This file implement the v1 api of the websocket protocol

'''

import time
import json
from komlog.komfig import logging
from komlog.komlibs.auth.passport import AgentPassport
from komlog.komlibs.general.time.timeuuid import TimeUUID
from komlog.komlibs.interface.websocket import status, exceptions
from komlog.komlibs.interface.websocket.model.response import GenericResponse, WSocketIfaceResponse
from komlog.komlibs.interface.websocket.model.types import Messages
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import message as procmsg



def process_message(passport, message):
    try:
        return _processing_funcs[message['action']](passport=passport, message=message)
    except KeyError:
        t=time.time()
        error=Errors.E_IWSPV1A_PM_IA
        log = {
            'func':'komlog.komlibs.interface.websocket.protocol.v1.api.process_message',
            'uid':passport.uid.hex,
            'aid':passport.aid.hex,
            'sid':passport.sid.hex,
            'ts':t,
            'error':error.name,
            'duration':0,
        }
        logging.c_logger.info(json.dumps(log))
        irt = TimeUUID(s=message['seq'])
        ws_res = GenericResponse(status=status.PROTOCOL_ERROR, error=error,reason='unsupported action', irt=irt, v=message['v'])
        result = WSocketIfaceResponse(status=status.PROTOCOL_ERROR, error=error)
        result.add_ws_message(ws_res)
        return result

_processing_funcs = {
    Messages.SEND_DS_DATA.value:procmsg._process_send_ds_data,
    Messages.SEND_DP_DATA.value:procmsg._process_send_dp_data,
    Messages.SEND_MULTI_DATA.value:procmsg._process_send_multi_data,
    Messages.HOOK_TO_URI.value:procmsg._process_hook_to_uri,
    Messages.UNHOOK_FROM_URI.value:procmsg._process_unhook_from_uri,
    Messages.REQUEST_DATA.value:procmsg._process_request_data,
}

