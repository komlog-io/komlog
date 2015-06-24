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

def get_node_info(ido,uri,counter):
    logger.logger.debug('get_node_info:'+str(ido)+','+str(uri)+','+str(counter))
    id_info=graphuri.get_id(ido=ido)
    if not id_info:
        return {}
    else:
        children_info=[]
        if counter>0:
            children=graphuri.get_id_adjacents(ido=ido, ascendants=False)
            counter=counter-len(children)
            for child in children:
                child_uri=graphuri.get_joined_uri(uri,child['path'])
                children_info.append(get_node_info(ido=child['id'],uri=child_uri,counter=counter))
        return {'id':ido.hex,'name':uri,'type':id_info['type'],'children':children_info}

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
        base_uri=graphuri.get_joined_uri(base=uri)
        uri_id=graphuri.get_id(ido=uid, uri=base_uri)
        if not uri_id:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND)
        else:
            root_id=uri_id['id']
    else:
        root_id=uid
        base_uri=''
    node_info=get_node_info(ido=root_id,uri=base_uri,counter=5)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=node_info)

