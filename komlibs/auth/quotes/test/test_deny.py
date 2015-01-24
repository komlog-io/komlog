import unittest
import uuid
from komlibs.auth.quotes import deny
from komlibs.gestaccount.user import api as userapi

class AuthQuotesDenyTest(unittest.TestCase):
    ''' komlog.auth.quotes.deny tests '''
    
    def setUp(self):
        username='test_auth.quotes.deny_user'
        password='password'
        email='test_auth.quotes.deny_user@komlog.org'
        try:
            self.user=userapi.get_user_config(username=username)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)

    def test_deny_quo_static_user_total_agents_no_uid(self):
        ''' deny_quo_static_user_total_agents should fail if no uid is passed '''
        params={}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_user_total_agents(params,deny_flag))

    def test_deny_quo_static_user_total_agents_deny_success(self):
        ''' deny_quo_static_user_total_agents should succeed if deny flag is True and UID is set'''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_user_total_agents(params,deny_flag))

    def test_deny_quo_static_user_total_agents_undeny_success(self):
        ''' deny_quo_static_user_total_agents should succeed if deny flag is False and UID is set'''
        params={'uid':self.user['uid']}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_user_total_agents(params,deny_flag))

    def test_deny_quo_static_user_total_datasources_no_uid(self):
        ''' deny_quo_static_user_total_datasources should fail if no uid is passed '''
        params={}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_user_total_datasources(params,deny_flag))

    def test_deny_quo_static_user_total_datasources_deny_success(self):
        ''' deny_quo_static_user_total_datasources should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_user_total_datasources(params,deny_flag))

    def test_deny_quo_static_user_total_datasources_undeny_success(self):
        ''' deny_quo_static_user_total_datasources should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_user_total_datasources(params,deny_flag))

    def test_deny_quo_static_user_total_datapoints_no_uid(self):
        ''' deny_quo_static_user_total_datapoints should fail if no uid is passed '''
        params={}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_user_total_datapoints(params,deny_flag))

    def test_deny_quo_static_user_total_datapoints_deny_success(self):
        ''' deny_quo_static_user_total_datapoints should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_user_total_datapoints(params,deny_flag))

    def test_deny_quo_static_user_total_datapoints_undeny_success(self):
        ''' deny_quo_static_user_total_datapoints should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_user_total_datapoints(params,deny_flag))

    def test_deny_quo_static_user_total_widgets_no_uid(self):
        ''' deny_quo_static_user_total_widgets should fail if no uid is passed '''
        params={}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_user_total_widgets(params,deny_flag))

    def test_deny_quo_static_user_total_widgets_deny_success(self):
        ''' deny_quo_static_user_total_widgets should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_user_total_widgets(params,deny_flag))

    def test_deny_quo_static_user_total_widgets_undeny_success(self):
        ''' deny_quo_static_user_total_widgets should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_user_total_widgets(params,deny_flag))

    def test_deny_quo_static_user_total_dashboards_no_uid(self):
        ''' deny_quo_static_user_total_dashboards should fail if no uid is passed '''
        params={}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_user_total_dashboards(params,deny_flag))

    def test_deny_quo_static_user_total_dashboards_deny_success(self):
        ''' deny_quo_static_user_total_dashboards should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_user_total_dashboards(params,deny_flag))

    def test_deny_quo_static_user_total_dashboards_undeny_success(self):
        ''' deny_quo_static_user_total_dashboards should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_user_total_dashboards(params,deny_flag))

    def test_deny_quo_static_agent_total_datasources_no_uid(self):
        ''' deny_quo_static_agent_total_datasources should fail if no uid is passed '''
        params={'aid':self.user['uid']}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_agent_total_datasources(params,deny_flag))

    def test_deny_quo_static_agent_total_datasources_no_aid(self):
        ''' deny_quo_static_agent_total_datasources should fail if no aid is passed '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_agent_total_datasources(params,deny_flag))

    def test_deny_quo_static_agent_total_datasources_deny_success(self):
        ''' deny_quo_static_agent_total_datasources should succeed if deny flag is True and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_agent_total_datasources(params,deny_flag))

    def test_deny_quo_static_agent_total_datasources_undeny_success(self):
        ''' deny_quo_static_agent_total_datasources should succeed if deny flag is False and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_agent_total_datasources(params,deny_flag))

    def test_deny_quo_static_agent_total_datapoints_no_uid(self):
        ''' deny_quo_static_agent_total_datapoints should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_agent_total_datapoints(params,deny_flag))

    def test_deny_quo_static_agent_total_datapoints_no_aid(self):
        ''' deny_quo_static_agent_total_datapoints should fail if no aid is passed '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_agent_total_datapoints(params,deny_flag))

    def test_deny_quo_static_agent_total_datapoints_deny_success(self):
        ''' deny_quo_static_agent_total_datapoints should succeed if deny flag is True and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_agent_total_datapoints(params,deny_flag))

    def test_deny_quo_static_agent_total_datapoints_undeny_success(self):
        ''' deny_quo_static_agent_total_datapoints should succeed if deny flag is False and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_agent_total_datapoints(params,deny_flag))

    def test_deny_quo_static_datasource_total_datapoints_no_uid(self):
        ''' deny_quo_static_datasource_total_datapoints should fail if no uid is passed '''
        params={'did':uuid.uuid4()}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_datasource_total_datapoints(params,deny_flag))

    def test_deny_quo_static_datasource_total_datapoints_no_did(self):
        ''' deny_quo_static_datasource_total_datapoints should fail if no did is passed '''
        params={'uid':self.user['uid']}
        deny_flag=True
        self.assertFalse(deny.deny_quo_static_datasource_total_datapoints(params,deny_flag))

    def test_deny_quo_static_datasource_total_datapoints_deny_success(self):
        ''' deny_quo_static_datasource_total_datapoints should succeed if deny flag is True and UID and DID are set '''
        params={'uid':self.user['uid'],'did':uuid.uuid4()}
        deny_flag=True
        self.assertTrue(deny.deny_quo_static_datasource_total_datapoints(params,deny_flag))

    def test_deny_quo_static_datasource_total_datapoints_undeny_success(self):
        ''' deny_quo_static_datasource_total_datapoints should succeed if deny flag is False and UID and DID are set '''
        params={'uid':self.user['uid'],'did':uuid.uuid4()}
        deny_flag=False
        self.assertTrue(deny.deny_quo_static_datasource_total_datapoints(params,deny_flag))

