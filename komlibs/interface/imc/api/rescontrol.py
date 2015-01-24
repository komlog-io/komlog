#coding:utf-8
'''

Resource Control message definitions

'''

from komfig import logger
from komlibs.auth import update
from komlibs.general.validation import arguments as args
from komlibs.interface.imc.model import messages, responses
from komlibs.interface.imc import status, exceptions


def process_message_UPDQUO(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    quotes_to_update=list(message.operation.get_quotes_to_update())
    params=message.operation.get_params()
    for quote in quotes_to_update:
        if update.update_quote(quote=quote, params=params):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
            logger.logger.debug('Quote update failed: '+quote)
    return response

def process_message_RESAUTH(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    auths_to_update=list(message.operation.get_auths_to_update())
    params=message.operation.get_params()
    for auth in auths_to_update:
        if update.update_resource_auth(auth=auth, params=params):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
            logger.logger.debug('Resource authorization update failed: '+auth)
    return response

