'''
Created on 14/12/2012

@author: jcazor
'''

import json

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
        
        
class DatapointDataORM(CassandraBase):
    __cf__ = 'dtp_data'

    def __init__(self, key=None, dbdict=None):
        date=str(dbdict.keys()[0].date())
        pkey=str(key)+'_'+date
        super(DatapointDataORM,self).__init__(pkey,dbdict)

class DatapointDtreePositivesORM(CassandraBase):
    __cf__ = 'dtp_dtree_positives'

    def __init__(self, key=None, dbdict=None):
        if dbdict:
            for dkey,value in dbdict.iteritems():
                print 'Tipo obj: '+str(type(value))
                dbdict[dkey]=json.dumps(value)
                print 'Tipo db:' +str(type(dbdict[dkey]))
        super(DatapointDtreePositivesORM,self).__init__(key,dbdict)

    def get_dbdict(self):
        if self.dbdict:
            dbdict={}
            for key,value in self.dbdict.iteritems():
                dbdict[key]=json.loads(value)
            return dbdict
        else:
            return None

class DatapointDtreeNegativesORM(CassandraBase):
    __cf__ = 'dtp_dtree_negatives'

    def __init__(self, key=None, dbdict=None):
        if dbdict:
            for dkey,value in dbdict.iteritems():
                dbdict[dkey]=json.dumps(value)
        super(DatapointDtreeNegativesORM,self).__init__(key,dbdict)
    
    def get_dbdict(self):
        if self.dbdict:
            dbdict={}
            for key,value in self.dbdict.iteritems():
                dbdict[key]=json.loads(value)
            return dbdict
        else:
            return None

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

class DatasourceMapDtpsORM(CassandraBase):
    __cf__ = 'ds_map_dtps'

    def __init__(self, key=None, dbdict=None):
        date=str(dbdict.keys()[0].date())
        pkey=str(key)+'_'+date
        super(DatasourceMapDtpsORM,self).__init__(pkey,dbdict)

    def get_key(self):
        return self.key.split('_')[0]

class UserUIDRelationORM(CassandraBase):
    __cf__ = 'user_uid_relation'

    def __init__(self, key=None, dbdict=None):
        super(UserUIDRelationORM,self).__init__(key, dbdict)

class EmailUIDRelationORM(CassandraBase):
    __cf__ = 'email_uid_relation'

    def __init__(self, key=None, dbdict=None):
        super(EmailUIDRelationORM,self).__init__(key, dbdict)

class UserCodeRelationORM(CassandraBase):
    __cf__ = 'new_user_codes'

    def __init__(self, key=None, dbdict=None):
        super(UserCodeRelationORM,self).__init__(key, dbdict)

class UserAgentRelationORM(CassandraBase):
    __cf__ = 'user_agent_relation'

    def __init__(self, key=None, dbdict=None):
        super(UserAgentRelationORM,self).__init__(key, dbdict)

class UserAgentPubKeyRelationORM(CassandraBase):
    __cf__ = 'user_agent_pubkey_relation'

    def __init__(self, key=None, dbdict=None):
        super(UserAgentPubKeyRelationORM,self).__init__(key, dbdict)

class AgentDsRelationORM(CassandraBase):
    __cf__ = 'agent_ds_relation'

    def __init__(self, key=None, dbdict=None):
        super(AgentDsRelationORM,self).__init__(key, dbdict)

class UserInfoORM(CassandraBase):
    __cf__ = 'user_info'
    
    def __init__(self, key=None, dbdict=None):
        super(UserInfoORM,self).__init__(key, dbdict)
        
       
class AgentInfoORM(CassandraBase):
    __cf__ = 'agent_info'
    
    def __init__(self, key=None, dbdict=None):
        super(AgentInfoORM,self).__init__(key, dbdict)
        
       
class DatasourceInfoORM(CassandraBase):
    __cf__ = 'ds_info'
    
    def __init__(self, key=None, dbdict=None):
        super(DatasourceInfoORM,self).__init__(key, dbdict)
        
       
