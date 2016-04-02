import unittest
import uuid
import json
from komlog.komlibs.events.api import user as usereventsapi
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.events import errors as eventserrors
from komlog.komlibs.interface.imc.api import events
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status
from komlog.komlibs.general.time import timeuuid


class InterfaceImcApiEventsTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.events tests '''

    def test_process_message_USEREV_success_new_user_event(self):
        ''' process_message_USEREV should succeed with NEW_USER events '''
        uid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_USER
        message=messages.UserEventMessage(uid=uid, event_type=event_type)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNU_UNF)

    def test_process_message_USEREV_success_new_agent_event(self):
        ''' process_message_USEREV should succeed with NEW_AGENT events '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':aid.hex}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNA_UNF)

    def test_process_message_USEREV_success_new_datasource_event(self):
        ''' process_message_USEREV should succeed with NEW_DATASOURCE events '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={'did':did.hex}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNDS_UNF)

    def test_process_message_USEREV_success_new_datapoint_event(self):
        ''' process_message_USEREV should succeed with NEW_DATAPOINT events '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={'pid':pid.hex}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNDP_UNF)

    def test_process_message_USEREV_success_new_widget_event(self):
        ''' process_message_USEREV should succeed with NEW_WIDGET events '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={'wid':wid.hex}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNWG_UNF)

    def test_process_message_USEREV_success_new_dashboard_event(self):
        ''' process_message_USEREV should succeed with NEW_DASHBOARD events '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={'bid':bid.hex}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNDB_UNF)

    def test_process_message_USEREV_success_new_circle_event(self):
        ''' process_message_USEREV should succeed with NEW_CIRCLE events '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={'cid':cid.hex}
        message=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        response=events.process_message_USEREV(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.error, eventserrors.E_EAU_IENNC_UNF)

    def test_process_message_USEREV_failure_unknown_event_type(self):
        ''' process_message_USEREV should fail if did does not exists '''
        uid=uuid.uuid4()
        event_type=10000
        message=messages.UserEventMessage(uid=uid, event_type=event_type)
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

