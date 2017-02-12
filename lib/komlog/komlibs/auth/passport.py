'''

A passport is the authorization card obtained from a cookie

'''

import uuid
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model.cookies import Cookies
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.user.states import UserStates
from komlog.komlibs.gestaccount.agent.states import AgentStates
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komfig import logging


class Passport:
    def __init__(self, uid, sid):
        self.uid = uid
        self.sid = sid

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
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, value):
        if args.is_valid_uuid(value):
            self._sid = value
        else:
            raise exceptions.PassportException(error = Errors.E_AP_PC_IS)

class UserPassport(Passport):

    def __init__(self, uid, sid):
        super().__init__(uid=uid, sid=sid)


class AgentPassport(Passport):

    def __init__(self, uid, sid, aid, pv):
        self.aid = aid
        self.pv = pv
        super().__init__(uid=uid, sid=sid)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, value):
        if args.is_valid_uuid(value):
            self._aid = value
        else:
            raise exceptions.PassportException(error = Errors.E_AP_APC_IA)

    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, value):
        if args.is_valid_int(value):
            self._pv = value
        else:
            raise exceptions.PassportException(error = Errors.E_AP_APC_IPV)

class Cookie:

    def __init__(self, sid, seq):
        self.sid = sid
        self.seq = seq

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        if args.is_valid_uuid(sid):
            self._sid = sid
        else:
            raise exceptions.CookieException(error = Errors.E_AP_CC_IS)

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, seq):
        if args.is_valid_sequence(seq):
            self._seq = seq
        else:
            raise exceptions.CookieException(error = Errors.E_AP_CC_ISQ)

class UserCookie(Cookie):
    __type__ = Cookies.USER

    def __init__(self, user, sid, seq):
        self.user = user
        super().__init__(sid=sid, seq=seq)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if args.is_valid_username(user):
            self._user = user
        else:
            raise exceptions.CookieException(error = Errors.E_AP_UCC_IU)

    @classmethod
    def load_from_dict(cls, cookie):
        if (isinstance(cookie, dict)
            and 't' in cookie
            and cookie['t'] == cls.__type__.value
            and 'sid' in cookie
            and args.is_valid_hex_uuid(cookie['sid'])
            and 'user' in cookie
            and 'seq' in cookie):
            sid = uuid.UUID(cookie['sid'])
            return cls(user=cookie['user'], sid=sid, seq=cookie['seq'])
        else:
            raise exceptions.CookieException(error = Errors.E_AP_UCC_ID)

    def to_dict(self):
        return {
            'user':self.user,
            'sid':self.sid.hex,
            'seq':self.seq,
            't':self.__type__.value
        }

class AgentCookie(Cookie):
    __type__ = Cookies.AGENT

    def __init__(self, aid, pv, sid, seq):
        self.aid = aid
        self.pv = pv
        super().__init__(sid=sid, seq=seq)

    @property
    def aid(self):
        return self._aid

    @aid.setter
    def aid(self, aid):
        if args.is_valid_uuid(aid):
            self._aid = aid
        else:
            raise exceptions.CookieException(error = Errors.E_AP_ACC_IA)

    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, value):
        if args.is_valid_int(value):
            self._pv = value
        else:
            raise exceptions.CookieException(error = Errors.E_AP_ACC_IPV)

    @classmethod
    def load_from_dict(cls, cookie):
        if (isinstance(cookie, dict)
            and 't' in cookie
            and cookie['t'] == cls.__type__.value
            and 'sid' in cookie
            and args.is_valid_hex_uuid(cookie['sid'])
            and 'aid' in cookie
            and args.is_valid_hex_uuid(cookie['aid'])
            and 'pv' in cookie
            and 'seq' in cookie):
            aid = uuid.UUID(cookie['aid'])
            sid = uuid.UUID(cookie['sid'])
            return cls(aid=aid, pv=cookie['pv'], sid=sid, seq=cookie['seq'])
        else:
            raise exceptions.CookieException(error = Errors.E_AP_ACC_ID)

    def to_dict(self):
        return {
            'aid':self.aid.hex,
            'pv':self.pv,
            'sid':self.sid.hex,
            'seq':self.seq,
            't':self.__type__.value
        }

def get_user_passport(cookie):
    cookie = UserCookie.load_from_dict(cookie)
    user = cassapiuser.get_user(username=cookie.user)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_AP_GUP_UNF)
    if user.state != UserStates.ACTIVE:
        raise exceptions.AuthorizationExpiredException(error=Errors.E_AP_GUP_IUS)
    return UserPassport(uid=user.uid, sid=cookie.sid)

def get_agent_passport(cookie):
    cookie = AgentCookie.load_from_dict(cookie)
    agent = cassapiagent.get_agent(aid=cookie.aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=Errors.E_AP_GAP_ANF)
    if agent.state != AgentStates.ACTIVE:
        raise exceptions.AuthorizationExpiredException(error=Errors.E_AP_GAP_IAS)
    return AgentPassport(uid=agent.uid, sid=cookie.sid, aid=agent.aid, pv=cookie.pv)

def check_agent_passport_validity(passport):
    if not isinstance(passport, AgentPassport):
        raise exceptions.PassportException(error=Errors.E_AP_CPV_IP)
    agent = cassapiagent.get_agent(aid=passport.aid)
    if agent is None:
        raise exceptions.AgentNotFoundException(error=Errors.E_AP_CPV_ANF)
    elif agent.state != AgentStates.ACTIVE:
        raise exceptions.AuthorizationExpiredException(error=Errors.E_AP_CPV_IAS)

