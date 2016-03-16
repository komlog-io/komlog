'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization
from komlibs.auth.requests import Requests
from komlibs.auth.passport import Passport
from komlibs.auth import update as authupdate
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.widget import types
from komlibs.gestaccount.common import delete as deleteapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def get_widgets_config_request(passport):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GWSCR_IPSP)
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
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_widget_config_request(passport, wid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GWCR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GWCR_IW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.GET_WIDGET_CONFIG,passport=passport,wid=wid)
    data=widgetapi.get_widget_config(wid=wid)
    widget={'wid':wid.hex}
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
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=widget)

@exceptions.ExceptionHandler
def delete_widget_request(passport, wid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DWR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DWR_IW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.DELETE_WIDGET,passport=passport,wid=wid)
    message=messages.DeleteWidgetMessage(wid=wid)
    msgapi.send_message(msg=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def new_widget_request(passport, data):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_IPSP)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_ID)
    authorization.authorize_request(request=Requests.NEW_WIDGET,passport=passport)
    if not 'type' in data or not data['type'] in [types.MULTIDP, types.LINEGRAPH, types.TABLE, types.HISTOGRAM]:
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_IT)
    if not 'widgetname' in data or not args.is_valid_widgetname(data['widgetname']):
        raise exceptions.BadParametersException(error=errors.E_IWAW_NWR_IWN)
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
        operation=weboperations.NewWidgetOperation(uid=widget['uid'], wid=widget['wid'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        if authupdate.update_resources(operation=auth_op, params=params):
            message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            message=messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_WIDGET, parameters={'wid':widget['wid'].hex})
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'wid':widget['wid'].hex})
        else:
            deleteapi.delete_widget(wid=widget['wid'])
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=errors.E_IWAW_NWR_AUTHERR)

    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=errors.E_IWAW_NWR_WCE)

@exceptions.ExceptionHandler
def add_datapoint_request(passport, wid, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_ADPR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_ADPR_IW)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_ADPR_IP)
    wid=uuid.UUID(wid)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.ADD_DATAPOINT_TO_WIDGET,passport=passport, wid=wid, pid=pid)
    if widgetapi.add_datapoint_to_widget(wid=wid, pid=pid):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_datapoint_request(passport, wid, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DDPR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DDPR_IW)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_DDPR_IP)
    wid=uuid.UUID(wid)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.DELETE_DATAPOINT_FROM_WIDGET,passport=passport, wid=wid)
    if widgetapi.delete_datapoint_from_widget(wid=wid, pid=pid):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def update_widget_config_request(passport, wid, data):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IW)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_ID)
    if not 'widgetname' in data and not 'datapoints' in data and not 'view' in data:
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
    if 'view' in data and not args.is_valid_int(data['view']):
        raise exceptions.BadParametersException(error=errors.E_IWAW_UWCR_IVW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.UPDATE_WIDGET_CONFIG,passport=passport, wid=wid)
    widgetname=data['widgetname'] if 'widgetname' in data else None
    colors=dict()
    if 'datapoints' in data:
        for element in data['datapoints']:
            colors[uuid.UUID(element['pid'])]=element['color']
    view=data['view'] if 'view' in data else None
    if widgetapi.update_widget_config(wid=wid, widgetname=widgetname, colors=colors, active_visualization=view):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def get_related_widgets_request(passport, wid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GRWR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWAW_GRWR_IW)
    wid=uuid.UUID(wid)
    authorization.authorize_request(request=Requests.GET_WIDGET_CONFIG,passport=passport,wid=wid)
    data=widgetapi.get_related_widgets(wid=wid)
    response_data=[]
    for widget in data:
        response_data.append({'type':widget['type'],\
                              'wid':widget['wid'].hex,\
                              'widgetname':widget['widgetname']})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

