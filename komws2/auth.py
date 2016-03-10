#coding: utf-8
'''
This file implements some methods for user and agent
authentication and authorization

2013/08/13
jcazor
'''

import json
import uuid
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
            if self.request.method in ('GET','HEAD','PUT','POST'):
                url = self.get_login_url()
                if '?' not in url:
                    if urllib.parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += '?' + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
        try:
            kid=json.loads(kid.decode('utf-8'))
            self.user=kid['user']
            self.agent=kid['agent']
        except Exception as e:
            print(str(e))
            return
        else:
            return method(self, *args, **kwargs)
    return authlogic

