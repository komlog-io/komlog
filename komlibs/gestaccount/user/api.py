'''
user.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid,crypt
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import circle as cassapicircle
from komcass.api import snapshot as cassapisnapshot
from komcass.model.orm import user as ormuser
from komlibs.gestaccount.user import states, segments
from komlibs.gestaccount import exceptions, errors
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.general.string import stringops


def get_hpassword(uid,password):
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=errors.E_GUA_GHP_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=errors.E_GUA_GHP_IP)
    salt='$6$'+str(uid).split('-')[1]+'$'
    try:
        hpassword=crypt.crypt(password,salt)
    except TypeError:
        return None
    return hpassword

def auth_user(username, password):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_GUA_AUU_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=errors.E_GUA_AUU_IP)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_AUU_UNF)
    hpassword=get_hpassword(user.uid,password)
    if not hpassword:
        raise exceptions.BadParametersException(error=errors.E_GUA_AUU_HPNF)
    if user.password==get_hpassword(user.uid, password):
        return True
    else:
        return False

def create_user(username, password, email):
    '''This function creates a new user in the database'''
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_GUA_CRU_IU)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=errors.E_GUA_CRU_IP)
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_GUA_CRU_IE)
    user=cassapiuser.get_user(username=username)
    if user:
        raise exceptions.UserAlreadyExistsException(error=errors.E_GUA_CRU_UAEU)
    user=cassapiuser.get_user(email=email)
    if user:
        raise exceptions.UserAlreadyExistsException(error=errors.E_GUA_CRU_UAEE)
    uid=uuid.uuid4()
    hpassword=get_hpassword(uid,password)
    if not hpassword:
        raise exceptions.BadParametersException(error=errors.E_GUA_CRU_HPNF)
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
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_GUA_COU_IE)
    if not args.is_valid_code(code):
        raise exceptions.BadParametersException(error=errors.E_GUA_COU_IC)
    signup_info=cassapiuser.get_signup_info(email=email)
    if signup_info is None:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_COU_CNF)
    if signup_info.signup_code!=code:
        raise exceptions.UserConfirmationException(error=errors.E_GUA_COU_CMM)
    if signup_info.utilization_date:
        raise exceptions.UserConfirmationException(error=errors.E_GUA_COU_CAU)
    user=cassapiuser.get_user(username=signup_info.username)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_COU_UNF)
    signup_info.utilization_date=timeuuid.uuid1()
    user.state=states.ACTIVE
    if not cassapiuser.insert_user(user=user):
        raise exceptions.UserConfirmationException(error=errors.E_GUA_COU_IUE)
    cassapiuser.insert_signup_info(signup_info=signup_info)
    return True

def update_user_config(username, new_email=None, old_password=None, new_password=None):
    ''' This function is used to update user configuration parameters.
    Parameters supported:
        - password
        - email
    '''
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_GUA_UUC_IU)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_UUC_UNF)
    user_bck=user
    if new_email is None and old_password is None and new_password is None:
        raise exceptions.BadParametersException(error=errors.E_GUA_UUC_EMP)
    if bool(old_password) ^ bool(new_password):
        raise exceptions.BadParametersException(error=errors.E_GUA_UUC_ONP)
    if new_password and old_password:
        if not args.is_valid_password(new_password) or not args.is_valid_password(old_password):
            raise exceptions.BadParametersException(error=errors.E_GUA_UUC_IP)
        if not user.password==get_hpassword(user.uid,old_password):
            raise exceptions.InvalidPasswordException(error=errors.E_GUA_UUC_PNM)
        if new_password==old_password:
            raise exceptions.BadParametersException(error=errors.E_GUA_UUC_EQP)
        new_password=get_hpassword(user.uid,new_password)
        if new_password:
            user.password=new_password
        else:
            raise exceptions.BadParametersException(error=errors.E_GUA_UUC_HPNF)
    if new_email:
        if not args.is_valid_email(new_email):
            raise exceptions.BadParametersException(error=errors.E_GUA_UUC_IE)
        if not new_email==user.email:
            user2=cassapiuser.get_user(email=new_email)
            if user2:
                ''' Email already used'''
                raise exceptions.EmailAlreadyExistsException(error=errors.E_GUA_UUC_EAE)
            user.email=new_email
    if cassapiuser.insert_user(user=user):
        return True
    else:
        return False

def get_user_config(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_GUA_GUC_IU)
    user=cassapiuser.get_user(username=username)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_GUC_UNF)
    data={}
    data['email']=user.email if user.email else ''
    data['uid']=user.uid
    data['username']=user.username
    data['state']=user.state
    return data

def get_uid(username):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_GUA_GUID_IU)
    uid=cassapiuser.get_uid(username=username)
    if not uid:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_GUID_UNF)
    return uid

def register_invitation_request(email):
    ''' register_invitation_request is used to store a request of invitation,
        associated with an email provided by the user.
    '''
    if not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_GUA_RIR_IEMAIL)
    request=cassapiuser.get_invitation_request(email=email)
    if request is None:
        now=timeuuid.uuid1()
        request=ormuser.InvitationRequest(email=email, date=now, state=states.INVITATION_REQUEST_REGISTERED)
        return cassapiuser.insert_invitation_request(invitation_request=request)
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
        raise exceptions.BadParametersException(error=errors.E_GUA_GUI_IEMAIL)
    generated=[]
    regs=[]
    if num>1 or (num==1 and email is None):
        requests=cassapiuser.get_invitation_requests(state=states.INVITATION_REQUEST_REGISTERED,num=num)
        for request in requests:
            regs.append(request)
    elif email is not None:
        request=cassapiuser.get_invitation_request(email=email)
        if not request:
            request=ormuser.InvitationRequest(email=email, date=timeuuid.uuid1(), state=states.INVITATION_REQUEST_REGISTERED)
            if cassapiuser.insert_invitation_request(request):
                regs.append(request)
        else:
            regs.append(request)
    for request in regs:
        invitation=ormuser.Invitation(inv_id=uuid.uuid4(), date=timeuuid.uuid1(),state=states.INVITATION_UNUSED)
        request.inv_id=invitation.inv_id
        request.state=states.INVITATION_REQUEST_ASSOCIATED
        if cassapiuser.insert_invitation_request(request) and cassapiuser.insert_invitation_info(invitation):
            generated.append({'email':request.email,'inv_id':request.inv_id})
        else:
            cassapiuser.delete_invitation_info(inv_id=invitation.inv_id, date=invitation.date)
            request.inv_id=None
            request.state=states.INVITATION_REQUEST_REGISTERED
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
    except Exception as e:
        if user_info:
            cassapiuser.delete_user(username=user_info['username'])
            cassapiuser.delete_signup_info(username=user_info['username'])
        undo_invitation_transactions(inv_id=inv_id, tran_id=tran_id)
        raise e
    else:
        return user_info

def start_invitation_process(inv_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_SIP_IINV)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=errors.E_GUA_SIP_INVNF)
    elif len(invitation_info)>1:
        raise exceptions.InvitationProcessException(error=errors.E_GUA_SIP_INVAU)
    elif invitation_info[0].state == states.INVITATION_UNUSED and invitation_info[0].tran_id == None:
        now=timeuuid.uuid1()
        tran_id=uuid.uuid4()
        new_info=ormuser.Invitation(inv_id=inv_id, date=now, state=states.INVITATION_USING, tran_id=tran_id)
        if not cassapiuser.insert_invitation_info(invitation_info=new_info):
            raise exceptions.InvitationProcessException(error=errors.E_GUA_SIP_EIII)
        return tran_id
    else:
        raise exceptions.InvitationProcessException(error=errors.E_GUA_SIP_ISNE)

def end_invitation_process(inv_id, tran_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_EIP_IINV)
    if not args.is_valid_uuid(tran_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_EIP_ITRN)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=errors.E_GUA_EIP_INVNF)
    elif len(invitation_info)==1:
        raise exceptions.InvitationProcessException(error=errors.E_GUA_EIP_INUE)
    else:
        using_found=False
        for reg in invitation_info:
            if reg.state==states.INVITATION_USING:
                if reg.tran_id != tran_id:
                    raise exceptions.InvitationProcessException(error=errors.E_GUA_EIP_RCF)
                else:
                    using_found=True
        if not using_found:
            raise exceptions.InvitationProcessException(error=errors.E_GUA_EIP_SNF)
        else:
            now=timeuuid.uuid1()
            new_info=ormuser.Invitation(inv_id=inv_id, date=now, state=states.INVITATION_USED, tran_id=tran_id)
            if not cassapiuser.insert_invitation_info(invitation_info=new_info):
                raise exceptions.InvitationProcessException(error=errors.E_GUA_EIP_EIII)
        return True

def undo_invitation_transactions(inv_id, tran_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_UIT_IINV)
    if not args.is_valid_uuid(tran_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_UIT_ITRN)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=errors.E_GUA_UIT_INVNF)
    for reg in invitation_info:
        if reg.tran_id==tran_id:
            cassapiuser.delete_invitation_info(inv_id=inv_id, date=reg.date)
    return True

def initialize_invitation(inv_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_II_IINV)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=errors.E_GUA_II_INVNF)
    for reg in invitation_info:
        cassapiuser.delete_invitation_info(inv_id=inv_id, date=reg.date)
    now=timeuuid.uuid1()
    new_info=ormuser.Invitation(inv_id=inv_id, date=now, state=states.INVITATION_UNUSED)
    if not cassapiuser.insert_invitation_info(invitation_info=new_info):
        raise exceptions.InvitationProcessException(error=errors.E_GUA_II_EIII)
    return True

def check_unused_invitation(inv_id):
    if not args.is_valid_uuid(inv_id):
        raise exceptions.BadParametersException(error=errors.E_GUA_CUI_IINV)
    invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
    if len(invitation_info)==0:
        raise exceptions.InvitationNotFoundException(error=errors.E_GUA_CUI_INVNF)
    elif len(invitation_info)>1:
        raise exceptions.InvitationProcessException(error=errors.E_GUA_CUI_INVAU)
    elif len(invitation_info)==1 and invitation_info[0].state==states.INVITATION_UNUSED:
        return True
    else:
        raise exceptions.InvitationProcessException(error=errors.E_GUA_CUI_INVIS)

def register_forget_request(username=None, email=None):
    ''' register_forget_request is used to store a request when a user wants to reset
        her password.
        we will register the request associated to her uid.
    '''
    if username is not None and not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_GUA_RFR_IU)
    if email is not None and not args.is_valid_email(email):
        raise exceptions.BadParametersException(error=errors.E_GUA_RFR_IEMAIL)
    if not username and not email:
        raise exceptions.BadParametersException(error=errors.E_GUA_RFR_NPP)
    user=cassapiuser.get_user(username=username, email=email)
    if user:
        code=uuid.uuid4()
        now=timeuuid.uuid1()
        request=ormuser.ForgetRequest(code=code, date=now, state=states.FORGET_REQUEST_UNUSED, uid=user.uid)
        if cassapiuser.insert_forget_request(forget_request=request):
            return {'code':code,'username':user.username, 'email':user.email, 'uid':user.uid}
        else:
            raise exceptions.ForgetRequestException(error=errors.E_GUA_RFR_DBE)
    else:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_RFR_UNF)

def check_unused_forget_code(code):
    if not args.is_valid_uuid(code):
        raise exceptions.BadParametersException(error=errors.E_GUA_CUFC_ICODE)
    request=cassapiuser.get_forget_request(code=code)
    if not request:
        raise exceptions.ForgetRequestNotFoundException(error=errors.E_GUA_CUFC_CNF)
    elif request.state != states.FORGET_REQUEST_UNUSED:
        raise exceptions.ForgetRequestException(error=errors.E_GUA_CUFC_CODEAU)
    else:
        return True

def reset_password(code, password):
    if not args.is_valid_uuid(code):
        raise exceptions.BadParametersException(error=errors.E_GUA_RP_ICODE)
    if not args.is_valid_password(password):
        raise exceptions.BadParametersException(error=errors.E_GUA_RP_IPWD)
    request=cassapiuser.get_forget_request(code=code)
    if not request:
        raise exceptions.ForgetRequestNotFoundException(error=errors.E_GUA_RP_CNF)
    elif request.state != states.FORGET_REQUEST_UNUSED:
        raise exceptions.ForgetRequestException(error=errors.E_GUA_RP_CODEAU)
    user=cassapiuser.get_user(uid=request.uid)
    if not user:
        raise exceptions.UserNotFoundException(error=errors.E_GUA_RP_UNF)
    new_password=get_hpassword(user.uid,password)
    if new_password:
        if cassapiuser.update_user_password(username=user.username, password=new_password):
            cassapiuser.update_forget_request_state(code=code, new_state=states.FORGET_REQUEST_USED)
            return True
        else:
            raise exceptions.ForgetRequestException(error=errors.E_GUA_RP_EUDB)
    raise exceptions.ForgetRequestException(error=errors.E_GUA_RP_EGPWD)


