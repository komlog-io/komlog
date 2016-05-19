'''
This file defines the cassandra statements for the creation of quotes related tables

'''

OBJECTS=[
    'AUTH_TICKET',
    'AUTH_TICKET_INDEX_01',
    'AUTH_TICKET_EXPIRED',
    'AUTH_TICKET_EXPIRED_INDEX_01',
]

AUTH_TICKET='''
    CREATE TABLE auth_ticket (
        tid uuid,
        date timeuuid,
        uid uuid,
        expires timeuuid,
        allowed_uids set<uuid>,
        allowed_cids set<uuid>,
        resources set<uuid>,
        permissions map<uuid,int>,
        interval_init timeuuid,
        interval_end timeuuid,
        PRIMARY KEY (tid)
    );
'''

AUTH_TICKET_INDEX_01='''
    CREATE INDEX ON auth_ticket (uid);
'''

AUTH_TICKET_EXPIRED='''
    CREATE TABLE auth_ticket_expired (
        tid uuid,
        date timeuuid,
        uid uuid,
        expires timeuuid,
        allowed_uids set<uuid>,
        allowed_cids set<uuid>,
        resources set<uuid>,
        permissions map<uuid,int>,
        interval_init timeuuid,
        interval_end timeuuid,
        PRIMARY KEY (tid)
    );
'''

AUTH_TICKET_EXPIRED_INDEX_01='''
    CREATE INDEX ON auth_ticket_expired (uid);
'''

