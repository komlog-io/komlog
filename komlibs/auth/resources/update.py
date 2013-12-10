#coding: utf-8
'''
update.py 

This file implements functions to update authorization to resources

@author: jcazor
@date: 2013/11/11

'''

from komcass import api as cassapi

def update_user_agent_perms(params,cf):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    useragentperms=cassapi.UserAgentPerms(uid)
    useragentperms.add_agent(aid)
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    if useragentr:
        if cassapi.insert_useragentperms(useragentperms,cf):
            return True
    return False

def update_user_ds_perms(params,cf):
    if not params.has_key('did') or not params.has_key('uid') or not params.has_key('aid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    userdsperms=cassapi.UserDsPerms(uid)
    userdsperms.add_ds(did)
    agentdsr=cassapi.get_agentdsrelation(aid,cf,dbcols={did:u''})
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    if agentdsr and useragentr:
        if cassapi.insert_userdsperms(userdsperms,cf):
            return True
    return False

def update_agent_ds_perms(params,cf):
    if not params.has_key('did') or not params.has_key('uid') or not params.has_key('aid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    agentdsperms=cassapi.AgentDsPerms(aid)
    agentdsperms.add_ds(did)
    agentdsr=cassapi.get_agentdsrelation(aid,cf,dbcols={did:u''})
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    if agentdsr and useragentr:
        if cassapi.insert_agentdsperms(agentdsperms,cf):
            return True
    return False

def update_user_dtp_perms(params,cf):
    if not params.has_key('did') or not params.has_key('uid') \
    or not params.has_key('aid') or not params.has_key('pid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    pid=params['pid']
    userdtpperms=cassapi.UserDtpPerms(uid)
    userdtpperms.add_dtp(pid)
    agentdsr=cassapi.get_agentdsrelation(aid,cf,dbcols={did:u''})
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    dsdtpr=cassapi.get_dsdtprelation(did,cf,dbcols={pid:u''})
    if agentdsr and useragentr and dsdtpr:
        if cassapi.insert_userdtpperms(userdtpperms,cf):
            return True
    return False

def update_user_graph_perms(params,cf):
    if not params.has_key('gid') or not params.has_key('uid'):
        return False
    gid=params['gid']
    uid=params['uid']
    usergraphperms=cassapi.UserGraphPerms(uid)
    usergraphperms.add_graph(gid)
    graphinfo=cassapi.get_graphinfo(gid,cf)
    if graphinfo and graphinfo.uid==uid:
        if cassapi.insert_usergraphperms(usergraphperms,cf):
            return True
    return False

