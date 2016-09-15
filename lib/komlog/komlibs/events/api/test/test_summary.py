import unittest
import uuid
import decimal
import random
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komlibs.auth.tickets import provision as ticketapi
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.widget import types as widget_types
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komlibs.gestaccount.snapshot import api as snapshotapi
from komlog.komlibs.events.api import summary
from komlog.komlibs.events.api import user as userevents
from komlog.komlibs.events.model import types, priorities
from komlog.komlibs.events import exceptions
from komlog.komlibs.events.errors import Errors
from komlog.komfig import logging

class EventsApiSummaryTest(unittest.TestCase):
    ''' komlibs.events.api.summary tests '''

    def test_get_user_event_data_summary_failure_invalid_uid(self):
        ''' get_user_event_data_summary should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=timeuuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                summary.get_user_event_data_summary(uid=uid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_EAS_GUEDS_IUID)

    def test_get_user_event_data_summary_failure_invalid_date(self):
        ''' get_user_event_data_summary should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                summary.get_user_event_data_summary(uid=uid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_EAS_GUEDS_IDATE)

    def test_get_user_event_data_summary_non_existent_event(self):
        ''' get_user_event_data_summary return None if there is no summary for the event '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(summary.get_user_event_data_summary(uid=uid, date=date))

    def test_get_user_event_data_summary_notification_new_snapshot_shared_ds(self):
        ''' get_user_event_data_summary return the summary of the event '''
        username='test_get_user_event_data_summary_notification_new_snapshot_shared_ds_success'
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
        ds_date=timeuuid.uuid1(seconds=50)
        content='1 datasource content'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=ds_date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=ds_date))
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
        event=userevents.new_event(uid=user['uid'], event_type=event_type, parameters=parameters)
        self.assertIsNotNone(event)
        db_events=userevents.get_events(uid=user['uid'])
        self.assertEqual(len(db_events),1)
        self.assertEqual(db_events[0]['uid'],user['uid'])
        self.assertEqual(db_events[0]['type'],types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED)
        self.assertEqual(db_events[0]['parameters'],{'nid':nid,'tid':tid,'widgetname':datasourcename})
        ev_summary = summary.get_user_event_data_summary(uid=event['uid'],date=event['date'])
        self.assertEqual(ev_summary['type'], widget_types.DATASOURCE)
        self.assertTrue(ev_summary['ts'],timeuuid.get_unix_timestamp(ds_date))
        self.assertTrue(ev_summary['widgetname'], datasourcename)
        self.assertTrue(ev_summary['datasource'], {'content':content})

    def test_get_user_event_data_summary_intervention_datapoint_identification(self):
        ''' get_user_event_data_summary return the summary of the event '''
        username='test_get_user_event_data_summary_intervention_datapoint_identification'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='1 datasource content'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        datapointname='datapoint_name'
        datapoint=datapointapi.monitor_new_datapoint(did=datasource['did'],date=date, position=0, length = 1,datapointname=datapointname)
        parameters={'did':datasource['did'].hex,'dates':[date.hex], 'pid':datapoint['pid'].hex}
        event = userevents.new_event(uid=user['uid'], event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, parameters=parameters)
        self.assertIsNotNone(event)
        ev_summary = summary.get_user_event_data_summary(uid=event['uid'],date=event['date'])
        self.assertEqual(ev_summary,{'data':[{'vars':[[0,1]],'content':content,'ts':timeuuid.get_unix_timestamp(date),'seq':timeuuid.get_custom_sequence(date)}]})

    def test_generate_user_event_data_summary_non_valid_event_type(self):
        ''' generate_user_event_data_summary should return None if event_type is not valid'''
        event_types=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        parameters={}
        for t in event_types:
            self.assertIsNone(summary.generate_user_event_data_summary(event_type=t, parameters=parameters))

    def test_generate_user_event_data_summary_event_type_has_no_summary_defined(self):
        ''' generate_user_event_data_summary should return None if event_type has no summary by default '''
        event_types=[types.USER_EVENT_NOTIFICATION_NEW_USER,types.USER_EVENT_NOTIFICATION_NEW_AGENT,types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE,types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT,types.USER_EVENT_NOTIFICATION_NEW_WIDGET]
        parameters={}
        for t in event_types:
            self.assertIsNone(summary.generate_user_event_data_summary(event_type=t, parameters=parameters))

    def test__generate_data_summary_UENNSS_failure_nid_parameter_not_found(self):
        ''' _generate_data_summary_UENNSS should fail if nid parameter is not found '''
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UENNSS(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUENNSS_NPNF)

    def test__generate_data_summary_UENNSS_failure_invalid_nid_parameter(self):
        ''' _generate_data_summary_UENNSS should fail if nid parameter is not found '''
        nids=[None,234234, 234234.234234, 'astring', uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for nid in nids:
            parameters={'nid':nid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                summary._generate_data_summary_UENNSS(parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUENNSS_INID)

    def test__generate_data_summary_UENNSS_failure_nid_not_found(self):
        ''' _generate_data_summary_UENNSS should fail if snapshot does not exist '''
        parameters={'nid':uuid.uuid4()}
        with self.assertRaises(exceptions.SummaryCreationException) as cm:
            summary._generate_data_summary_UENNSS(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUENNSS_NIDNF)

    def test__generate_data_summary_UENNSS_datasource_empty_no_data_found(self):
        ''' _generate_data_summary_UENNSS should return None if no data is found '''
        username='test__generate_data_summary_uennss_datasource_empty_no_data_found'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], datasource['did'])
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.DATASOURCE)
        self.assertEqual(widget['widgetname'], datasourcename)
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1(seconds=1))
        self.assertIsNotNone(snapshot)
        self.assertIsNone(summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']}))

    def test__generate_data_summary_UENNSS_datasource_success(self):
        ''' _generate_data_summary_UENNSS should return the summary '''
        username='test__generate_data_summary_uennss_datasource_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        for i in range(1,1000):
            date=timeuuid.uuid1(seconds=i)
            content='content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'+str(i)
            self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
            self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], datasource['did'])
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.DATASOURCE)
        self.assertEqual(widget['widgetname'], datasourcename)
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=5), interval_end=timeuuid.uuid1(seconds=100))
        self.assertIsNotNone(snapshot)
        data_summary=summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']})
        self.assertIsNotNone(data_summary)
        self.assertEqual(data_summary['type'], widget_types.DATASOURCE)
        self.assertEqual(data_summary['widgetname'], widget['widgetname'])
        self.assertTrue('content' in data_summary['datasource'])
        self.assertTrue(len(data_summary['datasource']['content'])>0)

    def test__generate_data_summary_UENNSS_datapoint_empty_no_data_found(self):
        ''' _generate_data_summary_UENNSS should return None if no data is found '''
        username='test__generate_data_summary_uennss_datapoint_empty_no_data_found'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        datapointname='test_datapoint'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=widgetapi.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], datapoint['pid'])
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.DATAPOINT)
        self.assertEqual(widget['widgetname'], '.'.join((datasourcename,datapointname)))
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=10000), interval_end=timeuuid.uuid1(seconds=80000))
        self.assertIsNotNone(snapshot)
        self.assertIsNone(summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']}))

    def test__generate_data_summary_UENNSS_datapoint_success(self):
        ''' _generate_data_summary_UENNSS should return the summary '''
        username='test__generate_data_summary_uennss_datapoint_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        datapointname='test_datapoint'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=widgetapi.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], datapoint['pid'])
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.DATAPOINT)
        self.assertEqual(widget['widgetname'], '.'.join((datasourcename,datapointname)))
        for i in range(1,1000):
            date=timeuuid.uuid1(seconds=i)
            value=decimal.Decimal(random.randint(-10000,10000))
            self.assertTrue(cassapidatapoint.insert_datapoint_data(pid=datapoint['pid'],date=date, value=value))
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=100), interval_end=timeuuid.uuid1(seconds=801))
        self.assertIsNotNone(snapshot)
        data_summary=summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']})
        self.assertIsNotNone(data_summary)
        self.assertEqual(data_summary['its'],100.0)
        self.assertEqual(data_summary['ets'],801.0)
        self.assertEqual(data_summary['widgetname'],widget['widgetname'])
        self.assertEqual(data_summary['type'],widget_types.DATAPOINT)
        self.assertEqual(len(data_summary['datapoints']),1)
        self.assertEqual(len(data_summary['datapoints'][0]['data']),50)
        self.assertEqual(data_summary['datapoints'][0]['color'],datapoint['color'])

    def test__generate_data_summary_UENNSS_multi_datapoint_empty_no_data_found(self):
        ''' _generate_data_summary_UENNSS should return None if no data is found '''
        username='test__generate_data_summary_uennss_multi_datapoint_empty_no_data_found'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        datapointname_1='test_datapoint_1'
        datapointname_2='test_datapoint_2'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint_1=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname_1)
        datapoint_2=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname_2)
        widget=widgetapi.new_widget_multidp(uid=user['uid'],widgetname='widget_multidp') 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.MULTIDP)
        self.assertEqual(widget['widgetname'],'widget_multidp')
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint_1['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint_2['pid']))
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=100), interval_end=timeuuid.uuid1(seconds=801))
        self.assertIsNotNone(snapshot)
        self.assertIsNone(summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']}))

    def test__generate_data_summary_UENNSS_multi_datapoint_only_one_has_data(self):
        ''' _generate_data_summary_UENNSS should return None if no data is found '''
        username='test__generate_data_summary_uennss_multi_datapoint_only_one_has_data'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        datapointname_1='test_datapoint_1'
        datapointname_2='test_datapoint_2'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint_1=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname_1)
        datapoint_2=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname_2)
        widget=widgetapi.new_widget_multidp(uid=user['uid'],widgetname='widget_multidp') 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.MULTIDP)
        self.assertEqual(widget['widgetname'],'widget_multidp')
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint_1['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint_2['pid']))
        for i in range(1,1000):
            date=timeuuid.uuid1(seconds=i+0.5)
            value=decimal.Decimal(random.randint(-10000,10000))
            self.assertTrue(cassapidatapoint.insert_datapoint_data(pid=datapoint_2['pid'],date=date, value=value))
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=100), interval_end=timeuuid.uuid1(seconds=801))
        self.assertIsNotNone(snapshot)
        data_summary=summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']})
        self.assertIsNotNone(data_summary)
        self.assertEqual(data_summary['its'],100.0)
        self.assertEqual(data_summary['ets'],801.0)
        self.assertEqual(data_summary['widgetname'],widget['widgetname'])
        self.assertEqual(data_summary['type'],widget_types.MULTIDP)
        self.assertEqual(len(data_summary['datapoints']),2)
        self.assertTrue(len(data_summary['datapoints'][0]['data']) in (0,50))
        self.assertTrue(len(data_summary['datapoints'][1]['data']) in (0,50))
        self.assertNotEqual(data_summary['datapoints'][0]['data'],data_summary['datapoints'][1]['data'])
        self.assertTrue(data_summary['datapoints'][0]['color'] in (datapoint_1['color'],datapoint_2['color']))
        self.assertTrue(data_summary['datapoints'][1]['color'] in (datapoint_1['color'],datapoint_2['color']))
        self.assertNotEqual(data_summary['datapoints'][0]['color'],data_summary['datapoints'][1]['color'])

    def test__generate_data_summary_UENNSS_multi_datapoint_success(self):
        ''' _generate_data_summary_UENNSS should return None if no data is found '''
        username='test__generate_data_summary_uennss_multi_datapoint_success'
        password='temporal'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='test_datasource'
        datapointname_1='test_datapoint_1'
        datapointname_2='test_datapoint_2'
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        datapoint_1=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname_1)
        datapoint_2=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname_2)
        widget=widgetapi.new_widget_multidp(uid=user['uid'],widgetname='widget_multidp') 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], widget_types.MULTIDP)
        self.assertEqual(widget['widgetname'],'widget_multidp')
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint_1['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint_2['pid']))
        for i in range(1,1000):
            date=timeuuid.uuid1(seconds=i)
            value=decimal.Decimal(random.randint(-10000,10000))
            self.assertTrue(cassapidatapoint.insert_datapoint_data(pid=datapoint_1['pid'],date=date, value=value))
        for i in range(1,1000):
            date=timeuuid.uuid1(seconds=i+0.5)
            value=decimal.Decimal(random.randint(-10000,10000))
            self.assertTrue(cassapidatapoint.insert_datapoint_data(pid=datapoint_2['pid'],date=date, value=value))
        snapshot=snapshotapi.new_snapshot(wid=widget['wid'],uid=user['uid'],interval_init=timeuuid.uuid1(seconds=100), interval_end=timeuuid.uuid1(seconds=801))
        self.assertIsNotNone(snapshot)
        data_summary=summary._generate_data_summary_UENNSS(parameters={'nid':snapshot['nid']})
        self.assertIsNotNone(data_summary)
        self.assertEqual(data_summary['its'],100.0)
        self.assertEqual(data_summary['ets'],801.0)
        self.assertEqual(data_summary['widgetname'],widget['widgetname'])
        self.assertEqual(data_summary['type'],widget_types.MULTIDP)
        self.assertEqual(len(data_summary['datapoints']),2)
        self.assertEqual(len(data_summary['datapoints'][0]['data']),50)
        self.assertEqual(len(data_summary['datapoints'][1]['data']),50)
        self.assertTrue(data_summary['datapoints'][0]['color'] in (datapoint_1['color'],datapoint_2['color']))
        self.assertTrue(data_summary['datapoints'][1]['color'] in (datapoint_1['color'],datapoint_2['color']))
        self.assertNotEqual(data_summary['datapoints'][0]['color'],data_summary['datapoints'][1]['color'])

    def test__generate_data_summary_UEIDPI_failure_did_parameter_not_found(self):
        ''' _generate_data_summary_UEIDPI should fail if did parameter is not found '''
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_IDID)

    def test__generate_data_summary_UEIDPI_failure_invalid_did_parameter(self):
        ''' _generate_data_summary_UEIDPI should fail if did parameter is invalid '''
        parameters={'did':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_IDID)

    def test__generate_data_summary_UEIDPI_failure_no_dates_parameter(self):
        ''' _generate_data_summary_UEIDPI should fail if dates parameter is not found '''
        parameters={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_IDATES)

    def test__generate_data_summary_UEIDPI_failure_no_dates_parameter_list(self):
        ''' _generate_data_summary_UEIDPI should fail if dates parameter is not a list '''
        parameters={'did':uuid.uuid4(), 'dates':1}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_IDATES)

    def test__generate_data_summary_UEIDPI_failure_no_dates(self):
        ''' _generate_data_summary_UEIDPI should fail if dates length is 0 '''
        parameters={'did':uuid.uuid4(),'dates':[]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_IDATES)

    def test__generate_data_summary_UEIDPI_failure_dates_item_not_date(self):
        ''' _generate_data_summary_UEIDPI should fail if dates item is not hex date '''
        parameters={'did':uuid.uuid4(),'dates':[uuid.uuid1(),uuid.uuid1().hex]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_IDATES)

    def test__generate_data_summary_UEIDPI_failure_data_not_found(self):
        ''' _generate_data_summary_UEIDPI should fail if data is not found '''
        parameters={'did':uuid.uuid4(),'dates':[uuid.uuid1()]}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_DSDNF)

    def test__generate_data_summary_UEIDPI_failure_data_has_no_vars(self):
        ''' _generate_data_summary_UEIDPI should fail if data content has no variables '''
        username='test__generate_data_summary_ueidpi_failure_data_has_no_vars'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='1 datasource content'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        datapointname='datapoint_name'
        datapoint=datapointapi.monitor_new_datapoint(did=datasource['did'],date=date, position=0, length = 1,datapointname=datapointname)
        date = timeuuid.uuid1()
        content='datasource content with no vars'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        parameters={'did':datasource['did'],'dates':[date]}
        with self.assertRaises(exceptions.UserEventCreationException) as cm:
            summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(cm.exception.error, Errors.E_EAS_GDSUEIDPI_DSVNF)

    def test__generate_data_summary_UEIDPI_success(self):
        ''' _generate_data_summary_UEIDPI should succeed '''
        username='test__generate_data_summary_ueidpi_success'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        date=uuid.uuid1()
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex]
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        datasourcename='datasource'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agent=agentapi.create_agent(uid=user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='1 datasource content'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        datapointname='datapoint_name'
        datapoint=datapointapi.monitor_new_datapoint(did=datasource['did'],date=date, position=0, length = 1,datapointname=datapointname)
        parameters={'did':datasource['did'],'dates':[date]}
        ev_summary = summary._generate_data_summary_UEIDPI(parameters=parameters)
        self.assertEqual(ev_summary,{'data':[{'vars':[(0,1),],'content':content,'ts':timeuuid.get_unix_timestamp(date),'seq':timeuuid.get_custom_sequence(date)}]})

