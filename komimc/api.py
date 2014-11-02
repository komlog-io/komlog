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

def retrieve_message(msgtype=None, mod_addr=True, timeout=0):
    s_message=msgbus.msgbus.retrieveMessage(msgtype, mod_addr, timeout)
    mtype = s_message.content.split('|')[0]
    logger.logger.debug('Message received of type: '+mtype)
    try:
        message=getattr(messages,messages.MESSAGE_TO_CLASS_MAPPING[mtype])(qpid_message=s_message)
        msgbus.msgbus.ackMessage()
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
            logger.logger.debug('Message Sent: '+msg.qpid_message.content)
    return True

