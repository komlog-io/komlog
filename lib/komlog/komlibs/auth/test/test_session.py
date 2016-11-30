import unittest
import uuid
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import agent as ormagent
from komlog.komlibs.auth import session, exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.general.time import timeuuid

class AuthSessionTest(unittest.TestCase):
    ''' komlog.auth.session tests '''

    def test_set_agent_session_failure_invalid_sid(self):
        ''' set_agent_session should fail if sid is invalid '''
        sids=['a',23,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv = 1
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.set_agent_session(sid=sid, aid=aid, uid=uid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AS_SAGS_ISID)

    def test_set_agent_session_failure_invalid_aid(self):
        ''' set_agent_session should fail if aid is invalid '''
        aids=['a',23,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        sid=uuid.uuid4()
        uid=uuid.uuid4()
        pv = 1
        for aid in aids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.set_agent_session(sid=sid, aid=aid, uid=uid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AS_SAGS_IAID)

    def test_set_agent_session_failure_invalid_pv(self):
        ''' set_agent_session should fail if pv is invalid '''
        pvs=['a',-1,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        sid=uuid.uuid4()
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        for pv in pvs:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.set_agent_session(sid=sid, aid=aid, uid=uid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AS_SAGS_IPV)

    def test_set_agent_session_failure_invalid_uid(self):
        ''' set_agent_session should fail if uid is invalid '''
        uids=['a',23,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        aid=uuid.uuid4()
        pv = 1
        sid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.set_agent_session(sid=sid, aid=aid, uid=uid, pv=pv)
            self.assertEqual(cm.exception.error, Errors.E_AS_SAGS_IUID)

    def test_set_agent_session_success(self):
        ''' set_agent_session should succeed '''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=pv))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)

    def test_unset_agent_session_failure_invalid_sid(self):
        ''' unset_agent_session should fail if sid is invalid '''
        sids=['a',23,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.unset_agent_session(sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_AS_USAGS_ISID)

    def test_unset_agent_session_failure_invalid_last_update(self):
        ''' unset_agent_session should fail if last_update is invalid '''
        last_updates=['a',23,23.23,uuid.uuid4(),uuid.uuid1().hex,{'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        sid=uuid.uuid4()
        for last_update in last_updates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.unset_agent_session(sid=sid, last_update=last_update)
            self.assertEqual(cm.exception.error, Errors.E_AS_USAGS_ILU)

    def test_unset_agent_session_success(self):
        ''' unset_agent_session should succeed '''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=pv))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(pv, agentsession.pv)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)
        self.assertTrue(session.unset_agent_session(sid=sid))
        agentsession2=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession2.sid)
        self.assertEqual(None, agentsession2.aid)
        self.assertEqual(None, agentsession2.pv)
        self.assertEqual(None, agentsession2.uid)
        self.assertEqual(None, agentsession2.imc_address)
        self.assertTrue(agentsession.last_update.time<agentsession2.last_update.time)

    def test_unset_agent_session_success_with_last_update(self):
        ''' unset_agent_session should succeed with last_update set'''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=pv))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual(pv, agentsession.pv)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)
        last_update=agentsession.last_update
        before_last_update=timeuuid.uuid1(seconds=1)
        self.assertFalse(session.unset_agent_session(sid=sid, last_update=before_last_update))
        agentsession2=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession2, ormagent.AgentSession))
        self.assertEqual(sid, agentsession2.sid)
        self.assertEqual(aid, agentsession2.aid)
        self.assertEqual(pv, agentsession2.pv)
        self.assertEqual(uid, agentsession2.uid)
        self.assertEqual(agentsession.imc_address, agentsession2.imc_address)
        self.assertTrue(agentsession.last_update.time==agentsession2.last_update.time)
        after_last_update=timeuuid.uuid1()
        self.assertTrue(session.unset_agent_session(sid=sid, last_update=after_last_update))
        agentsession2=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession2, ormagent.AgentSession))
        self.assertEqual(sid, agentsession2.sid)
        self.assertEqual(None, agentsession2.aid)
        self.assertEqual(None, agentsession2.pv)
        self.assertEqual(None, agentsession2.uid)
        self.assertEqual(None, agentsession2.imc_address)
        self.assertTrue(agentsession.last_update.time<agentsession2.last_update.time)

    def test_delete_agent_session_failure_invalid_sid(self):
        ''' delete_agent_session should fail if sid is invalid '''
        sids=['a',23,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.delete_agent_session(sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_AS_DAGS_ISID)

    def test_delete_agent_session_failure_invalid_last_update(self):
        ''' delete_agent_session should fail if last_update is invalid '''
        last_updates=['a',23,23.23,uuid.uuid4(),uuid.uuid1().hex,{'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        sid=uuid.uuid4()
        for last_update in last_updates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.delete_agent_session(sid=sid, last_update=last_update)
            self.assertEqual(cm.exception.error, Errors.E_AS_DAGS_ILU)

    def test_delete_agent_session_success(self):
        ''' delete_agent_session should succeed '''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=pv))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(pv, agentsession.pv)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)
        self.assertTrue(session.delete_agent_session(sid=sid))
        self.assertIsNone(cassapiagent.get_agent_session(sid=sid))

    def test_delete_agent_session_success_with_last_update(self):
        ''' delete_agent_session should succeed with last_update set'''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv= 1
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=pv))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(pv, agentsession.pv)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)
        last_update=agentsession.last_update
        before_last_update=timeuuid.uuid1(seconds=1)
        self.assertFalse(session.delete_agent_session(sid=sid, last_update=before_last_update))
        agentsession2=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession2, ormagent.AgentSession))
        self.assertEqual(sid, agentsession2.sid)
        self.assertEqual(aid, agentsession2.aid)
        self.assertEqual(pv, agentsession2.pv)
        self.assertEqual(uid, agentsession2.uid)
        self.assertEqual(agentsession.imc_address, agentsession2.imc_address)
        self.assertTrue(agentsession.last_update.time==agentsession2.last_update.time)
        after_last_update=timeuuid.uuid1()
        self.assertTrue(session.delete_agent_session(sid=sid, last_update=after_last_update))
        self.assertIsNone(cassapiagent.get_agent_session(sid=sid))

    def test_get_agent_session_info_failure_invalid_sid(self):
        ''' get_agent_session_info should fail if sid is not valid '''
        sids=['a',23,23.23,uuid.uuid4().hex,uuid.uuid1(),{'a':'dict'},['a','list'],('a','tuple'),{'set'},None]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                session.get_agent_session_info(sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_AS_GASI_ISID)

    def test_get_agent_session_info_failure_session_not_found(self):
        ''' get_agent_session_info should fail if sid is not found '''
        sid=uuid.uuid4()
        with self.assertRaises(exceptions.SessionNotFoundException) as cm:
            session.get_agent_session_info(sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_AS_GASI_SNF)

    def test_get_agent_session_info_success(self):
        ''' get_agent_session_info should return the AgentSession object '''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        pv = 1
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=pv))
        agentsession=session.get_agent_session_info(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual(pv, agentsession.pv)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)

