'''
This file declares the different auth operations that can be processed.

We define an operation as the result of a system/user request. So an operation differs
from a request in that the operation is something the system did, and a request is something
the system has received but is not done yet

'''

from enum import Enum

class Operations(Enum):
    NEW_AGENT                            = 0
    NEW_DATASOURCE                       = 1
    NEW_DATASOURCE_DATAPOINT             = 2
    NEW_WIDGET                           = 3
    NEW_DASHBOARD                        = 4
    NEW_WIDGET_SYSTEM                    = 5
    NEW_SNAPSHOT                         = 6
    NEW_CIRCLE                           = 7
    DELETE_USER                          = 8
    DELETE_AGENT                         = 9
    DELETE_DATASOURCE                    = 10
    DELETE_DATAPOINT                     = 11
    DELETE_WIDGET                        = 12
    DELETE_DASHBOARD                     = 13
    DELETE_SNAPSHOT                      = 14
    DELETE_CIRCLE                        = 15
    UPDATE_CIRCLE_MEMBERS                = 16
    DATASOURCE_DATA_STORED               = 17
    NEW_USER                             = 18
    NEW_USER_DATAPOINT                   = 19
    DISSOCIATE_DATAPOINT_FROM_DATASOURCE = 20

