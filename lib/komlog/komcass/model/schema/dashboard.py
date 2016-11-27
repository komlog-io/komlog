'''
This file defines the cassandra statements for the creation of dashboard related tables

'''
from komlog.komcass.model.schema import keyspace

OBJECTS=[
    'MST_DASHBOARD',
    'MST_DASHBOARD_INDEX_01'
]

MST_DASHBOARD='''
    CREATE TABLE mst_dashboard (
        bid uuid,
        uid uuid,
        dashboardname text,
        widgets set<uuid>,
        creation_date timeuuid,
        PRIMARY KEY (bid)
    );
'''

MST_DASHBOARD_INDEX_01='''
    CREATE INDEX ON mst_dashboard (uid);
'''

