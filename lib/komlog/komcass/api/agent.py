#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import agent as ormagent
from komlog.komcass.model.statement import agent as stmtagent
from komlog.komcass import connection, exceptions


@exceptions.ExceptionHandler
def get_agent(aid):
    row=connection.session.execute(stmtagent.S_A_MSTAGENT_B_AID,(aid,))
    if row:
        return ormagent.Agent(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def get_agents(uid):
    row=connection.session.execute(stmtagent.S_A_MSTAGENT_B_UID,(uid,))
    agents=[]
    if row:
        for agent in row:
            agents.append(ormagent.Agent(**agent))
    return agents

@exceptions.ExceptionHandler
def get_agents_aids(uid):
    row=connection.session.execute(stmtagent.S_AID_MSTAGENT_B_UID,(uid,))
    aids=[]
    if row:
        for r in row:
            aids.append(r['aid'])
    return aids

@exceptions.ExceptionHandler
def get_number_of_agents_by_uid(uid):
    row=connection.session.execute(stmtagent.S_COUNT_MSTAGENT_B_UID,(uid,))
    return row[0]['count'] if row else 0

@exceptions.ExceptionHandler
def new_agent(agent):
    if not isinstance(agent, ormagent.Agent):
        return False
    else:
        resp=connection.session.execute(stmtagent.I_A_MSTAGENT_INE,(agent.aid,agent.uid,agent.agentname,agent.pubkey,agent.version,agent.state,agent.creation_date))
        return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_agent(agent):
    if not isinstance(agent, ormagent.Agent):
        return False
    else:
        connection.session.execute(stmtagent.I_A_MSTAGENT,(agent.aid,agent.uid,agent.agentname,agent.pubkey,agent.version,agent.state,agent.creation_date))
        return True

@exceptions.ExceptionHandler
def delete_agent(aid):
    connection.session.execute(stmtagent.D_A_MSTAGENT_B_AID,(aid,))
    return True

@exceptions.ExceptionHandler
def get_agent_pubkey(uid, pubkey):
    row=connection.session.execute(stmtagent.S_A_MSTAGENTPUBKEY_B_UID_PUBKEY, (uid, pubkey))
    if row:
        return ormagent.AgentPubkey(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def get_agents_pubkeys(uid):
    data=[]
    row=connection.session.execute(stmtagent.S_A_MSTAGENTPUBKEY_B_UID, (uid, ))
    if row:
        for r in row:
            data.append(ormagent.AgentPubkey(**r))
    return data

@exceptions.ExceptionHandler
def new_agent_pubkey(obj):
    if not isinstance(obj, ormagent.AgentPubkey):
        return False
    else:
        resp=connection.session.execute(stmtagent.I_A_MSTAGENTPUBKEY_INE,(obj.uid,obj.pubkey,obj.aid,obj.state))
        return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_agent_pubkey(obj):
    if not isinstance(obj, ormagent.AgentPubkey):
        return False
    else:
        connection.session.execute(stmtagent.I_A_MSTAGENTPUBKEY,(obj.uid,obj.pubkey,obj.aid,obj.state))
        return True

@exceptions.ExceptionHandler
def delete_agent_pubkey(uid, pubkey):
    connection.session.execute(stmtagent.D_A_MSTAGENTPUBKEY,(uid,pubkey))
    return True

@exceptions.ExceptionHandler
def get_agent_challenge(aid, challenge):
    row=connection.session.execute(stmtagent.S_A_MSTAGENTCHALLENGE_B_AID_CH, (aid, challenge))
    if row:
        return ormagent.AgentChallenge(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_agent_challenge(obj):
    if not isinstance(obj, ormagent.AgentChallenge):
        return False
    else:
        connection.session.execute(stmtagent.I_A_MSTAGENTCHALLENGE,(obj.aid,obj.challenge,obj.generated,obj.validated))
        return True

@exceptions.ExceptionHandler
def delete_agent_challenge(aid, challenge):
    connection.session.execute(stmtagent.D_A_MSTAGENTCHALLENGE_B_AID_CHALLENGE,(aid,challenge))
    return True

@exceptions.ExceptionHandler
def delete_agent_challenges(aid):
    connection.session.execute(stmtagent.D_A_MSTAGENTCHALLENGE_B_AID,(aid,))
    return True

@exceptions.ExceptionHandler
def get_agent_session(sid):
    row=connection.session.execute(stmtagent.S_A_MSTAGENTSESSION_B_SID, (sid,))
    if row:
        return ormagent.AgentSession(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_agent_session(obj):
    if not isinstance(obj, ormagent.AgentSession):
        return False
    else:
        connection.session.execute(stmtagent.I_A_MSTAGENTSESSION,(obj.sid,obj.aid,obj.uid,obj.imc_address,obj.generated))
        return True

@exceptions.ExceptionHandler
def delete_agent_session(sid):
    connection.session.execute(stmtagent.D_A_MSTAGENTSESSION_B_SID,(sid,))
    return True

@exceptions.ExceptionHandler
def delete_agent_sessions(aid):
    rows=connection.session.execute(stmtagent.S_SID_MSTAGENTSESSION_B_AID,(aid,))
    if rows:
        for r in rows:
            connection.session.execute(stmtagent.D_A_MSTAGENTSESSION_B_SID,(r['sid'],))
    return True

