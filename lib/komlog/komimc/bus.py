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
        self.remotes={}

    async def start(self):
        try:
            self.local = await aioredis.create_redis(self.broker, encoding='utf-8')
            self.remotes[self.running_host]=self.local
        except Exception as e:
            logging.logger.error('Exception establishing connection with Redis Server: '+str(e))
            raise e

    async def stop(self):
        for host in self.remotes.keys():
            self.remotes[host].close()
        for host in self.remotes.keys():
            await self.remotes[host].wait_closed()
        return True

    async def send_message(self, komlog_message):
        try:
            addr=routing.get_address(komlog_message.type,self.module_id, self.module_instance, self.running_host)
            await self.local.rpush(addr,komlog_message.serialized_message.encode('utf-8'))
            return True
        except aioredis.RedisError:
            try:
                self.local = await aioredis.create_redis(self.broker,encoding='utf-8')
                self.remotes[self.running_host]=self.local
                await self.local.rpush(addr,komlog_message.serialized_message.encode('utf-8'))
            except aioredis.RedisError:
                #try on other running connections
                connections=[item[0] for item in list(self.remotes.items()) if item[0] != self.running_host]
                for host in connections:
                    try:
                        await self.remotes[host].rpush(addr,komlog_message.serialized_message.encode('utf-8'))
                    except aioredis.RedisError:
                        del self.remotes[host]
                    else:
                        return True
                return False
            else:
                return True
        except Exception as e:
            logging.logger.error('Exception sending message: '+str(e))
            return False

    async def retrieve_message(self, timeout):
        try:
            msg = await self.local.blpop(*self.addr_list, timeout=timeout)
            return msg
        except Exception as e:
            logging.logger.error('Exception retrieving message: '+str(e))
            return None

    async def send_message_to(self, remote_addr, komlog_message):
        try:
            host,addr=remote_addr.split(':')
            await self.remotes[host].rpush(addr,komlog_message.serialized_message.encode('utf-8'))
        except (KeyError, aioredis.RedisError):
            logging.logger.error('exception sending message to '+host+' addr: '+addr)
            try:
                self.remotes[host] = await aioredis.create_redis(host, encoding='utf-8')
                await self.remotes[host].rpush(addr,komlog_message.serialized_message.encode('utf-8'))
                logging.logger.error('Success in retry sending message to '+host+' addr: '+addr)
            except Exception:
                logging.logger.error('Error in retry sending message to '+host+' addr: '+addr)
                return False
        except Exception as e:
            logging.logger.error('Exception sending message: '+str(e))
            return False
        return True

    async def retrieve_message_from(self, addr, timeout=0):
        try:
            data = await self.local.blpop(addr,timeout=timeout)
            return data
        except Exception as e:
            logging.logger.error('Exception retrieving messages (timeout='+str(timeout)+') address_list: '+str(addr))
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
        if msgbus:
            loop.run_until_complete(msgbus.stop())
    except Exception as e:
        logging.logger.error('Exception stopping message bus: '+str(e))
        return False
    else:
        return True
    finally:
        msgbus=None

