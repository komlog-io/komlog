'''
This file defines the cassandra statements for the creation of segments related tables

'''

OBJECTS=[
    'MST_USER_SEGMENT',
    'DAT_USER_SEGMENT_TRANSITION',
    'PRM_USER_SEGMENT_QUO',
    'PRM_USER_SEGMENT_ALLOWED_TRANSITIONS',
    'PRM_USER_SEGMENT_FARE',
]


MST_USER_SEGMENT='''
    CREATE TABLE mst_user_segment (
        sid int,
        description text,
        PRIMARY KEY (sid)
    );
'''

DAT_USER_SEGMENT_TRANSITION='''
    CREATE TABLE dat_user_segment_transition (
        uid             uuid,
        date            timeuuid,
        sid             int,
        previous_sid    int,
        PRIMARY KEY     (uid,date)
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

PRM_USER_SEGMENT_ALLOWED_TRANSITIONS='''
    CREATE TABLE prm_user_segment_allowed_transitions (
        sid         int,
        sids        set<int>,
        PRIMARY KEY (sid)
    );
'''

PRM_USER_SEGMENT_FARE='''
    CREATE TABLE prm_user_segment_fare (
        sid         int,
        amount      decimal,
        currency    text,
        frequency   text,
        PRIMARY KEY (sid)
    );
'''

