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

class AuthorizationExpiredException(AuthException):
    def __init__(self, error):
        super(AuthorizationExpiredException,self).__init__(error=error)

class BadParametersException(AuthException):
    def __init__(self, error):
        super(BadParametersException, self).__init__(error=error)

class RequestNotFoundException(AuthException):
    def __init__(self, error):
        super(RequestNotFoundException,self).__init__(error=error)

class UserNotFoundException(AuthException):
    def __init__(self, error):
        super(UserNotFoundException,self).__init__(error=error)

class AgentNotFoundException(AuthException):
    def __init__(self, error):
        super(AgentNotFoundException,self).__init__(error=error)

class DatasourceNotFoundException(AuthException):
    def __init__(self, error):
        super(DatasourceNotFoundException,self).__init__(error=error)

class TicketCreationException(AuthException):
    def __init__(self, error):
        super(TicketCreationException, self).__init__(error=error)

class CookieException(AuthException):
    def __init__(self, error):
        super(CookieException, self).__init__(error=error)

class PassportException(AuthException):
    def __init__(self, error):
        super(PassportException, self).__init__(error=error)

