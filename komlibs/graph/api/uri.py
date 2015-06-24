'''

uri.py

In this file we implement specific methods for working with
the uri graph layer

'''

import uuid
from komcass.api import graph as cassapigraph
from komcass.model.orm import graph as ormgraph
from komlibs.graph.api import base as graphbase
from komlibs.graph.relations import edge, vertex
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid

def get_id(ido, uri=None):
    if not args.is_valid_uuid(ido):
        return None
    if uri is not None and not args.is_valid_relative_uri(uri):
        return None
    if uri is not None:
        uri_segments=uri.split('.')
        current_level=0
        current_id=ido
        rel_found=None
        next_level=True
        while next_level==True:
            next_level=False
            if uri_segments[current_level]=='':
                current_level+=1
                for rel in graphbase.gen_get_incoming_relations_at(idd=current_id,edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.URI_RELATION],depth_level=1):
                    if rel.uri==uri_segments[current_level]:
                        if (current_level==len(uri_segments)-1):
                            rel_found=rel
                            break;
                        else:
                            current_id=rel.ido
                            current_level+=1
                            next_level=True
                            break;
            else:
                for rel in graphbase.gen_get_outgoing_relations_from(ido=current_id,edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.URI_RELATION],depth_level=1):
                    if rel.uri==uri_segments[current_level]:
                        if (current_level==len(uri_segments)-1):
                            rel_found=rel
                            break;
                        else:
                            current_id=rel.idd
                            current_level+=1
                            next_level=True
                            break;
        if rel_found is None:
            return None
        else:
            selected_id={'id':rel_found.idd,'type':vertex.get_dest_vertex_type(rel_found.type)}
    else:
        selected_id={'id':ido,'type':None}
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido, edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.URI_RELATION], depth_level=1):
            selected_id['type']=vertex.get_origin_vertex_type(rel.type)
            break
        if selected_id['type']==None:
            for rel in graphbase.gen_get_incoming_relations_at(idd=ido, edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.URI_RELATION], depth_level=1):
                selected_id['type']=vertex.get_dest_vertex_type(rel.type)
                break
        if selected_id['type']==None:
            return None
    return selected_id

def get_id_adjacents(ido, ascendants=True):
    adjacents=[]
    if not args.is_valid_uuid(ido):
        return None
    for rel in graphbase.gen_get_outgoing_relations_from(ido=ido, edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.URI_RELATION], depth_level=1):
        adjacents.append({'id':rel.idd,'type':vertex.get_dest_vertex_type(rel.type),'path':rel.uri})
    if ascendants:
        for rel in graphbase.gen_get_incoming_relations_at(idd=ido, edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.URI_RELATION], depth_level=1):
            adjacents.append({'id':rel.ido,'type':vertex.get_origin_vertex_type(rel.type),'path':'.'+rel.uri})
    return adjacents

def get_joined_uri(base,path=None):
    if not args.is_valid_relative_uri(base):
        if not args.is_valid_string(base) or base!='':
            return None
    for i,group in enumerate(base.split('..')):
        if i==0:
            uri_segments=group.split('.') if len(group)>0 else []
        else:
            for j,subgroup in enumerate(group.split('.')):
                if j==0:
                    if uri_segments[-1]!=subgroup:
                        uri_segments.append('.'+subgroup)
                    else:
                        uri_segments.pop(-1)
                elif j==1:
                    if uri_segments[-1][0]=='.' and uri_segments[-1]=='.'+subgroup:
                        uri_segments.pop(-1)
                    else:
                        uri_segments.append(subgroup)
                else:
                    uri_segments.append(subgroup)
    if path is not None and len(path)>0:
        if len(uri_segments)==0:
            uri_segments.append(path)
        elif path[0]=='.' and uri_segments[-1]==path[1:]:
            uri_segments.pop(-1)
        else:
            uri_segments.append(path)
    return '.'.join(uri_segments)

def new_uri(ido,idd,uri,type):
    if not args.is_valid_uuid(ido) or not args.is_valid_uuid(idd) or not args.is_valid_uri(uri) or not args.is_valid_string(type):
        return False
    existent_uri=get_id(ido,uri)
    if existent_uri:
        return False
    uri_segments=uri.split('.')
    edge_list=[]
    if len(uri_segments)==1:
        edge_list.append((ido,idd,type,uri))
    elif len(uri_segments)>1:
        current_ido=ido
        current_origin_type=vertex.get_origin_vertex_type(type)
        for i,uri_segment in enumerate(uri_segments):
            existent_uri=get_id(ido=current_ido,uri=uri_segment)
            if not existent_uri:
                if i<len(uri_segments)-1:
                    new_idd=uuid.uuid4()
                    new_type=vertex.get_relation_type(origin=current_origin_type, dest=vertex.VOID)
                else:
                    new_idd=idd
                    new_type=vertex.get_relation_type(origin=current_origin_type, dest=vertex.get_dest_vertex_type(rel=type))
                edge_list.append((current_ido,new_idd,new_type,uri_segment))
                current_ido=new_idd
                current_origin_type=vertex.get_dest_vertex_type(rel=new_type)
            else:
                current_ido=existent_uri['id']
                current_origin_type=existent_uri['type']
    if len(edge_list)==0:
        return False
    else:
        for edge_to_add in edge_list:
            _ido,_idd,_type,_uri=edge_to_add
            graphbase.set_uri_edge(ido=_ido,idd=_idd,vertex_type=_type,uri=_uri)
    return True

def new_widget_uri(uid, wid, uri):
    if not args.is_valid_uuid(uid) or not args.is_valid_uuid(wid) or not args.is_valid_uri(uri):
        return False
    existent_uri=get_id(ido=uid, uri=uri)
    if not existent_uri:
        type=vertex.USER_WIDGET_RELATION
        return new_uri(ido=uid, idd=wid, uri=uri, type=type)
    else:
        if existent_uri['type']==vertex.VOID:
            return graphbase.replace_vertex(actual_vertex=existent_uri['id'], new_vertex=wid, new_vertex_type=vertex.WIDGET, edge_type_list=[edge.URI_RELATION])
        else:
            return False

def new_datasource_uri(uid, did, uri):
    if not args.is_valid_uuid(uid) or not args.is_valid_uuid(did) or not args.is_valid_uri(uri):
        return False
    existent_uri=get_id(ido=uid, uri=uri)
    if not existent_uri:
        type=vertex.USER_DATASOURCE_RELATION
        return new_uri(ido=uid, idd=did, uri=uri, type=type)
    else:
        if existent_uri['type']==vertex.VOID:
            return graphbase.replace_vertex(actual_vertex=existent_uri['id'], new_vertex=did, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION])
        else:
            return False

def new_datapoint_uri(pid, uri, did=None, uid=None):
    if not args.is_valid_uuid(pid) or not args.is_valid_uri(uri):
        return False
    if not pid and not did:
        return False
    if did and not args.is_valid_uuid(did):
        return False
    if uid and not args.is_valid_uuid(uid):
        return False
    if did:
        type=vertex.DATASOURCE_DATAPOINT_RELATION
        ido=did
    else:
        type=vertex.USER_DATAPOINT_RELATION
        ido=uid
    existent_uri=get_id(ido=ido, uri=uri)
    if not existent_uri:
        return new_uri(ido=ido, idd=pid, uri=uri, type=type)
    else:
        if existent_uri['type']==vertex.VOID:
            return graphbase.replace_vertex(actual_vertex=existent_uri['id'], new_vertex=pid, new_vertex_type=vertex.DATAPOINT, edge_type_list=[edge.URI_RELATION])
        else:
            return False

def dissociate_uri(ido, uri):
    ''' To dissociate a uri means to dissociate the actual element from the uri vertex and replace it with a void element.'''
    if not args.is_valid_uuid(ido) or not args.is_valid_uri(uri):
        return False
    existent_uri=get_id(ido=ido, uri=uri)
    if not existent_uri:
        return False
    else:
        if existent_uri['type']==vertex.VOID:
            return True
        else:
            vid=uuid.uuid4()
            return graphbase.replace_vertex(actual_vertex=existent_uri['id'], new_vertex=vid, new_vertex_type=vertex.VOID, edge_type_list=[edge.URI_RELATION])

def dissociate_vertex(ido):
    ''' Dissociate a vertex is replacing the actual vertex with a void id, migrating the previous vertex connection to the new one '''
    if not args.is_valid_uuid(ido):
        return False
    vid=uuid.uuid4()
    return graphbase.replace_vertex(actual_vertex=ido, new_vertex=vid, new_vertex_type=vertex.VOID, edge_type_list=[edge.URI_RELATION])

