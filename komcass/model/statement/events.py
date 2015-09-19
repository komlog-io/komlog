'''
This file contains the statements to operate with event tables
Statements range (150000-159999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
            150000:'select * from dat_user_events where uid=? and date=?',
            150001:'select * from dat_user_events where uid=? and date<=? order by date desc limit ?',
            150002:'select * from dat_user_events where uid=? and date<=? and date>=? order by date desc',
            150003:'select * from dat_user_events where uid=? and date>=? order by date desc',
            150004:'select * from dat_user_events_disabled where uid=? and date=?',
            150005:'select * from dat_user_events_disabled where uid=? and date<=? order by date desc limit ?',
            150006:'select * from dat_user_events_disabled where uid=? and date<=? and date>=? order by date desc',
            150007:'select * from dat_user_events_disabled where uid=? and date>=? order by date desc',
            150008:'select * from dat_ue_notif_new_user where uid=? and date=?',
            150009:'select * from dat_ue_notif_new_agent where uid=? and date=?',
            150010:'select * from dat_ue_notif_new_datasource where uid=? and date=?',
            150011:'select * from dat_ue_notif_new_datapoint where uid=? and date=?',
            150012:'select * from dat_ue_notif_new_widget where uid=? and date=?',
            150013:'select * from dat_ue_notif_new_dashboard where uid=? and date=?',
            150014:'select * from dat_ue_notif_new_circle where uid=? and date=?',
            150015:'select * from dat_ue_interv_dp_identification where uid=? and date=?',
            150016:'select * from dat_uer_interv_dp_identification where uid=? and date=?',
            150017:'select * from dat_uer_interv_dp_identification where uid=?',
            151000:'insert into dat_user_events (uid,date,priority,type) values (?,?,?,?)',
            151001:'insert into dat_user_events_disabled (uid,date,priority,type) values (?,?,?,?)',
            151002:'insert into dat_ue_notif_new_user (uid,date,username) values (?,?,?)',
            151003:'insert into dat_ue_notif_new_agent (uid,date,aid,agentname) values (?,?,?,?)',
            151004:'insert into dat_ue_notif_new_datasource (uid,date,aid,did,datasourcename) values (?,?,?,?,?)',
            151005:'insert into dat_ue_notif_new_datapoint (uid,date,did,pid,datasourcename,datapointname) values (?,?,?,?,?,?)',
            151006:'insert into dat_ue_notif_new_widget (uid,date,wid,widgetname) values (?,?,?,?)',
            151007:'insert into dat_ue_notif_new_dashboard (uid,date,bid,dashboardname) values (?,?,?,?)',
            151008:'insert into dat_ue_notif_new_circle (uid,date,cid,circlename) values (?,?,?,?)',
            151009:'insert into dat_ue_interv_dp_identification (uid,date,did,ds_date,doubts,discarded) values (?,?,?,?,?,?)',
            151010:'insert into dat_uer_interv_dp_identification (uid,date,response_date,missing,identified,not_belonging,to_update,update_failed,update_success) values (?,?,?,?,?,?,?,?,?)',
            152000:'delete from dat_user_events where uid=?',
            152001:'delete from dat_user_events where uid=? and date=?',
            152002:'delete from dat_user_events_disabled where uid=?',
            152003:'delete from dat_user_events_disabled where uid=? and date=?',
            152004:'delete from dat_ue_notif_new_user where uid=?',
            152005:'delete from dat_ue_notif_new_agent where uid=?',
            152006:'delete from dat_ue_notif_new_datasource where uid=?',
            152007:'delete from dat_ue_notif_new_datapoint where uid=?',
            152008:'delete from dat_ue_notif_new_widget where uid=?',
            152009:'delete from dat_ue_notif_new_dashboard where uid=?',
            152010:'delete from dat_ue_notif_new_circle where uid=?',
            152011:'delete from dat_ue_interv_dp_identification where uid=?',
            152012:'delete from dat_uer_interv_dp_identification where uid=? and date=?',
           }

# selects

S_A_DATUSEREVENTS_B_UID_DATE=150000
S_A_DATUSEREVENTS_B_UID_ENDDATE_COUNT=150001
S_A_DATUSEREVENTS_B_UID_ENDDATE_FROMDATE=150002
S_A_DATUSEREVENTS_B_UID_FROMDATE=150003
S_A_DATUSEREVENTSDISABLED_B_UID_DATE=150004
S_A_DATUSEREVENTSDISABLED_B_UID_ENDDATE_COUNT=150005
S_A_DATUSEREVENTSDISABLED_B_UID_ENDDATE_FROMDATE=150006
S_A_DATUSEREVENTSDISABLED_B_UID_FROMDATE=150007
S_A_DATUENOTIFNEWUSER_B_UID_DATE=150008
S_A_DATUENOTIFNEWAGENT_B_UID_DATE=150009
S_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE=150010
S_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE=150011
S_A_DATUENOTIFNEWWIDGET_B_UID_DATE=150012
S_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE=150013
S_A_DATUENOTIFNEWCIRCLE_B_UID_DATE=150014
S_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE=150015
S_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE=150016
S_A_DATUERINTERVDPIDENTIFICATION_B_UID=150017


# Inserts

I_A_DATUSEREVENTS=151000
I_A_DATUSEREVENTSDISABLED=151001
I_A_DATUENOTIFNEWUSER=151002
I_A_DATUENOTIFNEWAGENT=151003
I_A_DATUENOTIFNEWDATASOURCE=151004
I_A_DATUENOTIFNEWDATAPOINT=151005
I_A_DATUENOTIFNEWWIDGET=151006
I_A_DATUENOTIFNEWDASHBOARD=151007
I_A_DATUENOTIFNEWCIRCLE=151008
I_A_DATUEINTERVDPIDENTIFICATION=151009
I_A_DATUERINTERVDPIDENTIFICATION=151010

# Deletes

D_A_DATUSEREVENTS_B_UID=152000
D_A_DATUSEREVENTS_B_UID_DATE=152001
D_A_DATUSEREVENTSDISABLED_B_UID=152002
D_A_DATUSEREVENTSDISABLED_B_UID_DATE=152003
D_A_DATUENOTIFNEWUSER_B_UID=152004
D_A_DATUENOTIFNEWAGENT_B_UID=152005
D_A_DATUENOTIFNEWDATASOURCE_B_UID=152006
D_A_DATUENOTIFNEWDATAPOINT_B_UID=152007
D_A_DATUENOTIFNEWWIDGET_B_UID=152008
D_A_DATUENOTIFNEWDASHBOARD_B_UID=152009
D_A_DATUENOTIFNEWCIRCLE_B_UID=152010
D_A_DATUEINTERVDPIDENTIFICATION_B_UID=152011
D_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE=152012


