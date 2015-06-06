#coding:utf-8

'''
This library implements authorization mechanisms for shared elements


@date: 2015/03/08
@author: jcazor
'''

from komlibs.auth import permissions
from komlibs.graph.api import base as graphbase
from komlibs.graph.relations import edge

def authorize_get_datasource_config(uid,did):
    relations=[]
    for relation in graphbase.gen_get_outgoing_relations_from(ido=did,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.perm & permissions.CAN_READ:
            return True
        relations.append(relation)
    for circles in graphbase.gen_get_outgoing_relations_from(ido=uid,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        for relation in relations:
            if relation.idd==circles.idd and relation.perm & permissions.CAN_READ:
                return True
    return False

def authorize_get_datasource_data(uid,did,ii,ie):
    relations=[]
    for relation in graphbase.gen_get_outgoing_relations_from(ido=did,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.interval_init==ii and relation.interval_end==ie and relation.perm & permissions.CAN_READ:
            return True
        relations.append(relation)
    for circles in graphbase.gen_get_outgoing_relations_from(ido=uid,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        for relation in relations:
            if relation.idd==circles.idd and relation.interval_init==ii and relation.interval_end==ie and relation.perm & permissions.CAN_READ:
                return True
    return False

def authorize_get_datapoint_config(uid,pid):
    relations=[]
    for relation in graphbase.gen_get_outgoing_relations_from(ido=pid,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.perm & permissions.CAN_READ:
            return True
        relations.append(relation)
    for circles in graphbase.gen_get_outgoing_relations_from(ido=uid,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        for relation in relations:
            if relation.idd==circles.idd and relation.perm & permissions.CAN_READ:
                return True
    return False

def authorize_get_datapoint_data(uid,pid,ii,ie):
    relations=[]
    for relation in graphbase.gen_get_outgoing_relations_from(ido=pid,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.interval_init==ii and relation.interval_end==ie and relation.perm & permissions.CAN_READ:
            return True
        relations.append(relation)
    for circles in graphbase.gen_get_outgoing_relations_from(ido=uid,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        for relation in relations:
            if relation.idd==circles.idd and relation.interval_init==ii and relation.interval_end==ie and relation.perm & permissions.CAN_READ:
                return True
    return False

def authorize_get_snapshot_config(uid,nid):
    relations=[]
    for relation in graphbase.gen_get_outgoing_relations_from(ido=nid,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        if relation.idd==uid and relation.perm & permissions.CAN_READ:
            return True
        relations.append(relation)
    for circles in graphbase.gen_get_outgoing_relations_from(ido=uid,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
        for relation in relations:
            if relation.idd==circles.idd and relation.perm & permissions.CAN_READ:
                return True
    return False

