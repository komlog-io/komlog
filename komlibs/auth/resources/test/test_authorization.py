import unittest
import uuid
from komlibs.auth.resources import authorization
from komcass.api import permission as cassapiperm
from komlibs.gestaccount.user import api as userapi


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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_user_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_agent_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
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
        perm='A'
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_put_dashboard_config(uid=uid, bid=bid))

    def test_authorize_put_dashboard_config_failure(self):
        ''' authorize_put_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_dashboard_config(uid=uid, bid=bid))
