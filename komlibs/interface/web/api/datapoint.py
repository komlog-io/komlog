#coding: utf-8
'''

This file defines the logic associated with web interface operations

'''

import uuid
import time
from komfig import logger
from komlibs.auth import authorization
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api as widgetapi
from komimc import messages
from komimc import api as msgapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_datapoint_data_request(username, pid, start_date, end_date):
    if not end_date:
        end_date=time.time()
    if not start_date:
        start_date=end_date-86400
    if args.is_valid_username(username) and args.is_valid_hex_uuid(pid) and args.is_valid_timestamp(start_date) and args.is_valid_timestamp(end_date):
        authorization.authorize_request(request='GetDatapointDataRequest',username=username,pid=pid)
        data=datapointapi.get_datapoint_data(pid, end_date=end_date, start_date=start_date)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_datapoint_config_request(username, pid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(pid):
        pid=uuid.UUID(pid)
        authorization.authorize_request(request='GetDatapointConfigRequest',username=username,pid=pid)
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
        authorization.authorize_request(request='DatapointUpdateConfigurationRequest',username=username,pid=pid)
        datapointapi.update_datapoint_config(pid=pid,datapointname=datapointname, color=color)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_datapoint_request(username, did, sequence, position, length, datapointname):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(did) and args.is_valid_sequence(sequence) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_datapointname(datapointname):
        did=uuid.UUID(did)
        authorization.authorize_request(request='NewDatapointRequest',username=username,did=did)
        date=timeuuid.get_uuid1_from_custom_sequence(sequence=sequence)
        message=messages.MonitorVariableMessage(username=username, did=did, date=date, position=position, length=length, datapointname=datapointname)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

