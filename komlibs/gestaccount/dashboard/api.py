#coding: utf-8
'''
dashboard.py: library for managing dashboard operations

This file implements the logic of different dashboard operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2014/09/20
author: jcazor
'''

from komcass.api import dashboard as cassapidashboard
from komcass.api import user as cassapiuser
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments


def get_dashboards_config(username):
    if not arguments.is_valid_username(username):
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
    if not arguments.is_valid_uuid(bid):
        raise exceptions.BadParametersException()
    dashboard=cassapidashboard.get_dashboard(bid=bid)
    if dashboard:
        wids=[wid for wid in dashboard.widgets] if dashboard.widgets else []
        data={'bid':dashboard.bid,'dashboardname':dashboard.dashboardname,'wids':wids}
        return data
    else:
        raise exceptions.DashboardNotFoundException()

