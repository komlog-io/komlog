import unittest
import uuid
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komlibs.auth.quotes import compare
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.general.time import timeuuid

class AuthQuotesCompareTest(unittest.TestCase):
    ''' komlog.auth.quotes.compare tests '''
    
    def setUp(self):
        username='test_auth.quotes.user'
        password='password'
        email='test_auth.quotes.user@komlog.org'
        try:
            uid = userapi.get_uid(username=username)
            self.user=userapi.get_user_config(uid=uid)
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

    def test_quo_static_user_total_circles_no_uid(self):
        ''' quo_static_user_total_circles should fail if no uid is passed '''
        params={}
        self.assertIsNone(compare.quo_static_user_total_circles(params))

    def test_quo_static_user_total_circles_non_existent_user(self):
        ''' quo_static_user_total_circles should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_user_total_circles(params))

    def test_quo_static_user_total_circles_failure(self):
        ''' quo_static_user_total_circles should fail because user has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_user_total_circles(params))

    def test_quo_static_circle_total_members_no_uid(self):
        ''' quo_static_circle_total_members should fail if no uid is passed '''
        params={'cid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_circle_total_members(params))

    def test_quo_static_circle_total_members_no_cid(self):
        ''' quo_static_circle_total_members should fail if no uid is passed '''
        params={'uid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_circle_total_members(params))

    def test_quo_static_circle_total_members_non_existent_user(self):
        ''' quo_static_circle_total_members should fail if uid does not exist on system '''
        params={'uid':uuid.uuid4(),'cid':uuid.uuid4()}
        self.assertIsNone(compare.quo_static_circle_total_members(params))

    def test_quo_static_circle_total_members_failure(self):
        ''' quo_static_circle_total_members should fail because circle has no quote info yet '''
        params={'uid':self.user['uid']}
        self.assertFalse(compare.quo_static_circle_total_members(params))

    def test_quo_daily_datasource_occupation_failure_no_did(self):
        ''' quo_daily_datasource_occupation should return None if params has no did '''
        params={'date':timeuuid.uuid1()}
        self.assertIsNone(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_failure_no_date(self):
        ''' quo_daily_datasource_occupation should return None if params has no date '''
        params={'did':uuid.uuid4()}
        self.assertIsNone(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_failure_non_existent_datasource(self):
        ''' quo_daily_datasource_occupation should return None if datasource does not exist '''
        params={'date':timeuuid.uuid1(), 'did':uuid.uuid4()}
        self.assertIsNone(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_failure_non_existent_user(self):
        ''' quo_daily_datasource_occupation should return None if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_datasource_occupation_failure_non_existent_user'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        self.assertIsNone(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_non_existent_segment_quote(self):
        ''' quo_daily_datasource_occupation should return False if segment has not defined this quote '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation_non_existent_segment_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation_failure_non_existent_segment_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_non_existent_datasource_ts_quote(self):
        ''' quo_daily_datasource_occupation should return False if user has not set this quote yet '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation_non_existent_user_ts_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation_failure_non_existent_datasource_ts_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_datasource_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_datasource_quote_is_not_greater_than_segment_value(self):
        ''' quo_daily_datasource_occupation should return False if datasource quote value is not greater than the maximum value allowed set in the segment '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_datasource_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_datasource_ts_quote(did=did, quote=quote, ts=ts, value=9))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_datasource_occupation(params))
        self.assertTrue(cassapiquote.insert_datasource_ts_quote(did=did, quote=quote, ts=ts, value=10))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_user_quote_is_greater_than_segment_value(self):
        ''' quo_daily_datasource_occupation should return True if user quote value is greater than the maximum value allowed set in the segment '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_datasource_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_datasource_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_datasource_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_datasource_ts_quote(did=did, quote=quote, ts=ts, value=11))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_datasource_occupation(params))

    def test_quo_daily_user_datasources_occupation_failure_no_did(self):
        ''' quo_daily_user_datasources_occupation should return None if params has no did '''
        params={'date':timeuuid.uuid1()}
        self.assertIsNone(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_failure_no_date(self):
        ''' quo_daily_user_datasources_occupation should return None if params has no date '''
        params={'did':uuid.uuid4()}
        self.assertIsNone(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_failure_non_existent_datasource(self):
        ''' quo_daily_user_datasources_occupation should return None if datasource does not exist '''
        params={'date':timeuuid.uuid1(), 'did':uuid.uuid4()}
        self.assertIsNone(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_failure_non_existent_user(self):
        ''' quo_daily_user_datasources_occupation should return None if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_user_datasources_occupation_failure_non_existent_user'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        self.assertIsNone(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_non_existent_segment_quote(self):
        ''' quo_daily_user_datasources_occupation should return False if segment has not defined this quote '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation_non_existent_segment_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation_failure_non_existent_segment_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_non_existent_user_ts_quote(self):
        ''' quo_daily_user_datasources_occupation should return False if user has not set this quote yet '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation_non_existent_user_ts_quote'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation_failure_non_existent_user_ts_quote'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_user_quote_is_not_greater_than_segment_value(self):
        ''' quo_daily_user_datasources_occupation should return False if user quote value is not greater than the maximum value allowed set in the segment '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=9))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_user_datasources_occupation(params))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=10))
        params={'did':did, 'date':date}
        self.assertFalse(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_user_quote_is_greater_than_segment_value(self):
        ''' quo_daily_user_datasources_occupation should return True if user quote value is greater than the maximum value allowed set in the segment '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_daily_user_datasources_occupation'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='test_quo_daily_user_datasources_occupation'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment, quote=quote, value=10))
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=11))
        params={'did':did, 'date':date}
        self.assertTrue(compare.quo_daily_user_datasources_occupation(params))

    def test_quo_total_user_occupation_no_did_param(self):
        ''' quo_total_user_occupation should return None if no did param is passed '''
        params={}
        self.assertIsNone(compare.quo_total_user_occupation(params))

    def test_quo_total_user_occupation_no_datasource_found(self):
        ''' quo_total_user_occupation should return None if datasource does not exist '''
        did=uuid.uuid4()
        params={'did':did}
        self.assertIsNone(compare.quo_total_user_occupation(params))

    def test_quo_total_user_occupation_no_user_found(self):
        ''' quo_total_user_occupation should return None if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        self.assertIsNone(compare.quo_total_user_occupation(params))

    def test_quo_total_user_occupation_no_segment_quo_stablished(self):
        ''' quo_total_user_occupation should return False if segment quote is not established '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_total_user_occupation_no_segment_quo_stablished'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        self.assertFalse(compare.quo_total_user_occupation(params))

    def test_quo_total_user_occupation_no_user_quote_found(self):
        ''' quo_total_user_occupation should return False if user quote is not found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_total_user_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_total_user_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        params={'did':did}
        self.assertFalse(compare.quo_total_user_occupation(params))


    def test_quo_total_user_occupation_user_quote_less_than_limit(self):
        ''' quo_total_user_occupation should return False if user quote has not surpassed segment limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_total_user_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_total_user_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        ts=1
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=1))
        params={'did':did}
        self.assertFalse(compare.quo_total_user_occupation(params))

    def test_quo_total_user_occupation_user_quote_above_limit(self):
        ''' quo_total_user_occupation should return True if user quote has surpassed segment limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_total_user_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_total_user_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        ts=1
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=11))
        params={'did':did}
        self.assertTrue(compare.quo_total_user_occupation(params))

    def test_quo_total_user_occupation_user_quote_under_limit_after_surpassing(self):
        ''' quo_total_user_occupation should return True if user quote has surpassed segment limit and after that, the quote has decreased under segment limit '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_total_user_occupation_no_user_quote_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasourcename'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_total_user_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        ts=1
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=11))
        params={'did':did}
        self.assertTrue(compare.quo_total_user_occupation(params))
        ts=2
        self.assertTrue(cassapiquote.insert_user_ts_quote(uid=uid, quote=quote, ts=ts, value=1))
        self.assertFalse(compare.quo_total_user_occupation(params))

