'''
This file defines the cassandra statements for the creation of graph related tables

'''
from komcass.model.schema import keyspace

OBJECTS=[
         'GR_URI_IN',
         'GR_URI_OUT',
         'GR_KIN_IN',
         'GR_KIN_OUT',
        ]

GR_URI_IN='''
        CREATE TABLE gr_uri_in (
            idd uuid,
            ido uuid,
            type text,
            creation_date timeuuid,
            uri text,
            PRIMARY KEY (idd,ido)
        );
    '''

GR_URI_OUT='''
        CREATE TABLE gr_uri_out (
            ido uuid,
            idd uuid,
            type text,
            creation_date timeuuid,
            uri text,
            PRIMARY KEY (ido,idd)
        );
    '''

GR_KIN_IN='''
        CREATE TABLE gr_kin_in (
            idd uuid,
            ido uuid,
            type text,
            creation_date timeuuid,
            params map <text,text>,
            PRIMARY KEY (idd,ido)
        );
    '''

GR_KIN_OUT='''
        CREATE TABLE gr_kin_out (
            ido uuid,
            idd uuid,
            type text,
            creation_date timeuuid,
            params map <text,text>,
            PRIMARY KEY (ido,idd)
        );
    '''

