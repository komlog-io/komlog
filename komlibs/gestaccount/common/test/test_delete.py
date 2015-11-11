import unittest
import uuid
from komcass.api import user as cassapiuser
from komcass.api import agent as cassapiagent
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.api import snapshot as cassapisnapshot
from komcass.api import circle as cassapicircle
from komlibs.general import colors
from komlibs.general.time import timeuuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.dashboard import api as dashboardapi
from komlibs.gestaccount.snapshot import api as snapshotapi
from komlibs.gestaccount.circle import api as circleapi
from komlibs.gestaccount.common import delete as deleteapi
from komlibs.gestaccount import exceptions, errors
from komlibs.graph.api import uri as graphuri
from komlibs.graph.api import kin as graphkin

class GestaccountCommonDeleteTest(unittest.TestCase):
    ''' komlog.gestaccount.common.delete tests '''

    def setUp(self):
        username = 'test_komlog.gestaccount.common.common_user'
        password = 'test_password'
        email = username+'@komlog.org'
        try:
            self.user=userapi.get_user_config(username=username)
        except Exception:
            user=userapi.create_user(username=username, password=password, email=email)
            self.assertTrue(userapi.confirm_user(email=email, code=user['signup_code']))
            self.user=userapi.get_user_config(username=username)
            self.assertIsNotNone(self.user)

    def test_delete_user_failure_invalid_username(self):
        ''' delete_user should fail if username is invalid '''
        usernames=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4(), uuid.uuid1()]
        for username in usernames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_user(username=username)
            self.assertEqual(cm.exception.error, errors.E_GCD_DU_IU)

    def test_delete_user_failure_non_existent_username(self):
        ''' delete_user should fail if username does not exist '''
        username='test_delete_user_failure_non_existent_username'
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            deleteapi.delete_user(username=username)
        self.assertEqual(cm.exception.error, errors.E_GCD_DU_UNF)

    def test_delete_user_success(self):
        ''' delete_user should succeed if username exists and delete its info'''
        username='test_delete_user_success'
        password='test_password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        self.assertTrue(userapi.confirm_user(email=email, code=user['signup_code']))
        self.assertIsNotNone(cassapiuser.get_user(username=username))
        self.assertIsNotNone(cassapiuser.get_signup_info(username=username))
        self.assertTrue(deleteapi.delete_user(username=username))
        self.assertIsNone(cassapiuser.get_user(username=username))
        self.assertIsNone(cassapiuser.get_signup_info(username=username))

    def test_delete_agent_failure_invalid_aid(self):
        ''' delete_agent should fail if aid is invalid '''
        aids=[None, '123123',234234,2342.2342,{'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid1(),timeuuid.uuid1(), uuid.uuid4().hex]
        for aid in aids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_agent(aid=aid)
            self.assertEqual(cm.exception.error, errors.E_GCD_DA_IA)

    def test_delete_agent_non_existent_aid(self):
        ''' delete_agent should return True if delete where requested on the DB event if aid does not exist '''
        aid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_agent(aid=aid))

    def test_delete_agent_success(self):
        ''' delete_agent should succeed and delete agent from db '''
        agentname='test_delete_agent_success'
        pubkey='pubkeydeleteagentsuccess'
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
            self.assertEqual(cm.exception.error, errors.E_GCD_DDS_ID)

    def test_delete_datasource_non_existent_did(self):
        ''' delete_datasource should return True if deletes where executed successfully even if did does not exist '''
        did=uuid.uuid4()
        self.assertTrue(deleteapi.delete_datasource(did=did))

    def test_delete_datasource_success(self):
        ''' delete_datasource should succeed and delete datasource completely from db, even its associated widgets and datapoints, and these from its dashboards '''
        uid=self.user['uid']
        agentname='test_delete_datasource_success'
        pubkey='pubkeydeletedatasourcesuccess'
        version='Test Version'
        agent=agentapi.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        aid=agent['aid']
        datasourcename='test_delete_datasource_success'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        date=timeuuid.uuid1()
        content='delete_datasource_success content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        widget=widgetapi.new_widget_datasource(uid=uid, did=datasource['did'])
        data=datasourceapi.get_datasource_data(did=datasource['did'], date=date)
        self.assertIsNotNone(data)
        self.assertEqual(data['did'], datasource['did'])
        self.assertEqual(data['date'], date)
        self.assertEqual(data['content'], content)
        datasource2=datasourceapi.get_datasource_config(did=datasource['did'])
        self.assertEqual(datasource['did'],datasource2['did'])
        self.assertEqual(datasource['aid'],datasource2['aid'])
        self.assertEqual(datasource['uid'],datasource2['uid'])
        self.assertEqual(datasource['datasourcename'],datasource2['datasourcename'])
        widget2=widgetapi.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['wid'],widget2['wid'])
        self.assertEqual(widget['did'],widget2['did'])
        self.assertEqual(widget['type'],widget2['type'])
        self.assertTrue(deleteapi.delete_datasource(did=datasource['did']))
        self.assertIsNone(cassapidatasource.get_datasource(did=datasource['did']))
        self.assertIsNone(cassapidatasource.get_datasource_stats(did=datasource['did']))
        self.assertEqual(cassapidatasource.get_datasource_data(did=datasource['did'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_maps(did=datasource['did'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertEqual(cassapidatasource.get_datasource_text_summaries(did=datasource['did'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])

    def test_delete_datapoint_failure_bad_parameters(self):
        ''' delete_datapoint should fail if we pass incorrect parameters '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_datapoint(pid=pid)
            self.assertEqual(cm.exception.error, errors.E_GCD_DDP_IP)

    def test_delete_datapoint_non_existent_datapoint(self):
        ''' delete_datapoint should return True if deletes where launched against DB, even if datapoint does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_datapoint(pid=pid))

    def test_delete_datapoint_success_maps(self):
        ''' delete_datapoint should succeed, and delete it from the maps where appears '''
        uid=self.user['uid']
        agentname='test_delete_datapoint_success'
        pubkey='pubkeydeletedatapointsuccess'
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
        datasourceapi.generate_datasource_text_summary(did=datasource['did'], date=date)
        datasourceapi.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid'])
        dsdata=datasourceapi.get_datasource_data(did=did, date=date)
        self.assertTrue({'pid':datapoint['pid'],'position':8} in dsdata['datapoints'])
        self.assertIsNotNone(cassapidatapoint.get_datapoint(pid=datapoint['pid']))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_stats(pid=datapoint['pid']))
        self.assertNotEqual(cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid']),[])
        self.assertNotEqual(cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid']),[])
        self.assertNotEqual(cassapidatapoint.get_datapoint_data(pid=datapoint['pid'],fromdate=timeuuid.uuid1(seconds=1),todate=timeuuid.uuid1()),[])
        self.assertNotEqual(cassapidatasource.get_datasource_novelty_detectors_for_datapoint(pid=datapoint['pid'], did=datapoint['did']),[])
        self.assertTrue(deleteapi.delete_datapoint(pid=datapoint['pid']))
        dsdata=datasourceapi.get_datasource_data(did=did, date=date)
        self.assertFalse({'pid':datapoint['pid'],'position':8} in dsdata['datapoints'])
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
        pubkey='pubkeydeletedatapointsuccesswidgets'
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

    def test_delete_widget_failure_bad_parameters(self):
        ''' delete_widget should fail if we pass incorrect parameters '''
        wids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for wid in wids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                deleteapi.delete_widget(wid=wid)
            self.assertEqual(cm.exception.error, errors.E_GCD_DW_IW)

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
        pubkey='testdeletewidgetdssuccesspubkey'
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
        pubkey='testdeletewidgetdpsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        widgetds=widgetapi.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        color=colors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        datapoint2=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname2, color=color)
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
            self.assertEqual(cm.exception.error, errors.E_GCD_DDB_IB)

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
            self.assertEqual(cm.exception.error, errors.E_GCD_DC_IC)

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
            self.assertEqual(cm.exception.error, errors.E_GCD_DN_IN)

    def test_delete_snapshot_non_existent_snapshot(self):
        ''' delete_snapshot should return True if deletes where launched over DB, even if nid did not exist '''
        nid=uuid.uuid4()
        self.assertTrue(deleteapi.delete_snapshot(nid=nid))

    def test_delete_snapshot_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        uid=self.user['uid']
        datasourcename='test_delete_snapshot_success_datasource'
        agentname='test_delete_snapshot_success_agent'
        pubkey='testdeletesnapshotsuccesspubkey'
        version='Test Version'
        circlename='test_delete_snapshot_success'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'], datasourcename=datasourcename)
        circle=circleapi.new_users_circle(uid=uid, circlename=circlename)
        widgetds=widgetapi.new_widget_datasource(uid=uid, did=datasource['did']) 
        snapshot=snapshotapi.new_snapshot(uid=uid, wid=widgetds['wid'], interval_init=timeuuid.uuid1(seconds=1), interval_end=timeuuid.uuid1(seconds=2), shared_with_cids=[circle['cid']])
        self.assertIsNotNone(cassapisnapshot.get_snapshot(nid=snapshot['nid']))
        self.assertTrue(deleteapi.delete_snapshot(nid=snapshot['nid']))
        self.assertIsNone(cassapisnapshot.get_snapshot(nid=snapshot['nid']))

