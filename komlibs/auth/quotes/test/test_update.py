import unittest
import uuid
from komlibs.auth import operations
from komlibs.auth.quotes import update
from komcass.api import quote as cassapiquote


class AuthQuotesUpdateTest(unittest.TestCase):
    ''' komlog.auth.quotes.update tests '''
    
    def test_get_update_funcs_success(self):
        ''' test_update_funcs should return a list of functions '''
        operation=operations.NEW_AGENT
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, list))

    def test_get_update_funcs_success_empty_list(self):
        '''test_update_funcs should return an empty list of functions if operation does not exist'''
        operation='234234234'
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, list))
        self.assertEqual(update_funcs, [])

    def test_quo_static_user_total_agents_no_uid(self):
        ''' quo_static_user_total_agents should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_agents(params))

    def test_quo_static_user_total_agents_success(self):
        ''' quo_static_user_total_agents should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_agents(params)
        user_quotes=cassapiquote.get_user_quotes(uid=uid)
        self.assertEqual(user_quotes.get_quote('quo_static_user_total_agents'),result)

    def test_quo_static_user_total_datasources_no_uid(self):
        ''' quo_static_user_total_datasources should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_datasources(params))

    def test_quo_static_user_total_datasources_success(self):
        ''' quo_static_user_total_datasources should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_datasources(params)
        user_quotes=cassapiquote.get_user_quotes(uid=uid)
        self.assertEqual(user_quotes.get_quote('quo_static_user_total_datasources'),result)

    def test_quo_static_user_total_datapoints_no_uid(self):
        ''' quo_static_user_total_datapoints should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_datapoints(params))

    def test_quo_static_user_total_datapoints_success(self):
        ''' quo_static_user_total_datapoints should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_datapoints(params)
        user_quotes=cassapiquote.get_user_quotes(uid=uid)
        self.assertEqual(user_quotes.get_quote('quo_static_user_total_datapoints'),result)

    def test_quo_static_user_total_widgets_no_uid(self):
        ''' quo_static_user_total_widgets should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_widgets(params))

    def test_quo_static_user_total_widgets_success(self):
        ''' quo_static_user_total_widgets should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_widgets(params)
        user_quotes=cassapiquote.get_user_quotes(uid=uid)
        self.assertEqual(user_quotes.get_quote('quo_static_user_total_widgets'),result)

    def test_quo_static_user_total_dashboards_no_uid(self):
        ''' quo_static_user_total_dashboards should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_dashboards(params))

    def test_quo_static_user_total_dashboards_success(self):
        ''' quo_static_user_total_dashboards should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_dashboards(params)
        user_quotes=cassapiquote.get_user_quotes(uid=uid)
        self.assertEqual(user_quotes.get_quote('quo_static_user_total_dashboards'),result)

    def test_quo_static_agent_total_datasources_no_aid(self):
        ''' quo_static_agent_total_datasources should fail if no aid is passed '''
        params={}
        self.assertIsNone(update.quo_static_agent_total_datasources(params))

    def test_quo_static_agent_total_datasources_success(self):
        ''' quo_static_agent_total_datasources should succeed if AID is set'''
        aid=uuid.uuid4()
        params={'aid':aid}
        result=update.quo_static_agent_total_datasources(params)
        agent_quotes=cassapiquote.get_agent_quotes(aid=aid)
        self.assertEqual(agent_quotes.get_quote('quo_static_agent_total_datasources'),result)

    def test_quo_static_agent_total_datapoints_no_aid(self):
        ''' quo_static_agent_total_datapoints should fail if no aid is passed '''
        params={}
        self.assertIsNone(update.quo_static_agent_total_datapoints(params))

    def test_quo_static_agent_total_datapoints_success(self):
        ''' quo_static_agent_total_datapoints should succeed if AID is set'''
        aid=uuid.uuid4()
        params={'aid':aid}
        result=update.quo_static_agent_total_datapoints(params)
        agent_quotes=cassapiquote.get_agent_quotes(aid=aid)
        self.assertEqual(agent_quotes.get_quote('quo_static_agent_total_datapoints'),result)

    def test_quo_static_datasource_total_datapoints_no_did(self):
        ''' quo_static_datasource_total_datapoints should fail if no did is passed '''
        params={}
        self.assertIsNone(update.quo_static_datasource_total_datapoints(params))

    def test_quo_static_datasource_total_datapoints_success(self):
        ''' quo_static_datasource_total_datapoints should succeed if DID is set'''
        did=uuid.uuid4()
        params={'did':did}
        result=update.quo_static_datasource_total_datapoints(params)
        datasource_quotes=cassapiquote.get_datasource_quotes(did=did)
        self.assertEqual(datasource_quotes.get_quote('quo_static_datasource_total_datapoints'),result)

