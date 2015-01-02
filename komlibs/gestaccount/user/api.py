'''
user.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid,crypt
from datetime import datetime
from komcass.api import user as cassapiuser
from komcass.model.orm import user as ormuser
from komlibs.gestaccount.user import states, segments
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments


def get_hpassword(uid,password):
    if not arguments.is_valid_uuid(uid):
        raise exceptions.BadParametersException()
    if not arguments.is_valid_password(password):
        raise exceptions.BadParametersException()
    salt='$6$'+str(uid).split('-')[1]+'$'
    try:
        hpassword=crypt.crypt(password,salt)
    except TypeError:
        return None
    return hpassword

def auth_user(username, password):
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    if not arguments.is_valid_password(password):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    hpassword=get_hpassword(user.uid,password)
    if not hpassword:
        raise exceptions.BadParametersException()
    if user.password==get_hpassword(user.uid, password):
        return True
    else:
        return False

def create_user(username, password, email):
    '''This function creates a new user in the database'''
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    if not arguments.is_valid_password(password):
        raise exceptions.BadParametersException()
    if not arguments.is_valid_email(email):
        raise exceptions.BadParametersException()
    uid=uuid.uuid4()
    hpassword=get_hpassword(uid,password)
    if not hpassword:
        raise exceptions.BadParametersException()
    now=datetime.utcnow()
    segment=segments.FREE
    user=ormuser.User(username=username, uid=uid, password=hpassword, email=email, segment=segments.FREE, creation_date=now, state=states.PREACTIVE)
    if cassapiuser.new_user(user=user):
        return user
    else:
        return None

def confirm_user(email, code):
    '''This function confirm the user'''
    if not arguments.is_valid_email(email):
        raise exceptions.BadParametersException()
    if not arguments.is_valid_code(code):
        raise exceptions.BadParametersException()
    signup_info=cassapiuser.get_signup_info(signup_code=code)
    if not signup_info:
        raise exceptions.UserNotFoundException()
    if not signup_info.email==email:
        raise exceptions.UserNotFoundException()
    if signup_info.utilization_date:
        raise exceptions.UserConfirmationException()
    user=cassapiuser.get_user(username=signup_info.username)
    if not user:
        raise exceptions.UserNotFoundException()
    signup_info.utilization_date=datetime.utcnow()
    user.state=states.ACTIVE
    if not cassapiuser.insert_user(user=user):
        raise exceptions.UserConfirmationException()
    cassapiuser.insert_signup_info(signup_info=signup_info)
    return True
    
def update_user_profile(username, params):
    ''' This function is used to update user configuration parameters.
    Parameters supported:
        - password
        - email
    '''
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    if not arguments.is_valid_dict(params):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    user_bck=user
    if not user:
        raise exceptions.UserNotFoundException()
    if 'email' not in params and 'new_password' not in params:
        raise exceptions.BadParametersException()
    if bool('old_password' in params) ^ bool('new_password' in params):
        raise exceptions.BadParametersException()
    if 'new_password' in params and 'old_password' in params:
        if not arguments.is_valid_password(params['new_password']):
            raise exceptions.BadParametersException()
        if not arguments.is_valid_password(params['old_password']):
            raise exceptions.BadParametersException()
        if not user.password==get_hpassword(user.uid,params['old_password']):
            raise exceptions.BadParametersException()
        if params['new_password']==params['old_password']:
            raise exceptions.BadParametersException()
        user.password=get_hpassword(user.uid,params['new_password'])
    old_email=None
    if 'email' in params:
        if not arguments.is_valid_email(params['email']):
            raise exceptions.BadParametersException()
        params['email']=params['email'].lower()
        new_email=params['email']
        if not new_email==user.email:
            user2=cassapiuser.get_user(email=new_email)
            if user2:
                ''' Email already used'''
                raise exceptions.EmailAlreadyExistsException()
            user.email=params['email']
    if cassapiuser.insert_user(user=user):
        return True
    else:
        return False

def get_user_profile(username):
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data={}
    data['email']=user.email if user.email else ''
    return data

def get_user_config(username):
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    return user
