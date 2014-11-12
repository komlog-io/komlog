#!/usr/bin/env python

from komdb import api as dbapi
from komdb import connection as dbcon
from komdb import exceptions
import sys

import unittest, random, string


def get_random_string(length,prefix=None):
    if prefix:
        return prefix+''.join(random.choice(string.digits) for x in range(length))
    else:
        return ''.join(random.choice(string.digits) for x in range(length))


class KomdbFunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.db_uri='postgresql://komlog:temporal@be1/komlog'
        self.connection = dbcon.Connection(self.db_uri)
        self.users = []
        self.agents = []
        self.dss = []
        self.smpls = []
        
    def tearDown(self):
        for smpl in self.smpls:
            dbapi.delete_sample(smpl, self.connection.session)
        for ds in self.dss:
            dbapi.delete_datasource(ds, self.connection.session)
        for agent in self.agents:
            dbapi.delete_agent(agent, self.connection.session)
        for user in self.users:
            dbapi.delete_user(username=user, session=self.connection.session)
        self.connection = None

    def test_create_user_None_username(self):
        username=None
        password = get_random_string(11)
        self.assertRaises(exceptions.InvalidParameterValueError, dbapi.create_user,username,password, self.connection.session)
    
    def test_create_user_None_password(self):
        username = get_random_string(6,'tuser')
        password = None
        self.assertRaises(exceptions.InvalidParameterValueError, dbapi.create_user,username,password, self.connection.session)

    def test_create_user_invalid_state(self):
        username = get_random_string(6,'tuser')
        password = get_random_string(11)
        state = get_random_string(9)
        self.assertRaises(Exception,dbapi.create_user,username,password,self.connection.session,state=state)
        
    def test_create_user_invalid_type(self):
        username = get_random_string(6,'tuser')
        password = get_random_string(11)
        type = get_random_string(9)
        self.assertRaises(Exception,dbapi.create_user,username,password,self.connection.session,type=type)

    def test_create_user_OK(self):
        username = get_random_string(6,'tuser')
        password = get_random_string(11)
        uid = dbapi.create_user(username,password,self.connection.session)
        self.assertGreater(uid, 0, "test_user_creation uid>0")
        self.users.append(uid)
    
    def test_create_user_Duplicate(self):
        username = get_random_string(6,'tuser')
        password = get_random_string(11)
        uid = dbapi.create_user(username,password,self.connection.session)
        self.users.append(uid)
        self.assertRaises(exceptions.AlreadyExistingUserError, dbapi.create_user, username, password, self.connection.session)        

    def test_create_agent_None_username(self):
        username = None
        password = get_random_string(11)
        agentname = get_random_string(6,'tagent')
        self.assertRaises(exceptions.InvalidParameterValueError,dbapi.create_agent,username,agentname,password,self.connection.session)

    def test_create_agent_None_agentname(self):
        username = get_random_string(6,'tuser')
        password = get_random_string(11)
        agentname = None
        self.assertRaises(exceptions.InvalidParameterValueError,dbapi.create_agent,username,agentname,password,self.connection.session)

    def test_create_agent_None_password(self):
        username = get_random_string(6,'tuser')
        password = None
        agentname = get_random_string(6,'tagent')
        self.assertRaises(exceptions.InvalidParameterValueError,dbapi.create_agent,username,agentname,password,self.connection.session)

    def test_create_agent_invalid_state(self):
        password = get_random_string(11)
        agentname = get_random_string(6,'tagent')
        state = get_random_string(9)
        if len(self.users)==0:
            username = get_random_string(6,'tuser')
            uid = dbapi.create_user(username,password,self.connection.session)
            self.users.append(uid)
        uid = self.users[0]
        user = dbapi.User(uid=uid,session=self.connection.session)
        self.assertRaises(Exception,dbapi.create_agent,user.username,agentname,password,self.connection.session,state=state)
        self.connection.session.rollback()
        
    def test_create_agent_invalid_type(self):
        password = get_random_string(11)
        agentname = get_random_string(6,'tagent')
        if len(self.users)==0:
            username = get_random_string(6,'tuser')
            uid = dbapi.create_user(username,password,self.connection.session)
            self.users.append(uid)
        uid = self.users[0]
        user = dbapi.User(uid=uid,session=self.connection.session)
        type = get_random_string(9)
        self.assertRaises(Exception,dbapi.create_agent,user.username,agentname,password,self.connection.session,type=type)
        self.connection.session.rollback()

    def test_create_agent_OK(self):
        password = get_random_string(11)
        agentname = get_random_string(6,'tagent')
        if len(self.users)==0:
            username = get_random_string(6,'tuser')
            uid = dbapi.create_user(username,password,self.connection.session)
            self.users.append(uid)
        uid = self.users[0]
        user = dbapi.User(uid=uid,session=self.connection.session)
        aid = dbapi.create_agent(user.username,agentname,password,self.connection.session)
        self.assertGreater(aid, 0, "test_agent_creation aid>0")
        self.agents.append(aid)

    def test_create_agent_Duplicate(self):
        password = get_random_string(11)
        agentname = get_random_string(6,'tagent')
        if len(self.users)==0:
            username = get_random_string(6,'tuser')
            uid = dbapi.create_user(username,password,self.connection.session)
            self.users.append(uid)
        uid = self.users[0]
        user = dbapi.User(uid=uid,session=self.connection.session)
        aid = dbapi.create_agent(user.username,agentname,password,self.connection.session)
        self.agents.append(aid)
        self.assertRaises(exceptions.AlreadyExistingAgentError,dbapi.create_agent,user.username,agentname,password,self.connection.session)

    def test_create_agent_User_Not_Found(self):
        username = get_random_string(7,'tuser')
        password = get_random_string(11)
        agentname = get_random_string(6,'tagent')
        self.assertRaises(exceptions.NotFoundUserError,dbapi.create_agent,username,agentname,password,self.connection.session)    
    
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KomdbFunctionalTestCase)
    unittest.TextTestRunner(verbosity=3).run(suite)
