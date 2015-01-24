#coding: utf-8
'''
Textmining message definitions

'''

import json
from komfig import logger
from komlibs.general.validation import arguments as args
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.interface.imc.model import messages, responses
from komlibs.interface.imc import status, exceptions

@exceptions.ExceptionHandler
def process_message_GDTREE(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    pid=message.pid
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    if datapointapi.generate_decision_tree(pid=pid):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_MAPVARS(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did) or not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    if datasourceapi.generate_datasource_map(did=did, date=date):
        newmsg=messages.FillDatasourceMessage(did=did,date=date)
        response.add_msg_originated(newmsg)
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_FILLDP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    pid=message.pid
    date=message.date
    if not args.is_valid_uuid(pid) and not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    if datapointapi.store_datapoint_values(pid=pid, date=date):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_FILLDS(message):
    #este mensaje hay que dividirlo en 2: uno para guardar el contenido de todas las variables de un datasource y otro para guardar el contenido de un datapoint de multiples datasources
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did) or not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    if datapointapi.store_datasource_values(did=did, date=date):
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

