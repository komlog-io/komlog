#coding: utf-8
'''
This file defines the cassandra statements for the creation of segments related tables

'''

OBJECTS=['PRM_USER_SEGMENT',
         'PRM_USER_SEGMENT_INDEX_01'
        ]

PRM_USER_SEGMENT='''
        CREATE TABLE prm_user_segment (
            sid int,
            segmentname text,
            params map<text,text>,
            PRIMARY KEY (sid)
        );
    '''

PRM_USER_SEGMENT_INDEX_01='''
        CREATE INDEX ON prm_user_segment (segmentname);
    '''
