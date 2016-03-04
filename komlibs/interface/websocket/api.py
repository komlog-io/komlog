'''

this file implements methods for processing messages coming from the
websocket interface

'''

from komlibs.general.validation import arguments as args
from komlibs.interface.websocket.protocol.v1 import api as apiv1
from komlibs.interface.websocket.protocol.v1.model import response as responsev1
from komlibs.interface.websocket.protocol.v1 import status as statusv1
from komlibs.interface.websocket.protocol.v1 import errors as errorsv1

def process_message(username, aid, message):
    if not args.is_valid_dict(message)\
        or not 'v' in message\
        or not 'action' in message\
        or not args.is_valid_int(message['v'])\
        or not args.is_valid_int(message['action']):
        return responsev1.Response(status=statusv1.PROTOCOL_ERROR, reason='send a valid version and action', error=errorsv1.E_IWSA_PM_IVA)
    if message['v']==1:
        return apiv1.process_message(username, aid, message)
    else:
        return responsev1.Response(status=statusv1.PROTOCOL_ERROR, reason='unsupported protocol version', error=errorsv1.E_IWSA_PM_UPV)

