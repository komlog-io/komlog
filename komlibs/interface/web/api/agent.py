import uuid
from komfig import logger
from komlibs.auth import authorization
from komimc import messages
from komimc import api as msgapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def new_agent_request(username, agentname, pubkey, version):
    if args.is_valid_username(username) and args.is_valid_agentname(agentname) and args.is_valid_pubkey(pubkey) and args.is_valid_version(version):
        authorization.authorize_request(request='NewAgentRequest',username=username)
        agent=agentapi.create_agent(username, agentname, pubkey, version)
        if agent:
            operation=weboperations.NewAgentOperation(uid=agent['uid'],aid=agent['aid'])
            message=messages.UpdateQuotesMessage(operation=operation)
            msgapi.send_message(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'aid':agent['aid'].hex})
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_agents_config_request(username):
    if args.is_valid_username(username):
        data=agentapi.get_agents_config(username=username, dids_flag=True)
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
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_agent_config_request(username, aid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(aid):
        aid=uuid.UUID(aid)
        authorization.authorize_request(request='GetAgentConfigRequest',username=username,aid=aid)
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
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_agent_config_request(username, aid, data):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(aid) and args.is_valid_dict(data):
        aid=uuid.UUID(aid)
        if not 'agentname' in data or not args.is_valid_agentname(data['agentname']):
            raise exceptions.BadParametersException()
        authorization.authorize_request('AgentUpdateConfigurationRequest',username, aid=aid)
        if agentapi.update_agent_config(username=username, aid=aid, agentname=data['agentname']):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

