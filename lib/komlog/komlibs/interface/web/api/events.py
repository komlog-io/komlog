'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komfig import logging
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.passport import UserPassport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.api import user as userevents
from komlog.komlibs.events.api import user_responses as userresponsesevents
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_user_events_request(passport, ets=None, its=None):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_GEVR_IPSP)
    if ets and not args.is_valid_string_float(ets):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_GEVR_IETS)
    if its and not args.is_valid_string_float(its):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_GEVR_IITS)
    if its and ets and float(its)>float(ets):
        its,ets=ets,its
    end_date=timeuuid.uuid1(seconds=float(ets)) if ets else None
    init_date=timeuuid.uuid1(seconds=float(its)) if its else None
    authorization.authorize_request(request=Requests.GET_USER_EVENTS,passport=passport)
    events=userevents.get_events(uid=passport.uid, to_date=end_date, from_date=init_date, params_serializable=True, html_content=True)
    response_data=[]
    for event in events:
        reg={}
        reg['ts']=timeuuid.get_unix_timestamp(event['date'])
        reg['type']=event['type']
        reg['priority']=event['priority']
        reg['seq']=timeuuid.get_custom_sequence(event['date'])
        reg['params']=event['parameters']
        reg['html']=event['html']
        if 'summary' in event:
            reg['summary']=event['summary']
        response_data.append(reg)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def disable_event_request(passport, seq):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_DEVR_IPSP)
    if not args.is_valid_sequence(seq):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_DEVR_ISEQ)
    authorization.authorize_request(request=Requests.DISABLE_EVENT,passport=passport)
    date=timeuuid.get_uuid1_from_custom_sequence(seq)
    userevents.disable_event(uid=passport.uid, date=date)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def event_response_request(passport, seq, data):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_EVRPR_IPSP)
    if not args.is_valid_sequence(seq):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_EVRPR_ISEQ)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_EVRPR_IDAT)
    authorization.authorize_request(request=Requests.RESPONSE_EVENT,passport=passport)
    date=timeuuid.get_uuid1_from_custom_sequence(seq)
    event=userevents.get_event(uid=passport.uid, date=date)
    if event['type']==eventstypes.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
        parameters={'identified':[]}
        if not 'identified' in data or not isinstance(data['identified'],list):
            raise exceptions.BadParametersException(error=Errors.E_IWAEV_EVRPR_IIDF)
        for reg in data['identified']:
            if not (isinstance(reg, dict)
                and 'p' in reg
                and 'l' in reg
                and 's' in reg
                and (reg['p'] is None or args.is_valid_int(reg['p']))
                and (reg['l'] is None or args.is_valid_int(reg['l']))
                and args.is_valid_sequence(reg['s'])):
                raise exceptions.BadParametersException(error=Errors.E_IWAEV_EVRPR_IIDIT)
            else:
                parameters['identified'].append({'s':reg['s'],'p':reg['p'],'l':reg['l']})
        resp=response.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
        resp.add_message(messages.UserEventResponseMessage(uid=passport.uid,date=date,parameters=parameters))
        return resp
    else:
        raise exceptions.BadParametersException(error=Errors.E_IWAEV_EVRPR_IEVT)

