'''
agent.py: library for managing administrative agent operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
from komfig import logger
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.model.orm import agent as ormagent
from komlibs.gestaccount.agent import states
from komlibs.gestaccount import exceptions, errors
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


def decrypt(pubkey,cmsg):
    pubkey=RSA.importKey(pubkey)
    return pubkey.decrypt(cmsg)

def verify_signature(pubkey,text,b64sign):
    logger.logger.debug(pubkey)
    logger.logger.debug(text)
    rsakey=RSA.importKey(pubkey.encode('utf-8'))
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(text.encode('utf-8'))
    signature=b64decode(b64sign.encode('utf-8'))
    if signer.verify(digest,signature):
        logger.logger.debug('Verification success')
        return True
    logger.logger.debug('Verification failed')
    return False
    
def auth_agent(agentid, signature):
    if not args.is_valid_hex_uuid(agentid):
        raise exceptions.BadParametersException(error=errors.E_GAA_AUA_IA)
    if not args.is_valid_pubkey(signature):
        raise exceptions.BadParametersException(error=errors.E_GAA_AUA_IPK)
    aid=uuid.UUID(agentid)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=errors.E_GAA_AUA_ANF)
    if verify_signature(agent.pubkey, agentid, signature):
        return True
    else:
        return False

def create_agent(uid,agentname,pubkey,version):
    '''
    When the agent connects the first time, we will register it in a pending state, 
    waiting for the user validation to gain access to the system
    '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GAA_CRA_IU)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=errors.E_GAA_CRA_IA)
    if not args.is_valid_pubkey(pubkey):
        raise exceptions.BadParametersException(error=errors.E_GAA_CRA_IPK)
    if not args.is_valid_version(version):
        raise exceptions.BadParametersException(error=errors.E_GAA_CRA_IV)
    user=cassapiuser.get_user(uid=uid)
    if user:
        agents=cassapiagent.get_agents(uid=uid)
        for agent in agents:
            if agent.pubkey==pubkey:
                raise exceptions.AgentAlreadyExistsException(error=errors.E_GAA_CRA_AAE)
        ''' Register new agent '''
        aid=uuid.uuid4()
        now=timeuuid.uuid1()
        agent=ormagent.Agent(aid=aid, uid=uid, agentname=agentname, pubkey=pubkey, version=version, state=states.PENDING_USER_VALIDATION,creation_date=now)
        if cassapiagent.new_agent(agent=agent):
            return {'uid':agent.uid, 'aid':agent.aid, 'agentname':agent.agentname, 'pubkey':agent.pubkey, 'version':agent.version, 'state':agent.state}
        else:
            raise exceptions.AgentCreationException(error=errors.E_GAA_CRA_EIA)
    else:
        raise exceptions.UserNotFoundException(error=errors.E_GAA_CRA_UNF)

def activate_agent(aid):
    '''
    After an agent has been registered, the user can validate it.
    This function changes the state column of the agent to validate it
    '''
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_GAA_ACA_IA)
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        agent.state=states.ACTIVE
        if cassapiagent.insert_agent(agent=agent):
            return True
        else:
            raise exceptions.AgentUpdateException(error=errors.E_GAA_ACA_EIA)
    else:
        raise exceptions.AgentNotFoundException(error=errors.E_GAA_ACA_ANF)

def get_agent_config(aid,dids_flag=False):
    '''
    This function returns agent configuration parameters, if dids_flag is set
    to True, it will also return datasource ids associated to the agent
    '''
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_GAA_GAC_IA)
    if not args.is_valid_bool(dids_flag):
        raise exceptions.BadParametersException(error=errors.E_GAA_GAC_IF)
    data={}
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        data['aid']=agent.aid
        data['uid']=agent.uid
        data['agentname']=agent.agentname
        data['state']=agent.state
        data['version']=agent.version
        if dids_flag:
            dids=cassapidatasource.get_datasources_dids(aid=aid)
            data['dids']=[did for did in dids] if dids else []
        return data
    else:
        raise exceptions.AgentNotFoundException(error=errors.E_GAA_GAC_ANF)

def get_agents_config(uid,dids_flag=False):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GAA_GASC_IU)
    if not args.is_valid_bool(dids_flag):
        raise exceptions.BadParametersException(error=errors.E_GAA_GASC_IF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GAA_GASC_UNF)
    else:
        aids=cassapiagent.get_agents_aids(uid=uid)
        data=[]
        for aid in aids:
            try:
                agent_data=get_agent_config(aid=aid,dids_flag=dids_flag)
            except Exception:
                continue
            else:
                data.append(agent_data)
        return data
    
def update_agent_config(aid, agentname):
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_GAA_UAC_IA)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=errors.E_GAA_UAC_IAN)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=errors.E_GAA_UAC_ANF)
    agent.agentname=agentname
    if not cassapiagent.insert_agent(agent=agent):
        raise exceptions.AgentUpdateException(error=errors.E_GAA_UAC_IAE)
    else:
        return True

def delete_agent(aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_GAA_DA_IA)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=errors.E_GAA_DA_ANF)
    dids=cassapidatasource.get_datasources_dids(aid=aid)
    bids=cassapidashboard.get_dashboards_bids(uid=agent.uid)
    pids=[]
    wids=[]
    for did in dids:
        did_pids=cassapidatapoint.get_datapoints_pids(did=did)
        for pid in did_pids:
            pids.append(pid)
            dp_wid=cassapiwidget.get_widget_dp(pid=pid)
            if dp_wid:
                wids.append(dp_wid.wid)
        ds_wid=cassapiwidget.get_widget_ds(did=did)
        if ds_wid:
            wids.append(ds_wid.wid)
    cassapiagent.delete_agent(aid=aid)
    for bid in bids:
        for wid in wids:
            cassapidashboard.delete_widget_from_dashboard(wid=wid, bid=bid)
    for wid in wids:
        cassapiwidget.delete_widget(wid=wid)
    for pid in pids:
        cassapidatapoint.delete_datapoint(pid=pid)
        cassapidatapoint.delete_datapoint_stats(pid=pid)
        cassapidatapoint.delete_datapoint_data(pid=pid)
    for did in dids:
        cassapidatasource.delete_datasource(did=did)
        cassapidatasource.delete_datasource_stats(did=did)
        cassapidatasource.delete_datasource_data(did=did)
        cassapidatasource.delete_datasource_maps(did=did)
    return True

