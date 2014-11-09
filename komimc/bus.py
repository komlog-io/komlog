'''
Created on 07/02/2013

komimc: komlog inter module communication

bus.py: Messages Bus implementation

@author: jcazor
'''

from qpid.messaging import Connection, MessagingError
from komfig import config, logger, options
from komimc import routing

QPID_OPTS='; {create:always}'

msgbus=None

class MessageBus:
    def __init__(self, broker, module_id, module_instance, running_host):
        self.broker = broker
        self.module_id = module_id
        self.module_instance = module_instance
        self.running_host = running_host
        self.connection = Connection(self.broker)
        self.mod_address = routing.get_mod_address(module_id,module_instance,running_host)
        self.senders={}
        self.receivers={}
        try:
            self.connection.open()
            self.session = self.connection.session()
            logger.logger.debug('Session established with Message Broker: '+self.broker)
        except Exception as e:
            logger.logger.debug('Exception establishing connection with Message Broker: '+str(e))
            self.connection.close() if self.connection else None
            raise e
    
    def sendMessage(self, komlog_message):
        try:
            addr=routing.get_address(komlog_message.type,self.module_id, self.module_instance, self.running_host)
            if not self.senders.has_key(addr):
                if addr == None:
                    logger.logger.error('Invalid send address: None')
                    return False 
                self.senders[addr]=self.session.sender(addr+QPID_OPTS)
            self.senders[addr].send(komlog_message.qpid_message)
            logger.logger.debug('Message sent of type :'+komlog_message.type)
        except MessagingError as e:
            logger.logger.exception('Exception sending message: '+str(e))
            return False
        return True
    
    def retrieveMessage(self, message_type, from_modaddr, timeout):
        if from_modaddr==False:
            addr=routing.get_address(message_type,self.module_id, self.module_instance, self.running_host)
        else:
            addr=self.mod_address
        try:
            if not self.receivers.has_key(addr):
                if addr == None:
                    logger.logger.error('Invalid retrieve address: None')
                    return None
                logger.logger.debug('Opening session on address: '+addr)
                self.receivers[addr]=self.session.receiver(addr+QPID_OPTS)
            logger.logger.debug('Waiting for messages (timeout='+str(timeout)+')')
            if timeout == 0:
                message = self.receivers[addr].fetch()
            else:
                message = self.receivers[addr].fetch(timeout)
            return message
        except MessagingError as e:
            logger.logger.exception('Exception retrieving message: '+str(e))
            return None
        except AttributeError as e:
            logger.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    
    def ackMessage(self):
        try:
            self.session.acknowledge()
        except Exception:
            logger.logger.exception('Error acknowledging message')

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

