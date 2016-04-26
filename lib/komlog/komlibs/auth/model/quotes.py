'''
In this file we declare the different quotes that
can be checked in the system
'''

from enum import Enum

class AutoEnum(Enum):
    def __new__(cls):
        value = len(cls.__members__)+1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

class Quotes(AutoEnum):
    quo_static_agent_max_datapoints          = ()
    quo_static_agent_max_datasources         = ()
    quo_static_agent_total_datapoints        = ()
    quo_static_agent_total_datasources       = ()
    quo_static_circle_max_members            = ()
    quo_static_circle_total_members          = ()
    quo_static_datasource_max_datapoints     = ()
    quo_static_datasource_total_datapoints   = ()
    quo_static_user_max_agents               = ()
    quo_static_user_max_circles              = ()
    quo_static_user_max_dashboards           = ()
    quo_static_user_max_datapoints           = ()
    quo_static_user_max_datasources          = ()
    quo_static_user_max_snapshots            = ()
    quo_static_user_max_widgets              = ()
    quo_static_user_total_agents             = ()
    quo_static_user_total_circles            = ()
    quo_static_user_total_dashboards         = ()
    quo_static_user_total_datapoints         = ()
    quo_static_user_total_datasources        = ()
    quo_static_user_total_snapshots          = ()
    quo_static_user_total_widgets            = ()
