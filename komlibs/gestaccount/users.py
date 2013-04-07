'''
users.py: library for managing administrative user operations

creation date: 2013/03/31
author: jcazor
'''

import uuid,crypt
from datetime import datetime
from komcass import api as cassapi
from komlibs.gestaccount import states as states


def create_user(username, password, segment, session):
    '''This function creates a new user in the database'''
    uid=uuid.uuid4()
    salt='$6$'+str(uid).split('-')[1]+'$'
    hpassword=crypt.crypt(password,salt)
    now=datetime.utcnow()
    userinfo=cassapi.UserInfo(uid=uid, username=username, password=hpassword, segment=segment, creation_date=now, state=states.USER['ACTIVE'])
    if cassapi.register_user(userinfo,session):
        return True
    else:
        return False


