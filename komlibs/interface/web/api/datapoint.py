#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

import uuid
import time
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datapoint_data_request(username, pid, start_date, end_date, iseq=None, eseq=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_IU)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_IP)
    if start_date and not args.is_valid_string_float(start_date):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_ISD)
    if end_date and not args.is_valid_string_float(end_date):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_IED)
    if iseq and not args.is_valid_sequence(iseq):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_IIS)
    if eseq and not args.is_valid_sequence(eseq):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_IES)
    if bool(iseq) ^ bool(eseq):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPDR_OOS)
    pid=uuid.UUID(pid)
    ii=timeuuid.get_uuid1_from_custom_sequence(iseq) if iseq else None
    ie=timeuuid.get_uuid1_from_custom_sequence(eseq) if eseq else None
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_DATAPOINT_DATA,uid=uid,pid=pid,ii=ii,ie=ie)
    end_date=timeuuid.uuid1(seconds=float(end_date)) if end_date else None
    start_date=timeuuid.uuid1(seconds=float(start_date)) if start_date else None
    if ii or ie:
        if ii>start_date:
            start_date=ii
        if ie<end_date:
            end_date=ie
    if start_date>end_date:
        tmp_date=end_date
        end_date=start_date
        start_date=tmp_date
    data=datapointapi.get_datapoint_data(pid, fromdate=start_date, todate=end_date)
    response_data=[]
    for point in data:
        response_data.append({'ts':timeuuid.get_unix_timestamp(point['date']),
                              'value':int(point['value']) if point['value']%1==0 else float(point['value'])
                             })
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_datapoint_config_request(username, pid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPCR_IU)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWADP_GDPCR_IP)
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_DATAPOINT_CONFIG,uid=uid,pid=pid)
    data=datapointapi.get_datapoint_config(pid=pid)
    datapoint={}
    datapoint['did']=data['did'].hex
    datapoint['pid']=data['pid'].hex
    datapoint['color']=data['color']
    datapoint['datapointname']=data['datapointname']
    if 'decimalseparator' in data:
        datapoint['decimalseparator']=data['decimalseparator']
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datapoint)

@exceptions.ExceptionHandler
def update_datapoint_config_request(username, pid, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_UDPCR_IU)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWADP_UDPCR_IP)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWADP_UDPCR_ID)
    if not 'datapointname' in data and not 'color' in data:
        raise exceptions.BadParametersException(error=errors.E_IWADP_UDPCR_EMP)
    if 'datapointname' in data and not args.is_valid_datapointname(data['datapointname']):
        raise exceptions.BadParametersException(error=errors.E_IWADP_UDPCR_IDN)
    if 'color' in data and not args.is_valid_hexcolor(data['color']):
        raise exceptions.BadParametersException(error=errors.E_IWADP_UDPCR_IC)
    datapointname=data['datapointname'] if 'datapointname' in data else None
    color=data['color'] if 'color' in data else None
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.UPDATE_DATAPOINT_CONFIG,uid=uid,pid=pid)
    datapointapi.update_datapoint_config(pid=pid,datapointname=datapointname, color=color)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_datapoint_request(username, did, sequence, position, length, datapointname):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_NDPR_IU)
    if not args.is_valid_hex_uuid(did):
        raise exceptions.BadParametersException(error=errors.E_IWADP_NDPR_ID)
    if not args.is_valid_sequence(sequence):
        raise exceptions.BadParametersException(error=errors.E_IWADP_NDPR_IS)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=errors.E_IWADP_NDPR_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=errors.E_IWADP_NDPR_IL)
    if not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException(error=errors.E_IWADP_NDPR_IDN)
    did=uuid.UUID(did)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_DATAPOINT,uid=uid,did=did)
    date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
    message=messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
    msgapi.send_message(message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def mark_positive_variable_request(username, pid, sequence, position, length):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MPVR_IU)
    if not args.is_valid_sequence(sequence):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MPVR_IS)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MPVR_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MPVR_IL)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MPVR_IP)
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.MARK_POSITIVE_VARIABLE,uid=uid,pid=pid)
    date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
    datapoints_to_update=datapointapi.mark_positive_variable(pid=pid, date=date, position=position, length=length)
    if datapoints_to_update!=None:
        for datapoint in datapoints_to_update:
            message=messages.FillDatapointMessage(pid=pid, date=date)
            msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

@exceptions.ExceptionHandler
def mark_negative_variable_request(username, pid, sequence, position, length):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MNVR_IU)
    if not args.is_valid_sequence(sequence):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MNVR_IS)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MNVR_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MNVR_IL)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWADP_MNVR_IP)
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.MARK_NEGATIVE_VARIABLE,uid=uid,pid=pid)
    date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
    datapoints_to_update=datapointapi.mark_negative_variable(pid=pid, date=date, position=position, length=length)
    if datapoints_to_update!=None:
        for datapoint in datapoints_to_update:
            message=messages.FillDatapointMessage(pid=pid, date=date)
            msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

@exceptions.ExceptionHandler
def delete_datapoint_request(username, pid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWADP_DDPR_IU)
    if not args.is_valid_hex_uuid(pid):
        raise exceptions.BadParametersException(error=errors.E_IWADP_DDPR_IP)
    pid=uuid.UUID(pid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_DATAPOINT,uid=uid,pid=pid)
    message=messages.DeleteDatapointMessage(pid=pid)
    msgapi.send_message(message=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

