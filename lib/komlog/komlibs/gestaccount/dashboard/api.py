#coding: utf-8
'''
dashboard.py: library for managing dashboard operations

This file implements the logic of different dashboard operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2014/09/20
author: jcazor
'''

import uuid
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.model.orm import dashboard as ormdashboard
from komlog.komlibs.gestaccount import exceptions, errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


def get_dashboards_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GBA_GDSC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GBA_GDSC_UNF)
    data=[]
    dashboards=cassapidashboard.get_dashboards(uid=user.uid)
    if dashboards:
        for dashboard in dashboards:
            wids=[wid for wid in dashboard.widgets] if dashboard.widgets else []
            data.append({'bid':dashboard.bid,'dashboardname':dashboard.dashboardname,'wids':wids})
    return data

def get_dashboard_config(bid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_GBA_GDC_IB)
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if dashboard:
        wids=[wid for wid in dashboard.widgets] if dashboard.widgets else []
        data={'bid':dashboard.bid,'dashboardname':dashboard.dashboardname,'wids':wids}
        return data
    else:
        raise exceptions.DashboardNotFoundException(error=errors.E_GBA_GDC_DNF)

def create_dashboard(uid, dashboardname):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GBA_CRD_IU)
    if not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException(error=errors.E_GBA_CRD_IDN)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GBA_CRD_UNF)
    bid=uuid.uuid4()
    dashboard=ormdashboard.Dashboard(uid=user.uid, bid=bid, creation_date=timeuuid.uuid1(), dashboardname=dashboardname)
    if cassapidashboard.new_dashboard(dobj=dashboard):
        return {'uid':user.uid,'bid':bid,'dashboardname':dashboardname}
    else:
        raise exceptions.DashboardCreationException(error=errors.E_GBA_CRD_IDE)

def update_dashboard_config(bid, dashboardname):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_GBA_UDC_IB)
    if not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException(error=errors.E_GBA_UDC_IDN)
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException(error=errors.E_GBA_UDC_DNF)
    dashboard.dashboardname=dashboardname
    if cassapidashboard.insert_dashboard(dobj=dashboard):
        return True
    else:
        raise exceptions.DashboardUpdateException(error=errors.E_GBA_UDC_IDE)

def add_widget_to_dashboard(bid, wid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_GBA_AWTD_IB)
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GBA_AWTD_IW)
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException(error=errors.E_GBA_AWTD_DNF)
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException(error=errors.E_GBA_AWTD_WNF)
    if cassapidashboard.add_widget_to_dashboard(bid=bid, wid=wid):
        return True
    else:
        return False

def delete_widget_from_dashboard(bid, wid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_GBA_DWFD_IB)
    if not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_GBA_DWFD_IW)
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException(error=errors.E_GBA_DWFD_DNF)
    if cassapidashboard.delete_widget_from_dashboard(bid=bid, wid=wid):
        return True
    else:
        return False

