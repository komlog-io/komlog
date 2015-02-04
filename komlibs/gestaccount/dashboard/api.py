#coding: utf-8
'''
dashboard.py: library for managing dashboard operations

This file implements the logic of different dashboard operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2014/09/20
author: jcazor
'''

import uuid
from komcass.api import dashboard as cassapidashboard
from komcass.api import widget as cassapiwidget
from komcass.api import user as cassapiuser
from komcass.model.orm import dashboard as ormdashboard
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


def get_dashboards_config(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data=[]
    dashboards=cassapidashboard.get_dashboards(uid=user.uid)
    if dashboards:
        for dashboard in dashboards:
            wids=[wid for wid in dashboard.widgets] if dashboard.widgets else []
            data.append({'bid':dashboard.bid,'dashboardname':dashboard.dashboardname,'wids':wids})
    return data

def get_dashboard_config(bid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException()
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if dashboard:
        wids=[wid for wid in dashboard.widgets] if dashboard.widgets else []
        data={'bid':dashboard.bid,'dashboardname':dashboard.dashboardname,'wids':wids}
        return data
    else:
        raise exceptions.DashboardNotFoundException()

def delete_dashboard(bid):
    if not args.is_valid_uuid(bid):
        raise exceptions.BadParametersException()
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException()
    if cassapidashboard.delete_dashboard(bid=bid):
        return True
    else:
        return False

def create_dashboard(username, dashboardname):
    if not args.is_valid_username(username) or not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    bid=uuid.uuid4()
    dashboard=ormdashboard.Dashboard(uid=user.uid, bid=bid, creation_date=timeuuid.uuid1(), dashboardname=dashboardname)
    if cassapidashboard.new_dashboard(dobj=dashboard):
        return {'uid':user.uid,'bid':bid,'dashboardname':dashboardname}
    else:
        raise exceptions.DashboardCreationException()

def update_dashboard_config(bid, dashboardname):
    if not args.is_valid_uuid(bid) or not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException()
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException()
    dashboard.dashboardname=dashboardname
    if cassapidashboard.insert_dashboard(dobj=dashboard):
        return True
    else:
        raise exceptions.DashboardUpdateException()

def add_widget_to_dashboard(bid, wid):
    if not args.is_valid_uuid(bid) or not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException()
    widget=cassapiwidget.get_widget(wid=wid)
    if not widget:
        raise exceptions.WidgetNotFoundException()
    if cassapidashboard.add_widget_to_dashboard(bid=bid, wid=wid):
        return True
    else:
        return False

def delete_widget_from_dashboard(bid, wid):
    if not args.is_valid_uuid(bid) or not args.is_valid_uuid(wid):
        raise exceptions.BadParametersException()
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if not dashboard:
        raise exceptions.DashboardNotFoundException()
    if cassapidashboard.delete_widget_from_dashboard(bid=bid, wid=wid):
        return True
    else:
        return False

