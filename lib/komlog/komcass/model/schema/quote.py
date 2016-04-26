#coding: utf-8
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
]

QUO_USER='''
    CREATE TABLE quo_user (
        uid uuid,
        quote text,
        value int,
        PRIMARY KEY (uid,quote)
    );
'''

QUO_AGENT='''
    CREATE TABLE quo_agent (
        aid uuid,
        quote text,
        value int,
        PRIMARY KEY (aid,quote)
    );
'''

QUO_DATASOURCE='''
    CREATE TABLE quo_datasource (
        did uuid,
        quote text,
        value int,
        PRIMARY KEY (did,quote)
    );
'''

QUO_DATAPOINT='''
    CREATE TABLE quo_datapoint (
        pid uuid,
        quote text,
        value int,
        PRIMARY KEY (pid,quote)
    );
'''

QUO_WIDGET='''
    CREATE TABLE quo_widget (
        wid uuid,
        quote text,
        value int,
        PRIMARY KEY (wid,quote)
    );
'''

QUO_DASHBOARD='''
    CREATE TABLE quo_dashboard (
        bid uuid,
        quote text,
        value int,
        PRIMARY KEY (bid,quote)
    );
'''

QUO_CIRCLE='''
    CREATE TABLE quo_circle (
        cid uuid,
        quote text,
        value int,
        PRIMARY KEY (cid,quote)
    );
'''

