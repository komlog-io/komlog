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
from komlog.komlibs.interface.imc import exceptions as imcexcept


loop = asyncio.get_event_loop()

def send_message(msg):
    return loop.run_until_complete(msgbus.msgbus.send_message(msg))

def retrieve_message(timeout=0):
    data=loop.run_until_complete(msgbus.msgbus.retrieve_message(timeout))
    if data:
        addr, s_message = data
        try:
            msg = messages.IMCMessage.load_from_serialization(s_message)
            return msg
        except imcexcept.BadParametersException as e:
            logging.logger.error('Error loading IMCMessage: '+e.error.name)
            return None
    else:
        return None

def send_message_to(addr, msg):
    return loop.run_until_complete(msgbus.msgbus.send_message_to(addr, msg))

def retrieve_message_from(addr, timeout=0):
    data=loop.run_until_complete(msgbus.msgbus.retrieve_message_from(addr=addr, timeout=timeout))
    if data:
        addr, s_message = data
        try:
            msg = messages.IMCMessage.load_from_serialization(s_message)
            return msg
        except imcexcept.BadParametersException as e:
            logging.logger.error('Error loading IMCMessage: '+e.error.name)
            return None
    else:
        return None

def process_message(message):
    return imcapi.process_message(message=message)

async def async_send_message(msg):
    return await msgbus.msgbus.send_message(msg)

async def async_retrieve_message(timeout=0):
    data=await msgbus.msgbus.retrieve_message(timeout)
    if data:
        addr, s_message = data
        try:
            msg = messages.IMCMessage.load_from_serialization(s_message)
            return msg
        except imcexcept.BadParametersException as e:
            logging.logger.error('Error loading IMCMessage: '+e.error.name)
            logging.logger.error('message: '+str(s_message))
            return None
    else:
        return None

async def async_send_message_to(addr, msg):
    return await msgbus.msgbus.send_message_to(addr, msg)

async def async_retrieve_message_from(addr, timeout=0):
    data=await msgbus.msgbus.retrieve_message_from(addr=addr, timeout=timeout)
    if data:
        addr, s_message = data
        try:
            msg = messages.IMCMessage.load_from_serialization(s_message)
            return msg
        except imcexcept.BadParametersException as e:
            logging.logger.error('Error loading IMCMessage: '+e.error.name)
            return None
    else:
        return None

async def send_messages(messages):
    for addr,msgs in messages['routed'].items():
        for msg in msgs:
            logging.logger.debug('Sending message to redis server: '+msg._type_.value)
            await msgbus.msgbus.send_message_to(addr, msg)
    for msg in messages['unrouted']:
        logging.logger.debug('Sending message to redis server: '+msg._type_.value)
        await msgbus.msgbus.send_message(msg)
    return True

