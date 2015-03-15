import unittest
import uuid
from komlibs.auth import permissions
from komlibs.auth.resources import authorization
from komcass.api import permission as cassapiperm
from komlibs.gestaccount.user import api as userapi
from komfig import logger


class AuthResourcesAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.resources.authorization tests '''
    
    def setUp(self):
        username = 'test_komlibs.auth.resources.authorization_user'
        password = 'password'
        email = 'test_komlibs.auth.resources.authorization_user@komlog.org'
        try:
            self.user=userapi.get_user_config(username=username)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)
        

    def test_authorize_get_agent_config_success(self):
        ''' authorize_get_agent_config should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertTrue(authorization.authorize_get_agent_config(uid=uid, aid=aid))

    def test_authorize_get_agent_config_failure(self):
        ''' authorize_get_agent_config should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_agent_config(uid=uid, aid=aid))

    def test_authorize_get_datasource_config_success(self):
        ''' authorize_get_datasource_config should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_config_failure(self):
        ''' authorize_get_datasource_config should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_put_datasource_config_success(self):
        ''' authorize_put_datasource_config should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_put_datasource_config(uid=uid, did=did))

    def test_authorize_put_datasource_config_failure(self):
        ''' authorize_put_datasource_config should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_data_success(self):
        ''' authorize_get_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_get_datasource_data(uid=uid, did=did))

    def test_authorize_get_datasource_data_failure(self):
        ''' authorize_get_datasource_data should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datasource_data(uid=uid, did=did))

    def test_authorize_post_datasource_data_success(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure(self):
        ''' authorize_post_datasource_data should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_user_agent_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_user_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_agent_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_new_agent_success(self):
        ''' authorize_new_agent should succeed if permission is granted'''
        uid=self.user['uid']
        self.assertTrue(authorization.authorize_new_agent(uid=uid))

    def test_authorize_new_datasource_success(self):
        ''' authorize_new_datasource should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertTrue(authorization.authorize_new_datasource(uid=uid, aid=aid))

    def test_authorize_new_datasource_failure(self):
        ''' authorize_new_datasource should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        self.assertFalse(authorization.authorize_new_datasource(uid=uid, aid=aid))

    def test_authorize_get_datapoint_data_success(self):
        ''' authorize_get_datapoint_data should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_get_datapoint_data(uid=uid, pid=pid))

    def test_authorize_get_datapoint_data_failure(self):
        ''' authorize_get_datapoint_data should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datapoint_data(uid=uid, pid=pid))

    def test_authorize_get_datapoint_config_success(self):
        ''' authorize_get_datapoint_config should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_get_datapoint_config_failure(self):
        ''' authorize_get_datapoint_config should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_put_datapoint_config_success(self):
        ''' authorize_put_datapoint_config should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_put_datapoint_config(uid=uid, pid=pid))

    def test_authorize_put_datapoint_config_failure(self):
        ''' authorize_put_datapoint_config should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_datapoint_config(uid=uid, pid=pid))

    def test_authorize_new_datapoint_success(self):
        ''' authorize_new_datapoint should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_new_datapoint(uid=uid, did=did))

    def test_authorize_new_datapoint_failure(self):
        ''' authorize_new_datapoint should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_new_datapoint(uid=uid, did=did))

    def test_authorize_put_agent_config_success(self):
        ''' authorize_put_agent_config should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertTrue(authorization.authorize_put_agent_config(uid=uid, aid=aid))

    def test_authorize_put_agent_config_failure(self):
        ''' authorize_put_agent_config should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_agent_config(uid=uid, aid=aid))

    def test_authorize_new_widget_success(self):
        ''' authorize_new_widget should succeed if permission is granted'''
        uid=self.user['uid']
        self.assertTrue(authorization.authorize_new_widget(uid=uid))

    def test_authorize_get_widget_config_success(self):
        ''' authorize_get_widget_config should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_get_widget_config(uid=uid, wid=wid))

    def test_authorize_get_widget_config_failure(self):
        ''' authorize_get_widget_config should fail if permission is not granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_widget_config(uid=uid, wid=wid))

    def test_authorize_put_widget_config_success(self):
        ''' authorize_put_widget_config should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_put_widget_config(uid=uid, wid=wid))

    def test_authorize_put_widget_config_failure(self):
        ''' authorize_put_widget_config should fail if permission is not granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_widget_config(uid=uid, wid=wid))

    def test_authorize_new_dashboard_success(self):
        ''' authorize_new_dashboard should succeed if permission is granted'''
        uid=self.user['uid']
        self.assertTrue(authorization.authorize_new_dashboard(uid=uid))

    def test_authorize_get_dashboard_config_success(self):
        ''' authorize_get_dashboard_config should succeed if permission is granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_get_dashboard_config(uid=uid, bid=bid))

    def test_authorize_get_dashboard_config_failure(self):
        ''' authorize_get_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_dashboard_config(uid=uid, bid=bid))

    def test_authorize_put_dashboard_config_success(self):
        ''' authorize_put_dashboard_config should succeed if permission is granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_put_dashboard_config(uid=uid, bid=bid))

    def test_authorize_put_dashboard_config_failure(self):
        ''' authorize_put_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_dashboard_config(uid=uid, bid=bid))

    def test_authorize_add_widget_to_dashboard_failure_no_bid(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no permissions over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertFalse(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_add_widget_to_dashboard_failure_no_bid_edit_perm(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no edit permission over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertFalse(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_add_widget_to_dashboard_failure_no_wid(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no edit permission over wid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertFalse(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_add_widget_to_dashboard_failure_no_wid_read_perm(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no read permission over wid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertFalse(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_add_widget_to_dashboard_success(self):
        ''' authorize_add_widget_to_dashboard should succeed '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_delete_widget_from_dashboard_failure_no_bid(self):
        ''' authorize_delete_widget_from_dashboard should fail if user has no permissions over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_widget_from_dashboard(uid=uid,bid=bid))

    def test_authorize_delete_widget_from_dashboard_failure_no_bid_edit_perm(self):
        ''' authorize_delete_widget_to_dashboard should fail if user has no edit permission over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertFalse(authorization.authorize_delete_widget_from_dashboard(uid=uid,bid=bid))

    def test_authorize_delete_widget_from_dashboard_success(self):
        ''' authorize_delete_widget_from_dashboard should succeed '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_delete_widget_from_dashboard(uid=uid,bid=bid))

    def test_authorize_delete_dashboard_failure_non_existent_bid(self):
        ''' authorize_delete_dashboard should fail if no bid exists '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_dashboard(uid=uid, bid=bid))

    def test_authorize_delete_dashboard_failure_no_delete_perm(self):
        ''' authorize_delete_dashboard should fail if user has no delete perm over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertFalse(authorization.authorize_delete_dashboard(uid=uid, bid=bid))

    def test_authorize_delete_dashboard_success(self):
        ''' authorize_delete_dashboard should succeed if user has delete perm over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_delete_dashboard(uid=uid, bid=bid))

    def test_authorize_add_datapoint_to_widget_failure_non_existent_wid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has not the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertFalse(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_add_datapoint_to_widget_failure_no_edit_perm_over_wid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertFalse(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_add_datapoint_to_widget_failure_non_existent_pid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertFalse(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_add_datapoint_to_widget_failure_no_read_perm_over_pid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertFalse(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_add_datapoint_to_widget_success(self):
        ''' authorize_add_datapoint_to_widget should succeed if user has permissions over pid and wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_delete_datapoint_from_widget_failure_non_existent_wid(self):
        ''' authorize_delete_datapoint_from_widget should fail if user has not the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid))

    def test_authorize_delete_datapoint_from_widget_failure_no_edit_perm_over_wid(self):
        ''' authorize_delete_datapoint_from_widget should fail if user has not edit perm over the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertFalse(authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid))

    def test_authorize_delete_datapoint_from_widget_success(self):
        ''' authorize_delete_datapoint_from_widget should succeed if user has permssion over the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid))

    def test_authorize_new_snapshot_failure_non_existent_wid(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        wid=uuid.uuid4()
        self.assertFalse(authorization.authorize_new_snapshot(uid=uid,wid=wid))

    def test_authorize_new_snapshot_failure_non_existent_uid(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_new_snapshot(uid=uid,wid=wid))

    def test_authorize_new_snapshot_success(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_new_snapshot(uid=uid,wid=wid))

    def test_authorize_get_snapshot_data_failure_non_existent_nid(self):
        ''' authorize_get_snapshot_data should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_snapshot_data(uid=uid,nid=nid))

    def test_authorize_get_snapshot_data_failure_non_existent_uid(self):
        ''' authorize_get_snapshot_data should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_snapshot_data(uid=uid,nid=nid))

    def test_authorize_get_snapshot_data_success(self):
        ''' authorize_get_snapshot_data should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertTrue(authorization.authorize_get_snapshot_data(uid=uid,nid=nid))

    def test_authorize_get_snapshot_config_failure_non_existent_nid(self):
        ''' authorize_get_snapshot_config should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_snapshot_config(uid=uid,nid=nid))

    def test_authorize_get_snapshot_config_failure_non_existent_uid(self):
        ''' authorize_get_snapshot_config should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_snapshot_config(uid=uid,nid=nid))

    def test_authorize_get_snapshot_config_success(self):
        ''' authorize_get_snapshot_config should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=uid,nid=nid))

    def test_authorize_delete_snapshot_failure_non_existent_uid(self):
        ''' authorize_delete_snapshot should fail if uid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_snapshot(uid=uid,nid=nid))

    def test_authorize_delete_snapshot_failure_non_existent_nid(self):
        ''' authorize_delete_snapshot should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_snapshot(uid=uid,nid=nid))

    def test_authorize_delete_snapshot_success(self):
        ''' authorize_delete_snapshot should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertTrue(authorization.authorize_delete_snapshot(uid=uid,nid=nid))

    def test_authorize_get_circle_config_failure_non_existent_uid(self):
        ''' authorize_get_circle_config should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_circle_config(uid=uid,cid=cid))

    def test_authorize_get_circle_config_success(self):
        ''' authorize_get_circle_config should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertTrue(authorization.authorize_get_circle_config(uid=uid,cid=cid))

    def test_authorize_delete_circle_failure_non_existent_uid(self):
        ''' authorize_delete_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_circle(uid=uid,cid=cid))

    def test_authorize_delete_circle_failure_non_existent_cid(self):
        ''' authorize_delete_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_circle(uid=uid,cid=cid))

    def test_authorize_delete_circle_success(self):
        ''' authorize_delete_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertTrue(authorization.authorize_delete_circle(uid=uid,cid=cid))

    def test_authorize_update_circle_config_failure_non_existent_uid(self):
        ''' authorize_update_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_update_circle_config(uid=uid,cid=cid))

    def test_authorize_update_circle_config_failure_non_existent_cid(self):
        ''' authorize_update_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        self.assertFalse(authorization.authorize_update_circle_config(uid=uid,cid=cid))

    def test_authorize_update_circle_config_success(self):
        ''' authorize_update_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertTrue(authorization.authorize_update_circle_config(uid=uid,cid=cid))

    def test_authorize_add_member_to_circle_failure_non_existent_uid(self):
        ''' authorize_add_member_to_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_add_member_to_circle(uid=uid,cid=cid))

    def test_authorize_add_member_to_circle_failure_non_existent_cid(self):
        ''' authorize_add_member_to_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        self.assertFalse(authorization.authorize_add_member_to_circle(uid=uid,cid=cid))

    def test_authorize_add_member_to_circle_success(self):
        ''' authorize_add_member_to_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertTrue(authorization.authorize_add_member_to_circle(uid=uid,cid=cid))

    def test_authorize_delete_member_from_circle_failure_non_existent_uid(self):
        ''' authorize_delete_member_from_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_member_from_circle(uid=uid,cid=cid))

    def test_authorize_delete_member_from_circle_failure_non_existent_cid(self):
        ''' authorize_delete_member_from_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        self.assertFalse(authorization.authorize_delete_member_from_circle(uid=uid,cid=cid))

    def test_authorize_delete_member_from_circle_success(self):
        ''' authorize_delete_member_from_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertTrue(authorization.authorize_delete_member_from_circle(uid=uid,cid=cid))

