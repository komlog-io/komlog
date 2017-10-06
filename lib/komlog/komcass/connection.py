'''
Created on 01/10/2014

@author: komlog crew
'''

import asyncio
from functools import partial
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.policies import RetryPolicy
from cassandra.query import dict_factory, BatchStatement
from komlog.komcass.model import statement
from komlog.komfig import logging, config, options

session = None

class Session:
    def __init__(self, cluster, keyspace=None):
        self._loop = asyncio.get_event_loop()
        self.cluster = Cluster(cluster, default_retry_policy=RetryPolicy())
        self.session = self.cluster.connect(keyspace)
        self.session.row_factory = dict_factory
        self.stmts={}

    def _asyncio_result(self, fut, result):
        self._loop.call_soon_threadsafe(fut.set_result, result)

    def _asyncio_exception(self, fut, exc):
        self._loop.call_soon_threadsafe(fut.set_exception, exc)

    def execute(self,stmt,parameters):
        try:
            #c_fut = self.session.execute_async(self.stmts[stmt], parameters)
            #a_fut = self._loop.create_future()
            #c_fut.add_callbacks(
                #partial(self._asyncio_result, a_fut),
                #partial(self._asyncio_exception, a_fut)
            #)
            #return self._loop.run_until_complete(a_fut)
            return self.session.execute(self.stmts[stmt],parameters)
        except KeyError:
            self.stmts[stmt]=self.session.prepare(statement.get_statement(stmt))
            return self.execute(stmt,parameters)

    def execute_batch(self,stmts):
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
        for item in stmts:
            try:
                batch.add(self.stmts[item[0]],item[1])
            except KeyError:
                self.stmts[item[0]] = self.session.prepare(statement.get_statement(item[0]))
                batch.add(self.stmts[item[0]],item[1])
        #c_fut = self.session.execute_async(batch)
        #a_fut = self._loop.create_future()
        #c_fut.add_callbacks(
            #partial(self._asyncio_result, a_fut),
            #partial(self._asyncio_exception, a_fut)
        #)
        #return self._loop.run_until_complete(a_fut)
        return self.session.execute(batch)

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

