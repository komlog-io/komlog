import unittest
import uuid
from komlog.komlibs.auth.quotes import authorization
from komlog.komlibs.auth import exceptions
from komlog.komlibs.gestaccount.user import api as gestuserapi

class AuthQuotesAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.quotes.authorization tests '''
    
    def test_authorize_new_datapoint_non_existent_datasource(self):
        ''' authorize_new_datapoint should fail if datasource does not exist '''
        username = 'test_authorize_new_datapoint_non_existent_datasource_user'
        password = 'password'
        email = username+'@komlog.org'
        user = gestuserapi.create_user(username=username, password=password, email=email)
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, authorization.authorize_new_datapoint, uid=user['uid'], did=did)

