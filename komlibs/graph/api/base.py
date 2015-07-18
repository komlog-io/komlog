'''

api.py

In this file we implement the necessary methods for working with
graph vertex and edges

'''

from komcass.api import graph as cassapigraph
from komcass.model.orm import graph as ormgraph
from komlibs.graph.relations import edge, vertex
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komfig import logger

def gen_get_outgoing_relations_from(ido, edge_type_list=edge.ALL, path_edge_type_list=edge.ALL, depth_level=-1):
    ''' generator '''
    if args.is_valid_uuid(ido) and isinstance(edge_type_list,list) and isinstance(path_edge_type_list,list):
        current_level_vertices=[ido]
        all_evaluated_vertices=[ido]
        found_relations=[]
        next_level_vertices=[]
        while not depth_level==0:
            for vertex in current_level_vertices:
                for edge_type in edge_type_list:
                    current_level_relations=[]
                    if edge_type==edge.MEMBER_RELATION:
                        current_level_relations=cassapigraph.get_member_out_relations(ido=vertex)
                    elif edge_type==edge.BOUNDED_SHARE_RELATION:
                        current_level_relations=cassapigraph.get_bounded_share_out_relations(ido=vertex)
                    elif edge_type==edge.URI_RELATION:
                        current_level_relations=cassapigraph.get_uri_out_relations(ido=vertex)
                    elif edge_type==edge.KIN_RELATION:
                        current_level_relations=cassapigraph.get_kin_out_relations(ido=vertex)
                    for current_level_relation in current_level_relations:
                        if not current_level_relation in found_relations:
                            found_relations.append(current_level_relation)
                            yield current_level_relation
                if depth_level!=1:
                    for edge_type in path_edge_type_list:
                        connected_vertices=[]
                        if edge_type==edge.MEMBER_RELATION:
                            connected_vertices=cassapigraph.get_member_out_vertices(ido=vertex)
                        elif edge_type==edge.BOUNDED_SHARE_RELATION:
                            connected_vertices=cassapigraph.get_bounded_share_out_vertices(ido=vertex)
                        elif edge_type==edge.URI_RELATION:
                            connected_vertices=cassapigraph.get_uri_out_vertices(ido=vertex)
                        elif edge_type==edge.KIN_RELATION:
                            connected_vertices=cassapigraph.get_kin_out_vertices(ido=vertex)
                        for connected_vertex in connected_vertices:
                            if not connected_vertex in all_evaluated_vertices:
                                all_evaluated_vertices.append(connected_vertex)
                                next_level_vertices.append(connected_vertex)
            if next_level_vertices==[]:
                break
            else:
                current_level_vertices=next_level_vertices
                next_level_vertices=[]
                depth_level-=1

def gen_get_incoming_relations_at(idd, edge_type_list=edge.ALL, path_edge_type_list=edge.ALL, depth_level=-1):
    ''' generator '''
    if args.is_valid_uuid(idd) and isinstance(edge_type_list,list) and isinstance(path_edge_type_list,list):
        current_level_vertices=[idd]
        all_evaluated_vertices=[idd]
        found_relations=[]
        next_level_vertices=[]
        while not depth_level==0:
            for vertex in current_level_vertices:
                for edge_type in edge_type_list:
                    current_level_relations=[]
                    if edge_type==edge.MEMBER_RELATION:
                        current_level_relations=cassapigraph.get_member_in_relations(idd=vertex)
                    elif edge_type==edge.BOUNDED_SHARE_RELATION:
                        current_level_relations=cassapigraph.get_bounded_share_in_relations(idd=vertex)
                    elif edge_type==edge.URI_RELATION:
                        current_level_relations=cassapigraph.get_uri_in_relations(idd=vertex)
                    elif edge_type==edge.KIN_RELATION:
                        current_level_relations=cassapigraph.get_kin_in_relations(idd=vertex)
                    for current_level_relation in current_level_relations:
                        if not current_level_relation in found_relations:
                            found_relations.append(current_level_relation)
                            yield current_level_relation
                if depth_level!=1:
                    for edge_type in path_edge_type_list:
                        connected_vertices=[]
                        if edge_type==edge.MEMBER_RELATION:
                            connected_vertices=cassapigraph.get_member_in_vertices(idd=vertex)
                        elif edge_type==edge.BOUNDED_SHARE_RELATION:
                            connected_vertices=cassapigraph.get_bounded_share_in_vertices(idd=vertex)
                        elif edge_type==edge.URI_RELATION:
                            connected_vertices=cassapigraph.get_uri_in_vertices(idd=vertex)
                        elif edge_type==edge.KIN_RELATION:
                            connected_vertices=cassapigraph.get_kin_in_vertices(idd=vertex)
                        for connected_vertex in connected_vertices:
                            if not connected_vertex in all_evaluated_vertices:
                                all_evaluated_vertices.append(connected_vertex)
                                next_level_vertices.append(connected_vertex)
            if next_level_vertices==[]:
                break
            else:
                current_level_vertices=next_level_vertices
                next_level_vertices=[]
                depth_level-=1

def delete_edge(ido, idd, edge_type):
    if args.is_valid_uuid(ido) and args.is_valid_uuid(idd) and args.is_valid_int(edge_type):
        if edge_type==edge.MEMBER_RELATION:
            cassapigraph.delete_member_out_relation(ido=ido,idd=idd)
            cassapigraph.delete_member_in_relation(ido=ido,idd=idd)
            return True
        elif edge_type==edge.BOUNDED_SHARE_RELATION:
            cassapigraph.delete_bounded_share_out_relation(ido=ido,idd=idd)
            cassapigraph.delete_bounded_share_in_relation(ido=ido,idd=idd)
            return True
        elif edge_type==edge.URI_RELATION:
            cassapigraph.delete_uri_out_relation(ido=ido,idd=idd)
            cassapigraph.delete_uri_in_relation(ido=ido,idd=idd)
            return True
        elif edge_type==edge.KIN_RELATION:
            cassapigraph.delete_kin_out_relation(ido=ido,idd=idd)
            cassapigraph.delete_kin_in_relation(ido=ido,idd=idd)
            return True
        else:
            return False
    else:
        return False

def set_member_edge(ido, idd, vertex_type):
    if args.is_valid_uuid(ido) and args.is_valid_uuid(idd) and args.is_valid_string(vertex_type):
        now=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido, idd=idd, type=vertex_type, creation_date=now)
        if cassapigraph.insert_member_out_relation(relation) and cassapigraph.insert_member_in_relation(relation):
            return True
        else:
            delete_edge(ido=ido, idd=idd, edge_type=edge.MEMBER_RELATION)
            return False
    else:
        return False

def set_bounded_share_edge(ido, idd, vertex_type, perm, interval_init, interval_end):
    if args.is_valid_uuid(ido) and args.is_valid_uuid(idd) and args.is_valid_string(vertex_type) and args.is_valid_int(perm) and args.is_valid_date(interval_init) and args.is_valid_date(interval_end):
        now=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido, idd=idd, type=vertex_type, creation_date=now, perm=perm, interval_init=interval_init, interval_end=interval_end)
        if cassapigraph.insert_bounded_share_out_relation(relation) and cassapigraph.insert_bounded_share_in_relation(relation):
            return True
        else:
            delete_edge(ido=ido, idd=idd, edge_type=edge.BOUNDED_SHARE_RELATION)
            return False
    else:
        return False

def set_uri_edge(ido, idd, vertex_type, uri):
    if args.is_valid_uuid(ido) and args.is_valid_uuid(idd) and args.is_valid_string(vertex_type) and args.is_valid_uri(uri):
        now=timeuuid.uuid1()
        relation=ormgraph.UriRelation(ido=ido, idd=idd, type=vertex_type, creation_date=now, uri=uri)
        if cassapigraph.insert_uri_out_relation(relation) and cassapigraph.insert_uri_in_relation(relation):
            return True
        else:
            delete_edge(ido=ido, idd=idd, edge_type=edge.URI_RELATION)
            return False
    else:
        return False

def set_kin_edge(ido, idd, vertex_type, params):
    if args.is_valid_uuid(ido) and args.is_valid_uuid(idd) and args.is_valid_string(vertex_type) and args.is_valid_dict(params):
        now=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido, idd=idd, type=vertex_type, creation_date=now, params=params)
        if cassapigraph.insert_kin_out_relation(relation) and cassapigraph.insert_kin_in_relation(relation):
            return True
        else:
            delete_edge(ido=ido, idd=idd, edge_type=edge.KIN_RELATION)
            return False
    else:
        return False

def replace_vertex(actual_vertex, new_vertex, new_vertex_type, edge_type_list):
    if not args.is_valid_uuid(actual_vertex) or not args.is_valid_uuid(new_vertex) or not args.is_valid_string(new_vertex_type) or not isinstance(edge_type_list,list):
        return False
    incoming_relations=[]
    outgoing_relations=[]
    for rel in gen_get_incoming_relations_at(idd=actual_vertex, edge_type_list=edge_type_list, path_edge_type_list=edge_type_list, depth_level=1):
        incoming_relations.append(rel)
    for rel in gen_get_outgoing_relations_from(ido=actual_vertex, edge_type_list=edge_type_list, path_edge_type_list=edge_type_list, depth_level=1):
        outgoing_relations.append(rel)
    for rel in gen_get_incoming_relations_at(idd=new_vertex, edge_type_list=edge_type_list, path_edge_type_list=edge_type_list, depth_level=1):
        for actual_rel in incoming_relations:
            if rel.ido==actual_rel.ido and type(rel)==type(actual_rel):
                #conflict detected
                logger.logger.debug('conflict detected: same ido')
                return False
    for rel in gen_get_outgoing_relations_from(ido=new_vertex, edge_type_list=edge_type_list, path_edge_type_list=edge_type_list, depth_level=1):
        for actual_rel in outgoing_relations:
            if (rel.idd==actual_rel.idd and type(rel)==type(actual_rel)):
                #conflict detected
                logger.logger.debug('conflict detected: same idd')
                return False
            elif (isinstance(rel,ormgraph.UriRelation) and isinstance(actual_rel,ormgraph.UriRelation) and rel.uri==actual_rel.uri):
                #conflict detected
                logger.logger.debug('conflict detected: same outgoing uri')
                return False
    for rel in incoming_relations:
        if isinstance(rel, ormgraph.UriRelation):
            vertex_type=vertex.get_relation_type(origin=vertex.get_origin_vertex_type(rel.type),dest=new_vertex_type)
            edge_type=edge.URI_RELATION
            set_uri_edge(ido=rel.ido,idd=new_vertex,vertex_type=vertex_type, uri=rel.uri)
        elif isinstance(rel, ormgraph.BoundedShareRelation):
            vertex_type=vertex.get_relation_type(origin=vertex.get_origin_vertex_type(rel.type),dest=new_vertex_type)
            edge_type=edge.BOUNDED_SHARE_RELATION
            set_bounded_share_edge(ido=rel.ido, idd=new_id, vertex_type=vertex_type, perm=rel.perm, interval_init=rel.interval_init, interval_end=rel.interval_end)
        elif isinstance(rel, ormgraph.MemberRelation):
            vertex_type=vertex.get_relation_type(origin=vertex.get_origin_vertex_type(rel.type),dest=new_vertex_type)
            edge_type=edge.MEMBER_RELATION
            set_member_edge(ido=rel.ido, idd=new_vertex, vertex_type=vertex_type)
        elif isinstance(rel, ormgraph.KinRelation):
            vertex_type=vertex.get_relation_type(origin=vertex.get_origin_vertex_type(rel.type),dest=new_vertex_type)
            edge_type=edge.KIN_RELATION
            set_kin_edge(ido=rel.ido, idd=new_vertex, vertex_type=vertex_type)
        delete_edge(ido=rel.ido, idd=rel.idd, edge_type=edge_type)
    for rel in outgoing_relations:
        if isinstance(rel, ormgraph.UriRelation):
            vertex_type=vertex.get_relation_type(origin=new_vertex_type,dest=vertex.get_dest_vertex_type(rel.type))
            edge_type=edge.URI_RELATION
            set_uri_edge(ido=new_vertex, idd=rel.idd, vertex_type=vertex_type, uri=rel.uri)
        elif isinstance(rel, ormgraph.BoundedShareRelation):
            vertex_type=vertex.get_relation_type(origin=new_vertex_type,dest=vertex.get_dest_vertex_type(rel.type))
            edge_type=edge.BOUNDED_SHARE_RELATION
            set_bounded_share_edge(ido=new_vertex, idd=rel.idd, vertex_type=vertex_type, perm=rel.perm, interval_init=rel.interval_init, interval_end=rel.interval_end)
        elif isinstance(rel, ormgraph.MemberRelation):
            vertex_type=vertex.get_relation_type(origin=new_vertex_type,dest=vertex.get_dest_vertex_type(rel.type))
            edge_type=edge.MEMBER_RELATION
            set_member_edge(ido=new_vertex, idd=rel.idd, vertex_type=vertex_type)
        elif isinstance(rel, ormgraph.KinRelation):
            vertex_type=vertex.get_relation_type(origin=new_vertex_type,dest=vertex.get_dest_vertex_type(rel.type))
            edge_type=edge.KIN_RELATION
            set_kin_edge(ido=new_vertex, idd=rel.idd, vertex_type=vertex_type)
        delete_edge(ido=rel.ido, idd=rel.idd, edge_type=edge_type)
    return True

