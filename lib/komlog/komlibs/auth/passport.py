'''

A passport is the authorization card obtained from a cookie

'''

import uuid
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.user.states import UserStates
from komlog.komlibs.gestaccount.agent.states import AgentStates
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komfig import logging


class Passport:
    def __init__(self, uid, aid=None):
        self._uid=None
        self._aid=None
        self.uid = uid
        self.aid = aid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if args.is_valid_uuid(value):
            self._uid = value
        else:
            raise exceptions.PassportException(error = Errors.E_AP_PC_IU)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, value):
        if not value:
            self._aid = None
        elif args.is_valid_uuid(value):
            self._aid = value
        else:
            raise exceptions.PassportException(error = Errors.E_AP_PC_IA)

class Cookie:
    def __init__(self, cookie):
        self._user = None
        self._aid = None
        self._seq = None
        if (isinstance(cookie, dict)
            and 'user' in cookie
            and 'aid' in cookie
            and 'seq' in cookie):
            self.user= cookie['user']
            self.aid = cookie['aid']
            self.seq = cookie['seq']
        else:
            raise exceptions.CookieException(error = Errors.E_AP_CC_ID)
    
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if args.is_valid_username(user):
            self._user = user
        else:
            raise exceptions.CookieException(error = Errors.E_AP_CC_IU)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, hex_aid):
        if hex_aid is None:
            self._aid = None
        elif args.is_valid_hex_uuid(hex_aid):
            self._aid = uuid.UUID(hex_aid)
        else:
            raise exceptions.CookieException(error = Errors.E_AP_CC_IA)

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, seq):
        if args.is_valid_sequence(seq):
            self._seq = timeuuid.get_uuid1_from_custom_sequence(seq)
        else:
            raise exceptions.CookieException(error = Errors.E_AP_CC_IS)

def get_user_passport(cookie):
    cookie = Cookie(cookie)
    user = cassapiuser.get_user(username=cookie.user)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AP_GUP_UNF)
    if user.state not in (UserStates.ACTIVE, UserStates.PREACTIVE):
        raise exceptions.AuthorizationExpiredException(error=Errors.E_AP_GUP_IUS)
    return Passport(uid=user.uid)

def get_agent_passport(cookie):
    cookie = Cookie(cookie)
    if not cookie.aid:
        raise exceptions.CookieException(error=Errors.E_AP_GAP_CANF)
    agent = cassapiagent.get_agent(aid=cookie.aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=Errors.E_AP_GAP_ANF)
    if agent.state != AgentStates.ACTIVE:
        raise exceptions.AuthorizationExpiredException(error=Errors.E_AP_GAP_IAS)
    return Passport(uid=agent.uid, aid=agent.aid)

