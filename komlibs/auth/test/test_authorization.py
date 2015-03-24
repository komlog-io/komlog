import unittest
import uuid
from komlibs.auth import authorization, requests
from komlibs.auth import exceptions, permissions
from komlibs.gestaccount.user import api as gestuserapi
from komlibs.graph import api as graphapi
from komlibs.graph.relations import vertex
from komlibs.general.time import timeuuid

class AuthAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.authorization tests '''
    
    def test_authorize_request_non_existent_request(self):
        ''' authorize_request should fail if request does not exist '''
        username = 'test_authorize_reqeust_non_existent_request_user'
        password = 'password'
        email = username+'@komlog.org'
        user = gestuserapi.create_user(username=username, password=password, email=email)
        requests=[None,234234234,'TEST_AUTHORIZE_REQUEST_NON_EXISTENT_REQUEST']
        for request in requests:
            self.assertRaises(exceptions.RequestNotFoundException, authorization.authorize_request, request=request, uid=user['uid'])

    def test_authorize_request_non_existent_user(self):
        ''' authorize_request should fail if user does not exist. '''
        uid=uuid.uuid4()
        request=requests.NEW_AGENT
        self.assertRaises(exceptions.UserNotFoundException, authorization.authorize_request, request=request, uid=uid)

    def test_authorize_request_success(self):
        ''' authorize_request should succeed if user exists and has authorization.
        For this test we use the request, defined for these cases, 'DummyRequest' '''
        username = 'test_authorize_request_success_user'
        password = 'password'
        email = 'test_auth.authorization_user@komlog.org'
        user = gestuserapi.create_user(username=username, password=password, email=email)
        request=requests.NEW_AGENT
        self.assertIsNone(authorization.authorize_request(request=request, uid=user['uid']))

    def test_authorize_get_datasource_config_success_shared_auth_success(self):
        ''' authorize_get_datasource_config should succeed if the datasource is shared to the user '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        params={'uid':uid, 'did':did}
        self.assertIsNone(authorization.authorize_get_datasource_config(params=params))

    def test_authorize_get_datasource_config_failure(self):
        ''' authorize_get_datasource_config should fail if the datasource is not shared to the user '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        params={'uid':uid, 'did':did}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datasource_config, params=params)

    def test_authorize_get_datapoint_config_success_shared_auth_success(self):
        ''' authorize_get_datapoint_config should succeed if the datapoint is shared to the user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        params={'uid':uid, 'pid':pid}
        self.assertIsNone(authorization.authorize_get_datapoint_config(params=params))

    def test_authorize_get_datapoint_config_failure(self):
        ''' authorize_get_datapoint_config should fail if the datapoint is not shared to the user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        params={'uid':uid, 'pid':pid}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datapoint_config, params=params)

    def test_authorize_get_snapshot_config_success_shared_auth_success(self):
        ''' authorize_get_snapshot_config should succeed if the snapshot is shared to the user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        params={'uid':uid, 'nid':nid}
        self.assertIsNone(authorization.authorize_get_snapshot_config(params=params))

    def test_authorize_get_snapshot_config_failure(self):
        ''' authorize_get_snapshot_config should fail if the snapshot is not shared to the user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        params={'uid':uid, 'nid':nid}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_snapshot_config, params=params)

    def test_authorize_get_datasource_data_success_shared_auth_success(self):
        ''' authorize_get_datasource_data should succeed if the datasource is shared to the user and interval parameters match '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        params={'uid':uid, 'did':did, 'ii':ii, 'ie':ie}
        self.assertIsNone(authorization.authorize_get_datasource_data(params=params))

    def test_authorize_get_datasource_data_failure_interval_parameters_dont_match(self):
        ''' authorize_get_datasource_data should fail if the datasource is shared to the user but interval parameters dont match '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        params={'uid':uid, 'did':did, 'ii':ii, 'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datasource_data, params=params)

    def test_authorize_get_datasource_data_failure_uid_doesnt_match(self):
        ''' authorize_get_datasource_data should fail if the datasource is shared to a different user '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        params={'uid':uid, 'did':did, 'ii':ii, 'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datasource_data, params=params)

    def test_authorize_get_datasource_data_failure_did_doesnt_match(self):
        ''' authorize_get_datasource_data should fail if the datasource is not shared '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        did=uuid.uuid4()
        params={'uid':uid, 'did':did, 'ii':ii, 'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datasource_data, params=params)

    def test_authorize_get_datapoint_data_success_shared_auth_success(self):
        ''' authorize_get_datapoint_data should succeed if the datasource is shared to the user and interval parameters match '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        params={'uid':uid, 'pid':pid, 'ii':ii, 'ie':ie}
        self.assertIsNone(authorization.authorize_get_datapoint_data(params=params))

    def test_authorize_get_datapoint_data_failure_interval_parameters_dont_match(self):
        ''' authorize_get_datapoint_data should fail if the datasource is shared to the user but interval parameters dont match '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        params={'uid':uid, 'pid':pid, 'ii':ii, 'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datapoint_data, params=params)

    def test_authorize_get_datapoint_data_failure_uid_doesnt_match(self):
        ''' authorize_get_datapoint_data should fail if the datasource is shared to a different user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        params={'uid':uid, 'pid':pid, 'ii':ii, 'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datapoint_data, params=params)

    def test_authorize_get_datapoint_data_failure_pid_doesnt_match(self):
        ''' authorize_get_datapoint_data should fail if the datasource is not shared '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        pid=uuid.uuid4()
        params={'uid':uid, 'pid':pid, 'ii':ii, 'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datapoint_data, params=params)

