'''

authorization.py

Authorization Exceptions

@author: jcazor
@date: 2013/12/08
'''

class AuthException(Exception):
    def __init__(self, error, data=None):
        self.error=error
        self.data=data

class AuthorizationException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class AuthorizationExpiredException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class BadParametersException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class RequestNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class UserNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class AgentNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class TicketCreationException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class CookieException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class PassportException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class IntervalBoundsException(AuthException):
    def __init__(self, error, data):
        super().__init__(error=error, data=data)

class SessionNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

class CircleNotFoundException(AuthException):
    def __init__(self, error):
        super().__init__(error=error)

