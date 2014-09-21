#coding: utf-8
'''
dashboards.py: library for managing dashboard operations

This file implements the logic of different dashboard operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2014/09/20
author: jcazor
'''

from komcass import api as cassapi
from komlibs.gestaccount import states,types,exceptions


def get_dashboardsconfig(username,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.UserNotFoundException()
    data=[]
    userdashboards=cassapi.get_userdashboardrelation(useruidr.uid,session)
    if userdashboards:
        for bid in userdashboards.bids:
            dashboard=cassapi.get_dashboard(bid,session)
            dashboardwidgetr=cassapi.get_dashboardwidgetrelation(bid,session)
            if dashboard:
                bids=[str(bid) for bid in dashboardwidgetr.bids] if dashboardwidgetr else []
                data.append({'bid':str(dashboard.bid),'name':dashboard.name,'bids':bids})
        return data
    else:
        raise exceptions.DashboardNotFoundException()

def get_dashboardconfig(bid,session):
    dashboard=cassapi.get_dashboard(bid,session)
    dashboardwidgetr=cassapi.get_dashboardwidgetrelation(bid,session)
    if dashboard:
        bids=[str(bid) for bid in dashboardwidgetr.bids] if dashboardwidgetr else []
        data={'bid':str(dashboard.bid),'name':dashboard.name,'bids':bids}
        return data
    else:
        raise exceptions.DashboardNotFoundException()

