#coding:utf-8

'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komcass.api import permission as cassapiperm

def authorize_get_agent_config(user,aid):
    permission=cassapiperm.get_user_agent_perm(uid=user.uid,aid=aid)
    return True if permission else False

def authorize_get_datasource_config(user,did):
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    return True if permission else False

def authorize_put_datasource_config(user,did):
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    return True if permission else False

def authorize_get_datasource_data(user,did):
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    return True if permission else False

def authorize_post_datasource_data(user,aid,did):
    user_datasource_perm=cassapiperm.get_user_datasource_perm(uid=user.uid,did=did)
    user_agent_perm=cassapiperm.get_user_agent_perm(uid=user.uid, aid=aid)
    agent_datasource_perm=cassapiperm.get_agent_datasource_perm(aid=aid, did=did)
    return True if user_datasource_perm and user_agent_perm and agent_datasource_perm else False

def authorize_new_agent(user):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_new_datasource(user,aid):
    permission=cassapiperm.get_user_agent_perm(uid=user.uid, aid=aid)
    return True if permission else False

def authorize_get_datapoint_data(user,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=user.uid, pid=pid)
    return True if permission else False

def authorize_get_datapoint_config(user,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=user.uid, pid=pid)
    return True if permission else False

def authorize_put_datapoint_config(user,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=user.uid, pid=pid)
    return True if permission else False

def authorize_new_datapoint(user,did):
    permission=cassapiperm.get_user_datasource_perm(uid=user.uid, did=did)
    return True if permission else False

def authorize_put_agent_config(user,aid):
    permission=cassapiperm.get_user_agent_perm(uid=user.uid, aid=aid)
    return True if permission else False

def authorize_new_widget(user):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_get_widget_config(user,wid):
    permission=cassapiperm.get_user_widget_perm(uid=user.uid, wid=wid)
    return True if permission else False

def authorize_put_widget_config(user,wid):
    permission=cassapiperm.get_user_widget_perm(uid=user.uid, wid=wid)
    return True if permission else False

def authorize_new_dashboard(user):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_get_dashboard_config(user,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=user.uid, bid=bid)
    return True if permission else False

def authorize_put_dashboard_config(user,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=user.uid, bid=bid)
    return True if permission else False

