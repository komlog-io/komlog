'''

This file defines the logic associated with uri web interface operations

'''

import uuid
from komfig import logger
from komlibs.auth import authorization
from komlibs.gestaccount.user import api as userapi
from komlibs.general.validation import arguments as args
from komlibs.graph.api import uri as graphuri
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel


@exceptions.ExceptionHandler
def get_uri_request(username, uri=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAUR_GUR_IU)
    if uri is not None:
        if uri=='':
            uri=None
        elif not args.is_valid_relative_uri(uri):
            raise exceptions.BadParametersException(error=errors.E_IWAUR_GUR_IUR)
    uid=userapi.get_uid(username=username)
    response_data={'v':[],'e':[]}
    adjacents_pending=set()
    ids_retrieved=set()
    adjacents_retrieved=set()
    vertices=set()
    edges=set()
    max_ids_to_retrieve=10
    if uri is not None:
        new_uri=graphuri.get_joined_uri(base=uri)
        uri_id=graphuri.get_id(ido=uid, uri=new_uri)
        if not uri_id:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND)
        else:
            ids_retrieved.add(uri_id['id'])
            vertices.add((uri_id['id'],uri_id['type'],new_uri))
            adjacents_pending.add((uri_id['id'],new_uri))
    else:
        adjacents_pending.add((uid,''))
    while True:
        if len(ids_retrieved)>max_ids_to_retrieve:
            break
        try:
            next_id=adjacents_pending.pop()
        except Exception:
            break
        else:
            if next_id[0] not in adjacents_retrieved:
                adjacents=graphuri.get_id_adjacents(ido=next_id[0])
                adjacents_retrieved.add(next_id[0])
                if adjacents:
                    for adjacent in adjacents:
                        adjacent_uri=graphuri.get_joined_uri(base=next_id[1],path=adjacent['path'])
                        vertices.add((adjacent['id'],adjacent['type'],adjacent_uri))
                        edges.add((next_id[0],adjacent['id'],adjacent['path'])) if adjacent['path'][0]!='.' else edges.add((adjacent['id'],next_id[0],adjacent['path'][1:]))
                        adjacents_pending.add((adjacent['id'],adjacent_uri))
                        ids_retrieved.add(adjacent['id'])
    for vertex in vertices:
        response_data['v'].append({'id':vertex[0].hex,'type':vertex[1],'uri':vertex[2]})
    for edge in edges:
        response_data['e'].append({'o':edge[0].hex,'d':edge[1].hex,'p':edge[2]})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

