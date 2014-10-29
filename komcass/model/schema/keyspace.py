#coding: utf-8
'''
This file declares some parameters for the keyspace creation

'''

KEYSPACE = 'komlog'
REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1 }
