#coding:utf-8
import signal
import time
from komlog.test import test
from komlog.komfig import logger, config, options
from komlog.komapp.modules import modules
from komlog.komcass import connection as casscon
from komlog.komcass.model.schema import creation
from komlog.komimc import bus as msgbus
from komlog.komlibs.mail import connection as mailcon


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
                try:
                    logger.logger.debug('Sending tests report')
                    test.send_report(results, logfile=True)
                except Exception as e:
                    logger.logger.debug('Exception sending tests report: '+str(e))
                self.run=False
            else:
                self.run=False

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

