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
from komlog.komlibs.gestaccount.user.states import UserStates
from komlog.komlibs.gestaccount.agent.states import AgentStates
from komlog.komlibs.general.time import timeuuid
from komlog.komfig import logging

class AuthPassportTest(unittest.TestCase):
    ''' komlog.auth.passport tests '''

    def test_passport_creation_success(self):
        ''' a new passport instance should be create successfully '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        aid = None
        pv = None
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertTrue(isinstance(psp, passport.Passport))
        aid = uuid.uuid4()
        pv = 1
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertTrue(isinstance(psp, passport.Passport))

    def test_passport_creation_failure_invalid_uid(self):
        ''' a new passport instance should fail if uid is invalid '''
        uids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), None, ('a','tuple'), ['an','array'],{'set'}]
        sid=uuid.uuid4()
        aid = None
        pv = None
        for uid in uids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IU)

    def test_passport_creation_failure_invalid_aid(self):
        ''' a new passport instance should fail if aid is invalid '''
        aids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        pv = 1
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IA)

    def test_passport_creation_failure_invalid_pv(self):
        ''' a new passport instance should fail if pv is invalid '''
        pvs= ['234234',-1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        for pv in pvs:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IPV)

    def test_passport_creation_failure_invalid_sid(self):
        ''' a new passport instance should fail if sid is invalid '''
        sids = [None,'234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.Passport(uid=uid, sid=sid, aid=aid)
            self.assertEqual(cm.exception.error, Errors.E_AP_PC_IS)

    def test_passport_creation_failure_one_of_aid_or_pv_is_None(self):
        ''' a new passport instance should fail if one of pv or aid is None '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        with self.assertRaises(exceptions.PassportException) as cm:
            aid = uuid.uuid4()
            pv = None
            psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertEqual(cm.exception.error, Errors.E_AP_PC_AIDORPV)
        with self.assertRaises(exceptions.PassportException) as cm:
            aid = None
            pv = 1
            psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertEqual(cm.exception.error, Errors.E_AP_PC_AIDORPV)
        aid = uuid.uuid4()
        pv = 1
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertTrue(isinstance(psp, passport.Passport))
        aid = None
        pv = None
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertTrue(isinstance(psp, passport.Passport))

    def test_cookie_creation_failure_invalid_cookie(self):
        ''' a new cookie instance should fail if cookie is invalid '''
        cookies= ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'},{'user':'user','aid':'aid','seq':'seq'}]
        for cookie in cookies:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_ID)

    def test_cookie_creation_failure_invalid_user(self):
        ''' a new cookie instance should fail if cookie user is invalid '''
        usernames= [1,1.2,{'a':'dict'},uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'},None]
        cookie={'sid':uuid.uuid4().hex, 'aid':uuid.uuid4().hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),'pv':1}
        for user in usernames:
            cookie['user']=user
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_IU)

    def test_cookie_creation_failure_invalid_aid(self):
        ''' a new cookie instance should fail if cookie aid is invalid '''
        aids= ['string',1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        cookie={'user':'username','sid':uuid.uuid4().hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),'pv':1}
        for aid in aids:
            cookie['aid']=aid
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_IA)

    def test_cookie_creation_failure_invalid_pv(self):
        ''' a new cookie instance should fail if cookie pv is invalid '''
        pvs= ['string',-1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        cookie={'user':'username','aid':uuid.uuid4().hex,'sid':uuid.uuid4().hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        for pv in pvs:
            cookie['pv']=pv
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_IPV)

    def test_cookie_creation_failure_invalid_sid(self):
        ''' a new cookie instance should fail if cookie sid is invalid '''
        sids= [None,'string',1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        cookie={'user':'username','aid':uuid.uuid4().hex, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1()),'pv':1}
        for sid in sids:
            cookie['sid']=sid
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_IS)

    def test_cookie_creation_failure_invalid_seq(self):
        ''' a new cookie instance should fail if cookie seq is invalid '''
        seqs= ['string',1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}, None]
        cookie={'user':'username','sid':uuid.uuid4().hex, 'aid':uuid.uuid4().hex,'pv':1}
        for seq in seqs:
            cookie['seq']=seq
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, Errors.E_AP_CC_ISQ)

    def test_get_user_passport_failure_non_existing_user(self):
        ''' get_user_passport should fail if user does not exist '''
        cookie = {
            'user':'test_get_user_passport_failure_non_existing_user',
            'sid':uuid.uuid4().hex,
            'aid':None,
            'pv':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
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
            'aid':None,
            'pv':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        user = ormuser.User(uid=uuid.uuid4(), username=username, password=password, email=email)
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
            'aid':None,
            'pv':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        user = ormuser.User(uid=uuid.uuid4(), username=username, password=password, email=email, state=state)
        self.assertTrue(cassapiuser.new_user(user))
        psp=passport.get_user_passport(cookie)
        self.assertTrue(isinstance(psp, passport.Passport))
        self.assertEqual(psp.uid, user.uid)
        self.assertEqual(psp.aid, None)

    def test_get_agent_passport_failure_cookie_has_no_agent(self):
        ''' get_agent_passport should fail if cookie has no agent '''
        cookie = {
            'user':'test_get_agent_passport_failure_cookie_has_no_aid',
            'sid':uuid.uuid4().hex,
            'aid':None,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GAP_CANF)

    def test_get_agent_passport_failure_agent_does_not_exist(self):
        ''' get_agent_passport should fail if agent does not exist '''
        cookie = {
            'user':'test_get_agent_passport_failure_non_existing_agent',
            'sid':uuid.uuid4().hex,
            'aid':uuid.uuid4().hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
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
            'user':'test_get_agent_passport_failure_agent_state_not_valid',
            'sid':uuid.uuid4().hex,
            'aid':aid.hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, Errors.E_AP_GAP_IAS)

    def test_get_agent_passport_failure_invalid_pv(self):
        ''' get_agent_passport should fail if pv is invalid '''
        agentname='test_get_agent_passport_failure_invalid_pv'
        pubkey=b'pubkey'
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        state = AgentStates.ACTIVE
        agent = ormagent.Agent(uid=uid, aid=aid, agentname=agentname, pubkey=pubkey, state=state)
        self.assertTrue(cassapiagent.new_agent(agent))
        cookie = {
            'user':'test_get_agent_passport_failure_agent_state_not_valid',
            'sid':uuid.uuid4().hex,
            'aid':aid.hex,
            'pv':-1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error,Errors.E_AP_CC_IPV)

    def test_get_agent_passport_failure_pv_is_None(self):
        ''' get_agent_passport should fail if pv is None '''
        agentname='test_get_agent_passport_failure_pv_is_none'
        pubkey=b'pubkey'
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        state = AgentStates.ACTIVE
        agent = ormagent.Agent(uid=uid, aid=aid, agentname=agentname, pubkey=pubkey, state=state)
        self.assertTrue(cassapiagent.new_agent(agent))
        cookie = {
            'user':'test_get_agent_passport_failure_agent_state_not_valid',
            'sid':uuid.uuid4().hex,
            'aid':aid.hex,
            'pv':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error,Errors.E_AP_GAP_CPVNF)

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
            'user':'test_get_agent_passport_failure_agent_state_not_valid',
            'sid':uuid.uuid4().hex,
            'aid':aid.hex,
            'pv':1,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        psp=passport.get_agent_passport(cookie)
        self.assertTrue(isinstance(psp, passport.Passport))
        self.assertEqual(psp.aid, aid)
        self.assertEqual(psp.uid, uid)

    def test_check_agent_passport_validity_failure_invalid_passport(self):
        ''' check_agent_passport_validity should fail if passport is invalid '''
        psps = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        for psp in psps:
            with self.assertRaises(exceptions.PassportException) as cm:
                passport.check_agent_passport_validity(passport=psp)
            self.assertEqual(cm.exception.error, Errors.E_AP_CPV_IP)

    def test_check_agent_passport_validity_failure_passport_has_no_agent(self):
        ''' check_agent_passport_validity should fail if passport has no agent '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        psp = passport.Passport(uid=uid, sid=sid)
        with self.assertRaises(exceptions.PassportException) as cm:
            passport.check_agent_passport_validity(passport=psp)
        self.assertEqual(cm.exception.error, Errors.E_AP_CPV_IAID)

    def test_check_agent_passport_validity_failure_non_existent_agent(self):
        ''' check_agent_passport_validity should fail if agent does not exist '''
        uid = uuid.uuid4()
        sid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv = pv)
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
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv =pv)
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
        psp = passport.Passport(uid=uid, sid=sid, aid=aid, pv=pv)
        self.assertIsNone(passport.check_agent_passport_validity(passport=psp))

