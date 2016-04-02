'''
This file defines the cassandra statements for the creation of snapshot related tables
A snapshot is a widget in a specific time interval.

'''
from komlog.komcass.model.schema import keyspace

OBJECTS=['MST_CIRCLE',
         'MST_CIRCLE_INDEX_01',
        ]

MST_CIRCLE='''
        CREATE TABLE mst_circle (
            cid uuid,
            uid uuid,
            type text,
            creation_date timeuuid,
            circlename text,
            members set<uuid>,
            PRIMARY KEY (cid)
        );
    '''

MST_CIRCLE_INDEX_01='''
        CREATE INDEX ON mst_circle (uid);
    '''

