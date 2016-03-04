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

def agent_authenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        agent=self.get_secure_cookie('komlog_agent')
        if not agent:
            logger.logger.debug(str(method.__name__)+' no encontramos la cabecera komlog_agent')
            logger.logger.debug('cerramos la conexion')
            self.close(code=4003,reason='auth required')
        else:
            self.agent=agent.decode('utf-8')
            logger.logger.debug('Agent obtained: '+self.agent)
            return method(self, *args, **kwargs)
    return authlogic
