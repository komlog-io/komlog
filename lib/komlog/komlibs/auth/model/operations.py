'''
This file declares the different auth operations that can be processed.

We define an operation as the result of a system/user request. So an operation differs
from a request in that the operation is something the system did, and a request is something
the system has received but is not done yet

'''

from enum import Enum, unique

class AutoEnum(Enum):
    def __new__(cls):
        value = len(cls.__members__)+1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

@unique
class Operations(AutoEnum):
    DATASOURCE_DATA_STORED               = ()
    DELETE_AGENT                         = ()
    DELETE_CIRCLE                        = ()
    DELETE_DASHBOARD                     = ()
    DELETE_DATASOURCE                    = ()
    DELETE_DATASOURCE_DATAPOINT          = ()
    DELETE_SNAPSHOT                      = ()
    DELETE_USER                          = ()
    DELETE_USER_DATAPOINT                = ()
    DELETE_WIDGET                        = ()
    DISSOCIATE_DATAPOINT_FROM_DATASOURCE = ()
    UPDATE_CIRCLE_MEMBERS                = ()
    NEW_AGENT                            = ()
    NEW_CIRCLE                           = ()
    NEW_DASHBOARD                        = ()
    NEW_DATASOURCE                       = ()
    NEW_DATASOURCE_DATAPOINT             = ()
    NEW_SNAPSHOT                         = ()
    NEW_USER                             = ()
    NEW_USER_DATAPOINT                   = ()
    NEW_WIDGET                           = ()
    NEW_WIDGET_SYSTEM                    = ()

