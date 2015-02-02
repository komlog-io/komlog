#coding: utf-8
'''

This file defines the logic associated with web interface requests

'''

from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def new_user_request(username, password, email):
    if args.is_valid_username(username) and args.is_valid_password(password) and args.is_valid_email(email):
        #ensure we always create new users and emails in lowercase
        username=username.lower()
        email=email.lower()
        user=userapi.create_user(username, password, email)
        if user:
            message=messages.NewUserNotificationMessage(email=user['email'], code=user['signup_code'])
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'uid':user['uid'].hex})
    else:
        raise exceptions.BadParametersException()


@exceptions.ExceptionHandler
def confirm_user_request(email, code):
    if args.is_valid_email(email) and args.is_valid_code(code):
        if userapi.confirm_user(email, code):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_user_config_request(username):
    if args.is_valid_username(username):
        user=userapi.get_user_config(username=username)
        agents=agentapi.get_agents_config(username=username, dids_flag=True)
        agents_data=[]
        for agent in agents:
            dids=[]
            for did in agent['dids']:
                dids.append(did.hex)
            agents_data.append({'aid':agent['aid'].hex,
                               'agentname':agent['agentname'],
                               'state':agent['state'],
                               'version':agent['version'],
                               'dids':dids})
        data={'username':user['username'],
              'uid':user['uid'].hex,
              'email':user['email'],
              'state':user['state'],
              'agents':agents_data}
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_user_config_request(username, data):
    if args.is_valid_username(username) and args.is_valid_dict(data):
        #we dont authorize here because a user can always update herself
        request_params={}
        if 'email' in data:
            if not args.is_valid_email(data['email']):
                raise exceptions.BadParametersException()
            request_params['new_email']=data['email']
        if 'new_password' in data:
            if not args.is_valid_password(data['new_password']):
                raise exceptions.BadParametersException()
            request_params['new_password']=data['new_password']
        if 'old_password' in data:
            if not args.is_valid_password(data['old_password']):
                raise exceptions.BadParametersException()
            request_params['old_password']=data['old_password']
        if userapi.update_user_config(username=username, **request_params):
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_user_request(username):
    if args.is_valid_username(username):
        message=messages.DeleteUserMessage(username=username)
        msgapi.send_message(message=message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)
    else:
        raise exceptions.BadParametersException()

