#coding:utf-8
'''

authorization.py

Authorization Exceptions

@author: jcazor
@date: 2013/12/08
'''

class AuthorizationException(Exception):
    pass

class RequestNotFoundException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class DatasourceNotFoundException(Exception):
    pass

