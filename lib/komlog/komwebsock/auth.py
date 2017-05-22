'''
This file implements some methods for agent authentication

@date: 2016/02/29
@author: jcazor
'''

import time
import jwt
import functools, json
import traceback
from komlog.komlibs.auth import passport
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.interface.websocket import status
from komlog.komlibs.interface.websocket.errors import Errors
from komlog.komwebsock.settings import SETTINGS
from komlog.komfig import logging


def agent_authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        try:
            token=self.get_secure_cookie('kid').decode('utf-8')
            cookie = decryptCookie(token)
            self.passport=passport.get_agent_passport(cookie=cookie)
        except authexcept.AuthException as e:
            now=time.time()
            logging.c_logger.info(','.join(('komlog.komwebsock.auth.agent_authenticated',e.error.name,str(now),str(now))))
            self.close(code=status.ACCESS_DENIED, reason='Access denied')
        except AttributeError:
            now=time.time()
            error = Errors.E_KWSKA_AA_AE
            logging.c_logger.info(','.join(('komlog.komwebsock.auth.agent_authenticated',error.name,str(now),str(now))))
            self.close(code=status.ACCESS_DENIED, reason='Access denied')
        except Exception as e:
            now=time.time()
            error = getattr(e,'error',Errors.UNKNOWN)
            logging.c_logger.info(','.join(('komlog.komwebsock.auth.agent_authenticated',error.name,str(now),str(now))))
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            self.close(code=status.SERVICE_UNAVAILABLE)
        else:
            return method(self, *args, **kwargs)
    return authlogic

def agent_active(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        try:
            passport.check_agent_passport_validity(passport=self.passport)
        except authexcept.AuthException as e:
            now=time.time()
            logging.c_logger.info(','.join(('komlog.komwebsock.auth.agent_active',e.error.name,str(now),str(now))))
            self.close(code=status.ACCESS_DENIED, reason='Access denied')
        except Exception as e:
            now=time.time()
            error = getattr(e,'error',Errors.UNKNOWN)
            logging.c_logger.info(','.join(('komlog.komwebsock.auth.agent_active',error.name,str(now),str(now))))
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            self.close(code=status.SERVICE_UNAVAILABLE, reason='Access denied')
        else:
            return method(self, *args, **kwargs)
    return authlogic

def decryptCookie(token):
    return jwt.decode(token, SETTINGS['jwt_secret'], algorithms=['HS256'])

