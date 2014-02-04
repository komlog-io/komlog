#coding:utf-8

'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komcass import api as cassapi

def authorize_get_agent_config(username,session,aid):
    if not aid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    useragentperms=cassapi.get_useragentperms(useruidr.uid,session,aid=aid)
    if useragentperm:
        return True
    else:
        return False

def authorize_get_ds_config(username,did,session):
    if not did:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    if userdsperms:
        return True
    else:
        return False

def authorize_put_ds_config(username,did,session):
    if not did:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    if userdsperms:
        return True
    else:
        return False

def authorize_get_ds_data(username,did,session):
    if not did:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did=did)
    if userdsperms:
        return True
    else:
        return False

def authorize_post_ds_data(username,aid,did,session):
    if not aid or not did:
        return False
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
    if not aid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    useragperms=cassapi.get_useragentperms(useruidr.uid,session,aid)
    if useragperms:
        return True
    else:
        return False
    return True

def authorize_get_dp_data(username,pid,session):
    if not pid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdtpperms=cassapi.get_userdtpperms(useruidr.uid,session,pid=pid)
    if userdtpperms:
        return True
    else:
        return False

def authorize_get_dp_config(username,pid,session):
    if not pid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdtpperms=cassapi.get_userdtpperms(useruidr.uid,session,pid=pid)
    if userdtpperms:
        return True
    else:
        return False

def authorize_put_dp_config(username,pid,session):
    if not pid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdtpperms=cassapi.get_userdtpperms(useruidr.uid,session,pid=pid)
    if userdtpperms:
        return True
    else:
        return False

def authorize_new_datapoint(username,did,session):
    if not did:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdsperms=cassapi.get_userdsperms(useruidr.uid,session,did)
    if userdsperms:
        return True
    else:
        return False
    return True

def authorize_new_graph(username,pid,session):
    if not pid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    userdtpperms=cassapi.get_userdtpperms(useruidr.uid,session,pid)
    if userdtpperms:
        return True
    else:
        return False
    return True

def authorize_get_graph_config(username,gid,session):
    if not gid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    usergraphperms=cassapi.get_usergraphperms(useruidr.uid,session,gid=gid)
    if usergraphperms:
        return True
    else:
        return False

def authorize_put_graph_config(username,gid,session):
    if not gid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    if not useruidr:
        raise exceptions.BadParametersException()
    usergraphperms=cassapi.get_usergraphperms(useruidr.uid,session,gid=gid)
    if usergraphperms:
        return True
    else:
        return False

def authorize_put_agent_config(username,aid,session):
    if not aid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    useragentperms=cassapi.get_useragentperms(useruidr.uid,session,aid=aid)
    if useragentperms:
        return True
    else:
        return False

def authorize_get_plot_data(username,gid,session):
    if not gid:
        return False
    useruidr=cassapi.get_useruidrelation(username,session)
    usergraphperms=cassapi.get_usergraphperms(useruidr.uid,session,gid=gid)
    if usergraphperms:
        return True
    else:
        return False

