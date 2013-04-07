'''
agents.py: library for managing administrative agent operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
from komcass import api as cassapi
from komlibs.gestaccount import states as states

def create_agent(username,agentname,agentkey,version,session):
    '''
    When the agent connects the first time, we will register it in a pending state, 
    waiting for the user validation to gain access to the system
    '''
    useruidr=cassapi.get_useruidrelation(username,session)
    if useruidr:
        aid=uuid.uuid4()
        agentinfo=cassapi.AgentInfo(aid=aid, uid=useruidr.uid, agentname=agentname, agentkey=agentkey, version=version, state=states.AGENT['PENDING_USER_VALIDATION'])
        if cassapi.register_agent(agentinfo,session):
            return True
        else:
            return False
    else:
        return False

def validate_agent(aid,session):
    '''
    After an agent has been registered, the user can validate it.
    This function changes the state column of the agent to validate it
    '''
    agentinfo=cassapi.AgentInfo(aid=aid,state=states.AGENT['ACTIVE'])
    if cassapi.update_agent(agentinfo,session):
        return True
    else:
        return False

