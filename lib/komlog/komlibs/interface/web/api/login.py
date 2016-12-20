'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komfig import logging
from base64 import b64encode, b64decode
from komlog.komlibs.auth import authorization, passport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.interface.web.model import response
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid

@exceptions.ExceptionHandler
def login_request(username, password=None, pubkey=None, pv=None, challenge=None, signature=None):
    if password is not None:
        return _user_login_request(username=username, password=password)
    if pubkey is not None:
        if challenge is None and signature is None:
            return _agent_login_generate_challenge_request(username=username, pubkey=pubkey, pv=pv)
        else:
            return _agent_login_validate_challenge_request(username=username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_BAD_PARAMETERS, error=Errors.E_IWAL_LR_IPRM)

def _user_login_request(username, password):
    if not args.is_valid_username_with_caps(username):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ULR_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ULR_IPWD)
    if not userapi.auth_user(username=username.lower(), password=password):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED, error=Errors.E_IWAL_ULR_AUTHERR)
    data={'redirect':'/home'}
    resp=response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)
    resp.cookie=passport.UserCookie(user=username.lower(), seq=timeuuid.get_custom_sequence(timeuuid.uuid1()), sid=uuid.uuid4()).to_dict()
    return resp

def _agent_login_generate_challenge_request(username, pubkey, pv):
    if not args.is_valid_username_with_caps(username):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IU)
    if not args.is_valid_string(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IPK)
    if not args.is_valid_string_int(pv) or int(pv) == 0:
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IPV)
    try:
        pubkey=b64decode(pubkey.encode('utf-8'))
    except Exception:
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IPK)
    challenge=agentapi.generate_auth_challenge(username=username.lower(), pubkey=pubkey)
    data={'challenge':b64encode(challenge).decode('utf-8')}
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)

def _agent_login_validate_challenge_request(username, pubkey, pv, challenge, signature):
    if not args.is_valid_username_with_caps(username):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_IU)
    if not args.is_valid_string(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_IPK)
    if not args.is_valid_string_int(pv) or int(pv) == 0:
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_IPV)
    if not args.is_valid_string(challenge):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_ICH)
    if not args.is_valid_string(signature):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_ISG)
    try:
        pubkey=b64decode(pubkey.encode('utf-8'))
        challenge=b64decode(challenge.encode('utf-8'))
        signature=b64decode(signature.encode('utf-8'))
    except Exception:
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_IPK)
    aid=agentapi.validate_auth_challenge(username=username.lower(), pubkey=pubkey, challenge_hash=challenge, signature=signature)
    resp=response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    resp.cookie=passport.AgentCookie(aid=aid, pv=int(pv), seq=timeuuid.get_custom_sequence(timeuuid.uuid1()), sid=uuid.uuid4()).to_dict()
    return resp


