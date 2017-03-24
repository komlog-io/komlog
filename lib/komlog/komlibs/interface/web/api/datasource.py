'''

This file defines the logic associated with web interface operations

'''
import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.passport import UserPassport, AgentPassport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response, operation
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datasource_data_request(passport, did, seq=None, tid=None):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSDR_IPSP)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSDR_ID)
    if seq and not args.is_valid_sequence(seq):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSDR_IS)
    if tid and not args.is_valid_hex_uuid(tid):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSDR_IT)
    did=uuid.UUID(did)
    if seq:
        ii=timeuuid.get_uuid1_from_custom_sequence(seq)
        ie=ii
    else:
        ie=timeuuid.uuid1()
        ii=None
    tid=uuid.UUID(tid) if tid else None
    try:
        authorization.authorize_request(request=Requests.GET_DATASOURCE_DATA,passport=passport,did=did,ii=ii,ie=ie, tid=tid)
    except authexcept.IntervalBoundsException as e:
        if ii and ii.time<e.data['date'].time:
            raise
        else:
            if ie.time < e.data['date'].time:
                e.error=Errors.E_IWADS_GDSDR_ADIF
                raise e
            else:
                data=datasourceapi.get_mapped_datasource_data(did, todate=ie, count=1)
                if data[0]['date'].time < e.data['date'].time:
                    e.error=Errors.E_IWADS_GDSDR_LDBL
                    raise e
    else:
        data=datasourceapi.get_mapped_datasource_data(did, fromdate=ii, todate=ie, count=1)
    datasource={}
    datasource['did']=did.hex
    datasource['ts']=timeuuid.get_unix_timestamp(data[0]['date'])
    datasource['seq']=timeuuid.get_custom_sequence(data[0]['date'])
    datasource['variables']=data[0]['variables']
    datasource['content']=data[0]['content']
    datasource['datapoints']=[]
    for datapoint in data[0]['datapoints']:
        datasource['datapoints'].append({'pid':datapoint['pid'].hex,'index':datapoint['position']})
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datasource)

@exceptions.ExceptionHandler
def get_datasources_config_request(passport):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSSCR_IPSP)
    authorization.authorize_request(request=Requests.GET_DATASOURCES_CONFIG,passport=passport)
    data=datasourceapi.get_datasources_config(uid=passport.uid)
    response_data=[]
    for datasource in data:
        response_data.append({'did':datasource['did'].hex, 'aid':datasource['aid'].hex, 'datasourcename':datasource['datasourcename']})
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_datasource_config_request(passport, did):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSCR_IPSP)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_GDSCR_ID)
    did=uuid.UUID(did)
    authorization.authorize_request(request=Requests.GET_DATASOURCE_CONFIG,passport=passport,did=did)
    data=datasourceapi.get_datasource_config(did)
    datasource={}
    datasource['did']=data['did'].hex
    datasource['aid']=data['aid'].hex
    if data['uid'] != passport.uid:
        owner = userapi.get_user_config(uid=data['uid'])
        datasource['datasourcename'] = ':'.join((owner['username'],data['datasourcename']))
    else:
        datasource['datasourcename']=data['datasourcename']
    if 'pids' in data:
        datasource['pids']=[pid.hex for pid in data['pids']]
    if 'wid' in data:
        datasource['wid']=data['wid'].hex
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datasource)

@exceptions.ExceptionHandler
def update_datasource_config_request(passport, did, data):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_UDSCR_IPSP)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_UDSCR_ID)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_UDSCR_IDA)
    if 'datasourcename' not in data or not args.is_valid_datasourcename(data['datasourcename']):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_UDSCR_IDN)
    did=uuid.UUID(did)
    authorization.authorize_request(request=Requests.UPDATE_DATASOURCE_CONFIG,passport=passport,did=did)
    datasourceapi.update_datasource_config(did=did,datasourcename=data['datasourcename'])
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_datasource_request(passport, datasourcename):
    if not isinstance(passport, AgentPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_NDSR_IPSP)
    if not args.is_valid_datasourcename(datasourcename):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_NDSR_IDN)
    authorization.authorize_request(request=Requests.NEW_DATASOURCE,passport=passport)
    datasource=datasourceapi.create_datasource(uid=passport.uid,aid=passport.aid,datasourcename=datasourcename)
    if datasource:
        webop=operation.NewDatasourceOperation(uid=passport.uid,aid=passport.aid,did=datasource['did'])
        authop=webop.get_auth_operation()
        params=webop.get_params()
        try:
            if authupdate.update_resources(operation=authop, params=params):
                resp=response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data={'did':datasource['did'].hex})
                resp.add_imc_message(messages.UpdateQuotesMessage(operation=authop, params=params))
                resp.add_imc_message(messages.NewDSWidgetMessage(uid=passport.uid, did=datasource['did']))
                resp.add_imc_message(messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, parameters={'did':datasource['did'].hex}))
                return resp
            else:
                deleteapi.delete_datasource(did=datasource['did'])
                return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWADS_NDSR_AUTHERR)
        except cassexcept.KomcassException:
            deleteapi.delete_datasource(did=datasource['did'])
            raise

@exceptions.ExceptionHandler
def delete_datasource_request(passport, did):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_DDSR_IPSP)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IWADS_DDSR_ID)
    did=uuid.UUID(did)
    authorization.authorize_request(request=Requests.DELETE_DATASOURCE,passport=passport,did=did)
    resp=response.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    resp.add_imc_message(messages.DeleteDatasourceMessage(did=did))
    return resp

