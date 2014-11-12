'''
Created on 07/02/2013

komimc: komlog inter module communication

bus.py: Messages Bus implementation

@author: jcazor
'''

import redis
from komfig import config, logger, options
from komimc import routing

msgbus=None

class MessageBus:
    def __init__(self, broker, module_id, module_instance, running_host):
        self.broker = broker
        self.module_id = module_id
        self.module_instance = module_instance
        self.running_host = running_host
        self.addr_list = routing.get_mod_address(module_id,module_instance,running_host)
        try:
            self.connection = redis.StrictRedis(host=self.broker)
            logger.logger.debug('Session established with Redis Server: '+self.broker)
        except Exception as e:
            logger.logger.debug('Exception establishing connection with Redis Server: '+str(e))
            raise e
    
    def sendMessage(self, komlog_message):
        try:
            addr=routing.get_address(komlog_message.type,self.module_id, self.module_instance, self.running_host)
            if addr:
                logger.logger.debug('Sending message '+komlog_message.serialized_message+' to '+addr)
                self.connection.rpush(addr,komlog_message.serialized_message.encode('utf-8'))
            else:
                logger.logger.error('Could not determine message destination address: '+komlog_message.type)
                return False
        except Exception as e:
            logger.logger.exception('Exception sending message: '+str(e))
            return False
        logger.logger.debug('Message sent of type :'+komlog_message.type)
        return True
    
    def retrieveMessage(self, timeout=0):
        try:
            logger.logger.debug('Waiting for messages (timeout='+str(timeout)+') address_list: '+str(self.addr_list))
            data = self.connection.blpop(self.addr_list,timeout)
            if data:
                return data[0],data[1].decode('utf-8')
            else:
                return None
        except Exception as e:
            logger.logger.exception('Exception retrieveing message: '+str(e))
            return None
    
def initialize_msgbus(module_name, module_instance, hostname):
    global msgbus
    broker = config.get(options.MESSAGE_BROKER)
    if not broker:
        return False
    msgbus=MessageBus(broker, module_name, module_instance, hostname)
    if msgbus:
        return True
    else:
        return False

def terminate_msgbus():
    global msgbus
    if msgbus:
        msgbus=None

