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
    quo_daily_datasource_occupation          = ()
    quo_daily_user_datasources_occupation    = ()
    quo_agent_total_datapoints               = ()
    quo_agent_total_datasources              = ()
    quo_circle_total_members                 = ()
    quo_datasource_total_datapoints          = ()
    quo_user_total_agents                    = ()
    quo_user_total_circles                   = ()
    quo_user_total_dashboards                = ()
    quo_user_total_datapoints                = ()
    quo_user_total_datasources               = ()
    quo_user_total_snapshots                 = ()
    quo_user_total_widgets                   = ()
    quo_user_total_occupation                = ()

