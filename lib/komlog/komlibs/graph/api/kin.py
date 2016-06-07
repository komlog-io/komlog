'''

kin.py

In this file we implement specific methods for working with
the kin graph layer

'''

import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import graph as cassapigraph
from komlog.komcass.model.orm import graph as ormgraph
from komlog.komlibs.graph.api import base as graphbase
from komlog.komlibs.graph.relations import edge, vertex
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid

def get_kin_relations(ido, depth_level=1):
    if not args.is_valid_uuid(ido):
        return None
    if not args.is_valid_int(depth_level):
        return None
    relations=[]
    for rel in graphbase.gen_get_outgoing_relations_from(ido=ido, edge_type_list=[edge.KIN_RELATION],path_edge_type_list=[edge.KIN_RELATION], depth_level=depth_level):
        relations.append({'id':rel.idd,'type':vertex.get_dest_vertex_type(rel.type),'params':rel.params})
    return relations

def set_kin_relation(ido, idd, vertex_type, params):
    if not args.is_valid_uuid(ido):
        return False
    if not args.is_valid_uuid(idd):
        return False
    if not args.is_valid_string(vertex_type):
        return False
    if not args.is_valid_dict(params):
        return False
    try:
        return graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type, params=params)
    except cassexcept.KomcassException:
        delete_kin_relation(ido=ido, idd=idd)
        raise

def delete_kin_relations(ido):
    if not args.is_valid_uuid(ido):
        return False
    for rel in graphbase.gen_get_outgoing_relations_from(ido=ido, edge_type_list=[edge.KIN_RELATION],path_edge_type_list=[edge.KIN_RELATION], depth_level=1):
        graphbase.delete_edge(ido=rel.ido, idd=rel.idd, edge_type=edge.KIN_RELATION)
    return True

def delete_kin_relation(ido, idd):
    if not args.is_valid_uuid(ido):
        return False
    if not args.is_valid_uuid(idd):
        return False
    return graphbase.delete_edge(ido=ido, idd=idd, edge_type=edge.KIN_RELATION)

def kin_widgets(ido, idd, params=None):
    ''' this function establishes kin relations between widgets on both directions '''
    if not args.is_valid_uuid(ido) or not args.is_valid_uuid(idd):
        return False
    if params and not args.is_valid_dict(params):
        return False
    vertex_type=vertex.WIDGET_WIDGET_RELATION
    rel_params=params if params else dict()
    try:
        if set_kin_relation(ido=ido, idd=idd, vertex_type=vertex_type, params=rel_params) and set_kin_relation(ido=idd, idd=ido, vertex_type=vertex_type, params=rel_params):
            return True
        else:
            delete_kin_relation(ido=ido, idd=idd)
            delete_kin_relation(ido=idd, idd=ido)
            return False
    except cassexcept.KomcassException:
        delete_kin_relation(ido=ido, idd=idd)
        delete_kin_relation(ido=idd, idd=ido)
        raise

def unkin_widgets(ido, idd):
    ''' this function removes the kin relations between widgets on both directions '''
    if not args.is_valid_uuid(ido) or not args.is_valid_uuid(idd):
        return False
    if delete_kin_relation(ido=ido, idd=idd) and delete_kin_relation(ido=idd, idd=ido):
        return True
    else:
        return False

def get_kin_widgets(ido):
    widgets=[]
    if not args.is_valid_uuid(ido):
        return widgets
    for widget in get_kin_relations(ido=ido):
        if widget['type']==vertex.WIDGET:
            widgets.append({'wid':widget['id'],'params':widget['params']})
    return widgets

