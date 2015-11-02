import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def new_agent_request(username, agentname, pubkey, version):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAA_NAGR_IU)
    if not args.is_valid_agentname(agentname):
        raise exceptions.BadParametersException(error=errors.E_IWAA_NAGR_IAN)
    if not args.is_valid_pubkey(pubkey):
        raise exceptions.BadParametersException(error=errors.E_IWAA_NAGR_IPK)
    if not args.is_valid_version(version):
        raise exceptions.BadParametersException(error=errors.E_IWAA_NAGR_IV)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_AGENT,uid=uid)
    agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
    if agent:
        operation=weboperations.NewAgentOperation(uid=uid,aid=agent['aid'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.UserEventMessage(uid=uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_AGENT, parameters={'aid':agent['aid'].hex})
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'aid':agent['aid'].hex})

@exceptions.ExceptionHandler
def get_agents_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAA_GAGSCR_IU)
    uid=userapi.get_uid(username=username)
    data=agentapi.get_agents_config(uid=uid, dids_flag=True)
    response_data=[]
    for reg in data:
        agent_config={}
        agent_config['aid']=reg['aid'].hex
        agent_config['agentname']=reg['agentname']
        agent_config['state']=reg['state']
        agent_config['version']=reg['version']
        if 'dids' in reg:
            agent_config['dids']=[]
            for did in reg['dids']:
                agent_config['dids'].append(did.hex)
        response_data.append(agent_config)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_agent_config_request(username, aid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAA_GAGCR_IU)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_IWAA_GAGCR_IA)
    aid=uuid.UUID(aid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_AGENT_CONFIG,uid=uid,aid=aid)
    data=agentapi.get_agent_config(aid=aid,dids_flag=True)
    response_data={}
    response_data['aid']=data['aid'].hex
    response_data['agentname']=data['agentname']
    response_data['state']=data['state']
    response_data['version']=data['version']
    if 'dids' in data:
        response_data['dids']=[]
        for did in data['dids']:
            response_data['dids'].append(did.hex)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def update_agent_config_request(username, aid, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAA_UAGCR_IU)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_IWAA_UAGCR_IA)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAA_UAGCR_ID)
    aid=uuid.UUID(aid)
    if not 'agentname' in data or not args.is_valid_agentname(data['agentname']):
        raise exceptions.BadParametersException(error=errors.E_IWAA_UAGCR_IAN)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.UPDATE_AGENT_CONFIG,uid=uid, aid=aid)
    if agentapi.update_agent_config(aid=aid, agentname=data['agentname']):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_agent_request(username, aid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAA_DAGR_IU)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_IWAA_DAGR_IA)
    aid=uuid.UUID(aid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_AGENT,uid=uid,aid=aid)
    message=messages.DeleteAgentMessage(aid=aid)
    msgapi.send_message(msg=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

