'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

import uuid
import json
from komlibs.interface.web.operations import weboperations
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
NEW_DP_WIDGET_MESSAGE='NEWDPW'
NEW_DS_WIDGET_MESSAGE='NEWDSW'

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
                          NEW_DP_WIDGET_MESSAGE:'NewDPWidgetMessage',
                          NEW_DS_WIDGET_MESSAGE:'NewDSWidgetMessage',
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
    def __init__(self, serialized_message=None, username=None, did=None, date=None, position=None, length=None, datapointname=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,username,did,date,position,length,datapointname = self.serialized_message.split('|')
            self.type=mtype
            self.username=username
            self.did=uuid.UUID(did)
            self.date=uuid.UUID(date)
            self.position=int(position)
            self.length=int(length)
            self.datapointname=datapointname
        else:
            if not args.is_valid_username(username) or not args.is_valid_uuid(did) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length) or not args.is_valid_datapointname(datapointname):
                raise exceptions.BadParametersException()
            self.type=MON_VAR_MESSAGE
            self.username=username
            self.did=did
            self.date=date
            self.position=position
            self.length=length
            self.datapointname=datapointname
            self.serialized_message=self.type+'|'+self.username+'|'+self.did.hex+'|'+self.date.hex+'|'+str(self.position)+'|'+str(self.length)+'|'+self.datapointname

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
    def __init__(self, serialized_message=None, operation=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,json_serialization = self.serialized_message.split('|')
            self.type=mtype
            operation_dict=json.loads(json_serialization)
            operation_class=operation_dict['opclass']
            operation_dict.pop('opclass',None)
            self.operation=getattr(weboperations,operation_class)(**operation_dict)
        else:
            self.type=UPDATE_QUOTES_MESSAGE
            self.operation=operation
            self.serialized_message=self.type+'|'+self.operation.get_json_serialization()

class ResourceAuthorizationUpdateMessage:
    def __init__(self, serialized_message=None, operation=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,json_serialization = self.serialized_message.split('|')
            self.type=mtype
            operation_dict=json.loads(json_serialization)
            operation_class=operation_dict['opclass']
            operation_dict.pop('opclass',None)
            self.operation=getattr(weboperations,operation_class)(**operation_dict)
        else:
            self.type=RESOURCE_AUTHORIZATION_UPDATE_MESSAGE
            self.operation=operation
            self.serialized_message=self.type+'|'+self.operation.get_json_serialization()

class NewDPWidgetMessage:
    def __init__(self, serialized_message=None, username=None, pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,username,pid = self.serialized_message.split('|')
            self.type=mtype
            self.username=username
            self.pid=uuid.UUID(pid)
        else:
            if not args.is_valid_username(username) or not args.is_valid_uuid(pid):
                raise exceptions.BadParametersException()
            self.type=NEW_DP_WIDGET_MESSAGE
            self.username=username
            self.pid=pid
            self.serialized_message='|'.join((self.type,self.username,self.pid.hex))

class NewDSWidgetMessage:
    def __init__(self, serialized_message=None, username=None, did=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,username,did = self.serialized_message.split('|')
            self.type=mtype
            self.username=username
            self.did=uuid.UUID(did)
        else:
            if not args.is_valid_username(username) or not args.is_valid_uuid(did):
                raise exceptions.BadParametersException()
            self.type=NEW_DS_WIDGET_MESSAGE
            self.username=username
            self.did=did
            self.serialized_message='|'.join((self.type,self.username,self.did.hex))

