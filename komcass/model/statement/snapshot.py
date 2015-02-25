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
            120002:'select nid from mst_snapshot where uid=?',
            120003:'select * from mst_snapshot_ds where nid=?',
            120004:'select nid from mst_snapshot_ds where wid=?',
            120005:'select * from mst_snapshot_dp where nid=?',
            120006:'select nid from mst_snapshot_dp where wid=?',
            120007:'select * from mst_snapshot_histogram where nid=?',
            120008:'select nid from mst_snapshot_histogram where wid=?',
            120009:'select * from mst_snapshot_linegraph where nid=?',
            120010:'select nid from mst_snapshot_linegraph where wid=?',
            120011:'select * from mst_snapshot_table where nid=?',
            120012:'select nid from mst_snapshot_table where wid=?',
            120013:'select count(*) from mst_snapshot where uid=?',
            121000:'insert into mst_snapshot (nid,uid,type) values (?,?,?)',
            121001:'insert into mst_snapshot_ds (nid,uid,wid,interval_init,interval_end,widgetname,creation_date,did) values (?,?,?,?,?,?,?,?)',
            121002:'insert into mst_snapshot_dp (nid,uid,wid,interval_init,interval_end,widgetname,creation_date,pid) values (?,?,?,?,?,?,?,?)',
            121003:'insert into mst_snapshot_histogram (nid,uid,wid,interval_init,interval_end,widgetname,creation_date,datapoints,colors) values (?,?,?,?,?,?,?,?,?)',
            121004:'insert into mst_snapshot_linegraph (nid,uid,wid,interval_init,interval_end,widgetname,creation_date,datapoints,colors) values (?,?,?,?,?,?,?,?,?)',
            121005:'insert into mst_snapshot_table (nid,uid,wid,interval_init,interval_end,widgetname,creation_date,datapoints,colors) values (?,?,?,?,?,?,?,?,?)',
            122000:'delete from mst_snapshot where nid=?',
            122001:'delete from mst_snapshot_ds where nid=?',
            122002:'delete from mst_snapshot_dp where nid=?',
            122003:'delete from mst_snapshot_histogram where nid=?',
            122004:'delete from mst_snapshot_linegraph where nid=?',
            122005:'delete from mst_snapshot_table where nid=?',
           }

# selects

S_A_MSTSNAPSHOT_B_NID=120000
S_A_MSTSNAPSHOT_B_UID=120001
S_NID_MSTSNAPSHOT_B_UID=120002
S_A_MSTSNAPSHOTDS_B_NID=120003
S_NID_MSTSNAPSHOTDS_B_WID=120004
S_A_MSTSNAPSHOTDP_B_NID=120005
S_NID_MSTSNAPSHOTDP_B_WID=120006
S_A_MSTSNAPSHOTHISTOGRAM_B_NID=120007
S_NID_MSTSNAPSHOTHISTOGRAM_B_WID=120008
S_A_MSTSNAPSHOTLINEGRAPH_B_NID=120009
S_NID_MSTSNAPSHOTLINEGRAPH_B_WID=120010
S_A_MSTSNAPSHOTTABLE_B_NID=120011
S_NID_MSTSNAPSHOTTABLE_B_WID=120012
S_COUNT_MSTSNAPSHOT_B_UID=120013

# Inserts

I_A_MSTSNAPSHOT=121000
I_A_MSTSNAPSHOTDS=121001
I_A_MSTSNAPSHOTDP=121002
I_A_MSTSNAPSHOTHISTOGRAM=121003
I_A_MSTSNAPSHOTLINEGRAPH=121004
I_A_MSTSNAPSHOTTABLE=121005

# Deletes

D_A_MSTSNAPSHOT_B_NID=122000
D_A_MSTSNAPSHOTDS_B_NID=122001
D_A_MSTSNAPSHOTDP_B_NID=122002
D_A_MSTSNAPSHOTHISTOGRAM_B_NID=122003
D_A_MSTSNAPSHOTLINEGRAPH_B_NID=122004
D_A_MSTSNAPSHOTTABLE_B_NID=122005

