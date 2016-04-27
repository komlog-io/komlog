'''

This file defines the logic associated with web interface operations

'''

import uuid
from komlog.komfig import logging
from komlog.komimc import api as msgapi
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth import update as authupdate
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.model.requests import Requests
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web.operations import weboperations
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_users_circles_config_request(passport):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_GUCSCR_IPSP)
    authorization.authorize_request(request=Requests.GET_CIRCLES_CONFIG,passport=passport)
    data=circleapi.get_users_circles_config(uid=passport.uid)
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
def get_users_circle_config_request(passport, cid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_GUCCR_IPSP)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_GUCCR_IC)
    cid=uuid.UUID(cid)
    authorization.authorize_request(request=Requests.GET_CIRCLE_CONFIG,passport=passport,cid=cid)
    data=circleapi.get_users_circle_config(cid=cid)
    circle={'cid':cid.hex}
    circle['circlename']=data['circlename']
    circle['members']=[]
    for member in data['members']:
        circle['members'].append({'username':member['username'],'uid':member['uid'].hex})
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=circle)

@exceptions.ExceptionHandler
def delete_circle_request(passport, cid):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_DCR_IPSP)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_DCR_IC)
    cid=uuid.UUID(cid)
    authorization.authorize_request(request=Requests.DELETE_CIRCLE,passport=passport,cid=cid)
    deleteapi.delete_circle(cid=cid)
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def new_users_circle_request(passport, circlename, members_list=None):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_NUCR_IPSP)
    if not args.is_valid_circlename(circlename):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_NUCR_ICN)
    if members_list and not args.is_valid_list(members_list):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_NUCR_IML)
    authorization.authorize_request(request=Requests.NEW_CIRCLE,passport=passport)
    circle=circleapi.new_users_circle(uid=passport.uid,circlename=circlename,members_list=members_list)
    if circle:
        operation=weboperations.NewCircleOperation(uid=circle['uid'], cid=circle['cid'])
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        if authupdate.update_resources(operation=auth_op, params=params):
            message=messages.UpdateQuotesMessage(operation=auth_op.value, params=params)
            msgapi.send_message(message)
            message=messages.UserEventMessage(uid=passport.uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_CIRCLE, parameters={'cid':circle['cid'].hex})
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK,data={'cid':circle['cid'].hex})
        else:
            deleteapi.delete_circle(cid=circle['cid'])
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=Errors.E_IWACI_NUCR_AUTHERR.value)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=Errors.E_IWACI_NUCR_CCE.value)

@exceptions.ExceptionHandler
def update_circle_request(passport, cid, data):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_UCR_IPSP)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_UCR_IC)
    if not args.is_valid_dict(data):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_UCR_ID)
    if not 'circlename' in data or not args.is_valid_circlename(data['circlename']):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_UCR_ICN)
    cid=uuid.UUID(cid)
    authorization.authorize_request(request=Requests.UPDATE_CIRCLE_CONFIG,passport=passport,cid=cid)
    circleapi.update_circle(cid=cid, circlename=data['circlename'])
    return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)

@exceptions.ExceptionHandler
def add_user_to_circle_request(passport, cid, member):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_AUTCR_IPSP)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_AUTCR_IC)
    if not args.is_valid_username(member):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_AUTCR_IM)
    cid=uuid.UUID(cid)
    authorization.authorize_request(request=Requests.ADD_MEMBER_TO_CIRCLE,passport=passport,cid=cid)
    if circleapi.add_user_to_circle(cid=cid, username=member):
        operation=weboperations.UpdateCircleMembersOperation(uid=passport.uid, cid=cid)
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op.value, params=params)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=Errors.UNKNOWN.value)

@exceptions.ExceptionHandler
def delete_user_from_circle_request(passport, cid, member):
    if not isinstance(passport, Passport):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_DUFCR_IPSP)
    if not args.is_valid_hex_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_DUFCR_IC)
    if not args.is_valid_username(member):
        raise exceptions.BadParametersException(error=Errors.E_IWACI_DUFCR_IM)
    cid=uuid.UUID(cid)
    authorization.authorize_request(request=Requests.DELETE_MEMBER_FROM_CIRCLE,passport=passport,cid=cid)
    if circleapi.delete_user_from_circle(cid=cid, username=member):
        operation=weboperations.UpdateCircleMembersOperation(uid=passport.uid, cid=cid)
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op.value, params=params)
        msgapi.send_message(message)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=Errors.UNKNOWN.value)

