#coding: utf-8
'''
This file defines the cassandra statements for the creation of interface related tables

'''

OBJECTS=['IF_USER_DENY'
        ]

IF_USER_DENY='''
        CREATE TABLE if_user_deny (
            uid uuid,
            interface text,
            perm text,
            PRIMARY KEY (uid,interface)
        );
    '''

