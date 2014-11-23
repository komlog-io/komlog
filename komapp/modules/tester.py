#coding:utf-8
import signal
import time
from test import test
from komfig import logger, config, options
from komapp.modules import modules
from komcass import connection as casscon
from komcass.model.schema import creation
from komimc import bus as msgbus
from komlibs.mail import connection as mailcon


class Tester(modules.Module):
    def __init__(self, instance_number):
        super(Tester,self).__init__(name=self.__class__.__name__, instance_number=instance_number, needs_db=True, needs_msgbus=True, needs_mailer=True)

    def start(self):
        signal.signal(signal.SIGTERM,self.signal_handler)
        if not logger.initialize_logger(self.name+'_'+str(self.instance_number)):
            exit()
        logger.logger.info('Module started')
        keyspace = config.get(options.CASSANDRA_KEYSPACE)
        cluster = config.get(options.CASSANDRA_CLUSTER)
        cluster = list(host for host in cluster.split(',') if len(host)>0) if cluster else None
        if not keyspace or not cluster:
            logger.logger.error('Cassandra parameters not found. Cluster: '+str(cluster)+' keyspace: '+str(keyspace))
            exit()
        if not creation.create_database(cluster,keyspace):
            logger.logger.error('Error creation cassandra database, maybe it already exists. For security reasons, komtest does not work on already existing databases.')
            exit()
        if not casscon.initialize_session():
            logger.logger.error('Error initializing cassandra session')
            exit()
        if not msgbus.initialize_msgbus(self.name, self.instance_number, self.hostname):
            logger.logger.error('Error initializing broker session')
            exit()
        if not mailcon.initialize_mailer():
            logger.logger.error('Error initializing mailer')
            exit()
        self.loop()
        self.terminate()

    def loop(self):
        while self.run:
            results=test.run_tests()
            if results:
                logger.logger.debug('Now, send mail with results, if configured')
                self.run=False
            else:
                time.sleep(10)

    def terminate(self):
        if self.needs_db:
            logger.logger.info('Closing database connection')
            casscon.terminate_session()
        if self.needs_msgbus:
            logger.logger.info('Closing message bus connection')
            msgbus.terminate_msgbus()
        if self.needs_mailer: 
            logger.logger.info('Closing mailer connection')
            mailcon.terminate_mailer()
        keyspace = config.get(options.CASSANDRA_KEYSPACE)
        cluster = config.get(options.CASSANDRA_CLUSTER)
        cluster = list(host for host in cluster.split(',') if len(host)>0) if cluster else None
        if not keyspace or not cluster:
            pass
        else:
            creation.drop_database(cluster, keyspace)
        logger.logger.info('Module '+str(self.name)+'-'+str(self.instance_number)+' exiting')

