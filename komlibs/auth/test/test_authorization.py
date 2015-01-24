import unittest
from komlibs.auth import authorization
from komlibs.auth import exceptions
from komlibs.gestaccount.user import api as gestuserapi

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
            self.assertRaises(exceptions.RequestNotFoundException, authorization.authorize_request, request=request, username=username)

    def test_authorize_request_non_existent_user(self):
        ''' authorize_request should fail if user does not exist. '''
        username='test_authorize_request_non_existent_user'
        request='NewAgentRequest'
        self.assertRaises(exceptions.UserNotFoundException, authorization.authorize_request, request=request, username=username)

    def test_authorize_request_success(self):
        ''' authorize_request should succeed if user exists and has authorization.
        For this test we use the request, defined for these cases, 'DummyRequest' '''
        username = 'test_authorize_request_success_user'
        password = 'password'
        email = 'test_auth.authorization_user@komlog.org'
        user = gestuserapi.create_user(username=username, password=password, email=email)
        request='NewAgentRequest'
        self.assertIsNone(authorization.authorize_request(request=request, username=username))

