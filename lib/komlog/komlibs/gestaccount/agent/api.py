'''
agent.py: library for managing administrative agent operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
import os
from komlog.komfig import logging
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.model.orm import agent as ormagent
from komlog.komlibs.gestaccount.agent.states import *
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


def generate_auth_challenge(username, pubkey):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GAA_GAC_IU)
    if not args.is_valid_pubkey(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_GAA_GAC_IPK)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.ChallengeGenerationException(error=Errors.E_GAA_GAC_UNF)
    agent_pubkey=cassapiagent.get_agent_pubkey(uid=user.uid, pubkey=pubkey)
    if not agent_pubkey:
        raise exceptions.ChallengeGenerationException(error=Errors.E_GAA_GAC_ANF)
    challenge=crypto.get_random_sequence(size=64)
    ch_enc=crypto.encrypt(key=agent_pubkey.pubkey, plaintext=challenge)
    ch_hash=crypto.get_hash(message=challenge)
    if not ch_enc or not ch_hash:
        raise exceptions.ChallengeGenerationException(error=Errors.E_GAA_GAC_EGC)
    agent_challenge=ormagent.AgentChallenge(aid=agent_pubkey.aid, challenge=ch_hash, generated=timeuuid.uuid1())
    try:
        if cassapiagent.insert_agent_challenge(agent_challenge):
            return ch_enc
        else:
            raise exceptions.ChallengeGenerationException(error=Errors.E_GAA_GAC_EIDB)
    except cassexcept.KomcassException:
        cassapiagent.delete_agent_challenge(aid=agent_pubkey.aid, challenge=ch_hash)
        raise

def validate_auth_challenge(username, pubkey, challenge_hash, signature):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GAA_VAC_IU)
    if not args.is_valid_pubkey(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_GAA_VAC_IPK)
    if not args.is_valid_bytes(challenge_hash):
        raise exceptions.BadParametersException(error=Errors.E_GAA_VAC_ICH)
    if not args.is_valid_bytes(signature):
        raise exceptions.BadParametersException(error=Errors.E_GAA_VAC_ISG)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_UNF)
    agent_pubkey=cassapiagent.get_agent_pubkey(uid=user.uid, pubkey=pubkey)
    if not agent_pubkey:
        raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_ANF)
    agent_challenge=cassapiagent.get_agent_challenge(aid=agent_pubkey.aid, challenge=challenge_hash)
    if not agent_challenge:
        raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_CHNF)
    if agent_challenge.validated is not None:
        raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_CHAU)
    if timeuuid.get_unix_timestamp(agent_challenge.generated) < timeuuid.get_unix_timestamp(timeuuid.uuid1())-60:
        raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_CHEX)
    if crypto.verify_signature(key=agent_pubkey.pubkey, message=agent_challenge.challenge, signature=signature):
        agent_challenge.validated=timeuuid.uuid1()
        try:
            if cassapiagent.insert_agent_challenge(agent_challenge):
                return agent_challenge.aid
            else:
                raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_EIDB)
        except cassexcept.KomcassException:
            agent_challenge.validated=None
            cassapiagent.insert_agent_challenge(agent_challenge)
            raise
    else:
        raise exceptions.ChallengeValidationException(error=Errors.E_GAA_VAC_EVS)

def create_agent(uid,agentname,pubkey,version):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GAA_CRA_IU)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=Errors.E_GAA_CRA_IA)
    if not args.is_valid_pubkey(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_GAA_CRA_IPK)
    if not args.is_valid_version(version):
        raise exceptions.BadParametersException(error=Errors.E_GAA_CRA_IV)
    user=cassapiuser.get_user(uid=uid)
    if user:
        aid=uuid.uuid4()
        now=timeuuid.uuid1()
        agent_pubkey=ormagent.AgentPubkey(uid=uid, pubkey=pubkey, aid=aid, state=AgentStates.ACTIVE)
        agent=ormagent.Agent(aid=aid, uid=uid, agentname=agentname, pubkey=pubkey, version=version, state=AgentStates.ACTIVE,creation_date=now)
        try:
            if cassapiagent.new_agent_pubkey(obj=agent_pubkey):
                if cassapiagent.new_agent(agent=agent):
                    return {'uid':agent.uid, 'aid':agent.aid, 'agentname':agent.agentname, 'pubkey':agent.pubkey, 'version':agent.version, 'state':agent.state}
                else:
                    cassapiagent.delete_agent_pubkey(uid=uid, pubkey=pubkey)
                    raise exceptions.AgentCreationException(error=Errors.E_GAA_CRA_EIA)
            else:
                raise exceptions.AgentAlreadyExistsException(error=Errors.E_GAA_CRA_AAE)
        except cassexcept.KomcassException:
            cassapiagent.delete_agent_pubkey(uid=uid, pubkey=pubkey)
            cassapiagent.delete_agent(aid=agent.aid)
            raise
    else:
        raise exceptions.UserNotFoundException(error=Errors.E_GAA_CRA_UNF)

def activate_agent(aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_GAA_ACA_IA)
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        agent_pubkey=cassapiagent.get_agent_pubkey(uid=agent.uid, pubkey=agent.pubkey)
        if agent_pubkey:
            new_agent_pubkey=agent_pubkey
            new_agent_pubkey.state=AgentStates.ACTIVE
            new_agent=agent
            new_agent.state=AgentStates.ACTIVE
            try:
                if cassapiagent.insert_agent(agent=new_agent) and cassapiagent.insert_agent_pubkey(obj=new_agent_pubkey):
                    return True
                else:
                    raise exceptions.AgentUpdateException(error=Errors.E_GAA_ACA_EIA)
            except cassexcept.KomcassException:
                cassapiagent.insert_agent(agent=agent)
                cassapiagent.insert_agent_pubkey(agent_pubkey)
                raise
        else:
            raise exceptions.AgentNotFoundException(error=Errors.E_GAA_ACA_APKNF)
    else:
        raise exceptions.AgentNotFoundException(error=Errors.E_GAA_ACA_ANF)

def suspend_agent(aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_GAA_SPA_IA)
    agent=cassapiagent.get_agent(aid=aid)
    if agent:
        agent_pubkey=cassapiagent.get_agent_pubkey(uid=agent.uid, pubkey=agent.pubkey)
        if agent_pubkey:
            new_agent=agent
            new_agent.state=AgentStates.SUSPENDED
            new_agent_pubkey=agent_pubkey
            new_agent_pubkey.state=AgentStates.SUSPENDED
            try:
                if cassapiagent.insert_agent(agent=new_agent) and cassapiagent.insert_agent_pubkey(obj=new_agent_pubkey):
                    return True
                else:
                    raise exceptions.AgentUpdateException(error=Errors.E_GAA_SPA_EIA)
            except cassexcept.KomcassException:
                cassapiagent.insert_agent(agent=agent)
                cassapiagent.insert_agent_pubkey(agent_pubkey)
                raise
        else:
            raise exceptions.AgentNotFoundException(error=Errors.E_GAA_SPA_APKNF)
    else:
        raise exceptions.AgentNotFoundException(error=Errors.E_GAA_SPA_ANF)

def get_agent_config(aid,dids_flag=False):
    '''
    This function returns agent configuration parameters, if dids_flag is set
    to True, it will also return datasource ids associated to the agent
    '''
    if not args.is_valid_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_GAA_GACFG_IA)
    if not args.is_valid_bool(dids_flag):
        raise exceptions.BadParametersException(error=Errors.E_GAA_GACFG_IF)
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
        raise exceptions.AgentNotFoundException(error=Errors.E_GAA_GACFG_ANF)

def get_agents_config(uid,dids_flag=False):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GAA_GASC_IU)
    if not args.is_valid_bool(dids_flag):
        raise exceptions.BadParametersException(error=Errors.E_GAA_GASC_IF)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GAA_GASC_UNF)
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
        raise exceptions.BadParametersException(error=Errors.E_GAA_UAC_IA)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=Errors.E_GAA_UAC_IAN)
    agent=cassapiagent.get_agent(aid=aid)
    if not agent:
        raise exceptions.AgentNotFoundException(error=Errors.E_GAA_UAC_ANF)
    new_agent=agent
    new_agent.agentname=agentname
    try:
        if not cassapiagent.insert_agent(agent=new_agent):
            raise exceptions.AgentUpdateException(error=Errors.E_GAA_UAC_IAE)
        else:
            return True
    except cassexcept.KomcassException:
        cassapiagent.insert_agent(agent)
        raise

