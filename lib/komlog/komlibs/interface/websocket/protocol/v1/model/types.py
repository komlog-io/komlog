'''

This file declare the different message types (actions) supported by the protocol

'''

from enum import Enum, unique

class AutoEnum(Enum):
    def __new__(cls):
        value = len(cls.__members__)+1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

# MESSAGE TYPES

@unique
class Messages(Enum):
    SEND_DS_DATA='send_ds_data'
    SEND_DP_DATA='send_dp_data'
    SEND_MULTI_DATA='send_multi_data'

# OPERATION TYPES

@unique
class Operations(AutoEnum):
    NEW_DATASOURCE          = ()
    NEW_USER_DATAPOINT      = ()
    DATASOURCE_DATA_STORED  = ()


