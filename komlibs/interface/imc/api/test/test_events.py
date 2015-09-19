import unittest
import uuid
import json
from komlibs.events.api import user as usereventsapi
from komlibs.events.model import types as eventstypes
from komlibs.events import errors as eventserrors
from komlibs.interface.imc.api import events
from komlibs.interface.imc.model import messages
from komlibs.interface.imc import status
from komlibs.general.time import timeuuid


class InterfaceImcApiEventsTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.events tests '''

    def test_process_message_USEREV_success_new_user_event(self):
        ''' process_message_USEREV should succeed with NEW_USER events '''
        uid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_USER
        parameters={'username':'test_process_message_userev_success_new_user'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_success_new_agent_event(self):
        ''' process_message_USEREV should succeed with NEW_AGENT events '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':aid.hex, 'agentname':'test_process_message_userev_success_new_agent'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_AGENT)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_success_new_datasource_event(self):
        ''' process_message_USEREV should succeed with NEW_DATASOURCE events '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={'aid':aid.hex, 'did':did.hex, 'datasourcename':'test_process_message_userev_success_new_datasource'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_success_new_datapoint_event(self):
        ''' process_message_USEREV should succeed with NEW_DATAPOINT events '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={'pid':pid.hex, 'did':did.hex, 'datasourcename':'test_process_message_userev_success_new_datapoint', 'datapointname':'test_process_message_userev_success_new_datapoint'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_success_new_widget_event(self):
        ''' process_message_USEREV should succeed with NEW_WIDGET events '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={'wid':wid.hex, 'widgetname':'test_process_message_userev_success_new_widget'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_WIDGET)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_success_new_dashboard_event(self):
        ''' process_message_USEREV should succeed with NEW_DASHBOARD events '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={'bid':bid.hex, 'dashboardname':'test_process_message_userev_success_new_dashboard'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_success_new_circle_event(self):
        ''' process_message_USEREV should succeed with NEW_CIRCLE events '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={'cid':cid.hex, 'circlename':'test_process_message_userev_success_new_circle'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        user_events=usereventsapi.get_events(uid=uid, params_serializable=True)
        self.assertEqual(len(user_events),1)
        self.assertEqual(user_events[0]['type'],eventstypes.USER_EVENT_NOTIFICATION_NEW_CIRCLE)
        self.assertEqual(user_events[0]['parameters'],parameters)

    def test_process_message_USEREV_failure_invalid_username(self):
        ''' process_message_USEREV should fail if did does not exist '''
        uid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_USER
        parameters={'username':'test_process_message_USEREV_failure'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)

    def test_process_message_USEREV_failure_unknown_event_type(self):
        ''' process_message_USEREV should fail if did does not exists '''
        uid=uuid.uuid4()
        event_type=10000
        parameters={'username':'test_process_message_event_failure'}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)

    def test_process_message_USEREVRESP_failure_event_not_found(self):
        ''' process_message_USEREVRESP should fail if event does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={}
        message=messages.UserEventResponseMessage(uid=uid, date=date, parameters=parameters)
        response=events.process_message_USEREVRESP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventserrors.E_EAUR_PEVRP_EVNF)

