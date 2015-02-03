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
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datapoint_data_request(username, pid, start_date, end_date):
    if start_date and not args.is_valid_string_float(start_date):
        raise exceptions.BadParametersException()
    if end_date and not args.is_valid_string_float(end_date):
        raise exceptions.BadParametersException()
    if args.is_valid_username(username) and args.is_valid_hex_uuid(pid):
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.GET_DATAPOINT_DATA,username=username,pid=pid)
        end_date=timeuuid.uuid1(seconds=float(end_date)) if end_date else None
        start_date=timeuuid.uuid1(seconds=float(start_date)) if start_date else None
        data=datapointapi.get_datapoint_data(pid, fromdate=start_date, todate=end_date)
        response_data=[]
        for point in data:
            response_data.append({'timestamp':timeuuid.get_unix_timestamp(point['date']),
                                  'value':int(point['value']) if point['value']%1==0 else float(point['value'])
                                 })
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_datapoint_config_request(username, pid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(pid):
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.GET_DATAPOINT_CONFIG,username=username,pid=pid)
        data=datapointapi.get_datapoint_config(pid=pid)
        datapoint={}
        datapoint['did']=data['did'].hex
        datapoint['pid']=data['pid'].hex
        datapoint['color']=data['color']
        datapoint['datapointname']=data['datapointname']
        if 'decimalseparator' in data:
            datapoint['decimalseparator']=data['decimalseparator']
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=datapoint)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_datapoint_config_request(username, pid, data):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(pid) and args.is_valid_dict(data):
        if not 'datapointname' in data and not 'color' in data:
            raise exceptions.BadParametersException()
        if 'datapointname' in data and not args.is_valid_datapointname(data['datapointname']):
            raise exceptions.BadParametersException()
        if 'color' in data and not args.is_valid_hexcolor(data['color']):
            raise exceptions.BadParametersException()
        datapointname=data['datapointname'] if 'datapointname' in data else None
        color=data['color'] if 'color' in data else None
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.UPDATE_DATAPOINT_CONFIG,username=username,pid=pid)
        datapointapi.update_datapoint_config(pid=pid,datapointname=datapointname, color=color)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_datapoint_request(username, did, sequence, position, length, datapointname):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(did) and args.is_valid_sequence(sequence) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_datapointname(datapointname):
        did=uuid.UUID(did)
        authorization.authorize_request(request=requests.NEW_DATAPOINT,username=username,did=did)
        date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
        message=messages.MonitorVariableMessage(username=username, did=did, date=date, position=position, length=length, datapointname=datapointname)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def mark_positive_variable_request(username, pid, sequence, position, length):
    if args.is_valid_username(username) and args.is_valid_sequence(sequence) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_hex_uuid(pid):
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.MARK_POSITIVE_VARIABLE,username=username,pid=pid)
        date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
        datapoints_to_update=datapointapi.mark_positive_variable(pid=pid, date=date, position=position, length=length)
        if datapoints_to_update!=None:
            for datapoint in datapoints_to_update:
                message=messages.FillDatapointMessage(pid=pid, date=date)
                msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
        else:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def mark_negative_variable_request(username, pid, sequence, position, length):
    if args.is_valid_username(username) and args.is_valid_sequence(sequence) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_hex_uuid(pid):
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.MARK_NEGATIVE_VARIABLE,username=username,pid=pid)
        date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
        datapoints_to_update=datapointapi.mark_negative_variable(pid=pid, date=date, position=position, length=length)
        if datapoints_to_update!=None:
            for datapoint in datapoints_to_update:
                message=messages.FillDatapointMessage(pid=pid, date=date)
                msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
        else:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_datapoint_request(username, pid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(pid):
        pid=uuid.UUID(pid)
        authorization.authorize_request(request=requests.DELETE_DATAPOINT,username=username,pid=pid)
        message=messages.DeleteDatapointMessage(pid=pid)
        msgapi.send_message(message=message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

