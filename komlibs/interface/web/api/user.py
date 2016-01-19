#coding: utf-8
'''

This file defines the logic associated with web interface requests

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount import errors as gesterrors
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args


@exceptions.ExceptionHandler
def new_user_request(username, password, email, invitation=None, require_invitation=False):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAU_NUSR_IU)
    if not args.is_valid_password(password): 
        raise exceptions.BadParametersException(error=errors.E_IWAU_NUSR_IP)
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_IWAU_NUSR_IE)
    if require_invitation and not args.is_valid_hex_uuid(invitation):
        raise exceptions.BadParametersException(error=errors.E_IWAU_NUSR_IINV)
    #ensure we always create new users and emails in lowercase
    username=username.lower()
    email=email.lower()
    if require_invitation:
        inv_id=uuid.UUID(invitation)
        try:
            user=userapi.create_user_by_invitation(username, password, email, inv_id=inv_id)
        except gestexcept.InvitationNotFoundException:
            status_c=status.WEB_STATUS_BAD_PARAMETERS
            data={'message':'Invalid Invitation Code'}
            error=errors.E_IWAU_NUSR_INVNF
            return webmodel.WebInterfaceResponse(status=status_c, data=data, error=error)
        except gestexcept.InvitationProcessException as e:
            if e.error == gesterrors.E_GUA_SIP_INVAU:
                status_c=status.WEB_STATUS_BAD_PARAMETERS
                data={'message':'Invitation Already Used'}
                error=errors.E_IWAU_NUSR_INVAU
            else:
                status_c=status.WEB_STATUS_INTERNAL_ERROR
                data={'message':'Error code '+str(e.error)}
                error=e.error
            return webmodel.WebInterfaceResponse(status=status_c, data=data, error=error)
        except gestexcept.UserAlreadyExistsException as e:
            status_c=status.WEB_STATUS_BAD_PARAMETERS
            data={'message':'User already exists'}
            if e.error==gesterrors.E_GUA_CRU_UAEU:
                error=errors.E_IWAU_NUSR_UAEU
            elif e.error==gesterrors.E_GUA_CRU_UAEE:
                error=errors.E_IWAU_NUSR_UAEE
            else:
                error=e.error
            return webmodel.WebInterfaceResponse(status=status_c, data=data, error=error)
    else:
        user=userapi.create_user(username, password, email)
    if user:
        message=messages.NewUserNotificationMessage(email=user['email'], code=user['signup_code'])
        msgapi.send_message(message)
        message=messages.UserEventMessage(uid=user['uid'],event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_USER)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'uid':user['uid'].hex,'username':username})

@exceptions.ExceptionHandler
def confirm_user_request(email, code):
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_IWAU_CUSR_IE)
    if not args.is_valid_code(code):
        raise exceptions.BadParametersException(error=errors.E_IWAU_CUSR_IC)
    if userapi.confirm_user(email, code):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def get_user_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAU_GUSCR_IU)
    user=userapi.get_user_config(username=username)
    data={'username':user['username'],
          'uid':user['uid'].hex,
          'email':user['email'],
          'state':user['state']
         }
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)

@exceptions.ExceptionHandler
def update_user_config_request(username, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAU_UUSCR_IU)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWAU_UUSCR_ID)
    #we dont authorize here because a user can always update herself
    request_params={}
    if 'email' in data:
        if not args.is_valid_email(data['email']):
            raise exceptions.BadParametersException(error=errors.E_IWAU_UUSCR_IE)
        request_params['new_email']=data['email']
    if 'new_password' in data:
        if not args.is_valid_password(data['new_password']):
            raise exceptions.BadParametersException(error=errors.E_IWAU_UUSCR_INP)
        request_params['new_password']=data['new_password']
    if 'old_password' in data:
        if not args.is_valid_password(data['old_password']):
            raise exceptions.BadParametersException(error=errors.E_IWAU_UUSCR_IOP)
        request_params['old_password']=data['old_password']
    if userapi.update_user_config(username=username, **request_params):
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def delete_user_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWAU_DUSR_IU)
    message=messages.DeleteUserMessage(username=username)
    msgapi.send_message(msg=message)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_RECEIVED)

@exceptions.ExceptionHandler
def register_invitation_request(email):
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_IWAU_RIR_IEMAIL)
    if userapi.register_invitation_request(email=email):
        data={'email':email}
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

@exceptions.ExceptionHandler
def check_invitation_request(invitation):
    if not args.is_valid_hex_uuid(invitation):
        raise exceptions.BadParametersException(error=errors.E_IWAU_CIR_IINV)
    try:
        inv_id=uuid.UUID(invitation)
        userapi.check_unused_invitation(inv_id=inv_id)
    except gestexcept.InvitationNotFoundException as e:
        status_c=status.WEB_STATUS_NOT_FOUND
        data={'message':'Invitation not found'}
        error=errors.E_IWAU_CIR_INVNF
        return webmodel.WebInterfaceResponse(status=status_c, data=data, error=error)
    except gestexcept.InvitationProcessException as e:
        if e.error == gesterrors.E_GUA_CUI_INVAU:
            status_c=status.WEB_STATUS_BAD_PARAMETERS
            data={'message':'Invitation Already Used'}
            error=errors.E_IWAU_CIR_INVAU
        else:
            status_c=status.WEB_STATUS_INTERNAL_ERROR
            data={'message':'Error code '+str(e.error)}
            error=e.error
        return webmodel.WebInterfaceResponse(status=status_c, data=data, error=error)
    else:
        data={'invitation':invitation}
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=data)

@exceptions.ExceptionHandler
def send_invitation_request(email=None, num=1):
    if email is not None and not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_IWAU_SIR_IEMAIL)
    if not args.is_valid_int(num):
        raise exceptions.BadParametersException(error=errors.E_IWAU_SIR_INUM)
    invitations=userapi.generate_user_invitations(email=email, num=num)
    sent=[]
    for invitation in invitations:
        message=messages.NewInvitationMailMessage(email=invitation['email'], inv_id=invitation['inv_id'])
        msgapi.send_message(message)
        sent.append((invitation['email'],invitation['inv_id'].hex))
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data=sent)

