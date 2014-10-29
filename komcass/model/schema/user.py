#coding: utf-8
'''
This file defines the cassandra statements for the creation of user related tables

'''

OBJECTS=['MST_USER',
         'MST_USER_INDEX_01',
         'MST_USER_INDEX_02',
         'MST_SIGNUP',
         'MST_SIGNUP_INDEX_01',
         'MST_SIGNUP_INDEX_02'
        ]

MST_USER='''
        CREATE TABLE mst_user (
            username text,
            uid uuid,
            password text,
            email text,
            segment int,
            state int,
            creation_date timestamp,
            PRIMARY KEY (username)
        );
    '''

MST_USER_INDEX_01='''
        CREATE INDEX ON mst_user (uid);
    '''

MST_USER_INDEX_02='''
        CREATE INDEX ON mst_user (email);
    '''

MST_SIGNUP='''
        CREATE TABLE mst_signup (
            username text,
            signup_code text,
            email text,
            creation_date timestamp,
            utilization_date timestamp,
            PRIMARY KEY (username)
        );
    '''

MST_SIGNUP_INDEX_01='''
        CREATE INDEX ON mst_signup (email);
    '''

MST_SIGNUP_INDEX_02='''
        CREATE INDEX ON mst_signup (signup_code);
    '''
