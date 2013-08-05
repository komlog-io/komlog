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
from komimc import messages


def create_user(username, password, email, session, msgbus):
    '''This function creates a new user in the database'''
    print 'inicio create _user'
    uid=uuid.uuid4()
    salt='$6$'+str(uid).split('-')[1]+'$'
    hpassword=crypt.crypt(password,salt)
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
            cassapi.remove_user(userinfo,session)
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
    
