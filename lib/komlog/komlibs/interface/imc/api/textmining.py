'''
Textmining message definitions

'''

import json
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.imc import status, exceptions

@exceptions.ExceptionHandler
def process_message_GDTREE(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
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
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_MAPVARS_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_MAPVARS_IDT)
    if datasourceapi.generate_datasource_map(did=did, date=date):
        newmsg=messages.FillDatasourceMessage(did=did,date=date)
        response.add_message(newmsg)
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IAATM_MAPVARS_EGDSM
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_FILLDP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
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
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    did=message.did
    date=message.date
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_FILLDS_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_FILLDS_IDT)
    store_info=datapointapi.store_datasource_values(did=did, date=date)
    if store_info:
        response.status=status.IMC_STATUS_OK
        if len(store_info['dp_not_found'])>0:
            response.add_message(messages.MissingDatapointMessage(did=did,date=date))
        if len(store_info['dp_found'])>0:
            uris=[]
            for dp in store_info['dp_found']:
                uris.append({'type':vertex.DATAPOINT,'id':dp['pid'],'uri':dp['uri']})
            response.add_message(messages.UrisUpdatedMessage(uris=uris,date=date))
    else:
        response.error=Errors.E_IAATM_FILLDS_ESDSV
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_GENTEXTSUMMARY(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
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

@exceptions.ExceptionHandler
def process_message_ADTREE(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    result = datapointapi.get_datapoint_controversial_samples(pid=message.pid)
    if 'controversial_samples' in result and len(result['controversial_samples'])>0:
        params={'pid':message.pid.hex, 'did':result['did'].hex, 'dates':[date.hex for date in result['controversial_samples']]}
        msg=messages.UserEventMessage(uid=result['uid'], event_type=eventstypes.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, parameters=params)
        response.add_message(msg)
    response.status=status.IMC_STATUS_OK
    return response

