#coding: utf-8
'''

messages api

02/11/2014

'''

from komimc import bus as msgbus
from komimc import codes as msgcodes
from komimc import messages
from komfig import logger

def send_message(msg):
    if msgbus.msgbus.sendMessage(msg):
        return True
    else:
        return False

def retrieve_message(timeout=0):
    addr,s_message=msgbus.msgbus.retrieveMessage(timeout)
    logger.logger.debug('Message received: '+str(s_message))
    mtype = s_message.split('|')[0]
    logger.logger.debug('Message received of type: '+mtype)
    try:
        message=getattr(messages,messages.MESSAGE_TO_CLASS_MAPPING[mtype])(serialized_message=s_message)
        return message
    except Exception as e:
        logger.logger.exception('Cannot map message.typ to message Class: '+str(e))
        return None

def process_msg_result(msg_result):
    if msg_result.retcode==msgcodes.ERROR:
        logger.logger.error('Error processing message: '+msg_result.mparams)
    elif msg_result.retcode==msgcodes.SUCCESS:
        logger.logger.debug('Message processed successfully: '+msg_result.mparams)
    for msg in msg_result.get_msg_originated():
        if send_message(msg):
            logger.logger.debug('Message Sent: '+msg.serialized_message)
    return True

