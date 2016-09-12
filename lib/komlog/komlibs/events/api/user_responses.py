'''

Methods for manipulating User Events Responses

'''

import uuid, json
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import events as cassapievents
from komlog.komcass.model.orm import events as ormevents
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.events import exceptions
from komlog.komlibs.events.errors import Errors
from komlog.komlibs.events.model import types

def process_event_response(uid, date, response_data):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRP_IUID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRP_IDT)
    if not args.is_valid_dict(response_data):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRP_IDAT)
    event=cassapievents.get_user_event(uid=uid, date=date)
    if not event:
        raise exceptions.EventNotFoundException(error=Errors.E_EAUR_PEVRP_EVNF)
    else:
        if event.type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
            return _process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        else:
            return False

def _process_event_response_user_event_intervention_datapoint_identification(event, response_data):
    if not isinstance(event, ormevents.UserEventInterventionDatapointIdentification):
        return False
    if not args.is_valid_dict(response_data):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IRD)
    if not 'identified' in response_data or not isinstance(response_data['identified'],list):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IIDP)
    if not 'missing' in response_data or not isinstance(response_data['missing'],list):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IMSP)
    for dp_info in response_data['identified']:
        if not args.is_valid_dict(dp_info):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IIDI)
        if not 'pid' in dp_info or not args.is_valid_hex_uuid(dp_info['pid']):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IDPI)
        if not 'p' in dp_info or not args.is_valid_int(dp_info['p']):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IPI)
        if not 'l' in dp_info or not args.is_valid_int(dp_info['l']):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_ILI)
    for dp in response_data['missing']:
        if not args.is_valid_hex_uuid(dp):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IMSI)
    did=event.did
    ds_date=event.ds_date
    datasource_config=datasourceapi.get_datasource_config(did=did, pids_flag=True)
    now=timeuuid.uuid1()
    processing_result={'missing':set(), 'identified':dict(), 'dp_to_update':set(),'dp_not_belonging':set(),'dp_updated_failed':set(), 'dp_updated_successfully':set()}
    for dp in response_data['missing']:
        pid=uuid.UUID(dp)
        processing_result['missing'].add(pid)
        if pid in datasource_config['pids']:
            mark_result=datapointapi.mark_missing_datapoint(pid=pid, date=ds_date)
            for pid in mark_result['dtree_gen_success']:
                processing_result['dp_to_update'].add(pid)
            for pid in mark_result['dtree_gen_failed']:
                processing_result['dp_updated_failed'].add(pid)
        else:
            processing_result['dp_not_belonging'].add(pid)
    for dp_info in response_data['identified']:
        pid=uuid.UUID(dp_info['pid'])
        p=dp_info['p']
        l=dp_info['l']
        processing_result['identified'][pid]=p
        if pid in datasource_config['pids']:
            mark_result=datapointapi.mark_positive_variable(pid=pid, date=ds_date, position=p, length=l)
            for pid in mark_result['dtree_gen_success']:
                processing_result['dp_to_update'].add(pid)
            for pid in mark_result['dtree_gen_failed']:
                processing_result['dp_updated_failed'].add(pid)
        else:
            processing_result['dp_not_belonging'].add(pid)
    for pid in processing_result['dp_to_update']:
        if datapointapi.store_datapoint_values(pid=pid, date=ds_date):
            processing_result['dp_updated_successfully'].add(pid)
    event_response=ormevents.UserEventResponseInterventionDatapointIdentification(
        uid=event.uid,
        date=event.date,
        response_date=now,
        missing=processing_result['missing'],
        identified=processing_result['identified'],
        not_belonging=processing_result['dp_not_belonging'],
        to_update=processing_result['dp_to_update'],
        update_failed=processing_result['dp_updated_failed'],
        update_success=processing_result['dp_updated_successfully'])
    try:
        if cassapievents.insert_user_event_response(response=event_response):
            return True
        else:
            return False
    except cassexcept.KomcassException:
        cassapievents.delete_user_event_response(event_response)
        raise

