#coding:utf-8
'''

authorization.py

Authorization Exceptions

@author: jcazor
@date: 2013/12/08
'''

class AuthException(Exception):
    def __init__(self, error=None):
        self.error=error

class AuthorizationException(AuthException):
    def __init__(self):
        super(AuthorizationException,self).__init__()

class RequestNotFoundException(AuthException):
    def __init__(self):
        super(RequestNotFoundException,self).__init__()

class UserNotFoundException(AuthException):
    def __init__(self):
        super(UserNotFoundException,self).__init__()

class DatasourceNotFoundException(AuthException):
    def __init__(self):
        super(DatasourceNotFoundException,self).__init__()

