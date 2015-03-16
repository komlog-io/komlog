'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount.snapshot import api as snapshotapi
from komlibs.gestaccount.widget import types
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_snapshots_config_request(username):
    if args.is_valid_username(username):
        data=snapshotapi.get_snapshots_config(username=username)
        response_data=[]
        for snapshot in data:
            reg={}
            reg['type']=snapshot['type']
            reg['nid']=snapshot['nid'].hex
            reg['widgetname']=snapshot['widgetname']
            reg['its']=timeuuid.get_unix_timestamp(snapshot['interval_init'])
            reg['ets']=timeuuid.get_unix_timestamp(snapshot['interval_end'])
            reg['iseq']=timeuuid.get_custom_sequence(snapshot['interval_init'])
            reg['eseq']=timeuuid.get_custom_sequence(snapshot['interval_end'])
            if snapshot['type']==types.DATASOURCE:
                reg['did']=snapshot['did'].hex
            elif snapshot['type']==types.DATAPOINT:
                reg['pid']=snapshot['pid'].hex
            elif snapshot['type'] in [types.HISTOGRAM, types.LINEGRAPH, types.TABLE]:
                reg['datapoints']=[]
                for pid in snapshot['datapoints']:
                    if pid in snapshot['colors'].keys():
                        color= snapshot['colors'][pid]
                    else:
                        color=''
                    reg['datapoints'].append({'pid':pid.hex,'color':color})
            response_data.append(reg)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_snapshot_config_request(username, nid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(nid):
        nid=uuid.UUID(nid)
        authorization.authorize_request(request=requests.GET_SNAPSHOT_CONFIG,username=username,nid=nid)
        data=snapshotapi.get_snapshot_config(nid=nid)
        snapshot={'nid':nid.hex}
        snapshot['type']=data['type']
        snapshot['widgetname']=data['widgetname']
        snapshot['its']=timeuuid.get_unix_timestamp(data['interval_init'])
        snapshot['ets']=timeuuid.get_unix_timestamp(data['interval_end'])
        snapshot['iseq']=timeuuid.get_custom_sequence(data['interval_init'])
        snapshot['eseq']=timeuuid.get_custom_sequence(data['interval_end'])
        if data['type']==types.DATASOURCE:
            snapshot['did']=data['did'].hex
        elif data['type']==types.DATAPOINT:
            snapshot['pid']=data['pid'].hex
        elif data['type'] in [types.HISTOGRAM, types.LINEGRAPH, types.TABLE]:
            snapshot['datapoints']=[]
            for pid in data['datapoints']:
                if pid in data['colors'].keys():
                    color=data['colors'][pid]
                else:
                    color=''
                snapshot['datapoints'].append({'pid':pid.hex,'color':color})
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=snapshot)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_snapshot_request(username, nid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(nid):
        nid=uuid.UUID(nid)
        authorization.authorize_request(request=requests.DELETE_SNAPSHOT,username=username,nid=nid)
        snapshotapi.delete_snapshot(nid=nid)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_snapshot_request(username, wid, user_list=None, cid_list=None, its=None, ets=None, seq=None):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(wid):
        if user_list and not args.is_valid_list(user_list):
            raise exceptions.BadParametersException()
        if cid_list and not args.is_valid_list(cid_list):
            raise exceptions.BadParametersException()
        if user_list:
            for user in user_list:
                if not args.is_valid_username(user):
                    raise exceptions.BadParametersException()
        if cid_list:
            for cid in cid_list:
                if not args.is_valid_hex_uuid(cid):
                    raise exceptions.BadParametersException()
        wid=uuid.UUID(wid)
        cid_uuid_list=[uuid.UUID(cid) for cid in cid_list] if cid_list else None
        if seq and args.is_valid_sequence(seq):
            interval_init=timeuuid.get_uuid1_from_custom_sequence(seq)
            interval_end=interval_init
        elif its and ets and args.is_valid_timestamp(its) and args.is_valid_timestamp(ets):
            interval_init=timeuuid.uuid1(seconds=its)
            interval_end=timeuuid.uuid1(seconds=ets)
            if interval_init>interval_end:
                temp=interval_end
                interval_end=interval_init
                interval_init=temp
        else:
            raise exceptions.BadParametersException()
        authorization.authorize_request(request=requests.NEW_SNAPSHOT, username=username, wid=wid)
        snapshot=snapshotapi.new_snapshot(username=username,wid=wid,interval_init=interval_init,interval_end=interval_end,shared_with_users=user_list,shared_with_cids=cid_uuid_list)
        if snapshot:
            operation=weboperations.NewSnapshotOperation(uid=snapshot['uid'], nid=snapshot['nid'],wid=snapshot['wid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            message=messages.SharedAuthorizationUpdateMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'nid':snapshot['nid'].hex})
        else:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_snapshot_data_request(username, nid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(nid):
        nid=uuid.UUID(nid)
        authorization.authorize_request(request=requests.GET_SNAPSHOT_DATA, username=username, nid=nid)
        data=snapshotapi.get_snapshot_data(nid=nid)
        response_data=[]
        for item in data.keys():
            data_object={}
            data_object['id']=item.hex
            data_object['data']=[]
            for entry in data[reg]:
                entry_data={}
                if 'date' in entry:
                    entry_data['date']=timeuuid.get_unix_timestamp(entry['date'])
                if 'content' in entry:
                    entry_data['content']=entry['content']
                    entry_data['datapoints']=[{pid.hex:pos} for pid,pos in entry['datapoints'].items()]
                else:
                    entry_data['value']=int(entry['value']) if entry['value']%1==0 else float(entry['value'])
                data_object['data'].append(entry_data)
            response_data.append(data_object)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data=response_data)
    else:
        raise exceptions.BadParametersException()

