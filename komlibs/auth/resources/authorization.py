#coding:utf-8

'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komlibs.auth import permissions
from komcass.api import permission as cassapiperm

def authorize_get_agent_config(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid,aid=aid)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_get_datasource_config(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_put_datasource_config(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_get_datasource_data(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_post_datasource_data(uid,aid,did):
    user_datasource_perm=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    user_agent_perm=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    agent_datasource_perm=cassapiperm.get_agent_datasource_perm(aid=aid, did=did)
    return True if user_datasource_perm and user_agent_perm and agent_datasource_perm \
    and user_datasource_perm.perm & permissions.CAN_EDIT \
    and user_agent_perm.perm & permissions.CAN_EDIT \
    and agent_datasource_perm.perm & permissions.CAN_EDIT else False

def authorize_new_agent(uid):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_new_datasource(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_get_datapoint_data(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_get_datapoint_config(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_put_datapoint_config(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_new_datapoint(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_put_agent_config(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_new_widget(uid):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_get_widget_config(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_put_widget_config(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_new_dashboard(uid):
    ''' Resource authorization not needed in this request '''
    return True

def authorize_get_dashboard_config(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    return True if permission and permission.perm & permissions.CAN_READ else False

def authorize_put_dashboard_config(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_mark_positive_variable(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_mark_negative_variable(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if permission and permission.perm & permissions.CAN_EDIT else False

def authorize_add_widget_to_dashboard(uid,bid,wid):
    dbperm=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    wgperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    return True if dbperm and dbperm.perm & permissions.CAN_EDIT and wgperm and wgperm.perm & permissions.CAN_READ else False

def authorize_delete_widget_from_dashboard(uid,bid):
    dbperm=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    return True if dbperm and dbperm.perm & permissions.CAN_EDIT else False

def authorize_delete_agent(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    return True if permission and permission.perm & permissions.CAN_DELETE else False

def authorize_delete_datasource(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    return True if permission and permission.perm & permissions.CAN_DELETE else False

def authorize_delete_datapoint(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if permission and permission.perm & permissions.CAN_DELETE else False

def authorize_delete_widget(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    return True if permission and permission.perm & permissions.CAN_DELETE else False

def authorize_delete_dashboard(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    return True if permission and permission.perm & permissions.CAN_DELETE else False

def authorize_add_datapoint_to_widget(uid, pid, wid):
    uwperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    upperm=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    return True if uwperm and uwperm.perm & permissions.CAN_EDIT and upperm and upperm.perm & permissions.CAN_READ else False

def authorize_delete_datapoint_from_widget(uid, wid):
    uwperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    return True if uwperm and uwperm.perm & permissions.CAN_EDIT else False

def authorize_new_snapshot(uid,wid):
    ''' check that user has permission over widget '''
    uwperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    return True if uwperm and uwperm.perm & permissions.CAN_SNAPSHOT else False

def authorize_get_snapshot_data(uid,nid):
    uperm=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if uperm and uperm.perm & permissions.CAN_READ:
        return True
    return False

def authorize_get_snapshot_config(uid,nid):
    uperm=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if uperm and uperm.perm & permissions.CAN_READ:
        return True
    return False

def authorize_delete_snapshot(uid,nid):
    uperm=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if uperm and uperm.perm & permissions.CAN_DELETE:
        return True
    return False

def authorize_get_circle_config(uid,cid):
    uperm=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if uperm and uperm.perm & permissions.CAN_READ:
        return True
    return False

def authorize_delete_circle(uid,cid):
    uperm=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if uperm and uperm.perm & permissions.CAN_DELETE:
        return True
    return False

def authorize_update_circle_config(uid,cid):
    uperm=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    return True if uperm and uperm.perm & permissions.CAN_EDIT else False

def authorize_add_member_to_circle(uid,cid):
    uperm=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    return True if uperm and uperm.perm & permissions.CAN_EDIT else False

def authorize_delete_member_from_circle(uid,cid):
    uperm=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    return True if uperm and uperm.perm & permissions.CAN_EDIT else False

