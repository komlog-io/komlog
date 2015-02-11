#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount.dashboard import api as dashboardapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
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
        authorization.authorize_request(request=requests.GET_DASHBOARD_CONFIG,username=username,bid=bid)
        data=dashboardapi.get_dashboard_config(bid=bid)
        dashboard={}
        dashboard['bid']=data['bid'].hex
        dashboard['dashboardname']=data['dashboardname']
        dashboard['wids']=[wid.hex for wid in data['wids']]
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=dashboard)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_dashboard_request(username, dashboardname):
    if args.is_valid_username(username) and args.is_valid_dashboardname(dashboardname):
        authorization.authorize_request(request=requests.NEW_DASHBOARD, username=username)
        dashboard=dashboardapi.create_dashboard(username=username, dashboardname=dashboardname)
        if dashboard:
            operation=weboperations.NewDashboardOperation(uid=dashboard['uid'],bid=dashboard['bid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'bid':dashboard['bid'].hex})
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_dashboard_request(username, bid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(bid):
        bid=uuid.UUID(bid)
        authorization.authorize_request(request=requests.DELETE_DASHBOARD,username=username,bid=bid)
        message=messages.DeleteDashboardMessage(bid=bid)
        msgapi.send_message(msg=message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_dashboard_config_request(username, bid, data):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(bid) and args.is_valid_dict(data):
        bid=uuid.UUID(bid)
        if not 'dashboardname' in data or not args.is_valid_dashboardname(data['dashboardname']):
            raise exceptions.BadParametersException()
        authorization.authorize_request(request=requests.UPDATE_DASHBOARD_CONFIG, username=username, bid=bid)
        if dashboardapi.update_dashboard_config(bid=bid, dashboardname=data['dashboardname']):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def add_widget_request(username, bid, wid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(bid) and args.is_valid_hex_uuid(wid):
        bid=uuid.UUID(bid)
        wid=uuid.UUID(wid)
        authorization.authorize_request(request=requests.ADD_WIDGET_TO_DASHBOARD, username=username, bid=bid, wid=wid)
        if dashboardapi.add_widget_to_dashboard(bid=bid, wid=wid):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_widget_request(username, bid, wid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(bid) and args.is_valid_hex_uuid(wid):
        bid=uuid.UUID(bid)
        wid=uuid.UUID(wid)
        authorization.authorize_request(request=requests.DELETE_WIDGET_FROM_DASHBOARD, username=username, bid=bid, wid=wid)
        if dashboardapi.delete_widget_from_dashboard(bid=bid, wid=wid):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

