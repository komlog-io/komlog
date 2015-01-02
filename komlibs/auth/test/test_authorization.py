import unittest
from komlibs.auth import authorization
from komlibs.auth import exceptions
from komlibs.gestaccount.user import api as gestuserapi

class AuthAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.authorization tests '''
    
    def setUp(self):
        username = 'test_auth.authorization_user'
        password = 'password'
        email = 'test_auth.authorization_user@komlog.org'
        self.user = gestuserapi.create_user(username=username, password=password, email=email)

    def test_authorize_request_non_existent_request(self):
        ''' authorize_request should fail if request does not exist '''
        requests=[None,234234234,'TEST_AUTHORIZE_REQUEST_NON_EXISTENT_REQUEST']
        username='test_auth.authorization_user'
        for request in requests:
            self.assertRaises(exceptions.RequestNotFoundException, authorization.authorize_request, request=request, username=username)

    def test_authorize_request_non_existent_user(self):
        ''' authorize_request should fail if user does not exist.
        For this test we use the request, defined for these cases, 'DummyRequest' '''
        username='test_authorize_request_non_existent_user'
        request='DummyRequest'
        self.assertRaises(exceptions.UserNotFoundException, authorization.authorize_request, request=request, username=username)

    def test_authorize_request_success(self):
        ''' authorize_request should succeed if user exists and has authorization.
        For this test we use the request, defined for these cases, 'DummyRequest' '''
        username=self.user.username
        request='DummyRequest'
        self.assertIsNone(authorization.authorize_request(request=request, username=username))

