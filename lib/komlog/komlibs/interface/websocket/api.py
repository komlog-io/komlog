'''

this file implements methods for processing messages coming from the
websocket interface

'''

import time
from komlog.komfig import logging
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.auth.passport import AgentPassport
from komlog.komlibs.interface.websocket.model import response
from komlog.komlibs.interface.websocket import status
from komlog.komlibs.interface.websocket.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1 import api as apiv1

def process_message(passport, message):
    if not (args.is_valid_dict(message)
        and 'v' in message
        and 'action' in message
        and 'seq' in message
        and args.is_valid_int(message['v'])
        and args.is_valid_string(message['action'])
        and args.is_valid_message_sequence(message['seq'])):
        t=time.time()
        error=Errors.E_IWSA_PM_IVA
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.api.process_message',error.name,str(t),str(t))))
        v = message['v'] if 'v' in message and args.is_valid_int(message['v']) else 0
        irt = message['seq'] if 'seq' in message and args.is_valid_message_sequence(message['seq']) else None
        ws_res = response.GenericResponse(status=status.PROTOCOL_ERROR, reason='Malformed message', error=error, irt=irt, v=v)
        result = response.WSocketIfaceResponse(status=status.PROTOCOL_ERROR, error=error)
        result.add_ws_message(ws_res)
        return result
    if not isinstance(passport, AgentPassport):
        t=time.time()
        error=Errors.E_IWSA_PM_IPSP
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.api.process_message',error.name,str(t),str(t))))
        ws_res = response.GenericResponse(status=status.INTERNAL_ERROR, reason='Ups... Internal error', error=error, irt=message['seq'], v=message['v'])
        result = response.WSocketIfaceResponse(status=status.INTERNAL_ERROR, error=error)
        result.add_ws_message(ws_res)
        return result
    if message['v']==1:
        return apiv1.process_message(passport, message)
    else:
        t=time.time()
        error=Errors.E_IWSA_PM_UPV
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.api.process_message',error.name,str(t),str(t))))
        ws_res = response.GenericResponse(status=status.PROTOCOL_ERROR, reason='Unsupported protocol version', error=error, irt=message['seq'], v=message['v'])
        result = response.WSocketIfaceResponse(status=status.PROTOCOL_ERROR, error=error)
        result.add_ws_message(ws_res)
        return result

