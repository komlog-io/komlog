'''
snapshot.py: library for managing snapshot operations

This file implements the logic of different snapshot operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2015/02/15
author: jcazor
'''

import uuid
from komcass.api import snapshot as cassapisnapshot
from komcass.api import widget as cassapiwidget
from komcass.api import user as cassapiuser
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.model.orm import snapshot as ormsnapshot
from komlibs.gestaccount.widget import types
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komfig import logger

def get_snapshot_config(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException()
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.SnapshotNotFoundException()
    data={}
    if snapshot.type==types.DATASOURCE:
        snapshot=cassapisnapshot.get_snapshot_ds(nid=nid)
        if snapshot:
            data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid,'type':types.DATASOURCE,'did':snapshot.did,'interval_init':snapshot.interval_init,'interval_end':snapshot.interval_end}
    elif snapshot.type==types.DATAPOINT:
        snapshot=cassapisnapshot.get_snapshot_dp(nid=nid)
        if snapshot:
            data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid,'type':types.DATAPOINT,'pid':snapshot.pid, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.HISTOGRAM:
        snapshot=cassapisnapshot.get_snapshot_histogram(nid=nid)
        if snapshot:
            data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.HISTOGRAM,'datapoints':snapshot.datapoints, 'colors':snapshot.colors, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.LINEGRAPH:
        snapshot=cassapisnapshot.get_snapshot_linegraph(nid=nid)
        if snapshot:
            data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.LINEGRAPH,'datapoints':snapshot.datapoints, 'colors':snapshot.colors, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.TABLE:
        snapshot=cassapisnapshot.get_snapshot_table(nid=nid)
        if snapshot:
            data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.TABLE,'datapoints':snapshot.datapoints, 'colors':snapshot.colors, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    return data

def get_snapshots_config(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data=[]
    nids=cassapisnapshot.get_snapshots_nids(uid=user.uid)
    for nid in nids:
        snapshot=get_snapshot_config(nid=nid)
        data.append(snapshot)
    return data

def get_snapshot_data(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException()
    snapshot_config=get_snapshot_config(nid=nid)
    data={}
    if snapshot_config['type']==types.DATASOURCE:
        data[snapshot_config['did']]=[]
        datasources_data=cassapidatasource.get_datasource_data(did=snapshot_config['did'],fromdate=snapshot_config['interval_init'],todate=snapshot_config['interval_end'])
        for datasource_data in datasources_data:
            reg={}
            datapoints=cassapidatasource.get_datasource_map_datapoints(did=snapshot_config['did'], date=datasource_data.date)
            reg['date']=datasource_data.date
            reg['content']=datasource_data.content
            reg['datapoints']=datapoints if datapoints else {}
            data[snapshot_config['did']].append(reg)
    elif snapshot_config['type']==types.DATAPOINT:
        data[snapshot_config['pid']]=[]
        datapoint_datas=cassapidatapoint.get_datapoint_data(pid=snapshot_config['pid'],fromdate=snapshot_config['interval_init'],todate=snapshot_config['interval_end'])
        for datapoint_data in datapoint_datas:
            data[snapshot_config['pid']].append({'date':datapoint_data.date,'value':datapoint_data.value})
    elif snapshot_config['type'] in [types.HISTOGRAM,types.LINEGRAPH,types.TABLE]:
        for pid in snapshot_config['datapoints']:
            data[pid]=[]
            datapoint_datas=cassapidatapoint.get_datapoint_data(pid=pid,fromdate=snapshot_config['interval_init'],todate=snapshot_config['interval_end'])
            for datapoint_data in datapoint_datas:
                data[pid].append({'date':datapoint_data.date,'value':datapoint_data.value})
    return data

def delete_snapshot(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException()
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.SnapshotNotFoundException()
    cassapisnapshot.delete_snapshot(nid=nid)
    return True

def new_snapshot(username, wid, interval_init, interval_end):
    if not args.is_valid_username(username) or not args.is_valid_uuid(wid) or not args.is_valid_date(interval_init) or not args.is_valid_date(interval_end) or interval_init>interval_end:
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    snapshot=None
    if widget.type==types.DATASOURCE:
        snapshot=new_snapshot_datasource(username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.DATAPOINT:
        snapshot=new_snapshot_datapoint(username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.HISTOGRAM:
        snapshot=new_snapshot_histogram(username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.LINEGRAPH:
        snapshot=new_snapshot_linegraph(username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.TABLE:
        snapshot=new_snapshot_table(username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)
    if snapshot:
        return snapshot
    else:
        raise exceptions.SnapshotCreationException()

def new_snapshot_datasource(username,wid,interval_init, interval_end):
    if not args.is_valid_username(username) or not args.is_valid_uuid(wid) or not args.is_valid_date(interval_init) or not args.is_valid_date(interval_end):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    widget=cassapiwidget.get_widget_ds(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=user.uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, did=widget.did)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':snapshot.nid,'uid':user.uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException()

def new_snapshot_datapoint(username,wid,interval_init, interval_end):
    if not args.is_valid_username(username) or not args.is_valid_uuid(wid) or not args.is_valid_date(interval_init) or not args.is_valid_date(interval_end):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    widget=cassapiwidget.get_widget_dp(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=user.uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, pid=widget.pid)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':snapshot.nid,'uid':user.uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException()

def new_snapshot_histogram(username,wid,interval_init, interval_end):
    if not args.is_valid_username(username) or not args.is_valid_uuid(wid) or not args.is_valid_date(interval_init) or not args.is_valid_date(interval_end):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    widget=cassapiwidget.get_widget_histogram(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException()
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=user.uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, datapoints=widget.datapoints, colors=widget.colors)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':snapshot.nid,'uid':user.uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException()

def new_snapshot_linegraph(username,wid,interval_init, interval_end):
    if not args.is_valid_username(username) or not args.is_valid_uuid(wid) or not args.is_valid_date(interval_init) or not args.is_valid_date(interval_end):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    widget=cassapiwidget.get_widget_linegraph(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException()
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=user.uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, datapoints=widget.datapoints, colors=widget.colors)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':snapshot.nid,'uid':user.uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException()

def new_snapshot_table(username,wid,interval_init, interval_end):
    if not args.is_valid_username(username) or not args.is_valid_uuid(wid) or not args.is_valid_date(interval_init) or not args.is_valid_date(interval_end):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    widget=cassapiwidget.get_widget_table(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException()
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=user.uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, datapoints=widget.datapoints, colors=widget.colors)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':snapshot.nid,'uid':user.uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException()

