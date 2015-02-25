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
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.general import colors

def get_widget_config(wid):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
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

def get_widgets_config(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
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
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    bids=cassapidashboard.get_dashboards_bids(uid=widget.uid)
    for bid in bids:
        cassapidashboard.delete_widget_from_dashboard(bid=bid, wid=wid)
    nids=cassapisnapshot.get_snapshots_nids(uid=widget.uid)
    for nid in nids:
        cassapisnapshot.delete_snapshot(nid=nid)
    cassapiwidget.delete_widget(wid=wid)
    return True

def new_widget_datasource(username,did):
    if not args.is_valid_username(username) or not args.is_valid_uuid(did):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException()
    userwidgets=cassapiwidget.get_widgets(uid=user.uid)
    if userwidgets:
        for widget in userwidgets:
            if widget.type==types.DATASOURCE:
                widget_ds=cassapiwidget.get_widget_ds(wid=widget.wid)
                if widget_ds and widget_ds.did==did:
                    raise exceptions.WidgetAlreadyExistsException()
    wid=uuid.uuid4()
    widget=ormwidget.WidgetDs(wid=wid,widgetname=datasource.datasourcename, uid=datasource.uid,did=datasource.did,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type, 'did': widget.did}
    else:
        raise exceptions.WidgetCreationException()

def new_widget_datapoint(username,pid):
    if not args.is_valid_username(username) or not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    widgets=cassapiwidget.get_widgets(uid=user.uid)
    for widget in widgets:
        if widget.type==types.DATAPOINT:
            dpwidget=cassapiwidget.get_widget_dp(wid=widget.wid)
            if dpwidget and dpwidget.pid==pid:
                raise exceptions.WidgetAlreadyExistsException()
    wid=uuid.uuid4()
    widget=ormwidget.WidgetDp(wid=wid,widgetname=datapoint.datapointname, uid=user.uid,pid=datapoint.pid,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type, 'pid': widget.pid}
    else:
        raise exceptions.WidgetCreationException()

def new_widget_histogram(username, widgetname):
    if not args.is_valid_username(username) or not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    wid=uuid.uuid4()
    widget=ormwidget.WidgetHistogram(wid=wid,uid=user.uid,widgetname=widgetname,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type}
    else:
        raise exceptions.WidgetCreationException()

def new_widget_linegraph(username, widgetname):
    if not args.is_valid_username(username) or not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    wid=uuid.uuid4()
    widget=ormwidget.WidgetLinegraph(wid=wid,uid=user.uid,widgetname=widgetname,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type}
    else:
        raise exceptions.WidgetCreationException()

def new_widget_table(username, widgetname):
    if not args.is_valid_username(username) or not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    wid=uuid.uuid4()
    widget=ormwidget.WidgetTable(wid=wid,uid=user.uid,widgetname=widgetname,creation_date=timeuuid.uuid1())
    if cassapiwidget.new_widget(widget=widget):
        return {'wid': widget.wid, 'widgetname': widget.widgetname, 'uid': widget.uid, 'type': widget.type}
    else:
        raise exceptions.WidgetCreationException()

def add_datapoint_to_widget(wid, pid):
    if not args.is_valid_uuid(wid) or not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    color=datapoint.color if datapoint.color else colors.get_random_color()
    if widget.type==types.HISTOGRAM:
        if cassapiwidget.add_datapoint_to_histogram(wid=wid, pid=pid, color=color):
            return True
        else:
            raise exceptions.AddDatapointToWidgetException()
    elif widget.type==types.LINEGRAPH:
        if cassapiwidget.add_datapoint_to_linegraph(wid=wid, pid=pid, color=color):
            return True
        else:
            raise exceptions.AddDatapointToWidgetException()
    elif widget.type==types.TABLE:
        if cassapiwidget.add_datapoint_to_table(wid=wid, pid=pid, color=color):
            return True
        else:
            raise exceptions.AddDatapointToWidgetException()
    else:
        raise exceptions.WidgetUnsupportedOperationException()

def delete_datapoint_from_widget(wid, pid):
    if not args.is_valid_uuid(wid) or not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    if widget.type==types.HISTOGRAM:
        if cassapiwidget.delete_datapoint_from_histogram(wid=wid, pid=pid):
            return True
        else:
            raise exceptions.DeleteDatapointFromWidgetException()
    elif widget.type==types.LINEGRAPH:
        if cassapiwidget.delete_datapoint_from_linegraph(wid=wid, pid=pid):
            return True
        else:
            raise exceptions.DeleteDatapointFromWidgetException()
    elif widget.type==types.TABLE:
        if cassapiwidget.delete_datapoint_from_table(wid=wid, pid=pid):
            return True
        else:
            raise exceptions.DeleteDatapointFromWidgetException()
    else:
        raise exceptions.WidgetUnsupportedOperationException()

def update_widget_config(wid, widgetname=None, colors=None):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WdigetNotFoundException()
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
        raise exceptions.WidgetUnsupportedOperationException()

def update_widget_datasource(wid, widgetname):
    if not args.is_valid_uuid(wid) or not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget_ds(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if cassapiwidget.insert_widget_widgetname(wid=wid, widgetname=widgetname):
        return True
    else:
        return False

def update_widget_datapoint(wid, widgetname):
    if not args.is_valid_uuid(wid) or not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget_dp(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if cassapiwidget.insert_widget_widgetname(wid=wid, widgetname=widgetname):
        return True
    else:
        return False

def update_widget_histogram(wid, widgetname=None, colors=None):
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget_histogram(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not pid in widget.datapoints:
                raise exceptions.DatapointNotFoundException()
            elif not args.is_valid_hexcolor(colors[pid]):
                raise exceptions.BadParametersException()
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
        raise exceptions.BadParametersException()
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget_linegraph(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not pid in widget.datapoints:
                raise exceptions.DatapointNotFoundException()
            elif not args.is_valid_hexcolor(colors[pid]):
                raise exceptions.BadParametersException()
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
        raise exceptions.BadParametersException()
    if widgetname and not args.is_valid_widgetname(widgetname):
        raise exceptions.BadParametersException()
    if colors and not args.is_valid_dict(colors):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget_table(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not pid in widget.datapoints:
                raise exceptions.DatapointNotFoundException()
            elif not args.is_valid_hexcolor(colors[pid]):
                raise exceptions.BadParametersException()
    if widgetname:
        if not cassapiwidget.insert_widget_widgetname(wid,widgetname):
            return False
    if colors:
        pids=list(colors.keys())
        for pid in pids:
            if not cassapiwidget.add_datapoint_to_table(wid=wid, pid=pid, color=colors[pid]):
                return False
    return True

