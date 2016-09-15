'''

@author: komlog crew
'''

import json
from komlog.komcass.model.parametrization.events import types

class UserEvent:
    def __init__(self, uid, date, priority, type):
        self.uid=uid
        self.date=date
        self.priority=priority
        self.type=type

class UserEventDataSummary:
    def __init__(self, uid, date, summary=None):
        self.uid=uid
        self.date=date
        self.summary=json.loads(summary) if isinstance(summary,str) else summary

class UserEventNotificationNewUser(UserEvent):
    def __init__(self, uid, date, priority, username):
        self.username=username
        super(UserEventNotificationNewUser, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_USER)

class UserEventNotificationNewAgent(UserEvent):
    def __init__(self, uid, date, priority, aid, agentname):
        self.aid=aid
        self.agentname=agentname
        super(UserEventNotificationNewAgent, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_AGENT)

class UserEventNotificationNewDatasource(UserEvent):
    def __init__(self, uid, date, priority, aid, did, datasourcename):
        self.aid=aid
        self.did=did
        self.datasourcename=datasourcename
        super(UserEventNotificationNewDatasource, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)

class UserEventNotificationNewDatapoint(UserEvent):
    def __init__(self, uid, date, priority, did, pid, datasourcename, datapointname):
        self.did=did
        self.pid=pid
        self.datasourcename=datasourcename
        self.datapointname=datapointname
        super(UserEventNotificationNewDatapoint, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)

class UserEventNotificationNewWidget(UserEvent):
    def __init__(self, uid, date, priority, wid, widgetname):
        self.wid=wid
        self.widgetname=widgetname
        super(UserEventNotificationNewWidget, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET)

class UserEventNotificationNewDashboard(UserEvent):
    def __init__(self, uid, date, priority, bid, dashboardname):
        self.bid=bid
        self.dashboardname=dashboardname
        super(UserEventNotificationNewDashboard, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)

class UserEventNotificationNewCircle(UserEvent):
    def __init__(self, uid, date, priority, cid, circlename):
        self.cid=cid
        self.circlename=circlename
        super(UserEventNotificationNewCircle, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE)

class UserEventNotificationNewSnapshotShared(UserEvent):
    def __init__(self, uid, date, priority, nid, tid, widgetname, shared_with_users, shared_with_circles):
        self.nid=nid
        self.tid=tid
        self.widgetname=widgetname
        self.shared_with_users=shared_with_users
        self.shared_with_circles=shared_with_circles
        super(UserEventNotificationNewSnapshotShared, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)

class UserEventNotificationNewSnapshotSharedWithMe(UserEvent):
    def __init__(self, uid, date, priority, nid, tid, username, widgetname):
        self.nid=nid
        self.tid=tid
        self.username=username
        self.widgetname=widgetname
        super(UserEventNotificationNewSnapshotSharedWithMe, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)

class UserEventInterventionDatapointIdentification(UserEvent):
    def __init__(self, uid, date, priority, pid, datasourcename, datapointname):
        self.pid=pid
        self.datasourcename=datasourcename
        self.datapointname=datapointname
        super(UserEventInterventionDatapointIdentification, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)


##### RESPONSES 


class UserEventResponse:
    def __init__(self, uid, date, response_date, type):
        self.uid=uid
        self.date=date
        self.response_date=response_date
        self.type=type

class UserEventResponseInterventionDatapointIdentification(UserEventResponse):
    def __init__(self, uid, date, response_date, data):
        self.data=data
        super(UserEventResponseInterventionDatapointIdentification, self).__init__(uid=uid, date=date, response_date=response_date, type=types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)

