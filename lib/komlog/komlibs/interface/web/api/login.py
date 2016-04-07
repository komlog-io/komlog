'''

This file defines the logic associated with web interface operations

'''

from komlog.komfig import logging
from base64 import b64encode, b64decode
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.requests import Requests
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid

def cookie_appender(f):
    def func(*args, **kwargs):
        response=f(*args, **kwargs)
        if isinstance(response, tuple) and len(response)==2:
            return response
        return response,None
    return func

@cookie_appender
@exceptions.ExceptionHandler
def login_request(username, password=None, pubkey=None, challenge=None, signature=None):
    if password is not None:
        return _user_login_request(username=username, password=password)
    if pubkey is not None:
        if challenge is None and signature is None:
            return _agent_login_generate_challenge_request(username=username, pubkey=pubkey)
        else:
            return _agent_login_validate_challenge_request(username=username, pubkey=pubkey, challenge=challenge, signature=signature)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_BAD_PARAMETERS, error=Errors.E_IWAL_LR_IPRM), None

def _user_login_request(username, password):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ULR_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ULR_IPWD)
    if not userapi.auth_user(username=username, password=password):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED, error=Errors.E_IWAL_ULR_AUTHERR), None
    else:
        data={'redirect':'/home'}
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data), {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}

def _agent_login_generate_challenge_request(username, pubkey):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IU)
    if not args.is_valid_string(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IPK)
    try:
        pubkey=b64decode(pubkey.encode('utf-8'))
    except Exception:
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALGCR_IPK)
    challenge=agentapi.generate_auth_challenge(username=username, pubkey=pubkey)
    data={'challenge':b64encode(challenge).decode('utf-8')}
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data), None

def _agent_login_validate_challenge_request(username, pubkey, challenge, signature):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_IU)
    if not args.is_valid_string(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_IWAL_ALVCR_IPK)
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
    aid=agentapi.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge, signature=signature)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK), {'user':username, 'aid':aid.hex, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}


