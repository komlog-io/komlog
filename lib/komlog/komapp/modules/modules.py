'''
Created on 31/12/2012

@author: jcazor
'''

import socket
import signal
import asyncio
import functools
from komlog.komfig import logging
from komlog.komcass import connection as casscon
from komlog.komimc import api as msgapi
from komlog.komimc import bus as msgbus
from komlog.komlibs.mail import connection as mailcon
from komlog.komlibs.payment import api as paymentapi

loop = asyncio.get_event_loop()

class Module(object):
    def __init__(self, name, instance_number, needs_db=False, needs_msgbus=False, needs_mailer=False, needs_payment=False, tasks=[]):
        self.needs_db=needs_db
        self.needs_msgbus=needs_msgbus
        self.needs_mailer=needs_mailer
        self.needs_payment=needs_payment
        self.name = name
        self.instance_number = instance_number
        self.hostname = socket.gethostname()
        self.tasks=tasks

    def signal_handler(self, signum):
        if signum == signal.SIGTERM:
            logging.logger.info('SIGTERM received, terminating')
            self.shutdown()
        elif signum == signal.SIGINT:
            logging.logger.info('SIGINT received, terminating')
            self.shutdown()
        else:
            logging.logger.info('signal '+str(signum)+' received, ignoring')

    def start(self):
        loop.add_signal_handler(signal.SIGTERM,
            functools.partial(self.signal_handler, signal.SIGTERM))
        loop.add_signal_handler(signal.SIGINT,
            functools.partial(self.signal_handler, signal.SIGINT))
        if not logging.initialize_logging(self.name+'_'+str(self.instance_number)):
            exit()
        logging.logger.info('Module started')
        if self.needs_db:
            if not casscon.initialize_session():
                logging.logger.error('Error initializing cassandra session')
                exit()
        if self.needs_msgbus:
            if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
                logging.logger.error('Error initializing broker session')
                exit()
        if self.needs_mailer:
            if not mailcon.initialize_mailer():
                logging.logger.error('Error initializing mailer')
        if self.needs_payment:
            if not paymentapi.initialize_payment():
                logging.logger.error('Error initializing payment')
                exit()
        for task in self.tasks:
            loop.create_task(task())
        self.loop()
        self.terminate()
    
    def loop(self):
        try:
            loop.run_forever()
        except:
           pass

    def shutdown(self):
        for task in self.tasks:
            loop.create_task(task(start=False))
        deadline = loop.time() + 10
        def stop_loop():
            now = loop.time()
            logging.logger.info('waiting for loop finishing requests')
            if now < deadline and len(asyncio.Task.all_tasks())>0:
                logging.logger.info('No paramos porque existen estas tareas: '+str(asyncio.Task.all_tasks()))
                loop.call_later(1, stop_loop)
            elif len(asyncio.Task.all_tasks())==0:
                loop.stop()
                logging.logger.info('loop stopped')
            elif now > deadline:
                logging.logger.info('Timeout expired waiting for loop shutdown, forcing it')
                loop.stop()
                logging.logger.info('loop stopped')
        stop_loop()

    def terminate(self):
        if self.needs_db:
            logging.logger.info('Closing database connection')
            casscon.terminate_session()
        if self.needs_msgbus:
            logging.logger.info('Closing message bus connection')
            msgbus.terminate_msgbus()
        if self.needs_mailer: 
            logging.logger.info('Closing mailer connection')
            mailcon.terminate_mailer()
        if self.needs_payment:
            logging.logger.info('Closing mailer connection')
            paymentapi.disable_payment()
        logging.logger.info('Module '+str(self.name)+'-'+str(self.instance_number)+' exiting')
        loop.close()

    async def _messages_listener(self, start=True):
        if start:
            self.run = True
            while self.run:
                message = await msgapi.async_retrieve_message(5)
                if message:
                    try:
                        response=msgapi.process_message(message)
                        if response:
                            await msgapi.send_response_messages(response)
                        else:
                            logging.logger.error('msgresult is None: '+message.type)
                    except AttributeError:
                        logging.logger.exception('Exception processing message: '+message.type)
                    except Exception as e:
                        logging.logger.exception('Exception processing message: '+str(e))
            logging.logger.exception('Exiting messages listener loop')
        else:
            self.run = False

