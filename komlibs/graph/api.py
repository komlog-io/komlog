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
            delete_edge(ido=ido, idd=idd, edge_type=edge.BOUNDED_SHARE)
            return False
    else:
        return False

