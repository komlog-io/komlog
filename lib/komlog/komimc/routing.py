'''
Created on 02/11/2014

komimc: komlog inter module communication mappings

mappings: komlog message and address mappings

@author: jcazor
'''

from komlog.komlibs.interface.imc.model import messages

#ADDRESS CONSTANTS
BASE_IMC_ADDRESS = 'org.komlog.internal.imc.module'


#MODULE LIST
VALIDATION='Validation'
STORING='Storing'
TEXTMINING='Textmining'
GESTCONSOLE='Gestconsole'
RESCONTROL='Rescontrol'
EVENTS='Events'
ANOMALIES='Anomalies'
WEBSOCKETSERVER='Websocketserver'
LAMBDAS='Lambdas'


MESSAGE_TO_ADDRESS_MAPPING={
    messages.STORE_SAMPLE_MESSAGE:STORING+'.%h',
    messages.MAP_VARS_MESSAGE:TEXTMINING,
    messages.MON_VAR_MESSAGE:GESTCONSOLE,
    messages.GDTREE_MESSAGE:TEXTMINING,
    messages.FILL_DATAPOINT_MESSAGE:TEXTMINING,
    messages.FILL_DATASOURCE_MESSAGE:TEXTMINING,
    messages.GENERATE_TEXT_SUMMARY_MESSAGE:TEXTMINING,
    messages.NEG_VAR_MESSAGE:GESTCONSOLE,
    messages.POS_VAR_MESSAGE:GESTCONSOLE,
    messages.NEW_USR_NOTIF_MESSAGE:GESTCONSOLE,
    messages.UPDATE_QUOTES_MESSAGE:RESCONTROL,
    messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:RESCONTROL,
    messages.NEW_DP_WIDGET_MESSAGE:GESTCONSOLE,
    messages.NEW_DS_WIDGET_MESSAGE:GESTCONSOLE,
    messages.DELETE_USER_MESSAGE:GESTCONSOLE,
    messages.DELETE_AGENT_MESSAGE:GESTCONSOLE,
    messages.DELETE_DATASOURCE_MESSAGE:GESTCONSOLE,
    messages.DELETE_DATAPOINT_MESSAGE:GESTCONSOLE,
    messages.DELETE_WIDGET_MESSAGE:GESTCONSOLE,
    messages.DELETE_DASHBOARD_MESSAGE:GESTCONSOLE,
    messages.USER_EVENT_MESSAGE:EVENTS,
    messages.USER_EVENT_RESPONSE_MESSAGE:EVENTS,
    messages.MISSING_DATAPOINT_MESSAGE:ANOMALIES,
    messages.NEW_INV_MAIL_MESSAGE:GESTCONSOLE,
    messages.FORGET_MAIL_MESSAGE:GESTCONSOLE,
    messages.URIS_UPDATED_MESSAGE:LAMBDAS,
    messages.CLEAR_SESSION_HOOKS_MESSAGE:LAMBDAS,
}


#MODULE MAPPINGS
MODULE_TO_ADDRESS_MAPPING={
    VALIDATION:['%m.%h','%i.%m.%h'],
    STORING:['%m.%h','%i.%m.%h'],
    TEXTMINING:['%m','%i.%m.%h'],
    GESTCONSOLE:['%m','%i.%m.%h'],
    RESCONTROL:['%m','%i.%m.%h'],
    EVENTS:['%m','%i.%m.%h'],
    ANOMALIES:['%m','%i.%m.%h'],
    WEBSOCKETSERVER: ['%i.%m.%h'],
    LAMBDAS:['%m','%i.%m.%h'],
}


def get_address(type, module_id, module_instance, running_host):
    if type in MESSAGE_TO_ADDRESS_MAPPING:
        address = MESSAGE_TO_ADDRESS_MAPPING[type]
        address = address.replace('%h',running_host)
        address = address.replace('%m',module_id)
        address = address.replace('%i',str(module_instance))
        address = '.'.join((BASE_IMC_ADDRESS,address))
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
            address = '.'.join((BASE_IMC_ADDRESS,address))
            address_list.append(address)
        return address_list
    else:
        return None

def get_imc_address(module_id, module_instance, running_host):
    local='.'.join((BASE_IMC_ADDRESS,module_id,str(module_instance)))
    remote=':'.join((running_host,local))
    return remote


