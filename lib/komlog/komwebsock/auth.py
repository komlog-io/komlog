'''
This file implements some methods for agent authentication

@date: 2016/02/29
@author: jcazor
'''

import time
import functools, json
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.auth import passport
from komlog.komlibs.interface.websocket.protocol.v1 import status
from komlog.komfig import logging

def agent_authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        try:
            cookie=json.loads(self.get_secure_cookie('kid').decode('utf-8'))
            self.passport=passport.get_agent_passport(cookie=cookie)
        except cassexcept.KomcassException as e:
            now=time.time()
            logging.c_logger.info(','.join(('komlog.komwebsock.auth.agent_authenticated',e.error.name,str(now),str(now))))
            self.close(code=status.SERVICE_UNAVAILABLE)
        except Exception:
            self.close(code=status.ACCESS_DENIED,reason='access denied')
            return
        else:
            return method(self, *args, **kwargs)
    return authlogic

