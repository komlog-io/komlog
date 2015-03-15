'''

This file defines the logic associated with web interface operations

'''

import uuid
from komfig import logger
from komimc import api as msgapi
from komlibs.auth import authorization, requests
from komlibs.gestaccount.circle import api as circleapi
from komlibs.interface.web import status, exceptions
from komlibs.interface.web.model import webmodel
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid


@exceptions.ExceptionHandler
def get_users_circles_config_request(username):
    if args.is_valid_username(username):
        data=circleapi.get_users_circles_config(username=username)
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
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def get_users_circle_config_request(username, cid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(cid):
        cid=uuid.UUID(cid)
        authorization.authorize_request(request=requests.GET_CIRCLE_CONFIG,username=username,cid=cid)
        data=circleapi.get_users_circle_config(cid=cid)
        circle={'cid':cid.hex}
        circle['circlename']=data['circlename']
        circle['members']=[]
        for member in data['members']:
            circle['members'].append({'username':member['username'],'uid':member['uid'].hex})
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK, data=circle)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_circle_request(username, cid):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(cid):
        cid=uuid.UUID(cid)
        authorization.authorize_request(request=requests.DELETE_CIRCLE,username=username,cid=cid)
        circleapi.delete_circle(cid=cid)
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def new_users_circle_request(username, circlename, members_list=None):
    if args.is_valid_username(username) and args.is_valid_circlename(circlename):
        if members_list and not args.is_valid_list(members_list):
            raise exceptions.BadParametersException()
        authorization.authorize_request(request=requests.NEW_CIRCLE, username=username)
        circle=circleapi.new_users_circle(username=username,circlename=circlename,members_list=members_list)
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
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def update_circle_request(username, cid, data):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(cid) and args.is_valid_dict(data):
        if not 'circlename' in data or not args.is_valid_circlename(data['circlename']):
            raise exceptions.BadParametersException()
        cid=uuid.UUID(cid)
        authorization.authorize_request(request=requests.UPDATE_CIRCLE_CONFIG, username=username, cid=cid)
        circleapi.update_circle(cid=cid, circlename=data['circlename'])
        return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def add_user_to_circle_request(username, cid, member):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(cid) and args.is_valid_username(member):
        cid=uuid.UUID(cid)
        authorization.authorize_request(request=requests.ADD_MEMBER_TO_CIRCLE,username=username, cid=cid)
        if circleapi.add_user_to_circle(cid=cid, username=member):
            operation=weboperations.UpdateCircleMembersOperation(cid=cid)
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            #ESTE MENSAJE SE ENVIARA CUANDO OBTENGAMOS EL UID EN LAS FUNCIONES DE INTERFAZ
            #message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            #msgapi.send_message(message)
            message=messages.MembershipAuthorizationUpdateMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
        else:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
    else:
        raise exceptions.BadParametersException()

@exceptions.ExceptionHandler
def delete_user_from_circle_request(username, cid, member):
    if args.is_valid_username(username) and args.is_valid_hex_uuid(cid) and args.is_valid_username(member):
        cid=uuid.UUID(cid)
        authorization.authorize_request(request=requests.DELETE_MEMBER_FROM_CIRCLE,username=username, cid=cid)
        if circleapi.delete_user_from_circle(cid=cid, username=member):
            operation=weboperations.UpdateCircleMembersOperation(cid=cid)
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            #ESTE MENSAJE SE ENVIARA CUANDO OBTENGAMOS EL UID EN LAS FUNCIONES DE INTERFAZ
            #message=messages.UpdateQuotesMessage(operation=auth_op, params=params)
            #msgapi.send_message(message)
            message=messages.MembershipAuthorizationUpdateMessage(operation=auth_op, params=params)
            msgapi.send_message(message)
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_OK)
        else:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
    else:
        raise exceptions.BadParametersException()

