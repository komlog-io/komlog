#coding:utf-8

'''
This library implements authorization mechanisms for shared elements


@date: 2015/03/08
@author: jcazor
'''

from komlibs.auth import permissions
from komlibs.graph import api as graphapi
from komlibs.graph.relations import edge

def authorize_get_datasource_config(uid,did):
    for relation in graphapi.gen_get_outgoing_relations_from(ido=did,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.perm & permissions.CAN_READ:
            return True
    return False

def authorize_get_datasource_data(uid,did,ii,ie):
    for relation in graphapi.gen_get_outgoing_relations_from(ido=did,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.interval_init==ii and relation.interval_end==ie and relation.perm & permissions.CAN_READ:
            return True
    return False

def authorize_get_datapoint_config(uid,pid):
    for relation in graphapi.gen_get_outgoing_relations_from(ido=pid,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.perm & permissions.CAN_READ:
            return True
    return False

def authorize_get_datapoint_data(uid,pid,ii,ie):
    for relation in graphapi.gen_get_outgoing_relations_from(ido=pid,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.interval_init==ii and relation.interval_end==ie and relation.perm & permissions.CAN_READ:
            return True
    return False

def authorize_get_snapshot_config(uid,nid):
    for relation in graphapi.gen_get_outgoing_relations_from(ido=nid,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.perm & permissions.CAN_READ:
            return True
    return False

