#coding: utf-8
'''
This file implements some methods for user and agent
authentication and authorization

2013/08/13
jcazor
'''

import tornado.web
import functools
import urllib.parse
from urllib.parse import urlencode
from komfig import logger

def userauthenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        user=self.get_secure_cookie("komlog_user")
        if not user:
            if self.request.method in ('GET','HEAD','PUT','POST'):
                url = self.get_login_url()
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
        self.user=user.decode('utf-8')
        logger.logger.debug('User obtained: '+self.user)
        return method(self, *args, **kwargs)
    return authlogic

def agentauthenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        agent=self.get_secure_cookie("komlog_agent")
        user=self.get_secure_cookie("komlog_user")
        if not agent or not user:
            if self.request.method in ('GET','HEAD','PUT','POST'):
                url = self.get_login_url()
                if "?" not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        self.agent=agent.decode('utf-8')
        self.user=user.decode('utf-8')
        logger.logger.debug('User obtained: '+self.user)
        logger.logger.debug('Agent obtained: '+self.agent)
        return method(self, *args, **kwargs)
    return authlogic

def userauthorized(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        pass
    return authlogic

def agentauthorized(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        pass
    return authlogic
