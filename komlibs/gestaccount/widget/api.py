'''
widget.py: library for managing widget operations

This file implements the logic of different widget operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2014/09/18
author: jcazor
'''

import uuid
from komcass.api import widget as cassapiwidget
from komcass.api import user as cassapiuser
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import dashboard as cassapidashboard
from komcass.api import snapshot as cassapisnapshot
from komcass.model.orm import widget as ormwidget
from komlibs.gestaccount.widget import types
from komlibs.gestaccount import exceptions, errors
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.general import colors
from komlibs.graph.api import uri as graphuri
from komlibs.graph.api import kin as graphkin

def get_widget_config(wid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_GWC_IW)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_GWC_WNF)
    data={}
    if widget.type==types.DATASOURCE:
        widget=cassapiwidget.get_widget_ds(wid=wid)
        if widget:
            data={'uid':widget.uid, 'widgetname': widget.widgetname, 'wid':widget.wid,'type':types.DATASOURCE,'did':widget.did}
    elif widget.type==types.DATAPOINT:
        widget=cassapiwidget.get_widget_dp(wid=wid)
        if widget:
            data={'uid':widget.uid, 'widgetname': widget.widgetname, 'wid':widget.wid,'type':types.DATAPOINT,'pid':widget.pid}
    elif widget.type==types.HISTOGRAM:
        widget=cassapiwidget.get_widget_histogram(wid=wid)
        if widget:
            data={'uid':widget.uid, 'widgetname': widget.widgetname, 'wid':widget.wid,'type':types.HISTOGRAM,'datapoints':widget.datapoints, 'colors':widget.colors}
    elif widget.type==types.LINEGRAPH:
        widget=cassapiwidget.get_widget_linegraph(wid=wid)
        if widget:
            data={'uid':widget.uid, 'widgetname': widget.widgetname, 'wid':widget.wid,'type':types.LINEGRAPH,'datapoints':widget.datapoints, 'colors':widget.colors}
    elif widget.type==types.TABLE:
        widget=cassapiwidget.get_widget_table(wid=wid)
        if widget:
            data={'uid':widget.uid, 'widgetname': widget.widgetname, 'wid':widget.wid,'type':types.TABLE,'datapoints':widget.datapoints, 'colors':widget.colors}
    return data

def get_widgets_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GWA_GWSC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GWA_GWSC_UNF)
    data=[]
    widgets=cassapiwidget.get_widgets(uid=user.uid)
    for widget in widgets:
        if widget.type==types.DATASOURCE:
            dswidget=cassapiwidget.get_widget_ds(wid=widget.wid)
            if dswidget:
                data.append({'uid':dswidget.uid, 'widgetname': dswidget.widgetname, 'wid':dswidget.wid,'type':types.DATASOURCE,'did':dswidget.did})
        elif widget.type==types.DATAPOINT:
            dpwidget=cassapiwidget.get_widget_dp(wid=widget.wid)
            if dpwidget:
                data.append({'uid':dpwidget.uid, 'widgetname': dpwidget.widgetname, 'wid':dpwidget.wid,'type':types.DATAPOINT,'pid':dpwidget.pid})
        elif widget.type==types.HISTOGRAM:
            hgwidget=cassapiwidget.get_widget_histogram(wid=widget.wid)
            if hgwidget:
                data.append({'uid':hgwidget.uid, 'widgetname': hgwidget.widgetname, 'wid':hgwidget.wid,'type':types.HISTOGRAM,'datapoints':hgwidget.datapoints, 'colors':hgwidget.colors})
        elif widget.type==types.LINEGRAPH:
            lgwidget=cassapiwidget.get_widget_linegraph(wid=widget.wid)
            if lgwidget:
                data.append({'uid':lgwidget.uid, 'widgetname': lgwidget.widgetname, 'wid':lgwidget.wid,'type':types.LINEGRAPH,'datapoints':lgwidget.datapoints, 'colors':lgwidget.colors})
        elif widget.type==types.TABLE:
            tbwidget=cassapiwidget.get_widget_table(wid=widget.wid)
            if tbwidget:
                data.append({'uid':tbwidget.uid, 'widgetname': tbwidget.widgetname, 'wid':tbwidget.wid,'type':types.TABLE,'datapoints':tbwidget.datapoints, 'colors':tbwidget.colors})
    return data

def delete_widget(wid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_DW_IW)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_DW_WNF)
    bids=cassapidashboard.get_dashboards_bids(uid=widget.uid)
    for bid in bids:
        cassapidashboard.delete_widget_from_dashboard(bid=bid, wid=wid)
    nids=cassapisnapshot.get_snapshots_nids(uid=widget.uid)
    for nid in nids:
        cassapisnapshot.delete_snapshot(nid=nid)
    cassapiwidget.delete_widget(wid=wid)
    return True

def new_widget_datasource(uid,did):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWDS_IU)
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWDS_ID)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GWA_NWDS_UNF)
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=errors.E_GWA_NWDS_DNF)
    userwidgets=cassapiwidget.get_widgets(uid=user.uid)
    if userwidgets:
        for widget in userwidgets:
            if widget.type==types.DATASOURCE:
                widget_ds=cassapiwidget.get_widget_ds(wid=widget.wid)
                if widget_ds and widget_ds.did==did:
                    raise exceptions.WidgetAlreadyExistsException(error=errors.E_GWA_NWDS_WAE)
    wid=uuid.uuid4()
    widget=ormwidget.WidgetDs(wid=wid,widgetname=datasource.datasourcename, uid=user.uid,did=datasource.did,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type, 'did': widget.did}
    else:
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWDS_IWE)

def new_widget_datapoint(uid,pid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWDP_IU)
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWDP_ID)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GWA_NWDP_UNF)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=errors.E_GWA_NWDP_DNF)
    datasource=cassapidatasource.get_datasource(did=datapoint.did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=errors.E_GWA_NWDP_DSNF)
    widgets=cassapiwidget.get_widgets(uid=user.uid)
    for widget in widgets:
        if widget.type==types.DATAPOINT:
            dpwidget=cassapiwidget.get_widget_dp(wid=widget.wid)
            if dpwidget and dpwidget.pid==pid:
                raise exceptions.WidgetAlreadyExistsException(error=errors.E_GWA_NWDP_WAE)
    wid=uuid.uuid4()
    widgetname='.'.join((datasource.datasourcename,datapoint.datapointname))
    widget=ormwidget.WidgetDp(wid=wid,widgetname=widgetname, uid=user.uid,pid=datapoint.pid,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        dswidget=cassapiwidget.get_widget_ds(did=datapoint.did)
        if dswidget:
            graphkin.kin_widgets(ido=widget.wid, idd=dswidget.wid)
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type, 'pid': widget.pid}
    else:
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWDP_IWE)

def new_widget_histogram(uid, widgetname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWH_IU)
    if not args.is_valid_uri(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWH_IWN)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GWA_NWH_UNF)
    wid=uuid.uuid4()
    if not graphuri.new_widget_uri(uid=uid, uri=widgetname, wid=wid):
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWH_NWU)
    widget=ormwidget.WidgetHistogram(wid=wid,uid=user.uid,widgetname=widgetname,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type}
    else:
        graphuri.dissociate_uri(ido=uid, uri=widgetname)
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWH_IWE)

def new_widget_linegraph(uid, widgetname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWL_IU)
    if not args.is_valid_uri(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWL_IWN)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GWA_NWL_UNF)
    wid=uuid.uuid4()
    if not graphuri.new_widget_uri(uid=uid, uri=widgetname, wid=wid):
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWL_NWU)
    widget=ormwidget.WidgetLinegraph(wid=wid,uid=user.uid,widgetname=widgetname,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type}
    else:
        graphuri.dissociate_uri(ido=uid, uri=widgetname)
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWL_IWE)

def new_widget_table(uid, widgetname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWT_IU)
    if not args.is_valid_uri(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_NWT_IWN)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GWA_NWT_UNF)
    wid=uuid.uuid4()
    if not graphuri.new_widget_uri(uid=uid, uri=widgetname, wid=wid):
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWT_NWU)
    widget=ormwidget.WidgetTable(wid=wid,uid=user.uid,widgetname=widgetname,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type}
    else:
        graphuri.dissociate_uri(ido=uid, uri=widgetname)
        raise exceptions.WidgetCreationException(error=errors.E_GWA_NWT_IWE)

def add_datapoint_to_widget(wid, pid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_ADTW_IW)
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_GWA_ADTW_IP)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_ADTW_WNF)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=errors.E_GWA_ADTW_DNF)
    color=datapoint.color if datapoint.color else colors.get_random_color()
    if widget.type==types.HISTOGRAM:
        if not cassapiwidget.add_datapoint_to_histogram(wid=wid, pid=pid, color=color):
            raise exceptions.AddDatapointToWidgetException(error=errors.E_GWA_ADTW_IDHE)
    elif widget.type==types.LINEGRAPH:
        if not cassapiwidget.add_datapoint_to_linegraph(wid=wid, pid=pid, color=color):
            raise exceptions.AddDatapointToWidgetException(error=errors.E_GWA_ADTW_IDLE)
    elif widget.type==types.TABLE:
        if not cassapiwidget.add_datapoint_to_table(wid=wid, pid=pid, color=color):
            raise exceptions.AddDatapointToWidgetException(error=errors.E_GWA_ADTW_IDTE)
    else:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GWA_ADTW_WUO)
    dpwidget=cassapiwidget.get_widget_dp(pid=pid)
    if dpwidget:
        graphkin.kin_widgets(ido=dpwidget.wid, idd=wid)
    return True

def delete_datapoint_from_widget(wid, pid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_DDFW_IW)
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_GWA_DDFW_IP)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_DDFW_WNF)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=errors.E_GWA_DDFW_DNF)
    if widget.type==types.HISTOGRAM:
        if not cassapiwidget.delete_datapoint_from_histogram(wid=wid, pid=pid):
            raise exceptions.DeleteDatapointFromWidgetException(error=errors.E_GWA_DDFW_IDHE)
    elif widget.type==types.LINEGRAPH:
        if not cassapiwidget.delete_datapoint_from_linegraph(wid=wid, pid=pid):
            raise exceptions.DeleteDatapointFromWidgetException(error=errors.E_GWA_DDFW_IDLE)
    elif widget.type==types.TABLE:
        if not cassapiwidget.delete_datapoint_from_table(wid=wid, pid=pid):
            raise exceptions.DeleteDatapointFromWidgetException(error=errors.E_GWA_DDFW_IDTE)
    else:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GWA_DDFW_WUO)
    dpwidget=cassapiwidget.get_widget_dp(pid=pid)
    if dpwidget:
        graphkin.unkin_widgets(ido=dpwidget.wid, idd=wid)
    return True

def update_widget_config(wid, widgetname=None, colors=None):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWC_IW)
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWC_IWN)
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWC_IC)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WdigetNotFoundException(error=errors.E_GWA_UWC_WNF)
    if widget.type==types.DATASOURCE:
        return update_widget_datasource(wid=wid, widgetname=widgetname)
    elif widget.type==types.DATAPOINT:
        return update_widget_datapoint(wid=wid, widgetname=widgetname)
    elif widget.type==types.HISTOGRAM:
        return update_widget_histogram(wid=wid, widgetname=widgetname, colors=colors)
    elif widget.type==types.LINEGRAPH:
        return update_widget_linegraph(wid=wid, widgetname=widgetname, colors=colors)
    elif widget.type==types.TABLE:
        return update_widget_table(wid=wid, widgetname=widgetname, colors=colors)
    else:
        raise exceptions.WidgetUnsupportedOperationException(error=errors.E_GWA_UWC_WUO)

def update_widget_datasource(wid, widgetname):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWDS_IW)
    if not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWDS_IWN)
    widget=cassapiwidget.get_widget_ds(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_UWDS_WNF)
    if cassapiwidget.insert_widget_widgetname(wid=wid, widgetname=widgetname):
        return True
    else:
        return False

def update_widget_datapoint(wid, widgetname):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWDP_IW)
    if not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWDP_IWN)
    widget=cassapiwidget.get_widget_dp(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_UWDP_WNF)
    if cassapiwidget.insert_widget_widgetname(wid=wid, widgetname=widgetname):
        return True
    else:
        return False

def update_widget_histogram(wid, widgetname=None, colors=None):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWH_IW)
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWH_IWN)
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWH_ICD)
    widget=cassapiwidget.get_widget_histogram(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_UWH_WNF)
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not pid in widget.datapoints:
                raise exceptions.DatapointNotFoundException(error=errors.E_GWA_UWH_DNF)
            elif not args.is_valid_hexcolor(colors[pid]):
                raise exceptions.BadParametersException(error=errors.E_GWA_UWH_IC)
    if widgetname:
        if not cassapiwidget.insert_widget_widgetname(wid,widgetname):
            return False
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not cassapiwidget.add_datapoint_to_histogram(wid=wid, pid=pid, color=colors[pid]):
                return False
    return True

def update_widget_linegraph(wid, widgetname=None, colors=None):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWL_IW)
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWL_IWN)
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWL_ICD)
    widget=cassapiwidget.get_widget_linegraph(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_UWL_WNF)
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not pid in widget.datapoints:
                raise exceptions.DatapointNotFoundException(error=errors.E_GWA_UWL_DNF)
            elif not args.is_valid_hexcolor(colors[pid]):
                raise exceptions.BadParametersException(error=errors.E_GWA_UWL_IC)
    if widgetname:
        if not cassapiwidget.insert_widget_widgetname(wid,widgetname):
            return False
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not cassapiwidget.add_datapoint_to_linegraph(wid=wid, pid=pid, color=colors[pid]):
                return False
    return True

def update_widget_table(wid, widgetname=None, colors=None):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWT_IW)
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWT_IWN)
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException(error=errors.E_GWA_UWT_ICD)
    widget=cassapiwidget.get_widget_table(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GWA_UWT_WNF)
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not pid in widget.datapoints:
                raise exceptions.DatapointNotFoundException(error=errors.E_GWA_UWT_DNF)
            elif not args.is_valid_hexcolor(colors[pid]):
                raise exceptions.BadParametersException(error=errors.E_GWA_UWT_IC)
    if widgetname:
        if not cassapiwidget.insert_widget_widgetname(wid,widgetname):
            return False
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not cassapiwidget.add_datapoint_to_table(wid=wid, pid=pid, color=colors[pid]):
                return False
    return True

def get_related_widgets(wid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GWA_GRW_IW)
    widgets=[]
    for widget in graphkin.get_kin_widgets(ido=wid):
        widgets.append(get_widget_config(wid=widget['wid']))
    return widgets

