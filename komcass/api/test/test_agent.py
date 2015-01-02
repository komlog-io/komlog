import unittest
import uuid
import datetime
from komcass.api import agent as agentapi
from komcass.model.orm import agent as ormagent
from komcass.model.statement import agent as stmtagent
from komcass import connection


class KomcassApiAgentTest(unittest.TestCase):
    ''' komlog.komcass.api.agent tests '''

    def setUp(self):
        agentname='test_komlog.komcass.api.agent_agent1'
        pubkey='PUBKEY'
        version='VERSION'
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        creation_date=datetime.datetime.utcnow()
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
        pubkey='PUBKEY'
        version='VERSION'
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        creation_date=datetime.datetime.utcnow()
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
        ''' delete_agent should succeed if argument is an UUID '''
        self.assertTrue(agentapi.delete_agent(uuid.uuid4()))

