'''
users.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid,crypt
from datetime import datetime
from komcass import api as cassapi
from komlibs.gestaccount import states as states
from komlibs.gestaccount import segments
from komlibs.gestaccount import exceptions
from komimc import messages


def get_hpassword(uid,password):
    salt='$6$'+str(uid).split('-')[1]+'$'
    hpassword=crypt.crypt(password,salt)
    return hpassword

def create_user(username, password, email, session, msgbus):
    '''This function creates a new user in the database'''
    print 'inicio create _user'
    uid=uuid.uuid4()
    hpassword=get_hpassword(uid,password)
    now=datetime.utcnow()
    segment=segments.USER['FREE']
    print 'userinfo'
    userinfo=cassapi.UserInfo(uid=uid, username=username, password=hpassword, email=email, segment=segment, creation_date=now, state=states.USER['PREACTIVE'])
    print 'message'
    message=messages.NewUserMessage(uid=uid)
    print 'voy a registrar'
    if cassapi.register_user(userinfo,session):
        print 'ahora a enviar'
        if msgbus.sendMessage(message):
            return True
        else:
            cassapi.delete_user(userinfo,session)
            return False
    else:
        return False


def confirm_user(email, code, session):
    '''This function confirm the user'''
    print 'inicio confirm_user'
    usercoder=cassapi.get_usercoderelation(email,session)
    if not usercoder:
        raise exceptions.UserNotFoundException()
    if not code==usercoder.code:
        raise exceptions.UserNotFoundException()
    emailuidr=cassapi.get_emailuidrelation(email,session)
    if not emailuidr:
        raise exceptions.UserNotFoundException()
    userinfo=cassapi.get_userinfo(emailuidr.uid,{},session)
    if not userinfo:
        raise exceptions.UserNotFoundException()
    userinfo.state=states.USER['ACTIVE']
    if not cassapi.update_user(userinfo,session):
        raise exceptions.UserConfirmationException()
    return {'result':email+' confirmation OK'}
    
def update_user_configuration(username, params, session, msgbus):
    ''' This function is used to update user configuration parameters.
    Parameters supported:
        - password
        - email
    '''
    uidr=cassapi.get_useruidrelation(username, session)
    if not uidr:
        raise exceptions.UserNotFoundException()
    uid=uidr.uid
    print 'El UID: '+str(uid)
    userinfo=cassapi.get_userinfo(uid,{},session)
    print 'USERINFO: '+str(userinfo.__dict__)
    userinfo_bck=userinfo
    if not userinfo:
        raise Exception
    if not params.has_key('email') and not params.has_key('new_password'):
        raise exceptions.BadParametersException()
    if params.has_key('new_password') and not params.has_key('old_password'):
        raise exceptions.BadParametersException()
    if params.has_key('old_password') and not params.has_key('new_password'):
        raise exceptions.BadParametersException()
    if params.has_key('new_password') and params.has_key('old_password'):
        if not userinfo.password==get_hpassword(uid,params['old_password']):
            print 'Password incorrecto'
            raise exceptions.BadParametersException()
        if params['new_password']==params['old_password']:
            raise exceptions.BadParametersException()
        userinfo.password=get_hpassword(uid,params['new_password'])
    old_email=None
    if params.has_key('email'):
        params['email']=params['email'].lower()
        print 'Entramos al procesamiento del email'
        new_email=params['email']
        emailuidr=cassapi.get_emailuidrelation(new_email, session)
        if emailuidr:
            ''' Email already used'''
            print 'Email already used'
            raise exceptions.BadParametersException()
        old_email=userinfo.email
        if old_email:
            emailuidr=cassapi.get_emailuidrelation(old_email,session)
            if emailuidr:
                if emailuidr.uid==uid:
                    print 'Ahora borraria la relacion email-uid actual'
                    if not cassapi.delete_emailuidrelation(emailuidr,session):
                        raise Exception
                else:
                    'WTF: email not associated with current uid...data integrity problem...'
                    pass
        userinfo.email=params['email']
        new_emailuidr=cassapi.EmailUIDRelation(userinfo.email, uid)
        print 'Ahora insertaria la nueva relacion email-uid: '+str(new_emailuidr.__dict__)
        if not cassapi.insert_emailuidrelation(new_emailuidr,session):
            print 'Error al insertar la nueva relacion email-uid'
            raise Exception
    if cassapi.update_user(userinfo,session):
        print 'Actualizado Usuario OK'
        return True
    else:
        if old_email:
            emailuidr=cassapi.EmailUIDRelation(old_email, uid)
            cassapi.insert_emailuidrelation(emailuidr,session)
        new_emailuidr=cassapi.EmailUIDRelation(params['email'],uid)
        cassapi.delete_emailuidrelation(new_emailuidr,session)
        return False

