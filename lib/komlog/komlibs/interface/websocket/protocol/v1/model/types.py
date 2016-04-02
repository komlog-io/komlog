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
class Message(str, Enum):
    SEND_DS_DATA='send_ds_data'

# OPERATION TYPES

@unique
class Operation(AutoEnum):
    NEW_DATASOURCE = ()
