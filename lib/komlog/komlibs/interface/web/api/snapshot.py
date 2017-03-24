'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komfig import logging
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.auth.passport import UserPassport
from komlog.komlibs.auth.tickets import provision as ticketprov
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.snapshot import api as snapshotapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount.widget import types
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response, operation
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_snapshots_config_request(passport):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_GSNSCR_IPSP)
    authorization.authorize_request(request=Requests.GET_SNAPSHOTS_CONFIG,passport=passport)
    data=snapshotapi.get_snapshots_config(uid=passport.uid)
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
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_snapshot_config_request(passport, nid, tid=None):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_GSNCR_IPSP)
    if not args.is_valid_hex_uuid(nid):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_GSNCR_IN)
    if tid and not args.is_valid_hex_uuid(tid):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_GSNCR_IT)
    nid=uuid.UUID(nid)
    tid=uuid.UUID(tid) if tid else None
    authorization.authorize_request(request=Requests.GET_SNAPSHOT_CONFIG,passport=passport,nid=nid, tid=tid)
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
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=snapshot)

@exceptions.ExceptionHandler
def delete_snapshot_request(passport, nid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_DSNR_IPSP)
    if not args.is_valid_hex_uuid(nid):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_DSNR_IN)
    nid=uuid.UUID(nid)
    authorization.authorize_request(request=Requests.DELETE_SNAPSHOT,passport=passport,nid=nid)
    deleteapi.delete_snapshot(nid=nid)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_snapshot_request(passport, wid, user_list=None, cid_list=None, its=None, ets=None, seq=None):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_IPSP)
    if not args.is_valid_hex_uuid(wid):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_IW)
    if user_list and not args.is_valid_list(user_list):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_IUL)
    if cid_list and not args.is_valid_list(cid_list):
        raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_ICL)
    uids=set()
    if user_list:
        for user in user_list:
            if not args.is_valid_username_with_caps(user):
                raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_IULE)
            else:
                user_uid=userapi.get_uid(username=user.lower())
                if user_uid:
                    uids.add(user_uid)
    cids=set()
    if cid_list:
        for cid in cid_list:
            if not args.is_valid_hex_uuid(cid):
                raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_ICLE)
            else:
                cids.add(uuid.UUID(cid))
    wid=uuid.UUID(wid)
    if len(uids)+len(cids)==0:
        raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_ESL)
    if seq and args.is_valid_sequence(seq):
        interval_init=timeuuid.get_uuid1_from_custom_sequence(seq)
        interval_end=interval_init
    elif its and ets and args.is_valid_timestamp(its) and args.is_valid_timestamp(ets):
        if its>ets:
            its,ets=ets,its
        interval_init=timeuuid.min_uuid_from_time(its)
        interval_end=timeuuid.max_uuid_from_time(ets)
    else:
        raise exceptions.BadParametersException(error=Errors.E_IWASN_NSNR_NSNTS)
    authorization.authorize_request(request=Requests.NEW_SNAPSHOT,passport=passport, wid=wid)
    snapshot=snapshotapi.new_snapshot(uid=passport.uid,wid=wid,interval_init=interval_init,interval_end=interval_end)
    if snapshot:
        try:
            ticket=ticketprov.new_snapshot_ticket(uid=passport.uid,nid=snapshot['nid'],allowed_uids=uids, allowed_cids=cids)
            if ticket:
                webop=operation.NewSnapshotOperation(uid=passport.uid, nid=snapshot['nid'],wid=wid)
                authop=webop.get_auth_operation()
                params=webop.get_params()
                if authupdate.update_resources(operation=authop, params=params):
                    resp=response.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'nid':snapshot['nid'].hex,'tid':ticket['tid'].hex})
                    resp.add_imc_message(messages.UpdateQuotesMessage(operation=authop, params=params))
                    resp.add_imc_message(messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED, parameters={'nid':snapshot['nid'].hex,'tid':ticket['tid'].hex}))
                    return resp
                else:
                    deleteapi.delete_snapshot(nid=snapshot['nid'])
                    return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWASN_NSNR_AUTHERR)
            else:
                deleteapi.delete_snapshot(nid=snapshot['nid'])
                return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=Errors.E_IWASN_NSNR_TCKCE)
        except:
            deleteapi.delete_snapshot(nid=snapshot['nid'])
            raise
    return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=Errors.E_IWASN_NSNR_SCE)

