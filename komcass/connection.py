'''
Created on 14/12/2012

@author: jcazor
'''

import pycassa

class Pool(object):
    def __init__(self, keyspace=None, server_list=None, pool_size=None):
        self.connection_pool = pycassa.ConnectionPool(keyspace,server_list,pool_size=pool_size)

class CF(object):
    def __init__(self, pool, keyspace):
        self.cf = pycassa.ColumnFamily(pool, keyspace)
    
    def get(self, key):
        return key, self.cf.get(key)
    
    def insert(self, key, cols):
        self.cf.insert(key,cols)

class SamplesCF(CF):
    def __init__(self, pool):
        self.keyspace = 'samples'
        super(SamplesCF,self).__init__(pool, self.keyspace)
