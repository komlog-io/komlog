'''
Created on 07/02/2013

komimc: komlog inter module communication

bus.py: Messages Bus implementation

@author: jcazor
'''

import asyncio
import aioredis
import os.path
from komlog.komfig import logging, config, options
from komlog.komimc import routing

loop = asyncio.get_event_loop()
msgbus=None

class MessageBus:
    def __init__(self, broker, module_id, module_instance, running_host):
        self.broker = broker
        self.module_id = module_id
        self.module_instance = module_instance
        self.running_host = running_host
        self.imc_address = routing.get_imc_address(module_id, module_instance, running_host)
        self.addr_list = routing.get_mod_address(module_id,module_instance,running_host)
        self.local=None

    async def start(self):
        try:
            self.local = await aioredis.create_redis(self.broker, encoding='utf-8')
        except Exception as e:
            logging.logger.debug('Exception establishing connection with Redis Server: '+str(e))
            raise e

    def retrieve_message(self, timeout):
        msg = loop.run_until_complete(self.local.blpop(self.addr_list, timeout=1))
        return msg

    def send_message(self, komlog_message):
        try:
            addr=routing.get_address(komlog_message.type,self.module_id, self.module_instance, self.running_host)
            if addr:
                loop.run_until_complete(self.local.rpush(addr,komlog_message.serialized_message.encode('utf-8')))
                return True
            else:
                logging.logger.error('Could not determine message destination address: '+komlog_message.type)
                return False
        except Exception as e:
            logging.logger.exception('Exception sending message: '+str(e))
            return False

    async def stop(self):
        if self.local:
            await self.local.close()
        return True

    def send_message_to(self, addr, komlog_message):
        try:
            loop.run_until_complete(self.local.rpush(addr,komlog_message.serialized_message.encode('utf-8')))
        except Exception as e:
            logging.logger.exception('Exception sending message: '+str(e))
            return False
        return True

    def retrieve_message_from(self, addr, timeout=0):
        try:
            data = loop.run_until_complete(self.local.blpop(addr,timeout=timeout))
            return data
        except Exception as e:
            logging.logger.debug('Exception retrieving messages (timeout='+str(timeout)+') address_list: '+str(addr))
            logging.logger.exception('Exception retrieveing message: '+str(e))
            return None

def initialize_msgbus(module_name, module_instance, hostname):
    global msgbus
    broker = config.get(options.MESSAGE_BROKER)
    if not broker:
        return False
    msgbus=MessageBus(broker, module_name, module_instance, hostname)
    if msgbus:
        try:
            loop.run_until_complete(msgbus.start())
        except Exception as e:
            logging.logger.error('Exception initializing message bus: '+str(e))
            return False
        else:
            return True
    else:
        return False

def terminate_msgbus():
    global msgbus
    try:
        loop.run_until_complete(msgbus.stop())
    except Exception as e:
        logging.logger.error('Exception stopping message bus: '+str(e))
        return False
    else:
        return True
    finally:
        msgbus=None

