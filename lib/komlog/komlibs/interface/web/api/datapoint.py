'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komfig import logging
from komlog.komimc import api as msgapi
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web.operations import weboperations
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datapoint_data_request(passport, pid, start_date, end_date, tid=None):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPDR_IPSP)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPDR_IP)
    if start_date and not args.is_valid_string_float(start_date):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPDR_ISD)
    if end_date and not args.is_valid_string_float(end_date):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPDR_IED)
    if tid and not args.is_valid_hex_uuid(tid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPDR_IT)
    pid=uuid.UUID(pid)
    if start_date and end_date and start_date>end_date:
        start_date,end_date=end_date,start_date
    ii=timeuuid.min_uuid_from_time(timestamp=float(start_date)) if start_date else None
    ie=timeuuid.max_uuid_from_time(timestamp=float(end_date)) if end_date else None
    tid=uuid.UUID(tid) if tid else None
    try:
        authorization.authorize_request(request=Requests.GET_DATAPOINT_DATA,passport=passport,pid=pid,ii=ii,ie=ie,tid=tid)
    except authexcept.IntervalBoundsException as e:
        if ie and ie.time<e.data['date'].time:
            raise e
        else:
            ie=timeuuid.max_uuid_from_time(timestamp=float(end_date)) if end_date else None
        if not ii:
            ii=e.data['date']
        elif ii and ii.time<e.data['date'].time:
            ii=e.data['date']
    data=datapointapi.get_datapoint_data(pid, fromdate=ii, todate=ie, count=300) #300 regs max
    response_data=[]
    for point in data:
        response_data.append({
            'ts':timeuuid.get_unix_timestamp(point['date']),
            'value':int(point['value']) if point['value']%1==0 else float(point['value'])
        })
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_datapoint_config_request(passport, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPCR_IPSP)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_GDPCR_IP)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.GET_DATAPOINT_CONFIG,passport=passport,pid=pid)
    data=datapointapi.get_datapoint_config(pid=pid)
    datapoint={}
    datapoint['pid']=data['pid'].hex
    datapoint['color']=data['color']
    datapoint['datapointname']=data['datapointname']
    if data['did'] is not None:
        datapoint['did']=data['did'].hex
    if 'decimalseparator' in data:
        datapoint['decimalseparator']=data['decimalseparator']
    if 'wid' in data:
        datapoint['wid']=data['wid'].hex
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datapoint)

@exceptions.ExceptionHandler
def update_datapoint_config_request(passport, pid, data):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_UDPCR_IPSP)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_UDPCR_IP)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_UDPCR_ID)
    if not 'datapointname' in data and not 'color' in data:
        raise exceptions.BadParametersException(error=Errors.E_IWADP_UDPCR_EMP)
    if 'datapointname' in data and not args.is_valid_datapointname(data['datapointname']):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_UDPCR_IDN)
    if 'color' in data and not args.is_valid_hexcolor(data['color']):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_UDPCR_IC)
    datapointname=data['datapointname'] if 'datapointname' in data else None
    color=data['color'] if 'color' in data else None
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.UPDATE_DATAPOINT_CONFIG,passport=passport,pid=pid)
    datapointapi.update_datapoint_config(pid=pid,datapointname=datapointname, color=color)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_datasource_datapoint_request(passport, did, sequence, position, length, datapointname):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_NDPR_IPSP)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_NDPR_ID)
    if not args.is_valid_sequence(sequence):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_NDPR_IS)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_NDPR_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_NDPR_IL)
    if not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_NDPR_IDN)
    did=uuid.UUID(did)
    authorization.authorize_request(request=Requests.NEW_DATASOURCE_DATAPOINT,passport=passport,did=did)
    date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
    message=messages.MonitorVariableMessage(uid=passport.uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
    msgapi.send_message(message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def mark_positive_variable_request(passport, pid, sequence, position, length):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MPVR_IPSP)
    if not args.is_valid_sequence(sequence):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MPVR_IS)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MPVR_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MPVR_IL)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MPVR_IP)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.MARK_POSITIVE_VARIABLE,passport=passport,pid=pid)
    date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
    datapoints_to_update=datapointapi.mark_positive_variable(pid=pid, date=date, position=position, length=length)
    if datapoints_to_update!=None:
        for datapoint in datapoints_to_update:
            message=messages.FillDatapointMessage(pid=pid, date=date)
            msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, errors=Errors.UNKNOWN.value)

@exceptions.ExceptionHandler
def mark_negative_variable_request(passport, pid, sequence, position, length):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MNVR_IPSP)
    if not args.is_valid_sequence(sequence):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MNVR_IS)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MNVR_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MNVR_IL)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_MNVR_IP)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.MARK_NEGATIVE_VARIABLE,passport=passport,pid=pid)
    date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
    datapoints_to_update=datapointapi.mark_negative_variable(pid=pid, date=date, position=position, length=length)
    if datapoints_to_update!=None:
        for datapoint in datapoints_to_update:
            message=messages.FillDatapointMessage(pid=pid, date=date)
            msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, errors=Errors.UNKNOWN.value)

@exceptions.ExceptionHandler
def delete_datapoint_request(passport, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_DDPR_IPSP)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_DDPR_IP)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.DELETE_DATAPOINT,passport=passport,pid=pid)
    message=messages.DeleteDatapointMessage(pid=pid)
    msgapi.send_message(msg=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def dissociate_datapoint_from_datasource_request(passport, pid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_DDPFDS_IPSP)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_IWADP_DDPFDS_IP)
    pid=uuid.UUID(pid)
    authorization.authorize_request(request=Requests.DISSOCIATE_DATAPOINT_FROM_DATASOURCE,passport=passport,pid=pid)
    result=deleteapi.dissociate_datapoint_from_datasource(pid=pid)
    if result['did'] is not None:
        operation=weboperations.DissociateDatapointFromDatasourceOperation(pid=pid, did=result['did'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op.value, params=params)
        msgapi.send_message(message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

