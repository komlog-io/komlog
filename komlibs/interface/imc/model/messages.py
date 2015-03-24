'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

import uuid
import json
from komlibs.interface.imc import exceptions
from komlibs.general.validation import arguments as args
from komfig import logger


#MESSAGE LIST
STORE_SAMPLE_MESSAGE='STOSMP'
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
SHARED_AUTHORIZATION_UPDATE_MESSAGE='SHAREDAUTH'
MEMBERSHIP_AUTHORIZATION_UPDATE_MESSAGE='MEMBERSAUTH'
NEW_DP_WIDGET_MESSAGE='NEWDPW'
NEW_DS_WIDGET_MESSAGE='NEWDSW'
DELETE_USER_MESSAGE='DELUSER'
DELETE_AGENT_MESSAGE='DELAGENT'
DELETE_DATASOURCE_MESSAGE='DELDS'
DELETE_DATAPOINT_MESSAGE='DELDP'
DELETE_WIDGET_MESSAGE='DELWIDGET'
DELETE_DASHBOARD_MESSAGE='DELDASHB'


#MESSAGE MAPPINGS
MESSAGE_TO_CLASS_MAPPING={STORE_SAMPLE_MESSAGE:'StoreSampleMessage',
                          MAP_VARS_MESSAGE:'MapVarsMessage',
                          MON_VAR_MESSAGE:'MonitorVariableMessage',
                          GDTREE_MESSAGE:'GenerateDTreeMessage',
                          FILL_DATAPOINT_MESSAGE:'FillDatapointMessage',
                          FILL_DATASOURCE_MESSAGE:'FillDatasourceMessage',
                          NEG_VAR_MESSAGE:'NegativeVariableMessage',
                          POS_VAR_MESSAGE:'PositiveVariableMessage',
                          NEW_USR_NOTIF_MESSAGE:'NewUserNotificationMessage',
                          UPDATE_QUOTES_MESSAGE:'UpdateQuotesMessage',
                          RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:'ResourceAuthorizationUpdateMessage',
                          SHARED_AUTHORIZATION_UPDATE_MESSAGE:'SharedAuthorizationUpdateMessage',
                          MEMBERSHIP_AUTHORIZATION_UPDATE_MESSAGE:'MembershipAuthorizationUpdateMessage',
                          NEW_DP_WIDGET_MESSAGE:'NewDPWidgetMessage',
                          NEW_DS_WIDGET_MESSAGE:'NewDSWidgetMessage',
                          DELETE_USER_MESSAGE:'DeleteUserMessage',
                          DELETE_AGENT_MESSAGE:'DeleteAgentMessage',
                          DELETE_DATASOURCE_MESSAGE:'DeleteDatasourceMessage',
                          DELETE_DATAPOINT_MESSAGE:'DeleteDatapointMessage',
                          DELETE_WIDGET_MESSAGE:'DeleteWidgetMessage',
                          DELETE_DASHBOARD_MESSAGE:'DeleteDashboardMessage',
                          }


class StoreSampleMessage:
    def __init__(self, serialized_message=None, sample_file=None):
        if serialized_message:
            self.serialized_message=serialized_message
            self.type=self.serialized_message.split('|')[0]
            self.sample_file=self.serialized_message.split('|')[1]
        else:
            if not args.is_valid_string(sample_file):
                raise exceptions.BadParametersException()
            self.type=STORE_SAMPLE_MESSAGE
            self.sample_file=sample_file
            self.serialized_message=self.type+'|'+self.sample_file

class MapVarsMessage:
    def __init__(self, serialized_message=None, did=None,date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date=self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
        else:
            if not args.is_valid_uuid(did) or not args.is_valid_date(date):
                raise exceptions.BadParametersException()
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
            if not args.is_valid_uuid(uid) or not args.is_valid_uuid(did) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length) or not args.is_valid_datapointname(datapointname):
                raise exceptions.BadParametersException()
            self.type=MON_VAR_MESSAGE
            self.uid=uid
            self.did=did
            self.date=date
            self.position=position
            self.length=length
            self.datapointname=datapointname
            self.serialized_message=self.type+'|'+self.uid.hex+'|'+self.did.hex+'|'+self.date.hex+'|'+str(self.position)+'|'+str(self.length)+'|'+self.datapointname

class GenerateDTreeMessage:
    def __init__(self, serialized_message=None, pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid=self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
        else:
            if not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException()
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
            if not args.is_valid_uuid(pid) or not args.is_valid_date(date):
                raise exceptions.BadParametersException()
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
            if not args.is_valid_uuid(did) or not args.is_valid_date(date):
                raise exceptions.BadParametersException()
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
            if not args.is_valid_uuid(pid) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length):
                raise exceptions.BadParametersException()
            self.type=NEG_VAR_MESSAGE
            self.pid=pid
            self.date=date
            self.position=position
            self.length=length
            self.serialized_message=self.type+'|'+self.pid.hex+'|'+self.date.hex+'|'+str(self.position)+'|'+str(self.length)

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
            if not args.is_valid_uuid(pid) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length):
                raise exceptions.BadParametersException()
            self.type=POS_VAR_MESSAGE
            self.pid=pid
            self.date=date
            self.position=position
            self.length=length
            self.serialized_message=self.type+'|'+self.pid.hex+'|'+self.date.hex+'|'+str(self.position)+'|'+str(self.length)

class NewUserNotificationMessage:
    def __init__(self, serialized_message=None, email=None, code=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,email,code = self.serialized_message.split('|')
            self.type=mtype
            self.email=email
            self.code=code
        else:
            if not args.is_valid_email(email) or not args.is_valid_code(code):
                raise exceptions.BadParametersException()
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
            self.operation=int(operation)
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
            if not args.is_valid_int(operation) or not args.is_valid_dict(params):
                raise exceptions.BadParametersException()
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
            self.serialized_message='|'.join((self.type,str(self.operation),json.dumps(str_params)))

class ResourceAuthorizationUpdateMessage:
    def __init__(self, serialized_message=None, operation=None, params=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,operation,str_params = self.serialized_message.split('|')
            self.type=mtype
            self.operation=int(operation)
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
            if not args.is_valid_int(operation) or not args.is_valid_dict(params):
                raise exceptions.BadParametersException()
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
            self.serialized_message='|'.join((self.type,str(self.operation),json.dumps(str_params)))

class SharedAuthorizationUpdateMessage:
    def __init__(self, serialized_message=None, operation=None, params=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,operation,str_params = self.serialized_message.split('|')
            self.type=mtype
            self.operation=int(operation)
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
            if not args.is_valid_int(operation) or not args.is_valid_dict(params):
                raise exceptions.BadParametersException()
            self.type=SHARED_AUTHORIZATION_UPDATE_MESSAGE
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
            self.serialized_message='|'.join((self.type,str(self.operation),json.dumps(str_params)))

class MembershipAuthorizationUpdateMessage:
    def __init__(self, serialized_message=None, operation=None, params=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,operation,str_params = self.serialized_message.split('|')
            self.type=mtype
            self.operation=int(operation)
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
            if not args.is_valid_int(operation) or not args.is_valid_dict(params):
                raise exceptions.BadParametersException()
            self.type=MEMBERSHIP_AUTHORIZATION_UPDATE_MESSAGE
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
            self.serialized_message='|'.join((self.type,str(self.operation),json.dumps(str_params)))

class NewDPWidgetMessage:
    def __init__(self, serialized_message=None, uid=None, pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid,pid = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
            self.pid=uuid.UUID(pid)
        else:
            if not args.is_valid_uuid(uid) or not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException()
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
            if not args.is_valid_uuid(uid) or not args.is_valid_uuid(did):
                raise exceptions.BadParametersException()
            self.type=NEW_DS_WIDGET_MESSAGE
            self.uid=uid
            self.did=did
            self.serialized_message='|'.join((self.type,self.uid.hex,self.did.hex))

class DeleteUserMessage:
    def __init__(self, serialized_message=None, username=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,username = self.serialized_message.split('|')
            self.type=mtype
            self.username=username
        else:
            if not args.is_valid_username(username):
                raise exceptions.BadParametersException()
            self.type=DELETE_USER_MESSAGE
            self.username=username
            self.serialized_message='|'.join((self.type,self.username))

class DeleteAgentMessage:
    def __init__(self, serialized_message=None, aid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,aid = self.serialized_message.split('|')
            self.type=mtype
            self.aid=uuid.UUID(aid)
        else:
            if not args.is_valid_uuid(aid):
                raise exceptions.BadParametersException()
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
                raise exceptions.BadParametersException()
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
                raise exceptions.BadParametersException()
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
                raise exceptions.BadParametersException()
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
                raise exceptions.BadParametersException()
            self.type=DELETE_DASHBOARD_MESSAGE
            self.bid=bid
            self.serialized_message='|'.join((self.type,self.bid.hex))

