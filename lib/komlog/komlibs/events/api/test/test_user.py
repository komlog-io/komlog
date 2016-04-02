import unittest
import uuid
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komlibs.auth.tickets import provision as ticketapi
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komlibs.gestaccount.snapshot import api as snapshotapi
from komlog.komlibs.events.api import user as eventsuser
from komlog.komlibs.events.model import types, priorities
from komlog.komlibs.events import exceptions, errors
from komlog.komfig import logger

class EventsApiUserTest(unittest.TestCase):
    ''' komlibs.events.api.user tests '''

    def test_get_event_failure_invalid_uid(self):
        ''' get_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=timeuuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.get_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_GEV_IU)

    def test_get_event_failure_invalid_date(self):
        ''' get_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.get_event(uid=uid, date=date )
            self.assertEqual(cm.exception.error, errors.E_EAU_GEV_IDT)

    def test_get_event_failure_non_existent_event(self):
        ''' get_event should fail event does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.EventNotFoundException) as cm:
            eventsuser.get_event(uid=uid, date=date )
        self.assertEqual(cm.exception.error, errors.E_EAU_GEV_EVNF)

    def test_get_event_success_new_user(self):
        ''' get_event should succeed returning the event '''
        username='test_get_event_success_new_user'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(db_event['parameters'],{'username':username})

    def test_get_event_success_notification_new_agent(self):
        ''' get_event should return the event '''
        username='test_get_event_new_agent_success'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_get_event_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        self.assertIsNotNone(agent)
        parameters={'aid':agent['aid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_AGENT)
        self.assertEqual(db_event['parameters'],{'aid':agent['aid'],'agentname':agentname})

    def test_get_event_success_new_datasource(self):
        ''' get_event should return the event '''
        username='test_get_event_new_datasource_success'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_get_event_new_datasource_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_get_event_new_datasource_success_datasource'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],pubkey=pubkey,agentname=agentname,version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        parameters={'did':datasource['did'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)
        self.assertEqual(db_event['parameters'],{'did':datasource['did'],'aid':agent['aid'],'datasourcename':datasourcename})

    def test_get_event_success_new_datapoint(self):
        ''' get_event should return the event '''
        username='test_get_event_new_datapoint_success'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_get_event_new_datapoint_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_get_event_new_datapoint_success_datasource'
        datapointname='test_get_event_new_datapoint_success_datapoint'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],pubkey=pubkey,agentname=agentname,version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname,color='#AAAAAA')
        self.assertIsNotNone(datapoint)
        parameters={'pid':datapoint['pid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)
        self.assertEqual(db_event['parameters'],{'did':datasource['did'],'pid':datapoint['pid'],'datasourcename':datasourcename,'datapointname':datapointname})

    def test_get_event_success_new_widget(self):
        ''' get_event should return the event '''
        username='test_get_event_new_widget_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        agentname='test_get_event_new_widget_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_get_event_new_widget_success_datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(widget)
        parameters={'wid':widget['wid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_WIDGET)
        self.assertEqual(db_event['parameters'],{'wid':widget['wid'],'widgetname':datasourcename})

    def test_get_event_success_new_dashboard(self):
        ''' get_event should return the event '''
        username='test_get_event_new_dashboard_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        dashboardname='test_get_event_new_dashboard_success'
        dashboard=dashboardapi.create_dashboard(uid=user['uid'],dashboardname=dashboardname)
        self.assertIsNotNone(dashboard)
        parameters={'bid':dashboard['bid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)
        self.assertEqual(db_event['parameters'],{'bid':dashboard['bid'],'dashboardname':dashboardname})

    def test_get_event_success_new_circle(self):
        ''' get_event should return the event '''
        username='test_get_event_new_circle_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        circlename='test_get_event_new_circle_success'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertIsNotNone(circle)
        parameters={'cid':circle['cid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_CIRCLE)
        self.assertEqual(db_event['parameters'],{'cid':circle['cid'],'circlename':circlename})

    def test_get_event_success_new_intervention_datapoint_identification(self):
        ''' get_event should return the event '''
        username='test_get_event_intervention_datapoint_identirication'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        agentname='test_get_event_intervention_datapoint_identification_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_get_event_intervention_datapoint_identification_success_datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='datasource content'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        parameters={'did':datasource['did'].hex,'date':date.hex,'doubts':doubts,'discarded':discarded}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        self.assertTrue(isinstance(db_event, dict))
        self.assertEqual(db_event['parameters']['did'],datasource['did'])
        self.assertEqual(db_event['parameters']['ds_seq'],timeuuid.get_custom_sequence(date))
        self.assertEqual(sorted(db_event['parameters']['doubts']),sorted([uuid.UUID(pid) for pid in doubts]))
        self.assertEqual(sorted(db_event['parameters']['discarded']),sorted([uuid.UUID(pid) for pid in discarded]))

    def test_get_event_success_notification_new_snapshot_shared(self):
        ''' get_event should return the event '''
        username='test_get_event_notification_new_snapshot_shared_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_get_event_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_get_event_datasource'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(widget)
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1())
        self.assertIsNotNone(snapshot)
        ticket=ticketapi.new_snapshot_ticket(uid=user['uid'],nid=snapshot['nid'], allowed_uids={uuid.uuid4()})
        self.assertIsNotNone(ticket)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nid=snapshot['nid']
        tid=ticket['tid']
        parameters={'tid':tid.hex,'nid':nid.hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_events=eventsuser.get_events(uid=user['uid'])
        self.assertEqual(len(db_events),1)
        self.assertEqual(db_events[0]['uid'],user['uid'])
        self.assertEqual(db_events[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(db_events[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename})

    def test_get_event_success_new_notification_new_snapshot_shared_with_me(self):
        ''' get_event should return the event '''
        username='test_get_event_notification_new_snapshot_shared_success_with_sharing_users'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        user1=userapi.create_user(username=username+'1', password=password, email='1'+email)
        user2=userapi.create_user(username=username+'2', password=password, email='2'+email)
        user3=userapi.create_user(username=username+'3', password=password, email='3'+email)
        user4=userapi.create_user(username=username+'4', password=password, email='4'+email)
        user5=userapi.create_user(username=username+'5', password=password, email='5'+email)
        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)
        self.assertIsNotNone(user3)
        self.assertIsNotNone(user4)
        self.assertIsNotNone(user5)
        circle_members=[username+'2',username+'3',username+'4']
        circle=circleapi.new_users_circle(uid=user['uid'],circlename='circle',members_list=circle_members)
        self.assertIsNotNone(circle)
        agentname='test_get_event_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_get_event_datasource'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(widget)
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1())
        self.assertIsNotNone(snapshot)
        ticket=ticketapi.new_snapshot_ticket(uid=user['uid'],nid=snapshot['nid'], allowed_uids={user1['uid']},allowed_cids={circle['cid']})
        self.assertIsNotNone(ticket)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nid=snapshot['nid']
        tid=ticket['tid']
        parameters={'tid':tid.hex,'nid':nid.hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_events=eventsuser.get_events(uid=user['uid'])
        self.assertEqual(len(db_events),1)
        self.assertEqual(db_events[0]['uid'],user['uid'])
        self.assertEqual(db_events[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(db_events[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename})
        user1_event=eventsuser.get_events(uid=user1['uid'])
        self.assertEqual(len(user1_event),1)
        self.assertEqual(user1_event[0]['uid'],user1['uid'])
        self.assertEqual(user1_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user1_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user2_event=eventsuser.get_events(uid=user2['uid'])
        self.assertEqual(len(user2_event),1)
        self.assertEqual(user2_event[0]['uid'],user2['uid'])
        self.assertEqual(user2_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user2_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user3_event=eventsuser.get_events(uid=user3['uid'])
        self.assertEqual(len(user3_event),1)
        self.assertEqual(user3_event[0]['uid'],user3['uid'])
        self.assertEqual(user3_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user3_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user4_event=eventsuser.get_events(uid=user4['uid'])
        self.assertEqual(len(user4_event),1)
        self.assertEqual(user4_event[0]['uid'],user4['uid'])
        self.assertEqual(user4_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user4_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user5_event=eventsuser.get_events(uid=user5['uid'])
        self.assertEqual(len(user5_event),0)

    def test_get_events_failure_invalid_uid(self):
        ''' get_events should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.get_events(uid=uid)
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_IU)

    def test_get_events_failure_invalid_to_date(self):
        ''' get_events should fail if to_date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.get_events(uid=uid, to_date=date )
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_ITD)

    def test_get_events_failure_invalid_from_date(self):
        ''' get_events should fail if from_date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.get_events(uid=uid, from_date=date )
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_IFD)

    def test_get_events_failure_invalid_count(self):
        ''' get_events should fail if count is invalid '''
        counts=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for count in counts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.get_events(uid=uid, count=count)
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_ICNT)

    def test_get_events_success(self):
        ''' get_events should return the event list '''
        username='test_get_events_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)
        db_events=eventsuser.get_events(uid=user['uid'])
        self.assertIsNotNone(db_events)
        self.assertEqual(len(db_events),1)
        self.assertEqual(db_events[0]['uid'],user['uid'])
        self.assertEqual(db_events[0]['date'],event['date'])
        self.assertEqual(db_events[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(db_events[0]['parameters'],{'username':username})

    def test_enable_event_failure_invalid_uid(self):
        ''' enable_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=uuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.enable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_ENE_IU)

    def test_enable_event_failure_invalid_date(self):
        ''' enable_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.enable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_ENE_ID)

    def test_enable_event_failure_non_existent_event(self):
        ''' enable_event should fail if event does not exist '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        with self.assertRaises(exceptions.EventNotFoundException) as cm:
            eventsuser.enable_event(uid=uid, date=date)
        self.assertEqual(cm.exception.error, errors.E_EAU_ENE_EVNF)

    def test_enable_event_success_event_enabled_previously(self):
        ''' enable_event should succeed if event is enabled previously '''
        username='test_enable_event_success_event_enabled_previously'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(db_event['parameters'],{'username':username})
        self.assertTrue(eventsuser.enable_event(uid=user['uid'],date=event['date']))

    def test_disable_event_failure_invalid_uid(self):
        ''' disable_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=uuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.disable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_DISE_IU)

    def test_disable_event_failure_invalid_date(self):
        ''' disable_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.disable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_DISE_ID)

    def test_disable_event_failure_non_existent_event(self):
        ''' disable_event should fail if event does not exist '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        with self.assertRaises(exceptions.EventNotFoundException) as cm:
            eventsuser.disable_event(uid=uid, date=date)
        self.assertEqual(cm.exception.error, errors.E_EAU_DISE_EVNF)

    def test_disable_event_success_event_disabled_previously(self):
        ''' enable_event should succeed if event is enabled previously '''
        username='test_disable_event_success_event_disabled_previously'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(db_event['parameters'],{'username':username})
        self.assertTrue(eventsuser.disable_event(uid=user['uid'],date=event['date']))
        self.assertTrue(eventsuser.disable_event(uid=user['uid'],date=event['date']))

    def test_enable_disable_event_success(self):
        ''' enable_event and disable_event should succeed '''
        username='test_enable_disable_event_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)
        db_event=eventsuser.get_event(uid=user['uid'],date=event['date'])
        self.assertIsNotNone(db_event)
        self.assertEqual(db_event['uid'],user['uid'])
        self.assertEqual(db_event['date'],event['date'])
        self.assertEqual(db_event['type'],types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(db_event['parameters'],{'username':username})
        self.assertTrue(eventsuser.disable_event(uid=user['uid'],date=event['date']))
        self.assertTrue(eventsuser.disable_event(uid=user['uid'],date=event['date']))

    def test_delete_events_failure_invalid_uid(self):
        ''' delete_events should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.delete_events(uid=uid)
            self.assertEqual(cm.exception.error, errors.E_EAU_DEV_IU)

    def test_delete_events_success(self):
        ''' delete_events should succeed '''
        username='test_delete_events_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)
        db_events=eventsuser.get_events(uid=user['uid'])
        self.assertIsNotNone(db_events)
        self.assertEqual(len(db_events),1)
        self.assertTrue(eventsuser.delete_events(uid=user['uid']))
        db_events=eventsuser.get_events(uid=user['uid'])
        self.assertIsNotNone(db_events)
        self.assertEqual(len(db_events),0)

    def test_new_event_failure_invalid_event_type(self):
        ''' new_event should fail if type is invalid  '''
        event_types=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        parameters={}
        for event_type in event_types:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_IEVT)

    def test_new_event_failure_non_existent_event_type(self):
        ''' new_event should fail if type is invalid  '''
        event_type=234234
        uid=uuid.uuid4()
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_EVTNF)

    def test_new_event_new_user_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNU_IU)

    def test_new_event_new_user_failure_non_existent_user(self):
        ''' new_event should fail if type is NEW_USER and no user does not exist '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        parameters={}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNU_UNF)

    def test_new_event_new_user_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_user_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event=eventsuser.new_event(uid=user['uid'],parameters={},event_type=types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertIsNotNone(event)

    def test_new_event_new_agent_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNA_IU)

    def test_new_event_new_agent_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNA_IP)

    def test_new_event_new_agent_failure_no_aid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and no aid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNA_IPAID)

    def test_new_event_new_agent_failure_invalid_aid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        aids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for aid in aids:
            parameters={'aid':aid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNA_IPAID)

    def test_new_event_new_agent_failure_non_existent_user(self):
        ''' new_event should fail if event_type is NEW_AGENT and user does not exist '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNA_UNF)

    def test_new_event_new_agent_failure_non_existent_agent(self):
        ''' new_event should fail if event_type is NEW_AGENT and agent does not exist '''
        username='test_new_event_new_agent_failure_non_existent_agent'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':uuid.uuid4().hex}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNA_ANF)

    def test_new_event_new_agent_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_agent_success'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_new_event_new_agent_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        self.assertIsNotNone(agent)
        parameters={'aid':agent['aid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_new_datasource_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDS_IU)

    def test_new_event_new_datasource_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDS_IP)

    def test_new_event_new_datasource_failure_non_did_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and no did parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDS_IPDID)

    def test_new_event_new_datasource_failure_invalid_did_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        aids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for aid in aids:
            parameters={'aid':aid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDS_IPDID)

    def test_new_event_new_datasource_failure_non_existent_user(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and user does not exist '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={'did':uuid.uuid4().hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDS_UNF)

    def test_new_event_new_datasource_failure_non_existent_datasource(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and datasource does not exist '''
        username='test_new_event_new_datasource_failure_non_existent_datasource'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={'did':uuid.uuid4().hex}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDS_DNF)

    def test_new_event_new_datasource_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_datasource_success'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_new_event_new_datasource_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_new_datasource_success_datasource'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],pubkey=pubkey,agentname=agentname,version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        parameters={'did':datasource['did'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_new_datapoint_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_IU)

    def test_new_event_new_datapoint_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_IP)

    def test_new_event_new_datapoint_failure_non_pid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and no pid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_IPPID)

    def test_new_event_new_datapoint_failure_invalid_pid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and pid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        pids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for pid in pids:
            parameters={'pid':pid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_IPPID)

    def test_new_event_new_datapoint_failure_non_existent_user(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and user does not exist '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={'pid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_UNF)

    def test_new_event_new_datapoint_failure_non_existent_datapoint(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and datasource does not exist '''
        username='test_new_event_new_datapoint_failure_non_existent_datapoint'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={'pid':uuid.uuid4().hex}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_PNF)

    def test_new_event_new_datapoint_failure_non_existent_datasource(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and datapoint does not exist '''
        username='test_new_event_new_datapoint_failure_non_existent_datasource'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_new_event_new_datapoint_failure_non_existent_datasource_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_new_datapoint_failure_non_existent_datasource'
        datapointname='test_new_event_new_datapoint_failure_non_existent_datasource'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],pubkey=pubkey,agentname=agentname,version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname,color='#AAAAAA')
        self.assertIsNotNone(datapoint)
        parameters={'pid':datapoint['pid'].hex}
        self.assertTrue(cassapidatasource.delete_datasource(did=datasource['did']))
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDP_DNF)

    def test_new_event_new_datapoint_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_datapoint_success'
        password='temporal'
        email=username+'@komlog.org'
        agentname='test_new_event_new_datapoint_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_new_datapoint_success_datasource'
        datapointname='test_new_event_new_datapoint_success_datapoint'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],pubkey=pubkey,agentname=agentname,version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname,color='#AAAAAA')
        self.assertIsNotNone(datapoint)
        parameters={'pid':datapoint['pid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_new_widget_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNWG_IU)

    def test_new_event_new_widget_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNWG_IP)

    def test_new_event_new_widget_failure_non_wid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and no wid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNWG_IPWID)

    def test_new_event_new_widget_failure_invalid_wid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and wid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        wids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for wid in wids:
            parameters={'wid':wid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNWG_IPWID)

    def test_new_event_new_widget_failure_non_existent_user(self):
        ''' new_event should fail if event_type is NEW_WIDGET and widget does not exist '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={'wid':wid.hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNWG_UNF)

    def test_new_event_new_widget_failure_non_existent_widget(self):
        ''' new_event should fail if event_type is NEW_WIDGET and widget does not exist '''
        username='test_new_event_new_widget_failure_non_existent_widget'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={'wid':uuid.uuid4().hex}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNWG_WNF)

    def test_new_event_new_widget_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_widget_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        agentname='test_new_event_new_widget_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_new_widget_success_datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(widget)
        parameters={'wid':widget['wid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_new_dashboard_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDB_IU)

    def test_new_event_new_dashboard_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDB_IP)

    def test_new_event_new_dashboard_failure_non_bid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and no bid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDB_IPBID)

    def test_new_event_new_dashboard_failure_invalid_bid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and bid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        bids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for bid in bids:
            parameters={'bid':bid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNDB_IPBID)

    def test_new_event_new_dashboard_failure_non_existent_user(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and user does not exist '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={'bid':bid.hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDB_UNF)

    def test_new_event_new_dashboard_failure_non_existent_dashboard(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and dashboard does not exist '''
        username='test_new_event_new_dashboard_failure_non_existent_dashboard'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={'bid':uuid.uuid4().hex}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNDB_BNF)

    def test_new_event_new_dashboard_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_dashboard_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        dashboardname='test_new_event_new_dashboard_success'
        dashboard=dashboardapi.create_dashboard(uid=user['uid'],dashboardname=dashboardname)
        self.assertIsNotNone(dashboard)
        parameters={'bid':dashboard['bid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_new_circle_failure_invalid_uid(self):
        ''' new_event should fail if type is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNC_IU)

    def test_new_event_new_circle_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNC_IP)

    def test_new_event_new_circle_failure_non_cid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and no cid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNC_IPCID)

    def test_new_event_new_circle_failure_invalid_cid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and cid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        cids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for cid in cids:
            parameters={'cid':cid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNC_IPCID)

    def test_new_event_new_circle_failure_non_existent_user(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and user does not exist '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={'cid':cid.hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNC_UNF)

    def test_new_event_new_circle_failure_non_existent_circle(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and circle does not exist '''
        username='test_new_event_new_circle_failure_non_existent_circle'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={'cid':uuid.uuid4().hex}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNC_CNF)

    def test_new_event_new_circle_success(self):
        ''' new_event should succeed '''
        username='test_new_event_new_circle_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        circlename='test_new_event_new_circle_success'
        circle=circleapi.new_users_circle(uid=user['uid'],circlename=circlename)
        self.assertIsNotNone(circle)
        parameters={'cid':circle['cid'].hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_intervention_datapoint_identification_failure_invalid_uid(self):
        ''' new_event should fail if uid is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IEIDPI_IUID)

    def test_new_event_intervention_datapoint_identification_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is INTERVENTION_DATAPOINT_IDENTIFICATION and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IEIDPI_IP)

    def test_new_event_intervention_datapoint_identification_failure_no_did_parameter_passed(self):
        ''' new_event should fail if event_type is INTERVENTION_DATAPOINT_IDENTIFICATION and no did parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IEIDPI_IPDID)

    def test_new_event_intervention_datapoint_identification_failure_invalid_did_parameter_passed(self):
        ''' new_event should fail if event_type is INTERVENTION_DATAPOINT_IDENTIFICATION and did parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for did in dids:
            parameters={'did':did}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IEIDPI_IPDID)

    def test_new_event_intervention_datapoint_identification_failure_non_existent_user(self):
        ''' new_event should fail if event_type is INTERVENTION_DATAPOINT_IDENTIFICATION and user does not exist '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex,'date':date.hex,'doubts':doubts,'discarded':discarded}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IEIDPI_UNF)

    def test_new_event_intervention_datapoint_identification_failure_non_existent_datasource(self):
        ''' new_event should fail if event_type is INTERVENTION_DATAPOINT_IDENTIFICATION and circle does not exist '''
        username='test_new_event_intervention_datapoint_identirication_failure_non_existent_datasource'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        did=uuid.uuid4()
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        parameters={'did':did.hex,'date':date.hex,'doubts':doubts,'discarded':discarded}
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IEIDPI_DNF)

    def test_new_event_intervention_datapoint_identification_success(self):
        ''' new_event should succeed '''
        username='test_new_event_intervention_datapoint_identirication'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        agentname='test_new_event_intervention_datapoint_identification_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_intervention_datapoint_identification_success_datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='datasource content'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        parameters={'did':datasource['did'].hex,'date':date.hex,'doubts':doubts,'discarded':discarded}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)

    def test_new_event_notification_new_snapshot_shared_failure_invalid_uid(self):
        ''' new_event should fail if uid is invalid  '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        parameters={}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_IU)

    def test_new_event_notification_new_snapshot_shared_failure_invalid_parameters_passed(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and parameters is not a dict '''
        parameterss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_IP)

    def test_new_event_notification_new_snapshot_shared_failure_no_nid_parameter_passed(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and no nid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_IPNID)

    def test_new_event_notification_new_snapshot_shared_failure_invalid_nid_parameter_passed(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and nid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for nid in nids:
            parameters={'nid':nid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_IPNID)

    def test_new_event_notification_new_snapshot_shared_failure_no_tid_parameter_passed(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and no tid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        parameters={'nid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_IPTID)

    def test_new_event_notification_new_snapshot_shared_failure_invalid_tid_parameter_passed(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and tid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        tids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        nid=uuid.uuid4()
        for tid in tids:
            parameters={'tid':tid,'nid':nid.hex}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_IPTID)

    def test_new_event_notification_new_snapshot_shared_failure_user_not_found(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and user does not exist '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        parameters={'tid':tid.hex,'nid':nid.hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_UNF)

    def test_new_event_notification_new_snapshot_shared_failure_snapshot_not_found(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and user does not exist '''
        username='test_new_event_notification_new_snapshot_shared_failure_snapshot_not_found'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nid=uuid.uuid4()
        tid=uuid.uuid4()
        parameters={'tid':tid.hex,'nid':nid.hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_NNF)

    def test_new_event_notification_new_snapshot_shared_failure_ticket_not_found(self):
        ''' new_event should fail if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and user does not exist '''
        username='test_new_event_notification_new_snapshot_shared_failure_ticket_not_found'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_new_event_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_datasource'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(widget)
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1())
        self.assertIsNotNone(snapshot)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nid=snapshot['nid']
        tid=uuid.uuid4()
        parameters={'tid':tid.hex,'nid':nid.hex}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_IENNSS_TNF)

    def test_new_event_notification_new_snapshot_shared_success_insert_to_the_sharing_user_and_circles(self):
        ''' new_event should succeed if event_type is NOTIFICATION_NEW_SNAPSHOT_SHARED and insert the event in the sharing user only, because snapshot is not shared with anyone '''
        username='test_new_event_notification_new_snapshot_shared_success_with_sharing_users'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        user1=userapi.create_user(username=username+'1', password=password, email='1'+email)
        user2=userapi.create_user(username=username+'2', password=password, email='2'+email)
        user3=userapi.create_user(username=username+'3', password=password, email='3'+email)
        user4=userapi.create_user(username=username+'4', password=password, email='4'+email)
        user5=userapi.create_user(username=username+'5', password=password, email='5'+email)
        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)
        self.assertIsNotNone(user3)
        self.assertIsNotNone(user4)
        self.assertIsNotNone(user5)
        circle_members=[username+'2',username+'3',username+'4']
        circle=circleapi.new_users_circle(uid=user['uid'],circlename='circle',members_list=circle_members)
        self.assertIsNotNone(circle)
        agentname='test_new_event_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_new_event_datasource'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(widget)
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1())
        self.assertIsNotNone(snapshot)
        ticket=ticketapi.new_snapshot_ticket(uid=user['uid'],nid=snapshot['nid'], allowed_uids={user1['uid']}, allowed_cids={circle['cid']})
        self.assertIsNotNone(ticket)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED
        nid=snapshot['nid']
        tid=ticket['tid']
        parameters={'tid':tid.hex,'nid':nid.hex}
        event=eventsuser.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_events=eventsuser.get_events(uid=user['uid'])
        self.assertEqual(len(db_events),1)
        self.assertEqual(db_events[0]['uid'],user['uid'])
        self.assertEqual(db_events[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(db_events[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename})
        user1_event=eventsuser.get_events(uid=user1['uid'])
        self.assertEqual(len(user1_event),1)
        self.assertEqual(user1_event[0]['uid'],user1['uid'])
        self.assertEqual(user1_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user1_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user2_event=eventsuser.get_events(uid=user2['uid'])
        self.assertEqual(len(user2_event),1)
        self.assertEqual(user2_event[0]['uid'],user2['uid'])
        self.assertEqual(user2_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user2_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user3_event=eventsuser.get_events(uid=user3['uid'])
        self.assertEqual(len(user3_event),1)
        self.assertEqual(user3_event[0]['uid'],user3['uid'])
        self.assertEqual(user3_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user3_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user4_event=eventsuser.get_events(uid=user4['uid'])
        self.assertEqual(len(user4_event),1)
        self.assertEqual(user4_event[0]['uid'],user4['uid'])
        self.assertEqual(user4_event[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME)
        self.assertEqual(user4_event[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename,'username':username})
        user5_event=eventsuser.get_events(uid=user5['uid'])
        self.assertEqual(len(user5_event),0)

