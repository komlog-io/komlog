#coding: utf-8
'''
This file defines the cassandra statements for the creation of agent related tables

'''

OBJECTS=['MST_AGENT',
         'MST_AGENT_INDEX_01'
        ]

MST_AGENT='''
        CREATE TABLE mst_agent (
            aid uuid,
            uid uuid,
            agentname text,
            pubkey text,
            version text,
            state int,
            creation_date timestamp,
            PRIMARY KEY (aid)
        );
    '''

MST_AGENT_INDEX_01='''
        CREATE INDEX ON mst_agent (uid);
    '''

