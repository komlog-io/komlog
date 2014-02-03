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


def get_dsdtprelation(did, session, dbcols={}):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.DsDtpRelationORM(key=did,dbdict={}),kwargs)
        return DsDtpRelation(key=dbobj.key,dbdict=dbobj.dbdict)
    except NotFoundException:
        return None

class DatapointInfo:
    def __init__(self, pid=None, name=None, dtree=None, did=None, decimalseparator=None,  key=None,dbdict=None):
        if key:
            self.pid=key
            self.dbcols = dbdict
            if self.dbcols.has_key('did'):
                self.did=uuid.UUID(self.dbcols['did'])
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
            if did:
                self.dbcols['did']=str(did)
            else:
                raise exceptions.ParameterNotFoundException('did')
            if name:
                self.dbcols['name']=name
            else:
                raise exceptions.ParameterNotFoundException('name')
            if decimalseparator:
                self.dbcols['decimalseparator']=decimalseparator
            self.prestore()
    
    def prestore(self):
        if self.dbcols.has_key('dtree') and type(self.dbcols['dtree'])==list:
            self.dbcols['dtree']=json.dumps(self.dbcols['dtree'])
        self.key=self.pid
        self.dbdict=self.dbcols

    def get_decimalseparator(self):
        if self.dbcols.has_key('decimalseparator'):
            return self.dbcols['decimalseparator']
        else:
            return None

    def set_decimalseparator(self,char):
        self.dbcols['decimalseparator']=char


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
        delete_dtp(dtp,dsdtprelation,session)
        return False

def delete_dtp(dtp,dsdtprelation,session):
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
            self.content = content # Number()
            self.prestore()

    def prestore(self):
        self.key=str(self.pid)
        self.dbdict = {}
        self.dbdict[self.date]=self.content

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
    for date in datefuncs.get_range(start_date,end_date,interval='days',num=1,reverse_order=True if kwargs.has_key('column_reversed') else False):
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

def delete_datapointdata(pid,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatapointDataORM(key=pid,dbdict={date:u''}),kwargs):
        return True
    else:
        return False


class DatapointDtreePositives:
    def __init__(self, pid):
        self.pid=pid
        self.positives={}

    def set_positive(self, date, positive):
        self.positives[date]=positive
    
    def set_positives(self, positives):
        self.positives=positives

    def del_positive(self,date,positive):
        if self.positives.has_key(date) and self.positives[date]==positive:
            self.positive[date]=[]

    def _prestore(self):
        self._key=self.pid
        self._dbdict=self.positives

def get_dtp_dtree_positives(pid,session,date=None):
    kwargs={}
    if date:
        kwargs['columns']=(date,)
    try:
        dbobj=session.get(schema.DatapointDtreePositivesORM(key=pid,dbdict={date:u''}),kwargs)
        dtpdtreepositiveobj=DatapointDtreePositives(dbobj.get_key())
        dtpdtreepositiveobj.set_positives(dbobj.get_dbdict())
        return dtpdtreepositiveobj
    except NotFoundException:
        return None

def update_dtp_dtree_positives(dtpdtreepos,session):
    try:
        dtpdtreepos._prestore()
        if session.insert(schema.DatapointDtreePositivesORM(key=dtpdtreepos._key,dbdict=dtpdtreepos._dbdict)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_dtp_dtree_positives(dtpdtreepos, session):
    try:
        dtpdtreepos._prestore()
        kwargs={}
        if len(dtpdtreepos.positives.keys())>0:
            kwargs['columns']=(key for key in dtpdtreepos.positives.keys())
        if session.remove(schema.DatapointDtreePositivesORM(key=dtpdtreepos._key),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class DatapointDtreeNegatives:
    def __init__(self, pid):
        self.pid=pid
        self.negatives={}

    def add_negative(self, date, negative):
        if self.negatives.has_key(date):
            try:
                index=self.negatives[date].index(negative)
            except ValueError:
                self.negatives[date].append(negative)
        else:
            self.negatives[date]=[negative]

    def set_negatives(self, negatives):
        self.negatives=negatives

    def del_negative(self, date, negative):
        if self.negatives.has_key(date):
            try:
                index=self.negatives[date].index(negative)
                self.negatives[date].pop(index)
            except ValueError:
                pass

    def _prestore(self):
        self._key=self.pid
        self._dbdict=self.negatives

def get_dtp_dtree_negatives(pid,session,date=None):
    kwargs={}
    if date:
        kwargs['columns']=(date,)
    try:
        dbobj=session.get(schema.DatapointDtreeNegativesORM(key=pid,dbdict={date:u''}),kwargs)
        dtpdtreenegativeobj=DatapointDtreeNegatives(dbobj.get_key())
        dtpdtreenegativeobj.set_negatives(dbobj.get_dbdict())
        return dtpdtreenegativeobj
    except NotFoundException:
        return None

def update_dtp_dtree_negatives(dtpdtreeneg,session):
    dtpdtreeneg._prestore()
    if session.insert(schema.DatapointDtreeNegativesORM(key=dtpdtreeneg._key,dbdict=dtpdtreeneg._dbdict)):
        return True
    else:
        return False

def delete_dtp_dtree_negatives(dtpdtreeneg, session):
    try:
        dtpdtreeneg._prestore()
        kwargs={}
        if len(dtpdtreeneg.negatives.keys())>0:
            kwargs['columns']=(key for key in dtpdtreeneg.negatives.keys())
        if session.remove(schema.DatapointDtreeNegativesORM(key=dtpdtreeneg._key),kwargs):
            return True
        else:
            return False
    except Exception:
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

def delete_datasourcedata(did,date,session):
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
        delete_datasourcemap(dsmobj.did,dsmobj.date,session)
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
        kwargs['column_start']=todate
        kwargs['column_reversed']=True
        start_date=todate-timedelta(days=1)
        end_date=todate
    elif fromdate:
        kwargs['column_start']=fromdate
        start_date=fromdate
        end_date=todate+timedelta(days=1)
    for date in datefuncs.get_range(start_date,end_date,interval='days',num=1,reverse_order=True if kwargs.has_key('column_reversed') else False):
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

def delete_datasourcemap(did,date,session):
    kwargs={'columns':(date,)}
    if session.remove(schema.DatasourceMapORM(key=did,dbdict={date:u''}),kwargs) and \
       session.remove(schema.DatasourceMapVarsORM(key=did,dbdict={date:u''}),kwargs):
        return True
    else:
        return False

class DatasourceMapDtps:
    def __init__(self, did, fromdict=None, date=None, jsoncontent=None):
        if fromdict:
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

def delete_datasourcemapdtps(obj,session):
    try:
        obj._prestore()
        kwargs={}
        if obj.date:
            kwargs['columns']=obj.date
        if session.remove(schema.DatasourceMapDtpsORM(key=obj.key),kwargs):
            return True
        else:
            return False
    except Exception:
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

class EmailUIDRelation:
    def __init__(self, email, uid):
        self.uid=uid
        self.email=email

    def _prestore(self):
        self.key=self.email
        self.dbdict = {self.uid:u''}

def get_emailuidrelation(email, session):
    try:
        dbobj=session.get(schema.EmailUIDRelationORM(key=email,dbdict={}))
        email=dbobj.get_key()
        uid=dbobj.get_dbdict().keys()[0]
        return EmailUIDRelation(email,uid)
    except NotFoundException:
        return None

def insert_emailuidrelation(emailuidr,session):
    try:
        emailuidr._prestore()
        if session.insert(schema.EmailUIDRelationORM(key=emailuidr.key, dbdict=emailuidr.dbdict)):
            return True
        return False
    except Exception:
        return False

def delete_emailuidrelation(emailuidr,session):
    try:
        if session.remove(schema.EmailUIDRelationORM(key=emailuidr.email)):
            return True
        return False
    except Exception:
        return False

class UserCodeRelation:
    def __init__(self, email, code):
        self.email=email
        self.code=code

    def _prestore(self):
        self.key=self.email
        self.dbdict = {self.code:u''}

def get_usercoderelation(email,session):
    try:
        dbobj=session.get(schema.UserCodeRelationORM(key=email,dbdict={}))
        email=dbobj.get_key()
        code=dbobj.get_dbdict().keys()[0]
        return UserCodeRelation(email,code)
    except NotFoundException:
        return None

def insert_usercoderelation(usercoder,session):
    try:
        usercoder._prestore()
        if not session.insert(schema.UserCodeRelationORM(key=usercoder.key,dbdict=usercoder.dbdict)):
            return False
        return True
    except Exception:
        delete_usercoderelation(usercoder,session)
        return False

def delete_usercodrelation(usercoder,session):
    try:
        usercoder._prestore()
        session.remove(schema.UserCodeRelationORM(key=usercoder.key,dbdict=usercoder.dbdict))
        return True
    except Exception as e:
        return False

class UserAgentRelation:
    def __init__(self, uid, aids):
        self.uid=uid
        self.aids=aids
    def _prestore(self):
        self.key=self.uid
        self.dbdict = {}
        for aid in self.aids:
            self.dbdict[aid]=u''

def get_useragentrelation(uid, session, dbcols={}):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.UserAgentRelationORM(key=uid,dbdict={}),kwargs)
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


def get_agentdsrelation(aid, session, dbcols={}):
    try:
        kwargs={}
        if len(dbcols.keys())>0:
            kwargs['columns']=[key for key in dbcols.keys()]
        dbobj=session.get(schema.AgentDsRelationORM(key=aid,dbdict={}),kwargs)
        return AgentDsRelation(aid=dbobj.key,dids=[did for did in dbobj.dbdict.keys()])
    except NotFoundException:
        return None

''' USER CLASSES AND METHODS '''

class UserInfo:
    def __init__(self, uid, fromdict=None, username=None, password=None, email=None, segment=None, creation_date=None, state=None):
        if fromdict:
            self.uid=uid
            self.username=fromdict['username'] if fromdict.has_key('username') else None
            self.password=fromdict['password'] if fromdict.has_key('password') else None
            self.email=fromdict['email'] if fromdict.has_key('email') else None
            self.segment=fromdict['segment'] if fromdict.has_key('segment') else None
            self.creation_date=fromdict['creation_date'] if fromdict.has_key('creation_date') else None
            self.state=fromdict['state'] if fromdict.has_key('state') else None
        else:
            self.uid=uid
            self.username=username
            self.password=password
            self.email=email
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
        if self.email is not None:
            self.dbdict['email']=self.email
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
        email=userinfo.email
        emailuidr=get_emailuidrelation(email,session)
        useruidr=get_useruidrelation(username,session)
        userinfo2=get_userinfo(uid,{},session)
        if emailuidr or useruidr or userinfo2:
            return False
        emailuidr=EmailUIDRelation(email,uid)
        emailuidr._prestore()
        if not session.insert(schema.EmailUIDRelationORM(key=emailuidr.key,dbdict=emailuidr.dbdict)):
            delete_user(userinfo,session)
            return False
        useruidr=UserUIDRelation(username,uid)
        useruidr._prestore()
        if not session.insert(schema.UserUIDRelationORM(key=useruidr.key,dbdict=useruidr.dbdict)):
            delete_user(userinfo,session)
            return False
        userinfo._prestore()
        if not session.insert(schema.UserInfoORM(key=userinfo.key, dbdict=userinfo.dbdict)):
            delete_user(userinfo,session) 
            return False
        return True
    except Exception as e:
        delete_user(userinfo,session)
        return False

def update_user(userinfo,session):
    try:
        userinfo._prestore()
        uid=userinfo.uid
        if not session.insert(schema.UserInfoORM(key=userinfo.key, dbdict=userinfo.dbdict)):
            return False
        return True
    except Exception:
        return False

def delete_user(userinfo,session):
    try:
        userinfo._prestore()
        uid=userinfo.uid
        username=userinfo.username
        email=userinfo.email
        emailuidr=get_emauiluidrelation(email,session)
        if emailuidr and emailuidr.uid==uid:
            emailuidr._prestore()
            session.remove(schema.EmailUIDRelationORM(key=emailuidr.key,dbdict=emailuidr.dbdict))
        useruidr=get_useruidrelation(username,session)
        if useruidr and useruidr.uid==uid:
            useruidr._prestore()
            session.remove(schema.UserUIDRelationORM(key=useruidr.key,dbdict=useruidr.dbdict))
        userinfo2=get_userinfo(uid,{},session)
        if userinfo2:
            userinfo2._prestore()
            session.remove(schema.UserInfoORM(key=userinfo.key,dbdict=userinfo.dbdict))
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
    try:
        aid=agentinfo.aid
        uid=agentinfo.uid
        pubkey=agentinfo.agentkey
        useragentr=get_useragentrelation(uid,session)
        if useragentr:
            try:
                aidpos = useragentr.aids.index(aid)
                return False
            except ValueError:
                pass
        if not useragentr:
            useragentr=UserAgentRelation(uid=uid,aids=[])
        useragentr.aids.append(aid)
        useragentr._prestore()
        if session.insert(schema.UserAgentRelationORM(key=useragentr.key,dbdict=useragentr.dbdict)):
            useragentpubkeyr=UserAgentPubKeyRelation(uid=uid,pubkeys_aids=[(pubkey,aid)])
            useragentpubkeyr._prestore()
            if session.insert(schema.UserAgentPubKeyRelationORM(key=useragentpubkeyr.key,dbdict=useragentpubkeyr.dbdict)):
                agentinfo._prestore()
                if session.insert(schema.AgentInfoORM(key=agentinfo.key, dbdict=agentinfo.dbdict)):
                    return True
        delete_agent(agentinfo,session)
        return False
    except Exception as e:
        print str(e)
        delete_agent(agentinfo,session)
        return False

def delete_agent(agentinfo,session):
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
    def __init__(self, did, fromdict=None, dsname=None, last_received=None, last_mapped=None, dstype=None, aid=None, uid=None, creation_date=None, state=None, \
                 script_name=None, day_of_week=None, month=None, day_of_month=None, hour=None, minute=None):
        if fromdict:
            self.did=did
            self.aid=fromdict['aid'] if fromdict.has_key('aid') else None
            self.uid=fromdict['uid'] if fromdict.has_key('uid') else None
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
            self.uid=uid
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
        for field in ('aid','uid','dsname','dstype','last_received','last_mapped','creation_date',\
                      'state','script_name','day_of_week','month','day_of_month','hour','minute'):
            try:
                self.dbdict[field]=getattr(self, field)
            except AttributeError:
                pass

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
                delete_ds(dsinfo,session)
                return False
        else:
            delete_ds(dsinfo,session)
            return False
    except Exception as e:
        print str(e)
        delete_ds(dsinfo,session)
        return False

def delete_ds(dsinfo,session):
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

''' GRAPH CLASSES AND METHODS '''


class GraphInfo:
    def __init__(self,gid,uid=None,name=None):
        self.gid=gid
        self.uid=uid
        self.name=name
        self._datapoints=[]
        self._dtpcolors={}
        self._dtpnames={}

    def get_datapoints(self):
        return self._datapoints

    def get_datapoint_info(self,pid):
        dtpinfo={}
        try:
            dtpinfo['color']=self._dtpcolors[pid]
            dtpinfo['name']=self._dtpnames[pid]
            return dtpinfo
        except KeyError:
            return None

    def add_datapoint(self, pid,color,name):
        self._datapoints.append(pid)
        self._datapoints=list(set(self._datapoints))
        self._dtpcolors[pid]=color
        self._dtpnames[pid]=name

def get_graphinfo(gid,session):
    try:
        schemaobj=session.get(schema.GraphInfoORM(key=gid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def update_graphinfo(graphinfo,session):
    if not graphinfo:
        return False
    if not session.insert(schema.GraphInfoORM(apiobj=graphinfo)):
        return False
    return True

class GraphDatapointRelation:
    def __init__(self, gid):
        self.gid=gid
        self.pids=[]

    def add_datapoint(self, pid):
        self.pids.append(pid)
        self.pids=list(set(self.pids))

def get_graphdatapointrelation(gid,session):
    try:
        schemaobj=session.get(schema.GraphDatapointRelationORM(key=gid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

class DatapointGraphRelation:
    def __init__(self, pid):
        self.pid=pid
        self.gids=[]

    def add_graph(self, gid):
        self.gids.append(gid)
        self.gids=list(set(self.gids))

def get_datapointgraphrelation(pid,session):
    try:
        schemaobj=session.get(schema.DatapointGraphRelationORM(key=pid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def delete_graph(graphinfo, session):
    gid=graphinfo.gid
    graph_datapoints=graphinfo.get_datapoints()
    graph_datasourcesweight=get_graphdatasourceweight(gid,session)
    if graph_datasourcesweight:
        for did in graph_datasourcesweight.dids.keys():
            session.remove(DatasourceGraphWeightORM(key=did),{'columns':gid})
        session.remove(GraphDatasourceWeightORM(key=gid))
    if graph_datapoints:
        for pid in graph_datapoints:
            session.remove(DatapointGraphRelationORM(key=pid),{'columns':gid})
        session.remove(GraphDatapointRelationORM(key=gid))
    session.remove(GraphInfoORM(key=gid))
    return True

def create_graph(graphinfo, session):
    graph_datapoints=graphinfo.get_datapoints()
    gid=graphinfo.gid
    dtpgraphrarray=[]
    graphdtpr=get_graphdatapointrelation(gid,session)
    if not graphdtpr:
        graphdtpr=GraphDatapointRelation(gid)
    for pid in graph_datapoints:
        graphdtpr.add_datapoint(pid)
        dtpgraphr=get_datapointgraphrelation(pid,session)
        if not dtpgraphr:
            dtpgraphr=DatapointGraphRelation(pid)
        dtpgraphr.add_graph(gid)
        dtpgraphrarray.append(dtpgraphr)
    if not session.insert(schema.GraphInfoORM(apiobj=graphinfo)):
        return False
    if not session.insert(schema.GraphDatapointRelationORM(apiobj=graphdtpr)):
        delete_graph(graphinfo,session)
        return False
    for dtpgraphr in dtpgraphrarray:
        if not session.insert(schema.DatapointGraphRelationORM(apiobj=dtpgraphr)):
            delete_graph(graphinfo,session)
            return False
    return True

class DatasourceGraphWeight:
    def __init__(self, did):
        self.did=did
        self.gids={}

    def add_graph(self, gid,weight):
        self.gids[gid]=weight

    def set_data(self,data):
        self.gids=data

def get_datasourcegraphweight(did,session):
    try:
        schemaobj=session.get(schema.DatasourceGraphWeightORM(key=did))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_datasourcegraphweight(dsgwobj,session):
    try:
        if session.insert(schema.DatasourceGraphWeightORM(apiobj=dsgwobj)):
            return True
        else:
            return False
    except Exception:
        return False

def set_graphweight_on_datasource(did,gid,weight,session):
    dsgraphweight=session.get(schema.DatasourceGraphWeightORM(key=did))
    if not dsgraphweight:
        dsgraphweight=DatasourceGraphWeight(did)
    dsgraphweight.add_graph(gid,weight)
    if insert_datasourcegraphweight(dsgraphweight,session):
        return True
    else:
        return False

class GraphDatasourceWeight:
    def __init__(self, gid):
        self.gid=gid
        self.dids={}

    def add_datasource(self, did,weight):
        self.dids[did]=weight

    def set_data(self,data):
        self.dids=data

def get_graphdatasourceweight(gid,session):
    try:
        schemaobj=session.get(schema.GraphDatasourceWeightORM(key=gid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_graphdatasourceweight(gdswobj,session):
    try:
        if session.insert(schema.GraphDatasourceWeightORM(apiobj=gdswobj)):
            return True
        else:
            return False
    except Exception:
        return False

def set_datasourceweight_on_graph(gid,did,weight,session):
    graphdsweight=session.get(schema.GraphDatasourceWeightORM(key=gid))
    if not graphdsweight:
        graphdsweight=GraphDatasourceWeight(gid)
    graphdsweight.add_datasource(did,weight)
    if insert_graphdatasourceweight(graphdsweight,session):
        return True
    else:
        return False

class SegmentParams:
    def __init__(self,segid):
        self.segid=segid
        self._paramlist={}

    def add_param(self,param,value):
        self._paramlist[param]=value

    def set_params(self,params):
        self._paramlist=params

    def get_params(self):
        return self._paramlist

    def get_param(self, param):
        try:
            return self._paramlist[param]
        except KeyError:
            return None

def get_segment_info(segid,session):
    try:
        schemaobj=session.get(schema.SegmentParamsORM(key=segid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def set_segment_params(segid,paramlist,session):
    segmentparams=SegmentParams(segid)
    segmentparams.set_params(paramlist)
    try:
        if session.insert(schema.SegmentParamsORM(apiobj=segmentparams)):
            return True
        else:
            return False
    except Exception:
        return False

def del_segment_params(segid,paramlist,session):
    segmentparams=SegmentParams(segid)
    segmentparams.set_params(paramlist)
    try:
        if session.remove(schema.SegmentParamsORM(apiobj=segmentparams)):
            return True
        else:
            return False
    except Exception:
        return False

class UserQuo:
    def __init__(self,uid):
        self.uid=uid
        self._quotes={}

    def add_quote(self,quote,value):
        self._quotes[quote]=value

    def set_quotes(self,quotes):
        self._quotes=quotes

    def get_quotes(self):
        return self._quotes

    def get_quote(self,quote):
        try:
            return self._quotes[quote]
        except KeyError:
            return None

def get_user_quotes(uid,session):
    try:
        schemaobj=session.get(schema.UserQuoORM(key=uid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def set_user_quotes(uid,quotes,session):
    userquotes=UserQuo(uid)
    userquotes.set_quotes(quotes)
    objeto=schema.UserQuoORM(apiobj=userquotes)
    try:
        if session.insert(schema.UserQuoORM(apiobj=userquotes)):
            return True
        else:
            return False
    except Exception as e:
        print 'Exception: '+str(e)
        return False

def del_user_quotes(uid,quotes,session):
    userquotes=UserQuo(uid)
    userquotes.set_quotes(quotes)
    try:
        if session.remove(schema.UserQuoORM(apiobj=userquotes)):
            return True
        else:
            return False
    except Exception:
        return False

class AgentQuo:
    def __init__(self,aid):
        self.aid=aid
        self._quotes={}

    def add_quote(self,quote,value):
        self._quotes[quote]=value

    def set_quotes(self,quotes):
        self._quotes=quotes

    def get_quotes(self):
        return self._quotes

    def get_quote(self,quote):
        try:
            return self._quotes[quote]
        except KeyError:
            return None


def get_agent_quotes(aid,session):
    try:
        schemaobj=session.get(schema.AgentQuoORM(key=aid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def set_agent_quotes(aid,quotes,session):
    agentquotes=AgentQuo(aid)
    agentquotes.set_quotes(quotes)
    try:
        if session.insert(schema.AgentQuoORM(apiobj=agentquotes)):
            return True
        else:
            return False
    except Exception:
        return False

def del_agent_quotes(aid,quotes,session):
    agentquotes=AgentQuo(aid)
    agentquotes.set_quotes(quotes)
    try:
        if session.remove(schema.AgentQuoORM(apiobj=agentquotes)):
            return True
        else:
            return False
    except Exception:
        return False

class DatasourceQuo:
    def __init__(self,did):
        self.did=did
        self._quotes={}

    def add_quote(self,quote,value):
        self._quotes[quote]=value

    def set_quotes(self,quotes):
        self._quotes=quotes

    def get_quotes(self):
        return self._quotes

    def get_quote(self,quote):
        try:
            return self._quotes[quote]
        except KeyError:
            return None

def get_ds_quotes(did,session):
    try:
        schemaobj=session.get(schema.DatasourceQuoORM(key=did))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def set_ds_quotes(did,quotes,session):
    dsquotes=DatasourceQuo(did)
    dsquotes.set_quotes(quotes)
    try:
        if session.insert(schema.DatasourceQuoORM(apiobj=dsquotes)):
            return True
        else:
            return False
    except Exception:
        return False

def del_ds_quotes(did,quotes,session):
    dsquotes=DatasourceQuo(did)
    dsquotes.set_quotes(quotes)
    try:
        if session.remove(schema.DatasourceQuoORM(apiobj=dsquotes)):
            return True
        else:
            return False
    except Exception:
        return False

class DatapointQuo:
    def __init__(self,pid):
        self.pid=pid
        self._quotes={}

    def add_quote(self,quote,value):
        self._quotes[quote]=value

    def set_quotes(self,quotes):
        self._quotes=quotes

    def get_quotes(self):
        return self._quotes

def get_dtp_quotes(pid,session):
    try:
        schemaobj=session.get(schema.DatapointQuoORM(key=pid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def set_dtp_quotes(pid,quotes,session):
    dtpquotes=DatapointQuo(pid)
    dtpquotes.set_quotes(quotes)
    try:
        if session.insert(schema.DatapointQuoORM(apiobj=dtpquotes)):
            return True
        else:
            return False
    except Exception:
        return False

def del_dtp_quotes(pid,quotes,session):
    dtpquotes=DatapointQuo(pid)
    dtpquotes.set_quotes(quotes)
    try:
        if session.remove(schema.DatapointQuoORM(apiobj=dtpquotes)):
            return True
        else:
            return False
    except Exception:
        return False

class GraphQuo:
    def __init__(self,gid):
        self.gid=gid
        self._quotes={}

    def add_quote(self,quote,value):
        self._quotes[quote]=value

    def set_quotes(self,quotes):
        self._quotes=quotes

    def get_quotes(self):
        return self._quotes

def get_graph_quotes(gid,session):
    try:
        schemaobj=session.get(schema.GraphQuoORM(key=gid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def set_graph_quotes(gid,quotes,session):
    graphquotes=GraphQuo(gid)
    graphquotes.set_quotes(quotes)
    try:
        if session.insert(schema.GraphQuoORM(apiobj=graphquotes)):
            return True
        else:
            return False
    except Exception:
        return False

def del_graph_quotes(gid,quotes,session):
    graphquotes=GraphQuo(gid)
    graphquotes.set_quotes(quotes)
    try:
        if session.remove(schema.GraphQuoORM(apiobj=graphquotes)):
            return True
        else:
            return False
    except Exception:
        return False

class UserAgentPerms:
    ''' This class is used to access User - Agent permission relation '''
    def __init__(self, uid):
        self.uid=uid
        self._aids={}

    def add_agent(self, aid, perm=u'A'):
        self._aids[aid]=perm #at first A means ALL ACCESS to the resource

    def get_agents(self, aid=None):
        try:
            return {aid:self._aids[aid]} if aid else self._aids
        except KeyError:
            return None

    def set_agents(self, aids=None):
        self._aids=aids if aids else {}

def get_useragentperms(uid,session,aid=None):
    try:
        kwargs={}
        if aid:
            kwargs['columns']=(aid,)
        schemaobj=session.get(schema.UserAgentPermsORM(key=uid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_useragentperms(uapobj,session):
    try:
        if session.insert(schema.UserAgentPermsORM(apiobj=uapobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_useragentperms(uapobj,session):
    try:
        kwargs={}
        agents=uapobj.get_agents()
        if agents and len(agents.keys())>0:
            kwargs['columns']=[key for key in agents.keys()]
        if session.remove(schema.UserAgentPermsORM(apiobj=uapobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class UserDsPerms:
    ''' This class is used to access User-Datasource permission relation '''
    def __init__(self, uid):
        self.uid=uid
        self._dids={}

    def add_ds(self, did, perm=u'A'):
        self._dids[did]=perm #at first A means ALL ACCESS to the resource

    def get_dss(self, did=None):
        try:
            return {did:self._dids[did]} if did else self._dids
        except KeyError:
            return None

    def set_dss(self, dids=None):
        self._dids=dids if dids else {}

def get_userdsperms(uid,session,did=None):
    try:
        kwargs={}
        if did:
            kwargs['columns']=(did,)
        schemaobj=session.get(schema.UserDsPermsORM(key=uid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_userdsperms(udpobj,session):
    try:
        if session.insert(schema.UserDsPermsORM(apiobj=udpobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_userdsperms(udpobj,session):
    try:
        kwargs={}
        dss=udpobj.get_dss()
        if dss and len(dss.keys())>0:
            kwargs['columns']=[key for key in dss.keys()]
        if session.remove(schema.UserDsPermsORM(apiobj=udpobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class UserDtpPerms:
    ''' This class is used to access User-Datapoint permission relation '''
    def __init__(self, uid):
        self.uid=uid
        self._pids={}

    def add_dtp(self, pid, perm=u'A'):
        self._pids[pid]=perm #at first A means ALL ACCESS to the resource

    def get_dtps(self, pid=None):
        try:
            return {pid:self._pids[pid]} if pid else self._pids
        except KeyError:
            return None

    def set_dtps(self, pids=None):
        self._pids=pids if pids else {}

def get_userdtpperms(uid,session,pid=None):
    try:
        kwargs={}
        if pid:
            kwargs['columns']=(pid,)
        schemaobj=session.get(schema.UserDtpPermsORM(key=uid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_userdtpperms(uppobj,session):
    try:
        if session.insert(schema.UserDtpPermsORM(apiobj=uppobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_userdtpperms(uppobj,session):
    try:
        kwargs={}
        dtps=uppobj.get_dtps()
        if dtps and len(dtps.keys())>0:
            kwargs['columns']=[key for key in dtps.keys()]
        if session.remove(schema.UserDtpPermsORM(apiobj=uppobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class UserGraphPerms:
    ''' This class is used to access User-Graph permission relation '''
    def __init__(self, uid):
        self.uid=uid
        self._gids={}

    def add_graph(self, gid, perm=u'A'):
        self._gids[gid]=perm #at first A means ALL ACCESS to the resource

    def get_graphs(self, gid=None):
        try:
            return {gid:self._gids[gid]} if gid else self._gids
        except KeyError:
            return None

    def set_graphs(self, gids=None):
        self._gids=gids if gids else {}

def get_usergraphperms(uid,session,gid=None):
    try:
        kwargs={}
        if gid:
            kwargs['columns']=(gid,)
        schemaobj=session.get(schema.UserGraphPermsORM(key=uid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_usergraphperms(ugpobj,session):
    try:
        if session.insert(schema.UserGraphPermsORM(apiobj=ugpobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_usergraphperms(ugpobj,session):
    try:
        kwargs={}
        graphs=ugpobj.get_graphs()
        if graphs and len(graphs.keys())>0:
            kwargs['columns']=[key for key in graphs.keys()]
        if session.remove(schema.UserGraphPermsORM(apiobj=ugpobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class AgentDsPerms:
    ''' This class is used to access Agent-Datasource permission relation '''
    def __init__(self, aid):
        self.aid=aid
        self._dids={}

    def add_ds(self, did, perm=u'A'):
        self._dids[did]=perm #at first A means ALL ACCESS to the resource

    def get_dss(self, did=None):
        try:
            return {did:self._dids[did]} if did else self._dids
        except KeyError:
            return None

    def set_dss(self, dids=None):
        self._dids=dids if dids else {}

def get_agentdsperms(aid,session,did=None):
    try:
        kwargs={}
        if did:
            kwargs['columns']=(did,)
        schemaobj=session.get(schema.AgentDsPermsORM(key=aid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_agentdsperms(adpobj,session):
    try:
        if session.insert(schema.AgentDsPermsORM(apiobj=adpobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_agentdsperms(adpobj,session):
    try:
        kwargs={}
        dss=adpobj.get_dss()
        if dss and len(dss.keys())>0:
            kwargs['columns']=[key for key in dss.keys()]
        if session.remove(schema.AgentDsPermsORM(apiobj=adpobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class AgentDtpPerms:
    ''' This class is used to access Agent-Datapoint permission relation '''
    def __init__(self, aid):
        self.aid=aid
        self._pids={}

    def add_dtp(self, pid, perm=u'A'):
        self._pids[pid]=perm #at first A means ALL ACCESS to the resource

    def get_dtps(self, pid=None):
        try:
            return {pid:self._pids[pid]} if pid else self._pids
        except KeyError:
            return None

    def set_dtps(self, pids=None):
        self._pids=pids if pids else {}

def get_agentdtpperms(aid,session,pid=None):
    try:
        kwargs={}
        if pid:
            kwargs['columns']=(pid,)
        schemaobj=session.get(schema.AgentDtpPermsORM(key=aid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_agentdtpperms(appobj,session):
    try:
        if session.insert(schema.AgentDtpPermsORM(apiobj=appobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_agentdtpperms(appobj,session):
    try:
        kwargs={}
        dtps=appobj.get_dtps()
        if dtps and len(dtps.keys())>0:
            kwargs['columns']=[key for key in dtps.keys()]
        if session.remove(schema.AgentDtpPermsORM(apiobj=appobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class AgentGraphPerms:
    ''' This class is used to access Agent-Graph permission relation '''
    def __init__(self, aid):
        self.aid=aid
        self._gids={}

    def add_graph(self, gid, perm=u'A'):
        self._gids[gid]=perm #at first A means ALL ACCESS to the resource

    def get_graphss(self, gid=None):
        try:
            return {gid:self._gids[gid]} if gid else self._gids
        except KeyError:
            return None

    def set_graphs(self, gids=None):
        self._gids=gids if gids else {}

def get_agentgraphperms(aid,session,gid=None):
    try:
        kwargs={}
        if gid:
            kwargs['columns']=(gid,)
        schemaobj=session.get(schema.AgentGraphPermsORM(key=aid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_agentgraphperms(agpobj,session):
    try:
        if session.insert(schema.AgentGraphPermsORM(apiobj=agpobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_agentgraphperms(agpobj,session):
    try:
        kwargs={}
        graphs=agpobj.get_graphs()
        if dtps and len(graphs.keys())>0:
            kwargs['columns']=[key for key in graphs.keys()]
        if session.remove(schema.AgentGraphPermsORM(apiobj=agpobj),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class UserIfaceDeny:
    ''' This class is used to register interfaces whose access is denied to user requests'''
    def __init__(self, uid):
        self.uid=uid
        self._ifaces={}

    def add_interface(self, iface, perm=u'A'):
        self._ifaces[iface]=perm #at first A means DENY ALL ACCESS to the interface

    def get_interfaces(self, iface=None):
        try:
            return {iface:self._ifaces[iface]} if iface else self._ifaces
        except KeyError:
            return None

    def set_interfaces(self, ifaces=None):
        self._ifaces=ifaces if ifaces else {}

def get_userifacedeny(uid,session,iface=None):
    try:
        kwargs={}
        if iface:
            kwargs['columns']=(iface,)
        schemaobj=session.get(schema.UserIfaceDenyORM(key=uid),kwargs)
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def insert_userifacedeny(uifdobj,session):
    try:
        if session.insert(schema.UserIfaceDenyORM(apiobj=uifdobj)):
            return True
        else:
            return False
    except Exception:
        return False

def delete_userifacedeny(uifdobj,session):
    try:
        kwargs={}
        columns=uifdobj.get_interfaces()
        if columns:
            kwargs['columns']=columns.keys()
        if session.remove(schema.UserIfaceDenyORM(key=uifdobj.uid),kwargs):
            return True
        else:
            return False
    except Exception:
        return False

class DatasourceCard:
    def __init__(self,did):
        self.did=did
        self.uid=None
        self.aid=None
        self.ag_name=None
        self.ds_name=None
        self.ds_date=None
        self.priority=None
        self._datapoints=[]
        self._graphs=[]
        self._anomalies=[]

    def get_datapoints(self):
        return self._datapoints

    def add_datapoint(self, dtp_name,dtp_value):
        dtp_pair=(dtp_name,str(dtp_value))
        self._datapoints.append(dtp_pair)
        self._datapoints=list(set(self._datapoints))

    def empty_datapoints(self):
        self._datapoints=[]

    def get_graphs(self):
        return self._graphs

    def add_graph(self, graph):
        self._graphs.append(graph)

    def empty_graphs(self):
        self._graphs=[]

    def get_anomalies(self):
        return self._anomalies

    def add_anomaly(self, dtp_name,message):
        dtp_pair=(dtp_name,message)
        self._anomalies.append(dtp_pair)
        self._anomalies=list(set(self._anomalies))
        
    def empty_anomalies(self):
        self._anomalies=[]

def get_datasourcecard(did,session):
    try:
        schemaobj=session.get(schema.DatasourceCardORM(key=did))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def delete_datasourcecard(did,session):
    if session.remove(schema.DatasourceCardORM(key=did)):
        return True
    return False

def insert_datasourcecard(datasourcecard,session):
    if not datasourcecard:
        return False
    if not session.insert(schema.DatasourceCardORM(apiobj=datasourcecard)):
        return False
    return True

class UserDsCard:
    def __init__(self,uid):
        self.uid=uid
        self._cards={}

    def get_cards(self):
        return self._cards

    def add_card(self, did, priority):
        self._cards[did]=priority
    
    def delete_card(self, did, priority):
        if self._cards.has_key(did) and self._cards[did]==priority:
            self._cards.pop(did)
        return True

def get_userdscard(uid,session):
    try:
        schemaobj=session.get(schema.UserDsCardORM(key=uid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def delete_userdscard(userdscard,session):
    if not userdscard:
        return False
    userdscardorm=schema.UserDsCardORM(apiobj=userdscard)
    kwargs={}
    kwargs['columns']=userdscardorm.dbdict.keys()
    if session.remove(userdscardorm,kwargs):
        return True
    return False

def insert_userdscard(userdscard,session):
    if not userdscard:
        return False
    if not session.insert(schema.UserDsCardORM(apiobj=userdscard)):
        return False
    return True

class AgentDsCard:
    def __init__(self,aid):
        self.aid=aid
        self._cards={}

    def get_cards(self):
        return self._cards

    def add_card(self, did, priority):
        self._cards[did]=priority

    def delete_card(self, did, priority):
        if self._cards.has_key(did) and self._cards[did]==priority:
            self._cards.pop(did)
        return True

def get_agentdscard(aid,session):
    try:
        schemaobj=session.get(schema.AgentDsCardORM(key=aid))
        return schemaobj.to_apiobj()
    except NotFoundException:
        return None

def delete_agentdscard(agentdscard,session):
    if not agentdscard:
        return False
    agentdscardorm=schema.AgentDsCardORM(apiobj=agentdscard)
    kwargs={}
    kwargs['columns']=agentdscardorm.dbdict.keys()
    if session.remove(agentdscardorm,kwargs):
        return True
    return False

def insert_agentdscard(agentdscard,session):
    if not agentdscard:
        return False
    if not session.insert(schema.AgentDsCardORM(apiobj=agentdscard)):
        return False
    return True

