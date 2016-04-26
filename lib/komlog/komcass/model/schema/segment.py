#coding: utf-8
'''
This file defines the cassandra statements for the creation of segments related tables

'''

OBJECTS=[
    'PRM_USER_SEGMENT_QUO',
]

PRM_USER_SEGMENT_QUO='''
    CREATE TABLE prm_user_segment_quo (
        sid int,
        quote text,
        value int,
        PRIMARY KEY (sid,quote)
    );
'''
