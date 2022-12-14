import signal
import time
from komlog.test import test
from komlog.komfig import logging, config, options
from komlog.komapp.modules import modules
from komlog.komcass import connection as casscon
from komlog.komcass.model.schema import creation
from komlog.komimc import bus as msgbus
from komlog.komlibs.mail import connection as mailcon
from komlog.komlibs.payment import api as paymentapi


class Tester(modules.Module):
    def __init__(self, instance):
        super().__init__(
            name=self.__class__.__name__,
            instance=instance,
            needs_db=True,
            needs_msgbus=True,
            needs_mailer=True,
            needs_payment=True
        )

    def signal_handler(self, signum, frame):
        if signum == signal.SIGTERM:
            logging.logger.info('SIGTERM received, terminating')
            self.run = False
        else:
            logging.logger.info('signal '+str(signum)+' received, ignoring')

    def start(self):
        signal.signal(signal.SIGTERM,self.signal_handler)
        if not logging.initialize_logging(self.name+'_'+str(self.instance)):
            exit()
        logging.logger.info('Module started')
        keyspace = config.get(options.CASSANDRA_KEYSPACE)
        cluster = config.get(options.CASSANDRA_CLUSTER)
        cluster = list(host for host in cluster.split(',') if len(host)>0) if cluster else None
        if not keyspace or not cluster:
            logging.logger.error('Cassandra parameters not found. Cluster: '+str(cluster)+' keyspace: '+str(keyspace))
            exit()
        if not creation.create_database(cluster,keyspace):
            logging.logger.error('Error creation cassandra database, maybe it already exists. For security reasons, komtest does not work on already existing databases.')
            exit()
        if not casscon.initialize_session():
            logging.logger.error('Error initializing cassandra session')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance, self.hostname):
            logging.logger.error('Error initializing broker session')
            exit()
        if not mailcon.initialize_mailer():
            logging.logger.error('Error initializing mailer')
            exit()
        if not paymentapi.initialize_payment():
            logging.logger.error('Error initializing payment')
            exit()
        self.loop()
        self.terminate()

    def loop(self):
        self.run = True
        while self.run:
            results=test.run_tests()
            if results:
                try:
                    logging.logger.debug('Sending tests report')
                    test.send_report(results, logfile=True)
                except Exception as e:
                    logging.logger.debug('Exception sending tests report: '+str(e))
                self.run=False
            else:
                self.run=False

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
            logging.logger.info('Disabling payment')
            paymentapi.disable_payment()
        keyspace = config.get(options.CASSANDRA_KEYSPACE)
        cluster = config.get(options.CASSANDRA_CLUSTER)
        cluster = list(host for host in cluster.split(',') if len(host)>0) if cluster else None
        if not keyspace or not cluster:
            pass
        else:
            creation.drop_database(cluster, keyspace)
        logging.logger.info('Module '+str(self.name)+'-'+str(self.instance)+' exiting')

def get_module(instance):
    mod = Tester(instance=instance)
    return mod

