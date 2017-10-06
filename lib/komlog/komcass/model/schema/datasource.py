'''
This file defines the cassandra statements for the creation of datasource related tables

'''
from komlog.komcass.model.schema import keyspace

OBJECTS=[
    'MST_DATASOURCE',
    'MST_DATASOURCE_INDEX_01',
    'MST_DATASOURCE_INDEX_02',
    'MST_DATASOURCE_STATS',
    'DAT_DATASOURCE',
    'DAT_DATASOURCE_MAP',
    'DAT_DATASOURCE_HASH',
    'DAT_DATASOURCE_METADATA',
    'MST_DATASOURCE_HOOKS',
    'DAT_DATASOURCE_SUPPLIES',
    'MST_DATAPOINT_CLASSIFIER_DTREE',
    'MST_DATASOURCE_FEATURES',
    'MST_DATASOURCE_BY_FEATURE',
]

MST_DATASOURCE='''
    CREATE TABLE mst_datasource (
        did uuid,
        aid uuid,
        uid uuid,
        datasourcename text,
        creation_date timeuuid,
        PRIMARY KEY (did)
    );
'''

MST_DATASOURCE_INDEX_01='''
    CREATE INDEX ON mst_datasource (aid);
'''

MST_DATASOURCE_INDEX_02='''
    CREATE INDEX ON mst_datasource (uid);
'''

MST_DATASOURCE_STATS='''
    CREATE TABLE mst_datasource_stats (
        did uuid,
        last_received timeuuid,
        last_mapped timeuuid,
        PRIMARY KEY (did)
    );
'''

DAT_DATASOURCE='''
    CREATE TABLE dat_datasource (
        did uuid,
        date timeuuid,
        content text,
        PRIMARY KEY (did,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

DAT_DATASOURCE_MAP='''
    CREATE TABLE dat_datasource_map (
        did uuid,
        date timeuuid,
        variables map<int,int>,
        datapoints map<uuid,int>,
        PRIMARY KEY (did,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

DAT_DATASOURCE_HASH='''
    CREATE TABLE dat_datasource_hash (
        did uuid,
        date timeuuid,
        content text,
        PRIMARY KEY (did,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

DAT_DATASOURCE_METADATA='''
    CREATE TABLE dat_datasource_metadata (
        did uuid,
        date timeuuid,
        size varint,
        PRIMARY KEY (did,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

MST_DATASOURCE_HOOKS='''
    CREATE TABLE mst_datasource_hooks (
        did uuid,
        sid uuid,
        PRIMARY KEY (did,sid)
    );
'''

DAT_DATASOURCE_SUPPLIES='''
    CREATE TABLE dat_datasource_supplies (
        did uuid,
        date timeuuid,
        supplies set<text>,
        PRIMARY KEY (did,date)
    ) WITH CLUSTERING ORDER BY (date desc);
'''

MST_DATAPOINT_CLASSIFIER_DTREE='''
    CREATE TABLE mst_datapoint_classifier_dtree(
        did uuid,
        dtree blob,
        PRIMARY KEY (did)
    );
'''

MST_DATASOURCE_FEATURES='''
    CREATE TABLE mst_datasource_features (
        did uuid,
        date timeuuid,
        features set<double>,
        PRIMARY KEY (did)
    );
'''

MST_DATASOURCE_BY_FEATURE='''
    CREATE TABLE mst_datasource_by_feature (
        feature double,
        did uuid,
        weight float,
        PRIMARY KEY (feature, did)
    ) WITH CLUSTERING ORDER BY (did asc);
'''

