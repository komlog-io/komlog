'''
This file defines the cassandra statements for the creation of graph related tables

'''
from komcass.model.schema import keyspace

OBJECTS=['GR_MEMBERIN',
         'GR_MEMBEROUT',
         'GR_BOUNDED_SHAREIN',
         'GR_BOUNDED_SHAREOUT',
        ]

GR_MEMBERIN='''
        CREATE TABLE gr_member_in (
            idd uuid,
            ido uuid,
            type text,
            creation_date timeuuid,
            PRIMARY KEY (idd,ido)
        );
    '''

GR_MEMBEROUT='''
        CREATE TABLE gr_member_out (
            ido uuid,
            idd uuid,
            type text,
            creation_date timeuuid,
            PRIMARY KEY (ido,idd)
        );
    '''

GR_BOUNDED_SHAREIN='''
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

GR_BOUNDED_SHAREOUT='''
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

