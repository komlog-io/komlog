'''
This file contains the statements to operate with snapshot tables
Statements range (120000-129999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={120000:'select * from mst_snapshot where nid=?',
            120001:'select * from mst_snapshot where uid=?',
            120002:'select * from mst_snapshot where wid=?',
            120003:'select nid from mst_snapshot where uid=?',
            120004:'select nid from mst_snapshot where wid=?',
            120005:'select count(*) from mst_snapshot where uid=?',
            120006:'select count(*) from mst_snapshot where wid=?',
            120100:'select * from mst_snapshot_ds where nid=?',
            120200:'select * from mst_snapshot_dp where nid=?',
            120300:'select * from mst_snapshot_histogram where nid=?',
            120400:'select * from mst_snapshot_linegraph where nid=?',
            120500:'select * from mst_snapshot_table where nid=?',
            120600:'select * from mst_snapshot_multidp where nid=?',
            125000:'insert into mst_snapshot (nid,uid,wid,type,interval_init,interval_end,widgetname,creation_date,shared_with_uids,shared_with_cids) values (?,?,?,?,?,?,?,?,?,?)',
            125001:'insert into mst_snapshot (nid,uid,wid,type,interval_init,interval_end,widgetname,creation_date,shared_with_uids,shared_with_cids) values (?,?,?,?,?,?,?,?,?,?) if not exists',
            125100:'insert into mst_snapshot_ds (nid,did,datasource_config,datapoints_config) values (?,?,?,?)',
            125200:'insert into mst_snapshot_dp (nid,pid,datapoint_config) values (?,?,?)',
            125300:'insert into mst_snapshot_histogram (nid,datapoints,colors) values (?,?,?)',
            125400:'insert into mst_snapshot_linegraph (nid,datapoints,colors) values (?,?,?)',
            125500:'insert into mst_snapshot_table (nid,datapoints,colors) values (?,?,?)',
            125600:'insert into mst_snapshot_multidp (nid,active_visualization,datapoints,datapoints_config) values (?,?,?,?)',
            127000:'delete from mst_snapshot where nid=?',
            127100:'delete from mst_snapshot_ds where nid=?',
            127200:'delete from mst_snapshot_dp where nid=?',
            127300:'delete from mst_snapshot_histogram where nid=?',
            127400:'delete from mst_snapshot_linegraph where nid=?',
            127500:'delete from mst_snapshot_table where nid=?',
            127600:'delete from mst_snapshot_multidp where nid=?',
           }

# selects (120000 - 124999)

# mst_snapshot

S_A_MSTSNAPSHOT_B_NID=120000
S_A_MSTSNAPSHOT_B_UID=120001
S_A_MSTSNAPSHOT_B_WID=120002
S_NID_MSTSNAPSHOT_B_UID=120003
S_NID_MSTSNAPSHOT_B_WID=120004
S_COUNT_MSTSNAPSHOT_B_UID=120005
S_COUNT_MSTSNAPSHOT_B_WID=120006

# mst_snapshot_ds

S_A_MSTSNAPSHOTDS_B_NID=120100

# mst_snapshot_dp

S_A_MSTSNAPSHOTDP_B_NID=120200

# mst_snapshot_histogram

S_A_MSTSNAPSHOTHISTOGRAM_B_NID=120300

# mst_snapshot_linegraph

S_A_MSTSNAPSHOTLINEGRAPH_B_NID=120400

# mst_snapshot_table

S_A_MSTSNAPSHOTTABLE_B_NID=120500

# mst_snapshot_multidp

S_A_MSTSNAPSHOTMULTIDP_B_NID=120600

# Inserts (125000 - 126999)

# mst_snapshot

I_A_MSTSNAPSHOT=125000
I_A_MSTSNAPSHOT_INE=125001

# mst_snapshot_ds

I_A_MSTSNAPSHOTDS=125100

# mst_snapshot_dp

I_A_MSTSNAPSHOTDP=125200

# mst_snapshot_histogram

I_A_MSTSNAPSHOTHISTOGRAM=125300

# mst_snapshot_linegraph

I_A_MSTSNAPSHOTLINEGRAPH=125400

# mst_snapshot_table

I_A_MSTSNAPSHOTTABLE=125500

# mst_snapshot_multidp

I_A_MSTSNAPSHOTMULTIDP=125600


# Deletes (127000 - 128999)

# mst_snapshot

D_A_MSTSNAPSHOT_B_NID=127000

# mst_snapshot_ds

D_A_MSTSNAPSHOTDS_B_NID=127100

# mst_snapshot_dp

D_A_MSTSNAPSHOTDP_B_NID=127200

# mst_snapshot_histogram

D_A_MSTSNAPSHOTHISTOGRAM_B_NID=127300

# mst_snapshot_linegraph

D_A_MSTSNAPSHOTLINEGRAPH_B_NID=127400

# mst_snapshot_table

D_A_MSTSNAPSHOTTABLE_B_NID=127500

# mst_snapshot_multidp

D_A_MSTSNAPSHOTMULTIDP_B_NID=127600


# updates (129000 - 129999)


