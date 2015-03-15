#coding: utf-8
'''
This file contains the statements to operate with permission tables
Statements range (80000-89999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={80000:'select * from perm_user_agent where uid=?',
            80001:'select * from perm_user_agent where uid=? and aid=?',
            80002:'select * from perm_user_datasource where uid=?',
            80003:'select * from perm_user_datasource where uid=? and did=?',
            80004:'select * from perm_user_datapoint where uid=?',
            80005:'select * from perm_user_datapoint where uid=? and pid=?',
            80006:'select * from perm_user_widget where uid=?',
            80007:'select * from perm_user_widget where uid=? and wid=?',
            80008:'select * from perm_user_dashboard where uid=?',
            80009:'select * from perm_user_dashboard where uid=? and bid=?',
            80010:'select * from perm_agent_datasource where aid=?',
            80011:'select * from perm_agent_datasource where aid=? and did=?',
            80012:'select * from perm_agent_datapoint where aid=?',
            80013:'select * from perm_agent_datapoint where aid=? and pid=?',
            80014:'select * from perm_user_snapshot where uid=?',
            80015:'select * from perm_user_snapshot where uid=? and nid=?',
            80016:'select * from perm_user_circle where uid=?',
            80017:'select * from perm_user_circle where uid=? and cid=?',
            81000:'insert into perm_user_agent (uid,aid,perm) values (?,?,?)',
            81001:'insert into perm_user_datasource (uid,did,perm) values (?,?,?)',
            81002:'insert into perm_user_datapoint (uid,pid,perm) values (?,?,?)',
            81003:'insert into perm_user_widget (uid,wid,perm) values (?,?,?)',
            81004:'insert into perm_user_dashboard (uid,bid,perm) values (?,?,?)',
            81005:'insert into perm_agent_datasource (aid,did,perm) values (?,?,?)',
            81006:'insert into perm_agent_datapoint (aid,pid,perm) values (?,?,?)',
            81007:'insert into perm_user_snapshot (uid,nid,perm) values (?,?,?)',
            81008:'insert into perm_user_circle (uid,cid,perm) values (?,?,?)',
            82000:'delete from perm_user_agent where uid=?',
            82001:'delete from perm_user_agent where uid=? and aid=?',
            82002:'delete from perm_user_datasource where uid=?',
            82003:'delete from perm_user_datasource where uid=? and did=?',
            82004:'delete from perm_user_datapoint where uid=?',
            82005:'delete from perm_user_datapoint where uid=? and pid=?',
            82006:'delete from perm_user_widget where uid=?',
            82007:'delete from perm_user_widget where uid=? and wid=?',
            82008:'delete from perm_user_dashboard where uid=?',
            82009:'delete from perm_user_dashboard where uid=? and bid=?',
            82010:'delete from perm_agent_datasource where aid=?',
            82011:'delete from perm_agent_datasource where aid=? and did=?',
            82012:'delete from perm_agent_datapoint where aid=?',
            82013:'delete from perm_agent_datapoint where aid=? and pid=?',
            82014:'delete from perm_user_snapshot where uid=?',
            82015:'delete from perm_user_snapshot where uid=? and nid=?',
            82016:'delete from perm_user_circle where uid=?',
            82017:'delete from perm_user_circle where uid=? and cid=?',
           }

# selects

S_A_PERMUSERAGENT_B_UID=80000
S_A_PERMUSERAGENT_B_UID_AID=80001
S_A_PERMUSERDATASOURCE_B_UID=80002
S_A_PERMUSERDATASOURCE_B_UID_DID=80003
S_A_PERMUSERDATAPOINT_B_UID=80004
S_A_PERMUSERDATAPOINT_B_UID_PID=80005
S_A_PERMUSERWIDGET_B_UID=80006
S_A_PERMUSERWIDGET_B_UID_WID=80007
S_A_PERMUSERDASHBOARD_B_UID=80008
S_A_PERMUSERDASHBOARD_B_UID_BID=80009
S_A_PERMAGENTDATASOURCE_B_AID=80010
S_A_PERMAGENTDATASOURCE_B_AID_DID=80011
S_A_PERMAGENTDATAPOINT_B_AID=80012
S_A_PERMAGENTDATAPOINT_B_AID_PID=80013
S_A_PERMUSERSNAPSHOT_B_UID=80014
S_A_PERMUSERSNAPSHOT_B_UID_NID=80015
S_A_PERMUSERCIRCLE_B_UID=80016
S_A_PERMUSERCIRCLE_B_UID_CID=80017

# Inserts

I_A_PERMUSERAGENT=81000
I_A_PERMUSERDATASOURCE=81001
I_A_PERMUSERDATAPOINT=81002
I_A_PERMUSERWIDGET=81003
I_A_PERMUSERDASHBOARD=81004
I_A_PERMAGENTDATASOURCE=81005
I_A_PERMAGENTDATAPOINT=81006
I_A_PERMUSERSNAPSHOT=81007
I_A_PERMUSERCIRCLE=81008

# Deletes

D_P_PERMUSERAGENT_B_UID=82000
D_P_PERMUSERAGENT_B_UID_AID=82001
D_P_PERMUSERDATASOURCE_B_UID=82002
D_P_PERMUSERDATASOURCE_B_UID_DID=82003
D_P_PERMUSERDATAPOINT_B_UID=82004
D_P_PERMUSERDATAPOINT_B_UID_PID=82005
D_P_PERMUSERWIDGET_B_UID=82006
D_P_PERMUSERWIDGET_B_UID_WID=82007
D_P_PERMUSERDASHBOARD_B_UID=82008
D_P_PERMUSERDASHBOARD_B_UID_BID=82009
D_P_PERMAGENTDATASOURCE_B_AID=82010
D_P_PERMAGENTDATASOURCE_B_AID_DID=82011
D_P_PERMAGENTDATAPOINT_B_AID=82012
D_P_PERMAGENTDATAPOINT_B_AID_PID=82013
D_P_PERMUSERSNAPSHOT_B_UID=82014
D_P_PERMUSERSNAPSHOT_B_UID_NID=82015
D_P_PERMUSERCIRCLE_B_UID=82016
D_P_PERMUSERCIRCLE_B_UID_CID=82017

