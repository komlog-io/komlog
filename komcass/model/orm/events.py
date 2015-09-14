'''

@author: komlog crew
'''

from komcass.model.parametrization.events import types

class UserEvent:
    def __init__(self, uid, date, priority, type):
        self.uid=uid
        self.date=date
        self.priority=priority
        self.type=type

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

class UserEventInterventionDatapointIdentification(UserEvent):
    def __init__(self, uid, date, priority, did, ds_date, doubts, discarded):
        self.did=did
        self.ds_date=ds_date
        self.doubts=doubts
        self.discarded=discarded
        super(UserEventInterventionDatapointIdentification, self).__init__(uid=uid, date=date, priority=priority, type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)

