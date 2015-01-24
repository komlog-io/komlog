'''
user.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid,crypt
from komcass.api import user as cassapiuser
from komcass.model.orm import user as ormuser
from komlibs.gestaccount.user import states, segments
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments
from komlibs.general.time import timeuuid
from komlibs.general.string import stringops


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
    if not arguments.is_valid_username(username) or not arguments.is_valid_password(password) or not arguments.is_valid_email(email):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if user:
        raise exceptions.UserAlreadyExistsException()
    user=cassapiuser.get_user(email=email)
    if user:
        raise exceptions.UserAlreadyExistsException()
    uid=uuid.uuid4()
    hpassword=get_hpassword(uid,password)
    if not hpassword:
        raise exceptions.BadParametersException()
    now=timeuuid.uuid1()
    segment=segments.FREE
    user=ormuser.User(username=username, uid=uid, password=hpassword, email=email, segment=segments.FREE, creation_date=now, state=states.PREACTIVE)
    if cassapiuser.new_user(user=user):
        signup_code=stringops.get_randomstring(size=32)
        signup_info=ormuser.SignUp(username=user.username, signup_code=signup_code, email=user.email, creation_date=user.creation_date)
        if cassapiuser.insert_signup_info(signup_info=signup_info):
            return {'uid':user.uid, 'email':user.email, 'signup_code':signup_info.signup_code, 'username':user.username}
        else:
            cassapiuser.delete_user(username=user.username)
            return None
    else:
        return None

def confirm_user(email, code):
    '''This function confirm the user'''
    if not arguments.is_valid_email(email) or not arguments.is_valid_code(code):
        raise exceptions.BadParametersException()
    signup_info=cassapiuser.get_signup_info(email=email)
    if signup_info is None:
        raise exceptions.UserNotFoundException()
    if signup_info.signup_code!=code:
        raise exceptions.UserConfirmationException()
    if signup_info.utilization_date:
        raise exceptions.UserConfirmationException()
    user=cassapiuser.get_user(username=signup_info.username)
    if not user:
        raise exceptions.UserNotFoundException()
    signup_info.utilization_date=timeuuid.uuid1()
    user.state=states.ACTIVE
    if not cassapiuser.insert_user(user=user):
        raise exceptions.UserConfirmationException()
    cassapiuser.insert_signup_info(signup_info=signup_info)
    return True
    
def update_user_config(username, new_email=None, old_password=None, new_password=None):
    ''' This function is used to update user configuration parameters.
    Parameters supported:
        - password
        - email
    '''
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    user_bck=user
    if new_email is None and old_password is None and new_password is None:
        raise exceptions.BadParametersException()
    if bool(old_password) ^ bool(new_password):
        raise exceptions.BadParametersException()
    if new_password and old_password:
        if not arguments.is_valid_password(new_password) or not arguments.is_valid_password(old_password):
            raise exceptions.BadParametersException()
        if not user.password==get_hpassword(user.uid,old_password):
            raise exceptions.InvalidPasswordException()
        if new_password==old_password:
            raise exceptions.BadParametersException()
        new_password=get_hpassword(user.uid,new_password)
        if new_password:
            user.password=new_password
        else:
            raise exceptions.BadParametersException()
    if new_email:
        if not arguments.is_valid_email(new_email):
            raise exceptions.BadParametersException()
        if not new_email==user.email:
            user2=cassapiuser.get_user(email=new_email)
            if user2:
                ''' Email already used'''
                raise exceptions.EmailAlreadyExistsException()
            user.email=new_email
    if cassapiuser.insert_user(user=user):
        return True
    else:
        return False

def get_user_config(username):
    if not arguments.is_valid_username(username):
        raise exceptions.BadParametersException()
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data={}
    data['email']=user.email if user.email else ''
    data['uid']=user.uid
    data['username']=user.username
    data['state']=user.state
    return data

