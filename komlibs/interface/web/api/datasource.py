#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''
import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datasource_data_request(username, did, seq=None):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(did):
        if seq and not args.is_valid_sequence(seq):
            raise exceptions.BadParametersException()
        did=uuid.UUID(did)
        if seq:
            ii=timeuuid.get_uuid1_from_custom_sequence(seq)
            ie=ii
        else:
            ii=None
            ie=None
        authorization.authorize_request(request=requests.GET_DATASOURCE_DATA,username=username,did=did,ii=ii,ie=ie)
        if ii:
            data=datasourceapi.get_datasource_data(did,date=ii)
        else:
            data=datasourceapi.get_last_processed_datasource_data(did)
        datasource={}
        datasource['did']=data['did'].hex
        datasource['timestamp']=timeuuid.get_unix_timestamp(data['date'])
        datasource['sequence']=timeuuid.get_custom_sequence(data['date'])
        datasource['variables']=data['variables']
        datasource['content']=data['content']
        datasource['datapoints']=[]
        for datapoint in data['datapoints']:
            datasource['datapoints'].append({'pid':datapoint['pid'].hex,'index':datapoint['position']})
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datasource)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def upload_datasource_data_request(username, aid, did, content, destination):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(aid) and args.is_valid_hex_uuid(did) and args.is_valid_datasource_content(content) and args.is_valid_string(destination):
        aid=uuid.UUID(aid)
        did=uuid.UUID(did)
        authorization.authorize_request(request=requests.POST_DATASOURCE_DATA,username=username,aid=aid,did=did)
        destfile=datasourceapi.upload_datasource_data(did,content,destination)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_datasources_config_request(username):
    if args.is_valid_username(username):
        data=datasourceapi.get_datasources_config(username=username)
        response_data=[]
        for datasource in data:
            response_data.append({'did':datasource['did'].hex, 'aid':datasource['aid'].hex, 'datasourcename':datasource['datasourcename']})
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_datasource_config_request(username, did):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(did):
        did=uuid.UUID(did)
        authorization.authorize_request(request=requests.GET_DATASOURCE_CONFIG,username=username,did=did)
        data=datasourceapi.get_datasource_config(did)
        datasource={}
        datasource['did']=data['did'].hex
        datasource['aid']=data['aid'].hex
        datasource['datasourcename']=data['datasourcename']
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datasource)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_datasource_config_request(username, did, data):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(did) and args.is_valid_dict(data):
        if 'datasourcename' not in data or not args.is_valid_datasourcename(data['datasourcename']):
            raise exceptions.BadParametersException()
        did=uuid.UUID(did)
        authorization.authorize_request(request=requests.UPDATE_DATASOURCE_CONFIG,username=username,did=did)
        datasourceapi.update_datasource_config(did=did,datasourcename=data['datasourcename'])
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_datasource_request(username, aid, datasourcename):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(aid) and args.is_valid_datasourcename(datasourcename):
        aid=uuid.UUID(aid)
        authorization.authorize_request(request=requests.NEW_DATASOURCE,username=username,aid=aid)
        datasource=datasourceapi.create_datasource(username=username,aid=aid,datasourcename=datasourcename)
        if datasource:
            operation=weboperations.NewDatasourceOperation(uid=datasource['uid'],aid=aid,did=datasource['did'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op,params=params)
            msgapi.send_message(message)
            message=messages.NewDSWidgetMessage(username=username, did=datasource['did'])
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data={'did':datasource['did'].hex})
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_datasource_request(username, did):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(did):
        did=uuid.UUID(did)
        authorization.authorize_request(request=requests.DELETE_DATASOURCE,username=username,did=did)
        message=messages.DeleteDatasourceMessage(did=did)
        msgapi.send_message(message=message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

