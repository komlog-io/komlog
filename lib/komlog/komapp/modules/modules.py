'''
Created on 31/12/2012

@author: jcazor
'''

import socket
import signal
import asyncio
import functools
import traceback
from komlog.komfig import logging
from komlog.komcass import connection as casscon
from komlog.komimc import api as msgapi
from komlog.komimc import bus as msgbus
from komlog.komlibs.mail import connection as mailcon
from komlog.komlibs.payment import api as paymentapi

loop = asyncio.get_event_loop()

class Module(object):
    def __init__(self, name, instance, needs_db=False, needs_msgbus=False, needs_mailer=False, needs_payment=False, tasks=[]):
        self.needs_db=needs_db
        self.needs_msgbus=needs_msgbus
        self.needs_mailer=needs_mailer
        self.needs_payment=needs_payment
        self.name = name
        self.instance = instance
        self.hostname = socket.gethostname()
        self.tasks=tasks
        self._my_tasks = []

    def start(self):
        logging.logger.info('Module started')
        if self.needs_db:
            if not casscon.initialize_session():
                logging.logger.error('Error initializing cassandra session')
                exit()
        if self.needs_msgbus:
            if not msgbus.initialize_msgbus(self.name, self.instance, self.hostname):
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
            self._my_tasks.append(loop.create_task(task()))
        self.loop()
        self.terminate()

    def stop(self):
        for task in self.tasks:
            self._my_tasks.append(loop.create_task(task(start=False)))
        deadline = loop.time() + 10
        def stop_loop():
            now = loop.time()
            logging.logger.info('waiting for loop finishing requests')
            for task in self._my_tasks:
                if not task.done():
                    logging.logger.info('Pending tasks exists, waiting... ')
                    break
            else:
                logging.logger.info('Stopping loop')
                loop.stop()
                return
            if now < deadline:
                loop.call_later(1, stop_loop)
            else:
                logging.logger.info('Timeout expired waiting for tasks to finish.. forcing it')
                loop.stop()
        stop_loop()

    def loop(self):
        try:
            loop.run_forever()
        except:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
        self.terminate()

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
        logging.logger.info('Module '+str(self.name)+'-'+str(self.instance)+' exiting')
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
                            logging.logger.error('msgresult is None: '+message.type.value)
                    except AttributeError:
                        logging.logger.exception('Exception processing message: '+message.type.value)
                    except Exception as e:
                        logging.logger.exception('Exception processing message: '+str(e))
            logging.logger.info('Exiting messages listener loop')
        else:
            self.run = False

