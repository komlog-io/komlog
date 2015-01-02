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
        self.user = userapi.create_user(username=username, password=password, email=email)
        

    def test_authorize_get_agent_config_success(self):
        ''' authorize_get_agent_config should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_agent_perm(uid=user.uid, aid=aid, perm=perm)
        self.assertTrue(authorization.authorize_get_agent_config(user=user, aid=aid))

    def test_authorize_get_agent_config_failure(self):
        ''' authorize_get_agent_config should fail if permission is not granted'''
        user=self.user
        aid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_agent_config(user=user, aid=aid))

    def test_authorize_get_datasource_config_success(self):
        ''' authorize_get_datasource_config should succeed if permission is granted'''
        user=self.user
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_get_datasource_config(user=user, did=did))

    def test_authorize_get_datasource_config_failure(self):
        ''' authorize_get_datasource_config should fail if permission is not granted'''
        user=self.user
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datasource_config(user=user, did=did))

    def test_authorize_put_datasource_config_success(self):
        ''' authorize_put_datasource_config should succeed if permission is granted'''
        user=self.user
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_put_datasource_config(user=user, did=did))

    def test_authorize_put_datasource_config_failure(self):
        ''' authorize_put_datasource_config should fail if permission is not granted'''
        user=self.user
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_datasource_config(user=user, did=did))

    def test_authorize_get_datasource_data_success(self):
        ''' authorize_get_datasource_data should succeed if permission is granted'''
        user=self.user
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_get_datasource_data(user=user, did=did))

    def test_authorize_get_datasource_data_failure(self):
        ''' authorize_get_datasource_data should fail if permission is not granted'''
        user=self.user
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datasource_data(user=user, did=did))

    def test_authorize_post_datasource_data_success(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=user.uid, aid=aid, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_post_datasource_data(user=user, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure(self):
        ''' authorize_post_datasource_data should fail if permission is not granted'''
        user=self.user
        aid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_post_datasource_data(user=user, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_user_agent_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(user=user, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_user_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_agent_perm(uid=user.uid, aid=aid, perm=perm)
        cassapiperm.insert_agent_datasource_perm(aid=aid, did=did, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(user=user, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure_no_agent_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=user.uid, aid=aid, perm=perm)
        self.assertFalse(authorization.authorize_post_datasource_data(user=user, aid=aid, did=did))

    def test_authorize_new_agent_success(self):
        ''' authorize_new_agent should succeed if permission is granted'''
        user=self.user
        self.assertTrue(authorization.authorize_new_agent(user=user))

    def test_authorize_new_datasource_success(self):
        ''' authorize_new_datasource should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_agent_perm(uid=user.uid, aid=aid, perm=perm)
        self.assertTrue(authorization.authorize_new_datasource(user=user, aid=aid))

    def test_authorize_new_datasource_failure(self):
        ''' authorize_new_datasource should fail if permission is not granted'''
        user=self.user
        aid=uuid.uuid4()
        self.assertFalse(authorization.authorize_new_datasource(user=user, aid=aid))

    def test_authorize_get_datapoint_data_success(self):
        ''' authorize_get_datapoint_data should succeed if permission is granted'''
        user=self.user
        pid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datapoint_perm(uid=user.uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_get_datapoint_data(user=user, pid=pid))

    def test_authorize_get_datapoint_data_failure(self):
        ''' authorize_get_datapoint_data should fail if permission is not granted'''
        user=self.user
        pid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datapoint_data(user=user, pid=pid))

    def test_authorize_get_datapoint_config_success(self):
        ''' authorize_get_datapoint_config should succeed if permission is granted'''
        user=self.user
        pid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datapoint_perm(uid=user.uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_get_datapoint_config(user=user, pid=pid))

    def test_authorize_get_datapoint_config_failure(self):
        ''' authorize_get_datapoint_config should fail if permission is not granted'''
        user=self.user
        pid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datapoint_config(user=user, pid=pid))

    def test_authorize_put_datapoint_config_success(self):
        ''' authorize_put_datapoint_config should succeed if permission is granted'''
        user=self.user
        pid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datapoint_perm(uid=user.uid, pid=pid, perm=perm)
        self.assertTrue(authorization.authorize_put_datapoint_config(user=user, pid=pid))

    def test_authorize_put_datapoint_config_failure(self):
        ''' authorize_put_datapoint_config should fail if permission is not granted'''
        user=self.user
        pid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_datapoint_config(user=user, pid=pid))

    def test_authorize_new_datapoint_success(self):
        ''' authorize_new_datapoint should succeed if permission is granted'''
        user=self.user
        did=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_datasource_perm(uid=user.uid, did=did, perm=perm)
        self.assertTrue(authorization.authorize_new_datapoint(user=user, did=did))

    def test_authorize_new_datapoint_failure(self):
        ''' authorize_new_datapoint should fail if permission is not granted'''
        user=self.user
        did=uuid.uuid4()
        self.assertFalse(authorization.authorize_new_datapoint(user=user, did=did))

    def test_authorize_put_agent_config_success(self):
        ''' authorize_put_agent_config should succeed if permission is granted'''
        user=self.user
        aid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_agent_perm(uid=user.uid, aid=aid, perm=perm)
        self.assertTrue(authorization.authorize_put_agent_config(user=user, aid=aid))

    def test_authorize_put_agent_config_failure(self):
        ''' authorize_put_agent_config should fail if permission is not granted'''
        user=self.user
        aid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_agent_config(user=user, aid=aid))

    def test_authorize_new_widget_success(self):
        ''' authorize_new_widget should succeed if permission is granted'''
        user=self.user
        self.assertTrue(authorization.authorize_new_widget(user=user))

    def test_authorize_get_widget_config_success(self):
        ''' authorize_get_widget_config should succeed if permission is granted'''
        user=self.user
        wid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_widget_perm(uid=user.uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_get_widget_config(user=user, wid=wid))

    def test_authorize_get_widget_config_failure(self):
        ''' authorize_get_widget_config should fail if permission is not granted'''
        user=self.user
        wid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_widget_config(user=user, wid=wid))

    def test_authorize_put_widget_config_success(self):
        ''' authorize_put_widget_config should succeed if permission is granted'''
        user=self.user
        wid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_widget_perm(uid=user.uid, wid=wid, perm=perm)
        self.assertTrue(authorization.authorize_put_widget_config(user=user, wid=wid))

    def test_authorize_put_widget_config_failure(self):
        ''' authorize_put_widget_config should fail if permission is not granted'''
        user=self.user
        wid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_widget_config(user=user, wid=wid))

    def test_authorize_new_dashboard_success(self):
        ''' authorize_new_dashboard should succeed if permission is granted'''
        user=self.user
        self.assertTrue(authorization.authorize_new_dashboard(user=user))

    def test_authorize_get_dashboard_config_success(self):
        ''' authorize_get_dashboard_config should succeed if permission is granted'''
        user=self.user
        bid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_dashboard_perm(uid=user.uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_get_dashboard_config(user=user, bid=bid))

    def test_authorize_get_dashboard_config_failure(self):
        ''' authorize_get_dashboard_config should fail if permission is not granted'''
        user=self.user
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_dashboard_config(user=user, bid=bid))

    def test_authorize_put_dashboard_config_success(self):
        ''' authorize_put_dashboard_config should succeed if permission is granted'''
        user=self.user
        bid=uuid.uuid4()
        perm='A'
        cassapiperm.insert_user_dashboard_perm(uid=user.uid, bid=bid, perm=perm)
        self.assertTrue(authorization.authorize_put_dashboard_config(user=user, bid=bid))

    def test_authorize_put_dashboard_config_failure(self):
        ''' authorize_put_dashboard_config should fail if permission is not granted'''
        user=self.user
        bid=uuid.uuid4()
        self.assertFalse(authorization.authorize_put_dashboard_config(user=user, bid=bid))

