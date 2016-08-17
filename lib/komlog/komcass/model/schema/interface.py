#coding: utf-8
'''
This file defines the cassandra statements for the creation of interface related tables

'''

OBJECTS=[
    'IF_USER_DENY',
    'IF_TS_USER_DENY'
]

IF_USER_DENY='''
        CREATE TABLE if_user_deny (
            uid uuid,
            interface text,
            content text,
            PRIMARY KEY (uid,interface)
        );
    '''

IF_TS_USER_DENY='''
    CREATE TABLE if_ts_user_deny (
        uid uuid,
        interface text,
        ts int,
        content text,
        PRIMARY KEY (uid,interface,ts)
    ) WITH CLUSTERING ORDER BY (interface asc, ts desc);
'''

