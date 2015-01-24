import unittest
import uuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.dashboard import api
from komlibs.gestaccount import exceptions

class GestaccountDashboardApiTest(unittest.TestCase):
    ''' komlog.gestaccount.dashboard.api tests '''

    def test_get_dashboard_config_non_existent_dashboard(self):
        ''' get_dashboard_config should fail if bid is not in system '''
        bid=uuid.uuid4()
        self.assertRaises(exceptions.DashboardNotFoundException, api.get_dashboard_config, bid=bid)

    def test_get_dashboards_config_non_existent_username(self):
        ''' get_dashboards_config should fail if username is not in system '''
        username='test_get_dashboards_config_non_existent_username'
        self.assertRaises(exceptions.UserNotFoundException, api.get_dashboards_config, username=username)

    def test_get_dashboards_config_success_no_data(self):
        ''' get_dashboards_config should succeed if username exists, but returns and empty list if there is no dashboard '''
        username='test_get_dashboards_config_success_no_data_user'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        data=api.get_dashboards_config(username=username)
        self.assertEqual(data, [])

