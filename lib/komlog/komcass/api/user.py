#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komfig import logging
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.statement import user as stmtuser
from komlog.komcass.exception import user as excpuser
from komlog.komcass import connection

def get_user(username=None, uid=None, email=None):
    if username:
        row=connection.session.execute(stmtuser.S_A_MSTUSER_B_USERNAME,(username,))
        if not row:
            return None
        else:
            return ormuser.User(**row[0])
    elif uid:
        row=connection.session.execute(stmtuser.S_A_MSTUSER_B_UID,(uid,))
        if not row:
            return None
        else:
            return ormuser.User(**row[0])
    elif email:
        row=connection.session.execute(stmtuser.S_A_MSTUSER_B_EMAIL,(email,))
        if not row:
            return None
        else:
            return ormuser.User(**row[0])
    else:
        return None

def get_uid(username):
    row=connection.session.execute(stmtuser.S_UID_MSTUSER_B_USERNAME,(username,))
    return row[0]['uid'] if row else None

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
        resp=connection.session.execute(stmtuser.I_A_MSTUSER_INE,(user.username,user.uid,user.password,user.email,user.state,user.segment,user.creation_date))
        return resp[0]['[applied]'] if resp else False

def insert_user(user):
    if not isinstance(user, ormuser.User):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTUSER,(user.username,user.uid,user.password,user.email,user.state,user.segment,user.creation_date))
        return True

def update_user_password(username, password):
    resp=connection.session.execute(stmtuser.U_PASSWORD_MSTUSER_B_USERNAME,(password,username))
    return resp[0]['[applied]'] if resp else False

def delete_user(username):
    connection.session.execute(stmtuser.D_A_MSTUSER_B_USERNAME,(username,))
    return True

def get_signup_info(email=None, code=None, username=None):
    if email:
        row=connection.session.execute(stmtuser.S_A_MSTSIGNUP_B_EMAIL,(email,))
        if not row:
            return None
        else:
            return ormuser.SignUp(**row[0])
    elif code:
        row=connection.session.execute(stmtuser.S_A_MSTSIGNUP_B_CODE,(code,))
        if not row:
            return None
        else:
            return ormuser.SignUp(**row[0])
    elif username:
        row=connection.session.execute(stmtuser.S_A_MSTSIGNUP_B_USERNAME,(username,))
        if not row:
            return None
        else:
            return ormuser.SignUp(**row[0])
    else:
        return None

def insert_signup_info(signup_info):
    if not isinstance(signup_info, ormuser.SignUp):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTSIGNUP,(signup_info.username,signup_info.code,signup_info.email,signup_info.creation_date,signup_info.utilization_date))
        return True

def delete_signup_info(username):
    connection.session.execute(stmtuser.D_A_MSTSIGNUP_B_USERNAME,(username,))
    return True

def get_invitation_info(inv_id):
    row=connection.session.execute(stmtuser.S_A_DATINVITATION_B_INVID,(inv_id,))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.Invitation(**d))
    return data

def insert_invitation_info(invitation_info):
    if not isinstance(invitation_info, ormuser.Invitation):
        return False
    else:
        connection.session.execute(stmtuser.I_A_DATINVITATION,(invitation_info.inv_id,invitation_info.date,invitation_info.state,invitation_info.tran_id))
        return True

def delete_invitation_info(inv_id, date=None):
    if date:
        connection.session.execute(stmtuser.D_A_DATINVITATION_B_INVID_DATE,(inv_id,date))
    else:
        connection.session.execute(stmtuser.D_A_DATINVITATION_B_INVID,(inv_id,))
    return True

def get_invitation_request(email):
    row=connection.session.execute(stmtuser.S_A_DATINVITATIONREQUEST_B_EMAIL,(email,))
    return ormuser.InvitationRequest(**row[0]) if row else None

def get_invitation_requests(state, num=0):
    if num==0:
        row=connection.session.execute(stmtuser.S_A_DATINVITATIONREQUEST_B_STATE,(state,))
    else:
        row=connection.session.execute(stmtuser.S_A_DATINVITATIONREQUEST_B_STATE_NUM,(state,num))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.InvitationRequest(**d))
    return data

def insert_invitation_request(invitation_request):
    if not isinstance(invitation_request, ormuser.InvitationRequest):
        return False
    else:
        connection.session.execute(stmtuser.I_A_DATINVITATIONREQUEST,(invitation_request.email,invitation_request.date,invitation_request.state,invitation_request.inv_id))
        return True

def delete_invitation_request(email):
    connection.session.execute(stmtuser.D_A_DATINVITATIONREQUEST_B_EMAIL,(email,))
    return True

def update_invitation_request_state(email, new_state):
    resp=connection.session.execute(stmtuser.U_STATE_DATINVITATIONREQUEST_B_EMAIL,(new_state,email))
    return resp[0]['[applied]'] if resp else False

def get_forget_request(code):
    row=connection.session.execute(stmtuser.S_A_DATFORGETREQUEST_B_CODE,(code,))
    return ormuser.ForgetRequest(**row[0]) if row else None

def get_forget_requests(state, num=0):
    if num==0:
        row=connection.session.execute(stmtuser.S_A_DATFORGETREQUEST_B_STATE,(state,))
    else:
        row=connection.session.execute(stmtuser.S_A_DATFORGETREQUEST_B_STATE_NUM,(state,num))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.ForgetRequest(**d))
    return data

def get_forget_requests_by_uid(uid):
    row=connection.session.execute(stmtuser.S_A_DATFORGETREQUEST_B_UID,(uid,))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.ForgetRequest(**d))
    return data

def insert_forget_request(forget_request):
    if not isinstance(forget_request, ormuser.ForgetRequest):
        return False
    else:
        connection.session.execute(stmtuser.I_A_DATFORGETREQUEST,(forget_request.code,forget_request.date,forget_request.state,forget_request.uid))
        return True

def delete_forget_request(code):
    connection.session.execute(stmtuser.D_A_DATFORGETREQUEST_B_CODE,(code,))
    return True

def update_forget_request_state(code, new_state):
    resp=connection.session.execute(stmtuser.U_STATE_DATFORGETREQUEST_B_CODE,(new_state,code))
    return resp[0]['[applied]'] if resp else False

