'''
Created on 07/02/2013

komimc: komlog inter module communication

bus.py: Messages Bus implementation

@author: jcazor
'''

from qpid.messaging import Connection, MessagingError
import messages

class MessageBus:
    def __init__(self, broker, module_id, module_instance, running_host, logger):
        self.broker = broker
        self.module_id = module_id
        self.module_instance = module_instance
        self.running_host = running_host
        self.connection = Connection(self.broker)
        self.mod_address,self.mod_address_opts = messages.get_mod_address(module_id,module_instance,running_host)
        self.senders={}
        self.receivers={}
        self.logger = logger
        try:
            self.connection.open()
            self.session = self.connection.session()
            self.logger.debug('Session established with Message Broker: '+self.broker)
        except Exception as e:
            self.logger.debug('Exception establishing connection with Message Broker: '+str(e))
            self.connection.close() if self.connection else None
            raise e
    
    def sendMessage(self, komlog_message):
        try:
            addr,opts=messages.get_address(komlog_message.type,self.module_id, self.module_instance, self.running_host)
            if not self.senders.has_key(addr):
                if addr == None:
                    self.logger.error('Invalid send address: None')
                    return False 
                self.senders[addr]=self.session.sender(addr+opts)
            self.senders[addr].send(komlog_message.qpid_message)
            self.logger.debug('Message sent of type :'+komlog_message.type)
        except MessagingError as e:
            self.logger.exception('Exception sending message: '+str(e))
            return False
        return True
    
    def retrieveMessage(self, message_type=None, from_modaddr=False, timeout=0):
        if from_modaddr==False:
            addr,opts=messages.get_address(message_type,self.module_id, self.module_instance, self.running_host)
        else:
            addr,opts=self.mod_address,self.mod_address_opts
        try:
            if not self.receivers.has_key(addr):
                if addr == None:
                    self.logger.error('Invalid retrieve address: None')
                    return None
                self.receivers[addr]=self.session.receiver(addr+opts)
            if timeout == 0:
                message = self.receivers[addr].fetch()
            else:
                message = self.receivers[addr].fetch(timeout)
            mtype = message.content.split('|')[0]
            self.logger.debug('Message received of type: '+mtype)
            return getattr(messages,messages.MESSAGE_TO_CLASS_MAPPING[mtype])(qpid_message=message)
        except MessagingError as e:
            self.logger.exception('Exception retrieving message: '+str(e))
            return None
        except AttributeError as e:
            self.logger.exception('Cannot map message.type to message Class: '+str(e))
            return None
    
    def ackMessage(self):
        try:
            self.session.acknowledge()
        except Exception:
            self.logger.exception('Error acknowledging message')
        
