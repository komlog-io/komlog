import unittest
import time
import uuid
from komlibs.general.time import timeuuid
from komcass.api import events as eventsapi
from komcass.model.orm import events as ormevents
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
        event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
        self.assertTrue(eventsapi.insert_user_event(event))
        new_date=timeuuid.uuid1()
        self.assertIsNone(eventsapi.get_user_event(uid=uid, date=new_date))

    def test_get_user_event_success(self):
        ''' get_user_event should succeed if event exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertIsNotNone(db_user_event)
        self.assertEqual(event.uid,db_user_event.uid)
        self.assertEqual(event.date,db_user_event.date)
        self.assertEqual(event.priority,db_user_event.priority)
        self.assertEqual(event.active,db_user_event.active)
        self.assertEqual(event.type,db_user_event.type)
        self.assertEqual(event.parameters,db_user_event.parameters)

    def test_get_user_events_non_existing_uid(self):
        ''' get_user_events should return an empty array if uid does not exist '''
        uid=uuid.uuid4()
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=1000
        self.assertEqual(eventsapi.get_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_user_events_non_existing_user_events_in_date_interval(self):
        ''' get_user_events should return an empty array if no event at the specified interval exists '''
        uid=uuid.uuid4()
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())-50)
        count=1000
        self.assertEqual(eventsapi.get_user_events(uid=uid, end_date=end_date, count=count),[])

    def test_get_user_events_success(self):
        ''' get_user_events should return an array with the events '''
        uid=uuid.uuid4()
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=1000
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=count)
        self.assertEqual(len(events),9)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEvent))

    def test_get_user_events_success_limit_count(self):
        ''' get_user_events should return an array with the events limited by the counter variable'''
        uid=uuid.uuid4()
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        count=8
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=count)
        self.assertEqual(len(events),count)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEvent))

    def test_insert_user_event_failure_non_UserEvent_instance(self):
        ''' insert_user_event should return False if event is not an instance of UserEvent '''
        events=[None,23, '23423',uuid.uuid4(),{'dict':'dict'},{'set'},['list'],('tuple','tuple2')]
        for event in events:
            self.assertFalse(eventsapi.insert_user_event(event))

    def test_insert_user_event_success(self):
        ''' insert_user_event should succeed if event is an UserEvent instance '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(event.active, db_user_event.active)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)

    def test_delete_user_events_success(self):
        ''' delete_user_events should True and delete all the user events '''
        uid=uuid.uuid4()
        for i in range(1,10):
            date=timeuuid.uuid1()
            event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
            self.assertTrue(eventsapi.insert_user_event(event))
        end_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(timeuuid.uuid1())+5)
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=1000)
        self.assertEqual(len(events),9)
        for event in events:
            self.assertTrue(isinstance(event, ormevents.UserEvent))
        self.assertTrue(eventsapi.delete_user_events(uid=uid))
        events=eventsapi.get_user_events(uid=uid, end_date=end_date, count=1000)
        self.assertEqual(events,[])

    def test_activate_user_event_success(self):
        ''' activate_user_event should succeed and set the active flag to True '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid,date=date, active=False,priority=1,type=0)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(event.active, db_user_event.active)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)
        self.assertTrue(eventsapi.activate_user_event(uid=uid, date=date))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(True, db_user_event.active)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)

    def test_deactivate_user_event_success(self):
        ''' deactivate_user_event should succeed and set the active flag to False '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        event=ormevents.UserEvent(uid=uid,date=date, active=True,priority=1,type=0)
        self.assertTrue(eventsapi.insert_user_event(event))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(event.active, db_user_event.active)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)
        self.assertTrue(eventsapi.deactivate_user_event(uid=uid, date=date))
        db_user_event=eventsapi.get_user_event(uid=uid, date=date)
        self.assertEqual(event.uid, db_user_event.uid)
        self.assertEqual(event.date, db_user_event.date)
        self.assertEqual(False, db_user_event.active)
        self.assertEqual(event.priority, db_user_event.priority)
        self.assertEqual(event.type, db_user_event.type)

