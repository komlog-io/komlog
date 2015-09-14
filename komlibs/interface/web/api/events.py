'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komlibs.events.api import user as userevents
from komlibs.gestaccount.user import api as userapi
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

