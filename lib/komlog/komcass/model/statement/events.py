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
            150100:'select * from dat_user_events_disabled where uid=? and date=?',
            150101:'select * from dat_user_events_disabled where uid=? and date<=? order by date desc limit ?',
            150102:'select * from dat_user_events_disabled where uid=? and date<=? and date>=? order by date desc',
            150103:'select * from dat_user_events_disabled where uid=? and date>=? order by date desc',
            150150:'select * from dat_user_events_graph_summary where uid=? and date=?',
            150200:'select * from dat_ue_notif_new_user where uid=? and date=?',
            150300:'select * from dat_ue_notif_new_agent where uid=? and date=?',
            150400:'select * from dat_ue_notif_new_datasource where uid=? and date=?',
            150500:'select * from dat_ue_notif_new_datapoint where uid=? and date=?',
            150600:'select * from dat_ue_notif_new_widget where uid=? and date=?',
            150700:'select * from dat_ue_notif_new_dashboard where uid=? and date=?',
            150800:'select * from dat_ue_notif_new_circle where uid=? and date=?',
            150900:'select * from dat_ue_interv_dp_identification where uid=? and date=?',
            151000:'select * from dat_uer_interv_dp_identification where uid=? and date=?',
            151001:'select * from dat_uer_interv_dp_identification where uid=?',
            151100:'select * from dat_ue_notif_new_snapshot_shared where uid=? and date=?',
            151200:'select * from dat_ue_notif_new_snapshot_shared_with_me where uid=? and date=?',
            155000:'insert into dat_user_events (uid,date,priority,type) values (?,?,?,?)',
            155100:'insert into dat_user_events_disabled (uid,date,priority,type) values (?,?,?,?)',
            155150:'insert into dat_user_events_graph_summary (uid,date,summary) values (?,?,?)',
            155200:'insert into dat_ue_notif_new_user (uid,date,username) values (?,?,?)',
            155300:'insert into dat_ue_notif_new_agent (uid,date,aid,agentname) values (?,?,?,?)',
            155400:'insert into dat_ue_notif_new_datasource (uid,date,aid,did,datasourcename) values (?,?,?,?,?)',
            155500:'insert into dat_ue_notif_new_datapoint (uid,date,did,pid,datasourcename,datapointname) values (?,?,?,?,?,?)',
            155600:'insert into dat_ue_notif_new_widget (uid,date,wid,widgetname) values (?,?,?,?)',
            155700:'insert into dat_ue_notif_new_dashboard (uid,date,bid,dashboardname) values (?,?,?,?)',
            155800:'insert into dat_ue_notif_new_circle (uid,date,cid,circlename) values (?,?,?,?)',
            155900:'insert into dat_ue_interv_dp_identification (uid,date,did,ds_date,doubts,discarded) values (?,?,?,?,?,?)',
            156000:'insert into dat_uer_interv_dp_identification (uid,date,response_date,missing,identified,not_belonging,to_update,update_failed,update_success) values (?,?,?,?,?,?,?,?,?)',
            156100:'insert into dat_ue_notif_new_snapshot_shared (uid,date,nid,tid,widgetname,shared_with_users,shared_with_circles) values (?,?,?,?,?,?,?)',
            156200:'insert into dat_ue_notif_new_snapshot_shared_with_me (uid,date,nid,tid,username,widgetname) values (?,?,?,?,?,?)',
            157000:'delete from dat_user_events where uid=?',
            157001:'delete from dat_user_events where uid=? and date=?',
            157100:'delete from dat_user_events_disabled where uid=?',
            157101:'delete from dat_user_events_disabled where uid=? and date=?',
            157150:'delete from dat_user_events_graph_summary where uid=?',
            157151:'delete from dat_user_events_graph_summary where uid=? and date=?',
            157200:'delete from dat_ue_notif_new_user where uid=?',
            157201:'delete from dat_ue_notif_new_user where uid=? and date=?',
            157300:'delete from dat_ue_notif_new_agent where uid=?',
            157301:'delete from dat_ue_notif_new_agent where uid=? and date=?',
            157400:'delete from dat_ue_notif_new_datasource where uid=?',
            157401:'delete from dat_ue_notif_new_datasource where uid=? and date=?',
            157500:'delete from dat_ue_notif_new_datapoint where uid=?',
            157501:'delete from dat_ue_notif_new_datapoint where uid=? and date=?',
            157600:'delete from dat_ue_notif_new_widget where uid=?',
            157601:'delete from dat_ue_notif_new_widget where uid=? and date=?',
            157700:'delete from dat_ue_notif_new_dashboard where uid=?',
            157701:'delete from dat_ue_notif_new_dashboard where uid=? and date=?',
            157800:'delete from dat_ue_notif_new_circle where uid=?',
            157801:'delete from dat_ue_notif_new_circle where uid=? and date=?',
            157900:'delete from dat_ue_interv_dp_identification where uid=?',
            157901:'delete from dat_ue_interv_dp_identification where uid=? and date=?',
            158000:'delete from dat_uer_interv_dp_identification where uid=? and date=?',
            158001:'delete from dat_uer_interv_dp_identification where uid=? and date=? and response_date=?',
            158100:'delete from dat_ue_notif_new_snapshot_shared where uid=?',
            158101:'delete from dat_ue_notif_new_snapshot_shared where uid=? and date=?',
            158200:'delete from dat_ue_notif_new_snapshot_shared_with_me where uid=?',
            158201:'delete from dat_ue_notif_new_snapshot_shared_with_me where uid=? and date=?',
           }

# selects (150000 - 154999)

# dat_user_events

S_A_DATUSEREVENTS_B_UID_DATE=150000
S_A_DATUSEREVENTS_B_UID_ENDDATE_COUNT=150001
S_A_DATUSEREVENTS_B_UID_ENDDATE_FROMDATE=150002
S_A_DATUSEREVENTS_B_UID_FROMDATE=150003

# dat_user_events_disabled

S_A_DATUSEREVENTSDISABLED_B_UID_DATE=150100
S_A_DATUSEREVENTSDISABLED_B_UID_ENDDATE_COUNT=150101
S_A_DATUSEREVENTSDISABLED_B_UID_ENDDATE_FROMDATE=150102
S_A_DATUSEREVENTSDISABLED_B_UID_FROMDATE=150103

# dat_user_events_graph_summary

S_A_DATUSEREVENTSGRAPHSUMMARY_B_UID_DATE=150150

# dat_ue_notif_new_user

S_A_DATUENOTIFNEWUSER_B_UID_DATE=150200

# dat_ue_notif_new_agent

S_A_DATUENOTIFNEWAGENT_B_UID_DATE=150300

# dat_ue_notif_new_datasource

S_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE=150400

# dat_ue_notif_new_datapoint

S_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE=150500

# dat_ue_notif_new_widget

S_A_DATUENOTIFNEWWIDGET_B_UID_DATE=150600

# dat_ue_notif_new_dashboard

S_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE=150700

# dat_ue_notif_new_circle

S_A_DATUENOTIFNEWCIRCLE_B_UID_DATE=150800

# dat_ue_interv_datapoint_identification

S_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE=150900

# dat_uer_interv_datapoint_identification

S_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE=151000
S_A_DATUERINTERVDPIDENTIFICATION_B_UID=151001

# dat_ue_notif_new_snapshot_shared

S_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID_DATE=151100

# dat_ue_notif_new_snapshot_shared_with_me

S_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID_DATE=151200

# Inserts (155000 - 156999 )

# dat_user_events

I_A_DATUSEREVENTS=155000

# dat_user_events_disabled

I_A_DATUSEREVENTSDISABLED=155100

# dat_user_events_graph_summary

I_A_DATUSEREVENTSGRAPHSUMMARY=155150

# dat_ue_notif_new_user

I_A_DATUENOTIFNEWUSER=155200

# dat_ue_notif_new_agent

I_A_DATUENOTIFNEWAGENT=155300

# dat_ue_notif_new_datasource

I_A_DATUENOTIFNEWDATASOURCE=155400

# dat_ue_notif_new_datapoint

I_A_DATUENOTIFNEWDATAPOINT=155500

# dat_ue_notif_new_widget

I_A_DATUENOTIFNEWWIDGET=155600

# dat_ue_notif_new_dashboard

I_A_DATUENOTIFNEWDASHBOARD=155700

# dat_ue_notif_new_circle

I_A_DATUENOTIFNEWCIRCLE=155800

# dat_ue_intervention_datapoint_identification

I_A_DATUEINTERVDPIDENTIFICATION=155900

# dat_uer_intervention_datapoint_identification

I_A_DATUERINTERVDPIDENTIFICATION=156000

# dat_ue_notif_new_snapshot_shared

I_A_DATUENOTIFNEWSNAPSHOTSHARED=156100

# dat_ue_notif_new_snapshot_shared_with_me

I_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME=156200


# Deletes (157000 - 158999)

# dat_user_events

D_A_DATUSEREVENTS_B_UID=157000
D_A_DATUSEREVENTS_B_UID_DATE=157001

# dat_user_events_disabled

D_A_DATUSEREVENTSDISABLED_B_UID=157100
D_A_DATUSEREVENTSDISABLED_B_UID_DATE=157101

# dat_user_events_graph_summary

D_A_DATUSEREVENTSGRAPHSUMMARY_B_UID=157150
D_A_DATUSEREVENTSGRAPHSUMMARY_B_UID_DATE=157151

# dat_ue_notif_new_user

D_A_DATUENOTIFNEWUSER_B_UID=157200
D_A_DATUENOTIFNEWUSER_B_UID_DATE=157201

# dat_ue_notif_new_agent

D_A_DATUENOTIFNEWAGENT_B_UID=157300
D_A_DATUENOTIFNEWAGENT_B_UID_DATE=157301

# dat_ue_notif_new_datasource

D_A_DATUENOTIFNEWDATASOURCE_B_UID=157400
D_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE=157401

# dat_ue_notif_new_datapoint

D_A_DATUENOTIFNEWDATAPOINT_B_UID=157500
D_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE=157501

# dat_ue_notif_new_widget

D_A_DATUENOTIFNEWWIDGET_B_UID=157600
D_A_DATUENOTIFNEWWIDGET_B_UID_DATE=157601

# dat_ue_notif_new_dashboard

D_A_DATUENOTIFNEWDASHBOARD_B_UID=157700
D_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE=157701

# dat_ue_notif_new_circle

D_A_DATUENOTIFNEWCIRCLE_B_UID=157800
D_A_DATUENOTIFNEWCIRCLE_B_UID_DATE=157801

# dat_ue_intervention_datapoint_identification

D_A_DATUEINTERVDPIDENTIFICATION_B_UID=157900
D_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE=157901

# dat_uer_intervention_datapoint_identification

D_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE=158000
D_A_DATUERINTERVDPIDENTIFICATION_B_UID_DATE_RESPDATE=158001

# dat_ue_notif_new_snapshot_shared

D_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID=158100
D_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID_DATE=158101

# dat_ue_notif_new_snapshot_shared_with_me

D_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID=158200
D_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID_DATE=158201


# Updates (159000 - 159999)

