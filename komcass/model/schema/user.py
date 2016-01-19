'''
This file defines the cassandra statements for the creation of user related tables

'''

OBJECTS=['MST_USER',
         'MST_USER_INDEX_01',
         'MST_USER_INDEX_02',
         'MST_SIGNUP',
         'MST_SIGNUP_INDEX_01',
         'MST_SIGNUP_INDEX_02',
         'DAT_INVITATION',
         'DAT_INVITATION_REQUEST',
         'DAT_INVITATION_REQUEST_INDEX_01',
        ]

MST_USER='''
        CREATE TABLE mst_user (
            username text,
            uid uuid,
            password text,
            email text,
            segment int,
            state int,
            creation_date timeuuid,
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
            creation_date timeuuid,
            utilization_date timeuuid,
            PRIMARY KEY (username)
        );
    '''

MST_SIGNUP_INDEX_01='''
        CREATE INDEX ON mst_signup (email);
    '''

MST_SIGNUP_INDEX_02='''
        CREATE INDEX ON mst_signup (signup_code);
    '''

DAT_INVITATION='''
        CREATE TABLE dat_invitation (
            inv_id uuid,
            date timeuuid,
            state int,
            tran_id uuid,
            PRIMARY KEY (inv_id,date)
        );
    '''

DAT_INVITATION_REQUEST='''
        CREATE TABLE dat_invitation_request (
            email text,
            date timeuuid,
            state int,
            inv_id uuid,
            PRIMARY KEY (email)
        );
    '''

DAT_INVITATION_REQUEST_INDEX_01='''
        CREATE INDEX ON dat_invitation_request (state);
    '''

