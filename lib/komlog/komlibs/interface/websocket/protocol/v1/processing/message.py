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

@exceptions.ExceptionHandler
def _process_send_multi_data(passport, message):
    message = modmsg.SendMultiDataMessage(message=message)
    date=timeuuid.uuid1(seconds=message.payload['ts'])
    existing_uris=[]
    pending_ds_creations=[]
    pending_dp_creations=[]
    # execution authorization
    for item in message.payload['uris']:
        uri_info=graphuri.get_id(ido=passport.uid, uri=item['uri'])
        if uri_info is None or uri_info['type']==vertex.VOID:
            if args.is_valid_datapoint_content(item['content']):
                pending_dp_creations.append(item)
            elif args.is_valid_datasource_content(item['content']):
                pending_ds_creations.append(item)
            else:
                return Response(status=status.PROTOCOL_ERROR, reason='invalid content for uri: '+item['uri'], error=Errors.E_IWSPV1PM_PSMTD_IUC)
        elif uri_info['type'] not in (vertex.DATAPOINT,vertex.DATASOURCE):
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+item['uri'], error=Errors.E_IWSPV1PM_PSMTD_ONAOU)
        else:
            if uri_info['type'] == vertex.DATASOURCE and args.is_valid_datasource_content(item['content']):
                existing_uris.append({'id':uri_info['id'],'type':uri_info['type'],'content':item['content']})
            elif uri_info['type'] == vertex.DATAPOINT and args.is_valid_datapoint_content(item['content']):
                existing_uris.append({'id':uri_info['id'],'type':uri_info['type'],'content':item['content']})
            else:
                return Response(status=status.PROTOCOL_ERROR, reason='uri content not valid: '+item['uri'], error=Errors.E_IWSPV1PM_PSMTD_UCNV)
    if len(pending_ds_creations)>0:
        authorization.authorize_request(request=Requests.NEW_DATASOURCE,passport=passport)
    if len(pending_dp_creations)>0:
        authorization.authorize_request(request=Requests.NEW_USER_DATAPOINT,passport=passport)
    for item in existing_uris:
        if item['type']==vertex.DATAPOINT:
            pid=item['id']
            authorization.authorize_request(request=Requests.POST_DATAPOINT_DATA,passport=passport,pid=pid)
        elif item['type']==vertex.DATASOURCE:
            did=item['id']
            authorization.authorize_request(request=Requests.POST_DATASOURCE_DATA,passport=passport,did=did)
    new_ds=[]
    new_dp=[]
    #create new uris
    try:
        for item in pending_ds_creations:
            datasource=datasourceapi.create_datasource(uid=passport.uid, aid=passport.aid, datasourcename=item['uri'])
            if datasource:
                new_ds.append({'did':datasource['did'],'content':item['content']})
            else:
                raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_ECDS)
        for item in pending_dp_creations:
            datapoint=datapointapi.create_user_datapoint(uid=passport.uid,datapoint_uri=item['uri'])
            if datapoint:
                new_dp.append({'pid':datapoint['pid'],'content':item['content']})
            else:
                raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_ECDS)
    except:
        for item in new_ds:
            deleteapi.delete_datasource(did=ds['did'])
        for dp in new_dp:
            deleteapi.delete_datapoint(pid=dp['pid'])
        raise
    #store content
    try:
        for item in existing_uris:
            if item['type'] == vertex.DATAPOINT:
                pid=item['id']
                datapointapi.store_user_datapoint_value(pid=pid,date=date,content=item['content'])
            elif item['type'] == vertex.DATASOURCE:
                did=item['id']
                datasourceapi.store_datasource_data(did=did, date=date, content=item['content'])
        for item in new_ds:
            did=item['did']
            datasourceapi.store_datasource_data(did=did, date=date, content=item['content'])
        for item in new_dp:
            pid=item['pid']
            datapointapi.store_user_datapoint_value(pid=pid,date=date,content=item['content'])
    except:
        for item in new_ds:
            deleteapi.delete_datasource(did=ds['did'])
        for dp in new_dp:
            deleteapi.delete_datapoint(pid=dp['pid'])
        for item in existing_uris:
            if item['type']==vertex.DATAPOINT:
                deleteapi.delete_datapoint_data_at(pid=item['id'],date=date)
            elif item['type'] == vertex.DATASOURCE:
                deleteapi.delete_datasource_data_at(did=item['id'],date=date)
        raise
    #process operations, no clean rollback from here...
    try:
        for ds in new_ds:
            op=modop.NewDatasourceOperation(uid=passport.uid,aid=passport.aid,did=ds['did'])
            op_result=operation.process_operation(op)
            if op_result == False:
                raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_NDSOE)
            op=modop.DatasourceDataStoredOperation(did=ds['did'], date=date)
            op_result=operation.process_operation(op)
            if op_result == False:
                raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_NDSDSTE)
        for dp in new_dp:
            op=modop.NewUserDatapointOperation(uid=passport.uid,aid=passport.aid,pid=dp['pid'])
            op_result=operation.process_operation(op)
            if op_result == False:
                raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_NUDPOE)
        for item in existing_uris:
            if item['type']==vertex.DATASOURCE:
                op=modop.DatasourceDataStoredOperation(did=item['id'], date=date)
                op_result=operation.process_operation(op)
                if op_result == False:
                    raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_DSDSTE)
    except:
        for item in new_ds:
            deleteapi.delete_datasource(did=ds['did'])
        for dp in new_dp:
            deleteapi.delete_datapoint(pid=dp['pid'])
        for item in existing_uris:
            if item['type']==vertex.DATAPOINT:
                deleteapi.delete_datapoint_data_at(pid=item['id'],date=date)
            elif item['type'] == vertex.DATASOURCE:
                deleteapi.delete_datasource_data_at(did=item['id'],date=date)
        raise
    else:
        return Response(status=status.MESSAGE_EXECUTION_OK)

@exceptions.ExceptionHandler
def _process_hook_to_uri(passport, message):
    message = modmsg.HookToUriMessage(message=message)
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.payload['uri'])
    if not uri_info:
        return Response(status=status.RESOURCE_NOT_FOUND, reason='uri does not exist', error=Errors.E_IWSPV1PM_PHTU_UNF)
    elif uri_info['type'] not in (vertex.DATASOURCE,vertex.DATAPOINT):
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.payload['uri'], error=Errors.E_IWSPV1PM_PHTU_ONA)
    else:
        if uri_info['type'] == vertex.DATASOURCE:
            authorization.authorize_request(request=Requests.HOOK_TO_DATASOURCE,passport=passport,did=uri_info['id'])
            datasourceapi.hook_to_datasource(did=uri_info['id'], sid=passport.sid)
        elif uri_info['type'] == vertex.DATAPOINT:
            authorization.authorize_request(request=Requests.HOOK_TO_DATAPOINT,passport=passport,pid=uri_info['id'])
            datapointapi.hook_to_datapoint(pid=uri_info['id'], sid=passport.sid)
    return Response(status=status.MESSAGE_EXECUTION_OK)

@exceptions.ExceptionHandler
def _process_unhook_from_uri(passport, message):
    message = modmsg.UnHookFromUriMessage(message=message)
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.payload['uri'])
    if not uri_info:
        return Response(status=status.RESOURCE_NOT_FOUND, reason='uri does not exist', error=Errors.E_IWSPV1PM_PUHFU_UNF)
    elif uri_info['type'] not in (vertex.DATASOURCE,vertex.DATAPOINT):
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.payload['uri'], error=Errors.E_IWSPV1PM_PUHFU_ONA)
    else:
        if uri_info['type'] == vertex.DATASOURCE:
            authorization.authorize_request(request=Requests.UNHOOK_FROM_DATASOURCE,passport=passport,did=uri_info['id'])
            datasourceapi.unhook_from_datasource(did=uri_info['id'], sid=passport.sid)
        elif uri_info['type'] == vertex.DATAPOINT:
            authorization.authorize_request(request=Requests.UNHOOK_FROM_DATAPOINT,passport=passport, pid=uri_info['id'])
            datapointapi.unhook_from_datapoint(pid=uri_info['id'], sid=passport.sid)
    return Response(status=status.MESSAGE_EXECUTION_OK)

