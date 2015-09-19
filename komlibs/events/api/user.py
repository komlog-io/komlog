'''

Methods for manipulating User Events

'''

from komfig import logger
import uuid, json
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.events import errors, exceptions
from komlibs.events.model import types, priorities, templates
from komcass.model.orm import events as ormevents
from komcass.api import events as cassapievents

def get_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEV_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEV_IDT)
    event=cassapievents.get_user_event(uid=uid, date=date)
    if not event:
        raise exceptions.EventNotFoundException(error=errors.E_EAU_GEV_EVNF)
    else:
        return _get_event_data(event)

def get_events(uid, to_date=None, from_date=None, count=30, params_serializable=False, html_literal=False):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_IU)
    if to_date and not args.is_valid_date(to_date):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_ITD)
    if from_date and not args.is_valid_date(from_date):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_IFD)
    if not args.is_valid_int(count):
        raise exceptions.BadParametersException(error=errors.E_EAU_GEVS_ICNT)
    if not to_date and not from_date:
        to_date=timeuuid.uuid1()
        events=cassapievents.get_user_events(uid=uid, end_date=to_date, count=count)
    elif to_date and from_date:
        events=cassapievents.get_user_events(uid=uid, to_date=to_date, from_date=from_date)
    elif to_date:
        events=cassapievents.get_user_events(uid=uid, end_date=to_date, count=count)
    else:
        events=cassapievents.get_user_events(uid=uid, from_date=from_date)
    data=[]
    for event in events:
        event_data=_get_event_data(event, params_serializable=params_serializable, html_literal=html_literal)
        if event_data:
            data.append(event_data)
    return data

def _get_event_data(event, params_serializable=False, html_literal=False):
    if not isinstance(event, ormevents.UserEvent):
        return None
    else:
        if event.type==types.USER_EVENT_NOTIFICATION_NEW_USER:
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'username':event.username}}
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_AGENT:
            aid=event.aid.hex if params_serializable else event.aid
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'aid':aid, 'agentname':event.agentname}}
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:
            aid=event.aid.hex if params_serializable else event.aid
            did=event.did.hex if params_serializable else event.did
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'aid':aid, 'did':did, 'datasourcename':event.datasourcename}}
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:
            did=event.did.hex if params_serializable else event.did
            pid=event.pid.hex if params_serializable else event.pid
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'did':did, 'pid':pid, 'datasourcename':event.datasourcename, 'datapointname':event.datapointname}}
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_WIDGET:
            wid=event.wid.hex if params_serializable else event.wid
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'wid':wid, 'widgetname':event.widgetname}}
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:
            bid=event.bid.hex if params_serializable else event.bid
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'bid':bid, 'dashboardname':event.dashboardname}}
        elif event.type==types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:
            cid=event.cid.hex if params_serializable else event.cid
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'cid':cid, 'circlename':event.circlename}}
        elif event.type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
            did=event.did.hex if params_serializable else event.did
            ds_seq=timeuuid.get_custom_sequence(event.ds_date)
            doubts=[pid.hex for pid in event.doubts] if params_serializable else event.doubts
            discarded=[pid.hex for pid in event.discarded] if params_serializable else event.discarded
            event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'did':did, 'ds_seq':ds_seq, 'doubts':doubts, 'discarded':discarded}}
        else:
            return None
        if html_literal and params_serializable:
            event_data['html']=_get_event_html_template(event_type=event.type, parameters=event_data['parameters'])
        return event_data

def _get_event_html_template(event_type, parameters):
    if event_type in templates.HTML_TEMPLATES:
        return templates.HTML_TEMPLATES[event_type].render(parameters=parameters)
    else:
        return ''


def enable_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_ACE_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_ACE_ID)
    event=cassapievents.get_disabled_user_event(uid=uid, date=date)
    if event:
        return cassapievents.enable_user_event(event=event)
    else:
        event=cassapievents.get_user_event(uid=uid, date=date)
        if event:
            return True
        else:
            raise exceptions.EventNotFoundException(error=errors.E_EAU_ACE_EVNF)

def disable_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_DACE_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_DACE_ID)
    event=cassapievents.get_user_event(uid=uid, date=date)
    if event:
        return cassapievents.disable_user_event(event=event)
    else:
        event=cassapievents.get_disabled_user_event(uid=uid, date=date)
        if event:
            return True
        else:
            raise exceptions.EventNotFoundException(error=errors.E_EAU_DACE_EVNF)

def delete_events(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_DEV_IU)
    return cassapievents.delete_user_events(uid=uid)

def new_event(uid, event_type, parameters):
    if not event_type or not args.is_valid_int(event_type):
        raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_IEVT)
    if event_type==types.USER_EVENT_NOTIFICATION_NEW_USER:
        if not 'username' in parameters or not args.is_valid_username(parameters['username']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NUIU)
        username=parameters['username']
        return insert_new_user_event(uid=uid, username=username)
    elif event_type==types.USER_EVENT_NOTIFICATION_NEW_AGENT:
        if not 'aid' in parameters or not args.is_valid_hex_uuid(parameters['aid']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NAID)
        if not 'agentname' in parameters or not args.is_valid_agentname(parameters['agentname']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NAIA)
        aid=uuid.UUID(parameters['aid'])
        agentname=parameters['agentname']
        return insert_new_agent_event(uid=uid, aid=aid, agentname=agentname)
    elif event_type==types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:
        if not 'aid' in parameters or not args.is_valid_hex_uuid(parameters['aid']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NDIA)
        if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NDID)
        if not 'datasourcename' in parameters or not args.is_valid_datasourcename(parameters['datasourcename']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NDIN)
        aid=uuid.UUID(parameters['aid'])
        did=uuid.UUID(parameters['did'])
        datasourcename=parameters['datasourcename']
        return insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename)
    elif event_type==types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:
        if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NPID)
        if not 'pid' in parameters or not args.is_valid_hex_uuid(parameters['pid']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NPIP)
        if not 'datasourcename' in parameters or not args.is_valid_datasourcename(parameters['datasourcename']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NPIN)
        if not 'datapointname' in parameters or not args.is_valid_datapointname(parameters['datapointname']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NPIM)
        did=uuid.UUID(parameters['did'])
        pid=uuid.UUID(parameters['pid'])
        datasourcename=parameters['datasourcename']
        datapointname=parameters['datapointname']
        return insert_new_datapoint_event(uid=uid, did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname)
    elif event_type==types.USER_EVENT_NOTIFICATION_NEW_WIDGET:
        if not 'wid' in parameters or not args.is_valid_hex_uuid(parameters['wid']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NWIW)
        if not 'widgetname' in parameters or not args.is_valid_widgetname(parameters['widgetname']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NWIN)
        wid=uuid.UUID(parameters['wid'])
        widgetname=parameters['widgetname']
        return insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname)
    elif event_type==types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:
        if not 'bid' in parameters or not args.is_valid_hex_uuid(parameters['bid']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NBIB)
        if not 'dashboardname' in parameters or not args.is_valid_dashboardname(parameters['dashboardname']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NBIN)
        bid=uuid.UUID(parameters['bid'])
        dashboardname=parameters['dashboardname']
        return insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname)
    elif event_type==types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:
        if not 'cid' in parameters or not args.is_valid_hex_uuid(parameters['cid']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NCIC)
        if not 'circlename' in parameters or not args.is_valid_circlename(parameters['circlename']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_NCIN)
        cid=uuid.UUID(parameters['cid'])
        circlename=parameters['circlename']
        return insert_new_circle_event(uid=uid, cid=cid, circlename=circlename)
    elif event_type==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
        if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_UIDIID)
        if not 'date' in parameters or not args.is_valid_hex_date(parameters['date']):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_UIDIIDT)
        if not 'doubts' in parameters or not isinstance(parameters['doubts'],list):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_UIDIIDO)
        if not 'discarded' in parameters or not isinstance(parameters['discarded'],list):
            raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_UIDIIDI)
        for pid in parameters['doubts']:
            if not args.is_valid_hex_uuid(pid):
                raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_UIDIIDOP)
        for pid in parameters['discarded']:
            if not args.is_valid_hex_uuid(pid):
                raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_UIDIIDIP)
        did=uuid.UUID(parameters['did'])
        ds_date=uuid.UUID(parameters['date'])
        doubts=[uuid.UUID(pid) for pid in parameters['doubts']]
        discarded=[uuid.UUID(pid) for pid in parameters['discarded']]
        return insert_event_user_intervention_datapoint_identification(uid=uid, did=did, ds_date=ds_date, doubts=doubts, discarded=discarded)
    else:
        raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_EVTNF)

def insert_new_user_event(uid, username):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INUE_IU)
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_EAU_INUE_IUS)
    now=timeuuid.uuid1()
    event=ormevents.UserEventNotificationNewUser(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_USER, username=username)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

def insert_new_agent_event(uid, aid, agentname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INAE_IU)
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INAE_IA)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INAE_IAN)
    now=timeuuid.uuid1()
    event=ormevents.UserEventNotificationNewAgent(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_AGENT, aid=aid, agentname=agentname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

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
    event=ormevents.UserEventNotificationNewDatasource(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, aid=aid, did=did, datasourcename=datasourcename)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

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
    event=ormevents.UserEventNotificationNewDatapoint(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_DATAPOINT, did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

def insert_new_widget_event(uid, wid, widgetname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INWGE_IU)
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INWGE_IWID)
    if not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INWGE_IWN)
    now=timeuuid.uuid1()
    event=ormevents.UserEventNotificationNewWidget(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_WIDGET, wid=wid, widgetname=widgetname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

def insert_new_dashboard_event(uid, bid, dashboardname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDBE_IU)
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDBE_IBID)
    if not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException(error=errors.E_EAU_INDBE_IDBN)
    now=timeuuid.uuid1()
    event=ormevents.UserEventNotificationNewDashboard(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_DASHBOARD, bid=bid, dashboardname=dashboardname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

def insert_new_circle_event(uid, cid, circlename):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INCE_IU)
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INCE_ICID)
    if not args.is_valid_circlename(circlename):
        raise exceptions.BadParametersException(error=errors.E_EAU_INCE_ICN)
    now=timeuuid.uuid1()
    event=ormevents.UserEventNotificationNewCircle(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_CIRCLE, cid=cid, circlename=circlename)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

def insert_event_user_intervention_datapoint_identification(uid, did, ds_date, doubts, discarded):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IUID)
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IDID)
    if not args.is_valid_date(ds_date):
        raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IDT)
    if not isinstance(doubts,list):
        raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IDOU)
    if not isinstance(discarded,list):
        raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IDIS)
    for pid in doubts:
        if not args.is_valid_uuid(pid):
            raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IDOUP)
    for pid in discarded:
        if not args.is_valid_uuid(pid):
            raise exceptions.BadParametersException(error=errors.E_EAU_INEUIDI_IDISP)
    now=timeuuid.uuid1()
    event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=priorities.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, did=did, ds_date=ds_date, doubts=doubts, discarded=discarded)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        return None

