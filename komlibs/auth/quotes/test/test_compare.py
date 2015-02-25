import unittest
import uuid
from komlibs.auth.quotes import compare
from komlibs.gestaccount.user import api as userapi

class AuthQuotesCompareTest(unittest.TestCase):
    ''' komlog.auth.quotes.compare tests '''
    
    def setUp(self):
        username='test_auth.quotes.user'
        password='password'
        email='test_auth.quotes.user@komlog.org'
        try:
            self.user=userapi.get_user_config(username=username)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)

    def test_quo_static_user_total_agents_no_uid(self):
        ''' quo_static_user_total_agents should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_agents(params))

    def test_quo_static_user_total_agents_non_existent_user(self):
        ''' quo_static_user_total_agents should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_agents(params))

    def test_quo_static_user_total_agents_failure(self):
        ''' quo_static_user_total_agents should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_agents(params))

    def test_quo_static_user_total_datasources_no_uid(self):
        ''' quo_static_user_total_datasources should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_datasources(params))

    def test_quo_static_user_total_datasources_non_existent_user(self):
        ''' quo_static_user_total_datasources should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_datasources(params))

    def test_quo_static_user_total_datasources_failure(self):
        ''' quo_static_user_total_datasources should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_datasources(params))

    def test_quo_static_user_total_datapoints_no_uid(self):
        ''' quo_static_user_total_datapoints should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_datapoints(params))

    def test_quo_static_user_total_datapoints_non_existent_user(self):
        ''' quo_static_user_total_datapoints should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_datapoints(params))

    def test_quo_static_user_total_datapoints_failure(self):
        ''' quo_static_user_total_datapoints should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_datapoints(params))

    def test_quo_static_user_total_widgets_no_uid(self):
        ''' quo_static_user_total_widgets should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_widgets(params))

    def test_quo_static_user_total_widgets_non_existent_user(self):
        ''' quo_static_user_total_widgets should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_widgets(params))

    def test_quo_static_user_total_widgets_failure(self):
        ''' quo_static_user_total_widgets should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_widgets(params))

    def test_quo_static_user_total_dashboards_no_uid(self):
        ''' quo_static_user_total_dashboards should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_dashboards(params))

    def test_quo_static_user_total_dashboards_non_existent_user(self):
        ''' quo_static_user_total_dashboards should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_dashboards(params))

    def test_quo_static_user_total_dashboards_failure(self):
        ''' quo_static_user_total_dashboards should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_dashboards(params))

    def test_quo_static_agent_total_datasources_no_uid(self):
        ''' quo_static_agent_total_datasources should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_agent_total_datasources(params))

    def test_quo_static_agent_total_datasources_no_aid(self):
        ''' quo_static_agent_total_datasources should fail if no aid is passed '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_agent_total_datasources(params))

    def test_quo_static_agent_total_datasources_non_existent_user(self):
        ''' quo_static_agent_total_datasources should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'aid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_agent_total_datasources(params))

    def test_quo_static_agent_total_datasources_failure(self):
        ''' quo_static_agent_total_datasources should fail because agent does not exist '''
        params={'uid':self.user['uid'], 'aid':uuid.uuid4()}
        self.assertFalse(compare.quo_static_agent_total_datasources(params))

    def test_quo_static_agent_total_datapoints_no_uid(self):
        ''' quo_static_agent_total_datapoints should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_agent_total_datapoints(params))

    def test_quo_static_agent_total_datapoints_no_aid(self):
        ''' quo_static_agent_total_datapoints should fail if no aid is passed '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_agent_total_datapoints(params))

    def test_quo_static_agent_total_datapoints_non_existent_user(self):
        ''' quo_static_agent_total_datapoints should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'aid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_agent_total_datapoints(params))

    def test_quo_static_agent_total_datapoints_failure(self):
        ''' quo_static_agent_total_datapoints should fail because agent does not exist '''
        params={'uid':self.user['uid'], 'aid':uuid.uuid4()}
        self.assertFalse(compare.quo_static_agent_total_datapoints(params))

    def test_quo_static_datasource_total_datapoints_no_uid(self):
        ''' quo_static_datasource_total_datapoints should fail if no uid is passed '''
        params={'did':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_datasource_total_datapoints(params))

    def test_quo_static_datasource_total_datapoints_no_did(self):
        ''' quo_static_datasource_total_datapoints should fail if no did is passed '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_datasource_total_datapoints(params))

    def test_quo_static_datasource_total_datapoints_non_existent_user(self):
        ''' quo_static_datasource_total_datapoints should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'did':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_datasource_total_datapoints(params))

    def test_quo_static_datasource_total_datapoints_failure(self):
        ''' quo_static_datasource_total_datapoints should fail because datasource does not exist '''
        params={'uid':self.user['uid'], 'did':uuid.uuid4()}
        self.assertFalse(compare.quo_static_datasource_total_datapoints(params))

    def test_quo_static_user_total_snapshots_no_uid(self):
        ''' quo_static_user_total_snapshots should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_snapshots(params))

    def test_quo_static_user_total_snapshots_non_existent_user(self):
        ''' quo_static_user_total_snapshots should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_snapshots(params))

    def test_quo_static_user_total_snapshots_failure(self):
        ''' quo_static_user_total_snapshots should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_snapshots(params))

