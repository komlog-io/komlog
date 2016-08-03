'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

import uuid
import json
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.interface.imc import exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komfig import logging


#MESSAGE LIST
MAP_VARS_MESSAGE='MAPVARS'
MON_VAR_MESSAGE='MONVAR'
GDTREE_MESSAGE='GDTREE'
FILL_DATAPOINT_MESSAGE='FILLDP'
FILL_DATASOURCE_MESSAGE='FILLDS'
NEG_VAR_MESSAGE='NEGVAR'
POS_VAR_MESSAGE='POSVAR'
NEW_USR_NOTIF_MESSAGE='NEWUSR'
UPDATE_QUOTES_MESSAGE='UPDQUO'
RESOURCE_AUTHORIZATION_UPDATE_MESSAGE='RESAUTH'
NEW_DP_WIDGET_MESSAGE='NEWDPW'
NEW_DS_WIDGET_MESSAGE='NEWDSW'
DELETE_USER_MESSAGE='DELUSER'
DELETE_AGENT_MESSAGE='DELAGENT'
DELETE_DATASOURCE_MESSAGE='DELDS'
DELETE_DATAPOINT_MESSAGE='DELDP'
DELETE_WIDGET_MESSAGE='DELWIDGET'
DELETE_DASHBOARD_MESSAGE='DELDASHB'
USER_EVENT_MESSAGE='USEREV'
USER_EVENT_RESPONSE_MESSAGE='USEREVRESP'
GENERATE_TEXT_SUMMARY_MESSAGE='GENTEXTSUMMARY'
MISSING_DATAPOINT_MESSAGE='MISSINGDP'
NEW_INV_MAIL_MESSAGE='NEWINV'
FORGET_MAIL_MESSAGE='FORGETMAIL'
URIS_UPDATED_MESSAGE='URISUPDT'
SEND_SESSION_DATA_MESSAGE='SSDATA'
CLEAR_SESSION_HOOKS_MESSAGE='CLSHOOKS'
HOOK_NEW_URIS_MESSAGE='HOOKNEW'


class MapVarsMessage:
    def __init__(self, serialized_message=None, did=None,date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date=self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IDID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MVM_IDT)
            self.type=MAP_VARS_MESSAGE
            self.did=did
            self.date=date
            self.serialized_message='|'.join((self.type,self.did.hex,self.date.hex))

class MonitorVariableMessage:
    def __init__(self, serialized_message=None, uid=None, did=None, date=None, position=None, length=None, datapointname=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,did,date,position,length,datapointname = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
            self.position=int(position)
            self.length=int(length)
            self.datapointname=datapointname
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IUID)
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IDID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IDT)
            if not args.is_valid_int(position):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IPOS)
            if not args.is_valid_int(length):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_ILEN)
            if not args.is_valid_datapointname(datapointname):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MONVAR_IDPN)
            self.type=MON_VAR_MESSAGE
            self.uid=uid
            self.did=did
            self.date=date
            self.position=position
            self.length=length
            self.datapointname=datapointname
            self.serialized_message='|'.join((self.type,self.uid.hex,self.did.hex,self.date.hex,str(self.position),str(self.length),self.datapointname))

class GenerateDTreeMessage:
    def __init__(self, serialized_message=None, pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid=self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
        else:
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GDTREE_IPID)
            self.type=GDTREE_MESSAGE
            self.pid=pid
            self.serialized_message=self.type+'|'+self.pid.hex

class FillDatapointMessage:
    def __init__(self, serialized_message=None, pid=None,date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid,date=self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IPID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDP_IDT)
            self.type=FILL_DATAPOINT_MESSAGE
            self.pid=pid
            self.date=date
            self.serialized_message='|'.join((self.type,self.pid.hex,self.date.hex))

class FillDatasourceMessage:
    def __init__(self, serialized_message=None, did=None,date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date=self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IDID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FILLDS_IDT)
            self.type=FILL_DATASOURCE_MESSAGE
            self.did=did
            self.date=date
            self.serialized_message='|'.join((self.type,self.did.hex,self.date.hex))

class NegativeVariableMessage:
    def __init__(self, serialized_message=None, pid=None, date=None, position=None, length=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid,date,position,length = self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
            self.date=uuid.UUID(date)
            self.position=int(position)
            self.length=int(length)
        else:
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IPID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IDT)
            if not args.is_valid_int(position):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_IPOS)
            if not args.is_valid_int(length):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEGVAR_ILEN)
            self.type=NEG_VAR_MESSAGE
            self.pid=pid
            self.date=date
            self.position=position
            self.length=length
            self.serialized_message='|'.join((self.type,self.pid.hex,self.date.hex,str(self.position),str(self.length)))

class PositiveVariableMessage:
    def __init__(self, serialized_message=None, pid=None, date=None, position=None, length=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid,date,position,length = self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
            self.date=uuid.UUID(date)
            self.position=int(position)
            self.length=int(length)
        else:
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IPID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IDT)
            if not args.is_valid_int(position):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_IPOS)
            if not args.is_valid_int(length):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_POSVAR_ILEN)
            self.type=POS_VAR_MESSAGE
            self.pid=pid
            self.date=date
            self.position=position
            self.length=length
            self.serialized_message='|'.join((self.type,self.pid.hex,self.date.hex,str(self.position),str(self.length)))

class NewUserNotificationMessage:
    def __init__(self, serialized_message=None, email=None, code=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,email,code = self.serialized_message.split('|')
            self.type=mtype
            self.email=email
            self.code=code
        else:
            if not args.is_valid_email(email):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_IEMAIL)
            if not args.is_valid_code(code):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWUSR_ICODE)
            self.type=NEW_USR_NOTIF_MESSAGE
            self.email=email
            self.code=code
            self.serialized_message='|'.join((self.type,self.email,self.code))

class UpdateQuotesMessage:
    def __init__(self, serialized_message=None, operation=None, params=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,operation,str_params = self.serialized_message.split('|')
            self.type=mtype
            self.operation=getattr(Operations,operation)
            self.params={}
            for key,value in json.loads(str_params).items():
                if isinstance(value,list):
                    tmp_list=[]
                    for item in value:
                        tmp_list.append(uuid.UUID(item)) if args.is_valid_hex_uuid(item) or args.is_valid_hex_date(item) else item
                    self.params[key]=tmp_list
                else:
                    self.params[key]=uuid.UUID(value) if args.is_valid_hex_uuid(value) or args.is_valid_hex_date(value) else value
        else:
            if not args.is_valid_dict(params):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IPRM)
            if not isinstance(operation, Operations):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_UPDQUO_IOP)
            self.type=UPDATE_QUOTES_MESSAGE
            self.operation=operation
            self.params=params
            str_params={}
            for key,value in params.items():
                if isinstance(value,list):
                    tmp_list=[]
                    for item in value:
                        tmp_list.append(item.hex) if args.is_valid_uuid(item) or args.is_valid_date(item) else item
                    str_params[key]=tmp_list
                else:
                    str_params[key]=value.hex if args.is_valid_uuid(value) or args.is_valid_date(value) else value
            self.serialized_message='|'.join((self.type,self.operation.name,json.dumps(str_params)))

class ResourceAuthorizationUpdateMessage:
    def __init__(self, serialized_message=None, operation=None, params=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,operation,str_params = self.serialized_message.split('|')
            self.type=mtype
            self.operation=getattr(Operations,operation)
            self.params={}
            for key,value in json.loads(str_params).items():
                if isinstance(value,list):
                    tmp_list=[]
                    for item in value:
                        tmp_list.append(uuid.UUID(item)) if args.is_valid_hex_uuid(item) or args.is_valid_hex_date(item) else item
                    self.params[key]=tmp_list
                else:
                    self.params[key]=uuid.UUID(value) if args.is_valid_hex_uuid(value) or args.is_valid_hex_date(value) else value
        else:
            if not args.is_valid_dict(params):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IPRM)
            if not isinstance(operation, Operations):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_RESAUTH_IOP)
            self.type=RESOURCE_AUTHORIZATION_UPDATE_MESSAGE
            self.operation=operation
            self.params=params
            str_params={}
            for key,value in params.items():
                if isinstance(value,list):
                    tmp_list=[]
                    for item in value:
                        tmp_list.append(item.hex) if args.is_valid_uuid(item) or args.is_valid_date(item) else item
                    str_params[key]=tmp_list
                else:
                    str_params[key]=value.hex if args.is_valid_uuid(value) or args.is_valid_date(value) else value
            self.serialized_message='|'.join((self.type,self.operation.name,json.dumps(str_params)))

class NewDPWidgetMessage:
    def __init__(self, serialized_message=None, uid=None, pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,pid = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            self.pid=uuid.UUID(pid)
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IUID)
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDPW_IPID)
            self.type=NEW_DP_WIDGET_MESSAGE
            self.uid=uid
            self.pid=pid
            self.serialized_message='|'.join((self.type,self.uid.hex,self.pid.hex))

class NewDSWidgetMessage:
    def __init__(self, serialized_message=None, uid=None, did=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,did = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            self.did=uuid.UUID(did)
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IUID)
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWDSW_IDID)
            self.type=NEW_DS_WIDGET_MESSAGE
            self.uid=uid
            self.did=did
            self.serialized_message='|'.join((self.type,self.uid.hex,self.did.hex))

class DeleteUserMessage:
    def __init__(self, serialized_message=None, uid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid= self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELUSER_IUID)
            self.type=DELETE_USER_MESSAGE
            self.uid=uid
            self.serialized_message='|'.join((self.type,self.uid.hex))

class DeleteAgentMessage:
    def __init__(self, serialized_message=None, aid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,aid = self.serialized_message.split('|')
            self.type=mtype
            self.aid=uuid.UUID(aid)
        else:
            if not args.is_valid_uuid(aid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELAGENT_IAID)
            self.type=DELETE_AGENT_MESSAGE
            self.aid=aid
            self.serialized_message='|'.join((self.type,self.aid.hex))

class DeleteDatasourceMessage:
    def __init__(self, serialized_message=None, did=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did = self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
        else:
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDS_IDID)
            self.type=DELETE_DATASOURCE_MESSAGE
            self.did=did
            self.serialized_message='|'.join((self.type,self.did.hex))

class DeleteDatapointMessage:
    def __init__(self, serialized_message=None, pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid = self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
        else:
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDP_IPID)
            self.type=DELETE_DATAPOINT_MESSAGE
            self.pid=pid
            self.serialized_message='|'.join((self.type,self.pid.hex))

class DeleteWidgetMessage:
    def __init__(self, serialized_message=None, wid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,wid = self.serialized_message.split('|')
            self.type=mtype
            self.wid=uuid.UUID(wid)
        else:
            if not args.is_valid_uuid(wid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELWIDGET_IWID)
            self.type=DELETE_WIDGET_MESSAGE
            self.wid=wid
            self.serialized_message='|'.join((self.type,self.wid.hex))

class DeleteDashboardMessage:
    def __init__(self, serialized_message=None, bid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,bid = self.serialized_message.split('|')
            self.type=mtype
            self.bid=uuid.UUID(bid)
        else:
            if not args.is_valid_uuid(bid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_DELDASHB_IBID)
            self.type=DELETE_DASHBOARD_MESSAGE
            self.bid=bid
            self.serialized_message='|'.join((self.type,self.bid.hex))

class UserEventMessage:
    def __init__(self, serialized_message=None, uid=None, event_type=None, parameters=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,event_type,parameters = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            self.event_type=int(event_type)
            self.parameters=json.loads(parameters)
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IUID)
            if not args.is_valid_int(event_type):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IET)
            if parameters and not args.is_valid_dict(parameters):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREV_IPRM)
            self.type=USER_EVENT_MESSAGE
            self.uid=uid
            self.event_type=event_type
            self.parameters=parameters if parameters else {}
            self.serialized_message='|'.join((self.type,self.uid.hex,str(self.event_type),json.dumps(self.parameters)))

class UserEventResponseMessage:
    def __init__(self, serialized_message=None, uid=None, date=None, parameters=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,date,parameters = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            self.date=uuid.UUID(date)
            self.parameters=json.loads(parameters)
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IUID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IDT)
            if parameters and not args.is_valid_dict(parameters):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_USEREVR_IPRM)
            self.type=USER_EVENT_RESPONSE_MESSAGE
            self.uid=uid
            self.date=date
            self.parameters=parameters if parameters else {}
            self.serialized_message='|'.join((self.type,self.uid.hex,self.date.hex,json.dumps(self.parameters)))

class GenerateTextSummaryMessage:
    def __init__(self, serialized_message=None, did=None,date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date=self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IDID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_GTXS_IDT)
            self.type=GENERATE_TEXT_SUMMARY_MESSAGE
            self.did=did
            self.date=date
            self.serialized_message='|'.join((self.type,self.did.hex,self.date.hex))

class MissingDatapointMessage:
    def __init__(self, serialized_message=None, did=None,date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date=self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(did):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MISSDP_IDID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_MISSDP_IDT)
            self.type=MISSING_DATAPOINT_MESSAGE
            self.did=did
            self.date=date
            self.serialized_message='|'.join((self.type,self.did.hex,self.date.hex))

class NewInvitationMailMessage:
    def __init__(self, serialized_message=None, email=None, inv_id=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,email,inv_id = self.serialized_message.split('|')
            self.type=mtype
            self.email=email
            self.inv_id=uuid.UUID(inv_id)
        else:
            if not args.is_valid_email(email):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_IEMAIL)
            if not args.is_valid_uuid(inv_id):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_NEWINV_IINV)
            self.type=NEW_INV_MAIL_MESSAGE
            self.email=email
            self.inv_id=inv_id
            self.serialized_message='|'.join((self.type,self.email,self.inv_id.hex))

class ForgetMailMessage:
    def __init__(self, serialized_message=None, email=None, code=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,email,code= self.serialized_message.split('|')
            self.type=mtype
            self.email=email
            self.code=uuid.UUID(code)
        else:
            if not args.is_valid_email(email):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_IEMAIL)
            if not args.is_valid_uuid(code):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_FORGET_ICODE)
            self.type=FORGET_MAIL_MESSAGE
            self.email=email
            self.code=code
            self.serialized_message='|'.join((self.type,self.email,self.code.hex))

class UrisUpdatedMessage:
    def __init__(self, serialized_message=None, uris=None, date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uris,date=self.serialized_message.split('|')
            self.type=mtype
            uris=json.loads(uris)
            self.date=uuid.UUID(date)
            self.uris=[]
            for uri in uris:
                uri['id']=uuid.UUID(uri['id'])
                self.uris.append(uri)
        else:
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_URUP_IDT)
            self.type=URIS_UPDATED_MESSAGE
            self.uris=uris
            self.date=date
            uri_list=[]
            for uri in uris:
                uri_list.append({'uri':uri['uri'],'type':uri['type'],'id':uri['id'].hex})
            s_uris=json.dumps(uri_list)
            self.serialized_message='|'.join((self.type,s_uris,self.date.hex))

class SendSessionDataMessage:
    def __init__(self, serialized_message=None, sid=None, data=None, date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,sid,data,date=self.serialized_message.split('|')
            self.type=mtype
            self.sid=uuid.UUID(sid)
            self.data=json.loads(data)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(sid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_ISID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_SSDT_IDT)
            self.type=SEND_SESSION_DATA_MESSAGE
            self.sid=sid
            self.data=data
            self.date=date
            self.serialized_message='|'.join((self.type,self.sid.hex,json.dumps(self.data),self.date.hex))

class ClearSessionHooksMessage:
    def __init__(self, serialized_message=None, sid=None, ids=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,sid,ids=self.serialized_message.split('|')
            self.type=mtype
            self.sid=uuid.UUID(sid)
            self.ids=[]
            ids_array=json.loads(ids)
            for id_hex, id_type in ids_array:
                self.ids.append((uuid.UUID(id_hex),id_type))
        else:
            if not args.is_valid_uuid(sid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_CSH_ISID)
            self.type=CLEAR_SESSION_HOOKS_MESSAGE
            self.sid=sid
            self.ids=ids
            ids_array=[(item[0].hex,item[1]) for item in self.ids]
            self.serialized_message='|'.join((self.type,self.sid.hex,json.dumps(ids_array)))

class HookNewUrisMessage:
    def __init__(self, serialized_message=None, uid=None, uris=None, date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,uris,date=self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            uris=json.loads(uris)
            self.date=uuid.UUID(date)
            self.uris=[]
            for uri in uris:
                uri['id']=uuid.UUID(uri['id'])
                self.uris.append(uri)
        else:
            if not args.is_valid_uuid(uid):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IUID)
            if not args.is_valid_date(date):
                raise exceptions.BadParametersException(error=Errors.E_IIMM_HNU_IDT)
            self.type=HOOK_NEW_URIS_MESSAGE
            self.uid=uid
            self.uris=uris
            self.date=date
            uri_list=[]
            for uri in uris:
                uri_list.append({'uri':uri['uri'],'type':uri['type'],'id':uri['id'].hex})
            s_uris=json.dumps(uri_list)
            self.serialized_message='|'.join((self.type,self.uid.hex,s_uris,self.date.hex))

#MESSAGE MAPPINGS
MESSAGE_TO_CLASS_MAPPING={
    MAP_VARS_MESSAGE:MapVarsMessage,
    MON_VAR_MESSAGE:MonitorVariableMessage,
    GDTREE_MESSAGE:GenerateDTreeMessage,
    FILL_DATAPOINT_MESSAGE:FillDatapointMessage,
    FILL_DATASOURCE_MESSAGE:FillDatasourceMessage,
    NEG_VAR_MESSAGE:NegativeVariableMessage,
    POS_VAR_MESSAGE:PositiveVariableMessage,
    NEW_USR_NOTIF_MESSAGE:NewUserNotificationMessage,
    UPDATE_QUOTES_MESSAGE:UpdateQuotesMessage,
    RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:ResourceAuthorizationUpdateMessage,
    NEW_DP_WIDGET_MESSAGE:NewDPWidgetMessage,
    NEW_DS_WIDGET_MESSAGE:NewDSWidgetMessage,
    DELETE_USER_MESSAGE:DeleteUserMessage,
    DELETE_AGENT_MESSAGE:DeleteAgentMessage,
    DELETE_DATASOURCE_MESSAGE:DeleteDatasourceMessage,
    DELETE_DATAPOINT_MESSAGE:DeleteDatapointMessage,
    DELETE_WIDGET_MESSAGE:DeleteWidgetMessage,
    DELETE_DASHBOARD_MESSAGE:DeleteDashboardMessage,
    USER_EVENT_MESSAGE:UserEventMessage,
    USER_EVENT_RESPONSE_MESSAGE:UserEventResponseMessage,
    GENERATE_TEXT_SUMMARY_MESSAGE:GenerateTextSummaryMessage,
    MISSING_DATAPOINT_MESSAGE:MissingDatapointMessage,
    NEW_INV_MAIL_MESSAGE:NewInvitationMailMessage,
    FORGET_MAIL_MESSAGE:ForgetMailMessage,
    URIS_UPDATED_MESSAGE:UrisUpdatedMessage,
    SEND_SESSION_DATA_MESSAGE:SendSessionDataMessage,
    CLEAR_SESSION_HOOKS_MESSAGE:ClearSessionHooksMessage,
    HOOK_NEW_URIS_MESSAGE:HookNewUrisMessage,
}

