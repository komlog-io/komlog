'''
Created on 01/10/2014

@author: komlog crew
'''

from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from komcass.model import statement

session = None

class Session:
    def __init__(self, ip_list, keyspace=None):
        self.cluster = Cluster(ip_list)
        self.session = self.cluster.connect(keyspace)
        self.session.row_factory = dict_factory
        self.stmts={}

    def execute(self,stmt,parameters):
        try:
            row = self.session.execute(self.stmts[stmt],parameters)
            return row
        except KeyError:
            self.stmts[stmt]=self.session.prepare(statement.get_statement(stmt))
            row = self.session.execute(self.stmts[stmt],parameters)
            return row
        except Exception as e:
            print 'Otra exception en la session: '+str(e)
            return None

def initialize_session(ip_list,keyspace):
    global session
    if not session:
        session = Session(ip_list,keyspace)

