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
    
    def get(self, obj):
        key = obj.key
        dbdict = self.cf.get(key)
        obj.dbdict = dbdict        
        return obj
    
    def insert(self, obj):
        self.cf.insert(obj.key,obj.dbdict)
    
    def remove(self, obj):
        self.cf.remove(key=obj.key)

class SamplesCF(CF):
    __keyspace__ = 'samples'
    def __init__(self, pool):
        super(SamplesCF,self).__init__(pool, self.__keyspace__)
