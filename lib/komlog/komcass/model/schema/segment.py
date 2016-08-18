'''
This file defines the cassandra statements for the creation of segments related tables

'''

OBJECTS=[
    'MST_USER_SEGMENT',
    'PRM_USER_SEGMENT_QUO',
]


MST_USER_SEGMENT='''
    CREATE TABLE mst_user_segment (
        sid int,
        description text,
        PRIMARY KEY (sid)
    );
'''

PRM_USER_SEGMENT_QUO='''
    CREATE TABLE prm_user_segment_quo (
        sid int,
        quote text,
        value varint,
        PRIMARY KEY (sid,quote)
    );
'''
