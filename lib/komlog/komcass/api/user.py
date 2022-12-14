'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komfig import logging
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.statement import user as stmtuser
from komlog.komcass import connection, exceptions

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def get_uid(username):
    row=connection.session.execute(stmtuser.S_UID_MSTUSER_B_USERNAME,(username,))
    return row[0]['uid'] if row else None

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def insert_user(user):
    if not isinstance(user, ormuser.User):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTUSER,(user.username,user.uid,user.password,user.email,user.state,user.segment,user.creation_date))
        return True

@exceptions.ExceptionHandler
def update_user_password(username, password):
    resp=connection.session.execute(stmtuser.U_PASSWORD_MSTUSER_B_USERNAME,(password,username))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def update_user_segment(username, segment, current_segment=None):
    if current_segment != None:
        resp=connection.session.execute(stmtuser.U_SEGMENT_MSTUSER_B_USERNAME_IEQ_SEGMENT,(segment,username, current_segment))
    else:
        resp=connection.session.execute(stmtuser.U_SEGMENT_MSTUSER_B_USERNAME,(segment,username))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def delete_user(username):
    connection.session.execute(stmtuser.D_A_MSTUSER_B_USERNAME,(username,))
    return True

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def insert_signup_info(signup_info):
    if not isinstance(signup_info, ormuser.SignUp):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTSIGNUP,(signup_info.username,signup_info.email, signup_info.code,signup_info.inv_id,signup_info.creation_date,signup_info.utilization_date))
        return True

@exceptions.ExceptionHandler
def delete_signup_info(username):
    connection.session.execute(stmtuser.D_A_MSTSIGNUP_B_USERNAME,(username,))
    return True

@exceptions.ExceptionHandler
def get_invitation_info(inv_id):
    row=connection.session.execute(stmtuser.S_A_MSTINVITATION_B_INVID,(inv_id,))
    if row:
        return ormuser.Invitation(**row[0])
    return None

@exceptions.ExceptionHandler
def new_invitation_info(invitation_info):
    if not isinstance(invitation_info, ormuser.Invitation):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTINVITATION_INE,(invitation_info.inv_id,invitation_info.creation_date,invitation_info.state,invitation_info.count, invitation_info.max_count, invitation_info.active_from, invitation_info.active_until))
        return True

@exceptions.ExceptionHandler
def insert_invitation_info(invitation_info):
    if not isinstance(invitation_info, ormuser.Invitation):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTINVITATION,(invitation_info.inv_id,invitation_info.creation_date,invitation_info.state,invitation_info.count, invitation_info.max_count, invitation_info.active_from, invitation_info.active_until))
        return True

@exceptions.ExceptionHandler
def delete_invitation_info(inv_id):
    connection.session.execute(stmtuser.D_A_MSTINVITATION_B_INVID,(inv_id,))
    return True

@exceptions.ExceptionHandler
def update_invitation_info_state(inv_id, new_state):
    resp=connection.session.execute(stmtuser.U_STATE_MSTINVITATION_B_INVID,(new_state,inv_id))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def increment_invitation_used_count(inv_id, increment):
    ''' we use lightweight transactions to increment invitation count '''
    resp=connection.session.execute(stmtuser.U_COUNT_MSTINVITATION_I_COUNT,(increment, inv_id, 0))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    elif 'count' in resp[0]:
        cur_val = resp[0]['count']
        n_val=cur_val + increment
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtuser.U_COUNT_MSTINVITATION_I_COUNT,(n_val,inv_id, cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['count']
                n_val=cur_val+ increment
        return True
    return False

@exceptions.ExceptionHandler
def get_invitation_request(email):
    row=connection.session.execute(stmtuser.S_A_DATINVITATIONREQUEST_B_EMAIL,(email,))
    return ormuser.InvitationRequest(**row[0]) if row else None

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def new_invitation_request(invitation_request):
    if not isinstance(invitation_request, ormuser.InvitationRequest):
        return False
    else:
        resp = connection.session.execute(stmtuser.I_A_DATINVITATIONREQUEST_INE,(invitation_request.email,invitation_request.date,invitation_request.state,invitation_request.inv_id))
        return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_invitation_request(invitation_request):
    if not isinstance(invitation_request, ormuser.InvitationRequest):
        return False
    else:
        connection.session.execute(stmtuser.I_A_DATINVITATIONREQUEST,(invitation_request.email,invitation_request.date,invitation_request.state,invitation_request.inv_id))
        return True

@exceptions.ExceptionHandler
def delete_invitation_request(email):
    connection.session.execute(stmtuser.D_A_DATINVITATIONREQUEST_B_EMAIL,(email,))
    return True

@exceptions.ExceptionHandler
def update_invitation_request_state(email, new_state):
    resp=connection.session.execute(stmtuser.U_STATE_DATINVITATIONREQUEST_B_EMAIL,(new_state,email))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def get_forget_request(code):
    row=connection.session.execute(stmtuser.S_A_DATFORGETREQUEST_B_CODE,(code,))
    return ormuser.ForgetRequest(**row[0]) if row else None

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def get_forget_requests_by_uid(uid):
    row=connection.session.execute(stmtuser.S_A_DATFORGETREQUEST_B_UID,(uid,))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.ForgetRequest(**d))
    return data

@exceptions.ExceptionHandler
def insert_forget_request(forget_request):
    if not isinstance(forget_request, ormuser.ForgetRequest):
        return False
    else:
        connection.session.execute(stmtuser.I_A_DATFORGETREQUEST,(forget_request.code,forget_request.date,forget_request.state,forget_request.uid))
        return True

@exceptions.ExceptionHandler
def delete_forget_request(code):
    connection.session.execute(stmtuser.D_A_DATFORGETREQUEST_B_CODE,(code,))
    return True

@exceptions.ExceptionHandler
def update_forget_request_state(code, new_state):
    resp=connection.session.execute(stmtuser.U_STATE_DATFORGETREQUEST_B_CODE,(new_state,code))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def get_pending_hooks(uid, uri=None):
    if uri is None:
        row=connection.session.execute(stmtuser.S_A_MSTPENDINGHOOK_B_UID,(uid,))
    else:
        row=connection.session.execute(stmtuser.S_A_MSTPENDINGHOOK_B_UID_URI,(uid,uri))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.PendingHook(**d))
    return data

@exceptions.ExceptionHandler
def get_pending_hooks_by_sid(sid):
    row=connection.session.execute(stmtuser.S_A_MSTPENDINGHOOK_B_SID,(sid,))
    data=[]
    if row:
        for d in row:
            data.append(ormuser.PendingHook(**d))
    return data

@exceptions.ExceptionHandler
def get_pending_hook(uid, uri, sid):
    row=connection.session.execute(stmtuser.S_A_MSTPENDINGHOOK_B_UID_URI_SID,(uid,uri,sid))
    if row:
        return ormuser.PendingHook(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def insert_pending_hook(pending_hook):
    if not isinstance(pending_hook, ormuser.PendingHook):
        return False
    else:
        connection.session.execute(stmtuser.I_A_MSTPENDINGHOOK,(pending_hook.uid,pending_hook.uri,pending_hook.sid))
        return True

@exceptions.ExceptionHandler
def delete_pending_hooks(uid, uri=None):
    if uri is None:
        connection.session.execute(stmtuser.D_A_MSTPENDINGHOOK_B_UID,(uid,))
    else:
        connection.session.execute(stmtuser.D_A_MSTPENDINGHOOK_B_UID_URI,(uid,uri))
    return True

@exceptions.ExceptionHandler
def delete_pending_hook(uid, uri, sid):
    connection.session.execute(stmtuser.D_A_MSTPENDINGHOOK_B_UID_URI_SID,(uid,uri,sid))
    return True

@exceptions.ExceptionHandler
def get_user_billing_info(uid):
    row=connection.session.execute(stmtuser.S_A_MSTUSERBILLINGINFO_B_UID,(uid,))
    return ormuser.BillingInfo(**row[0]) if row else None

@exceptions.ExceptionHandler
def new_user_billing_info(uid, billing_day, last_billing):
    resp=connection.session.execute(stmtuser.I_A_MSTUSERBILLINGINFO_INE,(uid, billing_day, last_billing))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_user_billing_info(uid, billing_day, last_billing):
    connection.session.execute(stmtuser.I_A_MSTUSERBILLINGINFO,(uid, billing_day, last_billing))
    return True

@exceptions.ExceptionHandler
def delete_user_billing_info(uid):
    resp=connection.session.execute(stmtuser.D_A_MSTUSERBILLINGINFO_B_UID_IE,(uid,))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def update_user_billing_day(uid, billing_day, current_billing_day=None):
    if current_billing_day != None:
        resp=connection.session.execute(stmtuser.U_BILLINGDAY_MSTUSERBILLINGINFO_B_UID_IEQ_BILLINGDAY,(billing_day, uid, current_billing_day))
        return resp[0]['[applied]'] if resp else False
    else:
        connection.session.execute(stmtuser.U_BILLINGDAY_MSTUSERBILLINGINFO_B_UID,(billing_day, uid))
        return True

@exceptions.ExceptionHandler
def update_user_last_billing(uid, last_billing, current_last_billing=None):
    if current_last_billing != None:
        resp=connection.session.execute(stmtuser.U_LASTBILLING_MSTUSERBILLINGINFO_B_UID_IEQ_LASTBILLING,(last_billing, uid, current_last_billing))
        return resp[0]['[applied]'] if resp else False
    else:
        connection.session.execute(stmtuser.U_LASTBILLING_MSTUSERBILLINGINFO_B_UID,(last_billing, uid))
        return True

@exceptions.ExceptionHandler
def get_user_stripe_info(uid):
    row=connection.session.execute(stmtuser.S_A_MSTUSERSTRIPEINFO_B_UID,(uid,))
    return ormuser.StripeInfo(**row[0]) if row else None

@exceptions.ExceptionHandler
def new_user_stripe_info(uid, stripe_id):
    resp=connection.session.execute(stmtuser.I_A_MSTUSERSTRIPEINFO_INE,(uid,stripe_id))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_user_stripe_info(uid, stripe_id):
    connection.session.execute(stmtuser.I_A_MSTUSERSTRIPEINFO,(uid,stripe_id))
    return True

@exceptions.ExceptionHandler
def delete_user_stripe_info(uid):
    resp=connection.session.execute(stmtuser.D_A_MSTUSERSTRIPEINFO_B_UID_IE,(uid,))
    return resp[0]['[applied]'] if resp else False

