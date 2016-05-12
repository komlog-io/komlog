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
    'DAT_DATASOURCE_TEXT_SUMMARY',
    'DAT_DATASOURCE_NOVELTY_DETECTOR_DATAPOINT',
    'DAT_DATASOURCE_METADATA',
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

DAT_DATASOURCE_TEXT_SUMMARY='''
        CREATE TABLE dat_datasource_text_summary (
            did uuid,
            date timeuuid,
            content_length varint,
            num_lines int,
            num_words int,
            word_frecuency map<text,int>,
            PRIMARY KEY (did,date)
        ) WITH CLUSTERING ORDER BY (date desc);
    '''

DAT_DATASOURCE_NOVELTY_DETECTOR_DATAPOINT='''
        CREATE TABLE dat_datasource_novelty_detector_datapoint (
            did uuid,
            pid uuid,
            date timeuuid,
            nd blob,
            features set<text>,
            PRIMARY KEY ((did,pid),date)
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

