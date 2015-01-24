#coding: utf-8
'''

messages api

02/11/2014

'''

from komfig import logger
from komimc import bus as msgbus
from komlibs.interface.imc import api as imcapi
from komlibs.interface.imc import status
from komlibs.interface.imc.model import messages


def send_message(msg):
    if msgbus.msgbus.sendMessage(msg):
        return True
    else:
        return False

def retrieve_message(timeout=0):
    data=msgbus.msgbus.retrieveMessage(timeout)
    if data:
        addr, s_message = data
        mtype = s_message.split('|')[0]
        try:
            message=getattr(messages,messages.MESSAGE_TO_CLASS_MAPPING[mtype])(serialized_message=s_message)
            return message
        except Exception as e:
            logger.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    else:
        logger.logger.debug('Timeout expired waiting for messages')
        return None

def process_message(message):
    return imcapi.process_message(message=message)

def process_msg_result(msg_result):
    if msg_result.status==status.IMC_STATUS_INTERNAL_ERROR:
        logger.logger.error('Error processing message: '+msg_result.message_params)
    for msg in msg_result.get_msg_originated():
        send_message(msg)
    return True

def send_message_to(addr, msg):
    if msgbus.msgbus.send_message_to(addr, msg):
        return True
    else:
        return False

def retrieve_message_from(addr, timeout=0):
    data=msgbus.msgbus.retrieve_message_from(addr=addr, timeout=timeout)
    if data:
        addr, s_message = data
        mtype = s_message.split('|')[0]
        try:
            message=getattr(messages,messages.MESSAGE_TO_CLASS_MAPPING[mtype])(serialized_message=s_message)
            return message
        except Exception as e:
            logger.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    else:
        logger.logger.debug('Timeout expired waiting for messages')
        return None
