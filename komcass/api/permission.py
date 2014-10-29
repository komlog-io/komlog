#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import permission as ormperm
from komcass.model.statement import permission as stmtperm
from komcass.exception import permission as excpperm


def get_user_agent_perm(session, uid, aid):
    row=session.execute(stmtperm.S_A_PERMUSERAGENT_B_UID_AID,(uid,aid))
    if not row:
        return None
    elif len(row)==1:
        return ormperm.UserAgentPerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_useragentperm',field='aid',value=aid)

def get_user_agents_perm(session, uid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMUSERAGENT_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserAgentPerm(**perm))
    return perms

def insert_user_agent_perm(session, uid, aid, perm):
    session.execute(stmtperm.I_A_PERMUSERAGENT,(uid,aid,perm))
    return True

def delete_user_agent_perm(session, uid, aid):
    session.execute(stmtperm.D_P_PERMUSERAGENT_B_UID_AID,(uid,aid))
    return True

def delete_user_agents_perm(session, uid):
    session.execute(stmtperm.D_P_PERMUSERAGENT_B_UID,(uid,))
    return True

def get_user_datasource_perm(session, uid, did):
    row=session.execute(stmtperm.S_A_PERMUSERDATASOURCE_B_UID_DID,(uid,did))
    if not row:
        return None
    elif len(row)==1:
        return ormperm.UserDatasourcePerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_userdatasourceperm',field='did',value=did)

def get_user_datasources_perm(session, uid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMUSERDATASOURCE_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserDatasourcePerm(**perm))
    return perms

def insert_user_datasource_perm(session, uid, did, perm):
    session.execute(stmtperm.I_A_PERMUSERDATASOURCE,(uid,did,perm))
    return True

def delete_user_datasource_perm(session, uid, did):
    session.execute(stmtperm.D_P_PERMUSERDATASOURCE_B_UID_DID,(uid,did))
    return True

def delete_user_datasources_perm(session, uid):
    session.execute(stmtperm.D_P_PERMUSERDATASOURCE_B_UID,(uid,))
    return True

def get_user_datapoint_perm(session, uid, pid):
    row=session.execute(stmtperm.S_A_PERMUSERDATAPOINT_B_UID_PID,(uid,pid))
    if not row:
        return None
    elif len(row)==1:
        return ormperm.UserDatapointPerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_userdatapointperm',field='pid',value=pid)

def get_user_datapoints_perm(session, uid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMUSERDATAPOINT_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserDatapointPerm(**perm))
    return perms

def insert_user_datapoint_perm(session, uid, pid, perm):
    session.execute(stmtperm.I_A_PERMUSERDATAPOINT,(uid,pid,perm))
    return True

def delete_user_datapoint_perm(session, uid, pid):
    session.execute(stmtperm.D_P_PERMUSERDATAPOINT_B_UID_PID,(uid,pid))
    return True

def delete_user_datapoints_perm(session, uid):
    session.execute(stmtperm.D_P_PERMUSERDATAPOINT_B_UID,(uid,))
    return True

def get_user_widget_perm(session, uid, wid):
    row=session.execute(stmtperm.S_A_PERMUSERWIDGET_B_UID_WID,(uid,wid))
    if not row:
        return None
    elif len(row)==1:
        return ormperm.UserWidgetPerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_userwidgetperm',field='wid',value=wid)

def get_user_widgets_perm(session, uid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMUSERWIDGET_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserWidgetPerm(**perm))
    return perms

def insert_user_widget_perm(session, uid, wid, perm):
    session.execute(stmtperm.I_A_PERMUSERWIDGET,(uid,wid,perm))
    return True

def delete_user_widget_perm(session, uid, wid):
    session.execute(stmtperm.D_P_PERMUSERWIDGET_B_UID_WID,(uid,wid))
    return True

def delete_user_widgets_perm(session, uid):
    session.execute(stmtperm.D_P_PERMUSERWIDGET_B_UID,(uid,))
    return True

def get_user_dashboard_perm(session, uid, bid):
    row=session.execute(stmtperm.S_A_PERMUSERDASHBOARD_B_UID_BID,(uid,bid))
    if not row:
        return None
    elif len(row)==1:
        return ormperm.UserDashboardPerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_userdashboardperm',field='bid',value=bid)

def get_user_dashboards_perm(session, uid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMUSERDASHBOARD_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserDashboardPerm(**perm))
    return perms

def insert_user_dashboard_perm(session, uid, bid, perm):
    session.execute(stmtperm.I_A_PERMUSERDASHBOARD,(uid,bid,perm))
    return True

def delete_user_dashboard_perm(session, uid, bid):
    session.execute(stmtperm.D_P_PERMUSERDASHBOARD_B_UID_BID,(uid,bid))
    return True

def delete_user_dashboards_perm(session, uid):
    session.execute(stmtperm.D_P_PERMUSERDASHBOARD_B_UID,(uid,))
    return True

def get_agent_datasource_perm(session, aid, did):
    row=session.execute(stmtperm.S_A_PERMAGENTDATASOURCE_B_AID_DID,(aid,did))
    if not row:
        return None
    elif len(row)==1:
        return ormperm.AgentDatasourcePerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_agentdatasourceperm',field='did',value=did)

def get_agent_datasources_perm(session, aid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMAGENTDATASOURCE_B_AID,(aid,))
    if row:
        for perm in row:
            perms.append(ormperm.AgentDatasourcePerm(**perm))
    return perms

def insert_agent_datasource_perm(session, aid, did, perm):
    session.execute(stmtperm.I_A_PERMAGENTDATASOURCE,(aid,did,perm))
    return True

def delete_agent_datasource_perm(session, aid, did):
    session.execute(stmtperm.D_P_PERMAGENTDATASOURCE_B_AID_DID,(aid,did))
    return True

def delete_agent_datasources_perm(session, aid):
    session.execute(stmtperm.D_P_PERMAGENTDATASOURCE_B_AID,(aid,))
    return True

def get_agent_datapoint_perm(session, aid, pid):
    row=session.execute(stmtperm.S_A_PERMAGENTDATAPOINT_B_AID_PID,(aid,pid))
    if not row:
        return None
    if len(row)==1:
        return ormperm.AgentDatapointPerm(**row[0])
    else:
        raise excpperm.DataConsistencyException(function='get_agentdatapointperm',field='pid',value=pid)

def get_agent_datapoints_perm(session, aid):
    perms=[]
    row=session.execute(stmtperm.S_A_PERMAGENTDATAPOINT_B_AID,(aid,))
    if row:
        for perm in row:
            perms.append(ormperm.AgentDatapointPerm(**perm))
    return perms

def insert_agent_datapoint_perm(session, aid, pid, perm):
    session.execute(stmtperm.I_A_PERMAGENTDATAPOINT,(aid,pid,perm))
    return True

def delete_agent_datapoint_perm(session, aid, pid):
    session.execute(stmtperm.D_P_PERMAGENTDATAPOINT_B_AID_PID,(aid,pid))
    return True

def delete_agent_datapoints_perm(session, aid):
    session.execute(stmtperm.D_P_PERMAGENTDATAPOINT_B_AID,(aid,))
    return True

