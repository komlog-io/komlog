'''
This file defines the cassandra statements for the creation of widget related tables

'''
from komlog.komcass.model.schema import keyspace

OBJECTS=[
    'MST_WIDGET',
    'MST_WIDGET_INDEX_01',
    'MST_WIDGETDS',
    'MST_WIDGETDS_INDEX_01',
    'MST_WIDGETDP',
    'MST_WIDGETDP_INDEX_01',
    'MST_WIDGET_HISTOGRAM',
    'MST_WIDGET_HISTOGRAM_INDEX_01',
    'MST_WIDGET_HISTOGRAM_INDEX_02',
    'MST_WIDGET_LINEGRAPH',
    'MST_WIDGET_LINEGRAPH_INDEX_01',
    'MST_WIDGET_LINEGRAPH_INDEX_02',
    'MST_WIDGET_TABLE',
    'MST_WIDGET_TABLE_INDEX_01',
    'MST_WIDGET_TABLE_INDEX_02',
    'MST_WIDGET_MULTIDP',
    'MST_WIDGET_MULTIDP_INDEX_01',
]

MST_WIDGET='''
    CREATE TABLE mst_widget (
        wid uuid,
        uid uuid,
        type text,
        creation_date timeuuid,
        widgetname text,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGET_INDEX_01='''
    CREATE INDEX ON mst_widget (uid);
'''

MST_WIDGETDS='''
    CREATE TABLE mst_widget_ds (
        wid uuid,
        did uuid,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGETDS_INDEX_01='''
    CREATE INDEX ON mst_widget_ds (did);
'''

MST_WIDGETDP='''
    CREATE TABLE mst_widget_dp (
        wid uuid,
        pid uuid,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGETDP_INDEX_01='''
    CREATE INDEX ON mst_widget_dp (pid);
'''

MST_WIDGET_HISTOGRAM='''
    CREATE TABLE mst_widget_histogram (
        wid uuid,
        datapoints set<uuid>,
        colors map <uuid,text>,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGET_HISTOGRAM_INDEX_01='''
    CREATE INDEX ON mst_widget_histogram (datapoints);
'''

MST_WIDGET_HISTOGRAM_INDEX_02='''
    CREATE INDEX ON mst_widget_histogram (colors);
'''

MST_WIDGET_LINEGRAPH='''
    CREATE TABLE mst_widget_linegraph (
        wid uuid,
        datapoints set<uuid>,
        colors map <uuid,text>,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGET_LINEGRAPH_INDEX_01='''
    CREATE INDEX ON mst_widget_linegraph (datapoints);
'''

MST_WIDGET_LINEGRAPH_INDEX_02='''
    CREATE INDEX ON mst_widget_linegraph (colors);
'''

MST_WIDGET_TABLE='''
    CREATE TABLE mst_widget_table (
        wid uuid,
        datapoints set<uuid>,
        colors map <uuid,text>,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGET_TABLE_INDEX_01='''
    CREATE INDEX ON mst_widget_table (datapoints);
'''

MST_WIDGET_TABLE_INDEX_02='''
    CREATE INDEX ON mst_widget_table (colors);
'''

MST_WIDGET_MULTIDP='''
    CREATE TABLE mst_widget_multidp (
        wid uuid,
        active_visualization int,
        datapoints set<uuid>,
        PRIMARY KEY (wid)
    );
'''

MST_WIDGET_MULTIDP_INDEX_01='''
    CREATE INDEX ON mst_widget_multidp (datapoints);
'''

