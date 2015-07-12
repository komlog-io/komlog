'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komlibs.events.api import user as usereventsapi
from komlibs.gestaccount.user import api as userapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_user_events_request(username, end_date=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_GEVR_IU)
    if end_date and not args.is_valid_string_float(end_date):
        raise exceptions.BadParametersException(error=errors.E_IWAEV_GEVR_IED)
    uid=userapi.get_uid(username=username)
    end_date=timeuuid.uuid1(seconds=float(end_date)) if end_date else None
    events=usereventsapi.get_last_events(uid=uid, to_date=end_date)
    response_data=[]
    for event in events:
        #event_literal=eventsliteral.get_html_literal(type=event.type, parameters=event.parameters)
        response_data.append({'ts':timeuuid.get_unix_timestamp(event['date']),'type':event['type'], 'priority':event['priority'],'seq':timeuuid.get_custom_sequence(event['date']),'params':event['parameters']})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

