'''
Created on 14/12/2012

@author: jcazor
'''

import json
import uuid
import api as cassapi

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
                dbdict[dkey]=json.dumps(value)
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
        
       
class GraphInfoORM(CassandraBase):
    __cf__ = 'graph_info'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.gid
            dbdict={}
            if apiobj.uid:
                dbdict['uid']=str(apiobj.uid)
            if apiobj.name:
                dbdict['name']=apiobj.name
            for dtp in apiobj.get_datapoints():
                dtpinfo=apiobj.get_datapoint_info(dtp)
                dtpcolor=str(dtp)+'_color'
                dtpname=str(dtp)+'_name'
                dbdict[dtpcolor]=dtpinfo['color']
                dbdict[dtpname]=dtpinfo['name']
        super(GraphInfoORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.GraphInfo(self.key,uuid.UUID(self.dbdict['uid']),self.dbdict['name'])
        datapoints=[]
        dtpcolors={}
        dtpnames={}
        for col,value in self.dbdict.iteritems():
            if len(col.split('_'))==2:
                dtp,param=col.split('_')
                dtp=uuid.UUID(dtp)
                datapoints.append(dtp)
                datapoints=list(set(datapoints))
                if param=='color':
                    dtpcolors[dtp]=value
                elif param=='name':
                    dtpnames[dtp]=value
        datapoints=list(datapoints)
        for dtp in datapoints:
            try:
                apiobj.add_datapoint(dtp,dtpcolors[dtp],dtpnames[dtp])
            except KeyError:
                return None
        return apiobj

class GraphDatapointRelationORM(CassandraBase):
    __cf__ = 'graph_dtp_relation'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.gid
            dbdict={}
            for pid in apiobj.pids:
                dbdict[pid]=''
        super(GraphDatapointRelationORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.GraphDatapointRelation(gid)
        for pid in self.dbdict.keys():
            apiobj.add_datapoint(pid)
        return apiobj

class DatapointGraphRelationORM(CassandraBase):
    __cf__ = 'dtp_graph_relation'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.pid
            dbdict={}
            for gid in apiobj.gids:
                dbdict[gid]=''
        super(DatapointGraphRelationORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.DatapointGraphRelation(pid)
        for gid in self.dbdict.keys():
            apiobj.add_graph(gid)
        return apiobj

class DatasourceGraphWeightORM(CassandraBase):
    __cf__ = 'ds_graph_weight'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.did
            dbdict=apiobj.gids
        super(DatasourceGraphWeightORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.DatasourceGraphWeight(self.key)
        apiobj.set_data(self.dbdict)
        return apiobj

class GraphDatasourceWeightORM(CassandraBase):
    __cf__ = 'graph_ds_weight'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.gid
            dbdict=apiobj.dids
        super(GraphDatasourceWeightORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.GraphDatasourceWeight(gid)
        apiobj.set_data(self.dbdict)
        return apiobj

