#coding: utf-8
###############################################################################
# update.py 
# 
# This file implements functions to update quotes
#
# @author: jcazor
# @date: 01/10/2013
#
###############################################################################

from komcass import api as cassapi

def update_quo_static_user_total_agents(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    uidagentr=cassapi.get_useragentrelation(uid,cf)
    if uidagentr:
        num_agents=str(len(uidagentr.aids)) #str because always quote values will be strings
        if cassapi.set_user_quotes(uid,{'quo_static_user_total_agents':num_agents},cf):
            return num_agents
    return None

def update_quo_static_user_total_graphs(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    uidagentr=cassapi.get_useragentrelation(uid,cf)
    if uidagentr:
        dtplist=[]
        graphlist=[]
        for aid in uidagentr.aids:
            agentdsr=cassapi.get_agentdsrelation(aid,cf)
            dslist=agentdsr.dids if agentdsr else []
            for ds in dslist:
                dsdtpr=cassapi.get_dsdtprelation(ds,cf)
                if dsdtpr:
                    for dtp in dsdtpr.dtps:
                        dtplist.append(dtp)
        print 'Lista de dtps:'
        print dtplist
        print type(dtplist)
        for dtp in dtplist:
            print 'Obteniendo lista de gráficos de:'
            print dtp
            dtpgraphsr=cassapi.get_datapointgraphrelation(dtp,cf)
            if dtpgraphsr:
                for gid in dtpgraphsr.gids:
                    graphlist.append(gid)
        print 'Lista de gráficos:'
        print graphlist 
        num_graphs=str(len(set(graphlist))) #str because always quote values will be strings
        if cassapi.set_user_quotes(uid,{'quo_static_user_total_graphs':num_graphs},cf):
            return num_graphs
    return None

def update_quo_static_user_total_datasources(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    uidagentr=cassapi.get_useragentrelation(uid,cf)
    if uidagentr:
        dslist=[]
        for aid in uidagentr.aids:
            agentdsr=cassapi.get_agentdsrelation(aid,cf)
            if agentdsr:
                for did in agentdsr.dids:
                    dslist.append(did)
        print 'Lista de ds:'
        print dslist
        num_ds=str(len(dslist)) #str because always quote values will be strings
        if cassapi.set_user_quotes(uid,{'quo_static_user_total_datasources':num_ds},cf):
            return num_ds
    return None

def update_quo_static_user_total_datapoints(params,cf):
    if not params.has_key('uid'):
        return None
    uid=params['uid']
    uidagentr=cassapi.get_useragentrelation(uid,cf)
    if uidagentr:
        dtplist=[]
        for aid in uidagentr.aids:
            agentdsr=cassapi.get_agentdsrelation(aid,cf)
            if agentdsr:
                for did in agentdsr.dids:
                    dsdtpr=cassapi.get_dsdtprelation(did,cf)
                    if dsdtpr:
                        for pid in dsdtpr.dtps:
                            dtplist.append(pid)
        print 'Lista de dtps:'
        print dtplist
        num_dtp=str(len(dtplist)) #str because always quote values will be strings
        if cassapi.set_user_quotes(uid,{'quo_static_user_total_datapoints':num_dtp},cf):
            return num_dtp
    return None

def update_quo_static_agent_total_datasources(params,cf):
    print 'Empezamos agent_tota_ds'
    if not params.has_key('aid'):
        return None
    aid=params['aid']
    print 'obtenemos la relacion con los ds'
    print aid
    agentdsr=cassapi.get_agentdsrelation(aid,cf)
    print agentdsr
    if agentdsr:
        print 'tenemos datos'
        dslist=[]
        for did in agentdsr.dids:
            dslist.append(did)
        print 'Lista de ds:'
        print dslist
        num_ds=str(len(dslist)) #str because always quote values will be strings
        if cassapi.set_agent_quotes(aid,{'quo_static_agent_total_datasources':num_ds},cf):
            return num_ds
    return None

def update_quo_static_agent_total_datapoints(params,cf):
    if not params.has_key('uid') or not params.has_key('aid'):
        return None
    uid=params['uid']
    aid=params['aid']
    dtplist=[]
    agentdsr=cassapi.get_agentdsrelation(aid,cf)
    if agentdsr:
        for did in agentdsr.dids:
            dsdtpr=cassapi.get_dsdtprelation(did,cf)
            if dsdtpr:
                for pid in dsdtpr.dtps:
                    dtplist.append(pid)
    print 'Lista de dtps:'
    print dtplist
    num_dtp=str(len(dtplist)) #str because always quote values will be strings
    if cassapi.set_agent_quotes(aid,{'quo_static_agent_total_datapoints':num_dtp},cf):
        return num_dtp
    return None

def update_quo_static_ds_total_datapoints(params,cf):
    if not params.has_key('did'):
        return None
    did=params['did']
    dtplist=[]
    dsdtpr=cassapi.get_dsdtprelation(did,cf)
    if dsdtpr:
        for pid in dsdtpr.dtps:
            dtplist.append(pid)
    print 'Lista de dtps:'
    print dtplist
    num_dtp=str(len(dtplist)) #str because always quote values will be strings
    if cassapi.set_ds_quotes(did,{'quo_static_ds_total_datapoints':num_dtp},cf):
        return num_dtp
    return None

def resauth_update_user_agent_perms(params,cf):
    if not params.has_key('aid') or not params.has_key('uid'):
        return False
    aid=params['aid']
    uid=params['uid']
    useragentperms=cassapi.UserAgentPerms(uid).add_agent(aid)
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    if useragentr:
        if cassapi.insert_useragentperms(useragentperms,cf):
            return True
    return False

def resauth_update_user_ds_perms(params,cf):
    if not params.has_key('did') or not params.has_key('uid') or not params.has_key('aid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    userdsperms=cassapi.UserDsPerms(uid).add_ds(did)
    agentdsr=cassapi.get_agentdsrelation(aid,cf,dbcols={did:u''})
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    if agentdsr and useragentr:
        if cassapi.insert_userdsperms(userdsperms,cf):
                    return True
    return False

def resauth_update_agent_ds_perms(params,cf):
    if not params.has_key('did') or not params.has_key('uid') or not params.has_key('aid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    agentdsperms=cassapi.AgentDsPerms(aid).add_ds(did)
    agentdsr=cassapi.get_agentdsrelation(aid,cf,dbcols={did:u''})
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    if agentdsr and useragentr:
        if cassapi.insert_agentdsperms(agentdsperms,cf):
                    return True
    return False

def resauth_update_user_dtp_perms(params,cf):
    if not params.has_key('did') or not params.has_key('uid') \
    or not params.has_key('aid') or not params.has_key('pid'):
        return False
    did=params['did']
    uid=params['uid']
    aid=params['aid']
    pid=params['pid']
    userdtpperms=cassapi.UserDtpPerms(uid).add_dtp(pid)
    agentdsr=cassapi.get_agentdsrelation(aid,cf,dbcols={did:u''})
    useragentr=cassapi.get_useragentrelation(uid,cf,dbcols={aid:u''})
    dsdtpr=cassapi.get_dsdtprelation(did,cf,dbcols={pid:u''})
    if agentdsr and useragentr and dsdtpr:
        if cassapi.insert_userdtpperms(userdtpperms,cf):
            return True
    return False

def resauth_update_user_graph_perms(params,cf):
    if not params.has_key('gid') or not params.has_key('uid'):
        return False
    gid=params['gid']
    uid=params['uid']
    graphinfo=cassapi.get_graphinfo(gid,cf,dbcols={'uid':u''})
    if graphinfo and graphinfo.uid==uid:
        if cassapi.insert_usergraphperms(usergraphperms,cf):
            return True
    return False

