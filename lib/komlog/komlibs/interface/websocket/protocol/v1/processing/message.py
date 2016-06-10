'''

this file implement the processing of the different actions supported by the
protocol

'''

import uuid
import json
from komlog.komfig import logging, config, options
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.websocket.protocol.v1 import status, exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop
from komlog.komlibs.interface.websocket.protocol.v1.model.response import Response



@exceptions.ExceptionHandler
def _process_send_ds_data(passport, message):
    message = modmsg.SendDsDataMessage(message=message)
    did=None
    new_datasource=False
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.payload['uri'])
    if not uri_info or uri_info['type']==vertex.VOID:
        authorization.authorize_request(request=Requests.NEW_DATASOURCE,passport=passport)
        datasource=datasourceapi.create_datasource(uid=passport.uid, aid=passport.aid, datasourcename=message.payload['uri'])
        if datasource:
            new_datasource = True
            did=datasource['did']
        else:
            return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDSD_ECDS)
    elif uri_info['type']==vertex.DATASOURCE:
        did=uri_info['id']
        authorization.authorize_request(request=Requests.POST_DATASOURCE_DATA,passport=passport,did=did)
    else:
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='uri is not a datasource', error=Errors.E_IWSPV1PM_PSDSD_IURI)
    try:
        dest_dir=config.get(options.SAMPLES_RECEIVED_PATH)
        datasourceapi.upload_datasource_data(did=did, content=json.dumps({'content':message.payload['content'],'ts':message.payload['ts']}),dest_dir=dest_dir)
    except Exception:
        if new_datasource:
            deleteapi.delete_datasource(did=datasource['did'])
        return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDSD_EUR)
    else:
        if new_datasource:
            try:
                op=modop.NewDatasourceOperation(uid=passport.uid,aid=passport.aid,did=datasource['did'])
                op_result=operation.process_operation(op)
            except Exception as e:
                deleteapi.delete_datasource(did=datasource['did'])
                return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDSD_EUR)
            else:
                if op_result == False:
                    deleteapi.delete_datasource(did=datasource['did'])
                    return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDSD_FUR)
        return Response(status=status.MESSAGE_ACCEPTED_FOR_PROCESSING)

@exceptions.ExceptionHandler
def _process_send_dp_data(passport, message):
    message = modmsg.SendDpDataMessage(message=message)
    new_datapoint=False
    date=timeuuid.uuid1(seconds=message.payload['ts'])
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.payload['uri'])
    if uri_info and uri_info['type']==vertex.DATAPOINT:
        pid=uri_info['id']
        authorization.authorize_request(request=Requests.POST_DATAPOINT_DATA,passport=passport,pid=pid)
        datapointapi.store_user_datapoint_value(pid=pid,date=date,content=message.payload['content'])
    elif not uri_info or uri_info['type']==vertex.VOID:
        authorization.authorize_request(request=Requests.NEW_USER_DATAPOINT,passport=passport)
        datapoint=datapointapi.create_user_datapoint(uid=passport.uid, datapoint_uri=message.payload['uri'])
        if datapoint:
            pid=datapoint['pid']
            try:
                datapointapi.store_user_datapoint_value(pid=pid,date=date,content=message.payload['content'])
                op=modop.NewUserDatapointOperation(uid=passport.uid,aid=passport.aid,pid=datapoint['pid'])
                op_result=operation.process_operation(op)
                if op_result == False:
                    deleteapi.delete_datapoint(pid=datapoint['pid'])
                    return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDPD_FPOR)
            except:
                deleteapi.delete_datapoint(pid=datapoint['pid'])
                raise
        else:
            return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDPD_ECDP)
    else:
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='uri is not a datapoint', error=Errors.E_IWSPV1PM_PSDPD_IURI)
    return Response(status=status.MESSAGE_EXECUTION_OK)

