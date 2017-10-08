'''
Textmining message definitions

'''

from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.web.model import operation

@exceptions.ExceptionHandler
def process_message_GDTREE(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    did=message.did
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IAATM_GDTREE_IDID)
    if datapointapi.generate_decision_tree(did=did):
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
        response.add_imc_message(newmsg)
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
    result = datapointapi.store_datasource_values(did=did, date=date)
    if result:
        response.status=status.IMC_STATUS_OK
        if result['has_dtree'] == False:
            # ds has no associated dtree
            response.add_imc_message(messages.AssociateExistingDTreeMessage(did=message.did))
        elif result['dp_found']:
            if result['non_dp_uris']:
                response.add_imc_message(messages.MonitorIdentifiedUris(did=message.did, date=message.date))
            # dtree has identified some dps in this sample
            uris=[]
            for dp in result['dp_found']:
                uris.append({'type':vertex.DATAPOINT,'id':dp['pid'],'uri':dp['uri']})
            response.add_imc_message(messages.UrisUpdatedMessage(uris=uris,date=date))
        elif result['non_dp_uris']:
            # dtree has not identified any dp, but has identified uris not monitored yet.
            response.add_imc_message(messages.MonitorIdentifiedUris(did=message.did, date=message.date))
        elif not result['dp_missing']:
            # dtree has not identified any dp, any uri missing, and any dp is pending for identification.
            # we try to select another dtree for this ds (This operations has a max frec configured internally)
            response.add_imc_message(messages.AssociateExistingDTreeMessage(did=message.did))
    else:
        response.error=Errors.E_IAATM_FILLDS_ESDSV
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

@exceptions.ExceptionHandler
def process_message_AEDTREE(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_OK, message_type=message._type_, message_params=message.to_serialization())
    result = datapointapi.select_dtree_for_datasource(message.did)
    if result['dtree'] != None:
        response.add_imc_message(messages.MonitorIdentifiedUrisMessage(did=message.did))
    response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_DSFEATUPD(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_OK, message_type=message._type_, message_params=message.to_serialization())
    result = datasourceapi.update_datasource_features(message.did)
    response.status = status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_MONIDU(message):
    ''' Processing function for message MONITOR_IDENTIFIED_URIS_MESSAGE '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_OK, message_type=message._type_, message_params=message.to_serialization())
    result = datapointapi.monitor_identified_uris(message.did, message.date)
    uris = []
    uid = None
    for dp in result['monitored']:
        webop=operation.NewDatasourceDatapointOperation(uid=dp['uid'],aid=dp['aid'],did=dp['did'],pid=dp['pid'])
        authop=webop.get_auth_operation()
        params=webop.get_params()
        response.add_imc_message(messages.UpdateQuotesMessage(operation=authop, params=params))
        response.add_imc_message(messages.ResourceAuthorizationUpdateMessage(operation=authop, params=params))
        if dp['previously_existed'] == False:
            response.add_imc_message(messages.NewDPWidgetMessage(uid=dp['uid'],pid=dp['pid']))
            uris.append({'type':vertex.DATAPOINT, 'id':dp['pid'], 'uri':dp['uri']})
            uid = uid if uid else dp['uid']
    if uris:
        response.add_imc_message(messages.HookNewUrisMessage(uid=uid, uris=uris, date=result['sample_date']))
    response.status = status.IMC_STATUS_OK
    return response

