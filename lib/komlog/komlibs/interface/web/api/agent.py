import uuid
from base64 import b64decode
from komlog.komcass import exceptions as cassexcept
from komlog.komfig import logging
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.auth.passport import UserPassport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response, operation
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def new_agent_request(passport, agentname, pubkey, version):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_NAGR_IPSP)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_NAGR_IAN)
    if not args.is_valid_string(pubkey):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_NAGR_IPK)
    if not args.is_valid_version(version):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_NAGR_IV)
    authorization.authorize_request(request=Requests.NEW_AGENT,passport=passport)
    pubkey=b64decode(pubkey.encode('utf-8'))
    agent=agentapi.create_agent(uid=passport.uid, agentname=agentname, pubkey=pubkey, version=version)
    if agent:
        webop=operation.NewAgentOperation(uid=passport.uid,aid=agent['aid'])
        authop=webop.get_auth_operation()
        params=webop.get_params()
        try:
            if authupdate.update_resources(operation=authop, params=params):
                resp=response.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'aid':agent['aid'].hex})
                resp.add_imc_message(messages.UpdateQuotesMessage(operation=authop, params=params))
                resp.add_imc_message(messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_AGENT, parameters={'aid':agent['aid'].hex}))
                return resp
            else:
                deleteapi.delete_agent(aid=agent['aid'])
                return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWAA_NAGR_AUTHERR)
        except cassexcept.KomcassException:
            deleteapi.delete_agent(aid=agent['aid'])
            raise

@exceptions.ExceptionHandler
def get_agents_config_request(passport, dids_flag=True):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_GAGSCR_IPSP)
    authorization.authorize_request(request=Requests.GET_AGENTS_CONFIG, passport=passport)
    data=agentapi.get_agents_config(uid=passport.uid, dids_flag=dids_flag)
    response_data=[]
    for reg in data:
        agent_config={}
        agent_config['aid']=reg['aid'].hex
        agent_config['agentname']=reg['agentname']
        agent_config['state']=reg['state']
        agent_config['version']=reg['version']
        agent_config['pubkey']=reg['pubkey'].decode('utf-8')
        if 'dids' in reg:
            agent_config['dids']=[]
            for did in reg['dids']:
                agent_config['dids'].append(did.hex)
        response_data.append(agent_config)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_agent_config_request(passport, aid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_GAGCR_IPSP)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_GAGCR_IA)
    aid=uuid.UUID(aid)
    authorization.authorize_request(request=Requests.GET_AGENT_CONFIG,passport=passport,aid=aid)
    data=agentapi.get_agent_config(aid=aid,dids_flag=True)
    response_data={}
    response_data['aid']=data['aid'].hex
    response_data['agentname']=data['agentname']
    response_data['state']=data['state']
    response_data['version']=data['version']
    response_data['pubkey']=data['pubkey'].decode('utf-8')
    if 'dids' in data:
        response_data['dids']=[]
        for did in data['dids']:
            response_data['dids'].append(did.hex)
    return response.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def update_agent_config_request(passport, aid, data):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_UAGCR_IPSP)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_UAGCR_IA)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_UAGCR_ID)
    aid=uuid.UUID(aid)
    if not 'agentname' in data or not args.is_valid_agentname(data['agentname']):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_UAGCR_IAN)
    authorization.authorize_request(request=Requests.UPDATE_AGENT_CONFIG,passport=passport, aid=aid)
    if agentapi.update_agent_config(aid=aid, agentname=data['agentname']):
        return response.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_agent_request(passport, aid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_DAGR_IPSP)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_DAGR_IA)
    aid=uuid.UUID(aid)
    authorization.authorize_request(request=Requests.DELETE_AGENT, passport=passport, aid=aid)
    deleteapi.delete_agent(aid=aid)
    resp = response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    return resp

@exceptions.ExceptionHandler
def suspend_agent_request(passport, aid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_SAGR_IPSP)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_SAGR_IAID)
    aid=uuid.UUID(aid)
    authorization.authorize_request(request=Requests.UPDATE_AGENT_CONFIG, passport=passport, aid=aid)
    agentapi.suspend_agent(aid=aid)
    resp = response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    return resp

@exceptions.ExceptionHandler
def activate_agent_request(passport, aid):
    if not isinstance(passport, UserPassport):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_AAGR_IPSP)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=Errors.E_IWAA_AAGR_IAID)
    aid=uuid.UUID(aid)
    authorization.authorize_request(request=Requests.UPDATE_AGENT_CONFIG, passport=passport, aid=aid)
    agentapi.activate_agent(aid=aid)
    resp = response.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    return resp

