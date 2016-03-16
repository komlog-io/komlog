import unittest
import uuid
import inspect
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.model.orm import user as ormuser
from komcass.model.orm import agent as ormagent
from komlibs.auth import passport
from komlibs.auth import exceptions, errors
from komlibs.gestaccount.user.states import UserStates
from komlibs.gestaccount.agent.states import AgentStates
from komlibs.general.time import timeuuid
from komfig import logger

class AuthPassportTest(unittest.TestCase):
    ''' komlog.auth.passport tests '''

    def test_passport_creation_success(self):
        ''' a new passport instance should be create successfully '''
        uid = uuid.uuid4()
        aid = None
        psp = passport.Passport(uid=uid, aid=aid)
        self.assertTrue(isinstance(psp, passport.Passport))
        aid = uuid.uuid4()
        psp = passport.Passport(uid=uid, aid=aid)
        self.assertTrue(isinstance(psp, passport.Passport))

    def test_passport_creation_failure_invalid_uid(self):
        ''' a new passport instance should fail if uid is invalid '''
        uids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), None, ('a','tuple'), ['an','array'],{'set'}]
        aid = None
        for uid in uids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.Passport(uid=uid, aid=aid)
            self.assertEqual(cm.exception.error, errors.E_AP_PC_IU)

    def test_passport_creation_failure_invalid_aid(self):
        ''' a new passport instance should fail if aid is invalid '''
        aids = ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'}]
        uid = uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.PassportException) as cm:
                psp = passport.Passport(uid=uid, aid=aid)
            self.assertEqual(cm.exception.error, errors.E_AP_PC_IA)

    def test_cookie_creation_failure_invalid_cookie(self):
        ''' a new cookie instance should fail if cookie is invalid '''
        cookies= ['234234',1,1.2,{'a':'dict'},uuid.uuid4().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        for cookie in cookies:
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, errors.E_AP_CC_ID)

    def test_cookie_creation_failure_invalid_user(self):
        ''' a new cookie instance should fail if cookie user is invalid '''
        usernames= [1,1.2,{'a':'dict'},uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'},None]
        cookie={'aid':uuid.uuid4().hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        for user in usernames:
            cookie['user']=user
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, errors.E_AP_CC_IU)

    def test_cookie_creation_failure_invalid_aid(self):
        ''' a new cookie instance should fail if cookie aid is invalid '''
        aids= ['string',1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}]
        cookie={'user':'username','seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        for aid in aids:
            cookie['aid']=aid
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, errors.E_AP_CC_IA)

    def test_cookie_creation_failure_invalid_seq(self):
        ''' a new cookie instance should fail if cookie seq is invalid '''
        seqs= ['string',1,1.2,{'a':'dict'},uuid.uuid4(),uuid.uuid1().hex, uuid.uuid1(), ('a','tuple'), ['an','array'],{'set'},{'user':'user','aid':'aid'}, None]
        cookie={'user':'username','aid':uuid.uuid4().hex}
        for seq in seqs:
            cookie['seq']=seq
            with self.assertRaises(exceptions.CookieException) as cm:
                cookie = passport.Cookie(cookie)
            self.assertEqual(cm.exception.error, errors.E_AP_CC_IS)

    def test_get_user_passport_failure_non_existing_user(self):
        ''' get_user_passport should fail if user does not exist '''
        cookie = {
            'user':'test_get_user_passport_failure_non_existing_user',
            'aid':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            psp=passport.get_user_passport(cookie)
        self.assertEqual(cm.exception.error, errors.E_AP_GUP_UNF)

    def test_get_user_passport_failure_invalid_user_state(self):
        ''' get_user_passport should fail if user state does not exist nor allow connection '''
        username='test_get_user_passport_failure_invalid_user_state'
        password=b'password'
        email=username+'@komlog.org'
        cookie = {
            'user':username,
            'aid':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        user = ormuser.User(uid=uuid.uuid4(), username=username, password=password, email=email)
        self.assertTrue(cassapiuser.new_user(user))
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            psp=passport.get_user_passport(cookie)
        self.assertEqual(cm.exception.error, errors.E_AP_GUP_IUS)

    def test_get_user_passport_success(self):
        ''' get_user_passport should succeed '''
        username='test_get_user_passport_success'
        password=b'password'
        email=username+'@komlog.org'
        state=UserStates.ACTIVE
        cookie = {
            'user':username,
            'aid':None,
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
            'aid':None,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.CookieException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, errors.E_AP_GAP_CANF)

    def test_get_agent_passport_failure_agent_does_not_exist(self):
        ''' get_agent_passport should fail if agent does not exist '''
        cookie = {
            'user':'test_get_agent_passport_failure_non_existing_agent',
            'aid':uuid.uuid4().hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.AgentNotFoundException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, errors.E_AP_GAP_ANF)

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
            'aid':aid.hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        with self.assertRaises(exceptions.AuthorizationExpiredException) as cm:
            psp=passport.get_agent_passport(cookie)
        self.assertEqual(cm.exception.error, errors.E_AP_GAP_IAS)

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
            'aid':aid.hex,
            'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())
        }
        psp=passport.get_agent_passport(cookie)
        self.assertTrue(isinstance(psp, passport.Passport))
        self.assertEqual(psp.aid, aid)
        self.assertEqual(psp.uid, uid)

