import unittest
import uuid
from komlibs.general.time import timeuuid
from komlibs.events.api import user
from komlibs.events.model import types, priorities
from komlibs.events import exceptions, errors
from komfig import logger

class EventsApiUserTest(unittest.TestCase):
    ''' komlibs.events.api.user tests '''

    def test_get_events_failure_invalid_uid(self):
        ''' get_events should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.get_events(uid=uid)
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_IU)

    def test_get_events_failure_invalid_to_date(self):
        ''' get_events should fail if to_date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.get_events(uid=uid, to_date=date )
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_ITD)

    def test_get_events_failure_invalid_from_date(self):
        ''' get_events should fail if from_date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.get_events(uid=uid, from_date=date )
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_IFD)

    def test_get_events_failure_invalid_count(self):
        ''' get_events should fail if count is invalid '''
        counts=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for count in counts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.get_events(uid=uid, count=count)
            self.assertEqual(cm.exception.error, errors.E_EAU_GEVS_ICNT)

    def test_get_events_success(self):
        ''' get_events should return the event list '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        bid=uuid.uuid4()
        cid=uuid.uuid4()
        username='test_get_events_success_username'
        agentname='test_get_events_success_agentname'
        datasourcename='test_get_events_success_datasourcename'
        datapointname='test_get_events_success_datapointname'
        widgetname='test_get_events_success_widgetname'
        dashboardname='test_get_events_success_dashboardname'
        circlename='test_get_events_success_circlename'
        self.assertTrue(user.insert_new_user_event(uid=uid, username=username))
        self.assertTrue(user.insert_new_agent_event(uid=uid, aid=aid, agentname=username))
        self.assertTrue(user.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename))
        self.assertTrue(user.insert_new_datapoint_event(uid=uid, did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname))
        self.assertTrue(user.insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname))
        self.assertTrue(user.insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname))
        self.assertTrue(user.insert_new_circle_event(uid=uid, cid=cid, circlename=circlename))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),7)

    def test_enable_event_failure_invalid_uid(self):
        ''' enable_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=uuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.enable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_ACE_IU)

    def test_enable_event_failure_invalid_date(self):
        ''' enable_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.enable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_ACE_ID)

    def test_disable_event_failure_invalid_uid(self):
        ''' disable_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=uuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.disable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_DACE_IU)

    def test_disable_event_failure_invalid_date(self):
        ''' disable_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.disable_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_DACE_ID)

    def test_enable_disable_event_success(self):
        ''' enable_event and disable_event should succeed, for simplicity even if the event does not exist '''
        uid=uuid.uuid4()
        username='test_enable_event_success_username'
        self.assertTrue(user.insert_new_user_event(uid=uid, username=username))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        event=events[0]
        self.assertTrue(user.disable_event(uid=uid, date=event['date']))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),0)
        self.assertTrue(user.enable_event(uid=uid, date=event['date']))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)

    def test_delete_events_failure_invalid_uid(self):
        ''' delete_events should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.delete_events(uid=uid)
            self.assertEqual(cm.exception.error, errors.E_EAU_DEV_IU)

    def test_delete_events_success(self):
        ''' delete_events should succeed '''
        uid=uuid.uuid4()
        username='test_delete_events_success_username'
        self.assertTrue(user.insert_new_user_event(uid=uid, username=username))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertTrue(user.delete_events(uid=uid))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),0)

    def test_new_event_failure_invalid_event_type(self):
        ''' new_event should fail if type is invalid  '''
        event_types=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        parameters={}
        for event_type in event_types:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_IEVT)

    def test_new_event_failure_non_existent_event_type(self):
        ''' new_event should fail if type is invalid  '''
        event_type=234234
        uid=uuid.uuid4()
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_EVTNF)

    def test_new_event_new_user_failure_non_username_parameter_passed(self):
        ''' new_event should fail if type is NEW_USER and no username parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NUIU)

    def test_new_event_new_user_failure_invalid_username_passed(self):
        ''' new_event should fail if type is NEW_USER and username parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        usernames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for username in usernames:
            parameters={'username':username}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NUIU)

    def test_new_event_new_user_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        username='a_valid_username'
        parameters={'username':username}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_new_agent_failure_non_aid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and no aid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NAID)

    def test_new_event_new_agent_failure_invalid_aid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        aids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for aid in aids:
            parameters={'aid':aid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NAID)

    def test_new_event_new_agent_failure_non_agentname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and no agentname parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NAIA)

    def test_new_event_new_agent_failure_invalid_agentname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_AGENT and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        agentnames=[None,234234, 234234.234234, 'astring_WITH_ÑÑ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for agentname in agentnames:
            parameters={'aid':uuid.uuid4().hex, 'agentname':agentname}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NAIA)

    def test_new_event_new_agent_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        agentname='test_new_event_new_agent_success'
        parameters={'aid':uuid.uuid4().hex, 'agentname':agentname}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_new_datasource_failure_non_aid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and no aid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NDIA)

    def test_new_event_new_datasource_failure_invalid_aid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        aids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for aid in aids:
            parameters={'aid':aid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NDIA)

    def test_new_event_new_datasource_failure_non_did_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and no aid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={'aid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NDID)

    def test_new_event_new_datasource_failure_invalid_did_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for did in dids:
            parameters={'aid':uuid.uuid4().hex, 'did':did}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NDID)

    def test_new_event_new_datasource_failure_non_datasourcename_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and no datasourcename parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        parameters={'aid':uuid.uuid4().hex,'did':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NDIN)

    def test_new_event_new_datasource_failure_invalid_datasourcename_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATASOURCE and aid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        datasourcenames=[None,234234, 234234.234234, 'astring_ññññ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for datasourcename in datasourcenames:
            parameters={'aid':uuid.uuid4().hex, 'did':uuid.uuid4().hex, 'datasourcename':datasourcename}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NDIN)

    def test_new_event_new_datasource_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE
        datasourcename='test_new_event_new_datasource_success'
        parameters={'aid':uuid.uuid4().hex, 'did':uuid.uuid4().hex, 'datasourcename':datasourcename}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_new_datapoint_failure_non_did_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and no did parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPID)

    def test_new_event_new_datapoint_failure_invalid_did_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and did parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for did in dids:
            parameters={'did':did}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPID)

    def test_new_event_new_datapoint_failure_non_pid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and no pid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={'did':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPIP)

    def test_new_event_new_datapoint_failure_invalid_pid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and pid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        pids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for pid in pids:
            parameters={'did':uuid.uuid4().hex, 'pid':pid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPIP)

    def test_new_event_new_datapoint_failure_non_datasourcename_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and no datasourcename parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        parameters={'pid':uuid.uuid4().hex,'did':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPIN)

    def test_new_event_new_datapoint_failure_invalid_datasourcename_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and datasourcename parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        datasourcenames=[None,234234, 234234.234234, 'astring_ñññ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for datasourcename in datasourcenames:
            parameters={'pid':uuid.uuid4().hex, 'did':uuid.uuid4().hex, 'datasourcename':datasourcename}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPIN)

    def test_new_event_new_datapoint_failure_non_datapointname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and no datapointname parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        datasourcename='test_new_event_new_datapoint_failure_non_datapointname_parameter_passed'
        parameters={'pid':uuid.uuid4().hex,'did':uuid.uuid4().hex,'datasourcename':datasourcename}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPIM)

    def test_new_event_new_datapoint_failure_invalid_datapointname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DATAPOINT and datapointname parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        datasourcename='test_new_event_new_datapoint_failure_invalid_datapointname_parameter_passed'
        datapointnames=[None,234234, 234234.234234, 'astring_ññññ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for datapointname in datapointnames:
            parameters={'pid':uuid.uuid4().hex, 'did':uuid.uuid4().hex, 'datasourcename':datasourcename, 'datapointname':datapointname}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NPIM)

    def test_new_event_new_datapoint_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT
        datasourcename='test_new_event_new_datapoint_success'
        datapointname='test_new_event_new_datapoint_success'
        parameters={'pid':uuid.uuid4().hex, 'did':uuid.uuid4().hex, 'datasourcename':datasourcename, 'datapointname':datapointname}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_new_widget_failure_non_wid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and no wid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NWIW)

    def test_new_event_new_widget_failure_invalid_wid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and wid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        wids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for wid in wids:
            parameters={'wid':wid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NWIW)

    def test_new_event_new_widget_failure_non_widgetname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and no widgetname parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        parameters={'wid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NWIN)

    def test_new_event_new_widget_failure_invalid_widgetname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_WIDGET and widgetname parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        widgetnames=[None,234234, 234234.234234, 'astring_WITH_ÑÑ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for widgetname in widgetnames:
            parameters={'wid':uuid.uuid4().hex, 'widgetname':widgetname}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NWIN)

    def test_new_event_new_widget_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_WIDGET
        widgetname='test_new_event_new_agent_success'
        parameters={'wid':uuid.uuid4().hex, 'widgetname':widgetname}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_new_dashboard_failure_non_bid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and no bid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NBIB)

    def test_new_event_new_dashboard_failure_invalid_bid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and bid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        bids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for bid in bids:
            parameters={'bid':bid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NBIB)

    def test_new_event_new_dashboard_failure_non_dashboardname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and no dashboardname parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        parameters={'bid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NBIN)

    def test_new_event_new_dashboard_failure_invalid_dashboardname_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_DASHBOARD and dashboardname parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        dashboardnames=[None,234234, 234234.234234, 'astring_WITH_ÑÑ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for dashboardname in dashboardnames:
            parameters={'bid':uuid.uuid4().hex, 'dashboardname':dashboardname}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NBIN)

    def test_new_event_new_dashboard_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD
        dashboardname='test_new_event_new_dashboard_success'
        parameters={'bid':uuid.uuid4().hex, 'dashboardname':dashboardname}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_new_circle_failure_non_cid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and no cid parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NCIC)

    def test_new_event_new_circle_failure_invalid_cid_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and cid parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        cids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for cid in cids:
            parameters={'cid':cid}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NCIC)

    def test_new_event_new_circle_failure_non_circlename_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and no circlename parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        parameters={'cid':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NCIN)

    def test_new_event_new_circle_failure_invalid_circlename_parameter_passed(self):
        ''' new_event should fail if event_type is NEW_CIRCLE and circlename parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        circlenames=[None,234234, 234234.234234, 'astring_WITH_ÑÑ',uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for circlename in circlenames:
            parameters={'cid':uuid.uuid4().hex, 'circlename':circlename}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_NCIN)

    def test_new_event_new_circle_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_NOTIFICATION_NEW_CIRCLE
        circlename='test_new_event_new_circle_success'
        parameters={'cid':uuid.uuid4().hex, 'circlename':circlename}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_new_event_user_intervention_datapoint_identification_failure_non_did_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and no did parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIID)

    def test_new_event_user_intervention_datapoint_identification_failure_invalid_did_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and did parameter is invalid '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for did in dids:
            parameters={'did':did}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIID)

    def test_new_event_user_intervention_datapoint_identification_failure_non_date_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and no date parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':uuid.uuid4().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDT)

    def test_new_event_user_intervention_datapoint_identification_failure_invalid_date_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and date parameter is invalid '''
        uid=uuid.uuid4()
        did=uuid.uuid4().hex
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        dates=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1(), uuid.uuid4().hex, {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for date in dates:
            parameters={'did':did, 'date':date}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDT)

    def test_new_event_user_intervention_datapoint_identification_failure_non_doubts_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and no doubts parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':uuid.uuid4().hex, 'date':uuid.uuid1().hex}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDO)

    def test_new_event_user_intervention_datapoint_identification_failure_invalid_doubts_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and doubts parameter is invalid '''
        uid=uuid.uuid4()
        did=uuid.uuid4().hex
        date=uuid.uuid1().hex
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts_a=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1(), uuid.uuid4().hex, {'a':'dict'},('a','tuple'),{'set'}]
        for doubts in doubts_a:
            parameters={'did':did, 'date':date, 'doubts':doubts}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDO)

    def test_new_event_user_intervention_datapoint_identification_failure_non_discarded_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and no discarded parameter is passed '''
        uid=uuid.uuid4()
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':uuid.uuid4().hex, 'date':uuid.uuid1().hex, 'doubts':[]}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDI)

    def test_new_event_user_intervention_datapoint_identification_failure_invalid_discarded_parameter_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and discarded parameter is invalid '''
        uid=uuid.uuid4()
        did=uuid.uuid4().hex
        date=uuid.uuid1().hex
        doubts=[]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        discarded_a=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1(), uuid.uuid4().hex, {'a':'dict'},('a','tuple'),{'set'}]
        for discarded in discarded_a:
            parameters={'did':did, 'date':date, 'doubts':doubts, 'discarded':discarded}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDI)

    def test_new_event_user_intervention_datapoint_identification_failure_invalid_doubts_items_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and doubts item is invalid '''
        uid=uuid.uuid4()
        did=uuid.uuid4().hex
        date=uuid.uuid1().hex
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        items_a=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex, {'a':'dict'},('a','tuple'),{'set'}]
        for item in items_a:
            parameters={'did':did, 'date':date, 'doubts':[item], 'discarded':[]}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDOP)

    def test_new_event_user_intervention_datapoint_identification_failure_invalid_discarded_items_passed(self):
        ''' new_event should fail if event_type is USER_INTERVENTION_DATAPOINT_IDENTIFICATION and discarded item is invalid '''
        uid=uuid.uuid4()
        did=uuid.uuid4().hex
        date=uuid.uuid1().hex
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        items_a=[None,234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex, {'a':'dict'},('a','tuple'),{'set'}]
        for item in items_a:
            parameters={'did':did, 'date':date, 'doubts':[uuid.uuid4().hex, uuid.uuid4().hex], 'discarded':[item]}
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.new_event(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, errors.E_EAU_NEWE_UIDIIDIP)

    def test_new_event_user_intervention_datapoint_identification_success(self):
        ''' new_event should succeed '''
        uid=uuid.uuid4()
        did=uuid.uuid4().hex
        date=uuid.uuid1().hex
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did, 'date':date, 'doubts':doubts, 'discarded':discarded}
        self.assertTrue(user.new_event(uid=uid, event_type=event_type, parameters=parameters))

    def test_insert_new_user_event_failure_invalid_uid(self):
        ''' insert_new_user_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        username='test_insert_new_user_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_user_event(uid=uid, username=username)
            self.assertEqual(cm.exception.error, errors.E_EAU_INUE_IU)

    def test_insert_new_user_event_failure_invalid_username(self):
        ''' insert_new_user_event should fail if uid is invalid '''
        usernames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for username in usernames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_user_event(uid=uid, username=username)
            self.assertEqual(cm.exception.error, errors.E_EAU_INUE_IUS)

    def test_insert_new_user_event_success(self):
        ''' insert_new_user_event should succeed if parameters as valid '''
        username='test_insert_new_user_event_success'
        uid=uuid.uuid4()
        self.assertTrue(user.insert_new_user_event(uid=uid, username=username))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_USER)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_USER)

    def test_insert_new_agent_event_failure_invalid_uid(self):
        ''' insert_new_agent_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        aid=uuid.uuid4()
        agentname='test_insert_new_agent_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_agent_event(uid=uid, aid=aid, agentname=agentname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INAE_IU)

    def test_insert_new_agent_event_failure_invalid_aid(self):
        ''' insert_new_agent_event should fail if aid is invalid '''
        aids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        agentname='test_insert_new_agent_event_failure'
        for aid in aids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_agent_event(uid=uid, aid=aid, agentname=agentname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INAE_IA)

    def test_insert_new_agent_event_failure_invalid_agentname(self):
        ''' insert_new_agent_event should fail if uid is invalid '''
        agentnames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        for agentname in agentnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_agent_event(uid=uid, aid=aid, agentname=agentname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INAE_IAN)

    def test_insert_new_agent_event_success(self):
        ''' insert_new_agent_event should succeed if parameters as valid '''
        agentname='test_insert_new_agent_event_success'
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        self.assertTrue(user.insert_new_agent_event(uid=uid, aid=aid, agentname=agentname))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_AGENT)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_AGENT)

    def test_insert_new_widget_event_failure_invalid_uid(self):
        ''' insert_new_widget_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        wid=uuid.uuid4()
        widgetname='test_insert_new_widget_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INWGE_IU)

    def test_insert_new_widget_event_failure_invalid_wid(self):
        ''' insert_new_widget_event should fail if wid is invalid '''
        wids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        widgetname='test_insert_new_widget_event_failure'
        for wid in wids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INWGE_IWID)

    def test_insert_new_widget_event_failure_invalid_widgetname(self):
        ''' insert_new_widget_event should fail if uid is invalid '''
        widgetnames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        for widgetname in widgetnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INWGE_IWN)

    def test_insert_new_widget_event_success(self):
        ''' insert_new_widget_event should succeed if parameters as valid '''
        widgetname='test_insert_new_widget_event_success'
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        self.assertTrue(user.insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_WIDGET)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_WIDGET)

    def test_insert_new_dashboard_event_failure_invalid_uid(self):
        ''' insert_new_dashboard_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        bid=uuid.uuid4()
        dashboardname='test_insert_new_dashboard_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDBE_IU)

    def test_insert_new_dashboard_event_failure_invalid_bid(self):
        ''' insert_new_dashboard_event should fail if bid is invalid '''
        bids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        dashboardname='test_insert_new_dashboard_event_failure'
        for bid in bids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDBE_IBID)

    def test_insert_new_dashboard_event_failure_invalid_dashboardname(self):
        ''' insert_new_dashboard_event should fail if uid is invalid '''
        dashboardnames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        for dashboardname in dashboardnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDBE_IDBN)

    def test_insert_new_dashboard_event_success(self):
        ''' insert_new_dashboard_event should succeed if parameters as valid '''
        dashboardname='test_insert_new_dashboard_event_success'
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        self.assertTrue(user.insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_DASHBOARD)

    def test_insert_new_circle_event_failure_invalid_uid(self):
        ''' insert_new_circle_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        cid=uuid.uuid4()
        circlename='test_insert_new_circle_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_circle_event(uid=uid, cid=cid, circlename=circlename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INCE_IU)

    def test_insert_new_circle_event_failure_invalid_cid(self):
        ''' insert_new_circle_event should fail if cid is invalid '''
        cids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        circlename='test_insert_new_circle_event_failure'
        for cid in cids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_circle_event(uid=uid, cid=cid, circlename=circlename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INCE_ICID)

    def test_insert_new_circle_event_failure_invalid_circlename(self):
        ''' insert_new_circle_event should fail if uid is invalid '''
        circlenames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        for circlename in circlenames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_circle_event(uid=uid, cid=cid, circlename=circlename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INCE_ICN)

    def test_insert_new_circle_event_success(self):
        ''' insert_new_circle_event should succeed if parameters as valid '''
        circlename='test_insert_new_circle_event_success'
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        self.assertTrue(user.insert_new_circle_event(uid=uid, cid=cid, circlename=circlename))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_CIRCLE)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_CIRCLE)

    def test_insert_new_datasource_event_failure_invalid_uid(self):
        ''' insert_new_datasource_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        did=uuid.uuid4()
        aid=uuid.uuid4()
        datasourcename='test_insert_new_datasource_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDSE_IU)

    def test_insert_new_datasource_event_failure_invalid_aid(self):
        ''' insert_new_datasource_event should fail if aid is invalid '''
        aids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        did=uuid.uuid4()
        uid=uuid.uuid4()
        datasourcename='test_insert_new_datasource_event_failure'
        for aid in aids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDSE_IA)

    def test_insert_new_datasource_event_failure_invalid_did(self):
        ''' insert_new_datasource_event should fail if did is invalid '''
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        datasourcename='test_insert_new_datasource_event_failure'
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDSE_IDID)

    def test_insert_new_datasource_event_failure_invalid_datasourcename(self):
        ''' insert_new_datasource_event should fail if datasourcename is invalid '''
        datasourcenames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        for datasourcename in datasourcenames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDSE_IDSN)

    def test_insert_new_datasource_event_success(self):
        ''' insert_new_datasource_event should succeed if parameters as valid '''
        datasourcename='test_insert_new_datasource_event_success'
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertTrue(user.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_DATASOURCE)

    def test_insert_new_datapoint_event_failure_invalid_uid(self):
        ''' insert_new_datapoint_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='test_insert_new_datapoint_event_failure'
        datasourcename='test_insert_new_datapoint_event_failure'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datapoint_event(uid=uid, pid=pid, did=did, datasourcename=datasourcename, datapointname=datapointname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDPE_IU)

    def test_insert_new_datapoint_event_failure_invalid_pid(self):
        ''' insert_new_datapoint_event should fail if pid is invalid '''
        pids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        did=uuid.uuid4()
        uid=uuid.uuid4()
        datapointname='test_insert_new_datapoint_event_failure'
        datasourcename='test_insert_new_datapoint_event_failure'
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datapoint_event(uid=uid, pid=pid, did=did, datasourcename=datasourcename, datapointname=datapointname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDPE_IPID)

    def test_insert_new_datapoint_event_failure_invalid_did(self):
        ''' insert_new_datapoint_event should fail if did is invalid '''
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='test_insert_new_datapoint_event_failure'
        datasourcename='test_insert_new_datapoint_event_failure'
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datapoint_event(uid=uid, pid=pid, did=did, datasourcename=datasourcename, datapointname=datapointname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDPE_IDID)

    def test_insert_new_datapoint_event_failure_invalid_datapointname(self):
        ''' insert_new_datapoint_event should fail if datapointname is invalid '''
        datapointnames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        datasourcename='test_insert_new_datapoint_event_failure'
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        did=uuid.uuid4()
        for datapointname in datapointnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datapoint_event(uid=uid, pid=pid, did=did, datasourcename=datasourcename, datapointname=datapointname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDPE_IDPN)

    def test_insert_new_datapoint_event_failure_invalid_datasourcename(self):
        ''' insert_new_datapoint_event should fail if datasourcename is invalid '''
        datasourcenames=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        datapointname='test_insert_new_datapoint_event_failure'
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        did=uuid.uuid4()
        for datasourcename in datasourcenames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_new_datapoint_event(uid=uid, pid=pid, did=did, datasourcename=datasourcename, datapointname=datapointname)
            self.assertEqual(cm.exception.error, errors.E_EAU_INDPE_IDSN)

    def test_insert_new_datapoint_event_success(self):
        ''' insert_new_datapoint_event should succeed if parameters as valid '''
        datapointname='test_insert_new_datapoint_event_success'
        datasourcename='test_insert_new_datapoint_event_success'
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertTrue(user.insert_new_datapoint_event(uid=uid, pid=pid, did=did, datasourcename=datasourcename, datapointname=datapointname))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['type'], types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)
        self.assertEqual(events[0]['priority'], priorities.USER_EVENT_NOTIFICATION_NEW_DATAPOINT)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_uid(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        doubts=[]
        discarded=[]
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
            self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IUID)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_did(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if did is invalid '''
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        doubts=[]
        discarded=[]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
            self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IDID)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_date(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if date is invalid '''
        dates=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        did=uuid.uuid4()
        doubts=[]
        discarded=[]
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
            self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IDT)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_doubts_list(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if doubts is not a list '''
        doubts_s=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        discarded=[]
        for doubts in doubts_s:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
            self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IDOU)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_discarded_list(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if discarded is not a list '''
        discarded_s=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        doubts=[]
        for discarded in discarded_s:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
            self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IDIS)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_doubts_item(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if doubts item is not a pid '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        discarded=[]
        doubts=[32,23]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
        self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IDOUP)

    def test_insert_event_user_intervention_datapoint_identification_failure_invalid_discarded_item(self):
        ''' insert_event_user_intervention_datapoint_identification should fail if discarded item is not a pid '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        doubts=[]
        discarded=[32,23]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded)
        self.assertEqual(cm.exception.error, errors.E_EAU_INEUIDI_IDISP)

    def test_insert_event_user_intervention_datapoint_identification_success(self):
        ''' insert_event_user_intervention_datapoint_identification should succeed '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        doubts=[uuid.uuid4(), uuid.uuid4()]
        discarded=[uuid.uuid4(), uuid.uuid4()]
        self.assertTrue(user.insert_event_user_intervention_datapoint_identification(uid=uid, did=did, date=date, doubts=doubts, discarded=discarded))

