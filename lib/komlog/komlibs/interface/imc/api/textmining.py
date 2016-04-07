#coding: utf-8
'''
Textmining message definitions

'''

import json
from komlog.komfig import logging
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.imc import status, exceptions

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
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did) or not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    store_info=datapointapi.store_datasource_values(did=did, date=date)
    if store_info:
        response.status=status.IMC_STATUS_OK
        if 'dp_not_found' in store_info and len(store_info['dp_not_found'])>0:
            response.add_msg_originated(messages.MissingDatapointMessage(did=did,date=date))
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_GENTEXTSUMMARY(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did) or not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    if datasourceapi.generate_datasource_text_summary(did=did, date=date):
        logging.logger.debug('GENTEXTSUMMARY Success'+str(message.__dict__))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

