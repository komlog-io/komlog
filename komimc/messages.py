'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

from komimc import exceptions
from komimc import codes as msgcodes
from komlibs.ifaceops import operations
from komfig import logger
import uuid
import json
import dateutil.parser


#MESSAGE LIST
STORE_SAMPLE_MESSAGE='STOSMP'
MAP_VARS_MESSAGE='MAPVARS'
MON_VAR_MESSAGE='MONVAR'
GDTREE_MESSAGE='GDTREE'
FILL_DATAPOINT_MESSAGE='FILDTP'
NEG_VAR_MESSAGE='NEGVAR'
POS_VAR_MESSAGE='POSVAR'
NEW_USR_MESSAGE='NEWUSR'
UPDATE_QUOTES_MESSAGE='UPDQUO'
RESOURCE_AUTHORIZATION_UPDATE_MESSAGE='RESAUTH'

#MESSAGE MAPPINGS
MESSAGE_TO_CLASS_MAPPING={STORE_SAMPLE_MESSAGE:'StoreSampleMessage',
                          MAP_VARS_MESSAGE:'MapVarsMessage',
                          MON_VAR_MESSAGE:'MonitorVariableMessage',
                          GDTREE_MESSAGE:'GenerateDTreeMessage',
                          FILL_DATAPOINT_MESSAGE:'FillDatapointMessage',
                          NEG_VAR_MESSAGE:'NegativeVariableMessage',
                          POS_VAR_MESSAGE:'PositiveVariableMessage',
                          NEW_USR_MESSAGE:'NewUserMessage',
                          UPDATE_QUOTES_MESSAGE:'UpdateQuotesMessage',
                          RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:'ResourceAuthorizationUpdateMessage',
                          }


class MessageResult:
    def __init__(self,message):
        self.mtype=message.type
        self.mparams=message.serialized_message
        self.retcode=None
        self._msgoriginated=[]

    def add_msg_originated(self, msg, index=0):
        array_position=int(index) if index else len(self._msgoriginated)
        self._msgoriginated.insert(array_position,msg)

    def get_msg_originated(self):
        return self._msgoriginated

class StoreSampleMessage:
    def __init__(self, serialized_message=None, sample_file=None):
        if serialized_message:
            self.serialized_message=serialized_message
            self.type=self.serialized_message.split('|')[0]
            self.sample_file=self.serialized_message.split('|')[1]
        else:
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
            self.date=dateutil.parser.parse(date)
        else:
            self.type=MAP_VARS_MESSAGE
            self.did=did
            self.date=date
            self.serialized_message=self.type+'|'+str(self.did)+'|'+date.isoformat()

class MonitorVariableMessage:
    def __init__(self, serialized_message=None, did=None, date=None, pos=None, length=None, name=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date,pos,length,name = self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.date=dateutil.parser.parse(date)
            self.pos=str(pos)
            self.length=str(length)
            self.name=str(name)
        else:
            self.type=MON_VAR_MESSAGE
            self.did=did
            self.date=date
            self.pos=str(pos)
            self.length=str(length)
            self.name=str(name)
            self.serialized_message=self.type+'|'+str(self.did)+'|'+date.isoformat()+'|'+str(self.pos)+'|'+str(self.length)+'|'+str(self.name)

class GenerateDTreeMessage:
    def __init__(self, serialized_message=None, pid=None, date=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,pid,date=self.serialized_message.split('|')
            self.type=mtype
            self.pid=uuid.UUID(pid)
            self.date=dateutil.parser.parse(date)
        else:
            self.type=GDTREE_MESSAGE
            self.pid=pid
            self.date=date
            self.serialized_message=self.type+'|'+str(self.pid)+'|'+date.isoformat()

class FillDatapointMessage:
    def __init__(self, serialized_message=None, did=None,date=None,pid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,date,pid=self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did) if not str(did)=='None' else None
            self.date=dateutil.parser.parse(date) if not str(date)=='None' else None
            self.pid=uuid.UUID(pid) if not str(pid)=='None' else None
        else:
            self.type=FILL_DATAPOINT_MESSAGE
            self.did=did
            self.date=date
            self.pid=pid
            self.serialized_message=self.type+'|'+str(self.did)+'|'+self.date.isoformat()+'|'+str(self.pid)

class NegativeVariableMessage:
    def __init__(self, serialized_message=None, did=None, pid=None, date=None, pos=None, length=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,pid,date,pos,length = self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.pid=uuid.UUID(pid)
            self.date=dateutil.parser.parse(date)
            self.pos=str(pos)
            self.length=str(length)
        else:
            self.type=NEG_VAR_MESSAGE
            self.did=did
            self.pid=pid
            self.date=date
            self.pos=str(pos)
            self.length=str(length)
            self.serialized_message=self.type+'|'+str(self.did)+'|'+str(self.pid)+'|'+date.isoformat()+'|'+str(self.pos)+'|'+str(self.length)

class PositiveVariableMessage:
    def __init__(self, serialized_message=None, did=None, pid=None, date=None, pos=None, length=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,did,pid,date,pos,length = self.serialized_message.split('|')
            self.type=mtype
            self.did=uuid.UUID(did)
            self.pid=uuid.UUID(pid)
            self.date=dateutil.parser.parse(date)
            self.pos=int(pos)
            self.length=int(length)
        else:
            self.type=POS_VAR_MESSAGE
            self.did=did
            self.pid=pid
            self.date=date
            self.pos=pos
            self.length=length
            self.serialized_message=self.type+'|'+str(self.did)+'|'+str(self.pid)+'|'+date.isoformat()+'|'+str(self.pos)+'|'+str(self.length)

class NewUserMessage:
    def __init__(self, serialized_message=None, uid=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,uid = self.serialized_message.split('|')
            self.type=mtype
            self.uid=uuid.UUID(uid)
        else:
            self.type=NEW_USR_MESSAGE
            self.uid=uid
            self.serialized_message=self.type+'|'+str(self.uid)

class UpdateQuotesMessage:
    def __init__(self, serialized_message=None, operation=None):
        if serialized_message:
            self.serialized_message=serialized_message
            mtype,json_serialization = self.serialized_message.split('|')
            self.type=mtype
            operation_dict=json.loads(json_serialization)
            operation_class=operation_dict['opclass']
            operation_dict.pop('opclass',None)
            self.operation=getattr(operations,operation_class)(**operation_dict)
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
            self.operation=getattr(operations,operation_class)(**operation_dict)
        else:
            self.type=RESOURCE_AUTHORIZATION_UPDATE_MESSAGE
            self.operation=operation
            self.serialized_message=self.type+'|'+self.operation.get_json_serialization()

