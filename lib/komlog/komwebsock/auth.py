'''
This file implements some methods for agent authentication

@date: 2016/02/29
@author: jcazor
'''

import functools, json
from komlog.komlibs.auth import passport
from komlog.komfig import logger

def agent_authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        try:
            cookie=json.loads(self.get_secure_cookie('kid').decode('utf-8'))
            self.passport=passport.get_agent_passport(cookie=cookie)
        except Exception:
            self.clear_cookie('kid')
            self.close(code=4003,reason='auth required')
            return
        else:
            return method(self, *args, **kwargs)
    return authlogic

