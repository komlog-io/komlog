'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

import exceptions
from qpid.messaging import Message
import uuid
import dateutil.parser

#QPID ADDRESS CONSTANTS
BASE_IMC_ADDRESS = 'pro.komlog.internal.imc.address.'
QPID_ADDR_OPTIONS='; {create:always}'


#MESSAGE LIST
STORE_SAMPLE_MESSAGE='STOSMP'
MAP_VARS_MESSAGE='MAPVARS'
MON_VAR_MESSAGE='MONVAR'
GDTREE_MESSAGE='GDTREE'
FILL_DATAPOINT_MESSAGE='FILDTP'

#MODULE LIST
VALIDATION='Validation'
STORING='Storing'
TEXTMINING='Textmining'
GESTCONSOLE='Gestconsole'

#MESSAGE MAPPINGS
MESSAGE_TO_CLASS_MAPPING={STORE_SAMPLE_MESSAGE:'StoreSampleMessage',
                          MAP_VARS_MESSAGE:'MapVarsMessage',
                          MON_VAR_MESSAGE:'MonitorVariableMessage',
                          GDTREE_MESSAGE:'GenerateDTreeMessage',
                          FILL_DATAPOINT_MESSAGE:'FillDatapointMessage'}


MESSAGE_TO_ADDRESS_MAPPING={STORE_SAMPLE_MESSAGE:STORING+'.%h',
                            MAP_VARS_MESSAGE:TEXTMINING,
                            MON_VAR_MESSAGE:GESTCONSOLE,
                            GDTREE_MESSAGE:TEXTMINING,
                            FILL_DATAPOINT_MESSAGE:TEXTMINING}


#MODULE MAPPINGS
MODULE_TO_ADDRESS_MAPPING={VALIDATION:'%m.%h',
                           STORING:'%m.%h',
                           TEXTMINING:'%m',
                           GESTCONSOLE:'%m'}


def get_address(type, module_id, module_instance, running_host):
    if MESSAGE_TO_ADDRESS_MAPPING.has_key(type):
        address = MESSAGE_TO_ADDRESS_MAPPING[type]
        address = address.replace('%h',running_host)
        address = address.replace('%m',module_id)
        address = address.replace('%i',str(module_instance))
        address = BASE_IMC_ADDRESS+address
        address = address
        return address,QPID_ADDR_OPTIONS
    else:
        return None,QPID_ADDR_OPTIONS

def get_mod_address(module_id, module_instance, running_host):
    if MODULE_TO_ADDRESS_MAPPING.has_key(module_id):
        address = MODULE_TO_ADDRESS_MAPPING[module_id]
        address = address.replace('%h',running_host)
        address = address.replace('%m',module_id)
        address = address.replace('%i',str(module_instance))
        address = BASE_IMC_ADDRESS+address
        address = address
        return address,QPID_ADDR_OPTIONS
    else:
        return None,QPID_ADDR_OPTIONS

class StoreSampleMessage:
    def __init__(self, qpid_message=None, sample_file=None):
        if qpid_message:
            self.qpid_message=qpid_message
            self.type=self.qpid_message.content.split('|')[0]
            self.sample_file=self.qpid_message.content.split('|')[1]
        else:
            self.type=STORE_SAMPLE_MESSAGE
            self.sample_file=sample_file
            self.qpid_message=Message(self.type+'|'+self.sample_file)

class MapVarsMessage:
    def __init__(self, qpid_message=None, did=None,date=None):
        if qpid_message:
            self.qpid_message=qpid_message
            type,did,date=self.qpid_message.content.split('|')
            self.type=type
            self.did=uuid.UUID(did)
            self.date=dateutil.parser.parse(date)
        else:
            self.type=MAP_VARS_MESSAGE
            self.did=did
            self.date=date
            self.qpid_message=Message(self.type+'|'+str(self.did)+'|'+date.isoformat())

class MonitorVariableMessage:
    def __init__(self, qpid_message=None, did=None, date=None, var=None, name=None):
        if qpid_message:
            self.qpid_message=qpid_message
            type,did,date,var,name = self.qpid_message.content.split('|')
            self.type=type
            self.did=uuid.UUID(did)
            self.date=dateutil.parser.parse(date)
            self.var=str(var)
            self.name=str(name)
        else:
            self.type=MON_VAR_MESSAGE
            self.did=did
            self.date=date
            self.var=str(var)
            self.name=str(name)
            self.qpid_message=Message(self.type+'|'+str(self.did)+'|'+date.isoformat()+'|'+str(self.var)+'|'+str(self.name))

class GenerateDTreeMessage:
    def __init__(self, qpid_message=None, pid=None, date=None):
        if qpid_message:
            self.qpid_message=qpid_message
            type,pid,date=self.qpid_message.content.split('|')
            self.type=type
            self.pid=uuid.UUID(pid)
            self.date=date
        else:
            self.type=GDTREE_MESSAGE
            self.pid=pid
            self.date=date
            self.qpid_message=Message(self.type+'|'+str(self.pid)+'|'+date.isoformat())


class FillDatapointMessage:
    def __init__(self, qpid_message=None, did=None,date=None,pid=None):
        if qpid_message:
            self.qpid_message=qpid_message
            type,did,date,pid=self.qpid_message.content.split('|')
            self.type=type
            self.did=uuid.UUID(did) if not str(did)=='None' else None
            self.date=dateutil.parser.parse(date) if not str(date)=='None' else None
            self.pid=uuid.UUID(pid) if not str(pid)=='None' else None
        else:
            self.type=FILL_DATAPOINT_MESSAGE
            self.did=did
            self.date=date
            self.pid=pid
            self.qpid_message=Message(self.type+'|'+str(self.did)+'|'+self.date.isoformat()+'|'+str(self.pid))

