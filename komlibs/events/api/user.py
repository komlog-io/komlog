'''

Methods for manipulating User Events

'''

from komfig import logger
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.events import errors, exceptions
from komlibs.events.model import types 
from komlibs.events.model import priorities
from komcass.model.orm import events as ormevents
from komcass.api import events as cassapievents

def get_last_events(uid, to_date=None, count=30):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_IU)
    if to_date and not args.is_valid_date(to_date):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_ITD)
    if not args.is_valid_int(count):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_ICNT)
    if not to_date:
        to_date=timeuuid.uuid1()
    events=cassapievents.get_user_events(uid=uid, end_date=to_date, count=count)
    data=[]
    for event in events:
        data.append({'uid':event.uid, 'date':event.date,'active':event.active, 'type':event.type, 'priority':event.priority, 'parameters':event.parameters})
    return data

def activate_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_ACE_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_ACE_ID)
    return cassapievents.activate_user_event(uid, date)

def deactivate_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_DACE_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_DACE_ID)
    return cassapievents.deactivate_user_event(uid=uid, date=date)

def delete_events(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_DEV_IU)
    return cassapievents.delete_user_events(uid=uid)

def insert_new_user_event(uid, username):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INUE_IU)
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_EAU_INUE_IUS)
    now=timeuuid.uuid1()
    parameters={'username':username}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_USER, active=True, priority=priorities.NEW_USER, parameters=parameters)
    return cassapievents.insert_user_event(event)

def insert_new_agent_event(uid, aid, agentname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INAE_IU)
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INAE_IA)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INAE_IAN)
    now=timeuuid.uuid1()
    parameters={'aid':aid.hex, 'agentname':agentname}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_AGENT, active=True, priority=priorities.NEW_AGENT, parameters=parameters)
    return cassapievents.insert_user_event(event)

def insert_new_datasource_event(uid, aid, did, datasourcename):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDSE_IU)
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDSE_IA)
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDSE_IDID)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDSE_IDSN)
    now=timeuuid.uuid1()
    parameters={'aid':aid.hex, 'did':did.hex, 'datasourcename':datasourcename}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_DATASOURCE, active=True, priority=priorities.NEW_DATASOURCE, parameters=parameters)
    return cassapievents.insert_user_event(event)

def insert_new_datapoint_event(uid, did, pid, datasourcename, datapointname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDPE_IU)
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDPE_IDID)
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDPE_IPID)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDPE_IDSN)
    if not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDPE_IDPN)
    now=timeuuid.uuid1()
    parameters={'did':did.hex, 'pid':pid.hex, 'datasourcename':datasourcename, 'datapointname':datapointname}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_DATAPOINT, active=True, priority=priorities.NEW_DATAPOINT, parameters=parameters)
    return cassapievents.insert_user_event(event)

def insert_new_widget_event(uid, wid, widgetname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INWGE_IU)
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INWGE_IWID)
    if not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INWGE_IWN)
    now=timeuuid.uuid1()
    parameters={'wid':wid.hex, 'widgetname':widgetname}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_WIDGET, active=True, priority=priorities.NEW_WIDGET, parameters=parameters)
    return cassapievents.insert_user_event(event)

def insert_new_dashboard_event(uid, bid, dashboardname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDBE_IU)
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDBE_IBID)
    if not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDBE_IDBN)
    now=timeuuid.uuid1()
    parameters={'bid':bid.hex, 'dashboardname':dashboardname}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_DASHBOARD, active=True, priority=priorities.NEW_DASHBOARD, parameters=parameters)
    return cassapievents.insert_user_event(event)

def insert_new_circle_event(uid, cid, circlename):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INCE_IU)
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INCE_ICID)
    if not args.is_valid_circlename(circlename):
        raise exceptions.BadParametersException(error=errors.E_EAU_INCE_ICN)
    now=timeuuid.uuid1()
    parameters={'cid':cid.hex, 'circlename':circlename}
    event=ormevents.UserEvent(uid=uid, date=now, type=types.NEW_CIRCLE, active=True, priority=priorities.NEW_CIRCLE, parameters=parameters)
    return cassapievents.insert_user_event(event)

