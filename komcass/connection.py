'''
Created on 14/12/2012

@author: jcazor
'''

import pycassa

pool = pycassa.ConnectionPool('komlog', ['be1:9160'], pool_size=5)


class CF(object):
    def __init__(self, keyspace):
        self.cf = pycassa.ColumnFamily(pool, keyspace)
    
    def get(self, key):
        return key, self.cf.get(key)
    
    def insert(self, key, cols):
        self.cf.insert(key,cols)

class SamplesCF(CF):
    def __init__(self):
        self.keyspace = 'samples'
        super(SamplesCF,self).__init__(self.keyspace)
        

samples_cf = SamplesCF()
