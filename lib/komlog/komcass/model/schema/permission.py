'''
This file defines the cassandra statements for the creation of permission related tables

'''

OBJECTS=[
    'PERM_USER_AGENT',
    'PERM_USER_DATASOURCE',
    'PERM_USER_DATAPOINT',
    'PERM_USER_WIDGET',
    'PERM_USER_DASHBOARD',
    'PERM_USER_SNAPSHOT',
    'PERM_USER_CIRCLE',
    'PERM_USER_SHARED_URI',
    'PERM_USER_SHARED_URI_WITH_ME',
]

PERM_USER_AGENT='''
    CREATE TABLE perm_user_agent (
        uid uuid,
        aid uuid,
        perm int,
        PRIMARY KEY (uid,aid)
    );
'''

PERM_USER_DATASOURCE='''
    CREATE TABLE perm_user_datasource (
        uid uuid,
        did uuid,
        perm int,
        PRIMARY KEY (uid,did)
    );
'''

PERM_USER_DATAPOINT='''
    CREATE TABLE perm_user_datapoint (
        uid uuid,
        pid uuid,
        perm int,
        PRIMARY KEY (uid,pid)
    );
'''

PERM_USER_WIDGET='''
    CREATE TABLE perm_user_widget (
        uid uuid,
        wid uuid,
        perm int,
        PRIMARY KEY (uid,wid)
    );
'''

PERM_USER_DASHBOARD='''
    CREATE TABLE perm_user_dashboard (
        uid uuid,
        bid uuid,
        perm int,
        PRIMARY KEY (uid,bid)
    );
'''

PERM_USER_SNAPSHOT='''
    CREATE TABLE perm_user_snapshot (
        uid uuid,
        nid uuid,
        perm int,
        PRIMARY KEY (uid,nid)
    );
'''

PERM_USER_CIRCLE='''
    CREATE TABLE perm_user_circle (
        uid uuid,
        cid uuid,
        perm int,
        PRIMARY KEY (uid,cid)
    );
'''

PERM_USER_SHARED_URI='''
    CREATE TABLE perm_user_shared_uri (
        uid uuid,
        dest_uid uuid,
        uri text,
        perm int,
        PRIMARY KEY (uid,dest_uid,uri)
    );
'''

PERM_USER_SHARED_URI_WITH_ME='''
    CREATE TABLE perm_user_shared_uri_with_me (
        uid uuid,
        owner_uid uuid,
        uri text,
        perm int,
        PRIMARY KEY (uid,owner_uid,uri)
    );
'''

