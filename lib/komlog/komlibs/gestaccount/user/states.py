'''
This file contains the multiple states a user can be

creation date: 2013/03/31
author: jcazor
'''

from enum import Enum

class UserStates(int, Enum):
    PREACTIVE = 0
    ACTIVE    = 1

class InvitationStates(int, Enum):
    UNUSED = 0
    USING  = 1
    USED   = 2

class InvitationRequestStates(int, Enum):
    REGISTERED = 0
    ASSOCIATED = 1
    SENT       = 2

class ForgetRequestStates(int, Enum):
    UNUSED = 0
    USED   = 1

