#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komlibs.auth import authorization
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.widget import types
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def get_widgets_config_request(username):
    if args.is_valid_username(username):
        data=widgetapi.get_widgets_config(username=username)
        response_data=[]
        for widget in data:
            reg={}
            if widget['type']==types.DS_WIDGET:
                reg['type']=types.DS_WIDGET
                reg['wid']=widget['wid'].hex
                reg['did']=widget['did'].hex
            elif widget['type']==types.DP_WIDGET:
                reg['type']=types.DP_WIDGET
                reg['wid']=widget['wid'].hex
                reg['pid']=widget['pid'].hex
            response_data.append(reg)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_widget_config_request(username, wid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid):
        wid=uuid.UUID(wid)
        authorization.authorize_request(request='GetWidgetConfigRequest',username=username,wid=wid)
        data=widgetapi.get_widget_config(wid=wid)
        widget={'wid':wid.hex}
        if data['type']==types.DS_WIDGET:
            widget['type']=types.DS_WIDGET
            widget['did']=data['did'].hex
        elif widget['type']==types.DP_WIDGET:
            widget['type']=types.DP_WIDGET
            widget['pid']=data['pid'].hex
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=widget)
    else:
        raise exceptions.BadParametersException()

