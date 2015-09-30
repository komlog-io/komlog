import unittest
import uuid
from komlibs.auth import authorization, requests
from komlibs.auth import exceptions, permissions
from komlibs.gestaccount.user import api as gestuserapi
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

    def test_authorize_get_datasource_config_failure(self):
        ''' authorize_get_datasource_config should fail if the datasource is not shared to the user '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        params={'uid':uid, 'did':did}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datasource_config, params=params)

    def test_authorize_get_datapoint_config_failure(self):
        ''' authorize_get_datapoint_config should fail if the datapoint is not shared to the user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        params={'uid':uid, 'pid':pid}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datapoint_config, params=params)

    def test_authorize_get_snapshot_config_failure(self):
        ''' authorize_get_snapshot_config should fail if the snapshot is not shared to the user '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        tid=uuid.uuid4()
        params={'uid':uid, 'nid':nid,'tid':tid,'ii':ii,'ie':ie}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_snapshot_config, params=params)

    def test_authorize_get_datasource_data_failure_did_doesnt_match(self):
        ''' authorize_get_datasource_data should fail if the datasource is not shared '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        tid=uuid.uuid4()
        params={'uid':uid, 'did':did, 'ii':ii, 'ie':ie,'tid':tid}
        self.assertRaises(exceptions.AuthorizationException, authorization.authorize_get_datasource_data, params=params)

