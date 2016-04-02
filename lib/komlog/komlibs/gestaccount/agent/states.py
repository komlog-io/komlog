'''
This file contains the multiple states an agent can be

creation date: 2013/03/31
author: jcazor
'''

from enum import Enum

class AgentStates(int, Enum):
    PENDING_USER_VALIDATION  =   1 #: agent needs to be validated on creation.
    ACTIVE                   =   2 #: Active state.Usually agents will be created in this state.
    SUSPENDED                =   3 #: Suspended. Agent can't do things like upload info, login, etc.

