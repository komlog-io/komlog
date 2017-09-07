import unittest
import uuid
import decimal
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import snapshot as cassapisnapshot
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.gestaccount.snapshot import api as snapshotapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.api import kin as graphkin

class GestaccountCommonDeleteTest(unittest.TestCase):
    ''' komlog.gestaccount.common.delete tests '''

    def setUp(self):
        username = 'test_komlog.gestaccount.common.common_user'
        password = 'test_password'
        email = username+'@komlog.org'
        try:
            uid=userapi.get_uid(username=username)
        except Exception:
            user=userapi.create_user(username=username, password=password, email=email)
            uid=user['uid']
        finally:
            self.user=userapi.get_user_config(uid=uid)

    def test_delete_user_failure_invalid_uid(self):
        ''' delete_user should fail if username is invalid '''
        uids=[None, '123123',234234,2342.2342,{'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid1(),timeuuid.uuid1(), uuid.uuid4().hex]
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_user(uid=uid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DU_IU)

    def test_delete_user_failure_non_existent_username(self):
        ''' delete_user should fail if username does not exist '''
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            deleteapi.delete_user(uid=uid)
        self.assertEqual(cm.exception.error, Errors.E_GCD_DU_UNF)

    def test_delete_user_success(self):
        ''' delete_user should succeed if username exists and delete its info'''
        username='test_delete_user_success'
        password='test_password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        self.assertTrue(userapi.confirm_user(email=email, code=user['code']))
        self.assertIsNotNone(cassapiuser.get_user(username=username))
        self.assertIsNotNone(cassapiuser.get_signup_info(username=username))
        self.assertTrue(deleteapi.delete_user(uid=user['uid']))
        self.assertIsNone(cassapiuser.get_user(username=username))
        self.assertIsNone(cassapiuser.get_signup_info(username=username))

    def test_delete_agent_failure_invalid_aid(self):
        ''' delete_agent should fail if aid is invalid '''
        aids=[None, '123123',234234,2342.2342,{'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid1(),timeuuid.uuid1(), uuid.uuid4().hex]
        for aid in aids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_agent(aid=aid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DA_IA)

    def test_delete_agent_non_existent_aid(self):
        ''' delete_agent should return False if delete where requested on the DB event if aid does not exist '''
        aid=uuid.uuid4()
        self.assertFalse(deleteapi.delete_agent(aid=aid))

    def test_delete_agent_success(self):
        ''' delete_agent should succeed and delete agent from db '''
        agentname='test_delete_agent_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertIsNotNone(cassapiagent.get_agent(aid=agent['aid']))
        self.assertTrue(deleteapi.delete_agent(aid=agent['aid']))
        self.assertIsNone(cassapiagent.get_agent(aid=agent['aid']))

    def test_delete_datasource_failure_invalid_did(self):
        ''' delete_datasource should fail if did is invalid '''
        dids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datasource(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDS_ID)

    def test_delete_datasource_non_existent_did(self):
        ''' delete_datasource should return True if deletes where executed successfully even if did does not exist '''
        did=uuid.uuid4()
        self.assertTrue(deleteapi.delete_datasource(did=did))

    def test_delete_datasource_success(self):
        ''' delete_datasource should succeed and delete datasource completely from db, even its associated widgets and datapoints, and these from its dashboards. it also has to register pending hooks if it had associated hooks '''
        uid=self.user['uid']
        agentname='test_delete_datasource_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        aid=agent['aid']
        datasourcename='test_delete_datasource_success'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        sid=uuid.uuid4()
        self.assertTrue(datasourceapi.hook_to_datasource(did=datasource['did'],sid=sid))
        date=timeuuid.uuid1()
        content='delete_datasource_success content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        widget=widgetapi.new_widget_datasource(uid=uid, did=datasource['did'])
        data=datasourceapi.get_datasource_data(did=datasource['did'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['date'], date)
        self.assertEqual(data[0]['content'], content)
        datasource2=datasourceapi.get_datasource_config(did=datasource['did'])
        self.assertEqual(datasource['did'],datasource2['did'])
        self.assertEqual(datasource['aid'],datasource2['aid'])
        self.assertEqual(datasource['uid'],datasource2['uid'])
        self.assertEqual(datasource['datasourcename'],datasource2['datasourcename'])
        widget2=widgetapi.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['wid'],widget2['wid'])
        self.assertEqual(widget['did'],widget2['did'])
        self.assertEqual(widget['type'],widget2['type'])
        hooks=datasourceapi.get_datasource_hooks(did=datasource['did'])
        self.assertEqual(hooks,[sid])
        self.assertTrue(datasourceapi.update_datasource_supplies(did=datasource['did'], supplies=['a','b']))
        ds_sups = cassapidatasource.get_last_datasource_supplies_count(did=datasource['did'])
        self.assertEqual(len(ds_sups),1)
        self.assertTrue(deleteapi.delete_datasource(did=datasource['did']))
        self.assertIsNone(cassapidatasource.get_datasource(did=datasource['did']))
        self.assertIsNone(cassapidatasource.get_datasource_stats(did=datasource['did']))
        self.assertEqual(cassapidatasource.get_datasource_data(did=datasource['did'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_maps(did=datasource['did'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_text_summaries(did=datasource['did'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=datasource['uid'],uri=datasource['datasourcename']),[sid])
        self.assertEqual(cassapidatasource.get_last_datasource_supplies_count(did=datasource['did']),[])

    def test_delete_datapoint_failure_bad_parameters(self):
        ''' delete_datapoint should fail if we pass incorrect parameters '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datapoint(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDP_IP)

    def test_delete_datapoint_non_existent_datapoint(self):
        ''' delete_datapoint should return True if deletes where launched against DB, even if datapoint does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_datapoint(pid=pid))

    def test_delete_datapoint_success_maps(self):
        ''' delete_datapoint should succeed, and delete it from the maps where appears '''
        uid=self.user['uid']
        agentname='test_delete_datapoint_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename='test_delete_datapoint_success'
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='test_delete_datapoint_success_datapoint'
        datapoint=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        datapointapi.mark_negative_variable(pid=datapoint['pid'], date=date, position=11, length=2)
        self.assertTrue(datapointapi.store_datasource_values(did=did, date=date))
        data=datapointapi.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        datapointapi.generate_datasource_text_summary(did=datasource['did'], date=date)
        datapointapi.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid'])
        dsdata=datasourceapi.get_mapped_datasource_data(did=did, fromdate=date, todate=date)
        self.assertTrue({'pid':datapoint['pid'],'position':8} in dsdata[0]['datapoints'])
        self.assertIsNotNone(cassapidatapoint.get_datapoint(pid=datapoint['pid']))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_stats(pid=datapoint['pid']))
        self.assertNotEqual(cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid']),[])
        self.assertNotEqual(cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid']),[])
        self.assertNotEqual(cassapidatapoint.get_datapoint_data(pid=datapoint['pid'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertNotEqual(cassapidatasource.get_datasource_novelty_detectors_for_datapoint(pid=datapoint['pid'], did=datapoint['did']),[])
        self.assertTrue(deleteapi.delete_datapoint(pid=datapoint['pid']))
        dsdata=datasourceapi.get_mapped_datasource_data(did=did, fromdate=date, todate=date)
        self.assertFalse({'pid':datapoint['pid'],'position':8} in dsdata[0]['datapoints'])
        self.assertIsNone(cassapidatapoint.get_datapoint(pid=datapoint['pid']))
        self.assertIsNone(cassapidatapoint.get_datapoint_stats(pid=datapoint['pid']))
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_data(pid=datapoint['pid'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_novelty_detectors_for_datapoint(pid=datapoint['pid'], did=datapoint['did']),[])

    def test_delete_datapoint_success_widgets(self):
        ''' delete_datapoint should succeed, and delete it from the widgets where it appears '''
        uid=self.user['uid']
        agentname='test_delete_datapoint_success_widgets'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename='test_delete_datapoint_success_widgets'
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='test_store_datasource_values_success'
        datapoint=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        widget=widgetapi.new_widget_datapoint(uid=uid, pid=datapoint['pid'])
        self.assertTrue(datapointapi.store_datasource_values(did=did, date=date))
        data=datapointapi.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertTrue(deleteapi.delete_datapoint(pid=datapoint['pid']))
        self.assertIsNone(cassapidatapoint.get_datapoint(pid=datapoint['pid']))
        self.assertIsNone(cassapidatapoint.get_datapoint_stats(pid=datapoint['pid']))
        self.assertIsNone(cassapiwidget.get_widget(wid=widget['wid']))
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_data(pid=datapoint['pid'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_novelty_detectors_for_datapoint(pid=datapoint['pid'], did=datapoint['did']),[])

    def test_delete_datapoint_success_register_pending_hooks(self):
        ''' delete_datapoint should succeed, and register any hook is had as pending hooks '''
        uid=self.user['uid']
        agentname='test_delete_datapoint_success_register_pending_hooks'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename='test_delete_datapoint_success_register_pending_hooks'
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='datapoint'
        datapoint=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        sid=uuid.uuid4()
        self.assertTrue(datapointapi.hook_to_datapoint(pid=datapoint['pid'],sid=sid))
        widget=widgetapi.new_widget_datapoint(uid=uid, pid=datapoint['pid'])
        self.assertTrue(datapointapi.store_datasource_values(did=did, date=date))
        data=datapointapi.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        hooks=datapointapi.get_datapoint_hooks(pid=datapoint['pid'])
        self.assertEqual(hooks,[sid])
        self.assertTrue(deleteapi.delete_datapoint(pid=datapoint['pid']))
        self.assertIsNone(cassapidatapoint.get_datapoint(pid=datapoint['pid']))
        self.assertIsNone(cassapidatapoint.get_datapoint_stats(pid=datapoint['pid']))
        self.assertIsNone(cassapiwidget.get_widget(wid=widget['wid']))
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_data(pid=datapoint['pid'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_novelty_detectors_for_datapoint(pid=datapoint['pid'], did=datapoint['did']),[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=datapoint['uid'], uri=datapoint['datapointname']),[sid])

    def test_delete_widget_failure_bad_parameters(self):
        ''' delete_widget should fail if we pass incorrect parameters '''
        wids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for wid in wids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_widget(wid=wid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DW_IW)

    def test_delete_widget_non_existent_widget(self):
        ''' delete_widget should return True if deletes where executed over DB,even if widget is not in system '''
        wid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_widget(wid=wid))

    def test_delete_widget_ds_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        username='test_delete_widget_ds_success_user'
        agentname='test_delete_widget_ds_success_agent'
        datasourcename='test_delete_widget_ds_success_datasource'
        datapointname='test_delete_widget_ds_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        widget=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did'])
        self.assertIsNotNone(cassapiwidget.get_widget(wid=widget['wid']))
        self.assertTrue(deleteapi.delete_widget(wid=widget['wid']))
        self.assertIsNone(cassapiwidget.get_widget(wid=widget['wid']))

    def test_delete_widget_dp_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        username='test_delete_widget_dp_success_user'
        agentname='test_delete_widget_dp_success_agent'
        datasourcename='test_delete_widget_dp_success_datasource'
        datapointname='test_delete_widget_dp_success_datapoint'
        datapointname2='test_delete_widget_dp_success_datapoint2'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        widgetds=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=widgetapi.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        datapoint2=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname2)
        widget2=widgetapi.new_widget_datapoint(uid=user['uid'], pid=datapoint2['pid']) 
        self.assertIsNotNone(cassapiwidget.get_widget(wid=widget['wid']))
        self.assertNotEqual(graphkin.get_kin_widgets(ido=widgetds['wid']),[])
        self.assertNotEqual(graphkin.get_kin_widgets(ido=widget['wid']),[])
        self.assertTrue(deleteapi.delete_widget(wid=widget['wid']))
        self.assertIsNone(cassapiwidget.get_widget(wid=widget['wid']))
        self.assertEqual(graphkin.get_kin_widgets(ido=widget['wid']),[])
        self.assertNotEqual(graphkin.get_kin_widgets(ido=widgetds['wid']),[])

    def test_delete_dashboard_failure_invalid_bid(self):
        ''' delete_dashboard should fail if bid is invalid '''
        bids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        for bid in bids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_dashboard(bid=bid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDB_IB)

    def test_delete_dashboard_non_existent_bid(self):
        ''' delete_dashboard should return True if deletes where launched over DB, even if bid does not exist '''
        bid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_dashboard(bid=bid))

    def test_delete_dashboard_success(self):
        ''' delete_dashboard should succeed if bid exist '''
        dashboardname='test_delete_dashboard_success'
        uid=self.user['uid']
        result=dashboardapi.create_dashboard(uid=uid, dashboardname=dashboardname)
        bid=result['bid']
        self.assertIsNotNone(cassapidashboard.get_dashboard(bid=bid))
        self.assertTrue(deleteapi.delete_dashboard(bid=bid))
        self.assertIsNone(cassapidashboard.get_dashboard(bid=bid))

    def test_delete_circle_failure_invalid_cid(self):
        ''' delete_circle should fail if cid is invalid '''
        cids=[None,23234,23423.23423,'adfasdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4().hex]
        for cid in cids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_circle(cid=cid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DC_IC)

    def test_delete_circle_non_existent_circle(self):
        ''' delete_circle should return True if deletes where launched over DB, even if cid does not exist '''
        cid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_circle(cid=cid))

    def test_delete_circle_success(self):
        ''' delete_circle should succeed and delete the circle '''
        uid=self.user['uid']
        circlename='test_delete_circle_success_circlename'
        circle=circleapi.new_users_circle(uid=uid, circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],uid)
        self.assertEqual(db_circle['members'],[])
        self.assertTrue(deleteapi.delete_circle(cid=cid))
        self.assertIsNone(cassapicircle.get_circle(cid=cid))

    def test_delete_snapshot_failure_invalid_nid(self):
        ''' delete_snapshot should fail if nid is invalid '''
        nids=[None,23234,23423.23423,'adfasdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4().hex]
        for nid in nids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_snapshot(nid=nid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DN_IN)

    def test_delete_snapshot_non_existent_snapshot(self):
        ''' delete_snapshot should return True if deletes where launched over DB, even if nid did not exist '''
        nid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_snapshot(nid=nid))

    def test_delete_snapshot_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        uid=self.user['uid']
        datasourcename='test_delete_snapshot_success_datasource'
        agentname='test_delete_snapshot_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'], datasourcename=datasourcename)
        widgetds=widgetapi.new_widget_datasource(uid=uid, did=datasource['did']) 
        snapshot=snapshotapi.new_snapshot(uid=uid, wid=widgetds['wid'], interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1(seconds=2))
        self.assertIsNotNone(cassapisnapshot.get_snapshot(nid=snapshot['nid']))
        self.assertTrue(deleteapi.delete_snapshot(nid=snapshot['nid']))
        self.assertIsNone(cassapisnapshot.get_snapshot(nid=snapshot['nid']))

    def test_dissociate_datapoint_from_datasource_failure_invalid_pid(self):
        ''' dissociate_datapoint_from_datasource should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.dissociate_datapoint_from_datasource(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDPFDS_IP)

    def test_dissociate_datapoint_from_datasource_failure_non_existent_datapoint(self):
        ''' dissociate_datapoint_from_datasource should fail if pid does not exist '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            deleteapi.dissociate_datapoint_from_datasource(pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_GCD_DDPFDS_DPNF)

    def test_dissociate_datapoint_from_datasource_success_datapoint_was_not_associated_already(self):
        ''' dissociate_datapoint_from_datasource should succeed if we try to dissociate
            a datapoint that is not associated '''
        username='test_dissociate_datapoint_from_datasource_success_datapoint_was_not_associated_already'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        result=deleteapi.dissociate_datapoint_from_datasource(pid=datapoint['pid'])
        self.assertIsNone(result['did'])
        datapoint2=datapointapi.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(datapoint2['uid'],uid)
        self.assertEqual(datapoint2['did'],None)
        self.assertEqual(datapoint2['datapointname'],datapoint_uri)
        self.assertTrue(datapoint2['pid'],datapoint['pid'])
        self.assertTrue(datapoint2['color'],datapoint['color'])

    def test_dissociate_datapoint_from_datasource_success_datapoint_was_associated(self):
        ''' dissociate_datapoint_from_datasource should succeed if we try to dissociate
            a datapoint that is associated to a datasource '''
        username='test_dissociate_datapoint_from_datasource_success_datapoint_was_associated'
        agentname=username
        datasourcename='datasource'
        datapointname='datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        widgetds=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=widgetapi.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        datapoint_config=datapointapi.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(datapoint_config['did'], datasource['did'])
        self.assertIsNotNone(cassapiwidget.get_widget(wid=widget['wid']))
        self.assertNotEqual(graphkin.get_kin_widgets(ido=widgetds['wid']),[])
        self.assertNotEqual(graphkin.get_kin_widgets(ido=widget['wid']),[])
        result=deleteapi.dissociate_datapoint_from_datasource(pid=datapoint_config['pid'])
        self.assertEqual(result['did'],datasource['did'])
        datapoint_config=datapointapi.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(datapoint_config['did'], None)
        self.assertEqual(graphkin.get_kin_widgets(ido=widget['wid']),[])
        self.assertEqual(graphkin.get_kin_widgets(ido=widgetds['wid']),[])

    def test_delete_datapoint_data_at_failure_invalid_pid(self):
        ''' delete_datapoint_data_at should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datapoint_data_at(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDPDA_IPID)

    def test_delete_datapoint_data_at_failure_invalid_date(self):
        ''' delete_datapoint_data_at should fail if date is invalid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datapoint_data_at(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDPDA_IDATE)

    def test_delete_datapoint_data_at_success_no_data_existed_previously(self):
        ''' delete_datapoint_data_at should succeed even if data did not exist previously '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(deleteapi.delete_datapoint_data_at(pid,date))

    def test_delete_datapoint_data_at_success_data_existed_previously(self):
        ''' delete_datapoint_data_at should succeed even if data did not exist previously '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        value=decimal.Decimal(5)
        self.assertTrue(cassapidatapoint.insert_datapoint_data(pid, date, value))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_data_at(pid, date))
        self.assertTrue(deleteapi.delete_datapoint_data_at(pid,date))
        self.assertIsNone(cassapidatapoint.get_datapoint_data_at(pid, date))

    def test_delete_datasource_data_at_failure_invalid_did(self):
        ''' delete_datasource_data_at should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datasource_data_at(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDSDA_IDID)

    def test_delete_datasource_data_at_failure_invalid_date(self):
        ''' delete_datasource_data_at should fail if date is invalid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datasource_data_at(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GCD_DDSDA_IDATE)

    def test_delete_datasource_data_at_success_no_data_existed_previously(self):
        ''' delete_datasource_data_at should succeed even if data did not exist previously '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(deleteapi.delete_datasource_data_at(did,date))

    def test_delete_datasource_data_at_success_data_existed_previously(self):
        ''' delete_datasource_data_at should succeed even if data did not exist previously '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='content'
        dsdata=ormdatasource.DatasourceData(did,date,content)
        self.assertTrue(cassapidatasource.insert_datasource_data(dsdata))
        self.assertIsNotNone(cassapidatasource.get_datasource_data_at(did, date))
        self.assertTrue(deleteapi.delete_datasource_data_at(did,date))
        self.assertIsNone(cassapidatasource.get_datasource_data_at(did, date))

