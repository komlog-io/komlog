'''
Created on 14/12/2012

@author: jcazor
'''

class CassandraBase(object):
    def __init__(self, key=None, dbdict=None):
        self.key = key
        self.dbdict = dbdict

    def get_key(self):
        return self.key

    def get_dbdict(self):
        return self.dbdict

class SampleORM(CassandraBase):
    __cf__ = 'smp_data'
    
    def __init__(self, key=None, dbdict=None):
        super(SampleORM,self).__init__(key, dbdict)
        
      
class SampleMapORM(CassandraBase):
    __cf__ = 'smp_map'

    def __init__(self, key=None, dbdict=None):
        super(SampleMapORM,self).__init__(key, dbdict)

class SampleInfoORM(CassandraBase):
    __cf__ = 'smp_info'

    def __init__(self, key=None, dbdict=None):
        super(SampleInfoORM,self).__init__(key, dbdict)

class DatapointInfoORM(CassandraBase):
    __cf__ = 'dtp_info'
    
    def __init__(self, key=None, dbdict=None):
        super(DatapointInfoORM,self).__init__(key, dbdict)
        
        
class DatapointValuesORM(CassandraBase):
    __cf__ = 'dtp_data'

    def __init__(self, key=None, dbdict=None):
        super(DatapointValuesORM,self).__init__(key, dbdict)

class DsDtpRelationORM(CassandraBase):
    __cf__ = 'ds_dtp_relation'

    def __init__(self, key=None, dbdict=None):
        super(DsDtpRelationORM,self).__init__(key, dbdict)

############

class DatasourceDataORM(CassandraBase):
    __cf__ = 'ds_data'

    def __init__(self, key=None, dbdict=None):
        date=str(dbdict.keys()[0].date())
        pkey=str(key)+'_'+date
        super(DatasourceDataORM,self).__init__(pkey,dbdict)

    def get_key(self):
        return self.key.split('_')[0]

class DatasourceMapORM(CassandraBase):
    __cf__ = 'ds_map'

    def __init__(self, key=None, dbdict=None):
        date=str(dbdict.keys()[0].date())
        pkey=str(key)+'_'+date
        super(DatasourceMapORM,self).__init__(pkey,dbdict)

    def get_key(self):
        return self.key.split('_')[0]

class DatasourceMapVarsORM(CassandraBase):
    __cf__ = 'ds_map_vars'

    def __init__(self, key=None, dbdict=None):
        date=str(dbdict.keys()[0].date())
        pkey=str(key)+'_'+date
        super(DatasourceMapVarsORM,self).__init__(pkey,dbdict)

    def get_key(self):
        return self.key.split('_')[0]

