import unittest
import uuid
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.auth.quotes import update
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import circle as cassapicircle
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komcass.model.orm import circle as ormcircle
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.time import timeuuid


class AuthQuotesUpdateTest(unittest.TestCase):
    ''' komlog.auth.quotes.update tests '''

    def setUp(self):
        username='test_auth.quotes.update.user'
        password='password'
        email='test_auth.quotes.update.user@komlog.org'
        try:
            uid = userapi.get_uid(username=username)
            self.user=userapi.get_user_config(uid=uid)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)

    def test_quo_user_total_agents_no_uid(self):
        ''' quo_user_total_agents should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_agents(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTA_UIDNF)

    def test_quo_user_total_agents_non_existent_user(self):
        ''' quo_user_total_agents should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_agents(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTA_USRNF)

    def test_quo_user_total_agents_success(self):
        ''' quo_user_total_agents should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_agents(params)
        quote=Quotes.quo_user_total_agents.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_datasources_no_uid(self):
        ''' quo_user_total_datasources should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTDS_UIDNF)

    def test_quo_user_total_datasources_non_existent_user(self):
        ''' quo_user_total_datasources should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTDS_USRNF)

    def test_quo_user_total_datasources_success(self):
        ''' quo_user_total_datasources should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_datasources(params)
        quote=Quotes.quo_user_total_datasources.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_datapoints_no_uid(self):
        ''' quo_user_total_datapoints should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTDP_UIDNF)

    def test_quo_user_total_datapoints_non_existent_user(self):
        ''' quo_user_total_datapoints should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTDP_USRNF)

    def test_quo_user_total_datapoints_success(self):
        ''' quo_user_total_datapoints should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_datapoints(params)
        quote=Quotes.quo_user_total_datapoints.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_widgets_no_uid(self):
        ''' quo_user_total_widgets should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_widgets(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTW_UIDNF)

    def test_quo_user_total_widgets_non_existent_user(self):
        ''' quo_user_total_widgets should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_widgets(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTW_USRNF)

    def test_quo_user_total_widgets_success(self):
        ''' quo_user_total_widgets should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_widgets(params)
        quote=Quotes.quo_user_total_widgets.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_dashboards_no_uid(self):
        ''' quo_user_total_dashboards should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_dashboards(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTDB_UIDNF)

    def test_quo_user_total_dashboards_non_existent_user(self):
        ''' quo_user_total_dashboards should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_dashboards(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTDB_USRNF)

    def test_quo_user_total_dashboards_success(self):
        ''' quo_user_total_dashboards should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_dashboards(params)
        quote=Quotes.quo_user_total_dashboards.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_agent_total_datasources_no_aid(self):
        ''' quo_agent_total_datasources should fail if no aid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_agent_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QATDS_AIDNF)

    def test_quo_agent_total_datasources_non_existent_agent(self):
        ''' quo_agent_total_datasources should fail if agent does not exist '''
        params={'aid':uuid.uuid4()}
        with self.assertRaises(exceptions.AgentNotFoundException) as cm:
            update.quo_agent_total_datasources(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QATDS_AGNF)

    def test_quo_agent_total_datasources_success(self):
        ''' quo_agent_total_datasources should succeed if AID is set'''
        uid=self.user['uid']
        agentname='test_quo_agent_total_datasources_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        params={'aid':aid}
        result=update.quo_agent_total_datasources(params)
        quote=Quotes.quo_agent_total_datasources.name
        agent_quote=cassapiquote.get_agent_quote(aid=aid, quote=quote)
        self.assertEqual(agent_quote.value,result)

    def test_quo_agent_total_datapoints_no_aid(self):
        ''' quo_agent_total_datapoints should fail if no aid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_agent_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QATDP_AIDNF)

    def test_quo_agent_total_datapoints_non_existent_agent(self):
        ''' quo_agent_total_datapoints should fail if agent does not exist '''
        params={'aid':uuid.uuid4()}
        with self.assertRaises(exceptions.AgentNotFoundException) as cm:
            update.quo_agent_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QATDP_AGNF)

    def test_quo_agent_total_datapoints_success(self):
        ''' quo_agent_total_datapoints should succeed if AID is set'''
        uid=self.user['uid']
        agentname='test_quo_agent_total_datapoints_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        params={'aid':aid}
        result=update.quo_agent_total_datapoints(params)
        quote=Quotes.quo_agent_total_datapoints.name
        agent_quote=cassapiquote.get_agent_quote(aid=aid, quote=quote)
        self.assertEqual(agent_quote.value,result)

    def test_quo_datasource_total_datapoints_no_did(self):
        ''' quo_datasource_total_datapoints should fail if no did is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_datasource_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDSTDP_DIDNF)

    def test_quo_datasource_total_datapoints_non_existent_datasource(self):
        ''' quo_datasource_total_datapoints should fail if ds does not exist '''
        params={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            update.quo_datasource_total_datapoints(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDSTDP_DSNF)

    def test_quo_datasource_total_datapoints_success(self):
        ''' quo_datasource_total_datapoints should succeed if DID is set'''
        uid=self.user['uid']
        agentname='test_quo_ds_total_dps_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename='ds.uri'
        ds=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        did=ds['did']
        params={'did':did}
        result=update.quo_datasource_total_datapoints(params)
        quote=Quotes.quo_datasource_total_datapoints.name
        datasource_quote=cassapiquote.get_datasource_quote(did=did, quote=quote)
        self.assertEqual(datasource_quote.value,result)

    def test_quo_user_total_snapshots_no_uid(self):
        ''' quo_user_total_snapshots should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_snapshots(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTSN_UIDNF)

    def test_quo_user_total_snapshots_non_existent_user(self):
        ''' quo_user_total_snapshots should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_snapshots(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTSN_USRNF)

    def test_quo_user_total_snapshots_success(self):
        ''' quo_user_total_snapshots should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_snapshots(params)
        quote=Quotes.quo_user_total_snapshots.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_user_total_circles_no_uid(self):
        ''' quo_user_total_circles should fail if no uid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_circles(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTC_UIDNF)

    def test_quo_user_total_circles_non_existent_user(self):
        ''' quo_user_total_circles should fail if user does not exist '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_circles(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTC_USRNF)

    def test_quo_user_total_circles_success(self):
        ''' quo_user_total_circles should succeed if UID is set'''
        uid=self.user['uid']
        params={'uid':uid}
        result=update.quo_user_total_circles(params)
        quote=Quotes.quo_user_total_circles.name
        user_quote=cassapiquote.get_user_quote(uid=uid, quote=quote)
        self.assertEqual(user_quote.value,result)

    def test_quo_circle_total_members_no_cid(self):
        ''' quo_circle_total_members should fail if no cid is passed '''
        params={}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_circle_total_members(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QCTM_CIDNF)

    def test_quo_circle_total_members_non_existent_cid(self):
        ''' quo_circle_total_members should return None if cid does not exist '''
        params={'cid':uuid.uuid4()}
        with self.assertRaises(exceptions.CircleNotFoundException) as cm:
            update.quo_circle_total_members(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QCTM_CRNF)

    def test_quo_circle_total_members_existent_cid(self):
        ''' quo_circle_total_members should return None if cid does not exist '''
        uid=self.user['uid']
        circlename='circlename'
        circle=circleapi.new_users_circle(uid=uid, circlename=circlename)
        cid=circle['cid']
        params={'cid':cid}
        result=update.quo_circle_total_members(params)
        self.assertEqual(result,0)
        quote=Quotes.quo_circle_total_members.name
        circle_quote=cassapiquote.get_circle_quote(cid=cid, quote=quote)
        self.assertEqual(circle_quote.value,result)

    def test_quo_daily_datasource_occupation_no_did(self):
        ''' quo_daily_datasource_occupation should return None if did is not found in parameters '''
        params={'date':timeuuid.uuid1()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDDSO_PNF)

    def test_quo_daily_datasource_occupation_no_date(self):
        ''' quo_daily_datasource_occupation should return None if date is not found in parameters '''
        params={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDDSO_PNF)

    def test_quo_daily_datasource_occupation_no_datasource_found(self):
        ''' quo_daily_datasource_occupation should return None if no datasource is found '''
        params={'did':uuid.uuid4(), 'date':timeuuid.uuid1()}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            update.quo_daily_datasource_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDDSO_DSNF)

    def test_quo_daily_datasource_occupation_first_sample_added(self):
        ''' quo_daily_datasource_ocuppation should set the sample size if this sample is the one
            who creates the quote '''
        uid=self.user['uid']
        did=uuid.uuid4()
        aid=uuid.uuid4()
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
        uid=self.user['uid']
        did=uuid.uuid4()
        aid=uuid.uuid4()
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
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDSO_PNF)

    def test_quo_daily_user_datasources_occupation_no_date(self):
        ''' quo_daily_user_datasources_occupation should return None if date is not found in parameters '''
        params={'did':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDSO_PNF)

    def test_quo_daily_user_datasources_occupation_no_datasource_found(self):
        ''' quo_daily_user_datasources_occupation should return None if no datasource is found '''
        params={'did':uuid.uuid4(), 'date':timeuuid.uuid1()}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDSO_DSNF)

    def test_quo_daily_user_datasources_occupation_no_user_found(self):
        ''' quo_daily_user_datasources_ocuppation should fail if user does not exist '''
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
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_daily_user_datasources_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDSO_USRNF)

    def test_quo_daily_user_datasources_occupation_first_sample_added(self):
        ''' quo_daily_user_datasources_ocuppation should set the sample size if this sample is the one
            who creates the quote '''
        username='quo_user_daily_user_datasources_occupation_first_sample_added'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
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
        username='quo_user_daily_user_occupation_non_first_sample_added'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=self.user['uid']
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
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_user_total_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTO_DIDNF)

    def test_quo_user_total_occupation_datasource_not_found(self):
        ''' quo_user_total_occupation should return None if datasource does not exist '''
        did=uuid.uuid4()
        params={'did':did}
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            update.quo_user_total_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTO_DSNF)

    def test_quo_user_total_occupation_no_user_found(self):
        ''' quo_user_total_ocuppation should fail if user does not exist '''
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
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_user_total_occupation(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QUTO_USRNF)

    def test_quo_user_total_occupation_no_quotes_found_first_exec(self):
        ''' quo_user_total_ocuppation should return 0 if there is no quote found, and set the total occupation to 0 '''
        username='quo_user_total_occupation_no_quotes_found_first_exec'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
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
        username='quo_user_total_occupation_no_quotes_found'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
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
        self.assertEqual(result,None)

    def test_quo_user_total_occupation_quotes_found_first_exec(self):
        ''' quo_daily_user_ocuppation should add the sample size to the existing value '''
        username='quo_user_total_occupation_quotes_found'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
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

    def test_quo_daily_user_data_post_counter_failure_invalid_parameters_no_uid(self):
        ''' quo_daily_user_data_post_counter should fail if params has no uid key '''
        params={'date':timeuuid.uuid1()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_daily_user_data_post_counter(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDPC_PNF)

    def test_quo_daily_user_data_post_counter_failure_invalid_parameters_no_date(self):
        ''' quo_daily_user_data_post_counter should fail if params has no did key '''
        params={'uid':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            update.quo_daily_user_data_post_counter(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDPC_PNF)

    def test_quo_daily_user_data_post_counter_failure_user_not_found(self):
        ''' quo_daily_user_data_post_counter should fail if user does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        params={'uid':uid, 'date':date}
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            update.quo_daily_user_data_post_counter(params)
        self.assertEqual(cm.exception.error, Errors.E_AQU_QDUDPC_USRNF)

    def test_quo_daily_user_data_post_counter_success(self):
        ''' quo_daily_user_data_post_counter should succeed and increment the counter by 1 '''
        username='test_quo_daily_user_data_post_counter_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        date=timeuuid.uuid1()
        params={'uid':uid, 'date':date}
        counter=update.quo_daily_user_data_post_counter(params)
        self.assertEqual(counter, 1)
        counter=update.quo_daily_user_data_post_counter(params)
        self.assertEqual(counter, 2)
