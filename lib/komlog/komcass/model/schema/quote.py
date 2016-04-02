#coding: utf-8
'''
This file defines the cassandra statements for the creation of quotes related tables

'''

OBJECTS=['QUO_USER',
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
            quotes map<text,text>,
            PRIMARY KEY (uid)
        );
    '''

QUO_AGENT='''
        CREATE TABLE quo_agent (
            aid uuid,
            quotes map<text,text>,
            PRIMARY KEY (aid)
        );
    '''

QUO_DATASOURCE='''
        CREATE TABLE quo_datasource (
            did uuid,
            quotes map<text,text>,
            PRIMARY KEY (did)
        );
    '''

QUO_DATAPOINT='''
        CREATE TABLE quo_datapoint (
            pid uuid,
            quotes map<text,text>,
            PRIMARY KEY (pid)
        );
    '''

QUO_WIDGET='''
        CREATE TABLE quo_widget (
            wid uuid,
            quotes map<text,text>,
            PRIMARY KEY (wid)
        );
    '''

QUO_DASHBOARD='''
        CREATE TABLE quo_dashboard (
            bid uuid,
            quotes map<text,text>,
            PRIMARY KEY (bid)
        );
    '''

QUO_CIRCLE='''
        CREATE TABLE quo_circle (
            cid uuid,
            quotes map<text,text>,
            PRIMARY KEY (cid)
        );
    '''

