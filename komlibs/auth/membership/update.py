#coding: utf-8
'''
update.py 

This file implements functions to update authorization related to membership

@author: jcazor
@date: 2015/03/15

'''

from komcass.api import circle as cassapicircle
from komlibs.gestaccount.circle import types as circletypes
from komlibs.auth import operations, permissions
from komlibs.graph import api as graphapi
from komlibs.graph.relations import vertex, edge

update_funcs = {
                operations.NEW_CIRCLE: ['new_circle'],
                operations.UPDATE_CIRCLE_MEMBERS: ['update_circle_members'],
}

def get_update_funcs(operation):
    try:
        return update_funcs[operation]
    except KeyError:
        return []

def new_circle(params):
    if not 'cid' in params:
        return False
    cid=params['cid']
    circle=cassapicircle.get_circle(cid=cid)
    if circle:
        if circle.type==circletypes.USERS_CIRCLE:
            for member in circle.members:
                graphapi.set_member_edge(ido=member, idd=cid, vertex_type=vertex.USER_CIRCLE_RELATION)
        else:
            return False
        return True
    else:
        #nothing to do
        return True

def update_circle_members(params):
    if not 'cid' in params:
        return False
    cid=params['cid']
    circle=cassapicircle.get_circle(cid=cid)
    if circle:
        if circle.type==circletypes.USERS_CIRCLE:
            vertex_type=vertex.USER_CIRCLE_RELATION
        else:
            return False
        existent_members=set()
        for relation in graphapi.gen_get_incoming_relations_at(idd=circle.cid,edge_type_list=[edge.MEMBER_RELATION], depth_level=1):
            existent_members.add(relation.ido)
        members_to_add=circle.members-existent_members
        members_to_delete=existent_members-circle.members
        for member in members_to_add:
            graphapi.set_member_edge(ido=member, idd=circle.cid, vertex_type=vertex_type)
        for member in members_to_delete:
            graphapi.delete_edge(ido=member, idd=circle.cid, edge_type=edge.MEMBER_RELATION)
        return True
    else:
        #nothing to do
        return True

