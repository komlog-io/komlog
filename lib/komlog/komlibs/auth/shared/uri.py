
import uuid
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.auth import exceptions, permissions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.general.validation import arguments as args


def share_uri_tree(uid, dest_uid, uri):
    ''' This function gives READ and SNAPSHOT permissions
        for a uri and its descendants to a user identified by dest_uid '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_SUT_IUID)
    if not args.is_valid_uuid(dest_uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_SUT_IDUID)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_ASU_SUT_IURI)
    perm = permissions.CAN_READ | permissions.CAN_SNAPSHOT
    try:
        cassapiperm.insert_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri, perm=perm)
        cassapiperm.insert_user_shared_uri_with_me_perm(uid=dest_uid,owner_uid=uid,uri=uri,perm=perm)
    except:
        cassapiperm.delete_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
        cassapiperm.delete_user_shared_uri_with_me_perm(uid=dest_uid,owner_uid=uid,uri=uri)
        raise
    else:
        return True

def unshare_uri_tree(uid, uri, dest_uid=None):
    ''' This function revokes READ and SNAPSHOT permissions
        for a uri and its descendants.
        if dest_uid is passed, permissions are revoked only to her '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_USUT_IUID)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_ASU_USUT_IURI)
    if dest_uid != None and not args.is_valid_uuid(dest_uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_USUT_IDUID)

    if dest_uid:
        cassapiperm.delete_user_shared_uri_with_me_perm(uid=dest_uid, owner_uid=uid, uri=uri)
        cassapiperm.delete_user_shared_uri_perm(uid=uid, dest_uid=dest_uid, uri=uri)
    else:
        shared = cassapiperm.get_user_shared_uris(uid=uid, dest_uid=dest_uid)
        for item in shared:
            if item.uri == uri:
                cassapiperm.delete_user_shared_uri_with_me_perm(uid=item.dest_uid,owner_uid=uid,uri=uri)
                cassapiperm.delete_user_shared_uri_perm(uid=uid, dest_uid=item.dest_uid, uri=uri)
    return True

def get_uris_shared_with_me(uid, owner_uid=None):
    ''' Returns a list containing the uris shared with the user '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_GUSWM_IUID)
    if owner_uid != None and not args.is_valid_uuid(owner_uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_GUSWM_IOUID)
    shared = cassapiperm.get_user_shared_uris_with_me(uid=uid, owner_uid=owner_uid)
    data = [{'owner':item.owner_uid,'uri':item.uri,'perm':item.perm} for item in shared]
    return data

def get_uris_shared(uid, dest_uid=None):
    ''' Returns a list containing the uris shared with other users '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_GUS_IUID)
    if dest_uid != None and not args.is_valid_uuid(dest_uid):
        raise exceptions.BadParametersException(error=Errors.E_ASU_GUS_IDUID)
    shared = cassapiperm.get_user_shared_uris(uid=uid, dest_uid=dest_uid)
    data = [{'dest':item.dest_uid,'uri':item.uri,'perm':item.perm} for item in shared]
    return data

