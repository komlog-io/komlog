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
    if not isinstance(passport, AgentPassport):
        t=time.time()
        error=Errors.E_IWSA_PM_IPSP
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.api.process_message',error.name,str(t),str(t))))
        return response.Response(status=status.INTERNAL_ERROR, reason='Ups... Internal error', error=error.value)
    if not args.is_valid_dict(message)\
        or not 'v' in message\
        or not 'action' in message\
        or not args.is_valid_int(message['v'])\
        or not args.is_valid_string(message['action']):
        t=time.time()
        error=Errors.E_IWSA_PM_IVA
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.api.process_message',error.name,str(t),str(t))))
        return response.Response(status=status.PROTOCOL_ERROR, reason='Send a valid version and action', error=error.value)
    if message['v']==1:
        return apiv1.process_message(passport, message)
    else:
        t=time.time()
        error=Errors.E_IWSA_PM_UPV
        logging.c_logger.info(','.join(('komlog.komlibs.interface.websocket.api.process_message',error.name,str(t),str(t))))
        return response.Response(status=status.PROTOCOL_ERROR, reason='Unsupported protocol version', error=error.value)

