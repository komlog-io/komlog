'''

This file defines the logic associated with uri web interface operations

'''

import uuid
from komlog.komlibs.auth import authorization, permissions
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.shared import uri as shareduri
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.gestaccount import exceptions as gestexcept
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
        elif not (args.is_valid_uri(uri) or args.is_valid_global_uri(uri)):
            raise exceptions.BadParametersException(error=Errors.E_IWAUR_GUR_IUR)
    authorization.authorize_request(request=Requests.GET_URI,passport=passport, uri=uri)
    response_data={'v':[],'e':[]}
    adjacents_pending=set()
    ids_retrieved=set()
    adjacents_retrieved=set()
    vertices=set()
    edges=set()
    max_ids_to_retrieve=10
    if uri is not None:
        if args.is_valid_global_uri(uri):
            username,local_uri =uri.split(':')
            uid = userapi.get_uid(username.lower())
        else:
            uid = passport.uid
            local_uri=uri
        base_uri=graphuri.get_joined_uri(base=local_uri)
        uri_id=graphuri.get_id(ido=uid, uri=base_uri)
        if not uri_id:
            return response.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=Errors.E_IWAUR_GUR_URINF)
        else:
            root_id=uri_id['id']
    else:
        root_id=passport.uid
        base_uri=''
    node_info=get_node_info(ido=root_id,uri=base_uri,counter=5)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=node_info)

@exceptions.ExceptionHandler
def share_uri_request(passport, uri, users):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_SUR_IPSP)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_SUR_IURI)
    if not isinstance(users,list):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_SUR_IUSERS)
    for item in users:
        if not args.is_valid_username_with_caps(item):
            raise exceptions.BadParametersException(error=Errors.E_IWAUR_SUR_IUSER)
    if len(users) == 0:
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_SUR_NUSER)
    uri_info = graphuri.get_id(ido=passport.uid, uri=uri)
    if uri_info is None:
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_SUR_URINF)
    uids=[]
    for username in users:
        uid=userapi.get_uid(username.lower())
        uids.append(uid)
    shared=[]
    try:
        for dest_uid in uids:
            shareduri.share_uri_tree(uid=passport.uid, dest_uid=dest_uid, uri=uri)
            shared.append(dest_uid)
    except:
        for dest_uid in shared:
            shareduri.unshare_uri_tree(uid=passport.uid, uri=uri, dest_uid=dest_uid)
        raise
    else:
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def unshare_uri_request(passport, uri, users=None):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_USUR_IPSP)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_USUR_IURI)
    if users is not None:
        if not isinstance(users,list):
            raise exceptions.BadParametersException(error=Errors.E_IWAUR_USUR_IUSERS)
        for item in users:
            if not args.is_valid_username_with_caps(item):
                raise exceptions.BadParametersException(error=Errors.E_IWAUR_USUR_IUSER)
    uri_info = graphuri.get_id(ido=passport.uid, uri=uri)
    if uri_info is None:
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_USUR_URINF)
    if users is None or len(users) == 0:
        shareduri.unshare_uri_tree(uid=passport.uid, uri=uri)
    else:
        for username in users:
            try:
                uid = userapi.get_uid(username.lower())
                shareduri.unshare_uri_tree(uid=passport.uid, uri=uri, dest_uid=uid)
            except gestexcept.UserNotFoundException:
                pass
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def get_uris_shared_request(passport):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_GUSR_IPSP)
    shared=shareduri.get_uris_shared(uid=passport.uid)
    data={}
    usernames={}
    for item in shared:
        try:
            if not item['dest'] in usernames:
                user = userapi.get_user_config(uid=item['dest'])
                usernames[user['uid']]=user['username']
            data[item['uri']].append(usernames[item['dest']])
        except gestexcept.UserNotFoundException:
            shareduri.unshare_uri_tree(uid=passport.uid,uri=item['uri'],dest_uid=item['dest'])
        except KeyError:
            data[item['uri']]=[usernames[item['dest']],]
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)

@exceptions.ExceptionHandler
def get_uris_shared_with_me_request(passport):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWAUR_GUSWMR_IPSP)
    shared=shareduri.get_uris_shared_with_me(uid=passport.uid)
    data={}
    usernames={}
    for item in shared:
        try:
            if not item['owner'] in usernames:
                user = userapi.get_user_config(uid=item['owner'])
                usernames[user['uid']]=user['username']
            data[usernames[item['owner']]].append(item['uri'])
        except gestexcept.UserNotFoundException:
            shareduri.unshare_uri_tree(uid=item['owner'],uri=item['uri'],dest_uid=passport.uid)
        except KeyError:
            data[usernames[item['owner']]]=[item['uri']]
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)

