import unittest
import uuid
from komlibs.auth.quotes import authorization
from komlibs.auth import exceptions
from komlibs.gestaccount.user import api as gestuserapi

class AuthQuotesAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.quotes.authorization tests '''
    
    def setUp(self):
        username = 'test_auth.quotes.authorization_user'
        password = 'password'
        email = 'test_auth.quotes.authorization_user@komlog.org'
        self.user = gestuserapi.create_user(username=username, password=password, email=email)

    def test_authorize_new_datapoint_non_existent_datasource(self):
        ''' authorize_new_datapoint should fail if datasource does not exist '''
        user=self.user
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, authorization.authorize_new_datapoint, user=user, did=did)

