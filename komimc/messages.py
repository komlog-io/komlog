'''
Created on 07/02/2013

komimc: komlog inter module communication

messages: komlog custom messages class implementations for inter module communication

@author: jcazor
'''

import exceptions
from qpid.messaging import Message

BASE_IMC_ADDRESS = 'pro.komlog.internal.imc.address.'
QPID_ADDR_OPTIONS='; {create:always}'

STORE_SAMPLE_MESSAGE='STOSMP'
MAP_VARS_MESSAGE='MAPVAR'

MESSAGE_TO_CLASS_MAPPING={STORE_SAMPLE_MESSAGE:'StoreSampleMessage',
                          MAP_VARS_MESSAGE:'MapVarsMessage'}

MESSAGE_TO_ADDRESS_MAPPING={STORE_SAMPLE_MESSAGE:'Storing.%h',
                            MAP_VARS_MESSAGE:'Textmining'}

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
    def __init__(self, qpid_message=None, sid=None):
        if qpid_message:
            self.qpid_message=qpid_message
            self.type=self.qpid_message.content.split('|')[0]
            self.sid=self.qpid_message.content.split('|')[1]
        else:
            self.type=MAP_VARS_MESSAGE
            self.sid=sid
            self.qpid_message=Message(self.type+'|'+str(self.sid))
       

def get_address(type, module_id, module_instance, running_host):
    address = MESSAGE_TO_ADDRESS_MAPPING[type]
    address = address.replace('%h',running_host)
    address = address.replace('%m',module_id)
    address = address.replace('%i',str(module_instance))
    address = BASE_IMC_ADDRESS+address
    address = address+QPID_ADDR_OPTIONS
    return address

    
    
    
