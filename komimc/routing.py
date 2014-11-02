'''
Created on 02/11/2014

komimc: komlog inter module communication mappings

mappings: komlog message and address mappings

@author: jcazor
'''

from komimc import messages

#QPID ADDRESS CONSTANTS
BASE_IMC_ADDRESS = 'org.komlog.internal.imc.address.'


#MODULE LIST
VALIDATION='Validation'
STORING='Storing'
TEXTMINING='Textmining'
GESTCONSOLE='Gestconsole'
RESCONTROL='Rescontrol'


MESSAGE_TO_ADDRESS_MAPPING={messages.STORE_SAMPLE_MESSAGE:STORING+'.%h',
                            messages.MAP_VARS_MESSAGE:TEXTMINING,
                            messages.MON_VAR_MESSAGE:GESTCONSOLE,
                            messages.GDTREE_MESSAGE:TEXTMINING,
                            messages.FILL_DATAPOINT_MESSAGE:TEXTMINING,
                            messages.NEG_VAR_MESSAGE:GESTCONSOLE,
                            messages.POS_VAR_MESSAGE:GESTCONSOLE,
                            messages.NEW_USR_MESSAGE:GESTCONSOLE,
                            messages.UPDATE_QUOTES_MESSAGE:RESCONTROL,
                            messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:RESCONTROL
                            }


#MODULE MAPPINGS
MODULE_TO_ADDRESS_MAPPING={VALIDATION:'%m.%h',
                           STORING:'%m.%h',
                           TEXTMINING:'%m',
                           GESTCONSOLE:'%m',
                           RESCONTROL:'%m'
                           }


def get_address(type, module_id, module_instance, running_host):
    if MESSAGE_TO_ADDRESS_MAPPING.has_key(type):
        address = MESSAGE_TO_ADDRESS_MAPPING[type]
        address = address.replace('%h',running_host)
        address = address.replace('%m',module_id)
        address = address.replace('%i',str(module_instance))
        address = BASE_IMC_ADDRESS+address
        address = address
        return address
    else:
        return None

def get_mod_address(module_id, module_instance, running_host):
    if MODULE_TO_ADDRESS_MAPPING.has_key(module_id):
        address = MODULE_TO_ADDRESS_MAPPING[module_id]
        address = address.replace('%h',running_host)
        address = address.replace('%m',module_id)
        address = address.replace('%i',str(module_instance))
        address = BASE_IMC_ADDRESS+address
        address = address
        return address
    else:
        return None


