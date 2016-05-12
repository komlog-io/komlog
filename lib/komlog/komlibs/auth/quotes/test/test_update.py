import unittest
import uuid
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.auth.quotes import update
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komcass.model.orm import circle as ormcircle
from komlog.komlibs.general.time import timeuuid


class AuthQuotesUpdateTest(unittest.TestCase):
    ''' komlog.auth.quotes.update tests '''
    
    def test_quo_user_total_agents_no_uid(self):
        ''' quo_user_total_agents should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_agents(params))

    def test_quo_user_total_agents_success(self):
        ''' quo_user_total_agents should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_agents(params)
        quote=Quotes.quo_user_total_agents.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_datasources_no_uid(self):
        ''' quo_user_total_datasources should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_datasources(params))

    def test_quo_user_total_datasources_success(self):
        ''' quo_user_total_datasources should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_datasources(params)
        quote=Quotes.quo_user_total_datasources.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_datapoints_no_uid(self):
        ''' quo_user_total_datapoints should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_datapoints(params))

    def test_quo_user_total_datapoints_success(self):
        ''' quo_user_total_datapoints should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_datapoints(params)
        quote=Quotes.quo_user_total_datapoints.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_widgets_no_uid(self):
        ''' quo_user_total_widgets should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_widgets(params))

    def test_quo_user_total_widgets_success(self):
        ''' quo_user_total_widgets should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_widgets(params)
        quote=Quotes.quo_user_total_widgets.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_dashboards_no_uid(self):
        ''' quo_user_total_dashboards should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_dashboards(params))

    def test_quo_user_total_dashboards_success(self):
        ''' quo_user_total_dashboards should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_dashboards(params)
        quote=Quotes.quo_user_total_dashboards.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_agent_total_datasources_no_aid(self):
        ''' quo_agent_total_datasources should fail if no aid is passed '''
        params={}
        self.assertIsNone(update.quo_agent_total_datasources(params))

    def test_quo_agent_total_datasources_success(self):
        ''' quo_agent_total_datasources should succeed if AID is set'''
        aid=uuid.uuid4()
        params={'aid':aid}
        result=update.quo_agent_total_datasources(params)
        quote=Quotes.quo_agent_total_datasources.name
        agent_quote=cassapiquote.get_agent_quote(aid=aid, quote=quote)
        self.assertEqual(agent_quote.value,result)

    def test_quo_agent_total_datapoints_no_aid(self):
        ''' quo_agent_total_datapoints should fail if no aid is passed '''
        params={}
        self.assertIsNone(update.quo_agent_total_datapoints(params))

    def test_quo_agent_total_datapoints_success(self):
        ''' quo_agent_total_datapoints should succeed if AID is set'''
        aid=uuid.uuid4()
        params={'aid':aid}
        result=update.quo_agent_total_datapoints(params)
        quote=Quotes.quo_agent_total_datapoints.name
        agent_quote=cassapiquote.get_agent_quote(aid=aid, quote=quote)
        self.assertEqual(agent_quote.value,result)

    def test_quo_datasource_total_datapoints_no_did(self):
        ''' quo_datasource_total_datapoints should fail if no did is passed '''
        params={}
        self.assertIsNone(update.quo_datasource_total_datapoints(params))

    def test_quo_datasource_total_datapoints_success(self):
        ''' quo_datasource_total_datapoints should succeed if DID is set'''
        did=uuid.uuid4()
        params={'did':did}
        result=update.quo_datasource_total_datapoints(params)
        quote=Quotes.quo_datasource_total_datapoints.name
        datasource_quote=cassapiquote.get_datasource_quote(did=did, quote=quote)
        self.assertEqual(datasource_quote.value,result)

    def test_quo_user_total_snapshots_no_uid(self):
        ''' quo_user_total_snapshots should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_snapshots(params))

    def test_quo_user_total_snapshots_success(self):
        ''' quo_user_total_snapshots should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_snapshots(params)
        quote=Quotes.quo_user_total_snapshots.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_circles_no_uid(self):
        ''' quo_user_total_circles should fail if no uid is passed '''
        params={}
        self.assertIsNone(update.quo_user_total_circles(params))

    def test_quo_user_total_circles_success(self):
        ''' quo_user_total_circles should succeed if UID is set'''
        uid=uuid.uuid4()
        params={'uid':uid}
        result=update.quo_user_total_circles(params)
        quote=Quotes.quo_user_total_circles.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_circle_total_members_no_cid(self):
        ''' quo_circle_total_members should fail if no cid is passed '''
        params={}
        self.assertIsNone(update.quo_circle_total_members(params))

    def test_quo_circle_total_members_non_existent_cid(self):
        ''' quo_circle_total_members should return None if cid does not exist '''
        cid=uuid.uuid4()
        params={'cid':cid}
        self.assertEqual(update.quo_circle_total_members(params),'0')

    def test_quo_circle_total_members_existent_cid(self):
        ''' quo_circle_total_members should return None if cid does not exist '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        circlename='test_quo_circle_total_members_existent_cid'
        creation_date=timeuuid.uuid1()
        type='circletype'
        members={uuid.uuid4()}
        circle=ormcircle.Circle(uid=uid,cid=cid,circlename=circlename,creation_date=creation_date,type=type,members=members)
        cassapicircle.insert_circle(circle)
        params={'cid':cid}
        result=update.quo_circle_total_members(params)
        self.assertEqual(result,1)
        quote=Quotes.quo_circle_total_members.name
        circle_quote=cassapiquote.get_circle_quote(cid=cid, quote=quote)
        self.assertEqual(circle_quote.value,result)

    def test_quo_daily_datasource_occupation_no_did(self):
        ''' quo_daily_datasource_occupation should return None if did is not found in parameters '''
        params={'date':timeuuid.uuid1()}
        self.assertIsNone(update.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_no_date(self):
        ''' quo_daily_datasource_occupation should return None if date is not found in parameters '''
        params={'did':uuid.uuid4()}
        self.assertIsNone(update.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_no_datasource_found(self):
        ''' quo_daily_datasource_occupation should return None if no datasource is found '''
        params={'did':uuid.uuid4(), 'date':timeuuid.uuid1()}
        self.assertIsNone(update.quo_daily_datasource_occupation(params))

    def test_quo_daily_datasource_occupation_first_sample_added(self):
        ''' quo_daily_datasource_ocuppation should set the sample size if this sample is the one
            who creates the quote '''
        did=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_datasource_occupation(params)
        self.assertEqual(result,size)
        quote=Quotes.quo_daily_datasource_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        quotes=cassapiquote.get_datasource_ts_quotes(did=did, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].did,did)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,100)


    def test_quo_daily_datasource_occupation_non_first_sample_added(self):
        ''' quo_daily_datasource_ocuppation should add the sample size to the existing value '''
        did=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_datasource_occupation(params)
        self.assertEqual(result,size)
        date=timeuuid.uuid1()
        size=300
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_datasource_occupation(params)
        self.assertEqual(result, 400)
        quote=Quotes.quo_daily_datasource_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        quotes=cassapiquote.get_datasource_ts_quotes(did=did, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].did,did)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,400)

    def test_quo_daily_user_datasources_occupation_no_did(self):
        ''' quo_daily_user_datasources_occupation should return None if did is not found in parameters '''
        params={'date':timeuuid.uuid1()}
        self.assertIsNone(update.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_no_date(self):
        ''' quo_daily_user_datasources_occupation should return None if date is not found in parameters '''
        params={'did':uuid.uuid4()}
        self.assertIsNone(update.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_no_datasource_found(self):
        ''' quo_daily_user_datasources_occupation should return None if no datasource is found '''
        params={'did':uuid.uuid4(), 'date':timeuuid.uuid1()}
        self.assertIsNone(update.quo_daily_user_datasources_occupation(params))

    def test_quo_daily_user_datasources_occupation_first_sample_added(self):
        ''' quo_daily_user_datasources_ocuppation should set the sample size if this sample is the one
            who creates the quote '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(result,size)
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        quotes=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].uid,uid)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,100)

    def test_quo_daily_user_occupation_non_first_sample_added(self):
        ''' quo_daily_user_ocuppation should add the sample size to the existing value '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(result,size)
        date=timeuuid.uuid1()
        size=300
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(result, 400)
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=timeuuid.get_day_timestamp(date)
        quotes=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].uid,uid)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,400)

    def test_quo_user_total_occupation_did_not_found(self):
        ''' quo_user_total_occupation should return None if params has no did parameter '''
        params={}
        self.assertIsNone(update.quo_user_total_occupation(params))

    def test_quo_user_total_occupation_datasource_not_found(self):
        ''' quo_user_total_occupation should return None if datasource does not exist '''
        did=uuid.uuid4()
        params={'did':did}
        self.assertIsNone(update.quo_user_total_occupation(params))

    def test_quo_user_total_occupation_no_quotes_found_first_exec(self):
        ''' quo_user_total_ocuppation should return 0 if there is no quote found, and set the total occupation to 0 '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        params={'did':did}
        result=update.quo_user_total_occupation(params)
        self.assertEqual(result,0)
        quote=Quotes.quo_user_total_occupation.name
        ts=timeuuid.get_hour_timestamp(date)
        quotes=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].uid,uid)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,0)

    def test_quo_user_total_occupation_no_quotes_found_not_first_exec(self):
        ''' quo_user_total_ocuppation should return None if the hourly execution of the quote has already been done '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        params={'did':did}
        result=update.quo_user_total_occupation(params)
        self.assertEqual(result,0)
        quote=Quotes.quo_user_total_occupation.name
        ts=timeuuid.get_hour_timestamp(date)
        quotes=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].uid,uid)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,0)
        result=update.quo_user_total_occupation(params)
        self.assertEqual(result, None)

    def test_quo_user_total_occupation_quotes_found_first_exec(self):
        ''' quo_daily_user_ocuppation should add the sample size to the existing value '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        aid=uuid.uuid4()
        date=timeuuid.uuid1(seconds=1)
        size=100
        datasource=ormdatasource.Datasource(did=did, uid=uid, aid=aid, datasourcename='datasourcename', creation_date=date)
        self.assertTrue(cassapidatasource.new_datasource(datasource=datasource))
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(result,size)
        date=timeuuid.uuid1(seconds=100000)
        size=300
        metadata=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(cassapidatasource.insert_datasource_metadata(obj=metadata))
        params={'did':did, 'date':date}
        result=update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(result, 300)
        quote=Quotes.quo_daily_user_datasources_occupation.name
        quotes=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotes),2)
        params={'did':did}
        result=update.quo_user_total_occupation(params)
        self.assertEqual(result,400)
        quote=Quotes.quo_user_total_occupation.name
        ts=timeuuid.get_hour_timestamp(timeuuid.uuid1())
        quotes=cassapiquote.get_user_ts_quotes(uid=uid, quote=quote)
        self.assertEqual(len(quotes),1)
        self.assertEqual(quotes[0].uid,uid)
        self.assertEqual(quotes[0].quote,quote)
        self.assertEqual(quotes[0].ts,ts)
        self.assertEqual(quotes[0].value,400)
