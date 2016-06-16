import unittest
import uuid
from komlog.komlibs.auth import session
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import agent as ormagent

class AuthSessionTest(unittest.TestCase):
    ''' komlog.auth.session tests '''

    def test_set_agent_session_success(self):
        ''' set_agent_session should succeed '''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)

    def test_unset_agent_session_success(self):
        ''' unset_agent_session should succeed '''
        sid = uuid.uuid4()
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid))
        agentsession=cassapiagent.get_agent_session(sid=sid)
        self.assertTrue(isinstance(agentsession, ormagent.AgentSession))
        self.assertEqual(sid, agentsession.sid)
        self.assertEqual(aid, agentsession.aid)
        self.assertEqual(uid, agentsession.uid)
        self.assertEqual('koms1:org.komlog.internal.imc.module.Tester.0', agentsession.imc_address)
        self.assertTrue(session.unset_agent_session(sid=sid))
        self.assertIsNone(cassapiagent.get_agent_session(sid=sid))

