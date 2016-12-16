'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komfig import logging
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.widget import types
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response, operation
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def get_widgets_config_request(passport):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_GWSCR_IPSP)
    authorization.authorize_request(request=Requests.GET_WIDGETS_CONFIG,passport=passport)
    data=widgetapi.get_widgets_config(uid=passport.uid)
    response_data=[]
    for widget in data:
        reg={}
        if widget['type']==types.DATASOURCE:
            reg['type']=types.DATASOURCE
            reg['wid']=widget['wid'].hex
            reg['widgetname']=widget['widgetname']
            reg['did']=widget['did'].hex
        elif widget['type']==types.DATAPOINT:
            reg['type']=types.DATAPOINT
            reg['wid']=widget['wid'].hex
            reg['widgetname']=widget['widgetname']
            reg['pid']=widget['pid'].hex
        elif widget['type']==types.MULTIDP:
            reg['type']=types.MULTIDP
            reg['wid']=widget['wid'].hex
            reg['widgetname']=widget['widgetname']
            reg['datapoints']=[pid.hex for pid in widget['datapoints']]
            reg['view']=widget['active_visualization']
        elif widget['type'] in [types.HISTOGRAM, types.LINEGRAPH, types.TABLE]:
            reg['type']=widget['type']
            reg['wid']=widget['wid'].hex
            reg['widgetname']=widget['widgetname']
            reg['datapoints']=[]
            for pid in widget['datapoints']:
                if pid in widget['colors'].keys():
                    color=widget['colors'][pid]
                else:
                    color=''
                reg['datapoints'].append({'pid':pid.hex,'color':color})
        response_data.append(reg)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_widget_config_request(passport, wid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_GWCR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_GWCR_IW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.GET_WIDGET_CONFIG,passport=passport,wid=wid)
    data=widgetapi.get_widget_config(wid=wid)
    widget={'wid':wid.hex}
    if data['uid'] != passport.uid and data['type'] in (types.DATASOURCE,types.DATAPOINT):
        owner = userapi.get_user_config(uid=data['uid'])
        widget['widgetname'] = ':'.join((owner['username'],data['widgetname']))
    else:
        widget['widgetname']=data['widgetname']
    if data['type']==types.DATASOURCE:
        widget['type']=types.DATASOURCE
        widget['did']=data['did'].hex
    elif data['type']==types.DATAPOINT:
        widget['type']=types.DATAPOINT
        widget['pid']=data['pid'].hex
    elif data['type']==types.MULTIDP:
        widget['type']=types.MULTIDP
        widget['datapoints']=[pid.hex for pid in data['datapoints']]
        widget['view']=data['active_visualization']
    elif data['type'] in [types.HISTOGRAM, types.LINEGRAPH, types.TABLE]:
        widget['type']=data['type']
        widget['datapoints']=[]
        for pid in data['datapoints']:
            if pid in data['colors'].keys():
                color=data['colors'][pid]
            else:
                color=''
            widget['datapoints'].append({'pid':pid.hex,'color':color})
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=widget)

@exceptions.ExceptionHandler
def delete_widget_request(passport, wid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_DWR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_DWR_IW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.DELETE_WIDGET,passport=passport,wid=wid)
    resp=response.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    resp.add_message(messages.DeleteWidgetMessage(wid=wid))
    return resp

@exceptions.ExceptionHandler
def new_widget_request(passport, data):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_NWR_IPSP)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_NWR_ID)
    authorization.authorize_request(request=Requests.NEW_WIDGET,passport=passport)
    if not 'type' in data or not data['type'] in [types.MULTIDP, types.LINEGRAPH, types.TABLE, types.HISTOGRAM]:
        raise exceptions.BadParametersException(error=Errors.E_IWAW_NWR_IT)
    if not 'widgetname' in data or not args.is_valid_widgetname(data['widgetname']):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_NWR_IWN)
    widget=None
    if data['type']==types.MULTIDP:
        widget=widgetapi.new_widget_multidp(uid=passport.uid, widgetname=data['widgetname'])
    if data['type']==types.LINEGRAPH:
        widget=widgetapi.new_widget_linegraph(uid=passport.uid, widgetname=data['widgetname'])
    elif data['type']==types.TABLE:
        widget=widgetapi.new_widget_table(uid=passport.uid, widgetname=data['widgetname'])
    elif data['type']==types.HISTOGRAM:
        widget=widgetapi.new_widget_histogram(uid=passport.uid, widgetname=data['widgetname'])
    if widget:
        webop=operation.NewWidgetOperation(uid=widget['uid'], wid=widget['wid'])
        authop=webop.get_auth_operation()
        params=webop.get_params()
        try:
            if authupdate.update_resources(operation=authop, params=params):
                resp=response.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'wid':widget['wid'].hex})
                resp.add_message(messages.UpdateQuotesMessage(operation=authop, params=params))
                resp.add_message(messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_WIDGET, parameters={'wid':widget['wid'].hex}))
                return resp
            else:
                deleteapi.delete_widget(wid=widget['wid'])
                return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWAW_NWR_AUTHERR.value)
        except cassexcept.KomcassException:
            deleteapi.delete_widget(wid=widget['wid'])
            raise
    else:
        return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWAW_NWR_WCE.value)

@exceptions.ExceptionHandler
def add_datapoint_request(passport, wid, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_ADPR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_ADPR_IW)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_ADPR_IP)
    wid=uuid.UUID(wid)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.ADD_DATAPOINT_TO_WIDGET,passport=passport, wid=wid, pid=pid)
    if widgetapi.add_datapoint_to_widget(wid=wid, pid=pid):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWAW_ADPR_OE.value)

@exceptions.ExceptionHandler
def delete_datapoint_request(passport, wid, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_DDPR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_DDPR_IW)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_DDPR_IP)
    wid=uuid.UUID(wid)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.DELETE_DATAPOINT_FROM_WIDGET,passport=passport, wid=wid)
    if widgetapi.delete_datapoint_from_widget(wid=wid, pid=pid):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWAW_DDPR_OE.value)

@exceptions.ExceptionHandler
def update_widget_config_request(passport, wid, data):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IW)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_ID)
    if not 'widgetname' in data and not 'datapoints' in data and not 'view' in data:
        raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_EMP)
    if 'widgetname' in data and not args.is_valid_widgetname(data['widgetname']):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IWN)
    if 'datapoints' in data:
        if not isinstance(data['datapoints'],list):
            raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IDP)
        if len(data['datapoints'])==0:
            raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_EMDP)
        for element in data['datapoints']:
            if not args.is_valid_dict(element):
                raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IDPE)
            if not 'pid' in element:
                raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_EPNF)
            if not 'color' in element:
                raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_ECNF)
            if not args.is_valid_hex_uuid(element['pid']):
                raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IEP)
            if not args.is_valid_hexcolor(element['color']):
                raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IEC)
    if 'view' in data and not args.is_valid_int(data['view']):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_UWCR_IVW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.UPDATE_WIDGET_CONFIG,passport=passport, wid=wid)
    widgetname=data['widgetname'] if 'widgetname' in data else None
    colors=dict()
    if 'datapoints' in data:
        for element in data['datapoints']:
            colors[uuid.UUID(element['pid'])]=element['color']
    view=data['view'] if 'view' in data else None
    if widgetapi.update_widget_config(wid=wid, widgetname=widgetname, colors=colors, active_visualization=view):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWAW_UWCR_OE.value)

@exceptions.ExceptionHandler
def get_related_widgets_request(passport, wid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_GRWR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWAW_GRWR_IW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.GET_WIDGET_CONFIG,passport=passport,wid=wid)
    data=widgetapi.get_related_widgets(wid=wid)
    response_data=[]
    for widget in data:
        response_data.append({'type':widget['type'],\
                              'wid':widget['wid'].hex,\
                              'widgetname':widget['widgetname']})
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

