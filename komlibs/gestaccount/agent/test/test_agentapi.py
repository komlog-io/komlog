import unittest
import uuid
from komlibs.gestaccount.agent import api
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount import exceptions
from komcass.model.orm import agent as ormagent

class GestaccountAgentApiTest(unittest.TestCase):
    ''' komlog.gestaccount.agent.api tests '''
    
    def setUp(self):
        username='test_gestaccount.agent.api_user'
        password='password'
        email='test_gestaccount.agent.api_user@komlog.org'
        self.user=userapi.create_user(username=username, password=password, email=email)

    def test_create_agent_non_existent_user(self):
        ''' create_agent should fail if user is not found in system '''
        username='my_user_9'
        agentname='My Agent #9'
        pubkey='pubkeyRANDOM'
        version='Version X'
        self.assertRaises(exceptions.UserNotFoundException, api.create_agent,username=username, agentname=agentname, pubkey=pubkey, version=version) 

    def test_create_agent_success(self):
        ''' create_agent should succeed if arguments are OK, agent does not exists yet and user exists '''
        agentname='test_create_agent_success'
        pubkey='pubkey'
        version='Test Version'
        agent=api.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsInstance(agent, ormagent.Agent)

    def test_create_agent_already_existing_agent(self):
        ''' create_agent should fail if agent already exists '''
        agentname='test_create_agent_already_existing_agent'
        pubkey='pubkey'
        version='Test Version'
        agent=api.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertRaises(exceptions.AgentAlreadyExistsException, api.create_agent, username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)

    def test_activate_agent_non_existent_agent(self):
        ''' activate_agent should fail if agent is not found in system '''
        aid=uuid.uuid4()
        self.assertRaises(exceptions.AgentNotFoundException, api.activate_agent,aid=aid) 

    def test_activate_agent_success(self):
        ''' activate_agent should succeed if agent exists '''
        agentname='test_activate_agent_success'
        pubkey='pubkey'
        version='Test Version'
        agent=api.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(api.activate_agent(aid=agent.aid))

    def test_get_agent_config_non_existent_agent(self):
        ''' get_agent_config should fail if agent is not found in system '''
        aid=uuid.uuid4()
        self.assertRaises(exceptions.AgentNotFoundException, api.get_agent_config,aid=aid) 

    def test_get_agent_config_success(self):
        ''' get_agent_config should succeed if agent exists in system '''
        agentname='test_get_agent_config_success'
        pubkey='pubkey'
        version='Test Version'
        agent=api.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        data=api.get_agent_config(aid=agent.aid)
        self.assertIsInstance(data,dict) 

    def test_get_agents_config_non_existent_user(self):
        ''' get_agents_config should fail if username is not found in system '''
        username='my_user_10'
        self.assertRaises(exceptions.UserNotFoundException, api.get_agents_config,username=username)

    def test_get_agents_config_success(self):
        ''' get_agents_config should succeed if username exists in system '''
        username=self.user.username
        data=api.get_agents_config(username=username)
        self.assertIsInstance(data,list) 

    def test_update_agent_config_data_with_no_agentname(self):
        ''' update_agent_config should fail if data has no ag_name key'''
        username='my_user_16'
        aid=uuid.uuid4()
        data={'key':'value'}
        self.assertRaises(exceptions.BadParametersException, api.update_agent_config,username=username, aid=aid, data=data)

    def test_update_agent_config_data_with_empty_agentname(self):
        ''' update_agent_config should fail if data has empty ag_name'''
        username='my_user_17'
        aid=uuid.uuid4()
        data={'ag_name':None}
        self.assertRaises(exceptions.BadParametersException, api.update_agent_config,username=username, aid=aid, data=data)

    def test_update_agent_config_data_with_invalid_agentname(self):
        ''' update_agent_config should fail if data has invalid ag_name'''
        username='my_user_17'
        aid=uuid.uuid4()
        data={'ag_name':2342321434}
        self.assertRaises(exceptions.BadParametersException, api.update_agent_config,username=username, aid=aid, data=data)

    def test_update_agent_config_non_existent_agent(self):
        ''' update_agent_config should fail if agent is not in system '''
        username='my_user_18'
        aid=uuid.uuid4()
        data={'ag_name':'Agent Name #19'}
        self.assertRaises(exceptions.AgentNotFoundException, api.update_agent_config,username=username, aid=aid, data=data)

    def test_update_agent_config_success(self):
        ''' update_agent_config should succeed if agent exists in system '''
        agentname='test_update_agent_config_success'
        pubkey='pubkey'
        version='Test Version'
        agent=api.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        data={'ag_name':'test_update_agent_config_success_after_update'}
        self.assertTrue(api.update_agent_config(username=self.user.username, aid=agent.aid, data=data)) 

