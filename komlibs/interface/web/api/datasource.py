#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''
import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datasource_data_request(username, did, seq=None, tid=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSDR_IU)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSDR_ID)
    if seq and not args.is_valid_sequence(seq):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSDR_IS)
    if tid and not args.is_valid_hex_uuid(tid):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSDR_IT)
    did=uuid.UUID(did)
    if seq:
        ii=timeuuid.get_uuid1_from_custom_sequence(seq)
        ie=ii
    else:
        ii=None
        ie=None
    tid=uuid.UUID(tid) if tid else None
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_DATASOURCE_DATA,uid=uid,did=did,ii=ii,ie=ie, tid=tid)
    if ii:
        data=datasourceapi.get_datasource_data(did,date=ii)
    else:
        data=datasourceapi.get_last_processed_datasource_data(did)
    datasource={}
    datasource['did']=data['did'].hex
    datasource['ts']=timeuuid.get_unix_timestamp(data['date'])
    datasource['seq']=timeuuid.get_custom_sequence(data['date'])
    datasource['variables']=data['variables']
    datasource['content']=data['content']
    datasource['datapoints']=[]
    for datapoint in data['datapoints']:
        datasource['datapoints'].append({'pid':datapoint['pid'].hex,'index':datapoint['position']})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datasource)

@exceptions.ExceptionHandler
def upload_datasource_data_request(username, aid, did, content, destination):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSDR_IU)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSDR_IA)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSDR_ID)
    if not args.is_valid_datasource_content(content):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSDR_IDC)
    if not args.is_valid_string(destination):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSDR_IDST)
    aid=uuid.UUID(aid)
    did=uuid.UUID(did)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.POST_DATASOURCE_DATA,uid=uid,aid=aid,did=did)
    destfile=datasourceapi.upload_datasource_data(did,content,destination)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def get_datasources_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSSCR_IU)
    uid=userapi.get_uid(username=username)
    data=datasourceapi.get_datasources_config(uid=uid)
    response_data=[]
    for datasource in data:
        response_data.append({'did':datasource['did'].hex, 'aid':datasource['aid'].hex, 'datasourcename':datasource['datasourcename']})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_datasource_config_request(username, did):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSCR_IU)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_IWADS_GDSCR_ID)
    did=uuid.UUID(did)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_DATASOURCE_CONFIG,uid=uid,did=did)
    data=datasourceapi.get_datasource_config(did)
    datasource={}
    datasource['did']=data['did'].hex
    datasource['aid']=data['aid'].hex
    datasource['datasourcename']=data['datasourcename']
    if 'pids' in data:
        datasource['pids']=[pid.hex for pid in data['pids']]
    if 'wid' in data:
        datasource['wid']=data['wid'].hex
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datasource)

@exceptions.ExceptionHandler
def update_datasource_config_request(username, did, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSCR_IU)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSCR_ID)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSCR_IDA)
    if 'datasourcename' not in data or not args.is_valid_datasourcename(data['datasourcename']):
        raise exceptions.BadParametersException(error=errors.E_IWADS_UDSCR_IDN)
    did=uuid.UUID(did)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.UPDATE_DATASOURCE_CONFIG,uid=uid,did=did)
    datasourceapi.update_datasource_config(did=did,datasourcename=data['datasourcename'])
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_datasource_request(username, aid, datasourcename):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_NDSR_IU)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_IWADS_NDSR_IA)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=errors.E_IWADS_NDSR_IDN)
    aid=uuid.UUID(aid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_DATASOURCE,uid=uid,aid=aid)
    datasource=datasourceapi.create_datasource(uid=uid,aid=aid,datasourcename=datasourcename)
    if datasource:
        operation=weboperations.NewDatasourceOperation(uid=uid,aid=aid,did=datasource['did'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op,params=params)
        msgapi.send_message(message)
        message=messages.NewDSWidgetMessage(uid=uid, did=datasource['did'])
        msgapi.send_message(message)
        message=messages.UserEventMessage(uid=uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, parameters={'did':datasource['did'].hex})
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data={'did':datasource['did'].hex})

@exceptions.ExceptionHandler
def delete_datasource_request(username, did):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADS_DDSR_IU)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_IWADS_DDSR_ID)
    did=uuid.UUID(did)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_DATASOURCE,uid=uid,did=did)
    message=messages.DeleteDatasourceMessage(did=did)
    msgapi.send_message(message=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

