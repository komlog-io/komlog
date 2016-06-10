#coding: utf-8
'''
Textmining message definitions

'''

import json
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
        raise exceptions.BadParametersException(error=Errors.E_IAATM_GDTREE_IP)
    if datapointapi.generate_decision_tree(pid=pid):
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IAATM_GDTREE_EGDT
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_MAPVARS(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_MAPVARS_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_MAPVARS_IDT)
    if datasourceapi.generate_datasource_map(did=did, date=date):
        newmsg=messages.FillDatasourceMessage(did=did,date=date)
        response.add_msg_originated(newmsg)
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IAATM_MAPVARS_EGDSM
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_FILLDP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    pid=message.pid
    date=message.date
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_FILLDP_IPID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_FILLDP_IDT)
    if datapointapi.store_datapoint_values(pid=pid, date=date):
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IAATM_FILLDP_ESDPV
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_FILLDS(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_FILLDS_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_FILLDS_IDT)
    store_info=datapointapi.store_datasource_values(did=did, date=date)
    if store_info:
        response.status=status.IMC_STATUS_OK
        if isinstance(store_info,dict) and 'dp_not_found' in store_info and len(store_info['dp_not_found'])>0:
            response.add_msg_originated(messages.MissingDatapointMessage(did=did,date=date))
    else:
        response.error=Errors.E_IAATM_FILLDS_ESDSV
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_GENTEXTSUMMARY(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IAAATM_GTXS_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_IAAATM_GTXS_IDT)
    if datapointapi.generate_datasource_text_summary(did=did, date=date):
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IAATM_GTXS_EGDSTXS
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

