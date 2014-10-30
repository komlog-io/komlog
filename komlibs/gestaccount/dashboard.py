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
from komlibs.gestaccount import states,types,exceptions


def get_dashboards_config(username):
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data=[]
    dashboards=cassapidashboard.get_dashboards(uid=user.uid)
    if dashboards:
        for dashboard in dashboards:
            wids=[str(wid) for wid in dashboard.widgets] if dashboard.widgets else []
            data.append({'bid':str(dashboard.bid),'name':dashboard.dashboardname,'wids':wids})
        return data
    else:
        raise exceptions.DashboardNotFoundException()

def get_dashboard_config(bid):
    dashboard=cassapi.get_dashboard(bid=bid)
    if dashboard:
        wids=[str(wid) for wid in dashboard.widgets] if dashboard.widgets else []
        data={'bid':str(dashboard.bid),'name':dashboard.dashboardname,'wids':wids}
        return data
    else:
        raise exceptions.DashboardNotFoundException()

