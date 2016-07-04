#coding: utf-8
'''

messages api

02/11/2014

'''

import asyncio
from komlog.komfig import logging
from komlog.komimc import bus as msgbus
from komlog.komlibs.interface.imc import api as imcapi
from komlog.komlibs.interface.imc import status
from komlog.komlibs.interface.imc.model import messages


loop = asyncio.get_event_loop()

def send_message(msg):
    return loop.run_until_complete(msgbus.msgbus.send_message(msg))

def retrieve_message(timeout=0):
    data=loop.run_until_complete(msgbus.msgbus.retrieve_message(timeout))
    if data:
        addr, s_message = data
        mtype = s_message.split('|')[0]
        try:
            message=messages.MESSAGE_TO_CLASS_MAPPING[mtype](serialized_message=s_message)
            return message
        except Exception as e:
            logging.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    else:
        return None

def send_message_to(addr, msg):
    return loop.run_until_complete(msgbus.msgbus.send_message_to(addr, msg))

def retrieve_message_from(addr, timeout=0):
    data=loop.run_until_complete(msgbus.msgbus.retrieve_message_from(addr=addr, timeout=timeout))
    if data:
        addr, s_message = data
        mtype = s_message.split('|')[0]
        try:
            message=messages.MESSAGE_TO_CLASS_MAPPING[mtype](serialized_message=s_message)
            return message
        except Exception as e:
            logging.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    else:
        return None

def process_message(message):
    return imcapi.process_message(message=message)

async def send_response_messages(response):
    for addr,msgs in response.routed_messages.items():
        for msg in msgs:
            await msgbus.msgbus.send_message_to(addr, msg)
    for msg in response.unrouted_messages:
        await msgbus.msgbus.send_message(msg)
    return True

async def async_send_message(msg):
    return await msgbus.msgbus.send_message(msg)

async def async_retrieve_message(timeout=0):
    data=await msgbus.msgbus.retrieve_message(timeout)
    if data:
        addr, s_message = data
        mtype = s_message.split('|')[0]
        try:
            message=messages.MESSAGE_TO_CLASS_MAPPING[mtype](serialized_message=s_message)
            return message
        except Exception as e:
            logging.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    else:
        return None

async def async_send_message_to(addr, msg):
    return await msgbus.msgbus.send_message_to(addr, msg)

async def async_retrieve_message_from(addr, timeout=0):
    data=await msgbus.msgbus.retrieve_message_from(addr=addr, timeout=timeout)
    if data:
        addr, s_message = data
        mtype = s_message.split('|')[0]
        try:
            message=messages.MESSAGE_TO_CLASS_MAPPING[mtype](serialized_message=s_message)
            return message
        except Exception as e:
            logging.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    else:
        return None

