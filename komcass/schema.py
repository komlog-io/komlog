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

class DatapointStatsORM(CassandraBase):
    __cf__ = 'dtp_stats'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.pid
            dbdict={}
            if apiobj.last_received:
                dbdict['last_received']=apiobj.last_received
        super(DatapointStatsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.DatapointStats(self.key)
        for key,value in self.dbdict.iteritems():
            if key in ['last_received']:
                setattr(apiobj,key,value)
        return apiobj

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
        apiobj=cassapi.GraphDatapointRelation(self.key)
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
        apiobj=cassapi.DatapointGraphRelation(self.key)
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
        apiobj=cassapi.GraphDatasourceWeight(self.key)
        apiobj.set_data(self.dbdict)
        return apiobj

#Segmentation

class SegmentParamsORM(CassandraBase):
    __cf__ = 'prm_segment'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            key=int(key)
            dbdict=dbdict
        if apiobj:
            key=int(apiobj.segid)
            dbdict=apiobj._paramlist
        super(SegmentParamsORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.SegmentParams(self.key)
        apiobj.set_params(self.dbdict)
        return apiobj

class UserQuoORM(CassandraBase):
    __cf__ = 'mst_user_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.uid
            self.dbdict=apiobj._quotes
        super(UserQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.UserQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj

class AgentQuoORM(CassandraBase):
    __cf__ = 'mst_agent_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.aid
            self.dbdict=apiobj._quotes
        super(AgentQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.AgentQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj

class DatasourceQuoORM(CassandraBase):
    __cf__ = 'mst_ds_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.did
            self.dbdict=apiobj._quotes
        super(DatasourceQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.DatasourceQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj

class DatapointQuoORM(CassandraBase):
    __cf__ = 'mst_dtp_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.pid
            self.dbdict=apiobj._quotes
        super(DatapointQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.DatapointQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj

class GraphQuoORM(CassandraBase):
    __cf__ = 'mst_graph_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.gid
            self.dbdict=apiobj._quotes
        super(GraphQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.GraphQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj

class UserAgentPermsORM(CassandraBase):
    __cf__ = 'mst_user_agent_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj._aids
        else:
            key=key
            dbdict=dbdict
        super(UserAgentPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserAgentPerms(self.key)
        apiobj.set_agents(self.dbdict)
        return apiobj

class UserDsPermsORM(CassandraBase):
    __cf__ = 'mst_user_ds_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj._dids
        else:
            key=key
            dbdict=dbdict
        super(UserDsPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserDsPerms(self.key)
        apiobj.set_dss(self.dbdict)
        return apiobj

class UserDtpPermsORM(CassandraBase):
    __cf__ = 'mst_user_dtp_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj._pids
        else:
            key=key
            dbdict=dbdict
        super(UserDtpPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserDtpPerms(self.key)
        apiobj.set_dtps(self.dbdict)
        return apiobj

class UserGraphPermsORM(CassandraBase):
    __cf__ = 'mst_user_graph_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj._gids
        else:
            key=key
            dbdict=dbdict
        super(UserGraphPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserGraphPerms(self.key)
        apiobj.set_graphs(self.dbdict)
        return apiobj

class AgentDsPermsORM(CassandraBase):
    __cf__ = 'mst_agent_ds_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.aid
            dbdict=apiobj._dids
        else:
            key=key
            dbdict=dbdict
        super(AgentDsPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.AgentDsPerms(self.key)
        apiobj.set_dss(self.dbdict)
        return apiobj

class AgentDtpPermsORM(CassandraBase):
    __cf__ = 'mst_agent_dtp_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.aid
            dbdict=apiobj._pids
        else:
            key=key
            dbdict=dbdict
        super(AgentDtpPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.AgentDtpPerms(self.key)
        apiobj.set_dtps(self.dbdict)
        return apiobj

class AgentGraphPermsORM(CassandraBase):
    __cf__ = 'mst_agent_graph_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.aid
            dbdict=apiobj._gids
        else:
            key=key
            dbdict=dbdict
        super(AgentGraphPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.AgentGraphPerms(self.key)
        apiobj.set_graphs(self.dbdict)
        return apiobj

class UserIfaceDenyORM(CassandraBase):
    __cf__ = 'mst_user_iface_deny'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj.get_interfaces()
        else:
            key=key
            dbdict=dbdict
        super(UserIfaceDenyORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserIfaceDeny(self.key)
        apiobj.set_interfaces(self.dbdict)
        return apiobj

class DatasourceCardORM(CassandraBase):
    __cf__ = 'mst_ds_card'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.did
            dbdict={}
            if apiobj.uid:
                dbdict['uid']=apiobj.uid
            if apiobj.aid:
                dbdict['aid']=apiobj.aid
            if apiobj.ag_name:
                dbdict['ag_name']=apiobj.ag_name
            if apiobj.ds_name:
                dbdict['ds_name']=apiobj.ds_name
            if apiobj.ds_date:
                dbdict['ds_date']=apiobj.ds_date
            if apiobj.priority:
                dbdict['priority']=str(apiobj.priority).upper()
            dbdict['datapoints']=json.dumps(apiobj.get_datapoints())
            dbdict['graphs']=[]
            if len(apiobj.get_graphs())>0:
                for gid in apiobj.get_graphs():
                    s_gid=str(gid)
                    dbdict['graphs'].append(s_gid)
            dbdict['graphs']=json.dumps(dbdict['graphs'])
            dbdict['anomalies']=json.dumps(apiobj.get_anomalies())
        super(DatasourceCardORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.DatasourceCard(self.key)
        apiobj.uid=self.dbdict['uid'] if self.dbdict.has_key('uid') else None
        apiobj.aid=self.dbdict['aid'] if self.dbdict.has_key('aid') else None
        apiobj.ag_name=self.dbdict['ag_name'] if self.dbdict.has_key('ag_name') else None
        apiobj.ds_name=self.dbdict['ds_name'] if self.dbdict.has_key('ds_name') else None
        apiobj.ds_date=self.dbdict['ds_date'] if self.dbdict.has_key('ds_date') else None
        apiobj.priority=self.dbdict['priority'] if self.dbdict.has_key('priority') else None
        apiobj._datapoints=json.loads(self.dbdict['datapoints']) if self.dbdict.has_key('datapoints') else []
        if self.dbdict.has_key('graphs'):
            graphlist=json.loads(self.dbdict['graphs'])
            for graph in graphlist:
                gid=uuid.UUID(graph)
                apiobj.add_graph(gid)
        else:
            apiobj._graphs=[]
        apiobj._anomalies=json.loads(self.dbdict['anomalies']) if self.dbdict.has_key('anomalies') else []
        return apiobj


class UserDsCardORM(CassandraBase):
    __cf__ = 'rel_user_ds_card'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.uid
            dbdict={}
            for did,value in apiobj.get_cards().iteritems():
                dbdict[str(value).upper()+'_'+str(did)]=''
        super(UserDsCardORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.UserDsCard(self.key)
        for key in self.dbdict.keys():
            did=uuid.UUID(key.split('_')[-1])
            priority=key.split('_')[0]
            apiobj.add_card(did,priority)
        return apiobj


class AgentDsCardORM(CassandraBase):
    __cf__ = 'rel_agent_ds_card'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.aid
            dbdict={}
            for did,value in apiobj.get_cards().iteritems():
                dbdict[str(value).upper()+'_'+str(did)]=''
        super(AgentDsCardORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.AgentDsCard(self.key)
        for key in self.dbdict.keys():
            did=uuid.UUID(key.split('_')[-1])
            priority=key.split('_')[0]
            apiobj.add_card(did,priority)
        return apiobj

class UserWidgetRelationORM(CassandraBase):
    __cf__ = 'rel_user_widget'

    def __init__(self, key=None, dbdict=None):
        super(UserWidgetRelationORM,self).__init__(key, dbdict)

class UserDashboardRelationORM(CassandraBase):
    __cf__ = 'rel_user_dashboard'

    def __init__(self, key=None, dbdict=None):
        super(UserDashboardRelationORM,self).__init__(key, dbdict)


class DashboardWidgetRelationORM(CassandraBase):
    __cf__ = 'rel_dashboard_widget'

    def __init__(self, key=None, dbdict=None):
        super(DashboardWidgetRelationORM,self).__init__(key, dbdict)

class DashboardORM(CassandraBase):
    __cf__ = 'mst_dashboard'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.bid
            dbdict={}
            dbdict['uid']=apiobj.uid
            dbdict['name']=apiobj.name
        super(DashboardORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.Dashboard(self.key,self.dbdict['uid'],self.dbdict['name'])
        return apiobj

class WidgetORM(CassandraBase):
    __cf__ = 'mst_widget'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.wid
            dbdict={}
            dbdict['uid']=apiobj.uid
            dbdict['type']=apiobj.type
        super(WidgetORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.Widget(self.key,self.dbdict['uid'],self.dbdict['type'])
        return apiobj

class DatasourceWidgetORM(CassandraBase):
    __cf__ = 'mst_datasource_widget'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.wid
            dbdict={}
            dbdict['uid']=apiobj.uid
            dbdict['did']=apiobj.did
        super(DatasourceWidgetORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.DatasourceWidget(self.key,self.dbdict['uid'],self.dbdict['did'])
        return apiobj

class DatapointWidgetORM(CassandraBase):
    __cf__ = 'mst_datapoint_widget'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        key=key
        dbdict=dbdict
        if apiobj:
            key=apiobj.wid
            dbdict={}
            dbdict['uid']=apiobj.uid
            dbdict['pid']=apiobj.pid
        super(DatapointWidgetORM,self).__init__(key,dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.DatapointWidget(self.key,self.dbdict['uid'],self.dbdict['pid'])
        return apiobj

class WidgetQuoORM(CassandraBase):
    __cf__ = 'mst_widget_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.wid
            self.dbdict=apiobj._quotes
        super(WidgetQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.WidgetQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj


class DashboardQuoORM(CassandraBase):
    __cf__ = 'mst_dashboard_quo'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if key:
            self.key=key
            self.dbdict=dbdict
        if apiobj:
            self.key=apiobj.bid
            self.dbdict=apiobj._quotes
        super(DashboardQuoORM,self).__init__(self.key,self.dbdict)
    
    def to_apiobj(self):
        apiobj=cassapi.DashboardQuo(self.key)
        apiobj.set_quotes(self.dbdict)
        return apiobj

class UserWidgetPermsORM(CassandraBase):
    __cf__ = 'mst_user_widget_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj._wids
        else:
            key=key
            dbdict=dbdict
        super(UserWidgetPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserWidgetPerms(self.key)
        apiobj.set_widgets(self.dbdict)
        return apiobj

class UserDashboardPermsORM(CassandraBase):
    __cf__ = 'mst_user_dashboard_perm'

    def __init__(self, key=None, dbdict=None, apiobj=None):
        if apiobj:
            key=apiobj.uid
            dbdict=apiobj._bids
        else:
            key=key
            dbdict=dbdict
        super(UserDashboardPermsORM,self).__init__(key,dbdict)

    def to_apiobj(self):
        apiobj=cassapi.UserDashboardPerms(self.key)
        apiobj.set_dashboards(self.dbdict)
        return apiobj

