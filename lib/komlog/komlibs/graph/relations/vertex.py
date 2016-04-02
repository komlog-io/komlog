'''
vertex.py

This file enumerates the different vertex types that can be related,
for example a relation USER-USER, or USER-DATASOURCE, etc
This helps us identify the object type of every relation.

'''

def get_origin_vertex_type(rel):
    return rel[0]

def get_dest_vertex_type(rel):
    return rel[2]

def get_relation_type(origin, dest):
    return '2'.join((origin,dest))


USER                                 = 'u'
AGENT                                = 'a'
DATASOURCE                           = 'd'
DATAPOINT                            = 'p'
WIDGET                               = 'w'
DASHBOARD                            = 'b'
SNAPSHOT                             = 'n'
CIRCLE                               = 'c'
VOID                                 = 'v'


USER_USER_RELATION                   = 'u2u'
USER_AGENT_RELATION                  = 'u2a'
USER_DATASOURCE_RELATION             = 'u2d'
USER_DATAPOINT_RELATION              = 'u2p'
USER_WIDGET_RELATION                 = 'u2w'
USER_DASHBOARD_RELATION              = 'u2b'
USER_SNAPSHOT_RELATION               = 'u2n'
USER_CIRCLE_RELATION                 = 'u2c'
USER_VOID_RELATION                   = 'u2v'

AGENT_USER_RELATION                  = 'a2u'
AGENT_AGENT_RELATION                 = 'a2a'
AGENT_DATASOURCE_RELATION            = 'a2d'
AGENT_DATAPOINT_RELATION             = 'a2p'
AGENT_WIDGET_RELATION                = 'a2w'
AGENT_DASHBOARD_RELATION             = 'a2b'
AGENT_SNAPSHOT_RELATION              = 'a2n'
AGENT_CIRCLE_RELATION                = 'a2c'
AGENT_VOID_RELATION                  = 'a2v'

DATASOURCE_USER_RELATION             = 'd2u'
DATASOURCE_AGENT_RELATION            = 'd2a'
DATASOURCE_DATASOURCE_RELATION       = 'd2d'
DATASOURCE_DATAPOINT_RELATION        = 'd2p'
DATASOURCE_WIDGET_RELATION           = 'd2w'
DATASOURCE_DASHBOARD_RELATION        = 'd2b'
DATASOURCE_SNAPSHOT_RELATION         = 'd2n'
DATASOURCE_CIRCLE_RELATION           = 'd2c'
DATASOURCE_VOID_RELATION             = 'd2v'

DATAPOINT_USER_RELATION              = 'p2u'
DATAPOINT_AGENT_RELATION             = 'p2a'
DATAPOINT_DATASOURCE_RELATION        = 'p2d'
DATAPOINT_DATAPOINT_RELATION         = 'p2p'
DATAPOINT_WIDGET_RELATION            = 'p2w'
DATAPOINT_DASHBOARD_RELATION         = 'p2b'
DATAPOINT_SNAPSHOT_RELATION          = 'p2n'
DATAPOINT_CIRCLE_RELATION            = 'p2c'
DATAPOINT_VOID_RELATION              = 'p2v'

WIDGET_USER_RELATION                 = 'w2u'
WIDGET_AGENT_RELATION                = 'w2a'
WIDGET_DATASOURCE_RELATION           = 'w2d'
WIDGET_DATAPOINT_RELATION            = 'w2p'
WIDGET_WIDGET_RELATION               = 'w2w'
WIDGET_DASHBOARD_RELATION            = 'w2b'
WIDGET_SNAPSHOT_RELATION             = 'w2n'
WIDGET_CIRCLE_RELATION               = 'w2c'
WIDGET_VOID_RELATION                 = 'w2v'

DASHBOARD_USER_RELATION              = 'b2u'
DASHBOARD_AGENT_RELATION             = 'b2a'
DASHBOARD_DATASOURCE_RELATION        = 'b2d'
DASHBOARD_DATAPOINT_RELATION         = 'b2p'
DASHBOARD_WIDGET_RELATION            = 'b2w'
DASHBOARD_DASHBOARD_RELATION         = 'b2b'
DASHBOARD_SNAPSHOT_RELATION          = 'b2n'
DASHBOARD_CIRCLE_RELATION            = 'b2c'
DASHBOARD_VOID_RELATION              = 'b2v'

SNAPSHOT_USER_RELATION               = 'n2u'
SNAPSHOT_AGENT_RELATION              = 'n2a'
SNAPSHOT_DATASOURCE_RELATION         = 'n2d'
SNAPSHOT_DATAPOINT_RELATION          = 'n2p'
SNAPSHOT_WIDGET_RELATION             = 'n2w'
SNAPSHOT_DASHBOARD_RELATION          = 'n2b'
SNAPSHOT_SNAPSHOT_RELATION           = 'n2n'
SNAPSHOT_CIRCLE_RELATION             = 'n2c'
SNAPSHOT_VOID_RELATION               = 'n2v'

CIRCLE_USER_RELATION                 = 'c2u'
CIRCLE_AGENT_RELATION                = 'c2a'
CIRCLE_DATASOURCE_RELATION           = 'c2d'
CIRCLE_DATAPOINT_RELATION            = 'c2p'
CIRCLE_WIDGET_RELATION               = 'c2w'
CIRCLE_DASHBOARD_RELATION            = 'c2b'
CIRCLE_SNAPSHOT_RELATION             = 'c2n'
CIRCLE_CIRCLE_RELATION               = 'c2c'
CIRCLE_VOID_RELATION                 = 'c2v'

VOID_USER_RELATION                 = 'v2u'
VOID_AGENT_RELATION                = 'v2a'
VOID_DATASOURCE_RELATION           = 'v2d'
VOID_DATAPOINT_RELATION            = 'v2p'
VOID_WIDGET_RELATION               = 'v2w'
VOID_DASHBOARD_RELATION            = 'v2b'
VOID_SNAPSHOT_RELATION             = 'v2n'
VOID_CIRCLE_RELATION               = 'v2c'
VOID_VOID_RELATION                 = 'v2v'

