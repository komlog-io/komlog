import unittest
import time
import uuid
import random
from komlibs.general.time import timeuuid
from komcass.api import events as eventsapi
from komcass.model.orm import events as ormevents
from komcass.model.parametrization.events import types
from komcass.model.statement import events as stmtevents
from komcass import connection
from komfig import logger


class KomcassApiEventsTest(unittest.TestCase):
    ''' komlog.komcass.api.events tests '''

    def setUp(self):
        pass

    def test_get_user_event_non_existing_uid(self):
        ''' get_user_event should return None if uid does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(eventsapi.get_user_event(uid=uid, date=date))

    def test_get_user_event_non_existing_date(self):
        ''' get_user_event should return None if event at the specified date does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_get_user_event_non_existing_date'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        new_date=timeuuid.uuid1()
        self.assertIsNone(eventsapi.get_user_event(uid=uid, date=new_date))

    def test_get_user_event_success_user_event_notification_new_user(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_get_user_event_success_user_event_notification_new_user'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.username,db_user_event.username)

    def test_get_user_event_success_user_event_notification_new_agent(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        agentname='test_get_user_event_success_user_event_notification_new_agent'
        event=ormevents.UserEventNotificationNewAgent(uid=uid,date=date, priority=1,aid=aid,agentname=agentname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_AGENT)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.aid,db_user_event.aid)
        self.assertEqual(event.agentname,db_user_event.agentname)

    def test_get_user_event_success_user_event_notification_new_datasource(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_get_user_event_success_user_event_notification_new_datasource'
        event=ormevents.UserEventNotificationNewDatasource(uid=uid,date=date, priority=1,aid=aid, did=did, datasourcename=datasourcename)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.aid,db_user_event.aid)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.datasourcename,db_user_event.datasourcename)

    def test_get_user_event_success_user_event_notification_new_datapoint(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_get_user_event_success_user_event_notification_new_datapoint'
        datapointname='test_get_user_event_success_user_event_notification_new_datapoint'
        event=ormevents.UserEventNotificationNewDatapoint(uid=uid,date=date, priority=1,did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.pid,db_user_event.pid)
        self.assertEqual(event.datasourcename,db_user_event.datasourcename)
        self.assertEqual(event.datapointname,db_user_event.datapointname)

    def test_get_user_event_success_user_event_notification_new_widget(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        date=timeuuid.uuid1()
        widgetname='test_get_user_event_success_user_event_notification_new_widget'
        event=ormevents.UserEventNotificationNewWidget(uid=uid,date=date, priority=1,wid=wid,widgetname=widgetname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_WIDGET)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.wid,db_user_event.wid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)

    def test_get_user_event_success_user_event_notification_new_dashboard(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        date=timeuuid.uuid1()
        dashboardname='test_get_user_event_success_user_event_notification_new_dashboard'
        event=ormevents.UserEventNotificationNewDashboard(uid=uid,date=date, priority=1,bid=bid,dashboardname=dashboardname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.bid,db_user_event.bid)
        self.assertEqual(event.dashboardname,db_user_event.dashboardname)

    def test_get_user_event_success_user_event_notification_new_circle(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        date=timeuuid.uuid1()
        circlename='test_get_user_event_success_user_event_notification_new_circle'
        event=ormevents.UserEventNotificationNewCircle(uid=uid,date=date, priority=1,cid=cid,circlename=circlename)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_CIRCLE)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.cid,db_user_event.cid)
        self.assertEqual(event.circlename,db_user_event.circlename)

    def test_get_user_event_success_user_event_notification_new_snapshot_shared(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        widgetname='test_get_user_event_success_user_event_notification_new_snapshot_shared'
        shared_with_users={uuid.uuid4():'username1',uuid.uuid4():'username3'}
        shared_with_circles={uuid.uuid4():'circlename1',uuid.uuid4():'circlename5'}
        date=timeuuid.uuid1()
        event=ormevents.UserEventNotificationNewSnapshotShared(uid=uid,date=date, priority=1,nid=nid,tid=tid,widgetname=widgetname,shared_with_users=shared_with_users,shared_with_circles=shared_with_circles)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.nid,db_user_event.nid)
        self.assertEqual(event.tid,db_user_event.tid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)
        self.assertEqual(event.shared_with_users,db_user_event.shared_with_users)
        self.assertEqual(event.shared_with_circles,db_user_event.shared_with_circles)

    def test_get_user_event_success_user_event_notification_new_snapshot_shared_with_me(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        widgetname='test_get_user_event_success_user_event_notification_new_snapshot_shared'
        username='test_get_user_event_success_user_event_notification_new_snapshot_shared_username'
        date=timeuuid.uuid1()
        event=ormevents.UserEventNotificationNewSnapshotSharedWithMe(uid=uid,date=date, priority=1,nid=nid,tid=tid,widgetname=widgetname,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.nid,db_user_event.nid)
        self.assertEqual(event.tid,db_user_event.tid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)
        self.assertEqual(event.username,db_user_event.username)

    def test_get_user_event_success_user_event_intervention_datapoint_identification(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        discarded=[uuid.uuid4(), uuid.uuid4()]
        doubts=[uuid.uuid4(), uuid.uuid4()]
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid,date=date, priority=1,did=did, ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.ds_date,db_user_event.ds_date)
        self.assertEqual(sorted(event.doubts),sorted(db_user_event.doubts))
        self.assertEqual(sorted(event.discarded),sorted(db_user_event.discarded))

    def test_get_disabled_user_event_non_existing_uid(self):
        ''' get_disabled_user_event should return None if uid does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(eventsapi.get_disabled_user_event(uid=uid, date=date))

    def test_get_disabled_user_event_non_existing_date(self):
        ''' get_disabled_user_event should return None if event at the specified date does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_get_disabled_user_event_non_existing_date'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        new_date=timeuuid.uuid1()
        self.assertIsNone(eventsapi.get_disabled_user_event(uid=uid, date=new_date))

    def test_get_disabled_user_event_failure_event_is_enabled(self):
        ''' get_disabled_user_event should return None if event exists but is enabled '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_get_disabled_user_event_enabled'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertIsNone(eventsapi.get_disabled_user_event(uid=uid, date=date))

    def test_get_disabled_user_event_success_user_event_notification_new_user(self):
        ''' get_disabled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_get_disabled_user_event_success_user_event_notification_new_user'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.username,db_user_event.username)

    def test_get_disabled_user_event_success_user_event_notification_new_agent(self):
        ''' get_disabled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        agentname='test_get_disabled_user_event_success_user_event_notification_new_agent'
        event=ormevents.UserEventNotificationNewAgent(uid=uid,date=date, priority=1,aid=aid,agentname=agentname)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_AGENT)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.aid,db_user_event.aid)
        self.assertEqual(event.agentname,db_user_event.agentname)

    def test_get_disabled_user_event_success_user_event_notification_new_datasource(self):
        ''' get_disabled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_get_disabled_user_event_success_user_event_notification_new_datasource'
        event=ormevents.UserEventNotificationNewDatasource(uid=uid,date=date, priority=1,aid=aid, did=did, datasourcename=datasourcename)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.aid,db_user_event.aid)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.datasourcename,db_user_event.datasourcename)

    def test_get_disabled_user_event_success_user_event_notification_new_datapoint(self):
        ''' get_disabled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_get_disabled_user_event_success_user_event_notification_new_datapoint'
        datapointname='test_get_disabled_user_event_success_user_event_notification_new_datapoint'
        event=ormevents.UserEventNotificationNewDatapoint(uid=uid,date=date, priority=1,did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.pid,db_user_event.pid)
        self.assertEqual(event.datasourcename,db_user_event.datasourcename)
        self.assertEqual(event.datapointname,db_user_event.datapointname)

    def test_get_disabled_user_event_success_user_event_notification_new_widget(self):
        ''' get_disabled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        date=timeuuid.uuid1()
        widgetname='test_get_disabled_user_event_success_user_event_notification_new_widget'
        event=ormevents.UserEventNotificationNewWidget(uid=uid,date=date, priority=1,wid=wid,widgetname=widgetname)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_WIDGET)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.wid,db_user_event.wid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)

    def test_get_disabled_user_event_success_user_event_notification_new_dashboard(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        date=timeuuid.uuid1()
        dashboardname='test_get_disabled_user_event_success_user_event_notification_new_dashboard'
        event=ormevents.UserEventNotificationNewDashboard(uid=uid,date=date, priority=1,bid=bid,dashboardname=dashboardname)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.bid,db_user_event.bid)
        self.assertEqual(event.dashboardname,db_user_event.dashboardname)

    def test_get_disabled_user_event_success_user_event_notification_new_circle(self):
        ''' get_disasbled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        date=timeuuid.uuid1()
        circlename='test_get_disabled_user_event_success_user_event_notification_new_circle'
        event=ormevents.UserEventNotificationNewCircle(uid=uid,date=date, priority=1,cid=cid,circlename=circlename)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_CIRCLE)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.cid,db_user_event.cid)
        self.assertEqual(event.circlename,db_user_event.circlename)

    def test_get_disabled_user_event_success_user_event_notification_new_snapshot_shared(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        widgetname='test_get_user_event_success_user_event_notification_new_snapshot_shared'
        shared_with_users={uuid.uuid4():'username1',uuid.uuid4():'username3'}
        shared_with_circles={uuid.uuid4():'circlename1',uuid.uuid4():'circlename5'}
        date=timeuuid.uuid1()
        event=ormevents.UserEventNotificationNewSnapshotShared(uid=uid,date=date, priority=1,nid=nid,tid=tid,widgetname=widgetname,shared_with_users=shared_with_users,shared_with_circles=shared_with_circles)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.nid,db_user_event.nid)
        self.assertEqual(event.tid,db_user_event.tid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)
        self.assertEqual(event.shared_with_users,db_user_event.shared_with_users)
        self.assertEqual(event.shared_with_circles,db_user_event.shared_with_circles)

    def test_get_disabled_user_event_success_user_event_notification_new_snapshot_shared_with_me(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        widgetname='test_get_user_event_success_user_event_notification_new_snapshot_shared'
        username='test_get_user_event_success_user_event_notification_new_snapshot_shared_username'
        date=timeuuid.uuid1()
        event=ormevents.UserEventNotificationNewSnapshotSharedWithMe(uid=uid,date=date, priority=1,nid=nid,tid=tid,widgetname=widgetname,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.nid,db_user_event.nid)
        self.assertEqual(event.tid,db_user_event.tid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)
        self.assertEqual(event.username,db_user_event.username)

    def test_get_disabled_user_event_success_user_event_intervention_datapoint_identification(self):
        ''' get_disabled_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        discarded=[uuid.uuid4(), uuid.uuid4()]
        doubts=[uuid.uuid4(), uuid.uuid4()]
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid,date=date, priority=1,did=did, ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(eventsapi.insert_user_event(event))
        self.assertTrue(eventsapi.disable_user_event(event))
        db_user_event=eventsapi.get_disabled_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.ds_date,db_user_event.ds_date)
        self.assertEqual(sorted(event.doubts),sorted(db_user_event.doubts))
        self.assertEqual(sorted(event.discarded),sorted(db_user_event.discarded))

    def test_get_user_events_non_existing_uid(self):
        ''' get_user_events should return an empty array if uid does not exist '''
        uid=uuid.uuid4()
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=1000
        self.assertEqual(eventsapi.get_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_user_events_non_existing_user_events_in_date_interval(self):
        ''' get_user_events should return an empty array if no event at the specified interval exists '''
        uid=uuid.uuid4()
        username='test_get_user_events_non_existing_user_events_in_date_interval'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())-50)
        count=1000
        self.assertEqual(eventsapi.get_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_user_events_success(self):
        ''' get_user_events should return an array with the events '''
        uid=uuid.uuid4()
        username='test_get_user_events_success'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=1000
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=count)
        self.assertEqual(len(events),9)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEvent))
            self.assertTrue(isinstance(event, ormevents.UserEventNotificationNewUser))

    def test_get_user_events_success_limit_count(self):
        ''' get_user_events should return an array with the events limited by the counter variable'''
        uid=uuid.uuid4()
        username='test_get_user_events_success_limit_count'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=5
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=count)
        self.assertEqual(len(events),count)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEventNotificationNewUser))
            self.assertTrue(isinstance(event, ormevents.UserEvent))

    def test_get_disabled_user_events_non_existing_uid(self):
        ''' get_disabled_user_events should return an empty array if uid does not exist '''
        uid=uuid.uuid4()
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=1000
        self.assertEqual(eventsapi.get_disabled_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_disabled_user_events_non_existing_user_events_in_date_interval(self):
        ''' get_disabled_user_events should return an empty array if no event at the specified interval exists '''
        uid=uuid.uuid4()
        username='test_get_disabled_user_events_non_existing_user_events_in_date_interval'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
            self.assertTrue(eventsapi.disable_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())-50)
        count=1000
        self.assertEqual(eventsapi.get_disabled_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_disabled_user_events_non_existing_user_events_all_enabled(self):
        ''' get_disabled_user_events should return an empty array if no event at the specified interval exists '''
        uid=uuid.uuid4()
        username='test_get_disabled_user_events_non_existing_user_events_all_enabled'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())-50)
        count=1000
        self.assertEqual(eventsapi.get_disabled_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_disabled_user_events_success(self):
        ''' get_disabled_user_events should return an array with the events '''
        uid=uuid.uuid4()
        username='test_get_disabled_user_events_success'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
            self.assertTrue(eventsapi.disable_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=1000
        events=eventsapi.get_disabled_user_events(uid=uid, end_date=end_date, count=count)
        self.assertEqual(len(events),9)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEvent))
            self.assertTrue(isinstance(event, ormevents.UserEventNotificationNewUser))

    def test_get_disabled_user_events_success_limit_count(self):
        ''' get_disabled_user_events should return an array with the events limited by the counter variable'''
        uid=uuid.uuid4()
        username='test_get_disabled_user_events_success_limit_count'
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=username)
            self.assertTrue(eventsapi.insert_user_event(event))
            self.assertTrue(eventsapi.disable_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=5
        events=eventsapi.get_disabled_user_events(uid=uid, end_date=end_date, count=count)
        self.assertEqual(len(events),count)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEventNotificationNewUser))
            self.assertTrue(isinstance(event, ormevents.UserEvent))

    def test__get_user_event_failure_non_UserEvent_instance(self):
        ''' _get_user_event should return None if object passed is not a UserEvent instance '''
        events=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2')]
        for event in events:
            self.assertIsNone(eventsapi._get_user_event(event))

    def test__get_user_event_failure_invalid_event_type(self):
        ''' _get_user_event should return None if event type is not valid '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid,date=date, priority=1,type=9999999999)
        self.assertIsNone(eventsapi._get_user_event(event))

    def test_insert_user_event_failure_non_UserEvent_instance(self):
        ''' insert_user_event should return False if event is not an instance of UserEvent '''
        events=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2')]
        for event in events:
            self.assertFalse(eventsapi.insert_user_event(event))

    def test_insert_user_event_failure_invalid_event_type(self):
        ''' _get_user_event should return None if event type is not valid '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid,date=date, priority=1,type=9999999999)
        self.assertFalse(eventsapi.insert_user_event(event))

    def test_insert_user_event_success_user_event_notification_new_user(self):
        ''' insert_user_event should succeed if event is an UserEvent instance '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_insert_user_event_success'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date,priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)
        self.assertEqual(db_user_event.type, types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(event.username, db_user_event.username)

    def test_insert_user_event_success_user_event_notification_new_agent(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        agentname='test_insert_user_event_success_user_event_notification_new_agent'
        event=ormevents.UserEventNotificationNewAgent(uid=uid,date=date, priority=1,aid=aid,agentname=agentname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_AGENT)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.aid,db_user_event.aid)
        self.assertEqual(event.agentname,db_user_event.agentname)

    def test_insert_user_event_success_user_event_notification_new_datasource(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_insert_user_event_success_user_event_notification_new_datasource'
        event=ormevents.UserEventNotificationNewDatasource(uid=uid,date=date, priority=1,aid=aid, did=did, datasourcename=datasourcename)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.aid,db_user_event.aid)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.datasourcename,db_user_event.datasourcename)

    def test_insert_user_event_success_user_event_notification_new_datapoint(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_insert_user_event_success_user_event_notification_new_datapoint'
        datapointname='test_insert_user_event_success_user_event_notification_new_datapoint'
        event=ormevents.UserEventNotificationNewDatapoint(uid=uid,date=date, priority=1,did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.pid,db_user_event.pid)
        self.assertEqual(event.datasourcename,db_user_event.datasourcename)
        self.assertEqual(event.datapointname,db_user_event.datapointname)

    def test_insert_user_event_success_user_event_notification_new_widget(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        date=timeuuid.uuid1()
        widgetname='test_insert_user_event_success_user_event_notification_new_widget'
        event=ormevents.UserEventNotificationNewWidget(uid=uid,date=date, priority=1,wid=wid,widgetname=widgetname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_WIDGET)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.wid,db_user_event.wid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)

    def test_insert_user_event_success_user_event_notification_new_dashboard(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        date=timeuuid.uuid1()
        dashboardname='test_insert_user_event_success_user_event_notification_new_dashboard'
        event=ormevents.UserEventNotificationNewDashboard(uid=uid,date=date, priority=1,bid=bid,dashboardname=dashboardname)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.bid,db_user_event.bid)
        self.assertEqual(event.dashboardname,db_user_event.dashboardname)

    def test_insert_user_event_success_user_event_notification_new_circle(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        date=timeuuid.uuid1()
        circlename='test_insert_user_event_success_user_event_notification_new_circle'
        event=ormevents.UserEventNotificationNewCircle(uid=uid,date=date, priority=1,cid=cid,circlename=circlename)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_CIRCLE)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.cid,db_user_event.cid)
        self.assertEqual(event.circlename,db_user_event.circlename)

    def test_insert_user_event_success_user_event_notification_new_snapshot_shared(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        widgetname='test_get_user_event_success_user_event_notification_new_snapshot_shared'
        shared_with_users={uuid.uuid4():'username1',uuid.uuid4():'username3'}
        shared_with_circles={uuid.uuid4():'circlename1',uuid.uuid4():'circlename5'}
        date=timeuuid.uuid1()
        event=ormevents.UserEventNotificationNewSnapshotShared(uid=uid,date=date, priority=1,nid=nid,tid=tid,widgetname=widgetname,shared_with_users=shared_with_users,shared_with_circles=shared_with_circles)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.nid,db_user_event.nid)
        self.assertEqual(event.tid,db_user_event.tid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)
        self.assertEqual(event.shared_with_users,db_user_event.shared_with_users)
        self.assertEqual(event.shared_with_circles,db_user_event.shared_with_circles)

    def test_insert_user_event_success_user_event_notification_new_snapshot_shared_with_me(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        widgetname='test_get_user_event_success_user_event_notification_new_snapshot_shared'
        username='test_get_user_event_success_user_event_notification_new_snapshot_shared_username'
        date=timeuuid.uuid1()
        event=ormevents.UserEventNotificationNewSnapshotSharedWithMe(uid=uid,date=date, priority=1,nid=nid,tid=tid,widgetname=widgetname,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.nid,db_user_event.nid)
        self.assertEqual(event.tid,db_user_event.tid)
        self.assertEqual(event.widgetname,db_user_event.widgetname)
        self.assertEqual(event.username,db_user_event.username)

    def test_insert_user_event_success_user_event_intervention_datapoint_identification(self):
        ''' insert_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        discarded=[uuid.uuid4(), uuid.uuid4()]
        doubts=[uuid.uuid4(), uuid.uuid4()]
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid,date=date, priority=1,did=did, ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.type,types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.did,db_user_event.did)
        self.assertEqual(event.ds_date,db_user_event.ds_date)
        self.assertEqual(sorted(event.doubts),sorted(db_user_event.doubts))
        self.assertEqual(sorted(event.discarded),sorted(db_user_event.discarded))

    def test_delete_user_events_success(self):
        ''' delete_user_events should True and delete all the user events '''
        uid=uuid.uuid4()
        dates=[]
        name='name'
        num_events=0
        for i in range(1,50):
            for j in [types.USER_EVENT_NOTIFICATION_NEW_USER, types.USER_EVENT_NOTIFICATION_NEW_AGENT, types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE, types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT, types.USER_EVENT_NOTIFICATION_NEW_WIDGET, types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD, types.USER_EVENT_NOTIFICATION_NEW_CIRCLE, types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED, types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME]:
                date=timeuuid.uuid1()
                if j==types.USER_EVENT_NOTIFICATION_NEW_USER:
                    event=ormevents.UserEventNotificationNewUser(uid=uid,date=date, priority=1,username=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_AGENT:
                    event=ormevents.UserEventNotificationNewAgent(uid=uid,date=date, priority=1,aid=uuid.uuid4(), agentname=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:
                    event=ormevents.UserEventNotificationNewDatasource(uid=uid,date=date, priority=1,aid=uuid.uuid4(), did=uuid.uuid4(), datasourcename=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:
                    event=ormevents.UserEventNotificationNewDatapoint(uid=uid,date=date, priority=1,did=uuid.uuid4(), pid=uuid.uuid4(), datasourcename=name, datapointname=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_WIDGET:
                    event=ormevents.UserEventNotificationNewWidget(uid=uid,date=date, priority=1,wid=uuid.uuid4(), widgetname=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:
                    event=ormevents.UserEventNotificationNewCircle(uid=uid,date=date, priority=1,cid=uuid.uuid4(), circlename=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:
                    event=ormevents.UserEventNotificationNewDashboard(uid=uid,date=date, priority=1,bid=uuid.uuid4(), dashboardname=name)
                elif j==types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION:
                    event=ormevents.UserEventNotificationNewDashboard(uid=uid,date=date, priority=1,bid=uuid.uuid4(), dashboardname=name)
                elif j==types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:
                    event=ormevents.UserEventNotificationNewSnapshotShared(uid=uid,date=date, priority=1,nid=uuid.uuid4(), tid=uuid.uuid4(), widgetname=name, shared_with_users={}, shared_with_circles={})
                elif j==types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:
                    event=ormevents.UserEventNotificationNewSnapshotSharedWithMe(uid=uid,date=date, priority=1,nid=uuid.uuid4(), tid=uuid.uuid4(), widgetname=name, username=name)
                self.assertTrue(eventsapi.insert_user_event(event))
                dates.append(date)
                num_events+=1
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=1000)
        self.assertEqual(len(events),num_events)
        old_num_events=num_events
        for i,event in enumerate(events):
            if i==0 or random.random()<=0.4:
                self.assertTrue(eventsapi.disable_user_event(event))
                num_events-=1
        self.assertTrue(old_num_events>num_events)
        self.assertTrue(eventsapi.delete_user_events(uid=uid))
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=1000)
        self.assertEqual(events,[])
        for date in dates:
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUSEREVENTS_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUSEREVENTSDISABLED_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWUSER_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWAGENT_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDATASOURCE_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDATAPOINT_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWWIDGET_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWDASHBOARD_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWCIRCLE_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWSNAPSHOTSHARED_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUENOTIFNEWSNAPSHOTSHAREDWITHME_B_UID_DATE,(uid,date)),[])
            self.assertEqual(connection.session.execute(stmtevents.S_A_DATUEINTERVDPIDENTIFICATION_B_UID_DATE,(uid,date)),[])

    def test_enable_user_event_failure_non_UserEvent_instance(self):
        ''' enable_user_event should fail if event is not a UserEvent instance '''
        events=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2')]
        for event in events:
            self.assertFalse(eventsapi.enable_user_event(event))

    def test_enable_user_event_failure_non_existent_event(self):
        ''' enable_user_event should fail if event does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid, date=date, priority=1, type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertFalse(eventsapi.enable_user_event(event))

    def test_disable_user_event_failure_non_UserEvent_instance(self):
        ''' disable_user_event should fail if event is not a UserEvent instance '''
        events=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2')]
        for event in events:
            self.assertFalse(eventsapi.disable_user_event(event))

    def test_disable_user_event_failure_non_existent_event(self):
        ''' disable_user_event should fail if event does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid, date=date, priority=1, type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertFalse(eventsapi.disable_user_event(event))

    def test_enable_disable_user_event_success(self):
        ''' enable_user_event and disable_user_event should succeed '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_enable_user_event_success'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date,priority=1,username=username)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)
        self.assertEqual(types.USER_EVENT_NOTIFICATION_NEW_USER, db_user_event.type)
        self.assertEqual(event.username, db_user_event.username)
        self.assertTrue(eventsapi.disable_user_event(db_user_event))
        self.assertIsNone(eventsapi.get_user_event(uid=uid,date=date))
        self.assertTrue(eventsapi.enable_user_event(db_user_event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)
        self.assertEqual(types.USER_EVENT_NOTIFICATION_NEW_USER, db_user_event.type)
        self.assertEqual(event.username, db_user_event.username)

    def test_get_user_event_responses_failure_non_event_instance(self):
        ''' get_user_event_responses should return an empty array if no event instance is passed '''
        events=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2')]
        for event in events:
            self.assertEqual(eventsapi.get_user_event_responses(event),[])

    def test_get_user_event_responses_failure_non_supported_event(self):
        ''' get_user_event_responses should return an empty array if event type is not supported '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_get_user_event_responses_failure'
        event=ormevents.UserEventNotificationNewUser(uid=uid,date=date,priority=1,username=username)
        self.assertEqual(eventsapi.get_user_event_responses(event),[])

    def test_get_user_event_responses_success_some_responses_found(self):
        ''' get_user_event_responses should return an array with the responses '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        discarded=[uuid.uuid4(), uuid.uuid4()]
        doubts=[uuid.uuid4(), uuid.uuid4()]
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid,date=date, priority=1,did=did, ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(eventsapi.insert_user_event(event))
        response1=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=date, response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response1))
        response2=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=date, response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response2))
        responses=eventsapi.get_user_event_responses(event=event)
        self.assertEqual(len(responses),2)
        for response in responses:
            self.assertTrue(isinstance(response, ormevents.UserEventResponseInterventionDatapointIdentification))

    def test__get_user_event_responses_intervention_datapoint_identification_success_some_responses_found(self):
        ''' _get_user_event_responses_intervention_datapoint_identification should return an array with the responses '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        discarded=[uuid.uuid4(), uuid.uuid4()]
        doubts=[uuid.uuid4(), uuid.uuid4()]
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid,date=date, priority=1,did=did, ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(eventsapi.insert_user_event(event))
        response1=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=date, response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response1))
        response2=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=date, response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response2))
        responses=eventsapi._get_user_event_responses_intervention_datapoint_identification(event=event)
        self.assertEqual(len(responses),2)
        for response in responses:
            self.assertTrue(isinstance(response, ormevents.UserEventResponseInterventionDatapointIdentification))

    def test_get_user_events_responses_intervention_datapoint_identification_success_some_responses_found(self):
        ''' get_user_events_responses_intervention_datapoint_identification should return an array with the responses '''
        uid=uuid.uuid4()
        response1=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=timeuuid.uuid1(), response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response1))
        response2=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=timeuuid.uuid1(), response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response2))
        responses=eventsapi.get_user_events_responses_intervention_datapoint_identification(uid=uid)
        self.assertEqual(len(responses),2)
        for response in responses:
            self.assertTrue(isinstance(response, ormevents.UserEventResponseInterventionDatapointIdentification))

    def test_insert_user_event_response_failure_non_response_instance(self):
        ''' insert_user_event_responses should return an empty array if no response instance is passed '''
        responses=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2'),ormevents.UserEvent(uid=uuid.uuid4(), date=timeuuid.uuid1(),priority=1,type=0)]
        for response in responses:
            self.assertFalse(eventsapi.insert_user_event_response(response))

    def test_insert_user_event_response_failure_non_supported_response(self):
        ''' insert_user_event_response should return an empty array if response type is not supported '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        response_date=timeuuid.uuid1()
        type=11000000
        response=ormevents.UserEventResponse(uid=uid,date=date,response_date=response_date, type=type)
        self.assertFalse(eventsapi.insert_user_event_response(response))

    def test_insert_user_event_response_success(self):
        ''' insert_user_event_response should succeed '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        response=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=date, response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response))

    def test__insert_user_event_response_intervention_datapoint_identification_success(self):
        ''' _insert_user_event_response should succeed '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        response=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=date, response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi._insert_user_event_response_intervention_datapoint_identification(response))

    def test_delete_user_events_responses_intervention_datapoint_identification_success_some_responses_found(self):
        ''' get_user_events_responses_intervention_datapoint_identification should return an array with the responses '''
        uid=uuid.uuid4()
        response1=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=timeuuid.uuid1(), response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response1))
        response2=ormevents.UserEventResponseInterventionDatapointIdentification(uid=uid, date=timeuuid.uuid1(), response_date=timeuuid.uuid1())
        self.assertTrue(eventsapi.insert_user_event_response(response2))
        responses=eventsapi.get_user_events_responses_intervention_datapoint_identification(uid=uid)
        self.assertEqual(len(responses),2)
        for response in responses:
            self.assertTrue(isinstance(response, ormevents.UserEventResponseInterventionDatapointIdentification))
        self.assertTrue(eventsapi.delete_user_events_responses_intervention_datapoint_identification(uid=uid))
        responses=eventsapi.get_user_events_responses_intervention_datapoint_identification(uid=uid)
        self.assertEqual(len(responses),0)


