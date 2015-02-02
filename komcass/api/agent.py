#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import agent as ormagent
from komcass.model.statement import agent as stmtagent
from komcass.exception import agent as excpagent
from komcass import connection


def get_agent(aid):
    row=connection.session.execute(stmtagent.S_A_MSTAGENT_B_AID,(aid,))
    if not row:
        return None
    elif len(row)==1:
        return ormagent.Agent(**row[0])
    else:
        raise excpagent.DataConsistencyException(function='get_agent',field='aid',value=aid)

def get_agents(uid):
    row=connection.session.execute(stmtagent.S_A_MSTAGENT_B_UID,(uid,))
    agents=[]
    if row:
        for agent in row:
            agents.append(ormagent.Agent(**agent))
    return agents

def get_agents_aids(uid):
    row=connection.session.execute(stmtagent.S_AID_MSTAGENT_B_UID,(uid,))
    aids=[]
    if row:
        for r in row:
            aids.append(r['aid'])
    return aids

def get_number_of_agents_by_uid(uid):
    row=connection.session.execute(stmtagent.S_COUNT_MSTAGENT_B_UID,(uid,))
    return row[0]['count'] if row else 0

def new_agent(agent):
    if not isinstance(agent, ormagent.Agent):
        return False
    else:
        existing_agent=connection.session.execute(stmtagent.S_A_MSTAGENT_B_AID,(agent.aid,))
        if existing_agent:
            return False
        else:
            connection.session.execute(stmtagent.I_A_MSTAGENT,(agent.aid,agent.uid,agent.agentname,agent.pubkey,agent.version,agent.state,agent.creation_date))
            return True

def insert_agent(agent):
    if not isinstance(agent, ormagent.Agent):
        return False
    else:
        connection.session.execute(stmtagent.I_A_MSTAGENT,(agent.aid,agent.uid,agent.agentname,agent.pubkey,agent.version,agent.state,agent.creation_date))
        return True

def delete_agent(aid):
    connection.session.execute(stmtagent.D_A_MSTAGENT_B_AID,(aid,))
    return True

