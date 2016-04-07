import unittest
import uuid
from komlog.komcass.api import events as cassapievents
from komlog.komcass.model.orm import events as ormevents
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.events.api import user_responses
from komlog.komlibs.events.api import user
from komlog.komlibs.events.model import types, priorities
from komlog.komlibs.events import exceptions, errors
from komlog.komlibs.gestaccount import errors as gesterrors
from komlog.komlibs.gestaccount import exceptions as gestexcept
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
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRP_IUID)

    def test_process_event_response_failure_invalid_date(self):
        ''' process_event_response should fail if date is invalid '''
        dates=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        response_data=dict()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses.process_event_response(uid=uid, date=date, response_data=response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRP_IDT)

    def test_process_event_response_failure_invalid_response_data(self):
        ''' process_event_response should fail if response_data is invalid '''
        response_datas=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        date=uuid.uuid1()
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses.process_event_response(uid=uid, date=date, response_data=response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRP_IDAT)

    def test_process_event_response_failure_non_existent_event(self):
        ''' process_event_response should fail if event does not exist '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        response_data={}
        with self.assertRaises(exceptions.EventNotFoundException) as cm:
            user_responses.process_event_response(uid=uid, date=date, response_data=response_data)
        self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRP_EVNF)

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
        self.assertFalse(user_responses.process_event_response(uid=new_user['uid'], date=date, response_data=response_data))

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_no_UserEventInterventionDatapointIdentification_instance(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if event is not UserEventItervDatapointIdentification '''
        events=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        response_data={}
        for event in events:
            self.assertFalse(user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data))

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_type(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data is not a dict '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        responses=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        for response in responses:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IRD)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_identified(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{}, {'missing':[]},{'identified':23}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event=event, response_data=response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IIDP)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_missing(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{'identified':[],'missing':23423},{'identified':[]}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IMSP)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_identified_item_type(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{'identified':[1,2,3,4,5],'missing':[]}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IIDI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_identified_item_dp(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{'identified':[{'hola':'que tal'}],'missing':[]}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IDPI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_identified_item_p(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{'identified':[{'pid':uuid.uuid4().hex,'p':'34'}],'missing':[]}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IPI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_identified_item_l(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{'identified':[{'pid':uuid.uuid4().hex,'p':34,'l':[232]}],'missing':[]}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_ILI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_invalid_response_data_content_missing_item_type(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        now=timeuuid.uuid1()
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_datas=[{'identified':[{'pid':uuid.uuid4().hex,'p':34,'l':232}],'missing':['string']}]
        for response_data in response_datas:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
            self.assertEqual(cm.exception.error, errors.E_EAUR_PEVRPUEIDI_IMSI)

    def test__process_event_response_user_event_intervention_datapoint_identification_failure_datasource_not_found(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should fail if response_data parameter is invalid  '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ds_date=timeuuid.uuid1()
        now=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        event=ormevents.UserEventInterventionDatapointIdentification(uid=uid, date=now, priority=1,did=did,ds_date=ds_date,doubts=doubts,discarded=discarded)
        self.assertTrue(cassapievents.insert_user_event(event))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        response_data={'identified':[{'pid':uuid.uuid4().hex,'p':34,'l':232}],'missing':[uuid.uuid4().hex]}
        with self.assertRaises(gestexcept.DatasourceNotFoundException) as cm:
            user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
        self.assertEqual(cm.exception.error, gesterrors.E_GDA_GDC_DNF)

    def test__process_event_response_user_event_intervention_datapoint_identification_success(self):
        ''' _process_event_response_user_event_intervention_datapoint_identification should succeed '''
        username='test__process_event_response_user_event_intervention_datapoint_identification_success'
        password='password'
        email=username+'@komlog.org'
        komlog_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test__process_event_response_user_event_intervention_datapoint_identification_success_agentname'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test version'
        agent=agentapi.create_agent(uid=komlog_user['uid'],agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test__process_event_response_user_event_intervention_datapoint_identification_success_datasourcename'
        datasource=datasourceapi.create_datasource(uid=komlog_user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        uid=komlog_user['uid']
        init_date1=timeuuid.uuid1()
        content_type1='event processing content\n10\nand more variables like 30\n no more'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date1, content=content_type1))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date1))
        init_date2=timeuuid.uuid1()
        content_type2='only a number;9;? or whatever'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date2, content=content_type2))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date2))
        #now monitor vars in content1
        position=25
        length=2
        datapointname='datapoint_1'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=init_date1, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=init_date1))
        position=52
        length=2
        datapointname='datapoint_2'
        datapoint2=datapointapi.monitor_new_datapoint(did=did, date=init_date1, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint2['pid'], date=init_date1))
        #now monitor vars in content2
        position=14
        length=1
        datapointname='datapoint_3'
        datapoint3=datapointapi.monitor_new_datapoint(did=did, date=init_date2, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint3['pid'], date=init_date2))
        init_date3=timeuuid.uuid1()
        content_type3='only a number 34 or whatever it is 21'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date3, content=content_type3))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date3))
        ds_date=init_date3
        doubts=[datapoint1['pid'], datapoint2['pid'], datapoint3['pid']]
        discarded=[]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex,'date':ds_date.hex,'doubts':[pid.hex for pid in doubts],'discarded':[]}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        )
        event=cassapievents.get_user_event(uid=uid, date=events[0]['date'])
        not_belonging_pid=uuid.uuid4()
        response_data={'identified':[{'pid':datapoint3['pid'].hex,'p':14,'l':2}],'missing':[datapoint1['pid'].hex, datapoint2['pid'].hex,not_belonging_pid.hex]}
        user_responses._process_event_response_user_event_intervention_datapoint_identification(event, response_data)
        stored_response=cassapievents.get_user_events_responses_intervention_datapoint_identification(uid=uid)
        self.assertEqual(len(stored_response),1)
        response=stored_response[0]
        self.assertTrue(isinstance(response, ormevents.UserEventResponseInterventionDatapointIdentification))
        self.assertEqual(response.uid, event.uid)
        self.assertEqual(response.date, event.date)
        self.assertEqual(response.type, types.USER_EVENT_RESPONSE_INTERVENTION_DATAPOINT_IDENTIFICATION)
        self.assertEqual(response.missing, set([uuid.UUID(pid) for pid in response_data['missing']]))
        self.assertEqual(response.identified, {datapoint3['pid']:14})
        self.assertEqual(response.not_belonging,{not_belonging_pid})
        self.assertEqual(response.update_failed, set())
        self.assertEqual(response.update_success, set(sorted([datapoint1['pid'], datapoint2['pid'], datapoint3['pid']])))
        self.assertEqual(response.to_update, set(sorted([datapoint1['pid'], datapoint2['pid'], datapoint3['pid']])))

