#coding:utf-8

'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komcass.api import user as cassapiuser
from komcass.api import permission as cassapiperm

def authorize_get_agent_config(username,aid):
    if not aid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_agent_perm(uid=user.uid,aid=aid)
    if permission:
        return True
    else:
        return False

def authorize_get_datasource_config(username,did):
    if not did:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    if permission:
        return True
    else:
        return False

def authorize_put_datasource_config(username,did):
    if not did:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    if permission:
        return True
    else:
        return False

def authorize_get_datasource_data(username,did):
    if not did:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    if permission:
        return True
    else:
        return False

def authorize_post_datasource_data(username,aid,did):
    if not aid or not did:
        return False
    user=cassapiuser.get_user(username=username)
    datasource_perm=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    agent_perm=cassapiperm.get_user_agent_perm(uid=user.uid, aid=aid)
    if agent_perm and datasource_perm:
        return True
    else:
        return False

def authorize_new_agent(username):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_new_datasource(username,aid):
    if not aid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_agent_perm(uid=user.uid, aid=aid)
    if permission:
        return True
    else:
        return False

def authorize_get_datapoint_data(username,pid):
    if not pid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datapoint_perm(uid=user.uid, pid=pid)
    if permission:
        return True
    else:
        return False

def authorize_get_datapoint_config(username,pid):
    if not pid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datapoint_perm(uid=user.uid, pid=pid)
    if permission:
        return True
    else:
        return False

def authorize_put_datapoint_config(username,pid):
    if not pid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datapoint_perm(uid=user.uid, pid=pid)
    if permission:
        return True
    else:
        return False

def authorize_new_datapoint(username,did):
    if not did:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid, did=did)
    if permission:
        return True
    else:
        return False

def authorize_put_agent_config(username,aid):
    if not aid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_agent_perm(uid=user.uid, aid=aid)
    if permission:
        return True
    else:
        return False

def authorize_new_widget(username):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_get_widget_config(username,wid):
    if not wid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_widget_perm(uid=user.uid, wid=wid)
    if permission:
        return True
    else:
        return False

def authorize_put_widget_config(username,wid):
    if not wid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_widget_perm(uid=user.uid, wid=wid)
    if permission:
        return True
    else:
        return False

def authorize_new_dashboard(username):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_get_dashboard_config(username,bid):
    if not bid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_dashboard_perm(uid=user.uid, bid=bid)
    if permission:
        return True
    else:
        return False

def authorize_put_dashboard_config(username,bid):
    if not bid:
        return False
    user=cassapiuser.get_user(username=username)
    permission=cassapiperm.get_user_dashboard_perm(uid=user.uid, bid=bid)
    if permission:
        return True
    else:
        return False

