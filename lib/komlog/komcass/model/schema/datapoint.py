#coding: utf-8
'''
This file defines the cassandra statements for the creation of datapoint related tables

'''

OBJECTS=[
    'MST_DATAPOINT',
    'MST_DATAPOINT_INDEX_01',
    'MST_DATAPOINT_INDEX_02',
    'MST_DATAPOINT_STATS',
    'DAT_DATAPOINT',
    'DAT_DATAPOINT_DTREE_POSITIVES',
    'DAT_DATAPOINT_DTREE_NEGATIVES',
    'MST_DATAPOINT_HOOKS',
]

MST_DATAPOINT='''
    CREATE TABLE mst_datapoint (
        pid uuid,
        did uuid,
        uid uuid,
        datapointname text,
        color text,
        creation_date timeuuid,
        PRIMARY KEY (pid)
    );
'''

MST_DATAPOINT_INDEX_01='''
    CREATE INDEX ON mst_datapoint (did);
'''

MST_DATAPOINT_INDEX_02='''
    CREATE INDEX ON mst_datapoint (uid);
'''

MST_DATAPOINT_STATS='''
    CREATE TABLE mst_datapoint_stats (
        pid uuid,
        decimal_separator text,
        last_received timeuuid,
        PRIMARY KEY (pid)
    );
'''

DAT_DATAPOINT='''
    CREATE TABLE dat_datapoint (
        pid uuid,
        date timeuuid,
        value decimal,
        PRIMARY KEY (pid,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

DAT_DATAPOINT_DTREE_POSITIVES='''
    CREATE TABLE dat_datapoint_dtree_positives (
        pid uuid,
        date timeuuid,
        position int,
        length int,
        PRIMARY KEY (pid,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

DAT_DATAPOINT_DTREE_NEGATIVES='''
    CREATE TABLE dat_datapoint_dtree_negatives (
        pid uuid,
        date timeuuid,
        position int,
        length int,
        PRIMARY KEY (pid,date,position)
    ) WITH CLUSTERING ORDER BY (date desc,position asc);
'''

MST_DATAPOINT_HOOKS='''
    CREATE TABLE mst_datapoint_hooks (
        pid uuid,
        sid uuid,
        PRIMARY KEY (pid,sid)
    );
'''

