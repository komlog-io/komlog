'''
Created on 01/10/2014

@author: komlog crew
'''

from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from komlog.komcass.model import statement
from komlog.komfig import logging, config, options

session = None

class Session:
    def __init__(self, cluster, keyspace=None):
        self.cluster = Cluster(cluster)
        self.session = self.cluster.connect(keyspace)
        self.session.row_factory = dict_factory
        self.stmts={}

    def execute(self,stmt,parameters):
        try:
            row = self.session.execute(self.stmts[stmt],parameters)
            return row
        except KeyError:
            self.stmts[stmt]=self.session.prepare(statement.get_statement(stmt))
            row = self.execute(stmt,parameters)
            return row
        except Exception as e:
            logging.logger.exception('Exception in cassandra session: '+str(e))
            return None

def initialize_session():
    global session
    keyspace = config.get(options.CASSANDRA_KEYSPACE)
    cluster = config.get(options.CASSANDRA_CLUSTER)
    cluster = list(host for host in cluster.split(',') if len(host)>0) if cluster else None
    if cluster and keyspace:
        session = Session(cluster,keyspace)
        logging.logger.info('Cassandra session opened successfully to cluster: '+str(cluster)+', keyspace: '+str(keyspace))
        return True
    else:
        logging.logger.error('Cassandra parameters not found. Cluster: '+str(cluster)+' keyspace: '+str(keyspace))
        return None

def terminate_session():
    global session
    if session:
        session.cluster.shutdown()
