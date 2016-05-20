'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import permission as ormperm
from komlog.komcass.model.statement import permission as stmtperm
from komlog.komcass import connection, exceptions

@exceptions.ExceptionHandler
def get_user_agent_perm(uid, aid):
    row=connection.session.execute(stmtperm.S_A_PERMUSERAGENT_B_UID_AID,(uid,aid))
    if not row:
        return None
    else:
        return ormperm.UserAgentPerm(**row[0])

@exceptions.ExceptionHandler
def get_user_agents_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERAGENT_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserAgentPerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_agent_perm(uid, aid, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERAGENT,(uid,aid,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_agent_perm(uid, aid):
    connection.session.execute(stmtperm.D_P_PERMUSERAGENT_B_UID_AID,(uid,aid))
    return True

@exceptions.ExceptionHandler
def delete_user_agents_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERAGENT_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_datasource_perm(uid, did):
    row=connection.session.execute(stmtperm.S_A_PERMUSERDATASOURCE_B_UID_DID,(uid,did))
    if not row:
        return None
    else:
        return ormperm.UserDatasourcePerm(**row[0])

@exceptions.ExceptionHandler
def get_user_datasources_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERDATASOURCE_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserDatasourcePerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_datasource_perm(uid, did, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERDATASOURCE,(uid,did,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_datasource_perm(uid, did):
    connection.session.execute(stmtperm.D_P_PERMUSERDATASOURCE_B_UID_DID,(uid,did))
    return True

@exceptions.ExceptionHandler
def delete_user_datasources_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERDATASOURCE_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_datapoint_perm(uid, pid):
    row=connection.session.execute(stmtperm.S_A_PERMUSERDATAPOINT_B_UID_PID,(uid,pid))
    if not row:
        return None
    else:
        return ormperm.UserDatapointPerm(**row[0])

@exceptions.ExceptionHandler
def get_user_datapoints_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERDATAPOINT_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserDatapointPerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_datapoint_perm(uid, pid, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERDATAPOINT,(uid,pid,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_datapoint_perm(uid, pid):
    connection.session.execute(stmtperm.D_P_PERMUSERDATAPOINT_B_UID_PID,(uid,pid))
    return True

@exceptions.ExceptionHandler
def delete_user_datapoints_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERDATAPOINT_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_widget_perm(uid, wid):
    row=connection.session.execute(stmtperm.S_A_PERMUSERWIDGET_B_UID_WID,(uid,wid))
    if not row:
        return None
    else:
        return ormperm.UserWidgetPerm(**row[0])

@exceptions.ExceptionHandler
def get_user_widgets_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERWIDGET_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserWidgetPerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_widget_perm(uid, wid, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERWIDGET,(uid,wid,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_widget_perm(uid, wid):
    connection.session.execute(stmtperm.D_P_PERMUSERWIDGET_B_UID_WID,(uid,wid))
    return True

@exceptions.ExceptionHandler
def delete_user_widgets_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERWIDGET_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_dashboard_perm(uid, bid):
    row=connection.session.execute(stmtperm.S_A_PERMUSERDASHBOARD_B_UID_BID,(uid,bid))
    if not row:
        return None
    else:
        return ormperm.UserDashboardPerm(**row[0])

@exceptions.ExceptionHandler
def get_user_dashboards_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERDASHBOARD_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserDashboardPerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_dashboard_perm(uid, bid, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERDASHBOARD,(uid,bid,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_dashboard_perm(uid, bid):
    connection.session.execute(stmtperm.D_P_PERMUSERDASHBOARD_B_UID_BID,(uid,bid))
    return True

@exceptions.ExceptionHandler
def delete_user_dashboards_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERDASHBOARD_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_snapshot_perm(uid, nid):
    row=connection.session.execute(stmtperm.S_A_PERMUSERSNAPSHOT_B_UID_NID,(uid,nid))
    return ormperm.UserSnapshotPerm(**row[0]) if row else None

@exceptions.ExceptionHandler
def get_user_snapshots_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERSNAPSHOT_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserSnapshotPerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_snapshot_perm(uid, nid, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERSNAPSHOT,(uid,nid,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_snapshot_perm(uid, nid):
    connection.session.execute(stmtperm.D_P_PERMUSERSNAPSHOT_B_UID_NID,(uid,nid))
    return True

@exceptions.ExceptionHandler
def delete_user_snapshots_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERSNAPSHOT_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_user_circle_perm(uid, cid):
    row=connection.session.execute(stmtperm.S_A_PERMUSERCIRCLE_B_UID_CID,(uid,cid))
    return ormperm.UserCirclePerm(**row[0]) if row else None

@exceptions.ExceptionHandler
def get_user_circles_perm(uid):
    perms=[]
    row=connection.session.execute(stmtperm.S_A_PERMUSERCIRCLE_B_UID,(uid,))
    if row:
        for perm in row:
            perms.append(ormperm.UserCirclePerm(**perm))
    return perms

@exceptions.ExceptionHandler
def insert_user_circle_perm(uid, cid, perm):
    connection.session.execute(stmtperm.I_A_PERMUSERCIRCLE,(uid,cid,perm))
    return True

@exceptions.ExceptionHandler
def delete_user_circle_perm(uid, cid):
    connection.session.execute(stmtperm.D_P_PERMUSERCIRCLE_B_UID_CID,(uid,cid))
    return True

@exceptions.ExceptionHandler
def delete_user_circles_perm(uid):
    connection.session.execute(stmtperm.D_P_PERMUSERCIRCLE_B_UID,(uid,))
    return True

