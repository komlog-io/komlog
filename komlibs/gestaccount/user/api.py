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
from komimc import messages
from komimc import api as msgapi


def get_hpassword(uid,password):
    salt='$6$'+str(uid).split('-')[1]+'$'
    hpassword=crypt.crypt(password,salt)
    return hpassword

def create_user(username, password, email):
    '''This function creates a new user in the database'''
    uid=uuid.uuid4()
    hpassword=get_hpassword(uid,password)
    now=datetime.utcnow()
    segment=segments.FREE
    user=ormuser.User(username=username, uid=uid, password=hpassword, email=email, segment=segments.FREE, creation_date=now, state=states.PREACTIVE)
    message=messages.NewUserMessage(uid=uid)
    if cassapiuser.new_user(user=user):
        if msgapi.send_message(message):
            return True
        else:
            cassapiuser.delete_user(uid=user.uid)
            return False
    else:
        return False


def confirm_user(email, code):
    '''This function confirm the user'''
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
    return {'result':email+' confirmation OK'}
    
def update_userprofile(username, params):
    ''' This function is used to update user configuration parameters.
    Parameters supported:
        - password
        - email
    '''
    user=cassapiuser.get_user(username=username)
    user_bck=user
    if not user:
        raise exceptions.UserNotFoundException()
    if 'email' not in params and 'new_password' not in params:
        raise exceptions.BadParametersException()
    if 'new_password' in params and 'old_password' not in params:
        raise exceptions.BadParametersException()
    if 'old_password' in params and 'new_password' not in params:
        raise exceptions.BadParametersException()
    if 'new_password' in params and 'old_password' in params:
        if not user.password==get_hpassword(user.uid,params['old_password']):
            raise exceptions.BadParametersException()
        if params['new_password']==params['old_password']:
            raise exceptions.BadParametersException()
        user.password=get_hpassword(user.uid,params['new_password'])
    old_email=None
    if 'email' in params:
        params['email']=params['email'].lower()
        new_email=params['email']
        if not new_email==user.email:
            user2=cassapiuser.get_user(email=new_email)
            if user2:
                ''' Email already used'''
                raise exceptions.BadParametersException()
            user.email=params['email']
    if cassapiuser.insert_user(user=user):
        return True
    else:
        return False

def get_userprofile(username):
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException()
    data={}
    data['email']=user.email if user.email else ''
    return data


