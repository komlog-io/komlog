'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.widget import types
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def get_widgets_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GWSCR_IU)
    uid=userapi.get_uid(username=username)
    data=widgetapi.get_widgets_config(uid=uid)
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
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_widget_config_request(username, wid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GWCR_IU)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GWCR_IW)
    wid=uuid.UUID(wid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_WIDGET_CONFIG,uid=uid,wid=wid)
    data=widgetapi.get_widget_config(wid=wid)
    widget={'wid':wid.hex}
    widget['widgetname']=data['widgetname']
    if data['type']==types.DATASOURCE:
        widget['type']=types.DATASOURCE
        widget['did']=data['did'].hex
    elif data['type']==types.DATAPOINT:
        widget['type']=types.DATAPOINT
        widget['pid']=data['pid'].hex
    elif data['type'] in [types.HISTOGRAM, types.LINEGRAPH, types.TABLE]:
        widget['type']=data['type']
        widget['wid']=data['wid'].hex
        widget['datapoints']=[]
        for pid in data['datapoints']:
            if pid in data['colors'].keys():
                color=data['colors'][pid]
            else:
                color=''
            widget['datapoints'].append({'pid':pid.hex,'color':color})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=widget)

@exceptions.ExceptionHandler
def delete_widget_request(username, wid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DWR_IU)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DWR_IW)
    wid=uuid.UUID(wid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_WIDGET,uid=uid,wid=wid)
    message=messages.DeleteWidgetMessage(wid=wid)
    msgapi.send_message(msg=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def new_widget_request(username, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_IU)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_ID)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_WIDGET, uid=uid)
    if not 'type' in data or not data['type'] in [types.LINEGRAPH, types.TABLE, types.HISTOGRAM]:
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_IT)
    if not 'widgetname' in data or not args.is_valid_widgetname(data['widgetname']):
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_IWN)
    widget=None
    if data['type']==types.LINEGRAPH:
        widget=widgetapi.new_widget_linegraph(uid=uid, widgetname=data['widgetname'])
    elif data['type']==types.TABLE:
        widget=widgetapi.new_widget_table(uid=uid, widgetname=data['widgetname'])
    elif data['type']==types.HISTOGRAM:
        widget=widgetapi.new_widget_histogram(uid=uid, widgetname=data['widgetname'])
    if widget:
        operation=weboperations.NewWidgetOperation(uid=widget['uid'], wid=widget['wid'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.UserEventMessage(uid=uid,event_type=eventstypes.NEW_WIDGET, parameters={'wid':widget['wid'].hex, 'widgetname':data['widgetname']})
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'wid':widget['wid'].hex})
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

@exceptions.ExceptionHandler
def add_datapoint_request(username, wid, pid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_ADPR_IU)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_ADPR_IW)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_ADPR_IP)
    wid=uuid.UUID(wid)
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.ADD_DATAPOINT_TO_WIDGET, uid=uid, wid=wid, pid=pid)
    if widgetapi.add_datapoint_to_widget(wid=wid, pid=pid):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_datapoint_request(username, wid, pid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DDPR_IU)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DDPR_IW)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DDPR_IP)
    wid=uuid.UUID(wid)
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_DATAPOINT_FROM_WIDGET, uid=uid, wid=wid)
    if widgetapi.delete_datapoint_from_widget(wid=wid, pid=pid):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def update_widget_config_request(username, wid, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IU)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IW)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_ID)
    if not 'widgetname' in data and not 'datapoints' in data:
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_EMP)
    if 'widgetname' in data and not args.is_valid_widgetname(data['widgetname']):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IWN)
    if 'datapoints' in data:
        if not isinstance(data['datapoints'],list):
            raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IDP)
        if len(data['datapoints'])==0:
            raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_EMDP)
        for element in data['datapoints']:
            if not args.is_valid_dict(element):
                raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IDPE)
            if not 'pid' in element:
                raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_EPNF)
            if not 'color' in element:
                raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_ECNF)
            if not args.is_valid_hex_uuid(element['pid']):
                raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IEP)
            if not args.is_valid_hexcolor(element['color']):
                raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IEC)
    wid=uuid.UUID(wid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.UPDATE_WIDGET_CONFIG, uid=uid, wid=wid)
    widgetname=data['widgetname'] if 'widgetname' in data else None
    datapoints=None
    if 'datapoints' in data:
        colors=dict()
        for element in data['datapoints']:
            colors[uuid.UUID(element['pid'])]=element['color']
    if widgetapi.update_widget_config(wid=wid, widgetname=widgetname, colors=colors):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

