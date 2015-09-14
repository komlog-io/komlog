#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.dashboard import api as dashboardapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args

@exceptions.ExceptionHandler
def get_dashboards_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_GDBSCR_IU)
    uid=userapi.get_uid(username=username)
    data=dashboardapi.get_dashboards_config(uid=uid)
    response_data=[]
    for dashboard in data:
        reg={}
        reg['bid']=dashboard['bid'].hex
        reg['dashboardname']=dashboard['dashboardname']
        reg['wids']=[wid.hex for wid in dashboard['wids']]
        response_data.append(reg)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_dashboard_config_request(username, bid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_GDBCR_IU)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_GDBCR_IB)
    bid=uuid.UUID(bid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_DASHBOARD_CONFIG,uid=uid,bid=bid)
    data=dashboardapi.get_dashboard_config(bid=bid)
    dashboard={}
    dashboard['bid']=data['bid'].hex
    dashboard['dashboardname']=data['dashboardname']
    dashboard['wids']=[wid.hex for wid in data['wids']]
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=dashboard)

@exceptions.ExceptionHandler
def new_dashboard_request(username, dashboardname):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_NDBR_IU)
    if not args.is_valid_dashboardname(dashboardname):
        raise exceptions.BadParametersException(error=errors.E_IWADB_NDBR_IDN)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_DASHBOARD, uid=uid)
    dashboard=dashboardapi.create_dashboard(uid=uid, dashboardname=dashboardname)
    if dashboard:
        operation=weboperations.NewDashboardOperation(uid=dashboard['uid'],bid=dashboard['bid'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.UserEventMessage(uid=uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DASHBOARD, parameters={'bid':dashboard['bid'].hex, 'dashboardname':dashboardname})
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'bid':dashboard['bid'].hex})

@exceptions.ExceptionHandler
def delete_dashboard_request(username, bid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_DDBR_IU)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_DDBR_IB)
    bid=uuid.UUID(bid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_DASHBOARD,uid=uid,bid=bid)
    message=messages.DeleteDashboardMessage(bid=bid)
    msgapi.send_message(msg=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def update_dashboard_config_request(username, bid, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_UDBCR_IU)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_UDBCR_IB)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWADB_UDBCR_ID)
    if not 'dashboardname' in data or not args.is_valid_dashboardname(data['dashboardname']):
        raise exceptions.BadParametersException(error=errors.E_IWADB_UDBCR_IDN)
    bid=uuid.UUID(bid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.UPDATE_DASHBOARD_CONFIG, uid=uid, bid=bid)
    if dashboardapi.update_dashboard_config(bid=bid, dashboardname=data['dashboardname']):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def add_widget_request(username, bid, wid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_AWR_IU)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_AWR_IB)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_AWR_IW)
    bid=uuid.UUID(bid)
    wid=uuid.UUID(wid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.ADD_WIDGET_TO_DASHBOARD, uid=uid, bid=bid, wid=wid)
    if dashboardapi.add_widget_to_dashboard(bid=bid, wid=wid):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_widget_request(username, bid, wid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADB_DWR_IU)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_DWR_IB)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWADB_DWR_IW)
    bid=uuid.UUID(bid)
    wid=uuid.UUID(wid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_WIDGET_FROM_DASHBOARD, uid=uid, bid=bid, wid=wid)
    if dashboardapi.delete_widget_from_dashboard(bid=bid, wid=wid):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

