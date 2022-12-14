'''
This file contains the statements to operate with permission tables
Statements range (80000-89999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    80000:'select uid,aid,perm from perm_user_agent where uid=?',
    80001:'select uid,aid,perm from perm_user_agent where uid=? and aid=?',
    80100:'select uid,did,perm from perm_user_datasource where uid=?',
    80101:'select uid,did,perm from perm_user_datasource where uid=? and did=?',
    80200:'select uid,pid,perm from perm_user_datapoint where uid=?',
    80201:'select uid,pid,perm from perm_user_datapoint where uid=? and pid=?',
    80300:'select uid,wid,perm from perm_user_widget where uid=?',
    80301:'select uid,wid,perm from perm_user_widget where uid=? and wid=?',
    80400:'select uid,bid,perm from perm_user_dashboard where uid=?',
    80401:'select uid,bid,perm from perm_user_dashboard where uid=? and bid=?',
    80700:'select uid,nid,perm from perm_user_snapshot where uid=?',
    80701:'select uid,nid,perm from perm_user_snapshot where uid=? and nid=?',
    80800:'select uid,cid,perm from perm_user_circle where uid=?',
    80801:'select uid,cid,perm from perm_user_circle where uid=? and cid=?',
    80900:'select uid,dest_uid,uri,perm from perm_user_shared_uri where uid=?',
    80901:'select uid,dest_uid,uri,perm from perm_user_shared_uri where uid=? and dest_uid=?',
    80902:'select uid,dest_uid,uri,perm from perm_user_shared_uri where uid=? and dest_uid=? and uri=?',
    81000:'select uid,owner_uid,uri,perm from perm_user_shared_uri_with_me where uid=?',
    81001:'select uid,owner_uid,uri,perm from perm_user_shared_uri_with_me where uid=? and owner_uid=?',
    81002:'select uid,owner_uid,uri,perm from perm_user_shared_uri_with_me where uid=? and owner_uid=? and uri=?',
    85000:'insert into perm_user_agent (uid,aid,perm) values (?,?,?)',
    85100:'insert into perm_user_datasource (uid,did,perm) values (?,?,?)',
    85200:'insert into perm_user_datapoint (uid,pid,perm) values (?,?,?)',
    85300:'insert into perm_user_widget (uid,wid,perm) values (?,?,?)',
    85400:'insert into perm_user_dashboard (uid,bid,perm) values (?,?,?)',
    85700:'insert into perm_user_snapshot (uid,nid,perm) values (?,?,?)',
    85800:'insert into perm_user_circle (uid,cid,perm) values (?,?,?)',
    85900:'insert into perm_user_shared_uri (uid,dest_uid,uri,perm) values (?,?,?,?)',
    86000:'insert into perm_user_shared_uri_with_me (uid,owner_uid,uri,perm) values (?,?,?,?)',
    87000:'delete from perm_user_agent where uid=?',
    87001:'delete from perm_user_agent where uid=? and aid=?',
    87100:'delete from perm_user_datasource where uid=?',
    87101:'delete from perm_user_datasource where uid=? and did=?',
    87200:'delete from perm_user_datapoint where uid=?',
    87201:'delete from perm_user_datapoint where uid=? and pid=?',
    87300:'delete from perm_user_widget where uid=?',
    87301:'delete from perm_user_widget where uid=? and wid=?',
    87400:'delete from perm_user_dashboard where uid=?',
    87401:'delete from perm_user_dashboard where uid=? and bid=?',
    87700:'delete from perm_user_snapshot where uid=?',
    87701:'delete from perm_user_snapshot where uid=? and nid=?',
    87800:'delete from perm_user_circle where uid=?',
    87801:'delete from perm_user_circle where uid=? and cid=?',
    87900:'delete from perm_user_shared_uri where uid=?',
    87901:'delete from perm_user_shared_uri where uid=? and dest_uid=?',
    87902:'delete from perm_user_shared_uri where uid=? and dest_uid=? and uri=?',
    88000:'delete from perm_user_shared_uri_with_me where uid=?',
    88001:'delete from perm_user_shared_uri_with_me where uid=? and owner_uid=?',
    88002:'delete from perm_user_shared_uri_with_me where uid=? and owner_uid=? and uri=?',
}

# selects (80000 - 84999)

# perm_user_agent

S_A_PERMUSERAGENT_B_UID                         = 80000
S_A_PERMUSERAGENT_B_UID_AID                     = 80001

# perm_user_datasource

S_A_PERMUSERDATASOURCE_B_UID                    = 80100
S_A_PERMUSERDATASOURCE_B_UID_DID                = 80101

# perm_user_datapoint

S_A_PERMUSERDATAPOINT_B_UID                     = 80200
S_A_PERMUSERDATAPOINT_B_UID_PID                 = 80201

# perm_user_widget

S_A_PERMUSERWIDGET_B_UID                        = 80300
S_A_PERMUSERWIDGET_B_UID_WID                    = 80301

# perm_user_dashboard

S_A_PERMUSERDASHBOARD_B_UID                     = 80400
S_A_PERMUSERDASHBOARD_B_UID_BID                 = 80401

# perm_user_snapshot

S_A_PERMUSERSNAPSHOT_B_UID                      = 80700
S_A_PERMUSERSNAPSHOT_B_UID_NID                  = 80701

# perm_user_circle

S_A_PERMUSERCIRCLE_B_UID                        = 80800
S_A_PERMUSERCIRCLE_B_UID_CID                    = 80801

# perm_user_shared_uri

S_A_PERMUSERSHAREDURI_B_UID                     = 80900
S_A_PERMUSERSHAREDURI_B_UID_DESTUID             = 80901
S_A_PERMUSERSHAREDURI_B_UID_DESTUID_URI         = 80902

# perm_user_shared_uri_with_me

S_A_PERMUSERSHAREDURIWITHME_B_UID               = 81000
S_A_PERMUSERSHAREDURIWITHME_B_UID_OWNERUID      = 81001
S_A_PERMUSERSHAREDURIWITHME_B_UID_OWNERUID_URI  = 81002


# Inserts (85000 - 86999)

# perm_user_agent

I_A_PERMUSERAGENT                               = 85000

# perm_user_datasource

I_A_PERMUSERDATASOURCE                          = 85100

# perm_user_datapoint

I_A_PERMUSERDATAPOINT                           = 85200

# perm_user_widget

I_A_PERMUSERWIDGET                              = 85300

# perm_user_dashboard

I_A_PERMUSERDASHBOARD                           = 85400

# perm_user_snapshot

I_A_PERMUSERSNAPSHOT                            = 85700

# perm_user_circle

I_A_PERMUSERCIRCLE                              = 85800

# perm_user_shared_uri

I_A_PERMUSERSHAREDURI                           = 85900

# perm_user_shared_uri_with_me

I_A_PERMUSERSHAREDURIWITHME                     = 86000

# Deletes (87000 - 88999)

# perm_user_agent

D_P_PERMUSERAGENT_B_UID                         = 87000
D_P_PERMUSERAGENT_B_UID_AID                     = 87001

# perm_user_datasource

D_P_PERMUSERDATASOURCE_B_UID                    = 87100
D_P_PERMUSERDATASOURCE_B_UID_DID                = 87101

# perm_user_datapoint

D_P_PERMUSERDATAPOINT_B_UID                     = 87200
D_P_PERMUSERDATAPOINT_B_UID_PID                 = 87201

# perm_user_widget

D_P_PERMUSERWIDGET_B_UID                        = 87300
D_P_PERMUSERWIDGET_B_UID_WID                    = 87301

# perm_user_dashboard

D_P_PERMUSERDASHBOARD_B_UID                     = 87400
D_P_PERMUSERDASHBOARD_B_UID_BID                 = 87401

# perm_user_snapshot

D_P_PERMUSERSNAPSHOT_B_UID                      = 87700
D_P_PERMUSERSNAPSHOT_B_UID_NID                  = 87701

# perm_user_circle

D_P_PERMUSERCIRCLE_B_UID                        = 87800
D_P_PERMUSERCIRCLE_B_UID_CID                    = 87801

# perm_user_shared_uri

D_A_PERMUSERSHAREDURI_B_UID                     = 87900
D_A_PERMUSERSHAREDURI_B_UID_DESTUID             = 87901
D_A_PERMUSERSHAREDURI_B_UID_DESTUID_URI         = 87902

# perm_user_shared_uri_with_me

D_A_PERMUSERSHAREDURIWITHME_B_UID               = 88000
D_A_PERMUSERSHAREDURIWITHME_B_UID_OWNERUID      = 88001
D_A_PERMUSERSHAREDURIWITHME_B_UID_OWNERUID_URI  = 88002

# Updates (89000 - 89999)

# perm_user_agent

# perm_user_datasource

# perm_user_datapoint

# perm_user_widget

# perm_user_dashboard

# perm_user_snapshot

# perm_user_circle

# perm_user_shared_uri


