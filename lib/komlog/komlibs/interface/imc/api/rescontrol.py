#coding:utf-8
'''

Resource Control message definitions

'''

from komlog.komfig import logging
from komlog.komlibs.auth import update
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.imc import status, exceptions


def process_message_UPDQUO(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    operation=message.operation
    params=message.params
    if update.update_quotes(operation=operation, params=params):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
        logging.logger.debug('Quote update failed: '+str(operation))
    return response

def process_message_RESAUTH(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    operation=message.operation
    params=message.params
    if update.update_resources(operation=operation, params=params):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
        logging.logger.debug('Resource authorization update failed: '+str(operation))
    return response

