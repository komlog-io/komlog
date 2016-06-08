'''

This file declare the different operations types

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
    NEW_AGENT                            = ()
    NEW_DATASOURCE                       = ()
    NEW_DATASOURCE_DATAPOINT             = ()
    NEW_WIDGET                           = ()
    NEW_DASHBOARD                        = ()
    NEW_WIDGET_SYSTEM                    = ()
    NEW_SNAPSHOT                         = ()
    NEW_CIRCLE                           = ()
    DELETE_USER                          = ()
    DELETE_AGENT                         = ()
    DELETE_DATASOURCE                    = ()
    DELETE_DATASOURCE_DATAPOINT          = ()
    DELETE_WIDGET                        = ()
    DELETE_DASHBOARD                     = ()
    DELETE_SNAPSHOT                      = ()
    DELETE_CIRCLE                        = ()
    UPDATE_CIRCLE_MEMBERS                = ()
    NEW_USER                             = ()
    DISSOCIATE_DATAPOINT_FROM_DATASOURCE = ()
    DELETE_USER_DATAPOINT                = ()


