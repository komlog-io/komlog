'''
Created on 31/12/2012

@author: jcazor
'''

import socket
from komfig import logger
from komcass import connection as casscon
from komimc import api as msgapi
from komimc import bus as msgbus
from komlibs import messages
from komlibs.mail import connection as mailcon

class Module(object):
    def __init__(self, name, instance_number, needs_db=False, needs_msgbus=False, needs_mailer=False):
        self.needs_db=needs_db
        self.needs_msgbus=needs_msgbus
        self.needs_mailer=needs_mailer
        self.name = name
        self.instance_number = instance_number
        self.hostname = socket.gethostname()

    def start(self):
        if not logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            exit()
        logger.logger.info('Module started')
        if self.needs_db:
            if not casscon.initialize_session():
                logger.logger.error('Error initializing cassandra session')
                exit()
        if self.needs_msgbus:
            if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
                logger.logger.error('Error initializing broker session')
                exit()
        if self.needs_mailer:
            if not mailcon.initialize_mailer():
                logger.logger.error('Error initializing mailer')
        self.__loop()
        logger.logger.info('Module exiting')
    
    def __loop(self):
        while True:
            message = msgapi.retrieve_message()
            try:
                msgresult=messages.process_message(message)
                if msgresult:
                    msgapi.process_msg_result(msgresult)
                else:
                    logger.logger.error('msgresult is None: '+message.type)
            except AttributeError:
                logger.logger.exception('Exception processing message: '+message.type)
            except Exception as e:
                logger.logger.exception('Exception processing message: '+str(e))

