#coding: utf-8

from datetime import datetime
from komcass import connection as casscon
from komapp import modules
from komfig import config,logger, options
from komimc import bus as msgbus
from komimc import api as msgapi
from komlibs.mail import connection as mailcon
from komlibs import messages

class Gestconsole(modules.Module):
    def __init__(self, instance_number):
        super(Gestconsole,self).__init__(self.__class__.__name__, instance_number)

    def start(self):
        if not logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            exit()
        logger.logger.info('Module started')
        if not casscon.initialize_session():
            logger.logger.error('Error initializing cassandra session')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logger.logger.error('Error initializing broker session')
            exit()
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

