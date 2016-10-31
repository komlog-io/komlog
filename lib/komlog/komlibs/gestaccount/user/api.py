'''
user.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
import json
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.model.orm import user as ormuser
from komlog.komlibs.gestaccount.user import segments
from komlog.komlibs.gestaccount.user.states import *
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.string import stringops
from komlog.komlibs.payment import api as paymentapi


def auth_user(username, password):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GUA_AUU_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_GUA_AUU_IP)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_AUU_UNF)
    return crypto.verify_password(password, user.password, user.uid.bytes)

def create_user(username, password, email, inv_id=None, sid=None, token=None):
    '''This function creates a new user in the database'''
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IP)
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IE)
    if inv_id != None and not args.is_valid_string(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IINV)
    if sid!= None and not args.is_valid_int(sid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_ISID)
    if token != None and not args.is_valid_string(token):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_ITOK)
    user=cassapiuser.get_user(username=username)
    if user:
        raise exceptions.UserAlreadyExistsException(error=Errors.E_GUA_CRU_UAEU)
    user=cassapiuser.get_user(email=email)
    if user:
        raise exceptions.UserAlreadyExistsException(error=Errors.E_GUA_CRU_UAEE)
    uid=uuid.uuid4()
    hpassword=crypto.get_hashed_password(password, uid.bytes)
    if not hpassword:
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_HPNF)
    now=timeuuid.uuid1()
    if sid == None:
        sid=segments.FREE
    seginfo = cassapisegment.get_user_segment(sid=sid)
    if seginfo == None:
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_SEGNF)
    segfare = cassapisegment.get_user_segment_fare(sid=sid)
    if segfare != None and segfare.amount > 0 and token == None:
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_TOKNEED)
    if inv_id != None:
        inv_info = cassapiuser.get_invitation_info(inv_id=inv_id)
        if inv_info == None or inv_info.state != InvitationStates.ENABLED:
            raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_CRU_INVNF)
        if inv_info.count >= inv_info.max_count:
            raise exceptions.InvitationProcessException(error=Errors.E_GUA_CRU_INVMXCNTRCH)
        if (inv_info.active_from and now.time<inv_info.active_from.time) or (inv_info.active_until and now.time>inv_info.active_until.time):
            raise exceptions.InvitationProcessException(error=Errors.E_GUA_CRU_OUTINVINT)
        if not cassapiuser.increment_invitation_used_count(inv_id=inv_id, increment=1):
            raise exceptions.InvitationProcessException(error=Errors.E_GUA_CRU_EINCINVCNT)
    user=ormuser.User(username=username, uid=uid, password=hpassword, email=email, segment=sid, creation_date=now, state=UserStates.PREACTIVE)
    try:
        if token != None:
            customer = paymentapi.create_customer(uid=user.uid, token=token)
            if customer == None:
                raise exceptions.UserCreationException(error=Errors.E_GUA_CRU_ECREPAY)
        code=crypto.get_random_string(size=32)
        signup_info=ormuser.SignUp(username=user.username, code=code, email=user.email, creation_date=user.creation_date)
        if inv_id != None:
            signup_info.inv_id = inv_id
        billing_day = timeuuid.get_datetime_from_uuid1(now).day
        last_billing = timeuuid.min_uuid_from_time(timeuuid.get_unix_timestamp(now))
        if (cassapiuser.new_user(user=user) and
            cassapiuser.insert_signup_info(signup_info=signup_info) and
            cassapiuser.insert_user_billing_info(uid=user.uid, billing_day=billing_day, last_billing=last_billing)):
            return {'uid':user.uid, 'email':user.email, 'code':signup_info.code, 'username':user.username,'state':user.state, 'segment':user.segment}
        else:
            paymentapi.delete_customer(customer['id'])
            cassapiuser.delete_user(username=user.username)
            cassapiuser.delete_signup_info(username=user.username)
            cassapiuser.delete_user_billing_info(uid=user.uid)
            if inv_id != None:
                cassapiuser.increment_invitation_used_count(inv_id=inv_id, increment=-1)
            return None
    except:
        paymentapi.delete_customer(uid=user.uid)
        cassapiuser.delete_user(username=user.username)
        cassapiuser.delete_signup_info(username=user.username)
        cassapiuser.delete_user_billing_info(uid=user.uid)
        if inv_id != None:
            cassapiuser.increment_invitation_used_count(inv_id=inv_id, increment=-1)
        raise

def confirm_user(email, code):
    '''This function confirm the user'''
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_COU_IE)
    if not args.is_valid_code(code):
        raise exceptions.BadParametersException(error=Errors.E_GUA_COU_IC)
    signup_info=cassapiuser.get_signup_info(email=email)
    if signup_info is None:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_COU_CNF)
    if signup_info.code!=code:
        raise exceptions.UserConfirmationException(error=Errors.E_GUA_COU_CMM)
    if signup_info.utilization_date:
        raise exceptions.UserConfirmationException(error=Errors.E_GUA_COU_CAU)
    user=cassapiuser.get_user(username=signup_info.username)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_COU_UNF)
    new_signup_info=signup_info
    new_user=user
    new_signup_info.utilization_date=timeuuid.uuid1()
    new_user.state=UserStates.ACTIVE
    try:
        if not cassapiuser.insert_user(user=new_user):
            raise exceptions.UserConfirmationException(error=Errors.E_GUA_COU_IUE)
        cassapiuser.insert_signup_info(signup_info=new_signup_info)
        return True
    except:
        cassapiuser.insert_user(user=user)
        cassapiuser.insert_signup_info(signup_info=signup_info)
        raise

def update_user_config(uid, new_email=None, old_password=None, new_password=None):
    ''' This function is used to update user configuration parameters.
    Parameters supported:
        - password
        - email
    '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_UUC_UNF)
    new_user=user
    if new_email is None and old_password is None and new_password is None:
        raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_EMP)
    if bool(old_password) ^ bool(new_password):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_ONP)
    if new_password and old_password:
        if not args.is_valid_password(new_password) or not args.is_valid_password(old_password):
            raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_IP)
        if not crypto.verify_password(old_password, user.password, user.uid.bytes):
            raise exceptions.InvalidPasswordException(error=Errors.E_GUA_UUC_PNM)
        if new_password==old_password:
            raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_EQP)
        new_password=crypto.get_hashed_password(new_password, user.uid.bytes)
        if new_password:
            new_user.password=new_password
        else:
            raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_HPNF)
    if new_email:
        if not args.is_valid_email(new_email):
            raise exceptions.BadParametersException(error=Errors.E_GUA_UUC_IE)
        if not new_email==user.email:
            user2=cassapiuser.get_user(email=new_email)
            if user2:
                ''' Email already used'''
                raise exceptions.EmailAlreadyExistsException(error=Errors.E_GUA_UUC_EAE)
            new_user.email=new_email
    try:
        if cassapiuser.insert_user(user=new_user):
            return True
        else:
            return False
    except:
        cassapiuser.insert_user(user=user)
        raise

def get_user_config(uid):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUC_IU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_GUC_UNF)
    data={}
    data['email']=user.email if user.email else ''
    data['uid']=user.uid
    data['username']=user.username
    data['state']=user.state
    data['segment']=user.segment
    return data

def get_uid(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUID_IU)
    uid=cassapiuser.get_uid(username=username)
    if not uid:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_GUID_UNF)
    return uid

def register_invitation_request(email):
    ''' register_invitation_request is used to store a request of invitation,
        associated with an email provided by the user.
    '''
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RIR_IEMAIL)
    request=cassapiuser.get_invitation_request(email=email)
    if request is None:
        now=timeuuid.uuid1()
        request=ormuser.InvitationRequest(email=email, date=now, state=InvitationRequestStates.REGISTERED)
        try:
            return cassapiuser.new_invitation_request(invitation_request=request)
        except:
            cassapiuser.delete_invitation_request(email=email)
            raise
    else:
        if request.state == InvitationRequestStates.REGISTERED:
            return True #invitation registered, not sent yet
        else:
            if request.inv_id != None:
                inv_info = cassapiuser.get_invitation_info(inv_id = request.inv_id)
                if inv_info and inv_info.count > 0:
                    raise exceptions.UserUnsupportedOperationException(error=Errors.E_GUA_RIR_UAUAI)
                else:
                    cassapiuser.update_invitation_info_state(request.inv_id, InvitationStates.DISABLED)
            now=timeuuid.uuid1()
            request=ormuser.InvitationRequest(email=email, date=now, state=InvitationRequestStates.REGISTERED)
            try:
                return cassapiuser.insert_invitation_request(invitation_request=request)
            except:
                cassapiuser.delete_invitation_request(email=email)
                raise

def generate_user_invitations(email=None, num=1, max_count=1, active_from=None, active_until=None):
    ''' generate_user_invitations is used to provision a new invitation in initial state
        in the system.
        - If email is passed, the invitation its associtated to the specified email, if not
        the system selects one from the pending invitation requests.
        - If num is passed, the system generates as many invitations as requested by num.
        
        Note that if num is greater than 1, the email argument takes no effect.
        
        This function returns an array with as many invitations as requested. in JSON format
        as this example:
        [{'email':'email@example.com','inv_id':'invitation string'},...]
    '''
    if email is not None and not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUI_IEMAIL)
    if not args.is_valid_int(max_count):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUI_IMAXCNT)
    if active_from != None and not args.is_valid_date(active_from):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUI_IACTF)
    if active_until != None and not args.is_valid_date(active_until):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUI_IACTU)
    generated=[]
    regs=[]
    if num>1 or (num==1 and email is None):
        requests=cassapiuser.get_invitation_requests(state=InvitationRequestStates.REGISTERED,num=num)
        for request in requests:
            regs.append(request)
    elif email is not None:
        request=cassapiuser.get_invitation_request(email=email)
        if not request:
            register_invitation_request(email=email)
            request=cassapiuser.get_invitation_request(email=email)
            if request:
                regs.append(request)
        elif request.inv_id != None:
            inv_info = cassapiuser.get_invitation_info(inv_id=request.inv_id)
            if inv_info and inv_info.count > 0:
                raise exceptions.UserUnsupportedOperationException(error=Errors.E_GUA_GUI_UAUAI)
            else:
                cassapiuser.update_invitation_info_state(request.inv_id, InvitationStates.DISABLED)
                regs.append(request)
        else:
            regs.append(request)
    for request in regs:
        registered_invitation = False
        retry = 0
        while registered_invitation is False:
            inv_id = stringops.get_randomstring(length=10)
            invitation=ormuser.Invitation(inv_id=inv_id, creation_date=timeuuid.uuid1(),state=InvitationStates.ENABLED,max_count=max_count, active_from=active_from, active_until=active_until)
            if cassapiuser.new_invitation_info(invitation):
                registered_invitation = True
            else:
                if retry>=5:
                    raise exceptions.InvitationProcessException(error=Errors.E_GUA_GUI_ECINV)
                retry+=1
        request.inv_id=invitation.inv_id
        request.state=InvitationRequestStates.ASSOCIATED
        try:
            if cassapiuser.insert_invitation_request(request):
                generated.append({'email':request.email,'inv_id':request.inv_id})
            else:
                cassapiuser.delete_invitation_info(inv_id=invitation.inv_id)
                request.inv_id=None
                request.state=InvitationRequestStates.REGISTERED
                cassapiuser.insert_invitation_request(request)
        except:
            cassapiuser.delete_invitation_info(inv_id=invitation.inv_id)
            request.inv_id=None
            request.state=InvitationRequestStates.REGISTERED
            cassapiuser.insert_invitation_request(request)
    return generated

def check_unused_invitation(inv_id):
    if not args.is_valid_string(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CUI_IINV)
    now = timeuuid.uuid1()
    inv_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if inv_info == None or inv_info.state == InvitationStates.DISABLED:
        raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_CUI_INVNF)
    elif inv_info.count >= inv_info.max_count:
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_CUI_INVMXCNTRCH)
    elif (inv_info.active_from and now.time<inv_info.active_from.time) or (inv_info.active_until and now.time>inv_info.active_until.time):
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_CUI_OUTINVINT)
    else:
        return True

def register_forget_request(username=None, email=None):
    ''' register_forget_request is used to store a request when a user wants to reset
        her password.
        we will register the request associated to her uid.
    '''
    if username is not None and not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RFR_IU)
    if email is not None and not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RFR_IEMAIL)
    if not username and not email:
        raise exceptions.BadParametersException(error=Errors.E_GUA_RFR_NPP)
    user=cassapiuser.get_user(username=username, email=email)
    if user:
        code=uuid.uuid4()
        now=timeuuid.uuid1()
        request=ormuser.ForgetRequest(code=code, date=now, state=ForgetRequestStates.UNUSED, uid=user.uid)
        try:
            if cassapiuser.insert_forget_request(forget_request=request):
                return {'code':code,'username':user.username, 'email':user.email, 'uid':user.uid}
            else:
                raise exceptions.ForgetRequestException(error=Errors.E_GUA_RFR_DBE)
        except:
            cassapiuser.delete_forget_request(code=code)
            raise
    else:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_RFR_UNF)

def check_unused_forget_code(code):
    if not args.is_valid_uuid(code):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CUFC_ICODE)
    request=cassapiuser.get_forget_request(code=code)
    if not request:
        raise exceptions.ForgetRequestNotFoundException(error=Errors.E_GUA_CUFC_CNF)
    elif request.state != ForgetRequestStates.UNUSED:
        raise exceptions.ForgetRequestException(error=Errors.E_GUA_CUFC_CODEAU)
    else:
        return True

def reset_password(code, password):
    if not args.is_valid_uuid(code):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RP_ICODE)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RP_IPWD)
    request=cassapiuser.get_forget_request(code=code)
    if not request:
        raise exceptions.ForgetRequestNotFoundException(error=Errors.E_GUA_RP_CNF)
    elif request.state != ForgetRequestStates.UNUSED:
        raise exceptions.ForgetRequestException(error=Errors.E_GUA_RP_CODEAU)
    user=cassapiuser.get_user(uid=request.uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_RP_UNF)
    new_password=crypto.get_hashed_password(password, user.uid.bytes)
    if new_password:
        try:
            if cassapiuser.update_user_password(username=user.username, password=new_password):
                cassapiuser.update_forget_request_state(code=code, new_state=ForgetRequestStates.USED)
                return True
            else:
                raise exceptions.ForgetRequestException(error=Errors.E_GUA_RP_EUDB)
        except:
            cassapiuser.update_user_password(username=user.username, password=user.password)
            cassapiuser.update_forget_request_state(code=code, new_state=ForgetRequestStates.UNUSED)
            raise
    raise exceptions.ForgetRequestException(error=Errors.E_GUA_RP_EGPWD)

def register_pending_hook(uid, uri, sid):
    ''' This function register a new pending hook with the associated parameters. The pending
        hooks are hook requests over non existent uris. We register this requests so if the uri
        is eventually created by the user, this pending hooks will be automatically transformed
        into hooks to that uri, and notifications will be sent to the user on each update '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RPH_IUID)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RPH_IURI)
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_RPH_ISID)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_RPH_UNF)
    pending_hook=ormuser.PendingHook(uid=uid, uri=uri, sid=sid)
    cassapiuser.insert_pending_hook(pending_hook=pending_hook)
    return True

def get_uri_pending_hooks(uid, uri):
    ''' This function returns a list of the pending hooks associated to the uid and uri passed
        as arguments. We only return the sids in the list '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUPH_IUID)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUPH_IURI)
    found=cassapiuser.get_pending_hooks(uid=uid, uri=uri)
    sids=[item.sid for item in found]
    return sids

def delete_session_pending_hooks(sid):
    ''' This function deletes all pending hooks associated to one session id '''
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_DSPH_ISID)
    session_hooks=cassapiuser.get_pending_hooks_by_sid(sid=sid)
    for hook in session_hooks:
        cassapiuser.delete_pending_hook(uid=hook.uid, uri=hook.uri, sid=hook.sid)
    return True

def delete_uri_pending_hooks(uid, uri):
    ''' This function deletes all pending hooks associated to one uri '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_DUPH_IUID)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_GUA_DUPH_IURI)
    cassapiuser.delete_pending_hooks(uid=uid, uri=uri)
    return True

def delete_pending_hook(uid, uri, sid):
    ''' This function deletes the pending hook requested in parameters '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_DPH_IUID)
    if not args.is_valid_uri(uri):
        raise exceptions.BadParametersException(error=Errors.E_GUA_DPH_IURI)
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_DPH_ISID)
    cassapiuser.delete_pending_hook(uid=uid, uri=uri, sid=sid)
    return True

def update_segment(uid, sid, token=None):
    '''This function updates the segment of the user '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UPDSEG_IUID)
    if not args.is_valid_int(sid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UPDSEG_ISID)
    if token != None and not args.is_valid_string(token):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UPDSEG_ITOK)
    user=cassapiuser.get_user(uid=uid)
    if user is None:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_UPDSEG_UNF)
    if user.segment == sid:
        return True
    seginfo = cassapisegment.get_user_segment(sid=sid)
    if seginfo == None:
        raise exceptions.BadParametersException(error=Errors.E_GUA_UPDSEG_SEGNF)
    allowed_transitions=cassapisegment.get_user_segment_allowed_transitions(sid=user.segment)
    if allowed_transitions is None or sid not in allowed_transitions.sids:
        raise exceptions.UserUnsupportedOperationException(error=Errors.E_GUA_UPDSEG_TRNTAL)
    segfare = cassapisegment.get_user_segment_fare(sid=sid)
    if segfare != None and segfare.amount > 0:
        customer = paymentapi.get_customer(uid=uid)
        if customer is None and token is None:
            raise exceptions.BadParametersException(error=Errors.E_GUA_UPDSEG_TOKNEED)
    updated = False
    now = timeuuid.uuid1()
    try:
        if cassapiuser.update_user_segment(username=user.username, segment=sid, current_segment=user.segment):
            cassapisegment.insert_user_segment_transition(uid=uid, date=now, sid=sid, previous_sid=user.segment)
            updated = True
            if segfare != None and segfare.amount > 0:
                if customer is None and token:
                    if paymentapi.create_customer(uid=uid, token=token):
                        return True
                elif customer and token:
                    if paymentapi.update_customer(uid=uid, token=token):
                        return True
                else:
                    return True
                raise exceptions.UpdateOperationException(error=Errors.E_GUA_UPDSEG_EUPAY)
            return True
        else:
            raise exceptions.UpdateOperationException(error=Errors.E_GUA_UPDSEG_EUDB)
    except:
        if updated:
            cassapiuser.update_user_segment(username=user.username, segment=user.segment, current_segment = sid)
            cassapisegment.delete_user_segment_transition(uid=uid, date=now)
        raise

def get_user_segment_info(uid):
    '''This function returns user segment info and allowed transitions '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUSEGINF_IUID)
    user=cassapiuser.get_user(uid=uid)
    if user is None:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_GUSEGINF_UNF)
    seginfo = cassapisegment.get_user_segment(sid=user.segment)
    if seginfo == None:
        return None
    segfare = cassapisegment.get_user_segment_fare(sid=seginfo.sid)
    info = {}
    info['current_plan']={
        'description':seginfo.description,
        'id':seginfo.sid,
        'price':str(segfare.amount) if segfare else '0',
    }
    info['allowed_plans']=[]
    allowed_transitions=cassapisegment.get_user_segment_allowed_transitions(sid=user.segment)
    for tr_sid in allowed_transitions.sids:
        tr_info = cassapisegment.get_user_segment(sid=tr_sid)
        if tr_info:
            tr_fare = cassapisegment.get_user_segment_fare(sid=tr_sid)
            info['allowed_plans'].append({
                'description':tr_info.description,
                'id':tr_info.sid,
                'price':str(tr_fare.amount) if tr_fare else '0',
            })
    payment_info = paymentapi.get_customer(uid=uid)
    if payment_info:
        source_id = payment_info['default_source']
        if source_id:
            for source in payment_info['sources']['data']:
                if source['id'] == source_id:
                    info['payment_info']={
                        'last4':source['last4'],
                        'exp_month':source['exp_month'],
                        'exp_year':source['exp_year'],
                    }
    return info

