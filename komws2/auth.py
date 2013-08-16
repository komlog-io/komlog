#coding: utf-8
'''
This file implements some methods for user and agent
authentication and authorization

2013/08/13
jcazor
'''

import functools
import urlparse
from urllib import urlencode

def userauthenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        self.user=self.get_secure_cookie("komlog_user")
        print 'Usuario obtenido: ',
        print self.user
        if not self.user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return authlogic

def agentauthenticated(method):
    @functools.wraps(method)
    def authlogic(self,*args,**kwargs):
        self.agent=self.get_secure_cookie("komlog_agent")
        if not self.agent:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
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
