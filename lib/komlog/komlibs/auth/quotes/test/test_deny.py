import unittest
import uuid
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import quote as cassapiquote
from komlog.komcass.api import segment as cassapisegment
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.quotes import deny
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.model.quotes import Quotes
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.general.time import timeuuid

class AuthQuotesDenyTest(unittest.TestCase):
    ''' komlog.auth.quotes.deny tests '''
    
    def setUp(self):
        username='test_auth.quotes.user'
        password='password'
        email='test_auth.quotes.user@komlog.org'
        try:
            uid = userapi.get_uid(username=username)
            self.user=userapi.get_user_config(uid=uid)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)

    def test_quo_user_total_agents_no_uid(self):
        ''' quo_user_total_agents should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_agents(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTA_UIDNF)

    def test_quo_user_total_agents_success(self):
        ''' quo_user_total_agents should succeed if deny flag is True and UID is set'''
        params={'uid':self.user['uid']}
        flag=True
        iface=interfaces.User_AgentCreation().value
        self.assertTrue(deny.quo_user_total_agents(params,flag))
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.interface,interfaces.User_AgentCreation().value)
        self.assertEqual(db_iface.perm,deny.DEFAULT_PERM)
        self.assertEqual(db_iface.uid,params['uid'])

    def test_quo_user_total_agents_unsuccess(self):
        ''' quo_user_total_agents should succeed if deny flag is False and UID is set'''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_agents(params,flag))
        iface=interfaces.User_AgentCreation().value
        db_iface=cassapiiface.get_user_iface_deny(uid=params['uid'],iface=iface)
        self.assertIsNone(db_iface)

    def test_quo_user_total_datasources_no_uid(self):
        ''' quo_user_total_datasources should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_datasources(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTDS_UIDNF)

    def test_quo_user_total_datasources_success(self):
        ''' quo_user_total_datasources should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_user_total_datasources(params,flag))

    def test_quo_user_total_datasources_unsuccess(self):
        ''' quo_user_total_datasources should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_datasources(params,flag))

    def test_quo_user_total_datapoints_no_uid(self):
        ''' quo_user_total_datapoints should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_datapoints(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTDP_UIDNF)

    def test_quo_user_total_datapoints_success(self):
        ''' quo_user_total_datapoints should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_user_total_datapoints(params,flag))

    def test_quo_user_total_datapoints_unsuccess(self):
        ''' quo_user_total_datapoints should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_datapoints(params,flag))

    def test_quo_user_total_widgets_no_uid(self):
        ''' quo_user_total_widgets should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_widgets(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTW_UIDNF)

    def test_quo_user_total_widgets_success(self):
        ''' quo_user_total_widgets should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_user_total_widgets(params,flag))

    def test_quo_user_total_widgets_unsuccess(self):
        ''' quo_user_total_widgets should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_widgets(params,flag))

    def test_quo_user_total_dashboards_no_uid(self):
        ''' quo_user_total_dashboards should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_dashboards(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTDB_UIDNF)

    def test_quo_user_total_dashboards_success(self):
        ''' quo_user_total_dashboards should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_user_total_dashboards(params,flag))

    def test_quo_user_total_dashboards_unsuccess(self):
        ''' quo_user_total_dashboards should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_dashboards(params,flag))

    def test_quo_agent_total_datasources_no_uid(self):
        ''' quo_agent_total_datasources should fail if no uid is passed '''
        params={'aid':self.user['uid']}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_agent_total_datasources(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QATDS_PNF)

    def test_quo_agent_total_datasources_no_aid(self):
        ''' quo_agent_total_datasources should fail if no aid is passed '''
        params={'uid':self.user['uid']}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_agent_total_datasources(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QATDS_PNF)

    def test_quo_agent_total_datasources_success(self):
        ''' quo_agent_total_datasources should succeed if deny flag is True and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_agent_total_datasources(params,flag))

    def test_quo_agent_total_datasources_unsuccess(self):
        ''' quo_agent_total_datasources should succeed if deny flag is False and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_agent_total_datasources(params,flag))

    def test_quo_agent_total_datapoints_no_uid(self):
        ''' quo_agent_total_datapoints should fail if no uid is passed '''
        params={'aid':uuid.uuid4()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_agent_total_datapoints(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QATDP_PNF)

    def test_quo_agent_total_datapoints_no_aid(self):
        ''' quo_agent_total_datapoints should fail if no aid is passed '''
        params={'uid':self.user['uid']}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_agent_total_datapoints(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QATDP_PNF)

    def test_quo_agent_total_datapoints_success(self):
        ''' quo_agent_total_datapoints should succeed if deny flag is True and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_agent_total_datapoints(params,flag))

    def test_quo_agent_total_datapoints_unsuccess(self):
        ''' quo_agent_total_datapoints should succeed if deny flag is False and UID and AID are set '''
        params={'uid':self.user['uid'],'aid':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_agent_total_datapoints(params,flag))

    def test_quo_datasource_total_datapoints_no_uid(self):
        ''' quo_datasource_total_datapoints should fail if no uid is passed '''
        params={'did':uuid.uuid4()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_datasource_total_datapoints(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDSTDP_PNF)

    def test_quo_datasource_total_datapoints_no_did(self):
        ''' quo_datasource_total_datapoints should fail if no did is passed '''
        params={'uid':self.user['uid']}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_datasource_total_datapoints(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDSTDP_PNF)

    def test_quo_datasource_total_datapoints_success(self):
        ''' quo_datasource_total_datapoints should succeed if deny flag is True and UID and DID are set '''
        params={'uid':self.user['uid'],'did':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_datasource_total_datapoints(params,flag))

    def test_quo_datasource_total_datapoints_unsuccess(self):
        ''' quo_datasource_total_datapoints should succeed if deny flag is False and UID and DID are set '''
        params={'uid':self.user['uid'],'did':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_datasource_total_datapoints(params,flag))

    def test_quo_user_total_snapshots_no_uid(self):
        ''' quo_user_total_snapshots should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_snapshots(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTSN_UIDNF)

    def test_quo_user_total_snapshots_success(self):
        ''' quo_user_total_snapshots should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_user_total_snapshots(params,flag))

    def test_quo_user_total_snapshots_unsuccess(self):
        ''' quo_user_total_snapshots should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_snapshots(params,flag))

    def test_quo_user_total_circles_no_uid(self):
        ''' quo_user_total_circles should fail if no uid is passed '''
        params={}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_circles(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTC_UIDNF)

    def test_quo_user_total_circles_success(self):
        ''' quo_user_total_circles should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid']}
        flag=True
        self.assertTrue(deny.quo_user_total_circles(params,flag))

    def test_quo_user_total_circles_unsuccess(self):
        ''' quo_user_total_circles should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid']}
        flag=False
        self.assertTrue(deny.quo_user_total_circles(params,flag))

    def test_quo_circle_total_members_no_uid(self):
        ''' quo_circle_total_members should fail if no uid is passed '''
        params={'cid':uuid.uuid4()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_circle_total_members(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QCTM_PNF)

    def test_quo_circle_total_members_no_cid(self):
        ''' quo_circle_total_members should fail if no cid is passed '''
        params={'uid':uuid.uuid4()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_circle_total_members(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QCTM_PNF)

    def test_quo_circle_total_members_success(self):
        ''' quo_circle_total_members should succeed if deny flag is True and UID is set '''
        params={'uid':self.user['uid'],'cid':uuid.uuid4()}
        flag=True
        self.assertTrue(deny.quo_circle_total_members(params,flag))

    def test_quo_circle_total_members_unsuccess(self):
        ''' quo_circle_total_members should succeed if deny flag is False and UID is set '''
        params={'uid':self.user['uid'],'cid':uuid.uuid4()}
        flag=False
        self.assertTrue(deny.quo_circle_total_members(params,flag))

    def test_quo_daily_datasource_occupation_failure_no_did(self):  
        ''' quo_daily_datasource_occupation should return False if params has no did '''
        params={'date':timeuuid.uuid1()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_daily_datasource_occupation(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDDSO_PNF)

    def test_quo_daily_datasource_occupation_failure_no_date(self):  
        ''' quo_daily_datasource_occupation should return False if params has no date '''
        params={'did':uuid.uuid4()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_daily_datasource_occupation(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDDSO_PNF)

    def test_quo_daily_datasource_occupation_failure_non_existing_datasource(self):  
        ''' quo_daily_datasource_occupation should return False if datasource does not exist '''
        params={'did':uuid.uuid4(), 'date':timeuuid.uuid1()}
        flag=True
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            deny.quo_daily_datasource_occupation(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDDSO_DSNF)

    def test_quo_daily_datasource_occupation_success_deny_true(self):  
        ''' quo_daily_datasource_occupation should return True and set the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_datasource_occupation_success_deny_true'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        flag=True
        self.assertTrue(deny.quo_daily_datasource_occupation(params,flag))
        iface=interfaces.User_PostDatasourceDataDaily(did=did).value
        ts=timeuuid.get_day_timestamp(date)
        db_iface=cassapiiface.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, uid)
        self.assertEqual(db_iface.interface,iface)
        self.assertEqual(db_iface.ts,ts)
        self.assertEqual(db_iface.perm,deny.DEFAULT_PERM)

    def test_quo_daily_datasource_occupation_success_deny_false(self):  
        ''' quo_daily_datasource_occupation should return True and delete the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_datasource_occupation_success_deny_false'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        flag=False
        self.assertTrue(deny.quo_daily_datasource_occupation(params,flag))
        iface=interfaces.User_PostDatasourceDataDaily(did=did).value
        ts=timeuuid.get_day_timestamp(date)
        db_iface=cassapiiface.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
        self.assertIsNone(db_iface)

    def test_quo_daily_user_datasources_occupation_failure_no_did(self):  
        ''' quo_daily_user_datasources_occupation should return False if params has no did '''
        params={'date':timeuuid.uuid1()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_daily_user_datasources_occupation(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDUDSO_PNF)

    def test_quo_daily_user_datasources_occupation_failure_no_did(self):  
        ''' quo_daily_user_datasources_occupation should return False if params has no date '''
        params={'did':uuid.uuid4()}
        flag=True
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_daily_user_datasources_occupation(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDUDSO_PNF)

    def test_quo_daily_user_datasources_occupation_failure_non_existing_datasource(self):  
        ''' quo_daily_user_datasources_occupation should return False if datasource does not exist '''
        params={'did':uuid.uuid4(), 'date':timeuuid.uuid1()}
        flag=True
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            deny.quo_daily_user_datasources_occupation(params,flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QDUDSO_DSNF)

    def test_quo_daily_user_datasources_occupation_success_deny_true(self):  
        ''' quo_daily_user_datasources_occupation should return True and set the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_user_datasources_occupation_success_deny_true'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        flag=True
        self.assertTrue(deny.quo_daily_user_datasources_occupation(params,flag))
        iface=interfaces.User_PostDatasourceDataDaily().value
        ts=timeuuid.get_day_timestamp(date)
        db_iface=cassapiiface.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, uid)
        self.assertEqual(db_iface.interface,iface)
        self.assertEqual(db_iface.ts,ts)
        self.assertEqual(db_iface.perm,deny.DEFAULT_PERM)

    def test_quo_daily_user_datasources_occupation_success_deny_false(self):  
        ''' quo_daily_user_datasources_occupation should return True and delete the deny interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='test_quo_daily_user_datasources_occupation_success_deny_false'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did, 'date':date}
        flag=False
        self.assertTrue(deny.quo_daily_user_datasources_occupation(params,flag))
        iface=interfaces.User_PostDatasourceDataDaily().value
        ts=timeuuid.get_day_timestamp(date)
        db_iface=cassapiiface.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts)
        self.assertIsNone(db_iface)

    def test_quo_user_total_occupation_no_did_in_params(self):
        ''' quo_user_total_occupation should return False if no did parameter is passed '''
        params={}
        flag=False
        with self.assertRaises(exceptions.BadParametersException) as cm:
            deny.quo_user_total_occupation(params, flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTO_DIDNF)

    def test_quo_user_total_occupation_no_datasource_found(self):
        ''' quo_user_total_occupation should return False if datasource does not exist '''
        did=uuid.uuid4()
        params={'did':did}
        flag=False
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            deny.quo_user_total_occupation(params, flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTO_DSNF)

    def test_quo_user_total_occupation_no_user_found(self):
        ''' quo_user_total_occupation should return False if user does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        flag=False
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            deny.quo_user_total_occupation(params, flag)
        self.assertEqual(cm.exception.error, Errors.E_AQD_QUTO_USRNF)

    def test_quo_user_total_occupation_success_deny_false(self):
        ''' quo_user_total_occupation should return True and delete the interface '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_success_deny_false'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        flag=False
        self.assertTrue(deny.quo_user_total_occupation(params,flag))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid, iface=iface)
        self.assertIsNone(db_iface)

    def test_quo_user_total_occupation_failure_deny_true_but_no_segment_quote_stablished(self):
        ''' quo_user_total_occupation should return False if we want to set the deny interface 
            but the segment quote is not set
        '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_failure_deny_true_but_no_segment_quote_set'
        email=username+'@komlog.org'
        password=b'password'
        segment=99
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        params={'did':did}
        flag=True
        self.assertFalse(deny.quo_user_total_occupation(params,flag))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid, iface=iface)
        self.assertIsNone(db_iface)

    def test_quo_user_total_occupation_success_deny_true_but_no_min_ts_found(self):
        ''' quo_user_total_occupation should return True if we try to set the deny interface
            but the function does not find the minimal timestamp when it tries to calculate it
            because the sum of quotes does not surpasses the segment limit.'''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_failure_deny_true_but_no_min_ts_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        params={'did':did}
        flag=True
        self.assertTrue(deny.quo_user_total_occupation(params,flag))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid, iface=iface)
        self.assertIsNone(db_iface)

    def test_quo_user_total_occupation_success_deny_true_min_ts_found(self):
        ''' quo_user_total_occupation should return True and set the deny interface
            if the sum of quotes surpasses the segment limit.'''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_failure_deny_true_but_no_min_ts_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=1000
        value=100
        n_val=cassapiquote.new_user_ts_quote(uid=uid,quote=quote,ts=ts,value=value)
        params={'did':did}
        flag=True
        self.assertTrue(deny.quo_user_total_occupation(params,flag))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid, iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, uid)
        self.assertEqual(db_iface.interface,iface)
        self.assertEqual(db_iface.perm, timeuuid.min_uuid_from_time(ts).hex)

    def test_quo_user_total_occupation_success_deny_true_min_ts_found_on_second_occupation_value(self):
        ''' quo_user_total_occupation should return True and set the deny interface
            if the sum of quotes surpasses the segment limit. In this case, after the first quote
            value.
        '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        username='test_quo_user_total_occupation_failure_deny_true_but_no_min_ts_found'
        email=username+'@komlog.org'
        password=b'password'
        segment=0
        state=0
        user=ormuser.User(username=username, uid=uid, password=password, email=email, segment=segment, creation_date=timeuuid.uuid1(), state=state)
        self.assertTrue(cassapiuser.insert_user(user))
        datasourcename='datasource'
        datasource=ormdatasource.Datasource(uid=uid, did=did, datasourcename=datasourcename, aid=aid, creation_date=timeuuid.uuid1())
        self.assertTrue(cassapidatasource.new_datasource(datasource))
        quote=Quotes.quo_user_total_occupation.name
        self.assertTrue(cassapisegment.insert_user_segment_quote(sid=segment,quote=quote,value=1))
        quote=Quotes.quo_daily_user_datasources_occupation.name
        ts=1000
        value=1
        n_val=cassapiquote.new_user_ts_quote(uid=uid,quote=quote,ts=ts,value=value)
        ts=999
        value=1
        n_val=cassapiquote.new_user_ts_quote(uid=uid,quote=quote,ts=ts,value=value)
        params={'did':did}
        flag=True
        self.assertTrue(deny.quo_user_total_occupation(params,flag))
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        db_iface=cassapiiface.get_user_iface_deny(uid=uid, iface=iface)
        self.assertIsNotNone(db_iface)
        self.assertEqual(db_iface.uid, uid)
        self.assertEqual(db_iface.interface,iface)
        self.assertEqual(db_iface.perm, timeuuid.min_uuid_from_time(ts).hex)

