'''
This file defines the cassandra statements for the creation of snapshot related tables
A snapshot is a widget in a specific time interval.

'''
from komcass.model.schema import keyspace

OBJECTS=['MST_SNAPSHOT',
         'MST_SNAPSHOT_INDEX_01',
         'MST_SNAPSHOTDS',
         'MST_SNAPSHOTDS_INDEX_01',
         'MST_SNAPSHOTDP',
         'MST_SNAPSHOTDP_INDEX_01',
         'MST_SNAPSHOT_HISTOGRAM',
         'MST_SNAPSHOT_HISTOGRAM_INDEX_01',
         'MST_SNAPSHOT_LINEGRAPH',
         'MST_SNAPSHOT_LINEGRAPH_INDEX_01',
         'MST_SNAPSHOT_TABLE',
         'MST_SNAPSHOT_TABLE_INDEX_01',
        ]

MST_SNAPSHOT='''
        CREATE TABLE mst_snapshot (
            nid uuid,
            uid uuid,
            type text,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_INDEX_01='''
        CREATE INDEX ON mst_snapshot (uid);
    '''

MST_SNAPSHOTDS='''
        CREATE TABLE mst_snapshot_ds (
            nid uuid,
            uid uuid,
            wid uuid,
            interval_init timeuuid,
            interval_end timeuuid,
            widgetname text,
            creation_date timeuuid,
            did uuid,
            shared_with_uids set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOTDS_INDEX_01='''
        CREATE INDEX ON mst_snapshot_ds (wid);
    '''

MST_SNAPSHOTDP='''
        CREATE TABLE mst_snapshot_dp (
            nid uuid,
            uid uuid,
            wid uuid,
            interval_init timeuuid,
            interval_end timeuuid,
            widgetname text,
            creation_date timeuuid,
            pid uuid,
            shared_with_uids set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOTDP_INDEX_01='''
        CREATE INDEX ON mst_snapshot_dp (wid);
    '''

MST_SNAPSHOT_HISTOGRAM='''
        CREATE TABLE mst_snapshot_histogram (
            nid uuid,
            uid uuid,
            wid uuid,
            interval_init timeuuid,
            interval_end timeuuid,
            widgetname text,
            creation_date timeuuid,
            datapoints set<uuid>,
            colors map<uuid,text>,
            shared_with_uids set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_HISTOGRAM_INDEX_01='''
        CREATE INDEX ON mst_snapshot_histogram (wid);
    '''

MST_SNAPSHOT_LINEGRAPH='''
        CREATE TABLE mst_snapshot_linegraph (
            nid uuid,
            uid uuid,
            wid uuid,
            interval_init timeuuid,
            interval_end timeuuid,
            widgetname text,
            creation_date timeuuid,
            datapoints set<uuid>,
            colors map<uuid,text>,
            shared_with_uids set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_LINEGRAPH_INDEX_01='''
        CREATE INDEX ON mst_snapshot_linegraph (wid);
    '''

MST_SNAPSHOT_TABLE='''
        CREATE TABLE mst_snapshot_table (
            nid uuid,
            uid uuid,
            wid uuid,
            interval_init timeuuid,
            interval_end timeuuid,
            widgetname text,
            creation_date timeuuid,
            datapoints set<uuid>,
            colors map<uuid,text>,
            shared_with_uids set<uuid>,
            PRIMARY KEY (nid)
        );
    '''

MST_SNAPSHOT_TABLE_INDEX_01='''
        CREATE INDEX ON mst_snapshot_table (wid);
    '''

