'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.events.api import user as userevents
from komlibs.events.api import user_responses as userresponsesevents
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.user import api as userapi
from komlibs.interface.imc.model import messages
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_user_events_request(username, ets=None, its=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_GEVR_IU)
    if ets and not args.is_valid_string_float(ets):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_GEVR_IETS)
    if its and not args.is_valid_string_float(its):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_GEVR_IITS)
    uid=userapi.get_uid(username=username)
    end_date=timeuuid.uuid1(seconds=float(ets)) if ets else None
    init_date=timeuuid.uuid1(seconds=float(its)) if its else None
    logger.logger.debug('vamos a obtener eventos')
    events=userevents.get_events(uid=uid, to_date=end_date, from_date=init_date, params_serializable=True, html_literal=True)
    response_data=[]
    for event in events:
        reg={}
        reg['ts']=timeuuid.get_unix_timestamp(event['date'])
        reg['type']=event['type']
        reg['priority']=event['priority']
        reg['seq']=timeuuid.get_custom_sequence(event['date'])
        reg['params']=event['parameters']
        reg['html']=event['html']
        response_data.append(reg)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def disable_event_request(username, seq):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_DEVR_IU)
    if not args.is_valid_sequence(seq):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_DEVR_ISEQ)
    uid=userapi.get_uid(username=username)
    date=timeuuid.get_uuid1_from_custom_sequence(seq)
    userevents.disable_event(uid=uid, date=date)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def event_response_request(username, seq, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IU)
    if not args.is_valid_sequence(seq):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_ISEQ)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IDAT)
    uid=userapi.get_uid(username=username)
    date=timeuuid.get_uuid1_from_custom_sequence(seq)
    event=userevents.get_event(uid=uid, date=date)
    if event['type']==eventstypes.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
        parameters={'missing':[],'identified':[]}
        if not 'missing' in data or not isinstance(data['missing'],list):
            raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IMSF)
        if not 'identified' in data or not isinstance(data['identified'],list):
            raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IIDF)
        for dp in data['missing']:
            if not args.is_valid_hex_uuid(dp):
                raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IMSIT)
            else:
                parameters['missing'].append(dp)
        for dp_info in data['identified']:
            if not isinstance(dp_info, dict) or not 'pid' in dp_info \
                or not 'p' in dp_info or not 'l' in dp_info \
                or not args.is_valid_hex_uuid(dp_info['pid']) \
                or not args.is_valid_int(dp_info['p']) \
                or not args.is_valid_int(dp_info['l']):
                raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IIDIT)
            else:
                parameters['identified'].append({'pid':dp_info['pid'],'p':dp_info['p'],'l':dp_info['l']})
        message=messages.UserEventResponseMessage(uid=uid, date=date, parameters=parameters)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException(error=errors.E_IWAEV_EVRPR_IEVT)

