'''
user.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.model.orm import user as ormuser
from komlog.komlibs.gestaccount.user import segments
from komlog.komlibs.gestaccount.user.states import *
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto


def auth_user(username, password):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GUA_AUU_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_GUA_AUU_IP)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GUA_AUU_UNF)
    return crypto.verify_password(password, user.password, user.uid.bytes)

def create_user(username, password, email):
    '''This function creates a new user in the database'''
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IP)
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CRU_IE)
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
    segment=segments.FREE
    user=ormuser.User(username=username, uid=uid, password=hpassword, email=email, segment=segments.FREE, creation_date=now, state=UserStates.PREACTIVE)
    try:
        if cassapiuser.new_user(user=user):
            code=crypto.get_random_string(size=32)
            signup_info=ormuser.SignUp(username=user.username, code=code, email=user.email, creation_date=user.creation_date)
            if cassapiuser.insert_signup_info(signup_info=signup_info):
                return {'uid':user.uid, 'email':user.email, 'code':signup_info.code, 'username':user.username,'state':user.state, 'segment':user.segment}
            else:
                cassapiuser.delete_user(username=user.username)
                return None
        else:
            return None
    except cassexcept.KomcassException:
        cassapiuser.delete_user(username=user.username)
        cassapiuser.delete_signup_info(username=user.username)
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
    except cassexcept.KomcassException:
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
    except cassexcept.KomcassException:
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
            return cassapiuser.insert_invitation_request(invitation_request=request)
        except cassexcept.KomcassException:
            cassapiuser.delete_invitation_request(email=email)
            raise
    else:
        return True # request already registered

def generate_user_invitations(email=None, num=1):
    ''' generate_user_invitations is used to provision a new invitation in initial state
        in the system.
        - If email is passed, the invitation its associtated to the specified email, if not
        the system selects one from the pending invitation requests.
        - If num is passed, the system generates as many invitations as requested by num.
        
        Note that if num is greater than 1, the email argument takes no effect.
        
        This function returns an array with as many invitations as requested. in JSON format
        as this example:
        [{'email':'email@example.com','inv_id':uuid.UUID4() generated},...]
    '''
    if email is not None and not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=Errors.E_GUA_GUI_IEMAIL)
    generated=[]
    regs=[]
    if num>1 or (num==1 and email is None):
        requests=cassapiuser.get_invitation_requests(state=InvitationRequestStates.REGISTERED,num=num)
        for request in requests:
            regs.append(request)
    elif email is not None:
        request=cassapiuser.get_invitation_request(email=email)
        if not request:
            request=ormuser.InvitationRequest(email=email, date=timeuuid.uuid1(), state=InvitationRequestStates.REGISTERED)
            try:
                if cassapiuser.insert_invitation_request(request):
                    regs.append(request)
            except cassexcept.KomcassException:
                cassapiuser.delete_invitation_request(email=email)
        else:
            regs.append(request)
    for request in regs:
        invitation=ormuser.Invitation(inv_id=uuid.uuid4(), date=timeuuid.uuid1(),state=InvitationStates.UNUSED)
        request.inv_id=invitation.inv_id
        request.state=InvitationRequestStates.ASSOCIATED
        try:
            if cassapiuser.insert_invitation_request(request) and cassapiuser.insert_invitation_info(invitation):
                generated.append({'email':request.email,'inv_id':request.inv_id})
            else:
                cassapiuser.delete_invitation_info(inv_id=invitation.inv_id, date=invitation.date)
                request.inv_id=None
                request.state=InvitationRequestStates.REGISTERED
                cassapiuser.insert_invitation_request(request)
        except cassexcept.KomcassException:
            cassapiuser.delete_invitation_info(inv_id=invitation.inv_id, date=invitation.date)
            request.inv_id=None
            request.state=InvitationRequestStates.REGISTERED
            cassapiuser.insert_invitation_request(request)
    return generated

def create_user_by_invitation(username, password, email, inv_id):
    ''' This function creates a new user in the database if invitation is valid '''
    tran_id=start_invitation_process(inv_id=inv_id)
    user_info=None
    try:
        user_info=create_user(username=username, password=password, email=email)
        if user_info:
            end_invitation_process(inv_id=inv_id, tran_id=tran_id)
        else:
            initialize_invitation(inv_id=inv_id)
    except cassexcept.KomcassException:
        if user_info:
            cassapiuser.delete_user(username=user_info['username'])
            cassapiuser.delete_signup_info(username=user_info['username'])
        undo_invitation_transactions(inv_id=inv_id, tran_id=tran_id)
        raise
    else:
        return user_info

def start_invitation_process(inv_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_SIP_IINV)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_SIP_INVNF)
    elif len(invitation_info)>1:
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_SIP_INVAU)
    elif invitation_info[0].state == InvitationStates.UNUSED and invitation_info[0].tran_id == None:
        now=timeuuid.uuid1()
        tran_id=uuid.uuid4()
        new_info=ormuser.Invitation(inv_id=inv_id, date=now, state=InvitationStates.USING, tran_id=tran_id)
        try:
            if not cassapiuser.insert_invitation_info(invitation_info=new_info):
                raise exceptions.InvitationProcessException(error=Errors.E_GUA_SIP_EIII)
            return tran_id
        except cassexcept.KomcassException:
            cassapiuser.delete_invitation_info(inv_id=inv_id, date=now)
            raise
    else:
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_SIP_ISNE)

def end_invitation_process(inv_id, tran_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_EIP_IINV)
    if not args.is_valid_uuid(tran_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_EIP_ITRN)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_EIP_INVNF)
    elif len(invitation_info)==1:
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_EIP_INUE)
    else:
        using_found=False
        for reg in invitation_info:
            if reg.state==InvitationStates.USING:
                if reg.tran_id != tran_id:
                    raise exceptions.InvitationProcessException(error=Errors.E_GUA_EIP_RCF)
                else:
                    using_found=True
        if not using_found:
            raise exceptions.InvitationProcessException(error=Errors.E_GUA_EIP_SNF)
        else:
            now=timeuuid.uuid1()
            new_info=ormuser.Invitation(inv_id=inv_id, date=now, state=InvitationStates.USED, tran_id=tran_id)
            try:
                if not cassapiuser.insert_invitation_info(invitation_info=new_info):
                    raise exceptions.InvitationProcessException(error=Errors.E_GUA_EIP_EIII)
            except cassexcept.KomcassException:
                cassapiuser.delete_invitation_info(inv_id=new_info.inv_id, date=now)
                raise
        return True

def undo_invitation_transactions(inv_id, tran_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UIT_IINV)
    if not args.is_valid_uuid(tran_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_UIT_ITRN)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_UIT_INVNF)
    for reg in invitation_info:
        if reg.tran_id==tran_id:
            cassapiuser.delete_invitation_info(inv_id=inv_id, date=reg.date)
    return True

def initialize_invitation(inv_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_II_IINV)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_II_INVNF)
    for reg in invitation_info:
        cassapiuser.delete_invitation_info(inv_id=inv_id, date=reg.date)
    now=timeuuid.uuid1()
    new_info=ormuser.Invitation(inv_id=inv_id, date=now, state=InvitationStates.UNUSED)
    try:
        if not cassapiuser.insert_invitation_info(invitation_info=new_info):
            raise exceptions.InvitationProcessException(error=Errors.E_GUA_II_EIII)
    except cassexcept.KomcassException:
        cassapiuser.delete_invitation_info(inv_id=new_info.inv_id, date=now)
        raise
    return True

def check_unused_invitation(inv_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=Errors.E_GUA_CUI_IINV)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=Errors.E_GUA_CUI_INVNF)
    elif len(invitation_info)>1:
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_CUI_INVAU)
    elif len(invitation_info)==1 and invitation_info[0].state==InvitationStates.UNUSED:
        return True
    else:
        raise exceptions.InvitationProcessException(error=Errors.E_GUA_CUI_INVIS)

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
        except cassexcept.KomcassException:
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
        except cassapiexcept.KomcassException:
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

