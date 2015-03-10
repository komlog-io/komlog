'''
Created on 02/11/2014

komimc: komlog inter module communication mappings

mappings: komlog message and address mappings

@author: jcazor
'''

from komlibs.interface.imc.model import messages

#ADDRESS CONSTANTS
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
                            messages.FILL_DATASOURCE_MESSAGE:TEXTMINING,
                            messages.NEG_VAR_MESSAGE:GESTCONSOLE,
                            messages.POS_VAR_MESSAGE:GESTCONSOLE,
                            messages.NEW_USR_NOTIF_MESSAGE:GESTCONSOLE,
                            messages.UPDATE_QUOTES_MESSAGE:RESCONTROL,
                            messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:RESCONTROL,
                            messages.SHARED_AUTHORIZATION_UPDATE_MESSAGE:RESCONTROL,
                            messages.NEW_DP_WIDGET_MESSAGE:GESTCONSOLE,
                            messages.NEW_DS_WIDGET_MESSAGE:GESTCONSOLE,
                            messages.DELETE_USER_MESSAGE:GESTCONSOLE,
                            messages.DELETE_AGENT_MESSAGE:GESTCONSOLE,
                            messages.DELETE_DATASOURCE_MESSAGE:GESTCONSOLE,
                            messages.DELETE_DATAPOINT_MESSAGE:GESTCONSOLE,
                            messages.DELETE_WIDGET_MESSAGE:GESTCONSOLE,
                            messages.DELETE_DASHBOARD_MESSAGE:GESTCONSOLE,
                            }


#MODULE MAPPINGS
MODULE_TO_ADDRESS_MAPPING={VALIDATION:['%m.%h','%i.%m.%h'],
                           STORING:['%m.%h','%i.%m.%h'],
                           TEXTMINING:['%m','%i.%m.%h'],
                           GESTCONSOLE:['%m','%i.%m.%h'],
                           RESCONTROL:['%m','%i.%m.%h']
                           }


def get_address(type, module_id, module_instance, running_host):
    if type in MESSAGE_TO_ADDRESS_MAPPING:
        address = MESSAGE_TO_ADDRESS_MAPPING[type]
        address = address.replace('%h',running_host)
        address = address.replace('%m',module_id)
        address = address.replace('%i',str(module_instance))
        address = BASE_IMC_ADDRESS+address
        return address
    else:
        return None

def get_mod_address(module_id, module_instance, running_host):
    if module_id in MODULE_TO_ADDRESS_MAPPING:
        address_list=[]
        for address in MODULE_TO_ADDRESS_MAPPING[module_id]:
            address = address.replace('%h',running_host)
            address = address.replace('%m',module_id)
            address = address.replace('%i',str(module_instance))
            address = BASE_IMC_ADDRESS+address
            address_list.append(address)
        return address_list
    else:
        return None


