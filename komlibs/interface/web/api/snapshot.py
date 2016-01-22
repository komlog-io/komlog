'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.auth import update as authupdate
from komlibs.auth.tickets import provision as ticketprov
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.snapshot import api as snapshotapi
from komlibs.gestaccount.common import delete as deleteapi
from komlibs.gestaccount.widget import types
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_snapshots_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWASN_GSNSCR_IU)
    uid=userapi.get_uid(username=username)
    data=snapshotapi.get_snapshots_config(uid=uid)
    response_data=[]
    for snapshot in data:
        reg={}
        reg['type']=snapshot['type']
        reg['nid']=snapshot['nid'].hex
        reg['widgetname']=snapshot['widgetname']
        reg['its']=timeuuid.get_unix_timestamp(snapshot['interval_init'])
        reg['ets']=timeuuid.get_unix_timestamp(snapshot['interval_end'])
        if snapshot['type']==types.DATASOURCE:
            reg['seq']=timeuuid.get_custom_sequence(snapshot['interval_init'])
            reg['datasource']={
                               'did':snapshot['datasource_config']['did'].hex,
                               'datasourcename':snapshot['datasource_config']['datasourcename']
                              }
            reg['datapoints']=[]
            for datapoint in snapshot['datapoints_config']:
                reg['datapoints'].append({'pid':datapoint['pid'].hex,
                                          'datapointname':datapoint['datapointname'],
                                          'color':datapoint['color']
                                         })
        elif snapshot['type']==types.DATAPOINT:
            reg['datapoint']={
                              'pid':snapshot['datapoint_config']['pid'].hex,
                              'datapointname':snapshot['datapoint_config']['datapointname'],
                              'color':snapshot['datapoint_config']['color'],
                             }
        elif snapshot['type']==types.MULTIDP:
            reg['view']=snapshot['active_visualization']
            reg['datapoints']=[]
            for datapoint in snapshot['datapoints_config']:
                reg['datapoints'].append({'pid':datapoint['pid'].hex,
                                          'datapointname':datapoint['datapointname'],
                                          'color':datapoint['color']
                                          })
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

@exceptions.ExceptionHandler
def get_snapshot_config_request(username, nid, tid=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWASN_GSNCR_IU)
    if not args.is_valid_hex_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_IWASN_GSNCR_IN)
    if tid and not args.is_valid_hex_uuid(tid):
        raise exceptions.BadParametersException(error=errors.E_IWASN_GSNCR_IT)
    nid=uuid.UUID(nid)
    uid=userapi.get_uid(username=username)
    tid=uuid.UUID(tid) if tid else None
    authorization.authorize_request(request=requests.GET_SNAPSHOT_CONFIG,uid=uid,nid=nid, tid=tid)
    data=snapshotapi.get_snapshot_config(nid=nid)
    snapshot={'nid':nid.hex}
    snapshot['type']=data['type']
    snapshot['widgetname']=data['widgetname']
    snapshot['its']=timeuuid.get_unix_timestamp(data['interval_init'])
    snapshot['ets']=timeuuid.get_unix_timestamp(data['interval_end'])
    if data['type']==types.DATASOURCE:
        snapshot['seq']=timeuuid.get_custom_sequence(data['interval_init'])
        snapshot['datasource']={
                                'did':data['datasource_config']['did'].hex,
                                'datasourcename':data['datasource_config']['datasourcename']
                               }
        snapshot['datapoints']=[]
        for datapoint in data['datapoints_config']:
            snapshot['datapoints'].append({'pid':datapoint['pid'].hex,
                                           'datapointname':datapoint['datapointname'],
                                           'color':datapoint['color']
                                          })
    elif data['type']==types.DATAPOINT:
        snapshot['datapoint']={
                               'pid':data['datapoint_config']['pid'].hex,
                               'datapointname':data['datapoint_config']['datapointname'],
                               'color':data['datapoint_config']['color'],
                              }
    elif data['type']==types.MULTIDP:
        snapshot['view']=data['active_visualization']
        snapshot['datapoints']=[]
        for datapoint in data['datapoints_config']:
            snapshot['datapoints'].append({'pid':datapoint['pid'].hex,
                                           'datapointname':datapoint['datapointname'],
                                           'color':datapoint['color']
                                           })
    elif data['type'] in [types.HISTOGRAM, types.LINEGRAPH, types.TABLE]:
        snapshot['datapoints']=[]
        for pid in data['datapoints']:
            if pid in data['colors'].keys():
                color=data['colors'][pid]
            else:
                color=''
            snapshot['datapoints'].append({'pid':pid.hex,'color':color})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=snapshot)

@exceptions.ExceptionHandler
def delete_snapshot_request(username, nid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWASN_DSNR_IU)
    if not args.is_valid_hex_uuid(nid):
        raise exceptions.BadParametersException(error=errors.E_IWASN_DSNR_IN)
    nid=uuid.UUID(nid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_SNAPSHOT,uid=uid,nid=nid)
    deleteapi.delete_snapshot(nid=nid)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_snapshot_request(username, wid, user_list=None, cid_list=None, its=None, ets=None, seq=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_IU)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_IW)
    if user_list and not args.is_valid_list(user_list):
        raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_IUL)
    if cid_list and not args.is_valid_list(cid_list):
        raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_ICL)
    uids=set()
    if user_list:
        for user in user_list:
            if not args.is_valid_username(user):
                raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_IULE)
            else:
                user_uid=userapi.get_uid(username=user)
                if user_uid:
                    uids.add(user_uid)
    cids=set()
    if cid_list:
        for cid in cid_list:
            if not args.is_valid_hex_uuid(cid):
                raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_ICLE)
            else:
                cids.add(uuid.UUID(cid))
    wid=uuid.UUID(wid)
    if len(uids)+len(cids)==0:
        raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_ESL)
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
        raise exceptions.BadParametersException(error=errors.E_IWASN_NSNR_NSNTS)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_SNAPSHOT, uid=uid, wid=wid)
    snapshot=snapshotapi.new_snapshot(uid=uid,wid=wid,interval_init=interval_init,interval_end=interval_end)
    if snapshot:
        ticket=ticketprov.new_snapshot_ticket(uid=uid,nid=snapshot['nid'],allowed_uids=uids, allowed_cids=cids)
        if ticket:
            operation=weboperations.NewSnapshotOperation(uid=snapshot['uid'], nid=snapshot['nid'],wid=snapshot['wid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            if authupdate.update_resources(operation=auth_op, params=params):
                message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
                msgapi.send_message(message)
                message=messages.UserEventMessage(uid=uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED, parameters={'nid':snapshot['nid'].hex,'tid':ticket['tid'].hex})
                msgapi.send_message(message)
                return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'nid':snapshot['nid'].hex,'tid':ticket['tid'].hex})
            else:
                deleteapi.delete_snapshot(nid=snapshot['nid'])
                return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=errors.E_IWASN_NSNR_AUTHERR)
        else:
            deleteapi.delete_snapshot(nid=snapshot['nid'])
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=errors.E_IWASN_NSNR_TCKCE)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=errors.E_IWASN_NSNR_SCE)

