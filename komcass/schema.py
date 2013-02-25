'''
Created on 14/12/2012

@author: jcazor
'''

class CassandraBase(object):
    def __init__(self, key=None, dbdict=None):
        self.key = key
        self.dbdict = dbdict

class SampleORM(CassandraBase):
    __keyspace__ = 'samples'
    
    def __init__(self, key=None, dbdict=None):
        super(SampleORM,self).__init__(key, dbdict)
        
        
class SampleMapORM(CassandraBase):
    __keyspace__ = 'sample_m'

    def __init__(self, key=None, dbdict=None):
        super(SampleMapORM,self).__init__(key, dbdict)
