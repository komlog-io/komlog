#coding:utf-8

'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komcass import api as cassapi

def authorize_get_agent_config(username,session,aid):
    useruidr=cassapi.get_useruidrelation(username,session)
    useragentperms=cassapi.get_useragentperms(useruidr.uid,session,aid=aid)
    if useragentperm:
        return True
    else:
        return False

def authorize_get_ds_config(username,did,session):
    print 'Authorizacion get_ds_config'
    useruidr=cassapi.get_useruidrelation(username,session)
    print 'useruidr sale'
    print useruidr.__dict__
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    print 'userdsperms sale'
    print userdsperms.__dict__
    if userdsperms:
        print 'devolvemos true'
        return True
    else:
        print 'devolvemos false'
        return False

def authorize_put_ds_config(username,did,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    if userdsperms:
        return True
    else:
        return False

def authorize_get_ds_data(username,did,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    if userdsperms:
        return True
    else:
        return False

def authorize_post_ds_data(username,aid,did,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    agentdsperms=cassapi.get_agentdsperms(aid,session,did=did)
    if userdsperms and agentdsperms:
        return True
    else:
        return False

def authorize_new_agent(username,session):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_new_datasource(username,aid,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    useragperms=cassapi.get_useragentperms(useruidr.uid,session,aid)
    if useragperms:
        return True
    else:
        return False
    return True

def authorize_get_dp_data(username,pid,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    userdtpperms=cassapi.get_userdtpperms(useruidr.uid,session,pid=pid)
    if userdtpperms:
        return True
    else:
        return False

def authorize_new_datapoint(username,did,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did)
    if userdsperms:
        return True
    else:
        return False
    return True

def authorize_new_graph(username,pid,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    userdtpperms=cassapi.get_userdtpperms(useruidr.uid,session,pid)
    if userdtpperms:
        return True
    else:
        return False
    return True

def authorize_get_graph_config(username,gid,session):
    useruidr=cassapi.get_useruidrelation(username,session)
    usergraphperms=cassapi.get_usergraphperms(useruidr.uid,session,gid=gid)
    if usergraphperms:
        return True
    else:
        return False

