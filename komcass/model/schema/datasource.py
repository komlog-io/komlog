#coding: utf-8
'''
This file defines the cassandra statements for the creation of datasource related tables

'''
from komcass.model.schema import keyspace

OBJECTS=['MST_DATASOURCE',
         'MST_DATASOURCE_INDEX_01',
         'MST_DATASOURCE_INDEX_02',
         'MST_DATASOURCE_STATS',
         'DAT_DATASOURCE',
         'DAT_DATASOURCE_MAP'
        ]

MST_DATASOURCE='''
        CREATE TABLE mst_datasource (
            did uuid,
            aid uuid,
            uid uuid,
            datasourcename text,
            state int,
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
        );
    '''

DAT_DATASOURCE_MAP='''
        CREATE TABLE dat_datasource_map (
            did uuid,
            date timeuuid,
            content text,
            variables map<int,int>,
            datapoints map<uuid,int>,
            PRIMARY KEY (did,date)
        );
    '''

