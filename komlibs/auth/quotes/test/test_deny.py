import unittest
import uuid
from komlibs.auth.quotes import deny
from komlibs.gestaccount.user import api as userapi

class AuthQuotesDenyTest(unittest.TestCase):
    ''' komlog.auth.quotes.deny tests '''
    
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
        flag=True
        self.assertFalse(deny.quo_static_user_total_agents(params,flag))

    def test_quo_static_user_total_agents_success(self):
        ''' quo_static_user_total_agents should succeed if deny flag is True and UID is set'''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_static_user_total_agents(params,flag))

    def test_quo_static_user_total_agents_unsuccess(self):
        ''' quo_static_user_total_agents should succeed if deny flag is False and UID is set'''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_static_user_total_agents(params,flag))

    def test_quo_static_user_total_datasources_no_uid(self):
        ''' quo_static_user_total_datasources should fail if no uid is passed '''
        params={}
        flag=True
        self.assertFalse(deny.quo_static_user_total_datasources(params,flag))

    def test_quo_static_user_total_datasources_success(self):
        ''' quo_static_user_total_datasources should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_static_user_total_datasources(params,flag))

    def test_quo_static_user_total_datasources_unsuccess(self):
        ''' quo_static_user_total_datasources should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_static_user_total_datasources(params,flag))

    def test_quo_static_user_total_datapoints_no_uid(self):
        ''' quo_static_user_total_datapoints should fail if no uid is passed '''
        params={}
        flag=True
        self.assertFalse(deny.quo_static_user_total_datapoints(params,flag))

    def test_quo_static_user_total_datapoints_success(self):
        ''' quo_static_user_total_datapoints should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_static_user_total_datapoints(params,flag))

    def test_quo_static_user_total_datapoints_unsuccess(self):
        ''' quo_static_user_total_datapoints should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_static_user_total_datapoints(params,flag))

    def test_quo_static_user_total_widgets_no_uid(self):
        ''' quo_static_user_total_widgets should fail if no uid is passed '''
        params={}
        flag=True
        self.assertFalse(deny.quo_static_user_total_widgets(params,flag))

    def test_quo_static_user_total_widgets_success(self):
        ''' quo_static_user_total_widgets should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_static_user_total_widgets(params,flag))

    def test_quo_static_user_total_widgets_unsuccess(self):
        ''' quo_static_user_total_widgets should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_static_user_total_widgets(params,flag))

    def test_quo_static_user_total_dashboards_no_uid(self):
        ''' quo_static_user_total_dashboards should fail if no uid is passed '''
        params={}
        flag=True
        self.assertFalse(deny.quo_static_user_total_dashboards(params,flag))

    def test_quo_static_user_total_dashboards_success(self):
        ''' quo_static_user_total_dashboards should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_static_user_total_dashboards(params,flag))

    def test_quo_static_user_total_dashboards_unsuccess(self):
        ''' quo_static_user_total_dashboards should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_static_user_total_dashboards(params,flag))

    def test_quo_static_agent_total_datasources_no_uid(self):
        ''' quo_static_agent_total_datasources should fail if no uid is passed '''
        params={'aid':self.user['uid']}
        flag=True
        self.assertFalse(deny.quo_static_agent_total_datasources(params,flag))

    def test_quo_static_agent_total_datasources_no_aid(self):
        ''' quo_static_agent_total_datasources should fail if no aid is passed '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertFalse(deny.quo_static_agent_total_datasources(params,flag))

    def test_quo_static_agent_total_datasources_success(self):
        ''' quo_static_agent_total_datasources should succeed if deny flag is True and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_static_agent_total_datasources(params,flag))

    def test_quo_static_agent_total_datasources_unsuccess(self):
        ''' quo_static_agent_total_datasources should succeed if deny flag is False and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_static_agent_total_datasources(params,flag))

    def test_quo_static_agent_total_datapoints_no_uid(self):
        ''' quo_static_agent_total_datapoints should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        flag=True
        self.assertFalse(deny.quo_static_agent_total_datapoints(params,flag))

    def test_quo_static_agent_total_datapoints_no_aid(self):
        ''' quo_static_agent_total_datapoints should fail if no aid is passed '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertFalse(deny.quo_static_agent_total_datapoints(params,flag))

    def test_quo_static_agent_total_datapoints_success(self):
        ''' quo_static_agent_total_datapoints should succeed if deny flag is True and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_static_agent_total_datapoints(params,flag))

    def test_quo_static_agent_total_datapoints_unsuccess(self):
        ''' quo_static_agent_total_datapoints should succeed if deny flag is False and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_static_agent_total_datapoints(params,flag))

    def test_quo_static_datasource_total_datapoints_no_uid(self):
        ''' quo_static_datasource_total_datapoints should fail if no uid is passed '''
        params={'did':uuid.uuid4()}
        flag=True
        self.assertFalse(deny.quo_static_datasource_total_datapoints(params,flag))

    def test_quo_static_datasource_total_datapoints_no_did(self):
        ''' quo_static_datasource_total_datapoints should fail if no did is passed '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertFalse(deny.quo_static_datasource_total_datapoints(params,flag))

    def test_quo_static_datasource_total_datapoints_success(self):
        ''' quo_static_datasource_total_datapoints should succeed if deny flag is True and UID and DID are set '''
        params={'uid':self.user['uid'],'did':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_static_datasource_total_datapoints(params,flag))

    def test_quo_static_datasource_total_datapoints_unsuccess(self):
        ''' quo_static_datasource_total_datapoints should succeed if deny flag is False and UID and DID are set '''
        params={'uid':self.user['uid'],'did':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_static_datasource_total_datapoints(params,flag))

