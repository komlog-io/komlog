'''

this file implements methods for processing messages coming from the
websocket interface

'''

from komlog.komfig import logger
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.interface.websocket.protocol.v1 import api as apiv1
from komlog.komlibs.interface.websocket.protocol.v1.model import response as responsev1
from komlog.komlibs.interface.websocket.protocol.v1 import status as statusv1
from komlog.komlibs.interface.websocket.protocol.v1 import errors as errorsv1

def process_message(passport, message):
    if not isinstance(passport, Passport):
        return responsev1.Response(status=statusv1.INTERNAL_ERROR, reason='Ups... Internal error', error=errorsv1.E_IWSA_PM_IPSP)
    if not args.is_valid_dict(message)\
        or not 'v' in message\
        or not 'action' in message\
        or not args.is_valid_int(message['v'])\
        or not args.is_valid_string(message['action']):
        logger.logger.debug('invalid msg received: '+str(message))
        return responsev1.Response(status=statusv1.PROTOCOL_ERROR, reason='Send a valid version and action', error=errorsv1.E_IWSA_PM_IVA)
    if message['v']==1:
        return apiv1.process_message(passport, message)
    else:
        return responsev1.Response(status=statusv1.PROTOCOL_ERROR, reason='Unsupported protocol version', error=errorsv1.E_IWSA_PM_UPV)

