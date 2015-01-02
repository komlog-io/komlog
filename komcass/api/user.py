#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import user as ormuser
from komcass.model.statement import user as stmtuser
from komcass.exception import user as excpuser
from komcass import connection

def get_user(username=None, uid=None, email=None):
    if username:
        row=connection.session.execute(stmtuser.S_A_MSTUSER_B_USERNAME,(username,))
        if not row:
            return None
        elif len(row)==1:
            return ormuser.User(**row[0])
        else:
            raise excpuser.DataConsistencyException(function='get_user',field='username',value=username)
    elif uid:
        row=connection.session.execute(stmtuser.S_A_MSTUSER_B_UID,(uid,))
        if not row:
            return None
        if len(row)==1:
            return ormuser.User(**row[0])
        else:
            raise excpuser.DataConsistencyException(function='get_user',field='uid',value=uid)
    elif email:
        row=connection.session.execute(stmtuser.S_A_MSTUSER_B_EMAIL,(email,))
        if not row:
            return None
        if len(row)==1:
            return ormuser.User(**row[0])
        else:
            raise excpuser.DataConsistencyException(function='get_user',field='email',value=email)
    else:
        return None

def new_user(user):
    if not isinstance(user, ormuser.User):
        return False
    else:
        signup_info=get_signup_info(email=user.email)
        if signup_info:
            return False
        signup_info=get_signup_info(username=user.username)
        if signup_info:
            return False
        userinfo=get_user(uid=user.uid)
        if userinfo:
            return False
        connection.session.execute(stmtuser.I_A_MSTUSER,(user.username,user.uid,user.password,user.email,user.state,user.segment,user.creation_date))
        return True

def insert_user(user):
    if not isinstance(user, ormuser.User):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTUSER,(user.username,user.uid,user.password,user.email,user.state,user.segment,user.creation_date))
        return True

def delete_user(username):
    connection.session.execute(stmtuser.D_A_MSTUSER_B_UID,(username,))
    return True

def get_signup_info(email=None, signup_code=None, username=None):
    if email:
        row=connection.session.execute(stmtuser.S_A_MSTSIGNUP_B_EMAIL,(email,))
        if not row:
            return None
        elif len(row)==1:
            return ormuser.SignUp(**row[0])
        else:
            raise excpuser.DataConsistencyException(function='get_signup_info',field='email',value=email)
    elif signup_code:
        row=connection.session.execute(stmtuser.S_A_MSTSIGNUP_B_SIGNUPCODE,(signup_code,))
        if not row:
            return None
        elif len(row)==1:
            return ormuser.SignUp(**row[0])
        else:
            raise excpuser.DataConsistencyException(function='get_signup_info',field='signup_code',value=signup_code)
    elif username:
        row=connection.session.execute(stmtuser.S_A_MSTSIGNUP_B_USERNAME,(username,))
        if not row:
            return None
        elif len(row)==1:
            return ormuser.SignUp(**row[0])
        else:
            raise excpuser.DataConsistencyException(function='get_signup_info',field='username',value=username)
    else:
        return None

def insert_signup_info(signup_info):
    if not isinstance(signup_info, ormuser.SignUp):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTSIGNUP,(signup_info.username,signup_info.signup_code,signup_info.email,signup_info.creation_date,signup_info.utilization_date))
        return True

