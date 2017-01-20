'''
This file implements some methods for user and agent
authentication and authorization

2013/08/13
jcazor
'''

import time
import jwt
import functools, json
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.auth import passport
from komlog.komlibs.interface.web import status
from komlog.komws2.settings import SETTINGS
from komlog.komfig import logging

def authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        try:
            token=self.get_secure_cookie('kid').decode('utf-8')
            cookie = decryptCookie(token)
            self.passport=passport.get_user_passport(cookie=cookie)
        except cassexcept.KomcassException as e:
            now=time.time()
            logging.c_logger.info(','.join(('komlog.komws2.auth.authenticated',e.error.name,str(now),str(now))))
            self.set_status(status.WEB_STATUS_SERVICE_UNAVAILABLE)
            self.finish()
        except Exception as e:
            url = self.get_login_url()
            self.clear_cookie('kid')
            self.redirect(url)
            return
        else:
            return method(self, *args, **kwargs)
    return authlogic


def encryptCookie(cookie):
    return jwt.encode(cookie, SETTINGS['jwt_secret'], algorithm='HS256')

def decryptCookie(token):
    return jwt.decode(token, SETTINGS['jwt_secret'], algorithms=['HS256'])

