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
        username='test_get_events_success_username'
        agentname='test_get_events_success_agentname'
        self.assertTrue(user.insert_new_user_event(uid=uid, username=username))
        self.assertTrue(user.insert_new_agent_event(uid=uid, aid=aid, agentname=username))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),2)

    def test_activate_event_failure_invalid_uid(self):
        ''' activate_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=uuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.activate_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_ACE_IU)

    def test_activate_event_failure_invalid_date(self):
        ''' activate_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.activate_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_ACE_ID)

    def test_deactivate_event_failure_invalid_uid(self):
        ''' deactivate_event should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        date=uuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.deactivate_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_DACE_IU)

    def test_deactivate_event_failure_invalid_date(self):
        ''' deactivate_event should fail if date is invalid '''
        dates=[234234, 234234.234234, 'astring',uuid.uuid4(), uuid.uuid1().hex,  {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                user.deactivate_event(uid=uid, date=date)
            self.assertEqual(cm.exception.error, errors.E_EAU_DACE_ID)

    def test_activate_deactivate_event_success(self):
        ''' activate_event and deactivate_event should succeed, for simplicity even if the event does not exist '''
        uid=uuid.uuid4()
        username='test_activate_event_success_username'
        self.assertTrue(user.insert_new_user_event(uid=uid, username=username))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        event=events[0]
        self.assertTrue(user.deactivate_event(uid=uid, date=event['date']))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        event=events[0]
        self.assertEqual(event['active'],False)
        self.assertTrue(user.activate_event(uid=uid, date=event['date']))
        events=user.get_events(uid=uid)
        self.assertEqual(len(events),1)
        event=events[0]
        self.assertEqual(event['active'],True)

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
        self.assertEqual(events[0]['type'], types.NEW_USER)
        self.assertEqual(events[0]['priority'], priorities.NEW_USER)

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
        self.assertEqual(events[0]['type'], types.NEW_AGENT)
        self.assertEqual(events[0]['priority'], priorities.NEW_AGENT)

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
        self.assertEqual(events[0]['type'], types.NEW_WIDGET)
        self.assertEqual(events[0]['priority'], priorities.NEW_WIDGET)

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
        self.assertEqual(events[0]['type'], types.NEW_DASHBOARD)
        self.assertEqual(events[0]['priority'], priorities.NEW_DASHBOARD)

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
        self.assertEqual(events[0]['type'], types.NEW_CIRCLE)
        self.assertEqual(events[0]['priority'], priorities.NEW_CIRCLE)

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
        self.assertEqual(events[0]['type'], types.NEW_DATASOURCE)
        self.assertEqual(events[0]['priority'], priorities.NEW_DATASOURCE)

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
        self.assertEqual(events[0]['type'], types.NEW_DATAPOINT)
        self.assertEqual(events[0]['priority'], priorities.NEW_DATAPOINT)

