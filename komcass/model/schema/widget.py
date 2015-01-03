#coding: utf-8
'''
This file defines the cassandra statements for the creation of widget related tables

'''
from komcass.model.schema import keyspace

OBJECTS=['MST_WIDGET',
         'MST_WIDGET_INDEX_01',
         'MST_WIDGETDS',
         'MST_WIDGETDP'
        ]

MST_WIDGET='''
        CREATE TABLE mst_widget (
            wid uuid,
            uid uuid,
            type text,
            PRIMARY KEY (wid)
        );
    '''

MST_WIDGET_INDEX_01='''
        CREATE INDEX ON mst_widget (uid);
    '''

MST_WIDGETDS='''
        CREATE TABLE mst_widget_ds (
            wid uuid,
            uid uuid,
            did uuid,
            creation_date timeuuid,
            PRIMARY KEY (wid)
        );
    '''

MST_WIDGETDP='''
        CREATE TABLE mst_widget_dp (
            wid uuid,
            uid uuid,
            pid uuid,
            creation_date timeuuid,
            PRIMARY KEY (wid)
        );
    '''

