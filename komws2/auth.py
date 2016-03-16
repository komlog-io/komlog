'''
This file implements some methods for user and agent
authentication and authorization

2013/08/13
jcazor
'''

import functools, json
from komlibs.auth import passport
from komfig import logger

def authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        try:
            cookie=json.loads(self.get_secure_cookie('kid').decode('utf-8'))
            self.passport=passport.get_user_passport(cookie=cookie)
        except Exception as e:
            url = self.get_login_url()
            self.clear_cookie('kid')
            self.redirect(url)
            return
        else:
            return method(self, *args, **kwargs)
    return authlogic

