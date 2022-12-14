'''
circle.py: library for managing circle operations

This file implements the logic of different circle operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2015/03/11
author: jcazor
'''

import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.model.orm import circle as ormcircle
from komlog.komlibs.gestaccount.circle import types
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komfig import logging

def get_users_circle_config(cid):
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_GCA_GUCC_IC)
    circle=cassapicircle.get_circle(cid=cid)
    if not circle or not circle.type==types.USERS_CIRCLE:
        raise exceptions.CircleNotFoundException(error=Errors.E_GCA_GUCC_CNF)
    data={'cid':circle.cid,'uid':circle.uid,'circlename':circle.circlename,'members':[]}
    for member in circle.members:
        user=cassapiuser.get_user(uid=member)
        if user:
            data['members'].append({'username':user.username,'uid':user.uid})
    return data

def get_users_circles_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GCA_GUCSC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GCA_GUCSC_UNF)
    data=[]
    cids=cassapicircle.get_circles_cids(uid=user.uid,type=types.USERS_CIRCLE)
    for cid in cids:
        circle=get_users_circle_config(cid=cid)
        data.append(circle)
    return data

def new_users_circle(uid, circlename, members_list=None):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GCA_NUC_IU)
    if not args.is_valid_circlename(circlename):
        raise exceptions.BadParametersException(error=Errors.E_GCA_NUC_ICN)
    if members_list and not args.is_valid_list(members_list):
        raise exceptions.BadParametersException(error=Errors.E_GCA_NUC_IML)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GCA_NUC_UNF)
    if members_list:
        members=set()
        for member in members_list:
            if args.is_valid_username(member):
                user_member=cassapiuser.get_user(username=member)
                if user_member:
                    members.add(user_member.uid)
    else:
        members=None
    cid=uuid.uuid4()
    circle=ormcircle.Circle(cid=cid,uid=user.uid,type=types.USERS_CIRCLE,creation_date=timeuuid.uuid1(),circlename=circlename,members=members)
    try:
        if cassapicircle.new_circle(circle):
            return {'cid':cid,'uid':user.uid}
        else:
            raise exceptions.CircleCreationException(error=Errors.E_GCA_NUC_ICE)
    except cassexcept.KomcassException:
        cassapicircle.delete_circle(cid=cid)
        raise

def update_circle(cid, circlename):
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_GCA_UC_IC)
    if not args.is_valid_circlename(circlename):
        raise exceptions.BadParametersException(error=Errors.E_GCA_UC_ICN)
    circle=cassapicircle.get_circle(cid=cid)
    if not circle:
        raise exceptions.CircleNotFoundException(error=Errors.E_GCA_UC_CNF)
    new_circle=circle
    new_circle.circlename=circlename
    try:
        if cassapicircle.insert_circle(circle=new_circle):
            return True
        else:
            raise exceptions.CircleUpdateException(error=Errors.E_GCA_UC_ICE)
    except cassexcept.KomcassException:
        cassapicircle.insert_circle(circle=circle)
        raise

def add_user_to_circle(cid, username):
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_GCA_AUTC_IC)
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GCA_AUTC_IU)
    circle=cassapicircle.get_circle(cid=cid)
    if not circle or not circle.type==types.USERS_CIRCLE:
        raise exceptions.CircleNotFoundException(error=Errors.E_GCA_AUTC_CNF)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GCA_AUTC_UNF)
    if not user.uid in circle.members:
        try:
            if cassapicircle.add_member_to_circle(cid=cid, member=user.uid):
                return True
            else:
                raise exceptions.CircleAddMemberException(error=Errors.E_GCA_AUTC_AME)
        except cassexcept.KomcassException:
            cassapicircle.delete_member_from_circle(cid=cid, member=user.uid)
            raise
    return True

def delete_user_from_circle(cid, username):
    if not args.is_valid_uuid(cid):
        raise exceptions.BadParametersException(error=Errors.E_GCA_DUFC_IC)
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GCA_DUFC_IU)
    circle=cassapicircle.get_circle(cid=cid)
    if not circle or not circle.type==types.USERS_CIRCLE:
        raise exceptions.CircleNotFoundException(error=Errors.E_GCA_DUFC_IU)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GCA_DUFC_IU)
    if user.uid in circle.members:
        try:
            if cassapicircle.delete_member_from_circle(cid=cid, member=user.uid):
                return True
            else:
                raise exceptions.CircleDeleteMemberException(error=Errors.E_GCA_DUFC_IU)
        except cassexcept.KomcassException:
            cassapicircle.add_member_to_circle(cid=cid, member=user.uid)
            raise
    return True

