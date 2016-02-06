'''

@author: komlog crew
'''

import json
from komcass.model.parametrization.events import types

class UserEvent:
    def __init__(self, uid, date, priority, type):
        self.uid=uid
        self.date=date
        self.priority=priority
        self.type=type

class UserEventGraphSummary:
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
    def __init__(self, uid, date, priority, did, ds_date, doubts, discarded):
        self.did=did
        self.ds_date=ds_date
        self.doubts=doubts if doubts else set()
        self.discarded=discarded if discarded else set()
        super(UserEventInterventionDatapointIdentification, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)


##### RESPONSES 


class UserEventResponse:
    def __init__(self, uid, date, response_date, type):
        self.uid=uid
        self.date=date
        self.response_date=response_date
        self.type=type

class UserEventResponseInterventionDatapointIdentification(UserEventResponse):
    def __init__(self, uid, date, response_date, missing=None, identified=None, not_belonging=None, to_update=None, update_failed=None, update_success=None):
        self.missing=missing if missing else set()
        self.identified=identified if identified else dict()
        self.not_belonging=not_belonging if not_belonging else set()
        self.to_update=to_update if to_update else set()
        self.update_failed=update_failed if update_failed else set()
        self.update_success=update_success if update_success else set()
        super(UserEventResponseInterventionDatapointIdentification, self).__init__(uid=uid, date=date, response_date=response_date, type=types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)

