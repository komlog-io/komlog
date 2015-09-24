'''
This file defines the cassandra statements for the creation of snapshot related tables
A snapshot is a widget in a specific time interval.

'''
from komcass.model.schema import keyspace

OBJECTS=['MST_SNAPSHOT',
         'MST_SNAPSHOT_INDEX_01',
         'MST_SNAPSHOT_INDEX_02',
         'MST_SNAPSHOTDS',
         'MST_SNAPSHOTDP',
         'MST_SNAPSHOT_MULTIDP',
         'MST_SNAPSHOT_HISTOGRAM',
         'MST_SNAPSHOT_LINEGRAPH',
         'MST_SNAPSHOT_TABLE',
        ]

MST_SNAPSHOT='''
        CREATE TABLE mst_snapshot (
            nid uuid,
            uid uuid,
            wid uuid,
            type text,
            interval_init timeuuid,
            interval_end timeuuid,
            widgetname text,
            creation_date timeuuid,
            shared_with_uids set<uuid>,
            shared_with_cids set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_INDEX_01='''
        CREATE INDEX ON mst_snapshot (uid);
    '''

MST_SNAPSHOT_INDEX_02='''
        CREATE INDEX ON mst_snapshot (wid);
    '''

MST_SNAPSHOTDS='''
        CREATE TABLE mst_snapshot_ds (
            nid uuid,
            did uuid,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOTDP='''
        CREATE TABLE mst_snapshot_dp (
            nid uuid,
            pid uuid,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_HISTOGRAM='''
        CREATE TABLE mst_snapshot_histogram (
            nid uuid,
            datapoints set<uuid>,
            colors map<uuid,text>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_LINEGRAPH='''
        CREATE TABLE mst_snapshot_linegraph (
            nid uuid,
            datapoints set<uuid>,
            colors map<uuid,text>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_TABLE='''
        CREATE TABLE mst_snapshot_table (
            nid uuid,
            datapoints set<uuid>,
            colors map<uuid,text>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_MULTIDP='''
        CREATE TABLE mst_snapshot_multidp (
            nid uuid,
            active_visualization int,
            datapoints set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

