'''
This file defines the cassandra statements for the creation of user related tables

'''

OBJECTS=[
    'MST_USER',
    'MST_USER_INDEX_01',
    'MST_USER_INDEX_02',
    'MST_USER_BILLING_INFO',
    'MST_USER_BILLING_INFO_INDEX_01',
    'MST_USER_STRIPE_INFO',
    'MST_SIGNUP',
    'MST_SIGNUP_INDEX_01',
    'MST_SIGNUP_INDEX_02',
    'MST_INVITATION',
    'DAT_INVITATION_REQUEST',
    'DAT_INVITATION_REQUEST_INDEX_01',
    'DAT_FORGET_REQUEST',
    'DAT_FORGET_REQUEST_INDEX_01',
    'DAT_FORGET_REQUEST_INDEX_02',
    'MST_PENDING_HOOK',
    'MST_PENDING_HOOK_INDEX_01',
]

MST_USER='''
    CREATE TABLE mst_user (
        username text,
        uid uuid,
        password blob,
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

MST_USER_BILLING_INFO='''
    CREATE TABLE mst_user_billing_info (
        uid                 uuid,
        billing_day         int,
        last_billing        timeuuid,
        PRIMARY KEY (uid)
    );
'''

MST_USER_BILLING_INFO_INDEX_01='''
    CREATE INDEX ON mst_user_billing_info (billing_day);
'''

MST_USER_STRIPE_INFO='''
    CREATE TABLE mst_user_stripe_info (
        uid                 uuid,
        stripe_id           text,
        PRIMARY KEY (uid)
    );
'''

MST_SIGNUP='''
    CREATE TABLE mst_signup (
        username text,
        email text,
        code text,
        inv_id text,
        creation_date timeuuid,
        utilization_date timeuuid,
        PRIMARY KEY (username)
    );
'''

MST_SIGNUP_INDEX_01='''
    CREATE INDEX ON mst_signup (email);
'''

MST_SIGNUP_INDEX_02='''
    CREATE INDEX ON mst_signup (code);
'''

MST_INVITATION='''
    CREATE TABLE mst_invitation (
        inv_id text,
        creation_date timeuuid,
        state int,
        count int,
        max_count int,
        active_from timeuuid,
        active_until timeuuid,
        PRIMARY KEY (inv_id)
    );
'''

DAT_INVITATION_REQUEST='''
    CREATE TABLE dat_invitation_request (
        email text,
        date timeuuid,
        state int,
        inv_id text,
        PRIMARY KEY (email)
    );
'''

DAT_INVITATION_REQUEST_INDEX_01='''
    CREATE INDEX ON dat_invitation_request (state);
'''

DAT_FORGET_REQUEST='''
    CREATE TABLE dat_forget_request (
        code uuid,
        date timeuuid,
        state int,
        uid uuid,
        PRIMARY KEY (code)
    );
'''

DAT_FORGET_REQUEST_INDEX_01='''
    CREATE INDEX ON dat_forget_request (state);
'''

DAT_FORGET_REQUEST_INDEX_02='''
    CREATE INDEX ON dat_forget_request (uid);
'''

MST_PENDING_HOOK='''
    CREATE TABLE mst_pending_hook(
        uid uuid,
        uri text,
        sid uuid,
        PRIMARY KEY (uid, uri, sid)
    );
'''

MST_PENDING_HOOK_INDEX_01='''
    CREATE INDEX ON mst_pending_hook(sid);
'''

