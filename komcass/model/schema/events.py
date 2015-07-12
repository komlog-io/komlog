'''
This file defines the cassandra statements for the creation of datasource related tables

'''
from komcass.model.schema import keyspace

OBJECTS=[
         'DAT_USER_EVENTS',
        ]

DAT_USER_EVENTS='''
        CREATE TABLE dat_user_events (
            uid uuid,
            date timeuuid,
            active boolean,
            priority int,
            type int,
            parameters map <text,text>,
            PRIMARY KEY (uid,date)
        );
    '''

