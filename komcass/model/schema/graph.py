'''
This file defines the cassandra statements for the creation of graph related tables

'''
from komcass.model.schema import keyspace

OBJECTS=['GR_MEMBER_IN',
         'GR_MEMBER_OUT',
         'GR_BOUNDED_SHARE_IN',
         'GR_BOUNDED_SHARE_OUT',
         'GR_URI_IN',
         'GR_URI_OUT',
        ]

GR_MEMBER_IN='''
        CREATE TABLE gr_member_in (
            idd uuid,
            ido uuid,
            type text,
            creation_date timeuuid,
            PRIMARY KEY (idd,ido)
        );
    '''

GR_MEMBER_OUT='''
        CREATE TABLE gr_member_out (
            ido uuid,
            idd uuid,
            type text,
            creation_date timeuuid,
            PRIMARY KEY (ido,idd)
        );
    '''

GR_BOUNDED_SHARE_IN='''
        CREATE TABLE gr_bounded_share_in (
            idd uuid,
            ido uuid,
            type text,
            creation_date timeuuid,
            perm int,
            interval_init timeuuid,
            interval_end timeuuid,
            PRIMARY KEY (idd,ido)
        );
    '''

GR_BOUNDED_SHARE_OUT='''
        CREATE TABLE gr_bounded_share_out (
            ido uuid,
            idd uuid,
            type text,
            creation_date timeuuid,
            perm int,
            interval_init timeuuid,
            interval_end timeuuid,
            PRIMARY KEY (ido,idd)
        );
    '''

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

