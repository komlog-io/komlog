#coding: utf-8
'''
Created on 14/12/2012

@author: jcazor
'''

import exceptions, schema
from pycassa.cassandra.ttypes import NotFoundException
import uuid
import json
from komlibs.date import datefuncs
from datetime import timedelta

class DsDtpRelation:
    def __init__(self, did=None, dtps=None, key=None, dbdict=None):
        if key:
            self.did=key
            self.dbcols = dbdict
            self.dtps = []
            for key in self.dbcols.keys():
                self.dtps.append(key)
        else:
            self.did=did
            self.dtps = dtps if dtps else []
            self.prestore()

    def prestore(self):
        self.key=self.did
        self.dbdict = {}
        for pid in self.dtps:
            self.dbdict[pid]=u''


def get_dsdtprelation(did, session):
    try:
        dbobj=session.get(schema.DsDtpRelationORM(key=did,dbdict={}))
        return DsDtpRelation(key=dbobj.key,dbdict=dbobj.dbdict)
    except NotFoundException:
        return None

class DatapointInfo:
    def __init__(self, pid=None, name=None, dtree=None, positives=None, negatives=None, did=None, key=None,dbdict=None):
        if key:
            self.pid=key
            self.dbcols = dbdict
            if self.dbcols.has_key('did'):
                self.did=uuid.UUID(self.dbcols['did'])
            try:
                self.dbcols['positives']=json.loads(self.dbcols['positives'])
            except KeyError:
                self.dbcols['positives']=[]
            try:
                self.dbcols['negatives']=json.loads(self.dbcols['negatives'])
            except KeyError:
                self.dbcols['negatives']=[]
            try:
                self.dbcols['dtree']=json.loads(self.dbcols['dtree'])
            except KeyError:
                self.dbcols['dtree']=[]
        else:
            self.did=did
            self.pid=pid
            self.dbcols={}
            if dtree:
                dtree=json.dumps(dtree)
                self.dbcols['dtree']=dtree
            if positives:
                positives=json.dumps(positives)
                self.dbcols['positives']=positives
            if negatives:
                negatives=json.dumps(negatives)
                self.dbcols['negatives']=negatives
            if did:
                self.dbcols['did']=str(did)
            else:
                raise exceptions.ParameterNotFoundException('did')
            if name:
                self.dbcols['name']=name
            else:
                raise exceptions.ParameterNotFoundException('name')
            self.prestore()
    
    def prestore(self):
        if self.dbcols.has_key('dtree') and type(self.dbcols['dtree'])==list:
            self.dbcols['dtree']=json.dumps(self.dbcols['dtree'])
        if self.dbcols.has_key('positives') and type(self.dbcols['positives'])==list:
            self.dbcols['positives']=json.dumps(self.dbcols['positives'])
        if self.dbcols.has_key('negatives') and type(self.dbcols['negatives'])==list:
            self.dbcols['negatives']=json.dumps(self.dbcols['negatives'])
        self.key=self.pid
        self.dbdict=self.dbcols


def get_dtpinfo(pid,dbcols,session):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.DatapointInfoORM(key=pid,dbdict={}),kwargs)
        return DatapointInfo(key=dbobj.key,dbdict=dbobj.dbdict)
    except NotFoundException:
        return None

def register_dtp(dtp,dsdtprelation,session):
    try:
        dsdtprelation.dtps.insert(0,dtp.pid)
        dsdtprelation.prestore()
        session.insert(schema.DsDtpRelationORM(key=dsdtprelation.key, dbdict=dsdtprelation.dbdict))
        dtp.prestore()
        session.insert(schema.DatapointInfoORM(key=dtp.key, dbdict=dtp.dbdict))
        return True
    except Exception:
        remove_dtp(dtp,dsdtprelation,session)
        return False

def remove_dtp(dtp,dsdtprelation,session):
    try:
        session.remove(schema.DatapointInfoORM(key=dtp.key, dbdict=dtp.dbdict))
        kwargs={}
        kwargs['columns']=(dtp.pid,)
        session.remove(schema.DsDtpRelationORM(key=dsdtprelation.key, dbdict=dsdtprelation.dbdict),kwargs)
        return True
    except Exception as e:
        return False

def update_dtp(dtp,session):
    try:
        dtp.prestore()
        session.insert(schema.DatapointInfoORM(key=dtp.key, dbdict=dtp.dbdict))
        return True
    except Exception as e:
        return False

class DatapointData:
    def __init__(self, pid=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.pid=uuid.UUID(key)
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.pid = pid
            self.date = date
            self.content = content # unicode
            self.prestore()

    def prestore(self):
        self.key=str(self.pid)
        self.dbdict = {}
        self.dbdict[self.date]=self.content.encode('utf8')

def insert_datapointdata(dtpobj,session):
    dtpobj.prestore()
    if session.insert(schema.DatapointDataORM(key=dtpobj.key,dbdict=dtpobj.dbdict)):
        return True
    else:
        return False

def get_datapointdata(pid,session,date=None,fromdate=None,todate=None):
    dtpdatas=[]
    kwargs={}
    if date:
        kwargs['columns']=(date,)
        start_date=date
        end_date=date
    elif fromdate and todate:
        kwargs['column_start']=fromdate
        kwargs['column_finish']=todate
        start_date=fromdate
        end_date=todate
    elif todate:
        kwargs['column_start']=todate
        kwargs['column_reversed']=True
        start_date=todate-timedelta(days=1)
        end_date=todate
    elif fromdate:
        kwargs['column_start']=fromdate
        start_date=fromdate
        end_date=todate+timedelta(days=1)
    for date in datefuncs.get_range(start_date,end_date,interval='days',num=1,reverse_order=True):
        try:
            dbobj=session.get(schema.DatapointDataORM(key=pid,dbdict={date:u''}),kwargs)
            if dbobj:
                for date,content in dbobj.get_dbdict().iteritems():
                    dtpdatas.append(DatapointData(pid=dbobj.get_key(),date=date,content=content))
        except NotFoundException:
            pass
    if len(dtpdatas)>0:
        if fromdate or todate:
            return dtpdatas
        else:
            return dtpdatas[0] if len(dtpdatas)==1 else dtpdatas
    else:
        return None


def remove_datapointdata(pid,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatapointDataORM(key=pid,dbdict={date:u''}),kwargs):
        return True
    else:
        return False

class DatasourceData:
    def __init__(self, did=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.did=uuid.UUID(key)
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.did = did
            self.date = date
            self.content = content # unicode
            self.prestore()

    def prestore(self):
        self.key=str(self.did)
        self.dbdict = {}
        self.dbdict[self.date]=self.content.encode('utf8')

def insert_datasourcedata(dsobj,session):
    dsobj.prestore()
    if session.insert(schema.DatasourceDataORM(key=dsobj.key,dbdict=dsobj.dbdict)):
        dsinfo=get_dsinfo(dsobj.did,{'last_received':u''},session)
        if dsinfo:
            if dsinfo.last_received<dsobj.date:
                dsinfo.last_received=dsobj.date
                update_ds(dsinfo,session)
        else:
            dsinfo=DatasourceInfo(did=dsobj.did,last_received=dsobj.date)
            update_ds(dsinfo,session)
        return True
    else:
        return False

def get_datasourcedata(did,date,session):
    try:
        kwargs={}
        kwargs['columns']=(date,)
        dbobj=session.get(schema.DatasourceDataORM(key=did,dbdict={date:u''}),kwargs)
        return DatasourceData(key=dbobj.get_key(),dbdict=dbobj.get_dbdict())
    except NotFoundException:
        return None

def remove_datasourcedata(did,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatasourceDataORM(key=did,dbdict={date:u''}),kwargs):
        return True
    else:
        return False


class DatasourceMap:
    def __init__(self, did=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.did=key
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.did = did
            self.date = date
            self.content = content # unicode
            self._key=self.did
            self._dbdict = {}
            self._dbdict[date]=self.content.encode('utf8')

class DatasourceMapVars:
    def __init__(self, did=None, date=None, content=None,key=None,dbdict=None):
        if key:
            self.did=key
            self.date=dbdict.keys()[0] if len(dbdict.keys()) == 1 else dbdict.keys()
            self.content=dbdict.values()[0] if len(dbdict.values()) == 1 else dbdict.values()
        else:
            self.did = did
            self.date = date
            self.content = content # unicode
            self._key=self.did
            self._dbdict = {}
            self._dbdict[date]=self.content.encode('utf8')

def insert_datasourcemap(dsmobj,dsmvobj,session):
    if session.insert(schema.DatasourceMapORM(key=dsmobj._key,dbdict=dsmobj._dbdict)) and \
       session.insert(schema.DatasourceMapVarsORM(key=dsmvobj._key,dbdict=dsmvobj._dbdict)):
        return True
    else:
        remove_datasourcemap(dsmobj.did,dsmobj.date,session)
        return False

def get_datasourcemap(did,session,date=None,fromdate=None,todate=None):
    dsmaps=[]
    kwargs={}
    if date:
        kwargs['columns']=(date,)
        start_date=date
        end_date=date
    elif fromdate and todate:
        kwargs['column_start']=fromdate
        kwargs['column_finish']=todate
        start_date=fromdate
        end_date=todate
    elif todate:
        kwargs['column_finish']=todate
        start_date=todate-timedelta(days=1)
        end_date=todate
    elif fromdate:
        kwargs['column_start']=fromdate
        start_date=fromdate
        end_date=todate+timedelta(days=1)
    for date in datefuncs.get_range(start_date,end_date,interval='day',num=1):
        try:
            dbobj=session.get(schema.DatasourceMapORM(key=did,dbdict={date:u''}),kwargs)
            if dbobj:
                for date,content in dbobj.get_dbdict().iteritems():
                    dsmaps.append(DatasourceMap(did=dbobj.get_key(),date=date,content=content))
        except NotFoundException:
            pass
    if len(dsmaps)>0:
        if fromdate or todate:
            return dsmaps
        else:
            return dsmaps[0] if len(dsmaps)==1 else dsmaps
    else:
        return None

def get_datasourcemapvars(did,date,session):
    try:
        kwargs={}
        kwargs['columns']=(date,)
        dbobj=session.get(schema.DatasourceMapVarsORM(key=did,dbdict={date:u''}),kwargs)
        return DatasourceMapVars(key=dbobj.get_key(),dbdict=dbobj.get_dbdict())
    except NotFoundException:
        return None

def remove_datasourcemap(did,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatasourceMapORM(key=did,dbdict={date:u''}),kwargs) and \
       session.remove(schema.DatasourceMapVarsORM(key=did,dbdict={date:u''}),kwargs):
        return True
    else:
        return False

class DatasourceMapDtps:
    def __init__(self, did, fromdict=None, date=None, jsoncontent=None):
        if fromdict:
            print fromdict
            self.did=did
            self.date=fromdict.keys()[0]
            self.jsoncontent=fromdict.values()[0]
        else:
            self.did = did
            self.date = date
            self.jsoncontent = jsoncontent

    def _prestore(self):
        self.key=self.did
        self.dbdict={}
        self.dbdict[self.date]=self.jsoncontent

def get_datasourcemapdtps(did,date,session):
    try:
        kwargs={}
        kwargs['columns']=(date,)
        dbobj=session.get(schema.DatasourceMapDtpsORM(key=did,dbdict={date:u''}),kwargs)
        return DatasourceMapDtps(did=dbobj.get_key(),fromdict=dbobj.get_dbdict())
    except NotFoundException:
        return None

def insert_datasourcemapdtps(obj,session):
    obj._prestore()
    if session.insert(schema.DatasourceMapDtpsORM(key=obj.key,dbdict=obj.dbdict)):
        return True
    else:
        return False

def remove_datasourcemapdtps(obj,session):
    if session.remove(schema.DatasourceMapDtpsORM(key=obj.key,dbdict=obj.dbdict)):
        return True
    else:
        return False


class UserUIDRelation:
    def __init__(self, username, uid):
        self.uid=uid
        self.username=username

    def _prestore(self):
        self.key=self.username
        self.dbdict = {self.uid:u''}


def get_useruidrelation(username, session):
    try:
        dbobj=session.get(schema.UserUIDRelationORM(key=username,dbdict={}))
        return UserUIDRelation(username=dbobj.key,uid=dbobj.dbdict.keys()[0])
    except NotFoundException:
        return None

class UserAgentRelation:
    def __init__(self, uid, aids):
        self.uid=uid
        self.aids=aids
    def _prestore(self):
        self.key=self.uid
        self.dbdict = {}
        for aid in self.aids:
            self.dbdict[aid]=u''

def get_useragentrelation(uid, session):
    try:
        dbobj=session.get(schema.UserAgentRelationORM(key=uid,dbdict={}))
        return UserAgentRelation(uid=dbobj.key,aids=[aid for aid in dbobj.dbdict.keys()])
    except NotFoundException:
        return None

class UserAgentPubKeyRelation:
    def __init__(self, uid, pubkeys_aids):
        self.uid=uid
        self.pubkeys_aids=pubkeys_aids
        self._prestore()
    def _prestore(self):
        self.key=self.uid
        self.dbdict = {}
        for (pubkey,aid) in self.pubkeys_aids:
            self.dbdict[pubkey]=aid

def get_useragentpubkeyrelation(uid,dbcols,session):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.UserAgentPubKeyRelationORM(key=uid,dbdict={}),kwargs)
        return UserAgentPubKeyRelation(uid=dbobj.key,pubkeys_aids=[(pubkey,aid) for (pubkey,aid) in dbobj.dbdict.iteritems()])
    except NotFoundException:
        return None

class AgentDsRelation:
    def __init__(self, aid, dids):
        self.aid=aid
        self.dids=dids

    def _prestore(self):
        self.key=self.aid
        self.dbdict = {}
        for did in self.dids:
            self.dbdict[did]=u''


def get_agentdsrelation(aid, session):
    try:
        dbobj=session.get(schema.AgentDsRelationORM(key=aid,dbdict={}))
        return AgentDsRelation(aid=dbobj.key,dids=[did for did in dbobj.dbdict.keys()])
    except NotFoundException:
        return None

''' USER CLASSES AND METHODS '''

class UserInfo:
    def __init__(self, uid, fromdict=None, username=None, password=None, segment=None, creation_date=None, state=None):
        if fromdict:
            self.uid=uid
            self.username=fromdict['username'] if fromdict.has_key('username') else None
            self.password=fromdict['password'] if fromdict.has_key('password') else None
            self.segment=fromdict['segment'] if fromdict.has_key('segment') else None
            self.creation_date=fromdict['creation_date'] if fromdict.has_key('creation_date') else None
            self.state=fromdict['state'] if fromdict.has_key('state') else None
        else:
            self.uid=uid
            self.username=username
            self.password=password
            self.segment=segment
            self.creation_date=creation_date
            self.state=state
        
    def _prestore(self):
        self.key=self.uid
        self.dbdict={}
        if self.username is not None:
            self.dbdict['username']=self.username
        if self.password is not None:
            self.dbdict['password']=self.password
        if self.segment is not None:
            self.dbdict['segment']=self.segment
        if self.creation_date is not None:
            self.dbdict['creation_date']=self.creation_date
        if self.state is not None:
            self.dbdict['state']=self.state

def get_userinfo(uid,dbcols,session):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.UserInfoORM(key=uid,dbdict={}),kwargs)
        return UserInfo(uid=dbobj.key,fromdict=dbobj.dbdict)
    except NotFoundException:
        return None

def register_user(userinfo,session):
    try:
        uid=userinfo.uid
        username=userinfo.username
        useruidr=get_useruidrelation(username,session)
        if not useruidr:
            useruidr=UserUIDRelation(username,uid)
            useruidr._prestore()
            if session.insert(schema.UserUIDRelationORM(key=useruidr.key,dbdict=useruidr.dbdict)):
                userinfo._prestore()
                if session.insert(schema.UserInfoORM(key=userinfo.key, dbdict=userinfo.dbdict)):
                    return True
                else:
                    remove_user(userinfo,session)
                    return False
            else:
                remove_user(userinfo,session)
                return False
        elif useruidr.uid==uid:
            userinfo._prestore()
            if session.insert(schema.UserInfoORM(key=userinfo.key, dbdict=userinfo.dbdict)):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        remove_user(userinfo,session)
        return False

def remove_user(userinfo,session):
    try:
        userinfo._prestore()
        session.remove(schema.UserInfoORM(key=userinfo.key, dbdict=userinfo.dbdict))
        useruidr=get_useruidrelation(userinfo.username,session)
        if useruidr:
            useruidr._prestore()
            session.remove(schema.UserUIDRelationORM(key=useruidr.key, dbdict=useruidr.dbdict))
        return True
    except Exception as e:
        return False

def update_user(userinfo,session):
    try:
        userinfo._prestore()
        session.insert(schema.UserInfoORM(key=userinfo.key, dbdict=userinfo.dbdict))
        return True
    except Exception as e:
        return False

'''AGENT CLASSES AND METHODS'''

class AgentInfo:
    def __init__(self, aid, fromdict=None, agentname=None, agentkey=None, version=None, uid=None, state=None):
        if fromdict:
            self.aid=aid
            self.uid=fromdict['uid'] if fromdict.has_key('uid') else None
            self.agentname=fromdict['agentname'] if fromdict.has_key('agentname') else None
            self.agentkey=fromdict['agentkey'] if fromdict.has_key('agentkey') else None
            self.version=fromdict['version'] if fromdict.has_key('version') else None
            self.state=fromdict['state'] if fromdict.has_key('state') else None
        else:
            self.aid=aid
            self.uid=uid
            self.agentname=agentname
            self.agentkey=agentkey
            self.version=version
            self.state=state
        
    def _prestore(self):
        self.key=self.aid
        self.dbdict={}
        if self.uid is not None:
            self.dbdict['uid']=self.uid
        if self.agentname is not None:
            self.dbdict['agentname']=self.agentname
        if self.agentkey is not None:
            self.dbdict['agentkey']=self.agentkey
        if self.version is not None:
            self.dbdict['version']=self.version
        if self.state is not None:
            self.dbdict['state']=self.state

def get_agentinfo(aid,dbcols,session):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.AgentInfoORM(key=aid,dbdict={}),kwargs)
        return AgentInfo(aid=dbobj.key,fromdict=dbobj.dbdict)
    except NotFoundException:
        return None

def register_agent(agentinfo,session):
    print 'Vamos a registrar el agente'
    try:
        aid=agentinfo.aid
        uid=agentinfo.uid
        pubkey=agentinfo.agentkey
        useragentr=get_useragentrelation(uid,session)
        if useragentr:
            print 'useragentr con datos'
            try:
                aidpos = useragentr.aids.index(aid)
                return False
            except ValueError:
                pass
        if not useragentr:
            useragentr=UserAgentRelation(uid=uid,aids=[])
        useragentr.aids.append(aid)
        useragentr._prestore()
        print 'Empieza lo serio'
        if session.insert(schema.UserAgentRelationORM(key=useragentr.key,dbdict=useragentr.dbdict)):
            print 'registrada la relacion'
            useragentpubkeyr=UserAgentPubKeyRelation(uid=uid,pubkeys_aids=[(pubkey,aid)])
            print useragentpubkeyr.__dict__
            useragentpubkeyr._prestore()
            if session.insert(schema.UserAgentPubKeyRelationORM(key=useragentpubkeyr.key,dbdict=useragentpubkeyr.dbdict)):
                print 'registrada la key'
                agentinfo._prestore()
                print agentinfo.__dict__
                if session.insert(schema.AgentInfoORM(key=agentinfo.key, dbdict=agentinfo.dbdict)):
                    print 'Registrado correctamente'
                    return True
        remove_agent(agentinfo,session)
        return False
    except Exception as e:
        print str(e)
        remove_agent(agentinfo,session)
        return False

def remove_agent(agentinfo,session):
    try:
        agentinfo._prestore()
        session.remove(schema.AgentInfoORM(key=agentinfo.key, dbdict=agentinfo.dbdict))
        kwargs={}
        kwargs['columns']=(agentinfo.aid,)
        session.remove(schema.UserAgentRelationORM(key=agentinfo.uid, dbdict={}),kwargs)
        kwargs['columns']=(agentinfo.agentkey,)
        session.remove(schema.UserAgentPubKeyRelationORM(key=agentinfo.uid, dbdict={}),kwargs)
        return True
    except Exception as e:
        return False

def update_agent(agentinfo,session):
    try:
        agentinfo._prestore()
        session.insert(schema.AgentInfoORM(key=agentinfo.key, dbdict=agentinfo.dbdict))
        return True
    except Exception as e:
        return False

'''DATASOURCE CLASSES AND METHODS'''

class DatasourceInfo:
    def __init__(self, did, fromdict=None, dsname=None, last_received=None, last_mapped=None, dstype=None, aid=None, creation_date=None, state=None, \
                 script_name=None, day_of_week=None, month=None, day_of_month=None, hour=None, minute=None):
        if fromdict:
            self.did=did
            self.aid=fromdict['aid'] if fromdict.has_key('aid') else None
            self.dsname=fromdict['dsname'] if fromdict.has_key('dsname') else None
            self.dstype=fromdict['dstype'] if fromdict.has_key('dstype') else None
            self.last_received=fromdict['last_received'] if fromdict.has_key('last_received') else None
            self.last_mapped=fromdict['last_mapped'] if fromdict.has_key('last_mapped') else None
            self.creation_date=fromdict['creation_date'] if fromdict.has_key('creation_date') else None
            self.state=fromdict['state'] if fromdict.has_key('state') else None
            self.script_name=fromdict['script_name'] if fromdict.has_key('script_name') else None
            self.day_of_week=fromdict['day_of_week'] if fromdict.has_key('day_of_week') else None
            self.month=fromdict['month'] if fromdict.has_key('month') else None
            self.day_of_month=fromdict['day_of_month'] if fromdict.has_key('day_of_month') else None
            self.hour=fromdict['hour'] if fromdict.has_key('hour') else None
            self.minute=fromdict['minute'] if fromdict.has_key('minute') else None
        else:
            self.did=did
            self.aid=aid
            self.dsname=dsname
            self.last_received=last_received
            self.last_mapped=last_mapped
            self.dstype=dstype
            self.creation_date=creation_date
            self.state=state
            self.script_name=script_name
            self.day_of_week=day_of_week
            self.month=month
            self.day_of_month=day_of_month
            self.hour=hour
            self.minute=minute
        
    def _prestore(self):
        self.key=self.did
        self.dbdict={}
        if self.aid:
            self.dbdict['aid']=self.aid
        if self.dsname:
            self.dbdict['dsname']=self.dsname
        if self.dstype:
            self.dbdict['dstype']=self.dstype
        if self.last_received:
            self.dbdict['last_received']=self.last_received
        if self.last_mapped:
            self.dbdict['last_mapped']=self.last_mapped
        if self.creation_date:
            self.dbdict['creation_date']=self.creation_date
        if self.state:
            self.dbdict['state']=self.state
        if self.script_name:
            self.dbdict['script_name']=self.script_name
        if self.day_of_week:
            self.dbdict['day_of_week']=self.day_of_week
        if self.month:
            self.dbdict['month']=self.month
        if self.day_of_month:
            self.dbdict['day_of_month']=self.day_of_month
        if self.hour:
            self.dbdict['hour']=self.hour
        if self.minute:
            self.dbdict['minute']=self.minute

def get_dsinfo(did,dbcols,session):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.DatasourceInfoORM(key=did,dbdict={}),kwargs)
        return DatasourceInfo(did=dbobj.key,fromdict=dbobj.dbdict)
    except NotFoundException:
        return None

def register_datasource(dsinfo,session):
    try:
        did=dsinfo.did
        aid=dsinfo.aid
        agentdsr=get_agentdsrelation(aid,session)
        if agentdsr:
            try:
                didpos = agentdsr.dids.index(did)
                return False
            except ValueError:
                pass
        else:
            if not agentdsr:
                agentdsr=AgentDsRelation(aid=aid,dids=[])
            agentdsr.dids.append(did)
            agentdsr._prestore()
            if session.insert(schema.AgentDsRelationORM(key=agentdsr.key,dbdict=agentdsr.dbdict)):
                dsinfo._prestore()
                if session.insert(schema.DatasourceInfoORM(key=dsinfo.key, dbdict=dsinfo.dbdict)):
                    return True
                else:
                    remove_ds(dsinfo,session)
                    return False
            else:
                remove_ds(dsinfo,session)
                return False
    except Exception as e:
        print str(e)
        remove_ds(dsinfo,session)
        return False

def remove_ds(dsinfo,session):
    try:
        dsinfo._prestore()
        session.remove(schema.DatasourceInfoORM(key=dsinfo.key, dbdict=dsinfo.dbdict))
        kwargs={}
        kwargs['columns']=(dsinfo.did,)
        session.remove(schema.AgentDsRelationORM(key=dsinfo.aid, dbdict={}),kwargs)
        return True
    except Exception as e:
        return False

def update_ds(dsinfo,session):
    try:
        dsinfo._prestore()
        session.insert(schema.DatasourceInfoORM(key=dsinfo.key, dbdict=dsinfo.dbdict))
        return True
    except Exception as e:
        return False

