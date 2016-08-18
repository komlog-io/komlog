import unittest
import uuid
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komcass.model.orm import datapoint as ormdatapoint
from komlog.komlibs.auth.quotes import authorization
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.gestaccount.user import api as gestuserapi
from komlog.komlibs.general.time import timeuuid

class AuthQuotesAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.quotes.authorization tests '''
    
    def test_authorize_new_agent_success(self):
        ''' authorize_new_agent should execute successfully if user has no quote restrictions '''
        uid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_agent(uid=uid))

    def test_authorize_new_agent_failure(self):
        ''' authorize_new_agent should raise an exception if user has quote restrictions '''
        uid=uuid.uuid4()
        iface=interfaces.User_AgentCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_agent(uid=uid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANA_QE)

    def test_authorize_new_datasource_success(self):
        ''' authorize_new_datasource should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_datasource(uid=uid, aid=aid))

    def test_authorize_new_datasource_failure_invalid_aid(self):
        ''' authorize_new_datasource should fail if aid is invalid '''
        uid=uuid.uuid4()
        aid=uuid.uuid4().hex
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDS_IA)

    def test_authorize_new_datasource_failure_agent_restriction(self):
        ''' authorize_new_datasource should fail if agent has quote restrictions '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        iface=interfaces.Agent_DatasourceCreation(aid).value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDS_QE)

    def test_authorize_new_datasource_failure_user_restriction(self):
        ''' authorize_new_datasource should fail if user has quote restrictions '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        iface=interfaces.User_DatasourceCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDS_QE)

    def test_authorize_new_datasource_datapoint_failure_datasource_not_found(self):
        ''' authorize_new_datasource_datapoint should fail if datasource does not exist '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            authorization.authorize_new_datasource_datapoint(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDSDP_DSNF)

    def test_authorize_new_datasource_datapoint_non_existent_datasource(self):
        ''' authorize_new_datasource_datapoint should fail if datasource does not exist '''
        username = 'test_authorize_new_datasource_datapoint_non_existent_datasource_user'
        password = 'password'
        email = username+'@komlog.org'
        user = gestuserapi.create_user(username=username, password=password, email=email)
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, authorization.authorize_new_datasource_datapoint, uid=user['uid'], did=did)

    def test_authorize_new_datasource_datapoint_success(self):
        ''' authorize_new_datasource_datapoint should succeed if no quote restriction is found  '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        datasourcename='datasourcename'
        creation_date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename=datasourcename, creation_date=creation_date)
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        self.assertIsNone(authorization.authorize_new_datasource_datapoint(uid=uid, did=did))

    def test_authorize_new_datasource_datapoint_failure_user_datapoint_creation_limit(self):
        ''' authorize_new_datasource_datapoint should fail if user has reached his datapoint creation limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        datasourcename='datasourcename'
        creation_date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename=datasourcename, creation_date=creation_date)
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DatapointCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource_datapoint(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDSDP_QE)

    def test_authorize_new_datasource_datapoint_failure_agent_datapoint_creation_limit(self):
        ''' authorize_new_datasource_datapoint should fail if agent has reached his datapoint creation limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        datasourcename='datasourcename'
        creation_date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename=datasourcename, creation_date=creation_date)
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.Agent_DatapointCreation(aid).value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource_datapoint(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDSDP_QE)

    def test_authorize_new_datasource_datapoint_failure_datasource_datapoint_creation_limit(self):
        ''' authorize_new_datasource_datapoint should fail if datasource has reached his datapoint creation limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        datasourcename='datasourcename'
        creation_date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename=datasourcename, creation_date=creation_date)
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.Datasource_DatapointCreation(did).value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource_datapoint(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDSDP_QE)

    def test_authorize_new_user_datapoint_failure_aid_not_valid(self):
        ''' authorize_new_user_datapoint should fail if aid is not valid '''
        aids=[None, 'text',12, 222.22, {'a':'dict'}, {'set'}, ['a','list'],('tuple','yes'),{uuid.uuid4()},[uuid.uuid4(),],(uuid.uuid4(),),uuid.uuid1(), uuid.uuid4().hex]
        uid=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.AuthorizationException) as cm:
                authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
            self.assertEqual(cm.exception.error, Errors.E_AQA_ANUDP_IA)

    def test_authorize_new_user_datapoint_failure_user_datapoint_creation_deny(self):
        ''' authorize_new_user_datapoint should fail if user datapoint creation deny is found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        iface=interfaces.User_DatapointCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANUDP_QE)

    def test_authorize_new_user_datapoint_failure_agent_datapoint_creation_deny(self):
        ''' authorize_new_user_datapoint should fail if user datapoint creation deny is found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        iface=interfaces.Agent_DatapointCreation(aid).value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANUDP_QE)

    def test_authorize_new_user_datapoint_failure_user_and_agent_datapoint_creation_deny(self):
        ''' authorize_new_user_datapoint should fail if user datapoint creation deny is found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        iface=interfaces.User_DatapointCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        iface=interfaces.Agent_DatapointCreation(aid).value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANUDP_QE)

    def test_authorize_new_user_datapoint_success(self):
        ''' authorize_new_user_datapoint should succeed if no deny is found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_user_datapoint(uid=uid, aid=aid))

    def test_authorize_new_widget_success(self):
        ''' authorize_new_widget should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_widget(uid=uid))

    def test_authorize_new_widget_failure_user_widget_creation_limit(self):
        ''' authorize_new_widget should fail if user has reached his widget creation limit '''
        uid=uuid.uuid4()
        iface=interfaces.User_WidgetCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_widget(uid=uid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANW_QE)

    def test_authorize_new_dashboard_success(self):
        ''' authorize_new_dashboard should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_dashboard(uid=uid))

    def test_authorize_new_dashboard_failure_user_dashboard_creation_limit(self):
        ''' authorize_new_dashboard should fail if user has reached his dashboard creation limit '''
        uid=uuid.uuid4()
        iface=interfaces.User_DashboardCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_dashboard(uid=uid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANDB_QE)

    def test_authorize_new_snapshot_success(self):
        ''' authorize_new_snapshot should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_snapshot(uid=uid))

    def test_authorize_new_snapshot_failure_user_snapshot_creation_limit(self):
        ''' authorize_new_snapshot should fail if user has reached his snapshot creation limit '''
        uid=uuid.uuid4()
        iface=interfaces.User_SnapshotCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=uid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANS_QE)

    def test_authorize_new_circle_success(self):
        ''' authorize_new_circle should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_new_circle(uid=uid))

    def test_authorize_new_circle_failure_user_circle_creation_limit(self):
        ''' authorize_new_circle should fail if user has reached his circle creation limit '''
        uid=uuid.uuid4()
        iface=interfaces.User_CircleCreation().value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_circle(uid=uid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_ANC_QE)

    def test_authorize_add_member_to_circle_success(self):
        ''' authorize_add_member_to_circle should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_add_member_to_circle(uid=uid, cid=cid))

    def test_authorize_add_member_to_circle_failure_circle_member_limit(self):
        ''' authorize_add_member_to_circle should fail if circle has reached its member limit '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        iface=interfaces.User_AddMemberToCircle(cid).value
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_member_to_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AAMTC_QE)

    def test_authorize_post_datasource_data_success(self):
        ''' authorize_post_datasource_data should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertIsNone(authorization.authorize_post_datasource_data(uid=uid, did=did))

    def test_authorize_post_datasource_data_success_user_daily_quote_reached_other_day(self):
        ''' authorize_post_datasource_data should success if user reached his daily quote but not today '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1(seconds=1))
        iface=interfaces.User_PostDatasourceDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        self.assertIsNone(authorization.authorize_post_datasource_data(uid=uid, did=did))

    def test_authorize_post_datasource_data_success_datasource_daily_quote_reached_other_day(self):
        ''' authorize_post_datasource_data should succeed if datasource reached his daily quote but not today '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1(seconds=1))
        iface=interfaces.User_PostDatasourceDataDaily(did).value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        self.assertIsNone(authorization.authorize_post_datasource_data(uid=uid, did=did))

    def test_authorize_post_datasource_data_failure_user_daily_quote_reached(self):
        ''' authorize_post_datasource_data should fail if user has reached his daily upload quote '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDatasourceDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDSD_QE)

    def test_authorize_post_datasource_data_failure_datasource_daily_quote_reached(self):
        ''' authorize_post_datasource_data should fail if datasource has reached his daily upload quote '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDatasourceDataDaily(did).value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDSD_QE)

    def test_authorize_post_datasource_data_failure_data_post_daily_quote_reached(self):
        ''' authorize_post_datasource_data should fail if data post daily quote has been reached '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDSD_QE)

    def test_authorize_get_datasource_data_failure_datasource_not_found(self):
        ''' authorize_get_datasource_data should fail if datasource does not exist '''
        did=uuid.uuid4()
        ii=None
        ie=None
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_DSNF)

    def test_authorize_post_datapoint_data_success(self):
        ''' authorize_post_datapoint_data should return None if there is no quote restriction '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertIsNone(authorization.authorize_post_datapoint_data(uid=uid, pid=pid))

    def test_authorize_post_datapoint_data_success_user_daily_quote_reached_other_day(self):
        ''' authorize_post_datapoint_data should success if user reached his daily quote but not today '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1(seconds=1))
        iface=interfaces.User_PostDatapointDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        self.assertIsNone(authorization.authorize_post_datapoint_data(uid=uid, pid=pid))

    def test_authorize_post_datapoint_data_success_datapoint_daily_quote_reached_other_day(self):
        ''' authorize_post_datapoint_data should success if datapoint reached his daily quote but not today '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1(seconds=1))
        iface=interfaces.User_PostDatapointDataDaily(pid).value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        self.assertIsNone(authorization.authorize_post_datapoint_data(uid=uid, pid=pid))

    def test_authorize_post_datapoint_data_failure_user_daily_quote_reached(self):
        ''' authorize_post_datapoint_data should fail if user has reached his daily upload quote '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDatapointDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDPD_QE)

    def test_authorize_post_datapoint_data_failure_datapoint_daily_quote_reached(self):
        ''' authorize_post_datapoint_data should fail if datapoint has reached his daily upload quote '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDatapointDataDaily(pid).value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDPD_QE)

    def test_authorize_post_datapoint_data_failure_datapoint_and_user_daily_quote_reached(self):
        ''' authorize_post_datapoint_data should fail if datapoint and user have reached his daily upload quote '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDatapointDataDaily(pid).value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        iface=interfaces.User_PostDatapointDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts, 'A'))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDPD_QE)

    def test_authorize_post_datapoint_data_failure_data_daily_quote_reached(self):
        ''' authorize_post_datapoint_data should fail if data daily quote has been reached '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
        iface=interfaces.User_PostDataDaily().value
        self.assertTrue(cassapiiface.insert_user_ts_iface_deny(uid, iface, ts))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_AQA_APDPD_QE)

    def test_authorize_get_datasource_data_success_no_interface_limit_found_no_interval_set(self):
        ''' authorize_get_datasource_data should return None if limit is not found and interval 
            dates are not set '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=None
        ie=None
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        self.assertIsNone(authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_success_no_interface_limit_found_interval_set(self):
        ''' authorize_get_datasource_data should return None if limit is not found and interval 
            dates are set '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.uuid1(seconds=1000)
        ie=timeuuid.uuid1(seconds=1100)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        self.assertIsNone(authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_failure_interface_limit_found_no_interval_set(self):
        ''' authorize_get_datasource_data should fail if limit is found and interval 
            dates are not set '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=None
        ie=None
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datasource_data_failure_interface_limit_found_ii_set_less_than_limit(self):
        ''' authorize_get_datasource_data should fail if limit is found and interval requested is
            before the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datasource_data_failure_interface_limit_found_ii_and_ie_set_less_than_limit(self):
        ''' authorize_get_datasource_data should fail if limit is found and interval requested is
            before the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=100)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datasource_data_failure_interface_limit_found_ii_set_less_than_limit_ie_not_set(self):
        ''' authorize_get_datasource_data should fail if limit is found and interval requested is
            before the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.uuid1(seconds=1)
        ie=None
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datasource_data_failure_interface_limit_found_ie_set_less_than_limit_ii_not_set(self):
        ''' authorize_get_datasource_data should fail if limit is found and interval requested is
            before the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=None
        ie=timeuuid.uuid1(seconds=1)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datasource_data_success_interface_limit_found_ii_and_ie_set_more_than_limit(self):
        ''' authorize_get_datasource_data should succeed if limit is found but interval requested is
            after the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.max_uuid_from_time(500)
        ie=timeuuid.max_uuid_from_time(500)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_success_interface_limit_found_ii_set_equal_than_limit(self):
        ''' authorize_get_datasource_data should succeed if limit is found but interval requested is
            equal the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.min_uuid_from_time(1000)
        ie=timeuuid.max_uuid_from_time(1000)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(1000)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_success_interface_limit_found_ii_and_ie_set_equal_than_limit(self):
        ''' authorize_get_datasource_data should succeed if limit is found but interval requested is
            equal the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.min_uuid_from_time(1000)
        ie=timeuuid.min_uuid_from_time(1000)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(1000)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_failure_interface_limit_found_ii_set_less_than_limit_ie_set_equal_limit(self):
        ''' authorize_get_datasource_data should fail if limit is found and interval requested is
            before the limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        ii=None
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.min_uuid_from_time(1000)
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(1000)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datasource_data(did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDSD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_datapoint_not_found(self):
        ''' authorize_get_datapoint_data should fail if datapoint is not found '''
        pid=uuid.uuid4()
        ii=None
        ie=None
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_DPNF)

    def test_authorize_get_datapoint_data_success_limit_not_found_interval_not_set(self):
        ''' authorize_get_datapoint_data should succeed if limit is not found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        datasourcename='datasource'
        creation_date=timeuuid.uuid1()
        ii=None
        ie=None
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        self.assertIsNone(authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_success_limit_not_found_interval_set(self):
        ''' authorize_get_datapoint_data should succeed if limit is not found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=None
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        self.assertIsNone(authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_failure_limit_found_ii_less_than_limit_ie_more_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_more_than_limit_ie_less_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1(seconds=1000)
        ie=timeuuid.uuid1(seconds=50)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_less_than_limit_ie_not_set(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1(seconds=10)
        ie=None
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_not_set_ie_less_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=None
        ie=timeuuid.uuid1(seconds=50)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_less_than_limit_ie_less_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1(seconds=10)
        ie=timeuuid.uuid1(seconds=50)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_not_set_ie_not_set(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=None
        ie=None
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_not_set_ie_more_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=None
        ie=timeuuid.uuid1(seconds=1000)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_more_than_limit_ie_not_set(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1(seconds=1000)
        ie=None
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_less_than_limit_ie_equal_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.uuid1(seconds=10)
        ie=timeuuid.min_uuid_from_time(500)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_failure_limit_found_ii_equal_than_limit_ie_less_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.min_uuid_from_time(500)
        ie=timeuuid.uuid1(seconds=10)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        with self.assertRaises(exceptions.IntervalBoundsException) as cm:
            authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_AQA_AGDPD_IBE)
        self.assertEqual(cm.exception.data, {'date':minTs})

    def test_authorize_get_datapoint_data_success_limit_found_ii_equal_than_limit_ie_more_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.min_uuid_from_time(500)
        ie=timeuuid.uuid1(seconds=1000)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_success_limit_found_ii_more_than_limit_ie_equal_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.min_uuid_from_time(1000)
        ie=timeuuid.min_uuid_from_time(500)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_success_limit_found_ii_equal_than_limit_ie_equal_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.min_uuid_from_time(500)
        ie=timeuuid.min_uuid_from_time(500)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_success_limit_found_ii_more_than_limit_ie_more_than_limit(self):
        ''' authorize_get_datapoint_data should fail if limit is found  and requested interval is less than limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        datapointname='datapoint'
        creation_date=timeuuid.uuid1()
        ii=timeuuid.max_uuid_from_time(500)
        ie=timeuuid.max_uuid_from_time(500)
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(cassapidatapoint.new_datapoint(datapoint))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        self.assertIsNone(authorization.authorize_get_datapoint_data(pid=pid, ii=ii, ie=ie))

