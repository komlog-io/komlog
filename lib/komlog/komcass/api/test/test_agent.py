import unittest
import uuid
import os
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import agent as agentapi
from komlog.komcass.model.orm import agent as ormagent
from komlog.komcass.model.statement import agent as stmtagent
from komlog.komcass import connection


class KomcassApiAgentTest(unittest.TestCase):
    ''' komlog.komcass.api.agent tests '''

    def setUp(self):
        agentname='test_komlog.komcass.api.agent_agent1'
        pubkey=b'PUBKEY'
        version='VERSION'
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        self.agent1=ormagent.Agent(agentname=agentname, uid=uid, aid=aid, pubkey=pubkey, version=version, creation_date=creation_date)
        agentapi.insert_agent(self.agent1)
        agentname='test_komlog.komcass.api.agent_agent2'
        aid=uuid.uuid4()
        self.agent2=ormagent.Agent(agentname=agentname, uid=uid, aid=aid, pubkey=pubkey, version=version, creation_date=creation_date)
        agentapi.insert_agent(self.agent2)

    def test_get_agent_existing_aid(self):
        ''' get_agent should succeed if we pass an existing aid '''
        aid=self.agent1.aid
        agent=agentapi.get_agent(aid=aid)
        self.assertEqual(agent.agentname, self.agent1.agentname)
        self.assertEqual(agent.aid, self.agent1.aid)
        self.assertEqual(agent.uid, self.agent1.uid)

    def test_get_agent_non_existing_aid(self):
        ''' get_agent should return None if we pass a non existing aid '''
        aid=uuid.uuid4()
        self.assertIsNone(agentapi.get_agent(aid=aid))

    def test_get_agents_existing_uid(self):
        ''' get_agents should succeed if we pass an existing uid '''
        uid=self.agent1.uid
        agents=agentapi.get_agents(uid=uid)
        self.assertEqual(len(agents),2)
        for agent in agents:
            self.assertTrue(isinstance(agent, ormagent.Agent))

    def test_get_agents_non_existing_uid(self):
        ''' get_agents should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        agents=agentapi.get_agents(uid=uid)
        self.assertTrue(isinstance(agents,list))
        self.assertEqual(len(agents),0)

    def test_get_agents_aids_existing_uid(self):
        ''' get_agents_aids should return an array of aids if we pass an existing uid '''
        uid=self.agent1.uid
        aids=agentapi.get_agents_aids(uid=uid)
        self.assertEqual(len(aids),2)
        for aid in aids:
            self.assertTrue(isinstance(aid, uuid.UUID))

    def test_get_agents_aids_non_existing_uid(self):
        ''' get_agents_aids should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        aids=agentapi.get_agents(uid=uid)
        self.assertTrue(isinstance(aids,list))
        self.assertEqual(len(aids),0)

    def test_get_number_of_agents_by_uid_success(self):
        ''' get_number_of_agents by uid should return the number of agents belonging to a uid '''
        uid=self.agent1.uid
        num_agents=agentapi.get_number_of_agents_by_uid(uid)
        self.assertEqual(num_agents, 2)

    def test_get_number_of_agents_by_uid_no_agents(self):
        ''' get_number_of_agents by uid should return the number of agents belonging to a uid '''
        uid=uuid.uuid4()
        num_agents=agentapi.get_number_of_agents_by_uid(uid)
        self.assertEqual(num_agents, 0)

    def test_new_agent_no_object(self):
        ''' new_agent should fail if argument is not an Agent object '''
        agents=[None, 123123, '1231231', {'a':'dict'},['a','list']]
        for agent in agents:
            self.assertFalse(agentapi.new_agent(agent))

    def test_new_agent_success(self):
        ''' new_agent should succeed if agent does not exist yet '''
        agentname='test_new_agent_success_agent'
        pubkey=b'PUBKEY'
        version='VERSION'
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        agent=ormagent.Agent(agentname=agentname, uid=uid, aid=aid, pubkey=pubkey, version=version, creation_date=creation_date)
        self.assertTrue(agentapi.new_agent(agent))

    def test_new_agent_already_existing_agent(self):
        ''' new_agent should fail if agent does exist already '''
        agent=self.agent1
        self.assertFalse(agentapi.new_agent(agent))

    def test_insert_agent_no_object(self):
        ''' insert_agent should fail if argument is not an Agent object '''
        agents=[None, 123123, '1231231', {'a':'dict'},['a','list']]
        for agent in agents:
            self.assertFalse(agentapi.insert_agent(agent))

    def test_new_agent_success(self):
        ''' insert_agent should succeed if agent is an Agent object and query executes '''
        agent=self.agent1
        self.assertTrue(agentapi.insert_agent(agent))

    def test_delete_agent_success(self):
        ''' delete_agent should delete the agent successfully '''
        uid=uuid.uuid4()
        agent1=ormagent.Agent(aid=uuid.uuid4(),uid=uid,agentname='agent1')
        self.assertTrue(agentapi.insert_agent(agent1))
        self.assertTrue(agentapi.delete_agent(aid=agent1.aid))
        self.assertIsNone(agentapi.get_agent(aid=agent1.aid))

    def test_get_agent_pubkey_none_found(self):
        ''' get_agent_pubkey should return None if none is found '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        self.assertIsNone(agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey))

    def test_get_agent_pubkey_found(self):
        ''' get_agent_pubkey should return the agent pubkey object '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        aid=uuid.uuid4()
        state=0
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+1)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+2)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        db_pubkey=agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey)
        self.assertIsNotNone(db_pubkey)
        self.assertTrue(isinstance(db_pubkey, ormagent.AgentPubkey))
        self.assertEqual(db_pubkey.uid, uid)
        self.assertEqual(db_pubkey.aid, aid)
        self.assertEqual(db_pubkey.pubkey, pubkey)
        self.assertEqual(db_pubkey.state, state+2)

    def test_get_agents_pubkeys_none_found(self):
        ''' get_agents_pubkeys should return and empty array if none is found '''
        uid=uuid.uuid4()
        self.assertEqual(agentapi.get_agents_pubkeys(uid=uid),[])

    def test_get_agents_pubkeys_found(self):
        ''' get_agents_pubkeys should return an array with the agents pubkeys objects '''
        uid=uuid.uuid4()
        pubkey1=b'textpubkey1'
        pubkey2=b'textpubkey2'
        pubkey3=b'textpubkey3'
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        aid3=uuid.uuid4()
        state=0
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey1, aid=aid1, state=state)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey2, aid=aid2, state=state+1)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey3, aid=aid3, state=state+2)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        pubkeys=agentapi.get_agents_pubkeys(uid=uid)
        self.assertEqual(len(pubkeys),3)

    def test_new_agent_pubkey_failure_invalid_agent_pubkey_instance(self):
        ''' new_agent_pubkey should fail if ojb is not and AgentPubkey instance '''
        agents=[None, 123123, '1231231', {'a':'dict'},['a','list'], uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'), {'set'}]
        for agent in agents:
            self.assertFalse(agentapi.new_agent_pubkey(obj=agent))

    def test_new_agent_pubkey_success(self):
        ''' new_agent_pubkey should succeed '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        aid=uuid.uuid4()
        state=0
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state)
        self.assertTrue(agentapi.new_agent_pubkey(obj=agent_pubkey))
        db_pubkey=agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey)
        self.assertIsNotNone(db_pubkey)
        self.assertTrue(isinstance(db_pubkey, ormagent.AgentPubkey))
        self.assertEqual(db_pubkey.uid, uid)
        self.assertEqual(db_pubkey.aid, aid)
        self.assertEqual(db_pubkey.pubkey, pubkey)
        self.assertEqual(db_pubkey.state, state)

    def test_new_agent_pubkey_failure_already_existing_pubkey(self):
        ''' new_agent_pubkey should fail if uid-pubkey combination already exists '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        aid=uuid.uuid4()
        state=0
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state)
        self.assertTrue(agentapi.new_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+1)
        self.assertFalse(agentapi.new_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+2)
        self.assertFalse(agentapi.new_agent_pubkey(obj=agent_pubkey))
        db_pubkey=agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey)
        self.assertIsNotNone(db_pubkey)
        self.assertTrue(isinstance(db_pubkey, ormagent.AgentPubkey))
        self.assertEqual(db_pubkey.uid, uid)
        self.assertEqual(db_pubkey.aid, aid)
        self.assertEqual(db_pubkey.pubkey, pubkey)
        self.assertEqual(db_pubkey.state, state)

    def test_insert_agent_pubkey_failure_invalid_agent_pubkey_instance(self):
        ''' insert_agent_pubkey should fail if ojb is not and AgentPubkey instance '''
        agents=[None, 123123, '1231231', {'a':'dict'},['a','list'], uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'), {'set'}]
        for agent in agents:
            self.assertFalse(agentapi.insert_agent_pubkey(obj=agent))

    def test_insert_agent_pubkey_success(self):
        ''' insert_agent_pubkey should succeed '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        aid=uuid.uuid4()
        state=0
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+1)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+2)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        db_pubkey=agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey)
        self.assertIsNotNone(db_pubkey)
        self.assertTrue(isinstance(db_pubkey, ormagent.AgentPubkey))
        self.assertEqual(db_pubkey.uid, uid)
        self.assertEqual(db_pubkey.aid, aid)
        self.assertEqual(db_pubkey.pubkey, pubkey)
        self.assertEqual(db_pubkey.state, state+2)

    def test_delete_agent_pubkey(self):
        ''' delete_agent_pubkey should succeed even if pubkey does not exist '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        self.assertTrue(agentapi.delete_agent_pubkey(uid=uid, pubkey=pubkey))

    def test_delete_agent_pubkey_success(self):
        ''' delete_agent_pubkey should delete the pubkey from db '''
        uid=uuid.uuid4()
        pubkey=b'textpubkey'
        aid=uuid.uuid4()
        state=0
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+1)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=state+2)
        self.assertTrue(agentapi.insert_agent_pubkey(obj=agent_pubkey))
        db_pubkey=agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey)
        self.assertIsNotNone(db_pubkey)
        self.assertTrue(isinstance(db_pubkey, ormagent.AgentPubkey))
        self.assertEqual(db_pubkey.uid, uid)
        self.assertEqual(db_pubkey.aid, aid)
        self.assertEqual(db_pubkey.pubkey, pubkey)
        self.assertEqual(db_pubkey.state, state+2)
        self.assertTrue(agentapi.delete_agent_pubkey(uid=uid, pubkey=pubkey))
        self.assertIsNone(agentapi.get_agent_pubkey(uid=uid, pubkey=pubkey))

    def test_get_agent_challenge_none_found(self):
        ''' get_agent_challenge should return none if none is found '''
        aid=uuid.uuid4()
        challenge=os.urandom(64)
        self.assertIsNone(agentapi.get_agent_challenge(aid=aid, challenge=challenge))

    def test_get_agent_challenge_success(self):
        ''' get_agent_challenge should return the AgentChallenge object '''
        aid=uuid.uuid4()
        challenge=os.urandom(64)
        generated = timeuuid.uuid1()
        validated = None
        agent_ch = ormagent.AgentChallenge(aid=aid, challenge=challenge, generated=generated)
        self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
        db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
        self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertEqual(db_ch.aid, aid)
        self.assertEqual(db_ch.challenge, challenge)
        self.assertEqual(db_ch.generated, generated)
        self.assertEqual(db_ch.validated, validated)
        validated=timeuuid.uuid1()
        agent_ch.validated=validated
        self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
        db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
        self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertEqual(db_ch.aid, aid)
        self.assertEqual(db_ch.challenge, challenge)
        self.assertEqual(db_ch.generated, generated)
        self.assertEqual(db_ch.validated, validated)

    def test_insert_agent_challenge_failure_invalid_agent_challenge_instance(self):
        ''' insert_agent_challenge should fail if ojb is not and AgentChallenge instance '''
        agents=[None, 123123, '1231231', {'a':'dict'},['a','list'], uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'), {'set'}, ormagent.Agent(1,1), ormagent.AgentPubkey(1,1,1,1)]
        for agent in agents:
            self.assertFalse(agentapi.insert_agent_challenge(obj=agent))

    def test_insert_agent_challenge_success(self):
        ''' insert_agent_challenge should succeed '''
        aid=uuid.uuid4()
        challenge=os.urandom(64)
        generated = timeuuid.uuid1()
        validated = None
        agent_ch = ormagent.AgentChallenge(aid=aid, challenge=challenge, generated=generated)
        self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
        db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
        self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertEqual(db_ch.aid, aid)
        self.assertEqual(db_ch.challenge, challenge)
        self.assertEqual(db_ch.generated, generated)
        self.assertEqual(db_ch.validated, validated)
        validated=timeuuid.uuid1()
        agent_ch.validated=validated
        self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
        db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
        self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertEqual(db_ch.aid, aid)
        self.assertEqual(db_ch.challenge, challenge)
        self.assertEqual(db_ch.generated, generated)
        self.assertEqual(db_ch.validated, validated)

    def test_delete_agent_challenge(self):
        ''' delete_agent_challenge should succeed even if challenge does not exist '''
        aid=uuid.uuid4()
        challenge=os.urandom(64)
        self.assertTrue(agentapi.delete_agent_challenge(aid=aid, challenge=challenge))

    def test_delete_agent_challenge_success(self):
        ''' delete_agent_challenge should succeed '''
        aid=uuid.uuid4()
        challenge=os.urandom(64)
        generated = timeuuid.uuid1()
        validated = None
        agent_ch = ormagent.AgentChallenge(aid=aid, challenge=challenge, generated=generated)
        self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
        db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
        self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertEqual(db_ch.aid, aid)
        self.assertEqual(db_ch.challenge, challenge)
        self.assertEqual(db_ch.generated, generated)
        self.assertEqual(db_ch.validated, validated)
        validated=timeuuid.uuid1()
        agent_ch.validated=validated
        self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
        db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
        self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertEqual(db_ch.aid, aid)
        self.assertEqual(db_ch.challenge, challenge)
        self.assertEqual(db_ch.generated, generated)
        self.assertEqual(db_ch.validated, validated)
        self.assertTrue(agentapi.delete_agent_challenge(aid=aid, challenge=challenge))
        self.assertIsNone(agentapi.get_agent_challenge(aid=aid, challenge=challenge))

    def test_delete_agent_challenges(self):
        ''' delete_agent_challenges should succeed even if agent has no challenges '''
        aid=uuid.uuid4()
        self.assertTrue(agentapi.delete_agent_challenges(aid=aid))

    def test_delete_agent_challenges_success(self):
        ''' delete_agent_challenges should succeed '''
        aid=uuid.uuid4()
        challenges=[]
        for i in range(1,1001):
            challenge=os.urandom(64)
            generated = timeuuid.uuid1()
            validated = None
            agent_ch = ormagent.AgentChallenge(aid=aid, challenge=challenge, generated=generated)
            self.assertTrue(agentapi.insert_agent_challenge(obj=agent_ch))
            challenges.append(challenge)
        for challenge in challenges:
            db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
            self.assertTrue(isinstance(db_ch, ormagent.AgentChallenge))
        self.assertTrue(agentapi.delete_agent_challenges(aid=aid))
        for challenge in challenges:
            db_ch = agentapi.get_agent_challenge(aid=aid, challenge=challenge)
            self.assertIsNone(db_ch)

    def test_get_agent_session_not_found(self):
        ''' get_agent_session should return none if sid is not found '''
        sid=uuid.uuid4()
        self.assertIsNone(agentapi.get_agent_session(sid=sid))

    def test_get_agent_session_found(self):
        ''' get_agent_session should return an AgentSession object if sid is found '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)

    def test_insert_agent_session_failure_invalid_agent_session_instance(self):
        ''' insert_agent_session should fail if obj is not and AgentSession instance '''
        sessions=[None, 123123, '1231231', {'a':'dict'},['a','list'], uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'), {'set'}]
        for session in sessions:
            self.assertFalse(agentapi.insert_agent_session(obj=session))

    def test_insert_agent_session_success(self):
        ''' insert_agent_session should return True and insert the AgentSession object '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)

    def test_update_agent_session_if_last_update_failure_invalid_agent_session_instance(self):
        ''' update_agent_session_if_last_update should fail if obj is not and AgentSession instance '''
        sessions=[None, 123123, '1231231', {'a':'dict'},['a','list'], uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'), {'set'}]
        last_update=timeuuid.uuid1()
        for session in sessions:
            self.assertFalse(agentapi.update_agent_session_if_last_update(obj=session, last_update=last_update))

    def test_update_agent_session_if_last_update_failure_session_does_not_exist(self):
        ''' update_agent_session_if_last_update should fail if session does not exist '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        last_update=timeuuid.uuid1()
        self.assertFalse(agentapi.update_agent_session_if_last_update(obj=session, last_update=last_update))

    def test_update_agent_session_if_last_update_success(self):
        ''' update_agent_session_if_last_update should return True and insert the AgentSession object if it exists and last_update is later than saved value '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        imc_address='host@imc.address'
        pv=2
        last_update=timeuuid.uuid1()
        new_session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.update_agent_session_if_last_update(obj=new_session, last_update=last_update))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)

    def test_update_agent_session_if_last_update_failure_last_update_earlier(self):
        ''' update_agent_session_if_last_update should fail if last_update is earlier than saved value '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=3
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        new_session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        last_update=timeuuid.uuid1(seconds=1)
        self.assertFalse(agentapi.update_agent_session_if_last_update(obj=session, last_update=last_update))
        db_session2=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session2)
        self.assertEqual(db_session.sid,db_session2.sid)
        self.assertEqual(db_session.aid,db_session2.aid)
        self.assertEqual(db_session.uid,db_session2.uid)
        self.assertEqual(db_session.pv,db_session2.pv)
        self.assertEqual(db_session.last_update,db_session2.last_update)
        self.assertEqual(db_session.imc_address,db_session2.imc_address)

    def test_delete_agent_session_success_agent_session_does_not_exist(self):
        ''' delete_agent_session should return True even if sid does not exist '''
        sid=uuid.uuid4()
        self.assertTrue(agentapi.delete_agent_session(sid=sid))

    def test_delete_agent_session_success(self):
        ''' delete_agent_session should return True and delete the AgentSession object '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)
        self.assertTrue(agentapi.delete_agent_session(sid=sid))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNone(db_session)

    def test_delete_agent_sessions_success_agent_does_not_exist(self):
        ''' delete_agent_session should return True even if aid does not exist '''
        aid=uuid.uuid4()
        self.assertTrue(agentapi.delete_agent_sessions(aid=aid))

    def test_delete_agent_session_if_last_update_failure_agent_session_does_not_exist(self):
        ''' delete_agent_session_if_last_update should return False if sid does not exist '''
        sid=uuid.uuid4()
        last_update=uuid.uuid1()
        self.assertFalse(agentapi.delete_agent_session_if_last_update(sid=sid, last_update=last_update))

    def test_delete_agent_session_if_last_update_success(self):
        ''' delete_agent_session_if_last_update should return True and delete the AgentSession object if session exists and last_update is later than the stored value '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)
        last_update=timeuuid.uuid1()
        self.assertTrue(agentapi.delete_agent_session_if_last_update(sid=sid, last_update=last_update))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNone(db_session)

    def test_delete_agent_session_if_last_update_failure(self):
        ''' delete_agent_session_if_last_update should return False if session exists and last_update is earlier than the stored value '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        imc_address='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid, aid=aid,uid=uid,pv=pv,imc_address=imc_address,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)
        self.assertEqual(db_session.sid,sid)
        self.assertEqual(db_session.aid,aid)
        self.assertEqual(db_session.uid,uid)
        self.assertEqual(db_session.pv,pv)
        self.assertEqual(db_session.last_update,last_update)
        self.assertEqual(db_session.imc_address,imc_address)
        last_update=timeuuid.uuid1(seconds=1)
        self.assertFalse(agentapi.delete_agent_session_if_last_update(sid=sid, last_update=last_update))
        db_session=agentapi.get_agent_session(sid=sid)
        self.assertIsNotNone(db_session)

    def test_delete_agent_sessions_success(self):
        ''' delete_agent_sessions should return True and delete all agent sessions '''
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pv=1
        sid1=uuid.uuid4()
        imc_address1='host@imc.address'
        last_update=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid1, aid=aid,uid=uid,pv=pv,imc_address=imc_address1,last_update=last_update)
        self.assertTrue(agentapi.insert_agent_session(session))
        sid2=uuid.uuid4()
        imc_address2='host@imc.address2'
        last_update2=timeuuid.uuid1()
        session=ormagent.AgentSession(sid=sid2, aid=aid,uid=uid,pv=pv,imc_address=imc_address2,last_update=last_update2)
        self.assertTrue(agentapi.insert_agent_session(session))
        self.assertIsNotNone(agentapi.get_agent_session(sid=sid1))
        self.assertIsNotNone(agentapi.get_agent_session(sid=sid2))
        self.assertTrue(agentapi.delete_agent_sessions(aid=aid))
        self.assertIsNone(agentapi.get_agent_session(sid=sid1))
        self.assertIsNone(agentapi.get_agent_session(sid=sid2))

