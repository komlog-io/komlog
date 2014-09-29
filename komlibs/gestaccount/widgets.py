#coding: utf-8
'''
widgets.py: library for managing widget operations

This file implements the logic of different widget operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2014/09/18
author: jcazor
'''

import uuid
import json
import os
from datetime import datetime
from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions
from komlibs.ifaceops import operations
from komimc import messages

def get_widgetconfig(wid,session):
    widget=cassapi.get_widget(wid,session)
    if widget:
        data={}
        if widget.type==types.DS_WIDGET:
            dswidget=cassapi.get_datasource_widget(wid,session)
            if dswidget:
                data={'wid':str(dswidget.wid),'type':types.DS_WIDGET,'did':str(dswidget.did)}
        elif widget.type==types.DP_WIDGET:
            dpwidget=cassapi.get_datapoint_widget(wid,session)
            if dpwidget:
                data={'wid':str(dpwidget.wid),'type':types.DP_WIDGET,'pid':str(dpwidget.pid)}
        return data
    else:
        raise exceptions.WidgetNotFoundException()

def create_ds_widget(username,did,session,msgbus):
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    print 'obtenido useruidr '+username
    dsinfo=cassapi.get_dsinfo(did,{},session)
    if not dsinfo:
        raise exceptions.DatasourceNotFoundException()
    else:
        print 'obtenido dsinfo'
        userwidgets=cassapi.get_userwidgetrelation(useruidr.uid,session)
        if userwidgets:
            for wid in userwidgets.wids:
                widget=cassapi.get_widget(wid,session)
                if widget and widget.type==types.DS_WIDGET:
                    dswidget=cassapi.get_datasource_widget(wid,session)
                    if dswidget and dswidget.did==did:
                        print 'Datasource already linked to ds_widget'
                        return {'wid':str(wid)}
        wid=uuid.uuid4()
        dswidget=cassapi.DatasourceWidget(wid,dsinfo.uid,dsinfo.did)
        if cassapi.insert_datasource_widget(dswidget,session):
            print 'ds insertado correctamente en bbdd'
            operation=operations.NewWidgetOperation(uid=useruidr.uid,wid=wid)
            message=messages.UpdateQuotesMessage(operation=operation)
            msgbus.sendMessage(message)
            print 'enviado mensaje updatequotesoperation'
            message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            msgbus.sendMessage(message)
            print 'enviado mensaje resource authorizationupdate'
            return {'wid':str(wid)}
        else:
            raise exceptions.WidgetCreationException()

def delete_widget(username,wid,session,msgbus):
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    print 'obtenido useruidr '+username
    widget=cassapi.get_widget(wid,session)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    else:
        print 'obtenido widget'
        if widget.type == types.DS_WIDGET:
            if cassapi.delete_datasource_widget(widget,session):
#               TODO:
#               faltaría todo el envio de mensajes para actualizar quotas y permisos
#               pero para eso tenemos que crear operaciones nuevas, etc
                return True
            else:
                return False
        else:
            raise exceptions.WidgetTypeNotFoundException()

def get_widgetsconfig(username,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    data=[]
    userwidgets=cassapi.get_userwidgetrelation(useruidr.uid,session)
    if userwidgets:
        for wid in userwidgets.wids:
            widget=cassapi.get_widget(wid,session)
            if widget and widget.type==types.DS_WIDGET:
                dswidget=cassapi.get_datasource_widget(wid,session)
                if dswidget:
                    data.append({'wid':str(dswidget.wid),'type':types.DS_WIDGET,'did':str(dswidget.did)})
            elif widget.type==types.DP_WIDGET:
                dpwidget=cassapi.get_datapoint_widget(wid,session)
                if dpwidget:
                    data.append({'wid':str(dpwidget.wid),'type':types.DP_WIDGET,'pid':str(dpwidget.pid)})
        return data
    else:
        raise exceptions.WidgetNotFoundException()

def create_dp_widget(username,pid,session,msgbus):
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    print 'obtenido useruidr '+username
    dtpinfo=cassapi.get_dtpinfo(pid,{},session)
    if not dtpinfo:
        raise exceptions.DatapointNotFoundException()
    else:
        print 'obtenido dtpinfo'
        userwidgets=cassapi.get_userwidgetrelation(useruidr.uid,session)
        if userwidgets:
            for wid in userwidgets.wids:
                widget=cassapi.get_widget(wid,session)
                if widget and widget.type==types.DP_WIDGET:
                    dpwidget=cassapi.get_datapoint_widget(wid,session)
                    if dpwidget and dpwidget.pid==pid:
                        print 'Datapoint already linked to dp_widget'
                        return {'wid':str(wid)}
        wid=uuid.uuid4()
        dpwidget=cassapi.DatapointWidget(wid,useruidr.uid,dtpinfo.pid)
        if cassapi.insert_datapoint_widget(dpwidget,session):
            print 'dp insertado correctamente en bbdd'
            operation=operations.NewWidgetOperation(uid=useruidr.uid,wid=wid)
            message=messages.UpdateQuotesMessage(operation=operation)
            msgbus.sendMessage(message)
            print 'enviado mensaje updatequotesoperation'
            message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            msgbus.sendMessage(message)
            print 'enviado mensaje resource authorizationupdate'
            return {'wid':str(wid)}
        else:
            raise exceptions.WidgetCreationException()

