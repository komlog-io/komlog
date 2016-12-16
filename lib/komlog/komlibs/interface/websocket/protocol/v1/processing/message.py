'''

this file implement the processing of the different actions supported by the
protocol

'''

import uuid
import json
from komlog.komfig import logging, config, options
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.websocket import status, exceptions
from komlog.komlibs.interface.websocket.model.response import Response
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop



@exceptions.ExceptionHandler
def _process_send_ds_data(passport, message):
    message = modmsg.SendDsData.load_from_dict(message)
    did=None
    new_datasource=False
    msgs=[]
    if args.is_valid_global_uri(message.uri):
        username,local_uri=message.uri.split(':')
        try:
            user_uid = userapi.get_uid(username.lower())
        except gestexcept.UserNotFoundException:
            user_uid = None
        if user_uid != passport.uid:
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason="Cannot modify other user's uris", error=Errors.E_IWSPV1PM_PSDSD_EUGURI)
        else:
            message.uri = local_uri
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.uri)
    if not uri_info or uri_info['type']==vertex.VOID:
        authorization.authorize_request(request=Requests.NEW_DATASOURCE,passport=passport)
        datasource=datasourceapi.create_datasource(uid=passport.uid, aid=passport.aid, datasourcename=message.uri)
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
        date=timeuuid.get_uuid1_from_isodate(message.ts, predictable=True)
        datasourceapi.store_datasource_data(did=did, date=date, content=message.content)
        op=modop.DatasourceDataStoredOperation(uid=passport.uid, did=did, date=date)
        op_msgs=operation.process_operation(op)
        for msg in op_msgs:
            msgs.append(msg)
    except:
        if new_datasource:
            deleteapi.delete_datasource(did=did)
        raise
    else:
        if new_datasource:
            try:
                op=modop.NewDatasourceOperation(uid=passport.uid,aid=passport.aid,did=datasource['did'])
                op_msgs=operation.process_operation(op)
                for msg in op_msgs:
                    msgs.append(msg)
            except:
                deleteapi.delete_datasource(did=datasource['did'])
                raise
            msgs.append(messages.HookNewUrisMessage(uid=passport.uid, uris=[{'type':vertex.DATASOURCE,'id':did,'uri':message.uri}],date=date))
        resp = Response(status=status.MESSAGE_EXECUTION_OK)
        for msg in msgs:
            resp.add_message(msg)
        return resp

@exceptions.ExceptionHandler
def _process_send_dp_data(passport, message):
    message = modmsg.SendDpData.load_from_dict(message)
    new_datapoint=False
    date=timeuuid.get_uuid1_from_isodate(message.ts, predictable=True)
    msgs=[]
    if args.is_valid_global_uri(message.uri):
        username,local_uri=message.uri.split(':')
        try:
            user_uid = userapi.get_uid(username.lower())
        except gestexcept.UserNotFoundException:
            user_uid = None
        if user_uid != passport.uid:
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason="Cannot modify other user's uris", error=Errors.E_IWSPV1PM_PSDPD_EUGURI)
        else:
            message.uri = local_uri
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.uri)
    if not uri_info or uri_info['type']==vertex.VOID:
        authorization.authorize_request(request=Requests.NEW_USER_DATAPOINT,passport=passport)
        datapoint=datapointapi.create_user_datapoint(uid=passport.uid, datapoint_uri=message.uri)
        if datapoint:
            pid=datapoint['pid']
            new_datapoint=True
        else:
            return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDPD_ECDP)
    elif uri_info['type']==vertex.DATAPOINT:
        pid=uri_info['id']
        authorization.authorize_request(request=Requests.POST_DATAPOINT_DATA,passport=passport,pid=pid)
    else:
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='uri is not a datapoint', error=Errors.E_IWSPV1PM_PSDPD_IURI)
    try:
        datapointapi.store_user_datapoint_value(pid=pid,date=date,content=message.content)
        op=modop.DatapointDataStoredOperation(uid=passport.uid, pid=pid, date=date)
        op_msgs=operation.process_operation(op)
        for msg in op_msgs:
            msgs.append(msg)
    except:
        deleteapi.delete_datapoint(pid=pid)
        raise
    else:
        if new_datapoint:
            msgs.append(messages.HookNewUrisMessage(uid=passport.uid, uris=[{'type':vertex.DATAPOINT,'id':pid,'uri':message.uri}],date=date))
            op=modop.NewUserDatapointOperation(uid=passport.uid,aid=passport.aid,pid=pid)
            op_msgs=operation.process_operation(op)
            for msg in op_msgs:
                msgs.append(msg)
        else:
            msgs.append(messages.UrisUpdatedMessage(uris=[{'type':vertex.DATAPOINT,'id':pid,'uri':message.uri}],date=date))
    resp = Response(status=status.MESSAGE_EXECUTION_OK)
    for msg in msgs:
        resp.add_message(msg)
    return resp

@exceptions.ExceptionHandler
def _process_send_multi_data(passport, message):
    message = modmsg.SendMultiData.load_from_dict(message)
    date=timeuuid.get_uuid1_from_isodate(message.ts, predictable=True)
    existing_uris=[]
    pending_ds_creations=[]
    pending_dp_creations=[]
    msgs=[]
    # execution authorization
    for item in message.uris:
        if args.is_valid_global_uri(item['uri']):
            username,local_uri=item['uri'].split(':')
            try:
                user_uid = userapi.get_uid(username.lower())
            except gestexcept.UserNotFoundException:
                user_uid = None
            if user_uid != passport.uid:
                return Response(status=status.MESSAGE_EXECUTION_DENIED, reason="Cannot modify other user's uris", error=Errors.E_IWSPV1PM_PSMTD_EUGURI)
        else:
            local_uri = item['uri']
        uri_info=graphuri.get_id(ido=passport.uid, uri=local_uri)
        if uri_info is None or uri_info['type']==vertex.VOID:
            if item['type'] == vertex.DATAPOINT and args.is_valid_datapoint_content(item['content']):
                pending_dp_creations.append({'type':item['type'],'uri':local_uri,'content':item['content']})
            elif item['type'] == vertex.DATASOURCE and args.is_valid_datasource_content(item['content']):
                pending_ds_creations.append({'type':item['type'],'uri':local_uri,'content':item['content']})
            else:
                return Response(status=status.PROTOCOL_ERROR, reason='invalid content for uri: '+item['uri'], error=Errors.E_IWSPV1PM_PSMTD_IUC)
        elif uri_info['type'] not in (vertex.DATAPOINT,vertex.DATASOURCE):
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+item['uri'], error=Errors.E_IWSPV1PM_PSMTD_ONAOU)
        else:
            if uri_info['type'] == vertex.DATASOURCE and args.is_valid_datasource_content(item['content']):
                existing_uris.append({'uri':local_uri,'id':uri_info['id'],'type':uri_info['type'],'content':item['content']})
            elif uri_info['type'] == vertex.DATAPOINT and args.is_valid_datapoint_content(item['content']):
                existing_uris.append({'uri':local_uri,'id':uri_info['id'],'type':uri_info['type'],'content':item['content']})
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
                new_ds.append({'uri':item['uri'],'did':datasource['did'],'content':item['content']})
            else:
                raise exceptions.OperationExecutionException(error=Errors.E_IWSPV1PM_PSMTD_ECDS)
        for item in pending_dp_creations:
            datapoint=datapointapi.create_user_datapoint(uid=passport.uid,datapoint_uri=item['uri'])
            if datapoint:
                new_dp.append({'uri':item['uri'],'pid':datapoint['pid'],'content':item['content']})
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
        updated_uris=[]
        updated_new_uris=[]
        for item in existing_uris:
            if item['type'] == vertex.DATAPOINT:
                pid=item['id']
                datapointapi.store_user_datapoint_value(pid=pid,date=date,content=item['content'])
                updated_uris.append({'uri':item['uri'],'type':vertex.DATAPOINT,'id':pid})
            elif item['type'] == vertex.DATASOURCE:
                did=item['id']
                datasourceapi.store_datasource_data(did=did, date=date, content=item['content'])
                updated_uris.append({'uri':item['uri'],'type':vertex.DATASOURCE,'id':did})
        for item in new_ds:
            did=item['did']
            datasourceapi.store_datasource_data(did=did, date=date, content=item['content'])
            updated_new_uris.append({'uri':item['uri'],'type':vertex.DATASOURCE,'id':did})
        for item in new_dp:
            pid=item['pid']
            datapointapi.store_user_datapoint_value(pid=pid,date=date,content=item['content'])
            updated_new_uris.append({'uri':item['uri'],'type':vertex.DATAPOINT,'id':pid})
        if len(updated_uris)>0:
            msgs.append(messages.UrisUpdatedMessage(uris=updated_uris, date=date))
        if len(updated_new_uris)>0:
            msgs.append(messages.HookNewUrisMessage(uid=passport.uid, uris=updated_new_uris, date=date))
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
    #get process operations
    try:
        for ds in new_ds:
            op=modop.NewDatasourceOperation(uid=passport.uid,aid=passport.aid,did=ds['did'])
            op_msgs=operation.process_operation(op)
            for msg in op_msgs:
                msgs.append(msg)
            op=modop.DatasourceDataStoredOperation(uid=passport.uid, did=ds['did'], date=date)
            op_msgs=operation.process_operation(op)
            for msg in op_msgs:
                msgs.append(msg)
        for dp in new_dp:
            op=modop.NewUserDatapointOperation(uid=passport.uid,aid=passport.aid,pid=dp['pid'])
            op_msgs=operation.process_operation(op)
            for msg in op_msgs:
                msgs.append(msg)
            op=modop.DatapointDataStoredOperation(uid=passport.uid, pid=dp['pid'], date=date)
            op_msgs=operation.process_operation(op)
            for msg in op_msgs:
                msgs.append(msg)
        for item in existing_uris:
            if item['type']==vertex.DATASOURCE:
                op=modop.DatasourceDataStoredOperation(uid=passport.uid, did=item['id'], date=date)
                op_msgs=operation.process_operation(op)
                for msg in op_msgs:
                    msgs.append(msg)
            elif item['type'] == vertex.DATAPOINT:
                op=modop.DatapointDataStoredOperation(uid=passport.uid, pid=item['id'], date=date)
                op_msgs=operation.process_operation(op)
                for msg in op_msgs:
                    msgs.append(msg)
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
        resp = Response(status=status.MESSAGE_EXECUTION_OK)
        for msg in msgs:
            resp.add_message(msg)
        return resp

@exceptions.ExceptionHandler
def _process_hook_to_uri(passport, message):
    message = modmsg.HookToUri.load_from_dict(message)
    if args.is_valid_global_uri(message.uri):
        username,local_uri=message.uri.split(':')
        try:
            user_uid = userapi.get_uid(username.lower())
        except gestexcept.UserNotFoundException:
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.uri, error=Errors.E_IWSPV1PM_PHTU_OUNF)
    else:
        local_uri=message.uri
        user_uid=passport.uid
    uri_info=graphuri.get_id(ido=user_uid, uri=local_uri)
    if not uri_info or uri_info['type'] == vertex.VOID:
        authorization.authorize_request(request=Requests.REGISTER_PENDING_HOOK,passport=passport,uri=message.uri)
        userapi.register_pending_hook(uid=user_uid, uri=local_uri, sid=passport.sid)
        return Response(status=status.MESSAGE_EXECUTION_OK, reason='Operation registered, but uri does not exist yet')
    elif uri_info['type'] not in (vertex.DATASOURCE,vertex.DATAPOINT):
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.uri, error=Errors.E_IWSPV1PM_PHTU_ONA)
    else:
        if uri_info['type'] == vertex.DATASOURCE:
            authorization.authorize_request(request=Requests.HOOK_TO_DATASOURCE,passport=passport,did=uri_info['id'])
            datasourceapi.hook_to_datasource(did=uri_info['id'], sid=passport.sid)
        elif uri_info['type'] == vertex.DATAPOINT:
            authorization.authorize_request(request=Requests.HOOK_TO_DATAPOINT,passport=passport,pid=uri_info['id'])
            datapointapi.hook_to_datapoint(pid=uri_info['id'], sid=passport.sid)
    return Response(status=status.MESSAGE_EXECUTION_OK, reason='Hooked successfully')

@exceptions.ExceptionHandler
def _process_unhook_from_uri(passport, message):
    message = modmsg.UnHookFromUri.load_from_dict(message)
    if args.is_valid_global_uri(message.uri):
        username,local_uri=message.uri.split(':')
        try:
            user_uid = userapi.get_uid(username.lower())
        except gestexcept.UserNotFoundException:
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.uri, error=Errors.E_IWSPV1PM_PUHFU_OUNF)
    else:
        local_uri=message.uri
        user_uid=passport.uid
    uri_info=graphuri.get_id(ido=user_uid, uri=local_uri)
    if not uri_info or uri_info['type'] == vertex.VOID:
        authorization.authorize_request(request=Requests.DELETE_PENDING_HOOK,passport=passport,uri=message.uri)
        userapi.delete_pending_hook(uid=user_uid, uri=local_uri, sid=passport.sid)
        return Response(status=status.MESSAGE_EXECUTION_OK, reason='Unhooked')
    elif uri_info['type'] not in (vertex.DATASOURCE,vertex.DATAPOINT):
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.uri, error=Errors.E_IWSPV1PM_PUHFU_ONA)
    else:
        if uri_info['type'] == vertex.DATASOURCE:
            authorization.authorize_request(request=Requests.UNHOOK_FROM_DATASOURCE,passport=passport,did=uri_info['id'])
            datasourceapi.unhook_from_datasource(did=uri_info['id'], sid=passport.sid)
        elif uri_info['type'] == vertex.DATAPOINT:
            authorization.authorize_request(request=Requests.UNHOOK_FROM_DATAPOINT,passport=passport, pid=uri_info['id'])
            datapointapi.unhook_from_datapoint(pid=uri_info['id'], sid=passport.sid)
    return Response(status=status.MESSAGE_EXECUTION_OK)

@exceptions.ExceptionHandler
def _process_request_data(passport, message):
    message = modmsg.RequestData.load_from_dict(message)
    if args.is_valid_global_uri(message.uri):
        username,local_uri = message.uri.split(':')
        try:
            user_uid = userapi.get_uid(username.lower())
        except gestexcept.UserNotFoundException:
            return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.uri, error=Errors.E_IWSPV1PM_PRDI_OUNF)
    else:
        user_uid = passport.uid
        local_uri = message.uri
    uri_info=graphuri.get_id(ido=user_uid, uri=local_uri)
    if not uri_info or uri_info['type'] == vertex.VOID:
        authorization.authorize_request(request=Requests.GET_URI,passport=passport,uri=message.uri)
        return Response(status=status.RESOURCE_NOT_FOUND, reason='uri '+message.uri+' does not exist', error=Errors.E_IWSPV1PM_PRDI_UNF)
    elif uri_info['type'] not in (vertex.DATASOURCE,vertex.DATAPOINT):
        authorization.authorize_request(request=Requests.GET_URI,passport=passport,uri=message.uri)
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='operation not allowed on this uri: '+message.uri, error=Errors.E_IWSPV1PM_PRDI_ONA)
    if message.start is None and message.end is None:
        ii=timeuuid.min_uuid_from_time(1)
        ie=timeuuid.min_uuid_from_time(timeuuid.get_unix_timestamp(timeuuid.uuid1()))
    elif message.start <= message.end:
        ii=timeuuid.min_uuid_from_time(message.start.timestamp())
        ie=timeuuid.max_uuid_from_time(message.end.timestamp())
    else:
        ii=timeuuid.min_uuid_from_time(message.end.timestamp())
        ie=timeuuid.max_uuid_from_time(message.start.timestamp())
    try:
        if uri_info['type'] == vertex.DATASOURCE:
            authorization.authorize_request(request=Requests.GET_DATASOURCE_DATA,passport=passport,did=uri_info['id'], ii=ii, ie=ie, tid=None)
        elif uri_info['type'] == vertex.DATAPOINT:
            authorization.authorize_request(request=Requests.GET_DATAPOINT_DATA,passport=passport,pid=uri_info['id'], ii=ii, ie=ie, tid=None)
    except authexcept.IntervalBoundsException as e:
        if ie.time < e.data['date'].time:
            limit=timeuuid.get_isodate_from_uuid(e.data['date'])
            reason = 'Your interval requested for uri '+message.uri+' is wider than the limit allowed: '+limit+'. Access to data is not allowed before that date.'
            error=Errors.E_IWSPV1PM_PRDI_ANA
            stat=status.MESSAGE_EXECUTION_DENIED
            #however we will continue request and send a msg with no data so agent logic is simpler
        else:
            limit=timeuuid.get_isodate_from_uuid(e.data['date'])
            reason = 'Your current interval limit is within the range requested for uri '+message.uri+'. Limit is stablished at: '+limit+'. Data interval retrieved will be modified for that reason.'
            error=Errors.E_IWSPV1PM_PRDI_ALP
            stat=status.MESSAGE_ACCEPTED_FOR_PROCESSING
    else:
        error=Errors.OK
        reason='message accepted for processing'
        stat=status.MESSAGE_ACCEPTED_FOR_PROCESSING
    msg=messages.DataIntervalRequestMessage(sid=passport.sid, uri={'type':uri_info['type'],'id':uri_info['id'],'uri':local_uri}, ii=ii, ie=ie, count=message.count)
    resp=Response(status=stat, reason=reason, error=error)
    resp.add_message(msg)
    return resp

