'''
This file defines the cassandra statements for the creation of quotes related tables

'''

OBJECTS=[
    'QUO_USER',
    'QUO_AGENT',
    'QUO_DATASOURCE',
    'QUO_DATAPOINT',
    'QUO_WIDGET',
    'QUO_DASHBOARD',
    'QUO_CIRCLE',
    'QUO_TS_USER',
    'QUO_TS_DATASOURCE',
    'QUO_TS_DATAPOINT',
]

QUO_USER='''
    CREATE TABLE quo_user (
        uid uuid,
        quote text,
        value varint,
        PRIMARY KEY (uid,quote)
    );
'''

QUO_AGENT='''
    CREATE TABLE quo_agent (
        aid uuid,
        quote text,
        value varint,
        PRIMARY KEY (aid,quote)
    );
'''

QUO_DATASOURCE='''
    CREATE TABLE quo_datasource (
        did uuid,
        quote text,
        value varint,
        PRIMARY KEY (did,quote)
    );
'''

QUO_DATAPOINT='''
    CREATE TABLE quo_datapoint (
        pid uuid,
        quote text,
        value varint,
        PRIMARY KEY (pid,quote)
    );
'''

QUO_WIDGET='''
    CREATE TABLE quo_widget (
        wid uuid,
        quote text,
        value varint,
        PRIMARY KEY (wid,quote)
    );
'''

QUO_DASHBOARD='''
    CREATE TABLE quo_dashboard (
        bid uuid,
        quote text,
        value varint,
        PRIMARY KEY (bid,quote)
    );
'''

QUO_CIRCLE='''
    CREATE TABLE quo_circle (
        cid uuid,
        quote text,
        value varint,
        PRIMARY KEY (cid,quote)
    );
'''

QUO_TS_USER='''
    CREATE TABLE quo_ts_user (
        uid uuid,
        quote text,
        ts int,
        value varint,
        PRIMARY KEY (uid,quote,ts)
    ) WITH CLUSTERING ORDER BY (quote asc, ts desc);
'''

QUO_TS_DATASOURCE='''
    CREATE TABLE quo_ts_datasource (
        did uuid,
        quote text,
        ts int,
        value varint,
        PRIMARY KEY (did,quote,ts)
    ) WITH CLUSTERING ORDER BY (quote asc, ts desc);
'''

QUO_TS_DATAPOINT='''
    CREATE TABLE quo_ts_datapoint (
        pid uuid,
        quote text,
        ts int,
        value varint,
        PRIMARY KEY (pid,quote,ts)
    ) WITH CLUSTERING ORDER BY (quote asc, ts desc);
'''

