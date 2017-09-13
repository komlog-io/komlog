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
TEXTMINING='Textmining'
GESTCONSOLE='Gestconsole'
RESCONTROL='Rescontrol'
EVENTS='Events'
ANOMALIES='Anomalies'
WEBSOCKETSERVER='Websocketserver'
LAMBDAS='Lambdas'


MESSAGE_TO_ADDRESS_MAPPING={
    messages.Messages.MAP_VARS_MESSAGE:TEXTMINING,
    messages.Messages.MON_VAR_MESSAGE:GESTCONSOLE,
    messages.Messages.GDTREE_MESSAGE:TEXTMINING,
    messages.Messages.FILL_DATAPOINT_MESSAGE:TEXTMINING,
    messages.Messages.FILL_DATASOURCE_MESSAGE:TEXTMINING,
    messages.Messages.GENERATE_TEXT_SUMMARY_MESSAGE:TEXTMINING,
    messages.Messages.NEG_VAR_MESSAGE:GESTCONSOLE,
    messages.Messages.POS_VAR_MESSAGE:GESTCONSOLE,
    messages.Messages.NEW_USR_NOTIF_MESSAGE:GESTCONSOLE,
    messages.Messages.UPDATE_QUOTES_MESSAGE:RESCONTROL,
    messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE:RESCONTROL,
    messages.Messages.NEW_DP_WIDGET_MESSAGE:GESTCONSOLE,
    messages.Messages.NEW_DS_WIDGET_MESSAGE:GESTCONSOLE,
    messages.Messages.DELETE_USER_MESSAGE:GESTCONSOLE,
    messages.Messages.DELETE_AGENT_MESSAGE:GESTCONSOLE,
    messages.Messages.DELETE_DATASOURCE_MESSAGE:GESTCONSOLE,
    messages.Messages.DELETE_DATAPOINT_MESSAGE:GESTCONSOLE,
    messages.Messages.DELETE_WIDGET_MESSAGE:GESTCONSOLE,
    messages.Messages.DELETE_DASHBOARD_MESSAGE:GESTCONSOLE,
    messages.Messages.USER_EVENT_MESSAGE:EVENTS,
    messages.Messages.USER_EVENT_RESPONSE_MESSAGE:EVENTS,
    messages.Messages.MISSING_DATAPOINT_MESSAGE:ANOMALIES,
    messages.Messages.NEW_INV_MAIL_MESSAGE:GESTCONSOLE,
    messages.Messages.FORGET_MAIL_MESSAGE:GESTCONSOLE,
    messages.Messages.URIS_UPDATED_MESSAGE:LAMBDAS,
    messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE:LAMBDAS,
    messages.Messages.HOOK_NEW_URIS_MESSAGE:LAMBDAS,
    messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE:LAMBDAS,
    messages.Messages.ANALYZE_DTREE_MESSAGE:TEXTMINING,
    messages.Messages.IDENTIFY_NEW_DATAPOINTS_MESSAGE:TEXTMINING,
    messages.Messages.UPDATE_DATAPOINT_FEATURES_MESSAGE:TEXTMINING,
    messages.Messages.UPDATE_DATASOURCE_FEATURES_MESSAGE:TEXTMINING,
    messages.Messages.CLASSIFY_SAMPLE_MESSAGE:TEXTMINING,
    messages.Messages.IDENTIFY_SUPPLIES_MESSAGE:TEXTMINING,
}


#MODULE MAPPINGS
MODULE_TO_ADDRESS_MAPPING={
    TEXTMINING:['%m','%m.%i'],
    GESTCONSOLE:['%m','%m.%i'],
    RESCONTROL:['%m','%m.%i'],
    EVENTS:['%m','%m.%i'],
    ANOMALIES:['%m','%m.%i'],
    WEBSOCKETSERVER: ['%m.%i'],
    LAMBDAS:['%m','%m.%i'],
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


