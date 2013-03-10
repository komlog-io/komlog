'''
Created on 14/12/2012

@author: jcazor
'''

import pycassa

class Pool(object):
    def __init__(self, keyspace=None, server_list=None, pool_size=None):
        self.connection_pool = pycassa.ConnectionPool(keyspace,server_list,pool_size=pool_size)

class CF(object):
    def __init__(self, pool):
        self.pool = pool.connection_pool
        self.cf = {}
    
    def get(self, obj,kwargs={}):
        try:
            key = obj.key
            dbdict = self.cf[obj.__cf__].get(key,**kwargs)
            obj.dbdict = dbdict        
            return obj
        except KeyError:
            self.__new_cf(obj.__cf__)
            dbdict = self.cf[obj.__cf__].get(key,**kwargs)
            obj.dbdict = dbdict
            return obj
    
    def insert(self, obj):
        try:
            self.cf[obj.__cf__].insert(obj.key,obj.dbdict)
            return True
        except KeyError:
            self.__new_cf(obj.__cf__)
            self.cf[obj.__cf__].insert(obj.key,obj.dbdict)
            return True
        else:
            return False
    
    def remove(self, obj,kwargs={}):
        try:
            self.cf[obj.__cf__].remove(key=obj.key,**kwargs)
            return True
        except KeyError:
            self.__new_cf(obj.__cf__)
            self.cf[obj.__cf__].remove(key=obj.key,**kwargs)
            return True
        else:
            return False

    def __new_cf(self, cf):
        self.cf[cf]=pycassa.ColumnFamily(self.pool,cf)

    def __del_cf(self, cf):
        self.cf[cf]=None

