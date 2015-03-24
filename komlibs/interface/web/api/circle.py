'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.circle import api as circleapi
from komlibs.interface.web import status, exceptions, errors
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_users_circles_config_request(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_GUCSCR_IU)
    uid=userapi.get_uid(username=username)
    data=circleapi.get_users_circles_config(uid=uid)
    response_data=[]
    for circle in data:
        reg={}
        reg['cid']=circle['cid'].hex
        reg['circlename']=circle['circlename']
        reg['members']=[]
        for member in circle['members']:
            reg['members'].append({'username':member['username'],'uid':member['uid'].hex})
        response_data.append(reg)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=response_data)

@exceptions.ExceptionHandler
def get_users_circle_config_request(username, cid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_GUCCR_IU)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_IWACI_GUCCR_IC)
    cid=uuid.UUID(cid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.GET_CIRCLE_CONFIG,uid=uid,cid=cid)
    data=circleapi.get_users_circle_config(cid=cid)
    circle={'cid':cid.hex}
    circle['circlename']=data['circlename']
    circle['members']=[]
    for member in data['members']:
        circle['members'].append({'username':member['username'],'uid':member['uid'].hex})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=circle)

@exceptions.ExceptionHandler
def delete_circle_request(username, cid):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_DCR_IU)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_IWACI_DCR_IC)
    cid=uuid.UUID(cid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_CIRCLE,uid=uid,cid=cid)
    circleapi.delete_circle(cid=cid)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_users_circle_request(username, circlename, members_list=None):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_NUCR_IU)
    if not args.is_valid_circlename(circlename):
        raise exceptions.BadParametersException(error=errors.E_IWACI_NUCR_ICN)
    if members_list and not args.is_valid_list(members_list):
        raise exceptions.BadParametersException(error=errors.E_IWACI_NUCR_IML)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.NEW_CIRCLE, uid=uid)
    circle=circleapi.new_users_circle(uid=uid,circlename=circlename,members_list=members_list)
    if circle:
        operation=weboperations.NewCircleOperation(uid=circle['uid'], cid=circle['cid'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.MembershipAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'cid':circle['cid'].hex})
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

@exceptions.ExceptionHandler
def update_circle_request(username, cid, data):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_UCR_IU)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_IWACI_UCR_IC)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=errors.E_IWACI_UCR_ID)
    if not 'circlename' in data or not args.is_valid_circlename(data['circlename']):
        raise exceptions.BadParametersException(error=errors.E_IWACI_UCR_ICN)
    cid=uuid.UUID(cid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.UPDATE_CIRCLE_CONFIG, uid=uid, cid=cid)
    circleapi.update_circle(cid=cid, circlename=data['circlename'])
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def add_user_to_circle_request(username, cid, member):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_AUTCR_IU)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_IWACI_AUTCR_IC)
    if not args.is_valid_username(member):
        raise exceptions.BadParametersException(error=errors.E_IWACI_AUTCR_IM)
    cid=uuid.UUID(cid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.ADD_MEMBER_TO_CIRCLE, uid=uid, cid=cid)
    if circleapi.add_user_to_circle(cid=cid, username=member):
        operation=weboperations.UpdateCircleMembersOperation(uid=uid, cid=cid)
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.MembershipAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

@exceptions.ExceptionHandler
def delete_user_from_circle_request(username, cid, member):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWACI_DUFCR_IU)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=errors.E_IWACI_DUFCR_IC)
    if not args.is_valid_username(member):
        raise exceptions.BadParametersException(error=errors.E_IWACI_DUFCR_IM)
    cid=uuid.UUID(cid)
    uid=userapi.get_uid(username=username)
    authorization.authorize_request(request=requests.DELETE_MEMBER_FROM_CIRCLE, uid=uid, cid=cid)
    if circleapi.delete_user_from_circle(cid=cid, username=member):
        operation=weboperations.UpdateCircleMembersOperation(uid=uid, cid=cid)
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        message=messages.MembershipAuthorizationUpdateMessage(operation=auth_op, params=params)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)

