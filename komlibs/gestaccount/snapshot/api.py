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
from komcass.api import circle as cassapicircle
from komcass.model.orm import snapshot as ormsnapshot
from komlibs.gestaccount.widget import types
from komlibs.gestaccount import exceptions, errors
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komfig import logger

def get_snapshot_config(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_GSA_GSC_IN)
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.SnapshotNotFoundException(error=errors.E_GSA_GSC_SNF)
    data={}
    if snapshot.type==types.DATASOURCE:
        datapoints_config=[]
        for datapoint in snapshot.datapoints_config:
            datapoints_config.append({'pid':datapoint.pid,'datapointname':datapoint.datapointname,'color':datapoint.color})
        datasource_config={'did':snapshot.datasource_config.did, 'datasourcename':snapshot.datasource_config.datasourcename}
        data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid,'type':types.DATASOURCE, 'datasource_config':datasource_config, 'datapoints_config':datapoints_config, 'interval_init':snapshot.interval_init,'interval_end':snapshot.interval_end}
    elif snapshot.type==types.DATAPOINT:
        datapoint_config={'pid':snapshot.datapoint_config.pid, 'datapointname':snapshot.datapoint_config.datapointname,'color':snapshot.datapoint_config.color}
        data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid,'type':types.DATAPOINT,'datapoint_config':datapoint_config, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.MULTIDP:
        datapoints_config=[]
        for datapoint in snapshot.datapoints_config:
            datapoints_config.append({'pid':datapoint.pid,'datapointname':datapoint.datapointname,'color':datapoint.color})
        data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.MULTIDP,'datapoints':snapshot.datapoints, 'datapoints_config':datapoints_config, 'active_visualization':snapshot.active_visualization, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.HISTOGRAM:
        data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.HISTOGRAM,'datapoints':snapshot.datapoints, 'colors':snapshot.colors, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.LINEGRAPH:
        data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.LINEGRAPH,'datapoints':snapshot.datapoints, 'colors':snapshot.colors, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    elif snapshot.type==types.TABLE:
        data={'uid':snapshot.uid, 'widgetname':snapshot.widgetname, 'wid':snapshot.wid, 'nid':snapshot.nid, 'type':types.TABLE,'datapoints':snapshot.datapoints, 'colors':snapshot.colors, 'interval_init':snapshot.interval_init, 'interval_end':snapshot.interval_end}
    return data

def get_snapshots_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GSA_GSSC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GSA_GSSC_UNF)
    data=[]
    nids=cassapisnapshot.get_snapshots_nids(uid=user.uid)
    for nid in nids:
        snapshot=get_snapshot_config(nid=nid)
        data.append(snapshot)
    return data

def delete_snapshot(nid):
    if not args.is_valid_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_GSA_DS_IN)
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if not snapshot:
        raise exceptions.SnapshotNotFoundException(error=errors.E_GSA_DS_SNF)
    cassapisnapshot.delete_snapshot(nid=nid)
    return True

def new_snapshot(uid, wid, interval_init, interval_end):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GSA_NS_IU)
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GSA_NS_IW)
    if not args.is_valid_date(interval_init):
        raise exceptions.BadParametersException(error=errors.E_GSA_NS_III)
    if not args.is_valid_date(interval_end):
        raise exceptions.BadParametersException(error=errors.E_GSA_NS_IIE)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GSA_NS_UNF)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NS_WNF)
    if interval_init.time>interval_end.time:
        interval_init,interval_end=interval_end,interval_init
    snapshot=None
    if widget.type==types.DATASOURCE:
        snapshot=_new_snapshot_datasource(uid=user.uid,wid=wid,interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.DATAPOINT:
        snapshot=_new_snapshot_datapoint(uid=user.uid,wid=wid,interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.MULTIDP:
        snapshot=_new_snapshot_multidp(uid=user.uid,wid=wid,interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.HISTOGRAM:
        snapshot=_new_snapshot_histogram(uid=user.uid,wid=wid,interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.LINEGRAPH:
        snapshot=_new_snapshot_linegraph(uid=user.uid,wid=wid,interval_init=interval_init, interval_end=interval_end)
    elif widget.type==types.TABLE:
        snapshot=_new_snapshot_table(uid=user.uid,wid=wid,interval_init=interval_init, interval_end=interval_end)
    if snapshot:
        return snapshot
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NS_SCE)

def _new_snapshot_datasource(uid,wid,interval_init, interval_end):
    widget=cassapiwidget.get_widget_ds(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NSDS_WNF)
    datasource=cassapidatasource.get_datasource(did=widget.did)
    if not datasource:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSDS_DNF)
    datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=widget.did, datasourcename=datasource.datasourcename)
    datapoints=set()
    map_dates=cassapidatasource.get_datasource_map_dates(did=widget.did, fromdate=interval_init, todate=interval_end)
    for date in map_dates:
        map_datapoints=cassapidatasource.get_datasource_map_datapoints(did=widget.did, date=date)
        if map_datapoints:
            for pid in map_datapoints.keys():
                datapoints.add(pid)
    datapoints_config=[]
    for pid in datapoints:
        datapoint_info=cassapidatapoint.get_datapoint(pid=pid)
        if datapoint_info:
            datapoint=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=datapoint_info.datapointname, color=datapoint_info.color)
            datapoints_config.append(datapoint)
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, did=widget.did, datasource_config=datasource_config, datapoints_config=datapoints_config)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':nid,'uid':uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSDS_SCE)

def _new_snapshot_datapoint(uid,wid,interval_init, interval_end):
    widget=cassapiwidget.get_widget_dp(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NSDP_WNF)
    datapoint=cassapidatapoint.get_datapoint(pid=widget.pid)
    if not datapoint:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSDP_PNF)
    datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=widget.pid, datapointname=datapoint.datapointname, color=datapoint.color)
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, pid=widget.pid, datapoint_config=datapoint_config)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':nid,'uid':uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSDP_SCE)

def _new_snapshot_histogram(uid,wid,interval_init, interval_end):
    widget=cassapiwidget.get_widget_histogram(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NSH_WNF)
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GSA_NSH_ZDP)
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, datapoints=widget.datapoints, colors=widget.colors)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':nid,'uid':uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSH_SCE)

def _new_snapshot_linegraph(uid,wid,interval_init, interval_end):
    widget=cassapiwidget.get_widget_linegraph(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NSL_WNF)
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GSA_NSL_ZDP)
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, datapoints=widget.datapoints, colors=widget.colors)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':nid,'uid':uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSL_SCE)

def _new_snapshot_table(uid,wid,interval_init, interval_end):
    widget=cassapiwidget.get_widget_table(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NST_WNF)
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GSA_NST_ZDP)
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, datapoints=widget.datapoints, colors=widget.colors)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':nid,'uid':uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NST_SCE)

def _new_snapshot_multidp(uid,wid,interval_init, interval_end):
    widget=cassapiwidget.get_widget_multidp(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GSA_NSMP_WNF)
    if len(widget.datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GSA_NSMP_ZDP)
    datapoints_config=[]
    datapoints=set()
    for pid in widget.datapoints:
        datapoint=cassapidatapoint.get_datapoint(pid=pid)
        if datapoint:
            datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=datapoint.pid, datapointname=datapoint.datapointname, color=datapoint.color)
            datapoints_config.append(datapoint_config)
            datapoints.add(pid)
    if len(datapoints)==0:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GSA_NSMP_ZDPF)
    nid=uuid.uuid4()
    creation_date=timeuuid.uuid1()
    snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widget.widgetname, creation_date=creation_date, active_visualization=widget.active_visualization, datapoints=datapoints, datapoints_config=datapoints_config)
    if cassapisnapshot.new_snapshot(snapshot):
        return {'nid':nid,'uid':uid,'wid':wid, 'interval_init':interval_init, 'interval_end':interval_end}
    else:
        raise exceptions.SnapshotCreationException(error=errors.E_GSA_NSMP_SCE)

