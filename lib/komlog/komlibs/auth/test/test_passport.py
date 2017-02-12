import unittest
import uuid
import inspect
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.orm import agent as ormagent
from komlog.komlibs.auth import passport
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model.cookies import Cookies
from komlog.komlibs.gestaccount.user.states import UserStates
from komlog.komlibs.gestaccount.agent.states import AgentStates
from komlog.komlibs.general.time import timeuuid
from komlog.komfig import logging

class AuthPassportTest(unittest.TestCase):
    ''' komlog.auth.passport tests '''

    def test_user_passport_creation_success(self):
        ''' a new agent passport instance should be create successfully '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        psp = passport.UserPassport(uid=uid, sid=sid)
        self.assertTrue(isinstance(psp, passport.UserPassport))

    def test_agent_passport_creation_success(self):
        ''' a new agent passport instance should be create successfully '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertTrue(isinstance(psp, passport.AgentPassport))

    def test_user_passport_creation_failure_invalid_uid(self):
        ''' a new passport instance should fail if uid is invalid '''
        uids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), None, ('a','tuple'), ['an','array'],{'set'}]
        sid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.UserPassport(uid=uid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IU)

    def test_agent_passport_creation_failure_invalid_uid(self):
        ''' a new passport instance should fail if uid is invalid '''
        uids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), None, ('a','tuple'), ['an','array'],{'set'}]
        sid=uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        for uid in uids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IU)

    def test_agent_passport_creation_failure_invalid_aid(self):
        ''' a new passport instance should fail if aid is invalid '''
        aids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        pv = 1
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_APC_IA)

    def test_agent_passport_creation_failure_invalid_pv(self):
        ''' a new passport instance should fail if pv is invalid '''
        pvs= ['234234',-1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        for pv in pvs:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_APC_IPV)

    def test_user_passport_creation_failure_invalid_sid(self):
        ''' a new passport instance should fail if sid is invalid '''
        sids = [None,'234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        uid = uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.UserPassport(uid=uid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IS)

    def test_agent_passport_creation_failure_invalid_sid(self):
        ''' a new passport instance should fail if sid is invalid '''
        sids = [None,'234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        for sid in sids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IS)

    def test_user_cookie_creation_failure_invalid_user(self):
        ''' a new cookie instance should fail if user is invalid '''
        usernames= [1,1.2,{'a':'dict'},uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'},None,'Withcapitals']
        sid = uuid.uuid4()
        seq = timeuuid.get_custom_sequence(uuid.uuid1())
        for user in usernames:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.UserCookie(user=user, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_UCC_IU)

    def test_user_cookie_creation_failure_invalid_sid(self):
        ''' a new cookie instance should fail if sid is invalid '''
        sids= [1,1.2,{'a':'dict'},uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'},None, uuid.uuid4().hex]
        user='username'
        seq = timeuuid.get_custom_sequence(uuid.uuid1())
        for sid in sids:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.UserCookie(user=user, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_IS)

    def test_user_cookie_creation_failure_invalid_seq(self):
        ''' a new cookie instance should fail if seq is invalid '''
        seqs= [1,1.2,{'a':'dict'},uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'},None, uuid.uuid4().hex, uuid.uuid4()]
        user='username'
        sid=uuid.uuid4()
        for seq in seqs:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.UserCookie(user=user, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_ISQ)

    def test_user_cookie_load_from_dict_success(self):
        ''' a new cookie instance should be create successfully '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'user':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        c = passport.UserCookie.load_from_dict(cookie)
        self.assertTrue(isinstance(c,passport.UserCookie))
        self.assertEqual(c.sid, uuid.UUID(cookie['sid']))
        self.assertEqual(c.user, cookie['user'])
        self.assertEqual(c.seq, cookie['seq'])

    def test_user_cookie_load_from_dict_failure_no_type(self):
        ''' a new cookie instance should fail if type is not found '''
        cookie = {
            'at':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'user':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_not_a_dict(self):
        ''' a new cookie instance should fail if it is not a dict '''
        cookie = [
            't',Cookies.AGENT.value,
            'sid',uuid.uuid4().hex,
            'user','username',
            'seq',timeuuid.get_custom_sequence(uuid.uuid1()),
        ]
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_invalid_type(self):
        ''' a new cookie instance should fail if type is invalid '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'user':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_no_sid(self):
        ''' a new cookie instance should fail if sid is not found '''
        cookie = {
            't':Cookies.USER.value,
            'asid':uuid.uuid4().hex,
            'user':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_invalid_sid(self):
        ''' a new cookie instance should fail if sid is invalid '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4(),
            'user':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_user_not_found(self):
        ''' a new cookie instance should fail if user is not found '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'auser':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_user_invalid(self):
        ''' a new cookie instance should fail if user is invalid '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'user':'Username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_IU)

    def test_user_cookie_load_from_dict_failure_seq_not_found(self):
        ''' a new cookie instance should fail if seq is not found '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'user':'username',
            'aseq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_UCC_ID)

    def test_user_cookie_load_from_dict_failure_seq_invalid(self):
        ''' a new cookie instance should fail if seq is invalid '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'user':'username',
            'seq':'seq',
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.UserCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_CC_ISQ)

    def test_user_cookie_to_dict_success(self):
        ''' a new cookie instance should be created successfully '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'user':'username',
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        c = passport.UserCookie.load_from_dict(cookie)
        self.assertTrue(isinstance(c,passport.UserCookie))
        self.assertEqual(c.sid, uuid.UUID(cookie['sid']))
        self.assertEqual(c.user, cookie['user'])
        self.assertEqual(c.seq, cookie['seq'])
        to_d = c.to_dict()
        self.assertEqual(to_d, cookie)

    def test_agent_cookie_creation_failure_invalid_aid(self):
        ''' a new agent cookie instance should fail if aid is invalid '''
        aids= ['string',1,1.2,{'a':'dict'},uuid.uuid1(), uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        sid = uuid.uuid4()
        seq = timeuuid.get_custom_sequence(uuid.uuid1())
        pv = 1
        for aid in aids:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.AgentCookie(aid=aid, pv=pv, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_ACC_IA)

    def test_agent_cookie_creation_failure_invalid_pv(self):
        ''' a new agent cookie instance should fail if pv is invalid '''
        pvs= ['string',-1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        seq = timeuuid.get_custom_sequence(uuid.uuid1())
        for pv in pvs:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.AgentCookie(aid=aid, pv=pv, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_ACC_IPV)

    def test_agent_cookie_creation_failure_invalid_sid(self):
        ''' a new agent cookie instance should fail if sid is invalid '''
        sids= ['string',1,1.2,{'a':'dict'},uuid.uuid4().hex,uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        aid = uuid.uuid4()
        seq = timeuuid.get_custom_sequence(uuid.uuid1())
        pv = 1
        for sid in sids:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.AgentCookie(aid=aid, pv=pv, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_IS)

    def test_agent_cookie_creation_failure_invalid_seq(self):
        ''' a new agent cookie instance should fail if seq is invalid '''
        seqs = ['string',1,1.2,{'a':'dict'},uuid.uuid4(), uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        for seq in seqs:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.AgentCookie(aid=aid, pv=pv, sid=sid, seq=seq)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_ISQ)

    def test_agent_cookie_load_from_dict_success(self):
        ''' a new agent cookie instance should be created successfully '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        c = passport.AgentCookie.load_from_dict(cookie)
        self.assertTrue(isinstance(c,passport.AgentCookie))
        self.assertEqual(c.sid, uuid.UUID(cookie['sid']))
        self.assertEqual(c.aid, uuid.UUID(cookie['aid']))
        self.assertEqual(c.seq, cookie['seq'])
        self.assertEqual(c.pv, cookie['pv'])

    def test_agent_cookie_load_from_dict_failure_not_a_dict(self):
        ''' AgentCookie class instantiation should fail if is not a dict '''
        cookie = [
            't',Cookies.AGENT.value,
            'sid',uuid.uuid4().hex,
            'aid',uuid.uuid4().hex,
            'pv',1,
            'seq',timeuuid.get_custom_sequence(uuid.uuid1()),
        ]
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_type_not_found(self):
        ''' AgentCookie class instantiation should fail if t is not found '''
        cookie = {
            'at':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_type_invalid(self):
        ''' AgentCookie class instantiation should fail if t is invalid '''
        cookie = {
            't':Cookies.USER.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_sid_not_found(self):
        ''' AgentCookie class instantiation should fail if sid is not_ found '''
        cookie = {
            't':Cookies.AGENT.value,
            'asid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_sid_invalid(self):
        ''' AgentCookie class instantiation should fail if sid is invalid '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4(),
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_aid_not_found(self):
        ''' AgentCookie class instantiation should fail if aid is not found '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aaid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_aid_invalid(self):
        ''' AgentCookie class instantiation should fail if aid is invalid '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4(),
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_pv_not_found(self):
        ''' AgentCookie class instantiation should fail if pv is not found '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'apv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_pv_invalid(self):
        ''' AgentCookie class instantiation should fail if pv is invalid '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':-1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_IPV)

    def test_agent_cookie_load_from_dict_failure_seq_not_found(self):
        ''' AgentCookie class instantiation should fail if seq is not found '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'aseq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_ACC_ID)

    def test_agent_cookie_load_from_dict_failure_seq_invalid(self):
        ''' AgentCookie class instantiation should fail if seq is invalid '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':'seq',
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            c = passport.AgentCookie.load_from_dict(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_CC_ISQ)

    def test_agent_cookie_to_dict_success(self):
        ''' a new agent cookie instance should be created successfully '''
        cookie = {
            't':Cookies.AGENT.value,
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(uuid.uuid1()),
        }
        c = passport.AgentCookie.load_from_dict(cookie)
        self.assertTrue(isinstance(c,passport.AgentCookie))
        self.assertEqual(c.sid, uuid.UUID(cookie['sid']))
        self.assertEqual(c.aid, uuid.UUID(cookie['aid']))
        self.assertEqual(c.seq, cookie['seq'])
        self.assertEqual(c.pv, cookie['pv'])
        to_d = c.to_dict()
        self.assertEqual(to_d, cookie)

    def test_get_user_passport_failure_non_existing_user(self):
        ''' get_user_passport should fail if user does not exist '''
        cookie = {
            'user':'test_get_user_passport_failure_non_existing_user',
            'sid':uuid.uuid4().hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.USER.value
        }
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            psp=passport.get_user_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GUP_UNF)

    def test_get_user_passport_failure_invalid_user_state(self):
        ''' get_user_passport should fail if user state does not exist nor allow connection '''
        username='test_get_user_passport_failure_invalid_user_state'
        password=b'password'
        email=username+'@komlog.org'
        cookie = {
            'user':username,
            'sid':uuid.uuid4().hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.USER.value
        }
        user = ormuser.User(uid=uuid.uuid4(), username=username, password=password, email=email)
        self.assertTrue(cassapiuser.new_user(user))
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            psp=passport.get_user_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GUP_IUS)

    def test_get_user_passport_failure_user_not_confirmed_yet(self):
        ''' get_user_passport should fail if user has not confirmed his account yet '''
        username='test_get_user_passport_failure_user_not_confirmed_yet'
        password=b'password'
        email=username+'@komlog.org'
        state=UserStates.PREACTIVE
        cookie = {
            'user':username,
            'sid':uuid.uuid4().hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.USER.value
        }
        user = ormuser.User(uid=uuid.uuid4(), username=username, password=password, email=email, state=state)
        self.assertTrue(cassapiuser.new_user(user))
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            psp=passport.get_user_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GUP_IUS)

    def test_get_user_passport_success(self):
        ''' get_user_passport should succeed '''
        username='test_get_user_passport_success'
        password=b'password'
        email=username+'@komlog.org'
        state=UserStates.ACTIVE
        cookie = {
            'user':username,
            'sid':uuid.uuid4().hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.USER.value
        }
        user = ormuser.User(uid=uuid.uuid4(), username=username, password=password, email=email, state=state)
        self.assertTrue(cassapiuser.new_user(user))
        psp=passport.get_user_passport(cookie)
        self.assertTrue(isinstance(psp, passport.UserPassport))
        self.assertEqual(psp.uid, user.uid)
        self.assertEqual(psp.sid, uuid.UUID(cookie['sid']))

    def test_get_agent_passport_failure_agent_does_not_exist(self):
        ''' get_agent_passport should fail if agent does not exist '''
        cookie = {
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.AGENT.value
        }
        with self.assertRaises(exceptions.AgentNotFoundException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GAP_ANF)

    def test_get_agent_passport_failure_agent_state_not_valid(self):
        ''' get_agent_passport should fail if agent has no state or is non valid '''
        agentname='test_get_agent_passport_failure_agent_state_not_valid'
        pubkey=b'pubkey'
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        agent = ormagent.Agent(uid=uid, aid=aid, agentname=agentname, pubkey=pubkey)
        self.assertTrue(cassapiagent.new_agent(agent))
        cookie = {
            'sid':uuid.uuid4().hex,
            'aid':aid.hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.AGENT.value
        }
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GAP_IAS)

    def test_get_agent_passport_success(self):
        ''' get_agent_passport should succeed '''
        agentname='test_get_agent_passport_failure_agent_state_not_valid'
        pubkey=b'pubkey'
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        state = AgentStates.ACTIVE
        agent = ormagent.Agent(uid=uid, aid=aid, agentname=agentname, pubkey=pubkey, state=state)
        self.assertTrue(cassapiagent.new_agent(agent))
        cookie = {
            'sid':uuid.uuid4().hex,
            'aid':aid.hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),
            't':Cookies.AGENT.value
        }
        psp=passport.get_agent_passport(cookie)
        self.assertTrue(isinstance(psp, passport.AgentPassport))
        self.assertEqual(psp.aid, aid)
        self.assertEqual(psp.uid, uid)
        self.assertEqual(psp.sid, uuid.UUID(cookie['sid']))
        self.assertEqual(psp.pv, cookie['pv'])

    def test_check_agent_passport_validity_failure_invalid_passport(self):
        ''' check_agent_passport_validity should fail if passport is invalid '''
        psps = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}, passport.UserPassport(uid=uuid.uuid4(),sid=uuid.uuid4())]
        for psp in psps:
            with self.assertRaises(exceptions.PassportException) as cm:
                passport.check_agent_passport_validity(passport=psp)
            self.assertEqual(cm.exception.error, Errors.E_AP_CPV_IP)

    def test_check_agent_passport_validity_failure_non_existent_agent(self):
        ''' check_agent_passport_validity should fail if agent does not exist '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv = pv)
        with self.assertRaises(exceptions.AgentNotFoundException) as cm:
            passport.check_agent_passport_validity(passport=psp)
        self.assertEqual(cm.exception.error, Errors.E_AP_CPV_ANF)

    def test_check_agent_passport_validity_failure_invalid_agent_state(self):
        ''' check_agent_passport_validity should fail if agent is not active '''
        agentname='test_check_agent_passport_validity_failure_invalid_agent_state'
        pubkey=b'pubkey'
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        sid = uuid.uuid4()
        pv = 1
        state = AgentStates.SUSPENDED
        agent = ormagent.Agent(uid=uid, aid=aid, agentname=agentname, pubkey=pubkey, state=state)
        self.assertTrue(cassapiagent.new_agent(agent))
        psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv =pv)
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            passport.check_agent_passport_validity(passport=psp)
        self.assertEqual(cm.exception.error, Errors.E_AP_CPV_IAS)

    def test_check_agent_passport_validity_success(self):
        ''' check_agent_passport_validity should succeed '''
        agentname='test_check_agent_passport_validity_success'
        pubkey=b'pubkey'
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        sid = uuid.uuid4()
        pv = 1
        state = AgentStates.ACTIVE
        agent = ormagent.Agent(uid=uid, aid=aid, agentname=agentname, pubkey=pubkey, state=state)
        self.assertTrue(cassapiagent.new_agent(agent))
        psp = passport.AgentPassport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertIsNone(passport.check_agent_passport_validity(passport=psp))

