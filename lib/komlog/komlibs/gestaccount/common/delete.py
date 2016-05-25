'''

This file implement delete operations of gestaccount elements.


'''

from komlog.komfig import logging
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import events as cassapievents
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import ticket as cassapiticket
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.widget import types as widgettypes
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.api import kin as graphkin

def delete_user(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DU_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GCD_DU_UNF)
    aids=cassapiagent.get_agents_aids(uid=uid)
    dids=cassapidatasource.get_datasources_dids(uid=uid)
    wids=cassapiwidget.get_widgets_wids(uid=uid)
    bids=cassapidashboard.get_dashboards_bids(uid=uid)
    cids=cassapicircle.get_circles_cids(uid=uid)
    nids=cassapisnapshot.get_snapshots_nids(uid=uid)
    for aid in aids:
        delete_agent(aid=aid)
    for bid in bids:
        delete_dashboard(bid=bid)
    for cid in cids:
        delete_circle(cid=cid)
    for nid in nids:
        delete_snapshot(nid=nid)
    for wid in wids:
        delete_widget(wid=wid)
    for did in dids:
        delete_datasource(did=did)
    cassapiuser.delete_user(username=user.username)
    cassapiuser.delete_signup_info(username=user.username)
    inv_req=cassapiuser.get_invitation_request(email=user.email)
    if inv_req:
        cassapiuser.delete_invitation_request(email=user.email)
        cassapiuser.delete_invitation_info(inv_id=inv_req.inv_id)
    forget_req=cassapiuser.get_forget_requests_by_uid(uid=uid)
    for req in forget_req:
        cassapiuser.delete_forget_request(code=req.code)
    tickets=cassapiticket.get_tickets_by_uid(uid=uid)
    for ticket in tickets:
        cassapiticket.delete_ticket(ticket.tid)
    tickets=cassapiticket.get_expired_tickets_by_uid(uid=uid)
    for ticket in tickets:
        cassapiticket.delete_expired_ticket(ticket.tid)
    cassapievents.delete_user_events(uid=uid)
    cassapiiface.delete_user_ifaces_deny(uid=uid)
    cassapiiface.delete_user_ts_ifaces_deny(uid=uid)
    cassapiperm.delete_user_agents_perm(uid=uid)
    cassapiperm.delete_user_datasources_perm(uid=uid)
    cassapiperm.delete_user_datapoints_perm(uid=uid)
    cassapiperm.delete_user_widgets_perm(uid=uid)
    cassapiperm.delete_user_dashboards_perm(uid=uid)
    cassapiperm.delete_user_snapshots_perm(uid=uid)
    cassapiperm.delete_user_circles_perm(uid=uid)
    cassapiquote.delete_user_quotes(uid=uid)
    cassapiquote.delete_user_ts_quotes(uid=uid)
    return True

def delete_agent(aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DA_IA)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        return False
    cassapiagent.delete_agent(aid=aid)
    cassapiagent.delete_agent_pubkey(uid=agent.uid, pubkey=agent.pubkey)
    cassapiagent.delete_agent_challenges(aid=aid)
    cassapiquote.delete_agent_quotes(aid=aid)
    return True

def delete_datasource(did, delete_datapoints=True):
    ''' Delete all datasource config and data, related widgets, and datapoints too '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DDS_ID)
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    widget=cassapiwidget.get_widget_ds(did=did)
    cassapidatasource.delete_datasource(did=did)
    cassapidatasource.delete_datasource_stats(did=did)
    cassapidatasource.delete_datasource_data(did=did)
    cassapidatasource.delete_datasource_metadata(did=did)
    cassapidatasource.delete_datasource_maps(did=did)
    cassapidatasource.delete_datasource_hashes(did=did)
    cassapidatasource.delete_datasource_text_summaries(did=did)
    cassapiquote.delete_datasource_quotes(did=did)
    cassapiquote.delete_datasource_ts_quotes(did=did)
    if delete_datapoints:
        for pid in pids:
            delete_datapoint(pid=pid)
    else:
        for pid in pids:
            dissociate_datapoint(pid=pid)
    if widget:
        delete_widget(wid=widget.wid)
    graphuri.dissociate_vertex(ido=did)
    return True

def dissociate_datapoint(pid):
    ''' Dissociate a datapoint from its current datasource.
        The data already identified is not deleted, we only delete
        the datasource association and the algorithms calculated for the identification
        in the datasource.  '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DSDP_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    cassapidatapoint.dissociate_datapoint_from_datasource(pid)
    cassapidatapoint.set_datapoint_dtree(pid=pid, dtree=None)
    cassapidatapoint.set_datapoint_dtree_inv(pid=pid, dtree=None)
    cassapidatapoint.delete_datapoint_dtree_positives(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_negatives(pid=pid)
    if datapoint and datapoint.did:
        cassapidatasource.delete_datasource_novelty_detector_for_datapoint(did=datapoint.did,pid=pid)
    return True

def delete_datapoint(pid):
    ''' Delete all datapoint info. '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DDP_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    widget=cassapiwidget.get_widget_dp(pid=pid)
    if widget:
        related_widgets=graphkin.get_kin_widgets(ido=widget.wid)
        for related_widget in related_widgets:
            rel_w_conf=cassapiwidget.get_widget(wid=related_widget['wid'])
            if rel_w_conf and rel_w_conf.type==widgettypes.MULTIDP:
                cassapiwidget.delete_datapoint_from_multidp(wid=related_widget['wid'],pid=pid)
        delete_widget(wid=widget.wid)
    if datapoint and datapoint.did:
        cassapidatasource.delete_datasource_novelty_detector_for_datapoint(did=datapoint.did,pid=pid)
        fromdate=timeuuid.LOWEST_TIME_UUID
        todate=timeuuid.uuid1()
        dsmap_dates=cassapidatasource.get_datasource_map_dates(did=datapoint.did, fromdate=fromdate, todate=todate)
        for date in dsmap_dates:
            cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did, date=date, pid=pid)
    cassapidatapoint.delete_datapoint(pid=pid)
    cassapidatapoint.delete_datapoint_stats(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_positives(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_negatives(pid=pid)
    cassapidatapoint.delete_datapoint_data(pid=pid)
    cassapiquote.delete_datapoint_quotes(pid=pid)
    graphuri.dissociate_vertex(ido=pid)
    return True

def delete_widget(wid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DW_IW)
    widget=cassapiwidget.get_widget(wid=wid)
    if widget:
        bids=cassapidashboard.get_dashboards_bids(uid=widget.uid)
        for bid in bids:
            cassapidashboard.delete_widget_from_dashboard(bid=bid, wid=wid)
    nids=cassapisnapshot.get_snapshots_nids(wid=wid)
    for nid in nids:
        delete_snapshot(nid=nid)
    kin_widgets=graphkin.get_kin_widgets(ido=wid)
    for kin_widget in kin_widgets:
        graphkin.unkin_widgets(ido=wid, idd=kin_widget['wid'])
    cassapiwidget.delete_widget(wid=wid)
    cassapiquote.delete_widget_quotes(wid=wid)
    return True

def delete_dashboard(bid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DDB_IB)
    cassapidashboard.delete_dashboard(bid=bid)
    cassapiquote.delete_dashboard_quotes(bid=bid)
    return True

def delete_circle(cid):
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DC_IC)
    cassapicircle.delete_circle(cid=cid)
    cassapiquote.delete_circle_quotes(cid=cid)
    return True

def delete_snapshot(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException(error=Errors.E_GCD_DN_IN)
    return True if cassapisnapshot.delete_snapshot(nid=nid) else False

