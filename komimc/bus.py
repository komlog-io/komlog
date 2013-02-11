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
            if not self.senders.has_key(komlog_message.type):
                self.senders[komlog_message.type]=self.session.sender(messages.get_address(type,self.module_id, self.module_instance, self.running_host))
            self.senders[komlog_message.type].send(komlog_message.qpid_message)
            self.logger.debug('Message sent of type :'+komlog_message.type)
        except MessagingError as e:
            self.logger.exception('Exception sending message: '+str(e))
            return False
        return True
    
    def retrieveMessage(self, message_type, timeout=0):
        try:
            if not self.receivers.has_key(message_type):
                self.receivers[type]=self.session.receiver(messages.get_address(message_type,self.module_id, self.module_instance, self.running_host))
            message = self.receivers[message_type].fetch(timeout)
            self.logger.debug('Message received of type :'+message_type)
            return getattr(messages,messages.MESSAGE_TO_CLASS_MAPPING[message_type])(qpid_message=message)
        except MessagingError as e:
            self.logger.exception('Exception retrieving message: '+str(e))
            return None 
        except AttributeError as e:
            self.logger.exception('Cannot map message_type to message_class: '+str(e))
            return None
        
        
        
            
        
            
            
            
        