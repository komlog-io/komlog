'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.widget import types
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def get_widgets_config_request(username):
    if args.is_valid_username(username):
        data=widgetapi.get_widgets_config(username=username)
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
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_widget_config_request(username, wid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid):
        wid=uuid.UUID(wid)
        authorization.authorize_request(request=requests.GET_WIDGET_CONFIG,username=username,wid=wid)
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
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_widget_request(username, wid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid):
        wid=uuid.UUID(wid)
        authorization.authorize_request(request=requests.DELETE_WIDGET,username=username,wid=wid)
        message=messages.DeleteWidgetMessage(wid=wid)
        msgapi.send_message(msg=message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_widget_request(username, data):
    if args.is_valid_username(username) and args.is_valid_dict(data):
        authorization.authorize_request(request=requests.NEW_WIDGET, username=username)
        if not 'type' in data or not data['type'] in [types.LINEGRAPH, types.TABLE, types.HISTOGRAM] or not 'widgetname' in data or not args.is_valid_widgetname(data['widgetname']):
            raise exceptions.BadParametersException()
        widget=None
        if data['type']==types.LINEGRAPH:
            widget=widgetapi.new_widget_linegraph(username=username, widgetname=data['widgetname'])
        elif data['type']==types.TABLE:
            widget=widgetapi.new_widget_table(username=username, widgetname=data['widgetname'])
        elif data['type']==types.HISTOGRAM:
            widget=widgetapi.new_widget_histogram(username=username, widgetname=data['widgetname'])
        if widget:
            operation=weboperations.NewWidgetOperation(uid=widget['uid'], wid=widget['wid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'wid':widget['wid'].hex})
        else:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def add_datapoint_request(username, wid, pid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid) and args.is_valid_hex_uuid(pid):
        wid=uuid.UUID(wid)
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.ADD_DATAPOINT_TO_WIDGET, username=username, wid=wid, pid=pid)
        if widgetapi.add_datapoint_to_widget(wid=wid, pid=pid):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_datapoint_request(username, wid, pid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid) and args.is_valid_hex_uuid(pid):
        wid=uuid.UUID(wid)
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.DELETE_DATAPOINT_FROM_WIDGET, username=username, wid=wid)
        if widgetapi.delete_datapoint_from_widget(wid=wid, pid=pid):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_widget_config_request(username, wid, data):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid) and args.is_valid_dict(data):
        wid=uuid.UUID(wid)
        if not 'widgetname' in data and not 'colors' in data:
            raise exceptions.BadParametersException()
        if 'widgetname' in data and not args.is_valid_widgetname(data['widgetname']):
            raise exceptions.BadParametersException()
        if 'colors' in data:
            if not isinstance(data['colors'],list):
                raise exceptions.BadParametersException()
            if len(data['colors'])==0:
                raise exceptions.BadParametersException()
            for element in data['colors']:
                if not args.is_valid_dict(element) or not 'pid' in element or not 'color' in element or not args.is_valid_hex_uuid(element['pid']) or not args.is_valid_hexcolor(element['color']):
                    raise exceptions.BadParametersException()
        authorization.authorize_request(request=requests.UPDATE_WIDGET_CONFIG, username=username, wid=wid)
        widgetname=data['widgetname'] if 'widgetname' in data else None
        colors=None
        if 'colors' in data:
            colors=dict()
            for element in data['colors']:
                colors[uuid.UUID(element['pid'])]=element['color']
        if widgetapi.update_widget_config(wid=wid, widgetname=widgetname, colors=colors):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

