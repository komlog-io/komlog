'''

This file defines the logic associated with uri web interface operations

'''

import uuid
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response

def get_node_info(ido,uri,counter):
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
def get_uri_request(passport, uri=None):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_GUR_IPSP)
    if uri is not None:
        if uri=='':
            uri=None
        elif not args.is_valid_relative_uri(uri):
            raise exceptions.BadParametersException(error=Errors.E_IWAUR_GUR_IUR)
    authorization.authorize_request(request=Requests.GET_URI,passport=passport)
    response_data={'v':[],'e':[]}
    adjacents_pending=set()
    ids_retrieved=set()
    adjacents_retrieved=set()
    vertices=set()
    edges=set()
    max_ids_to_retrieve=10
    if uri is not None:
        base_uri=graphuri.get_joined_uri(base=uri)
        uri_id=graphuri.get_id(ido=passport.uid, uri=base_uri)
        if not uri_id:
            return response.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND)
        else:
            root_id=uri_id['id']
    else:
        root_id=passport.uid
        base_uri=''
    node_info=get_node_info(ido=root_id,uri=base_uri,counter=5)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=node_info)

