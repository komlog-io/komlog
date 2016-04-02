'''
This file defines the cassandra statements for the creation of agent related tables

'''

OBJECTS=['MST_AGENT',
         'MST_AGENT_INDEX_01',
         'MST_AGENT_PUBKEY',
         'MST_AGENT_CHALLENGE',
        ]

MST_AGENT='''
        CREATE TABLE mst_agent (
            aid uuid,
            uid uuid,
            agentname text,
            pubkey blob,
            version text,
            state int,
            creation_date timeuuid,
            PRIMARY KEY (aid)
        );
    '''

MST_AGENT_INDEX_01='''
        CREATE INDEX ON mst_agent (uid);
    '''

MST_AGENT_PUBKEY='''
        CREATE TABLE mst_agent_pubkey (
            uid uuid,
            pubkey blob,
            aid uuid,
            state int,
            PRIMARY KEY (uid,pubkey)
        );
    '''

MST_AGENT_CHALLENGE='''
        CREATE TABLE mst_agent_challenge (
            aid uuid,
            challenge blob,
            generated timeuuid,
            validated timeuuid,
            PRIMARY KEY (aid,challenge)
        );
    '''
