'''

This file implement delete operations of gestaccount elements.


'''

from komfig import logger
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import snapshot as cassapisnapshot
from komcass.api import circle as cassapicircle
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.gestaccount.widget import types as widgettypes
from komlibs.gestaccount import exceptions, errors
from komlibs.graph.api import uri as graphuri
from komlibs.graph.api import kin as graphkin

def delete_user(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DU_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GCD_DU_UNF)
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
    return True

def delete_agent(aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DA_IA)
    return True if cassapiagent.delete_agent(aid=aid) else False

def delete_datasource(did):
    ''' Delete all datasource config and data, related widgets, and datapoints too '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GCD_DDS_ID)
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    widget=cassapiwidget.get_widget_ds(did=did)
    cassapidatasource.delete_datasource(did=did)
    cassapidatasource.delete_datasource_stats(did=did)
    cassapidatasource.delete_datasource_data(did=did)
    cassapidatasource.delete_datasource_maps(did=did)
    cassapidatasource.delete_datasource_text_summaries(did=did)
    for pid in pids:
        delete_datapoint(pid=pid)
    if widget:
        delete_widget(wid=widget.wid)
    graphuri.dissociate_vertex(ido=did)
    return True

def delete_datapoint(pid):
    ''' Delete all datapoint info. '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DDP_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    widget=cassapiwidget.get_widget_dp(pid=pid)
    if widget:
        related_widgets=graphkin.get_kin_widgets(ido=widget.wid)
        for related_widget in related_widgets:
            rel_w_conf=cassapiwidget.get_widget(wid=related_widget['wid'])
            if rel_w_conf and rel_w_conf.type==widgettypes.MULTIDP:
                cassapiwidget.delete_datapoint_from_multidp(wid=related_widget['wid'],pid=pid)
        delete_widget(wid=widget.wid)
    if datapoint:
        did=datapoint.did
        cassapidatasource.delete_datasource_novelty_detector_for_datapoint(did=did,pid=pid)
        fromdate=timeuuid.LOWEST_TIME_UUID
        todate=timeuuid.uuid1()
        dsmap_dates=cassapidatasource.get_datasource_map_dates(did=did, fromdate=fromdate, todate=todate)
        for date in dsmap_dates:
            cassapidatasource.delete_datapoint_from_datasource_map(did=did, date=date, pid=pid)
    cassapidatapoint.delete_datapoint(pid=pid)
    cassapidatapoint.delete_datapoint_stats(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_positives(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_negatives(pid=pid)
    cassapidatapoint.delete_datapoint_data(pid=pid)
    graphuri.dissociate_vertex(ido=pid)
    return True

def delete_widget(wid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DW_IW)
    widget=cassapiwidget.get_widget(wid=wid)
    if widget:
        bids=cassapidashboard.get_dashboards_bids(uid=widget.uid)
        for bid in bids:
            cassapidashboard.delete_widget_from_dashboard(bid=bid, wid=wid)
    nids=cassapisnapshot.get_snapshots_nids(wid=wid)
    for nid in nids:
        cassapisnapshot.delete_snapshot(nid=nid)
    kin_widgets=graphkin.get_kin_widgets(ido=wid)
    for kin_widget in kin_widgets:
        graphkin.unkin_widgets(ido=wid, idd=kin_widget['wid'])
    cassapiwidget.delete_widget(wid=wid)
    return True

def delete_dashboard(bid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DDB_IB)
    return True if cassapidashboard.delete_dashboard(bid=bid) else False

def delete_circle(cid):
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DC_IC)
    return True if cassapicircle.delete_circle(cid=cid) else False

def delete_snapshot(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_GCD_DN_IN)
    return True if cassapisnapshot.delete_snapshot(nid=nid) else False

