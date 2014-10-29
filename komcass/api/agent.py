#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import agent as ormagent
from komcass.model.statement import agent as stmtagent
from komcass.exception import agent as excpagent


def get_agent(session, aid):
    row=session.execute(stmtagent.S_A_MSTAGENT_B_AID,(aid,))
    if len(row)==1:
        return ormagent.Agent(**row[0])
    elif len(row)==0:
        return None
    else:
        raise excpagent.DataConsistencyException(function='get_agent',field='aid',value=aid)

def get_agents(session, uid):
    row=session.execute(stmtagent.S_A_MSTAGENT_B_UID,(uid,))
    agents=[]
    if row:
        for agent in row:
            agents.append(ormagent.Agent(**agent))
    return agents

def get_agents_aids(session, uid):
    row=session.execute(stmtagent.S_AID_MSTAGENT_B_UID,(uid,))
    aids=[]
    if row:
        for r in row:
            aids.append(r['aid'])
        return aids

def get_number_of_agents_by_uid(session, uid):
    row=session.execute(stmtagent.S_COUNT_MSTAGENT_B_UID,(uid,))
    return row[0]['count']

def new_agent(session, agent):
    if not agent:
        return False
    else:
        existing_agent=session.execute(stmtagent.S_A_MSTAGENT_B_AID,(agent.aid,))
        if existing_agent:
            return False
        else:
            session.execute(stmtagent.I_A_MSTAGENT,(agent.aid,agent.uid,agent.agentname,agent.pubkey,agent.version,agent.state,agent.creation_date))
            return True

def insert_agent(session, agent):
    if not agent:
        return False
    else:
        session.execute(stmtagent.I_A_MSTAGENT,(agent.aid,agent.uid,agent.agentname,agent.pubkey,agent.version,agent.state,agent.creation_date))
        return True

def delete_agent(session, aid):
    session.execute(stmtagent.D_A_MSTAGENT,(aid,))
    return True

