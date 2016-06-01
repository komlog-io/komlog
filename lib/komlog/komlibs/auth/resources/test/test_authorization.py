import unittest
import uuid
from komlog.komlibs.auth import permissions, exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.resources import authorization
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komfig import logging


class AuthResourcesAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.resources.authorization tests '''
    
    def setUp(self):
        username = 'test_komlibs.auth.resources.authorization_user'
        password = 'password'
        email = 'test_komlibs.auth.resources.authorization_user@komlog.org'
        try:
            uid = userapi.get_uid(username=username)
            self.user=userapi.get_user_config(uid=uid)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)
        

    def test_authorize_get_agent_config_success(self):
        ''' authorize_get_agent_config should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_get_agent_config(uid=uid, aid=aid))

    def test_authorize_get_agent_config_failure(self):
        ''' authorize_get_agent_config should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_agent_config(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGAC_RE)

    def test_authorize_get_datasource_config_success(self):
        ''' authorize_get_datasource_config should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_config_failure(self):
        ''' authorize_get_datasource_config should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_config(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSC_RE)

    def test_authorize_put_datasource_config_success(self):
        ''' authorize_put_datasource_config should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_put_datasource_config(uid=uid, did=did))

    def test_authorize_put_datasource_config_failure(self):
        ''' authorize_put_datasource_config should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_datasource_config(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APDSC_RE)

    def test_authorize_get_datasource_data_success(self):
        ''' authorize_get_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_get_datasource_data(uid=uid, did=did))

    def test_authorize_get_datasource_data_failure(self):
        ''' authorize_get_datasource_data should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSD_RE)

    def test_authorize_post_datasource_data_success(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure(self):
        ''' authorize_post_datasource_data should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDSD_RE)

    def test_authorize_post_datasource_data_failure_no_user_agent_perm(self):
        ''' authorize_post_datasource_data should fail if not user_agent perm is found '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDSD_RE)

    def test_authorize_post_datasource_data_failure_no_user_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDSD_RE)

    def test_authorize_post_datapoint_data_failure_invalid_aid(self):
        ''' authorize_post_datapoint_data should fail if aid is invalid '''
        uid=uuid.uuid4()
        aids=[None, 'text',12, 222.22, {'a':'dict'}, {'set'}, ['a','list'],('tuple','yes'),{uuid.uuid4()},[uuid.uuid4(),],(uuid.uuid4(),),uuid.uuid1(), uuid.uuid4().hex]
        pid=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.AuthorizationException) as cm:
                authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_ANF)

    def test_authorize_post_datapoint_data_success(self):
        ''' authorize_post_datapoint_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid))

    def test_authorize_post_datapoint_data_failure_no_permission_over_datapoint(self):
        ''' authorize_post_datapoint_data should fail if user has no permission over datapoint '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_RE)

    def test_authorize_post_datapoint_data_failure_no_permission_over_agent(self):
        ''' authorize_post_datapoint_data should fail if user has no permission over agent '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_RE)

    def test_authorize_post_datapoint_data_failure_no_permission_over_agent_nor_datapoint(self):
        ''' authorize_post_datapoint_data should fail if user has no permission over agent nor dp '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_RE)

    def test_authorize_new_datasource_success(self):
        ''' authorize_new_datasource should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_new_datasource(uid=uid, aid=aid))

    def test_authorize_new_datasource_failure(self):
        ''' authorize_new_datasource should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANDS_RE)

    def test_authorize_get_datapoint_data_success(self):
        ''' authorize_get_datapoint_data should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_get_datapoint_data(uid=uid, pid=pid))

    def test_authorize_get_datapoint_data_failure(self):
        ''' authorize_get_datapoint_data should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPD_RE)

    def test_authorize_get_datapoint_config_success(self):
        ''' authorize_get_datapoint_config should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_get_datapoint_config_failure(self):
        ''' authorize_get_datapoint_config should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_config(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPC_RE)

    def test_authorize_put_datapoint_config_success(self):
        ''' authorize_put_datapoint_config should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_put_datapoint_config(uid=uid, pid=pid))

    def test_authorize_put_datapoint_config_failure(self):
        ''' authorize_put_datapoint_config should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_datapoint_config(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APDPC_RE)

    def test_authorize_new_datasource_datapoint_success(self):
        ''' authorize_new_datasource_datapoint should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_new_datasource_datapoint(uid=uid, did=did))

    def test_authorize_new_datasource_datapoint_failure(self):
        ''' authorize_new_datasource_datapoint should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource_datapoint(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANDSDP_RE)

    def test_authorize_new_user_datapoint_failure_invalid_aid(self):
        ''' authorize_new_user_datapoint should fail if aid is invalid '''
        aids=[None, 'text',12, 222.22, {'a':'dict'}, {'set'}, ['a','list'],('tuple','yes'),{uuid.uuid4()},[uuid.uuid4(),],(uuid.uuid4(),),uuid.uuid1(), uuid.uuid4().hex]
        uid=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.AuthorizationException) as cm:
                authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
            self.assertEqual(cm.exception.error, Errors.E_ARA_ANUDP_IA)

    def test_authorize_new_user_datapoint_failure_no_permission_found(self):
        ''' authorize_new_user_datapoint should fail if no permission is found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANUDP_RE)

    def test_authorize_new_user_datapoint_success(self):
        ''' authorize_new_user_datapoint should succeed if user has permission over agent '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        self.assertTrue(cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm))
        self.assertIsNone(authorization.authorize_new_user_datapoint(uid=uid, aid=aid))

    def test_authorize_put_agent_config_success(self):
        ''' authorize_put_agent_config should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_put_agent_config(uid=uid, aid=aid))

    def test_authorize_put_agent_config_failure(self):
        ''' authorize_put_agent_config should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_agent_config(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APAC_RE)

    def test_authorize_get_widget_config_success(self):
        ''' authorize_get_widget_config should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_get_widget_config(uid=uid, wid=wid))

    def test_authorize_get_widget_config_failure(self):
        ''' authorize_get_widget_config should fail if permission is not granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_widget_config(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGWC_RE)

    def test_authorize_put_widget_config_success(self):
        ''' authorize_put_widget_config should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_put_widget_config(uid=uid, wid=wid))

    def test_authorize_put_widget_config_failure(self):
        ''' authorize_put_widget_config should fail if permission is not granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_widget_config(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APWC_RE)

    def test_authorize_get_dashboard_config_success(self):
        ''' authorize_get_dashboard_config should succeed if permission is granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_get_dashboard_config(uid=uid, bid=bid))

    def test_authorize_get_dashboard_config_failure(self):
        ''' authorize_get_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_dashboard_config(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDBC_RE)

    def test_authorize_put_dashboard_config_success(self):
        ''' authorize_put_dashboard_config should succeed if permission is granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_put_dashboard_config(uid=uid, bid=bid))

    def test_authorize_put_dashboard_config_failure(self):
        ''' authorize_put_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_dashboard_config(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APDBC_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_bid(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no permissions over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_bid_edit_perm(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no edit permission over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_wid(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no edit permission over wid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_wid_read_perm(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no read permission over wid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_success(self):
        ''' authorize_add_widget_to_dashboard should succeed '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_delete_widget_from_dashboard_failure_no_bid(self):
        ''' authorize_delete_widget_from_dashboard should fail if user has no permissions over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_widget_from_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADWFDB_RE)

    def test_authorize_delete_widget_from_dashboard_failure_no_bid_edit_perm(self):
        ''' authorize_delete_widget_to_dashboard should fail if user has no edit permission over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_widget_from_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADWFDB_RE)

    def test_authorize_delete_widget_from_dashboard_success(self):
        ''' authorize_delete_widget_from_dashboard should succeed '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_widget_from_dashboard(uid=uid,bid=bid))

    def test_authorize_delete_dashboard_failure_non_existent_bid(self):
        ''' authorize_delete_dashboard should fail if no bid exists '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDB_RE)

    def test_authorize_delete_dashboard_failure_no_delete_perm(self):
        ''' authorize_delete_dashboard should fail if user has no delete perm over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDB_RE)

    def test_authorize_delete_dashboard_success(self):
        ''' authorize_delete_dashboard should succeed if user has delete perm over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_dashboard(uid=uid, bid=bid))

    def test_authorize_add_datapoint_to_widget_failure_non_existent_wid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has not the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_no_edit_perm_over_wid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_non_existent_pid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_no_read_perm_over_pid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_success(self):
        ''' authorize_add_datapoint_to_widget should succeed if user has permissions over pid and wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_delete_datapoint_from_widget_failure_non_existent_wid(self):
        ''' authorize_delete_datapoint_from_widget should fail if user has not the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFW_RE)

    def test_authorize_delete_datapoint_from_widget_failure_no_edit_perm_over_wid(self):
        ''' authorize_delete_datapoint_from_widget should fail if user has not edit perm over the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFW_RE)

    def test_authorize_delete_datapoint_from_widget_success(self):
        ''' authorize_delete_datapoint_from_widget should succeed if user has permssion over the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid))

    def test_authorize_new_snapshot_failure_non_existent_wid(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_failure_non_existent_uid(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_success(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_new_snapshot(uid=uid,wid=wid))

    def test_authorize_get_snapshot_data_failure_non_existent_nid(self):
        ''' authorize_get_snapshot_data should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_data(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSD_RE)

    def test_authorize_get_snapshot_data_failure_non_existent_uid(self):
        ''' authorize_get_snapshot_data should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_data(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSD_RE)

    def test_authorize_get_snapshot_data_success(self):
        ''' authorize_get_snapshot_data should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertIsNone(authorization.authorize_get_snapshot_data(uid=uid,nid=nid))

    def test_authorize_get_snapshot_config_failure_non_existent_nid(self):
        ''' authorize_get_snapshot_config should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSC_RE)

    def test_authorize_get_snapshot_config_failure_non_existent_uid(self):
        ''' authorize_get_snapshot_config should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSC_RE)

    def test_authorize_get_snapshot_config_success(self):
        ''' authorize_get_snapshot_config should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertIsNone(authorization.authorize_get_snapshot_config(uid=uid,nid=nid))

    def test_authorize_delete_snapshot_failure_non_existent_uid(self):
        ''' authorize_delete_snapshot should fail if uid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_snapshot(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADS_RE)

    def test_authorize_delete_snapshot_failure_non_existent_nid(self):
        ''' authorize_delete_snapshot should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_snapshot(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADS_RE)

    def test_authorize_delete_snapshot_success(self):
        ''' authorize_delete_snapshot should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_snapshot(uid=uid,nid=nid))

    def test_authorize_get_circle_config_failure_non_existent_uid(self):
        ''' authorize_get_circle_config should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_circle_config(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGCC_RE)

    def test_authorize_get_circle_config_success(self):
        ''' authorize_get_circle_config should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_get_circle_config(uid=uid,cid=cid))

    def test_authorize_delete_circle_failure_non_existent_uid(self):
        ''' authorize_delete_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADC_RE)

    def test_authorize_delete_circle_failure_non_existent_cid(self):
        ''' authorize_delete_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADC_RE)

    def test_authorize_delete_circle_success(self):
        ''' authorize_delete_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_circle(uid=uid,cid=cid))

    def test_authorize_update_circle_config_failure_non_existent_uid(self):
        ''' authorize_update_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_update_circle_config(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUCC_RE)

    def test_authorize_update_circle_config_failure_non_existent_cid(self):
        ''' authorize_update_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_update_circle_config(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUCC_RE)

    def test_authorize_update_circle_config_success(self):
        ''' authorize_update_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_update_circle_config(uid=uid,cid=cid))

    def test_authorize_add_member_to_circle_failure_non_existent_uid(self):
        ''' authorize_add_member_to_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_member_to_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAMTC_RE)

    def test_authorize_add_member_to_circle_failure_non_existent_cid(self):
        ''' authorize_add_member_to_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_member_to_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAMTC_RE)

    def test_authorize_add_member_to_circle_success(self):
        ''' authorize_add_member_to_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_add_member_to_circle(uid=uid,cid=cid))

    def test_authorize_delete_member_from_circle_failure_non_existent_uid(self):
        ''' authorize_delete_member_from_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_member_from_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADMFC_RE)

    def test_authorize_delete_member_from_circle_failure_non_existent_cid(self):
        ''' authorize_delete_member_from_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_member_from_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADMFC_RE)

    def test_authorize_delete_member_from_circle_success(self):
        ''' authorize_delete_member_from_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_member_from_circle(uid=uid,cid=cid))

    def test_authorize_dissociate_datapoint_from_datasource_failure_non_existent_pid(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user has not the pid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFDS_RE)

    def test_authorize_dissociate_datapoint_from_datasource_failure_non_existent_uid(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user does not exist '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFDS_RE)

    def test_authorize_dissociate_datapoint_from_datasource_failure_non_enought_perms(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user has not the necessary permissions '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFDS_RE)

    def test_authorize_dissociate_datapoint_from_datasource_success(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user has the necessary permissions over datapoint '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid))

