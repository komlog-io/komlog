'''
agents.py: library for managing administrative agent operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
from komcass import api as cassapi
from komlibs.gestaccount import states as states
from komlibs.gestaccount import exceptions
from Crypto.PublicKey import RSA


def decrypt(pubkey,cmsg):
    pubkey=RSA.importKey(pubkey)
    return pubkey.decrypt(cmsg)

    
def create_agent(username,agentname,agentkey,version,session):
    '''
    When the agent connects the first time, we will register it in a pending state, 
    waiting for the user validation to gain access to the system
    '''
    useruidr=cassapi.get_useruidrelation(username,session)
    if useruidr:
        useragentpubkeyr=cassapi.get_useragentpubkeyrelation(useruidr.uid,{agentkey:u''},session)
        if useragentpubkeyr:
            ''' Agent public key already on system, return its aid '''
            data={'aid':str(useragentpubkeyr.dbdict[agentkey])}
            return data
        else:
            ''' Register new agent '''
            aid=uuid.uuid4()
            agentinfo=cassapi.AgentInfo(aid=aid, uid=useruidr.uid, agentname=agentname, agentkey=agentkey, version=version, state=states.AGENT['PENDING_USER_VALIDATION'])
            if cassapi.register_agent(agentinfo,session):
                print 'Devuelvo todo correcto'
                data={'aid':str(aid)}
                return data
            else:
                raise exceptions.AgentCreationException()
    else:
        raise exceptions.UserNotFoundException()

def activate_agent(aid,session):
    '''
    After an agent has been registered, the user can validate it.
    This function changes the state column of the agent to validate it
    '''
    agentinfo=cassapi.get_agentinfo(aid,session)
    if agentinfo:
        if cassapi.update_agent(agentinfo,session):
            return True
        else:
            raise excpetions.AgentUpdateException()
    else:
        raise exceptions.AgentNotFoundException()

def get_agentconfig(aid,session,dids_flag=False):
    '''
    This function returns agent configuration parameters, if dids_flag is set
    to True, it will also return datasource ids associated to the agent
    '''
    data={}
    agentinfo=cassapi.get_agentinfo(aid,{},session)
    if agentinfo:
        data['aid']=str(aid)
        data['ag_name']=agentinfo.agentname
        data['ag_state']=agentinfo.state
        data['ag_version']=agentinfo.version
        if dids_flag:
            agentdsr=cassapi.get_agentdsrelation(aid,session)
            dids=[]
            if agentdsr:
                for did in agentdsr.dids:
                    dids.append(str(did))
            data['dids']=dids
        return data
    else:
        raise exceptions.AgentNotFoundException()

