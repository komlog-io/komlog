import unittest
import uuid
from komlog.komcass.api import events as cassapievents
from komlog.komcass.model.orm import events as ormevents
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.events.api import user_responses
from komlog.komlibs.events.api import user
from komlog.komlibs.events.model import types, priorities
from komlog.komlibs.events import exceptions
from komlog.komlibs.events.errors import Errors
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komfig import logging

class EventsApiUserResponsesTest(unittest.TestCase):
    ''' komlibs.events.api.user_responses tests '''

    def test_process_event_response_failure_invalid_uid(self):
        ''' process_event_response should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=timeuuid.uuid1()
        response_data=dict()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses.process_event_response(uid=uid, date=date, response_data=response_data)
            self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRP_IUID)

    def test_process_event_response_failure_invalid_date(self):
        ''' process_event_response should fail if date is invalid '''
        dates=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        response_data=dict()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses.process_event_response(uid=uid, date=date, response_data=response_data)
            self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRP_IDT)

    def test_process_event_response_failure_non_existent_event(self):
        ''' process_event_response should fail if event does not exist '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        response_data={}
        with self.assertRaises(exceptions.EventNotFoundException) as cm:
            user_responses.process_event_response(uid=uid, date=date, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRP_EVNF)

    def test_process_event_response_failure_non_supported_event(self):
        ''' process_event_response should fail if event type is not supported '''
        username='test_process_event_response_failure_non_supported_event'
        password='temporal'
        email=username+'@komlog.org'
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        new_user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(new_user)
        self.assertTrue(user.new_event(uid=new_user['uid'],event_type=event_type,parameters={}))
        events=user.get_events(uid=new_user['uid'])
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_USER)
        date=events[0]['date']
        response_data={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses.process_event_response(uid=new_user['uid'], date=date, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRP_IEVT)


    def test__process_event_response_user_event_intervention_datapoint_identification_failure_no_UserEventInterventionDatapointIdentification_instance(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if event is not UserEventItervDatapointIdentification '''
        events=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        response_data={}
        for event in events:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IEVT)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_type(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data is not a dict '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        responses=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        for response in responses:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response)
            self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IRD)

    def test__process_event_response_user_event_intervention_datapoint_identification_identified_not_found(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data has no identified parameter '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IDFNF)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_identified(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter identified is invalid  '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':1}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IDFTI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_item_type(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data identified item type is not a dict '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[1]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IIDI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_identified_item_has_no_sequence(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if identified item has no sequence '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'p':None,'l':None}]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_ISEQI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_identified_item_has_invalid_sequence(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if identified item has invalid sequence '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'s':1,'p':None,'l':None}]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_ISEQI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_identified_item_has_no_position(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if identified item has no position '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'s':timeuuid.get_custom_sequence(now),'pa':None,'l':None}]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IPI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_identified_item_has_invalid_position(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if identified item has invalid position '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'s':timeuuid.get_custom_sequence(now),'p':-1,'l':None}]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_IPI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_identified_item_has_no_length(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if identified item has invalid length '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'s':timeuuid.get_custom_sequence(now),'p':1,'la':None}]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_ILI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_identified_item_has_invalid_length(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if identified item has invalid length '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'s':timeuuid.get_custom_sequence(now),'p':1,'l':-1}]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(cm.exception.error, Errors.E_EAUR_PEVRPUEIDI_ILI)

    def test__process_event_response_user_event_intervention_datapoint_identification_non_existent_datapoint_positives_and_missing(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should return a dict indicating that the mark could not be made if pid does not exist '''
        uid=uuid.uuid4()
        pid = uuid.uuid4()
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        seq1=timeuuid.get_custom_sequence(timeuuid.uuid1())
        seq2=timeuuid.get_custom_sequence(timeuuid.uuid1())
        response_data={'identified':[
            {'s':seq1,'p':1,'l':1},
            {'s':seq2,'p':1,'l':1},
        ]}
        result=user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(sorted(result['mark_failed']),sorted([item['s'] for item in response_data['identified']]))
        self.assertEqual(result['dtree_gen_success'],[])
        self.assertEqual(result['dtree_gen_failed'],[])
        self.assertEqual(result['type'],types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)

    def test__process_event_response_user_event_intervention_datapoint_identification_success_processing_dtree(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should succeed processing dtree '''
        username='test__process_event_response_user_event_intervention_datapoint_identification_success_processing_dtree'
        password='password'
        email=username+'@komlog.org'
        komlog_user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test version'
        agent=agentapi.create_agent(uid=komlog_user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=komlog_user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        uid=komlog_user['uid']
        init_date1=timeuuid.uuid1()
        content_type1='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date1, content=content_type1))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date1))
        init_date2=timeuuid.uuid1()
        content_type2='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date2, content=content_type2))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date2))
        #now monitor vars in content1
        position=4
        length=1
        datapointname='datapoint_1'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=init_date1, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=init_date1))
        pid = datapoint1['pid']
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        seq1=timeuuid.get_custom_sequence(init_date1)
        seq2=timeuuid.get_custom_sequence(init_date2)
        response_data={'identified':[
            {'s':seq2,'p':4,'l':1},
        ]}
        result=user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(sorted(result['mark_failed']),[])
        self.assertEqual(result['dtree_gen_success'],[did])
        self.assertEqual(result['dtree_gen_failed'],[])
        self.assertEqual(result['type'],types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_processing_dtree(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should succeed processing dtree '''
        username='test__process_event_response_user_event_intervention_datapoint_identification_failure_processing_dtree'
        password='password'
        email=username+'@komlog.org'
        komlog_user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test version'
        agent=agentapi.create_agent(uid=komlog_user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=komlog_user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        uid=komlog_user['uid']
        init_date1=timeuuid.uuid1()
        content_type1='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date1, content=content_type1))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date1))
        init_date2=timeuuid.uuid1()
        content_type2='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date2, content=content_type2))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date2))
        #now monitor vars in content1
        position=4
        length=1
        datapointname='datapoint_1'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=init_date1, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=init_date1))
        pid = datapoint1['pid']
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        seq1=timeuuid.get_custom_sequence(init_date1)
        seq2=timeuuid.get_custom_sequence(init_date2)
        response_data={'identified':[
            {'s':seq2,'p':None,'l':None},
        ]}
        result=user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(sorted(result['mark_failed']),[])
        self.assertEqual(result['dtree_gen_success'],[])
        self.assertEqual(result['dtree_gen_failed'],[did])
        self.assertEqual(result['type'],types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)

    def test__process_event_response_user_event_intervention_datapoint_identification_success_some_datapoints(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should succeed processing dtrees of multiple datapoints '''
        username='test__process_event_response_user_event_intervention_datapoint_identification_success_some_datapoints'
        password='password'
        email=username+'@komlog.org'
        komlog_user=userapi.create_user(username=username, password=password, email=email)
        agentname='agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test version'
        agent=agentapi.create_agent(uid=komlog_user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=komlog_user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        uid=komlog_user['uid']
        init_date1=timeuuid.uuid1()
        content_type1='x = 1, y = 2'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date1, content=content_type1))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date1))
        init_date2=timeuuid.uuid1()
        content_type2='x = 1, y = 2'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date2, content=content_type2))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date2))
        #monitor x
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=init_date1, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=init_date1))
        pid1 = datapoint1['pid']
        #monitor y
        position = 11 
        length = 1
        datapointname = 'y'
        datapoint2=datapointapi.monitor_new_datapoint(did=did, date=init_date1, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint2['pid'], date=init_date1))
        pid1 = datapoint1['pid']
        pid2 = datapoint2['pid']
        datasourcename='dsname'
        datapointname='dpname'
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,pid=pid1, datapointname=datapointname, datasourcename=datasourcename)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        seq1=timeuuid.get_custom_sequence(init_date1)
        seq2=timeuuid.get_custom_sequence(init_date2)
        seq3=timeuuid.get_custom_sequence(uuid.uuid1())
        response_data={'identified':[
            {'s':seq2,'p':4,'l':1},
            {'s':seq3,'p':4,'l':1},
        ]}
        result=user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
        self.assertEqual(sorted(result['mark_failed']),[seq3])
        self.assertEqual(sorted(result['dtree_gen_success']),[did])
        self.assertEqual(result['dtree_gen_failed'],[])
        self.assertEqual(result['type'],types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)

