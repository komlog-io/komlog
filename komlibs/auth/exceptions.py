#coding:utf-8
'''

authorization.py

Authorization Exceptions

@author: jcazor
@date: 2013/12/08
'''

class AuthException(Exception):
    def __init__(self, error):
        self.error=error

class AuthorizationException(AuthException):
    def __init__(self, error):
        super(AuthorizationException,self).__init__(error=error)

class RequestNotFoundException(AuthException):
    def __init__(self, error):
        super(RequestNotFoundException,self).__init__(error=error)

class UserNotFoundException(AuthException):
    def __init__(self, error):
        super(UserNotFoundException,self).__init__(error=error)

class DatasourceNotFoundException(AuthException):
    def __init__(self, error):
        super(DatasourceNotFoundException,self).__init__(error=error)

