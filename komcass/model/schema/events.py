'''
This file defines the cassandra statements for the creation of datasource related tables

'''
from komcass.model.schema import keyspace

OBJECTS=[
         'DAT_USER_EVENTS',
         'DAT_USER_EVENTS_DISABLED',
         'DAT_USER_EVENTS_GRAPH_SUMMARY',
         'DAT_UE_NOTIF_NWUS',
         'DAT_UE_NOTIF_NWAG',
         'DAT_UE_NOTIF_NWDS',
         'DAT_UE_NOTIF_NWDP',
         'DAT_UE_NOTIF_NWWG',
         'DAT_UE_NOTIF_NWDB',
         'DAT_UE_NOTIF_NWCI',
         'DAT_UE_NOTIF_NWSNS',
         'DAT_UE_NOTIF_NWSNSWM',
         'DAT_UE_INTERV_DPID', 
         'DAT_UER_INTERV_DPID',
         'DAT_UER_INTERV_DPID_INDEX_01',
        ]

DAT_USER_EVENTS='''
        CREATE TABLE dat_user_events (
            uid uuid,
            date timeuuid,
            priority int,
            type int,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_USER_EVENTS_DISABLED='''
        CREATE TABLE dat_user_events_disabled (
            uid uuid,
            date timeuuid,
            priority int,
            type int,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_USER_EVENTS_GRAPH_SUMMARY='''
        CREATE TABLE dat_user_events_graph_summary (
            uid uuid,
            date timeuuid,
            summary text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWUS='''
        CREATE TABLE dat_ue_notif_new_user (
            uid uuid,
            date timeuuid,
            username text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWAG='''
        CREATE TABLE dat_ue_notif_new_agent (
            uid uuid,
            date timeuuid,
            aid uuid,
            agentname text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWDS='''
        CREATE TABLE dat_ue_notif_new_datasource (
            uid uuid,
            date timeuuid,
            aid uuid,
            did uuid,
            datasourcename text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWDP='''
        CREATE TABLE dat_ue_notif_new_datapoint (
            uid uuid,
            date timeuuid,
            did uuid,
            pid uuid,
            datasourcename text,
            datapointname text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWWG='''
        CREATE TABLE dat_ue_notif_new_widget (
            uid uuid,
            date timeuuid,
            wid uuid,
            widgetname text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWDB='''
        CREATE TABLE dat_ue_notif_new_dashboard (
            uid uuid,
            date timeuuid,
            bid uuid,
            dashboardname text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWCI='''
        CREATE TABLE dat_ue_notif_new_circle (
            uid uuid,
            date timeuuid,
            cid uuid,
            circlename text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWSNS='''
        CREATE TABLE dat_ue_notif_new_snapshot_shared (
            uid uuid,
            date timeuuid,
            nid uuid,
            tid uuid,
            widgetname text,
            shared_with_users map<uuid,text>,
            shared_with_circles map<uuid,text>,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_NOTIF_NWSNSWM='''
        CREATE TABLE dat_ue_notif_new_snapshot_shared_with_me (
            uid uuid,
            date timeuuid,
            nid uuid,
            tid uuid,
            username text,
            widgetname text,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UE_INTERV_DPID='''
        CREATE TABLE dat_ue_interv_dp_identification (
            uid uuid,
            date timeuuid,
            did uuid,
            ds_date uuid,
            doubts set<uuid>,
            discarded set<uuid>,
            PRIMARY KEY (uid,date)
        );
    '''

DAT_UER_INTERV_DPID='''
        CREATE TABLE dat_uer_interv_dp_identification (
            uid uuid,
            date timeuuid,
            response_date timeuuid,
            missing set<uuid>,
            identified map<uuid,int>,
            not_belonging set<uuid>,
            to_update set<uuid>,
            update_failed set<uuid>,
            update_success set<uuid>,
            PRIMARY KEY ((uid,date),response_date)
        );
    '''
DAT_UER_INTERV_DPID_INDEX_01='''
        CREATE INDEX ON dat_uer_interv_dp_identification (uid);
    '''

