import unittest
import uuid
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.auth.quotes import update
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.model.orm import circle as ormcircle
from komlog.komlibs.general.time import timeuuid


class AuthQuotesUpdateTest(unittest.TestCase):
    ''' komlog.auth.quotes.update tests '''
    
    def test_get_update_funcs_success(self):
        ''' test_update_funcs should return a list of functions '''
        operation=Operations.NEW_AGENT
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
        quote=Quotes.quo_static_user_total_agents.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_user_total_datasources_no_uid(self):
        ''' quo_static_user_total_datasources should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_datasources(params))

    def test_quo_static_user_total_datasources_success(self):
        ''' quo_static_user_total_datasources should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_datasources(params)
        quote=Quotes.quo_static_user_total_datasources.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_user_total_datapoints_no_uid(self):
        ''' quo_static_user_total_datapoints should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_datapoints(params))

    def test_quo_static_user_total_datapoints_success(self):
        ''' quo_static_user_total_datapoints should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_datapoints(params)
        quote=Quotes.quo_static_user_total_datapoints.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_user_total_widgets_no_uid(self):
        ''' quo_static_user_total_widgets should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_widgets(params))

    def test_quo_static_user_total_widgets_success(self):
        ''' quo_static_user_total_widgets should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_widgets(params)
        quote=Quotes.quo_static_user_total_widgets.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_user_total_dashboards_no_uid(self):
        ''' quo_static_user_total_dashboards should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_dashboards(params))

    def test_quo_static_user_total_dashboards_success(self):
        ''' quo_static_user_total_dashboards should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_dashboards(params)
        quote=Quotes.quo_static_user_total_dashboards.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_agent_total_datasources_no_aid(self):
        ''' quo_static_agent_total_datasources should fail if no aid is passed '''
        params={}
        self.assertIsNone(update.quo_static_agent_total_datasources(params))

    def test_quo_static_agent_total_datasources_success(self):
        ''' quo_static_agent_total_datasources should succeed if AID is set'''
        aid=uuid.uuid4()
        params={'aid':aid}
        result=update.quo_static_agent_total_datasources(params)
        quote=Quotes.quo_static_agent_total_datasources.name
        agent_quote=cassapiquote.get_agent_quote(aid=aid, quote=quote)
        self.assertEqual(agent_quote.value,result)

    def test_quo_static_agent_total_datapoints_no_aid(self):
        ''' quo_static_agent_total_datapoints should fail if no aid is passed '''
        params={}
        self.assertIsNone(update.quo_static_agent_total_datapoints(params))

    def test_quo_static_agent_total_datapoints_success(self):
        ''' quo_static_agent_total_datapoints should succeed if AID is set'''
        aid=uuid.uuid4()
        params={'aid':aid}
        result=update.quo_static_agent_total_datapoints(params)
        quote=Quotes.quo_static_agent_total_datapoints.name
        agent_quote=cassapiquote.get_agent_quote(aid=aid, quote=quote)
        self.assertEqual(agent_quote.value,result)

    def test_quo_static_datasource_total_datapoints_no_did(self):
        ''' quo_static_datasource_total_datapoints should fail if no did is passed '''
        params={}
        self.assertIsNone(update.quo_static_datasource_total_datapoints(params))

    def test_quo_static_datasource_total_datapoints_success(self):
        ''' quo_static_datasource_total_datapoints should succeed if DID is set'''
        did=uuid.uuid4()
        params={'did':did}
        result=update.quo_static_datasource_total_datapoints(params)
        quote=Quotes.quo_static_datasource_total_datapoints.name
        datasource_quote=cassapiquote.get_datasource_quote(did=did, quote=quote)
        self.assertEqual(datasource_quote.value,result)

    def test_quo_static_user_total_snapshots_no_uid(self):
        ''' quo_static_user_total_snapshots should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_snapshots(params))

    def test_quo_static_user_total_snapshots_success(self):
        ''' quo_static_user_total_snapshots should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_snapshots(params)
        quote=Quotes.quo_static_user_total_snapshots.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_user_total_circles_no_uid(self):
        ''' quo_static_user_total_circles should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_static_user_total_circles(params))

    def test_quo_static_user_total_circles_success(self):
        ''' quo_static_user_total_circles should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_static_user_total_circles(params)
        quote=Quotes.quo_static_user_total_circles.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_static_circle_total_members_no_cid(self):
        ''' quo_static_circle_total_members should fail if no cid is passed '''
        params={}
        self.assertIsNone(update.quo_static_circle_total_members(params))

    def test_quo_static_circle_total_members_non_existent_cid(self):
        ''' quo_static_circle_total_members should return None if cid does not exist '''
        cid=uuid.uuid4()
        params={'cid':cid}
        self.assertEqual(update.quo_static_circle_total_members(params),'0')

    def test_quo_static_circle_total_members_existent_cid(self):
        ''' quo_static_circle_total_members should return None if cid does not exist '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        circlename='test_quo_static_circle_total_members_existent_cid'
        creation_date=timeuuid.uuid1()
        type='circletype'
        members={uuid.uuid4()}
        circle=ormcircle.Circle(uid=uid,cid=cid,circlename=circlename,creation_date=creation_date,type=type,members=members)
        cassapicircle.insert_circle(circle)
        params={'cid':cid}
        result=update.quo_static_circle_total_members(params)
        self.assertEqual(result,1)
        quote=Quotes.quo_static_circle_total_members.name
        circle_quote=cassapiquote.get_circle_quote(cid=cid, quote=quote)
        self.assertEqual(circle_quote.value,result)

