#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komlibs.auth import authorization
from komlibs.gestaccount.dashboard import api as dashboardapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.general.validation import arguments as args

@exceptions.ExceptionHandler
def get_dashboards_config_request(username):
    if args.is_valid_username(username):
        data=dashboardapi.get_dashboards_config(username=username)
        response_data=[]
        for dashboard in data:
            reg={}
            reg['bid']=dashboard['bid'].hex
            reg['dashboardname']=dashboard['dashboardname']
            reg['wids']=[wid.hex for wid in dashboard['wids']]
            response_data.append(reg)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_dashboard_config_request(username, bid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(bid):
        bid=uuid.UUID(bid)
        authorization.authorize_request(request='GetDashboardConfigRequest',username=username,bid=bid)
        data=dashboardapi.get_dashboard_config(bid=bid)
        dashboard={}
        dashboard['bid']=data['bid'].hex
        dashboard['dashboardname']=data['dashboardname']
        dashboard['wids']=[wid.hex for wid in data['wids']]
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=dashboard)
    else:
        raise exceptions.BadParametersException()

