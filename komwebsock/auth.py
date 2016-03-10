'''
This file implements some methods for agent authentication

@date: 2016/02/29
@author: jcazor
'''

import tornado.web
import functools
import urllib.parse
from urllib.parse import urlencode
from komfig import logger

def authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        kid=self.get_secure_cookie('kid')
        if not kid:
            self.close(code=4003,reason='auth required')
            return
        else:
            try:
                kid=json.loads(kid.decode('utf-8'))
                self.user=kid['user']
                self.agent=kid['agent']
            except Exception:
                return
            else:
                return method(self, *args, **kwargs)
    return authlogic

