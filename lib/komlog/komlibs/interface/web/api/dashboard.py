'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komfig import logging
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.auth.passport import UserPassport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response, operation
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args

@exceptions.ExceptionHandler
def get_dashboards_config_request(passport):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_GDBSCR_IPSP)
    authorization.authorize_request(request=Requests.GET_DASHBOARDS_CONFIG,passport=passport)
    data=dashboardapi.get_dashboards_config(uid=passport.uid)
    response_data=[]
    for dashboard in data:
        reg={}
        reg['bid']=dashboard['bid'].hex
        reg['dashboardname']=dashboard['dashboardname']
        reg['wids']=[wid.hex for wid in dashboard['wids']]
        response_data.append(reg)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_dashboard_config_request(passport, bid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_GDBCR_IPSP)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_GDBCR_IB)
    bid=uuid.UUID(bid)
    authorization.authorize_request(request=Requests.GET_DASHBOARD_CONFIG,passport=passport,bid=bid)
    data=dashboardapi.get_dashboard_config(bid=bid)
    dashboard={}
    dashboard['bid']=data['bid'].hex
    dashboard['dashboardname']=data['dashboardname']
    dashboard['wids']=[wid.hex for wid in data['wids']]
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=dashboard)

@exceptions.ExceptionHandler
def new_dashboard_request(passport, data):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_NDBR_IPSP)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_NDBR_ID)
    if not 'dashboardname' in data or not args.is_valid_dashboardname(data['dashboardname']):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_NDBR_IDN)
    authorization.authorize_request(request=Requests.NEW_DASHBOARD,passport=passport)
    dashboard=dashboardapi.create_dashboard(uid=passport.uid, dashboardname=data['dashboardname'])
    if dashboard:
        webop=operation.NewDashboardOperation(uid=passport.uid,bid=dashboard['bid'])
        authop=webop.get_auth_operation()
        params=webop.get_params()
        try:
            if authupdate.update_resources(operation=authop, params=params):
                resp = response.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'bid':dashboard['bid'].hex})
                resp.add_message(messages.UpdateQuotesMessage(operation=authop, params=params))
                resp.add_message(messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DASHBOARD, parameters={'bid':dashboard['bid'].hex}))
                return resp
            else:
                deleteapi.delete_dashboard(bid=dashboard['bid'])
                return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWADB_NDBR_AUTHERR)
        except cassexcept.KomcassException:
            deleteapi.delete_dashboard(bid=dashboard['bid'])
            raise

@exceptions.ExceptionHandler
def delete_dashboard_request(passport, bid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_DDBR_IPSP)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_DDBR_IB)
    bid=uuid.UUID(bid)
    authorization.authorize_request(request=Requests.DELETE_DASHBOARD,passport=passport,bid=bid)
    resp=response.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    resp.add_message(messages.DeleteDashboardMessage(bid=bid))
    return resp

@exceptions.ExceptionHandler
def update_dashboard_config_request(passport, bid, data):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_UDBCR_IPSP)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_UDBCR_IB)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_UDBCR_ID)
    if not 'dashboardname' in data or not args.is_valid_dashboardname(data['dashboardname']):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_UDBCR_IDN)
    bid=uuid.UUID(bid)
    authorization.authorize_request(request=Requests.UPDATE_DASHBOARD_CONFIG,passport=passport,bid=bid)
    if dashboardapi.update_dashboard_config(bid=bid, dashboardname=data['dashboardname']):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def add_widget_request(passport, bid, wid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_AWR_IPSP)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_AWR_IB)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_AWR_IW)
    bid=uuid.UUID(bid)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.ADD_WIDGET_TO_DASHBOARD,passport=passport, bid=bid, wid=wid)
    if dashboardapi.add_widget_to_dashboard(bid=bid, wid=wid):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_widget_request(passport, bid, wid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_DWR_IPSP)
    if not args.is_valid_hex_uuid(bid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_DWR_IB)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWADB_DWR_IW)
    bid=uuid.UUID(bid)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.DELETE_WIDGET_FROM_DASHBOARD,passport=passport, bid=bid)
    if dashboardapi.delete_widget_from_dashboard(bid=bid, wid=wid):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

