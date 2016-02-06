'''

Methods for manipulating User Events

'''

from komfig import logger
import uuid
from komcass.api import events as cassapievents
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import circle as cassapicircle
from komcass.api import snapshot as cassapisnapshot
from komcass.api import ticket as cassapiticket
from komcass.model.orm import events as ormevents
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.events import errors, exceptions
from komlibs.events.api import summary
from komlibs.events.model import types, priorities, templates

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

def get_events(uid, to_date=None, from_date=None, count=30, params_serializable=False, html_content=False):
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
        event_data=_get_event_data(event, params_serializable=params_serializable, html_content=html_content)
        if event_data:
            data.append(event_data)
    return data

def _get_event_data(event, params_serializable=False, html_content=False):
    if not isinstance(event, ormevents.UserEvent):
        return None
    else:
        try:
            event_data=get_event_data_funcs[event.type](event, params_serializable)
        except Exception:
            raise exceptions.EventNotFoundException(error=errors.E_EAU_GEVD_EVNF)
        else:
            if html_content and params_serializable:
                event_data['html']=_get_event_html_template(event_type=event.type, parameters=event_data['parameters'])
                event_data['summary']=summary.get_user_event_graph_summary_data(uid=event.uid, date=event.date)
            return event_data

def _get_event_data_notification_new_user(event,params_serializable):
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'username':event.username}}
    return event_data

def _get_event_data_notification_new_agent(event,params_serializable):
    aid=event.aid.hex if params_serializable else event.aid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'aid':aid, 'agentname':event.agentname}}
    return event_data

def _get_event_data_notification_new_datasource(event,params_serializable):
    aid=event.aid.hex if params_serializable else event.aid
    did=event.did.hex if params_serializable else event.did
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'aid':aid, 'did':did, 'datasourcename':event.datasourcename}}
    return event_data

def _get_event_data_notification_new_datapoint(event, params_serializable):
    did=event.did.hex if params_serializable else event.did
    pid=event.pid.hex if params_serializable else event.pid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'did':did, 'pid':pid, 'datasourcename':event.datasourcename, 'datapointname':event.datapointname}}
    return event_data

def _get_event_data_notification_new_widget(event, params_serializable):
    wid=event.wid.hex if params_serializable else event.wid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'wid':wid, 'widgetname':event.widgetname}}
    return event_data

def _get_event_data_notification_new_dashboard(event, params_serializable):
    bid=event.bid.hex if params_serializable else event.bid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'bid':bid, 'dashboardname':event.dashboardname}}
    return event_data

def _get_event_data_notification_new_circle(event, params_serializable):
    cid=event.cid.hex if params_serializable else event.cid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'cid':cid, 'circlename':event.circlename}}
    return event_data

def _get_event_data_intervention_datapoint_identification(event, params_serializable):
    did=event.did.hex if params_serializable else event.did
    ds_seq=timeuuid.get_custom_sequence(event.ds_date)
    doubts=[pid.hex for pid in event.doubts] if params_serializable else [pid for pid in event.doubts]
    discarded=[pid.hex for pid in event.discarded] if params_serializable else [pid for pid in event.discarded]
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'did':did, 'ds_seq':ds_seq, 'doubts':doubts, 'discarded':discarded}}
    return event_data

def _get_event_data_notification_new_snapshot_shared(event, params_serializable):
    nid=event.nid.hex if params_serializable else event.nid
    tid=event.tid.hex if params_serializable else event.tid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'nid':nid, 'tid':tid, 'widgetname':event.widgetname}}
    return event_data

def _get_event_data_notification_new_snapshot_shared_with_me(event, params_serializable):
    nid=event.nid.hex if params_serializable else event.nid
    tid=event.tid.hex if params_serializable else event.tid
    event_data={'uid':event.uid, 'date':event.date, 'type':event.type, 'priority':event.priority, 'parameters':{'nid':nid, 'tid':tid, 'widgetname':event.widgetname, 'username':event.username}}
    return event_data

def _get_event_html_template(event_type, parameters):
    if event_type in templates.HTML_TEMPLATES:
        title=templates.HTML_TITLE_TEMPLATES[event_type].render(parameters=parameters)
        body=templates.HTML_BODY_TEMPLATES[event_type].render(parameters=parameters)
        return {'title':title,'body':body}
    else:
        return {}

def enable_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_ENE_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_ENE_ID)
    event=cassapievents.get_disabled_user_event(uid=uid, date=date)
    if event:
        return cassapievents.enable_user_event(event=event)
    else:
        event=cassapievents.get_user_event(uid=uid, date=date)
        if event:
            return True
        else:
            raise exceptions.EventNotFoundException(error=errors.E_EAU_ENE_EVNF)

def disable_event(uid, date):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_DISE_IU)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=errors.E_EAU_DISE_ID)
    event=cassapievents.get_user_event(uid=uid, date=date)
    if event:
        return cassapievents.disable_user_event(event=event)
    else:
        event=cassapievents.get_disabled_user_event(uid=uid, date=date)
        if event:
            return True
        else:
            raise exceptions.EventNotFoundException(error=errors.E_EAU_DISE_EVNF)

def delete_events(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_DEV_IU)
    return cassapievents.delete_user_events(uid=uid)

def new_event(uid, event_type, parameters):
    if not event_type or not args.is_valid_int(event_type):
        raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_IEVT)
    try:
        return insert_event_funcs[event_type](uid=uid, parameters=parameters)
    except KeyError:
        raise exceptions.BadParametersException(error=errors.E_EAU_NEWE_EVTNF)

def _insert_event_notification_new_user(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNU_IU)
    now=timeuuid.uuid1()
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNU_UNF)
    event=ormevents.UserEventNotificationNewUser(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_USER, username=user.username)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNU_DBIE)

def _insert_event_notification_new_agent(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNA_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNA_IP)
    if not 'aid' in parameters or not args.is_valid_hex_uuid(parameters['aid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNA_IPAID)
    now=timeuuid.uuid1()
    aid=uuid.UUID(parameters['aid'])
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNA_UNF)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNA_ANF)
    event=ormevents.UserEventNotificationNewAgent(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_AGENT, aid=aid, agentname=agent.agentname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNA_DBIE)

def _insert_event_notification_new_datasource(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDS_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDS_IP)
    if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDS_IPDID)
    now=timeuuid.uuid1()
    did=uuid.UUID(parameters['did'])
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDS_UNF)
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDS_DNF)
    event=ormevents.UserEventNotificationNewDatasource(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, aid=datasource.aid, did=did, datasourcename=datasource.datasourcename)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDS_DBIE)

def _insert_event_notification_new_datapoint(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDP_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDP_IP)
    if not 'pid' in parameters or not args.is_valid_hex_uuid(parameters['pid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDP_IPPID)
    now=timeuuid.uuid1()
    pid=uuid.UUID(parameters['pid'])
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDP_UNF)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDP_PNF)
    datasource=cassapidatasource.get_datasource(did=datapoint.did)
    if not datasource:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDP_DNF)
    event=ormevents.UserEventNotificationNewDatapoint(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_DATAPOINT, did=datapoint.did, pid=pid, datasourcename=datasource.datasourcename, datapointname=datapoint.datapointname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDP_DBIE)

def _insert_event_notification_new_widget(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNWG_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNWG_IP)
    if not 'wid' in parameters or not args.is_valid_hex_uuid(parameters['wid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNWG_IPWID)
    now=timeuuid.uuid1()
    wid=uuid.UUID(parameters['wid'])
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNWG_UNF)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNWG_WNF)
    event=ormevents.UserEventNotificationNewWidget(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_WIDGET, wid=wid, widgetname=widget.widgetname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNWG_DBIE)

def _insert_event_notification_new_dashboard(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDB_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDB_IP)
    if not 'bid' in parameters or not args.is_valid_hex_uuid(parameters['bid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNDB_IPBID)
    now=timeuuid.uuid1()
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDB_UNF)
    bid=uuid.UUID(parameters['bid'])
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDB_BNF)
    event=ormevents.UserEventNotificationNewDashboard(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_DASHBOARD, bid=bid, dashboardname=dashboard.dashboardname)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNDB_DBIE)

def _insert_event_notification_new_circle(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNC_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNC_IP)
    if not 'cid' in parameters or not args.is_valid_hex_uuid(parameters['cid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNC_IPCID)
    now=timeuuid.uuid1()
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNC_UNF)
    cid=uuid.UUID(parameters['cid'])
    circle=cassapicircle.get_circle(cid=cid)
    if not circle:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNC_CNF)
    event=ormevents.UserEventNotificationNewCircle(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_CIRCLE, cid=cid, circlename=circle.circlename)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNC_DBIE)

def _insert_event_intervention_datapoint_identification(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IUID)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IP)
    if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IPDID)
    if not 'date' in parameters or not args.is_valid_hex_date(parameters['date']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IPDATE)
    if not 'doubts' in parameters or not isinstance(parameters['doubts'],list):
        raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IPDBT)
    if not 'discarded' in parameters or not isinstance(parameters['discarded'],list):
        raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IPDISC)
    for pid in parameters['doubts']:
        if not args.is_valid_hex_uuid(pid):
            raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IIDBT)
    for pid in parameters['discarded']:
        if not args.is_valid_hex_uuid(pid):
            raise exceptions.BadParametersException(error=errors.E_EAU_IEIDPI_IIDISC)
    now=timeuuid.uuid1()
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IEIDPI_UNF)
    did=uuid.UUID(parameters['did'])
    ds_date=uuid.UUID(parameters['date'])
    datasource_map=cassapidatasource.get_datasource_map(did=did, date=ds_date)
    if not datasource_map:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IEIDPI_DNF)
    doubts=[uuid.UUID(pid) for pid in parameters['doubts']]
    discarded=[uuid.UUID(pid) for pid in parameters['discarded']]
    event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=priorities.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, did=did, ds_date=ds_date, doubts=doubts, discarded=discarded)
    if cassapievents.insert_user_event(event):
        return {'uid':uid, 'date':now}
    else:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IEIDPI_DBIE)

def _insert_event_notification_new_snapshot_shared(uid, parameters):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNSS_IU)
    if not args.is_valid_dict(parameters):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNSS_IP)
    if not 'nid' in parameters or not args.is_valid_hex_uuid(parameters['nid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNSS_IPNID)
    if not 'tid' in parameters or not args.is_valid_hex_uuid(parameters['tid']):
        raise exceptions.BadParametersException(error=errors.E_EAU_IENNSS_IPTID)
    now=timeuuid.uuid1()
    nid=uuid.UUID(parameters['nid'])
    tid=uuid.UUID(parameters['tid'])
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNSS_UNF)
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNSS_NNF)
    ticket=cassapiticket.get_ticket(tid=tid)
    if not ticket:
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNSS_TNF)
    shared_uids=set()
    users_info={}
    circles_info={}
    for shared_uid in ticket.allowed_uids:
        shared_user=cassapiuser.get_user(uid=shared_uid)
        if shared_user:
            shared_uids.add(shared_user.uid)
            users_info[shared_user.uid]=shared_user.username
    for shared_cid in ticket.allowed_cids:
        shared_circle=cassapicircle.get_circle(cid=shared_cid)
        if shared_circle:
            for shared_uid in shared_circle.members:
                shared_user=cassapiuser.get_user(uid=shared_uid)
                if shared_user:
                    shared_uids.add(shared_user.uid)
            circles_info[shared_circle.cid]=shared_circle.circlename
    shared_event=ormevents.UserEventNotificationNewSnapshotShared(uid=user.uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED, widgetname=snapshot.widgetname, nid=snapshot.nid, tid=ticket.tid, shared_with_users=users_info, shared_with_circles=circles_info)
    summary_data=summary.generate_user_event_graph_summary_data(event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED, parameters=parameters)
    op_failed=False
    if cassapievents.insert_user_event(shared_event):
        graph_summary=ormevents.UserEventGraphSummary(uid=user.uid, date=now, summary=summary_data)
        cassapievents.insert_user_event_graph_summary(graph_summary)
        insert_events=[]
        for uid in shared_uids:
            event=ormevents.UserEventNotificationNewSnapshotSharedWithMe(uid=uid, date=now, priority=priorities.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME, username=user.username, widgetname=snapshot.widgetname, nid=snapshot.nid, tid=ticket.tid)
            if not cassapievents.insert_user_event(event):
                op_failed=True
                break
            else:
                graph_summary=ormevents.UserEventGraphSummary(uid=uid, date=now, summary=summary_data)
                cassapievents.insert_user_event_graph_summary(graph_summary)
                insert_events.append(event)
        if op_failed:
            for event in insert_events:
                cassapievents.delete_user_event(event=event)
                cassapievents.delete_user_event_graph_summary(uid=event.uid, date=event.date)
    if op_failed:
        cassapievents.delete_user_event(event=shared_event)
        cassapievents.delete_user_event_graph_summary(uid=shared_event.uid, date=shared_event.date)
        raise exceptions.UserEventCreationException(error=errors.E_EAU_IENNSS_DBPIE)
    else:
        return {'uid':uid, 'date':now}


## association functions

get_event_data_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:_get_event_data_notification_new_user,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:_get_event_data_notification_new_agent,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:_get_event_data_notification_new_datasource,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:_get_event_data_notification_new_datapoint,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:_get_event_data_notification_new_widget,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:_get_event_data_notification_new_dashboard,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:_get_event_data_notification_new_circle,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_get_event_data_notification_new_snapshot_shared,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:_get_event_data_notification_new_snapshot_shared_with_me,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_get_event_data_intervention_datapoint_identification,
}

insert_event_funcs = {
    types.USER_EVENT_NOTIFICATION_NEW_USER:_insert_event_notification_new_user,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:_insert_event_notification_new_agent,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:_insert_event_notification_new_datasource,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:_insert_event_notification_new_datapoint,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:_insert_event_notification_new_widget,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:_insert_event_notification_new_dashboard,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:_insert_event_notification_new_circle,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:_insert_event_notification_new_snapshot_shared,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:_insert_event_intervention_datapoint_identification,
}

