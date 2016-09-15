'''

Methods for manipulating User Events Responses

'''

import uuid, json
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import events as cassapievents
from komlog.komcass.model.orm import events as ormevents
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount import exceptions as gestexcept
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
    event=cassapievents.get_user_event(uid=uid, date=date)
    if not event:
        raise exceptions.EventNotFoundException(error=Errors.E_EAUR_PEVRP_EVNF)
    else:
        if event.type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
            return _process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        else:
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRP_IEVT)

def _process_event_response_user_event_intervention_datapoint_identification(event, response_data):
    if not isinstance(event, ormevents.UserEventInterventionDatapointIdentification):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IEVT)
    if not args.is_valid_dict(response_data):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IRD)
    if not 'identified' in response_data:
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IDFNF)
    if not isinstance(response_data['identified'],list):
        raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IDFTI)
    for reg in response_data['identified']:
        if not args.is_valid_dict(reg):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IIDI)
        if not 's' in reg or not args.is_valid_sequence(reg['s']):
            raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_ISEQI)
        if 'p' in reg and 'l' in reg and reg['p'] is None and reg['l'] is None:
            pass
        else:
            if not 'p' in reg or not args.is_valid_int(reg['p']):
                raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_IPI)
            if not 'l' in reg or not args.is_valid_int(reg['l']):
                raise exceptions.BadParametersException(error=Errors.E_EAUR_PEVRPUEIDI_ILI)
    now=timeuuid.uuid1()
    pid=event.pid
    processing_result={'dtree_gen_success':[],'dtree_gen_failed':[],'mark_failed':[]}
    response={
        'type':types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION,
        'dtree_gen_success':[],
        'dtree_gen_failed':[],
        'mark_failed':[]
    }
    pending_dtree_updates=set()
    for reg in response_data['identified']:
        try:
            ds_date=timeuuid.get_uuid1_from_custom_sequence(reg['s'])
            if reg['p'] is None and reg['l'] is None:
                mark_result=datapointapi.mark_missing_datapoint(pid=pid, date=ds_date, dtree_update=False)
            else:
                mark_result=datapointapi.mark_positive_variable(pid=pid, date=ds_date, position=reg['p'], length=reg['l'], dtree_update=False)
            for pid in mark_result['dtree_pending']:
                pending_dtree_updates.add(pid)
        except gestexcept.GestaccountException:
            processing_result['mark_failed'].append(reg['s'])
            response['mark_failed'].append(reg['s'])
    for pid in pending_dtree_updates:
        try:
            datapointapi.generate_decision_tree(pid=pid)
            datapointapi.generate_inverse_decision_tree(pid=pid)
        except gestexcept.GestaccountException:
            processing_result['dtree_gen_failed'].append(pid.hex)
            response['dtree_gen_failed'].append(pid)
        else:
            processing_result['dtree_gen_success'].append(pid.hex)
            response['dtree_gen_success'].append(pid)
    event_response=ormevents.UserEventResponseInterventionDatapointIdentification(
        uid=event.uid,
        date=event.date,
        response_date=now,
        data = json.dumps(processing_result))
    cassapievents.insert_user_event_response(response=event_response)
    return response

