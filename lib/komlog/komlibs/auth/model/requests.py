'''
In this file we declare the different requests that
can be authorized
'''

from enum import Enum

class AutoEnum(Enum):
    def __new__(cls):
        value = len(cls.__members__)+1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

class Requests(AutoEnum):
    ADD_DATAPOINT_TO_WIDGET        = ()
    ADD_MEMBER_TO_CIRCLE           = ()
    ADD_WIDGET_TO_DASHBOARD        = ()
    DELETE_AGENT                   = ()
    DELETE_CIRCLE                  = ()
    DELETE_DASHBOARD               = ()
    DELETE_DATAPOINT               = ()
    DELETE_DATAPOINT_FROM_WIDGET   = ()
    DELETE_DATASOURCE              = ()
    DELETE_MEMBER_FROM_CIRCLE      = ()
    DELETE_SNAPSHOT                = ()
    DELETE_USER                    = ()
    DELETE_WIDGET                  = ()
    DELETE_WIDGET_FROM_DASHBOARD   = ()
    DISABLE_EVENT                  = ()
    GET_AGENT_CONFIG               = ()
    GET_AGENTS_CONFIG              = ()
    GET_CIRCLE_CONFIG              = ()
    GET_CIRCLES_CONFIG             = ()
    GET_DASHBOARD_CONFIG           = ()
    GET_DASHBOARDS_CONFIG          = ()
    GET_DATAPOINT_CONFIG           = ()
    GET_DATAPOINT_DATA             = ()
    GET_DATASOURCE_CONFIG          = ()
    GET_DATASOURCES_CONFIG         = ()
    GET_DATASOURCE_DATA            = ()
    GET_SNAPSHOT_CONFIG            = ()
    GET_SNAPSHOTS_CONFIG           = ()
    GET_SNAPSHOT_DATA              = ()
    GET_URI                        = ()
    GET_USER_CONFIG                = ()
    GET_USER_EVENTS                = ()
    GET_WIDGET_CONFIG              = ()
    GET_WIDGETS_CONFIG             = ()
    MARK_NEGATIVE_VARIABLE         = ()
    MARK_POSITIVE_VARIABLE         = ()
    NEW_AGENT                      = ()
    NEW_CIRCLE                     = ()
    NEW_DASHBOARD                  = ()
    NEW_DATASOURCE_DATAPOINT       = ()
    NEW_DATASOURCE                 = ()
    NEW_SNAPSHOT                   = ()
    NEW_USER_DATAPOINT             = ()
    NEW_WIDGET                     = ()
    UPDATE_DATASOURCE_CONFIG       = ()
    UPDATE_DATAPOINT_CONFIG        = ()
    UPDATE_AGENT_CONFIG            = ()
    UPDATE_WIDGET_CONFIG           = ()
    UPDATE_DASHBOARD_CONFIG        = ()
    UPDATE_CIRCLE_CONFIG           = ()
    UPDATE_USER_CONFIG             = ()
    POST_DATASOURCE_DATA           = ()
    POST_DATAPOINT_DATA            = ()
    RESPONSE_EVENT                 = ()

