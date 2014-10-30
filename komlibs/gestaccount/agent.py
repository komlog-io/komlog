'''
agent.py: library for managing administrative agent operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
from komcass.api import agent as cassapiagent
from komcass.api import user as cassapiuser
from komcass.api import datasource as cassapidatasource
from komcass.model.orm import agent as ormagent
from komlibs.gestaccount import states as states
from komlibs.gestaccount import exceptions
from komlibs.ifaceops import operations
from komimc import messages
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from datetime import datetime


def decrypt(pubkey,cmsg):
    pubkey=RSA.importKey(pubkey)
    return pubkey.decrypt(cmsg)

def verify_signature(pubkey,text,b64sign):
    rsakey=RSA.importKey(pubkey)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(text)
    signature=b64decode(b64sign)
    if signer.verify(digest,signature):
        return True
    return False
    
def create_agent(username,agentname,pubkey,version,msgbus):
    '''
    When the agent connects the first time, we will register it in a pending state, 
    waiting for the user validation to gain access to the system
    '''
    user=cassapiuser.get_user(username=username)
    if user:
        agents=cassapiagent.get_agents(uid=user.uid)
        for agent in agents:
            if agent.pubkey==pubkey:
                data={'aid':agent.pubkey}
                return data
        ''' Register new agent '''
        print 'llegamos al registro del agente'
        aid=uuid.uuid4()
        now=datetime.utcnow()
        agent=ormagent.Agent(aid=aid, uid=user.uid, agentname=agentname, pubkey=pubkey, version=version, state=states.AGENT['PENDING_USER_VALIDATION'],creation_date=now)
        if cassapiagent.new_agent(agent=agent):
            ''' Send Quote and Resource Authorization Message before returning'''
            operation=operations.NewAgentOperation(uid=agent.uid,aid=agent.aid)
            message=messages.UpdateQuotesMessage(operation=operation)
            msgbus.sendMessage(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            msgbus.sendMessage(message)
            print 'Return New Agent id'
            data={'aid':str(aid)}
            return data
        else:
            raise exceptions.AgentCreationException()
    else:
        raise exceptions.UserNotFoundException()

def activate_agent(aid):
    '''
    After an agent has been registered, the user can validate it.
    This function changes the state column of the agent to validate it
    '''
    #TODO: Change agent state
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        if cassapiagent.insert_agent(agent=agent):
            return True
        else:
            raise exceptions.AgentUpdateException()
    else:
        raise exceptions.AgentNotFoundException()

def get_agent_config(aid,dids_flag=False):
    '''
    This function returns agent configuration parameters, if dids_flag is set
    to True, it will also return datasource ids associated to the agent
    '''
    data={}
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        data['aid']=str(aid)
        data['name']=agent.agentname
        data['state']=agent.state
        data['version']=agent.version
        if dids_flag:
            dids=cassapidatasource.get_datasources_dids(aid=aid)
            data['dids']=[str(did) for did in dids] if dids else []
        return data
    else:
        raise exceptions.AgentNotFoundException()

def get_agents_config(username,dids_flag=False):
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    else:
        aids=cassapiagent.get_agents_aids(uid=user.uid)
        data=[]
        for aid in aids:
            try:
                agent_data=get_agent_config(aid=aid,dids_flag=dids_flag)
            except Exception:
                continue
            else:
                data.append(agent_data)
        return data
    
def update_agent_config(username, aid, data, msgbus):
    if not data.has_key('ag_name'):
        raise exceptions.BadParametersException()
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException()
    agent.agentname=data['ag_name']
    if not cassapiagent.insert_agent(agent=agent):
        raise exceptions.AgentUpdateException()

