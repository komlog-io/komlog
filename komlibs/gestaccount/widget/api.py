#coding: utf-8
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
from komcass.model.orm import widget as ormwidget
from komlibs.gestaccount.widget import types
from komlibs.gestaccount import exceptions
from komlibs.ifaceops import operations
from komlibs.general.validation import arguments
from komlibs.general.time import timeuuid

def get_widget_config(wid):
    if not arguments.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    widget=cassapiwidget.get_widget(wid=wid)
    if widget:
        data={}
        if widget.type==types.DS_WIDGET:
            dswidget=cassapiwidget.get_widget_ds(wid=wid)
            if dswidget:
                data={'wid':str(dswidget.wid),'type':types.DS_WIDGET,'did':str(dswidget.did)}
        elif widget.type==types.DP_WIDGET:
            dpwidget=cassapiwidget.get_widget_dp(wid=wid)
            if dpwidget:
                data={'wid':str(dpwidget.wid),'type':types.DP_WIDGET,'pid':str(dpwidget.pid)}
        return data
    else:
        raise exceptions.WidgetNotFoundException()

def get_widgets_config(username):
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data=[]
    widgets=cassapiwidget.get_widgets(uid=user.uid)
    for widget in widgets:
        if widget.type==types.DS_WIDGET:
            dswidget=cassapiwidget.get_widget_ds(wid=widget.wid)
            if dswidget:
                data.append({'wid':str(dswidget.wid),'type':types.DS_WIDGET,'did':str(dswidget.did)})
        elif widget.type==types.DP_WIDGET:
            dpwidget=cassapiwidget.get_widget_dp(wid=widget.wid)
            if dpwidget:
                data.append({'wid':str(dpwidget.wid),'type':types.DP_WIDGET,'pid':str(dpwidget.pid)})
    return data

def delete_widget(username,wid):
    if not arguments.is_valid_username(username) or not arguments.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    else:
        if cassapiwidget.delete_widget(wid=widget.wid):
            return True
        else:
            return False

def new_widget_ds(username,did):
    if not arguments.is_valid_username(username) or not arguments.is_valid_uuid(did):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException()
    else:
        userwidgets=cassapiwidget.get_widgets(uid=user.uid)
        if userwidgets:
            for widget in userwidgets:
                if widget.type==types.DS_WIDGET:
                    widget_ds=cassapiwidget.get_widget_ds(wid=widget.wid)
                    if widget_ds and widget_ds.did==did:
                        return {'wid':str(wid)}
        wid=uuid.uuid4()
        widget=ormwidget.WidgetDs(wid=wid,uid=datasource.uid,did=datasource.did,creation_date=timeuuid.uuid1())
        if cassapiwidget.new_widget(widget=widget):
            return widget
        else:
            raise exceptions.WidgetCreationException()

def new_widget_dp(username,pid):
    if not arguments.is_valid_username(username) or not arguments.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    else:
        widgets=cassapiwidget.get_widgets(uid=user.uid)
        for widget in widgets:
            if widget.type==types.DP_WIDGET:
                dpwidget=cassapiwidget.get_widget_dp(wid=widget.wid)
                if dpwidget and dpwidget.pid==pid:
                    return {'wid':str(widget.wid)}
        wid=uuid.uuid4()
        widget=ormwidget.WidgetDp(wid=wid,uid=user.uid,pid=datapoint.pid,creation_date=timeuuid.uuid1())
        if cassapiwidget.new_widget(widget=widget):
            return widget
        else:
            raise exceptions.WidgetCreationException()

