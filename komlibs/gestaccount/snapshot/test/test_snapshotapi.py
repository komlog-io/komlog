import unittest
import uuid
from komcass.api import datapoint as cassapidatapoint
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi 
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.snapshot import api as snapshotapi
from komlibs.gestaccount.widget import types
from komlibs.gestaccount import exceptions
from komcass.model.orm import widget as ormwidget
from komcass.model.orm import snapshot as ormsnapshot
from komlibs.general import colors as libcolors
from komlibs.general.time import timeuuid
from decimal import Decimal

class GestaccountSnapshotApiTest(unittest.TestCase):
    ''' komlog.gestaccount.snapshot.api tests '''

    def test_new_snapshot_failure_invalid_username(self):
        ''' new_snapshot should fail if username is invalid '''
        usernames=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), 'Usernames','user name']
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.new_snapshot, username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_failure_invalid_wid(self):
        ''' new_snapshot should fail if wid is invalid '''
        wids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        username='test_new_snapshot_username'
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.new_snapshot, username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_failure_invalid_interval_init(self):
        ''' new_snapshot should fail if interval_init is invalid '''
        interval_inits=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1().hex, 'Usernames','user name']
        username='test_new_snapshot_username'
        wid=uuid.uuid4()
        interval_end=timeuuid.uuid1()
        for interval_init in interval_inits:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.new_snapshot, username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_failure_invalid_interval_end(self):
        ''' new_snapshot should fail if interval_end is invalid '''
        interval_ends=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1().hex, 'Usernames','user name']
        username='test_new_snapshot_username'
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        for interval_end in interval_ends:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.new_snapshot, username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_failure_non_existent_widget(self):
        ''' new_widget should fail if widget does not exist '''
        username='test_new_snapshot_failure_non_existent_widget'
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        self.assertRaises(exceptions.WidgetNotFoundException, snapshotapi.new_snapshot, username=username, wid=wid, interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_datasource_success(self):
        ''' new_snapshot_datasource should succeed if widget exists and user too '''
        username='test_new_snapshot_datasource_success_user'
        agentname='test_new_snapshot_datasource_success_agent'
        datasourcename='test_new_snapshot_datasource_success_datasource'
        datapointname='test_new_snapshot_datasource_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testnewsnapshotdssuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        uid=user['uid']
        did=datasource['did']
        widget=widgetapi.new_widget_datasource(username=username, did=did)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], did)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DATASOURCE)
        self.assertEqual(widget['widgetname'],datasourcename)
        self.assertEqual(len(widget.keys()),5)
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],uid)
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))

    def test_new_snapshot_datapoint_success(self):
        ''' new_snapshot_datapoint should succeed if widget exists and user too '''
        username='test_new_snapshot_datapoint_success_user'
        agentname='test_new_snapshot_datapoint_success_agent'
        datasourcename='test_new_snapshot_datapoint_success_datasource'
        datapointname='test_new_snapshot_datapoint_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testnewsnapshotdpsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_datapoint(username=username, pid=datapoint['pid']) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], datapoint['pid'])
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.DATAPOINT)
        self.assertEqual(widget['widgetname'],datapointname)
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))

    def test_new_snapshot_histogram_failure_empty_widget(self):
        ''' new_snapshot_histogram should fail if widget exists but has no datapoints '''
        username='test_new_snapshot_histogram_failure_user'
        agentname='test_new_snapshot_histogram_failure_agent'
        datasourcename='test_new_snapshot_histogram_failure_datasource'
        datapointname='test_new_snapshot_histogram_failure_datapoint'
        widgetname='test_new_snapshot_histogram_failure_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_histogram(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertEqual(widget['widgetname'],widgetname)
        interval_init=timeuuid.uuid1(seconds=1)
        interval_end=timeuuid.uuid1(seconds=3)
        self.assertRaises(exceptions.WidgetUnsupportedOperationException, snapshotapi.new_snapshot, username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_histogram_success(self):
        ''' new_snapshot_histogram should succeed if widget exists and user too '''
        username='test_new_snapshot_histogram_success_user'
        agentname='test_new_snapshot_histogram_success_agent'
        datasourcename='test_new_snapshot_histogram_success_datasource'
        datapointname='test_new_snapshot_histogram_success_datapoint'
        widgetname='test_new_snapshot_histogram_success_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_histogram(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))

    def test_new_snapshot_linegraph_failure_empty_widget(self):
        ''' new_snapshot_linegraph should fail if widget exists but has not datapoints '''
        username='test_new_snapshot_linegraph_failure_user'
        agentname='test_new_snapshot_linegraph_failure_agent'
        datasourcename='test_new_snapshot_linegraph_failure_datasource'
        datapointname='test_new_snapshot_linegraph_failure_datapoint'
        widgetname='test_new_snapshot_linegraph_failure_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_linegraph(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertEqual(widget['widgetname'],widgetname)
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        self.assertRaises(exceptions.WidgetUnsupportedOperationException, snapshotapi.new_snapshot, username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_linegraph_success(self):
        ''' new_snapshot_linegraph should succeed if widget exists and user too '''
        username='test_new_snapshot_linegraph_success_user'
        agentname='test_new_snapshot_linegraph_success_agent'
        datasourcename='test_new_snapshot_linegraph_success_datasource'
        datapointname='test_new_snapshot_linegraph_success_datapoint'
        widgetname='test_new_snapshot_linegraph_success_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_linegraph(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))

    def test_new_snapshot_table_failure_empty_widget(self):
        ''' new_snapshot_table should fail if widget exists but has no datapoints '''
        username='test_new_snapshot_table_failure_user'
        agentname='test_new_snapshot_table_failure_agent'
        datasourcename='test_new_snapshot_table_failure_datasource'
        datapointname='test_new_snapshot_table_failure_datapoint'
        widgetname='test_new_snapshot_table_failure_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_table(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertEqual(widget['widgetname'],widgetname)
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        self.assertRaises(exceptions.WidgetUnsupportedOperationException, snapshotapi.new_snapshot, username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)

    def test_new_snapshot_table_success(self):
        ''' new_snapshot_linegraph should succeed if widget exists and user too '''
        username='test_new_snapshot_table_success_user'
        agentname='test_new_snapshot_table_success_agent'
        datasourcename='test_new_snapshot_table_success_datasource'
        datapointname='test_new_snapshot_table_success_datapoint'
        widgetname='test_new_snapshot_table_success_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_table(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))

    def test_get_snapshot_config_failure_invalid_nid(self):
        ''' get_snapshot_config should fail if nid is not valid '''
        nids=[None, 2342, 23422.2342, {'a':'dict'}, ['a','list'], ('a','tuple'), {'set'},'username',uuid.uuid4().hex, uuid.uuid1(), timeuuid.uuid1()]
        for nid in nids:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.get_snapshot_config, nid=nid)

    def test_get_snapshot_config_failure_non_existent_nid(self):
        ''' get_snapshot_config should fail if nid does not exist '''
        nid=uuid.uuid4()
        self.assertRaises(exceptions.SnapshotNotFoundException, snapshotapi.get_snapshot_config, nid=nid)

    def test_get_snapshot_config_success_snapshot_datasource(self):
        ''' get_snapshot_config should succeed and return snapshot datasource config '''
        username='test_get_snapshot_config_success_snapshot_datasource_user'
        agentname='test_get_snapshot_config_success_snapshot_datasource_agent'
        datasourcename='test_get_snapshot_config_success_snapshot_datasource_datasource'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotconfigsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        uid=user['uid']
        did=datasource['did']
        widget=widgetapi.new_widget_datasource(username=username, did=did)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], did)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DATASOURCE)
        self.assertEqual(widget['widgetname'],datasourcename)
        self.assertEqual(len(widget.keys()),5)
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(interval_init)+1)
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],uid)
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        self.assertEqual(snapshot['nid'],snapshot_config['nid'])
        self.assertEqual(snapshot['wid'],snapshot_config['wid'])
        self.assertEqual(snapshot['uid'],snapshot_config['uid'])
        self.assertEqual(snapshot['interval_init'],snapshot_config['interval_init'])
        self.assertEqual(snapshot['interval_end'],snapshot_config['interval_end'])
        self.assertEqual(datasource['did'],snapshot_config['did'])
        self.assertEqual(datasourcename,snapshot_config['widgetname'])
        self.assertEqual(types.DATASOURCE,snapshot_config['type'])

    def test_get_snapshot_config_success_snapshot_datapoint(self):
        ''' get_snapshot_config should succeed and return snapshot datapoint config '''
        username='test_get_snapshot_config_success_snapshot_datapoint_user'
        agentname='test_get_snapshot_config_success_snapshot_datapoint_agent'
        datasourcename='test_get_snapshot_config_success_snapshot_datapoint_datasource'
        datapointname='test_get_snapshot_config_success_snapshot_datapoint_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotconfigdpsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_datapoint(username=username, pid=datapoint['pid']) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], datapoint['pid'])
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.DATAPOINT)
        self.assertEqual(widget['widgetname'],datapointname)
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        self.assertEqual(snapshot['nid'],snapshot_config['nid'])
        self.assertEqual(snapshot['wid'],snapshot_config['wid'])
        self.assertEqual(snapshot['uid'],snapshot_config['uid'])
        self.assertEqual(snapshot['interval_init'],snapshot_config['interval_init'])
        self.assertEqual(snapshot['interval_end'],snapshot_config['interval_end'])
        self.assertEqual(datapoint['pid'],snapshot_config['pid'])
        self.assertEqual(datapointname,snapshot_config['widgetname'])
        self.assertEqual(types.DATAPOINT,snapshot_config['type'])

    def test_get_snapshot_config_success_snapshot_histogram(self):
        ''' get_snapshot_config should succeed and return snapshot histogram config '''
        username='test_get_snapshot_config_success_snapshot_histogram_user'
        agentname='test_get_snapshot_config_success_snapshot_histogram_agent'
        datasourcename='test_get_snapshot_config_success_snapshot_histogram_datasource'
        datapointname='test_get_snapshot_config_success_snapshot_histogram_datapoint'
        widgetname='test_get_snapshot_config_success_snapshot_histogram_widget'
        email=username+'@komlog.org'
        pubkey='testpubkey'
        password='password'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_histogram(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        self.assertEqual(snapshot['nid'],snapshot_config['nid'])
        self.assertEqual(snapshot['wid'],snapshot_config['wid'])
        self.assertEqual(snapshot['uid'],snapshot_config['uid'])
        self.assertEqual(snapshot['interval_init'],snapshot_config['interval_init'])
        self.assertEqual(snapshot['interval_end'],snapshot_config['interval_end'])
        self.assertEqual({datapoint['pid']},snapshot_config['datapoints'])
        self.assertEqual({datapoint['pid']:color},snapshot_config['colors'])
        self.assertEqual(widgetname,snapshot_config['widgetname'])
        self.assertEqual(types.HISTOGRAM,snapshot_config['type'])

    def test_get_snapshot_config_success_snapshot_linegraph(self):
        ''' get_snapshot_config should succeed and return snapshot linegraph config '''
        username='test_get_snapshot_config_success_snapshot_linegraph_user'
        agentname='test_get_snapshot_config_success_snapshot_linegraph_agent'
        datasourcename='test_get_snapshot_config_success_snapshot_linegraph_datasource'
        datapointname='test_get_snapshot_config_success_snapshot_linegraph_datapoint'
        widgetname='test_get_snapshot_config_success_snapshot_linegraph_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_linegraph(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        self.assertEqual(snapshot['nid'],snapshot_config['nid'])
        self.assertEqual(snapshot['wid'],snapshot_config['wid'])
        self.assertEqual(snapshot['uid'],snapshot_config['uid'])
        self.assertEqual(snapshot['interval_init'],snapshot_config['interval_init'])
        self.assertEqual(snapshot['interval_end'],snapshot_config['interval_end'])
        self.assertEqual({datapoint['pid']},snapshot_config['datapoints'])
        self.assertEqual({datapoint['pid']:color},snapshot_config['colors'])
        self.assertEqual(widgetname,snapshot_config['widgetname'])
        self.assertEqual(types.LINEGRAPH,snapshot_config['type'])

    def test_get_snapshot_config_success_snapshot_table(self):
        ''' get_snapshot_config should succeed and return snapshot table config '''
        username='test_get_snapshot_config_success_snapshot_table_user'
        agentname='test_get_snapshot_config_success_snapshot_table_agent'
        datasourcename='test_get_snapshot_config_success_snapshot_table_datasource'
        datapointname='test_get_snapshot_config_success_snapshot_table_datapoint'
        widgetname='test_get_snapshot_config_success_snapshot_table_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_table(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        self.assertEqual(snapshot['nid'],snapshot_config['nid'])
        self.assertEqual(snapshot['wid'],snapshot_config['wid'])
        self.assertEqual(snapshot['uid'],snapshot_config['uid'])
        self.assertEqual(snapshot['interval_init'],snapshot_config['interval_init'])
        self.assertEqual(snapshot['interval_end'],snapshot_config['interval_end'])
        self.assertEqual({datapoint['pid']},snapshot_config['datapoints'])
        self.assertEqual({datapoint['pid']:color},snapshot_config['colors'])
        self.assertEqual(widgetname,snapshot_config['widgetname'])
        self.assertEqual(types.TABLE,snapshot_config['type'])

    def test_get_snapshots_config_failure_invalid_username(self):
        ''' get_snapshots_config should fail if username is not valid '''
        usernames=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), 'Usernames','user name']
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.get_snapshots_config, username=username)

    def test_get_snapshots_config_failure_non_existent_username(self):
        ''' get_snapshots_config should fail if username does not exist '''
        username='test_get_snapshots_config_failure_non_existent_username'
        self.assertRaises(exceptions.UserNotFoundException, snapshotapi.get_snapshots_config, username=username)

    def test_get_snapshots_config_success_no_snapshots(self):
        ''' get_snapshots should succeed and return an empty array if user has no snapshots '''
        username='test_get_snapshots_config_success_no_snapshots'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(snapshotapi.get_snapshots_config(username=username),[])
    
    def test_get_snapshots_config_success_some_snapshots(self):
        ''' get_snapshots should succeed and return some snapshots '''
        username='test_get_snapshots_config_success_some_snapshots'
        email=username+'@komlog.org'
        password='password'
        agentname='test_get_snapshot_config_success_snapshot_table_agent'
        datasourcename='test_get_snapshot_config_success_snapshot_table_datasource'
        datapointname='test_get_snapshot_config_success_snapshot_table_datapoint'
        widgetname='test_get_snapshot_config_success_snapshot_table_widget'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget_tb=widgetapi.new_widget_table(username=username, widgetname=widgetname) 
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget_tb['wid'],pid=datapoint['pid']))
        widget_ds=widgetapi.new_widget_datasource(username=username, did=datasource['did'])
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot_ds=snapshotapi.new_snapshot(username=username, wid=widget_ds['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshot_tb=snapshotapi.new_snapshot(username=username, wid=widget_tb['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshots=snapshotapi.get_snapshots_config(username=username)
        self.assertEqual(len(snapshots),2)
        counter=0
        for snapshot in snapshots:
            if snapshot['type']==types.TABLE:
                counter+=1
                self.assertEqual(snapshot['nid'],snapshot_tb['nid'])
                self.assertEqual(snapshot['wid'],snapshot_tb['wid'])
                self.assertEqual(snapshot['uid'],snapshot_tb['uid'])
                self.assertEqual(snapshot['interval_init'],interval_init)
                self.assertEqual(snapshot['interval_end'],interval_end)
                self.assertEqual({datapoint['pid']},snapshot['datapoints'])
                self.assertEqual({datapoint['pid']:color},snapshot['colors'])
                self.assertEqual(widgetname,snapshot['widgetname'])
            elif snapshot['type']==types.DATASOURCE:
                counter+=1
                self.assertEqual(snapshot['nid'],snapshot_ds['nid'])
                self.assertEqual(snapshot['wid'],snapshot_ds['wid'])
                self.assertEqual(snapshot['uid'],snapshot_ds['uid'])
                self.assertEqual(snapshot['interval_init'],interval_init)
                self.assertEqual(snapshot['interval_end'],interval_end)
                self.assertEqual(datasource['did'],snapshot['did'])
        self.assertEqual(counter,2)

    def test_delete_snapshot_failure_invalid_nid(self):
        ''' delete_snapshot should fail if nid is invalid '''
        nids=[None, 2342, 23422.2342, {'a':'dict'}, ['a','list'], ('a','tuple'), {'set'},'username',uuid.uuid4().hex, uuid.uuid1(), timeuuid.uuid1()]
        for nid in nids:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.delete_snapshot, nid=nid)

    def test_delete_snapshot_failure_non_existent_nid(self):
        ''' delete_snapshot should fail if nid does not exist '''
        nid=uuid.uuid4()
        self.assertRaises(exceptions.SnapshotNotFoundException, snapshotapi.delete_snapshot, nid=nid)
    
    def test_delete_snapshot_success(self):
        ''' delete_snapshot should succeed and delete the snapshot successfully '''
        username='test_delete_snapshot_success'
        agentname='test_get_snapshot_success'
        datasourcename='test_delete_snapshot_success'
        datapointname='test_delete_snapshot_success'
        widgetname='test_delete_snapshot_success'
        email=username+'@komlog.org'
        password='password'
        pubkey='testpubkey'
        version='test_version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=widgetapi.new_widget_table(username=username, widgetname=widgetname) 
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['uid'], user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertEqual(widget['widgetname'],widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        self.assertEqual(snapshot['wid'],widget['wid'])
        self.assertEqual(snapshot['uid'],user['uid'])
        self.assertEqual(snapshot['interval_init'],interval_init)
        self.assertEqual(snapshot['interval_end'],interval_end)
        self.assertTrue(isinstance(snapshot['nid'],uuid.UUID))
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        self.assertEqual(snapshot['nid'],snapshot_config['nid'])
        self.assertEqual(snapshot['wid'],snapshot_config['wid'])
        self.assertEqual(snapshot['uid'],snapshot_config['uid'])
        self.assertEqual(snapshot['interval_init'],snapshot_config['interval_init'])
        self.assertEqual(snapshot['interval_end'],snapshot_config['interval_end'])
        self.assertEqual({datapoint['pid']},snapshot_config['datapoints'])
        self.assertEqual({datapoint['pid']:color},snapshot_config['colors'])
        self.assertEqual(widgetname,snapshot_config['widgetname'])
        self.assertEqual(types.TABLE,snapshot_config['type'])
        self.assertTrue(snapshotapi.delete_snapshot(nid=snapshot_config['nid']))
        self.assertRaises(exceptions.SnapshotNotFoundException, snapshotapi.get_snapshot_config, nid=snapshot_config['nid'])

    def test_get_snapshot_data_failure_invalid_nid(self):
        ''' get_snapshot_data should fail if nid is invalid '''
        nids=[None, 2342, 23422.2342, {'a':'dict'}, ['a','list'], ('a','tuple'), {'set'},'username',uuid.uuid4().hex, uuid.uuid1(), timeuuid.uuid1()]
        for nid in nids:
            self.assertRaises(exceptions.BadParametersException, snapshotapi.get_snapshot_data, nid=nid)

    def test_get_snapshot_data_failure_non_existent_nid(self):
        ''' get_snapshot_data should fail if nid does not exist '''
        nid=uuid.uuid4()
        self.assertRaises(exceptions.SnapshotNotFoundException, snapshotapi.get_snapshot_data, nid=nid)
    
    def test_get_snapshot_data_success_datasource(self):
        ''' get_snapshot_data should succeed and return the datasource content '''
        username='test_get_snapshot_data_success_datasource_user'
        agentname='test_get_snapshot_data_success_datasource_agent'
        datasourcename='test_get_snapshot_data_success_datasource_datasource'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotdatasuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        uid=user['uid']
        did=datasource['did']
        widget=widgetapi.new_widget_datasource(username=username, did=did)
        content='DATASOURCE CONTENT'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        date2=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-2)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date2,content=content))
        interval_init=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-1)
        interval_end=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)+1)
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        snapshot_data=snapshotapi.get_snapshot_data(nid=snapshot_config['nid'])
        self.assertEqual(list(snapshot_data.keys()),[datasource['did']])
        self.assertEqual(len(snapshot_data[datasource['did']]),1)
        self.assertEqual(snapshot_data[datasource['did']][0]['date'],date)
        self.assertEqual(snapshot_data[datasource['did']][0]['content'],content)
        self.assertEqual(snapshot_data[datasource['did']][0]['datapoints'],{})

    def test_get_snapshot_data_success_datapoint(self):
        ''' get_snapshot_data should succeed and return the datapoint content '''
        username='test_get_snapshot_data_success_datapoint_user'
        agentname='test_get_snapshot_data_success_datapoint_agent'
        datasourcename='test_get_snapshot_data_success_datapoint_datasource'
        datapointname='test_get_snapshot_data_success_datapoint_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotdatasuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        for i in range(1,100):
            date=timeuuid.uuid1(seconds=i)
            value=i
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value),pid=datapoint['pid'])
        widget=widgetapi.new_widget_datapoint(username=username, pid=datapoint['pid'])
        interval_init=timeuuid.uuid1(seconds=10.5)
        interval_end=timeuuid.uuid1(seconds=30.5)
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        snapshot_data=snapshotapi.get_snapshot_data(nid=snapshot_config['nid'])
        self.assertEqual(list(snapshot_data.keys()),[datapoint['pid']])
        self.assertEqual(len(snapshot_data[datapoint['pid']]),20)
        for i in range(20,0):
            self.assertEqual(snapshot_data[datapoint['pid']][i]['value'],Decimal(10+i))

    def test_get_snapshot_data_success_histogram(self):
        ''' get_snapshot_data should succeed and return the histogram content '''
        username='test_get_snapshot_data_success_histogram_user'
        agentname='test_get_snapshot_data_success_histogram_agent'
        datasourcename='test_get_snapshot_data_success_histogram_datasource'
        widgetname='test_get_snapshot_data_success_histogram_widget'
        datapointname1='test_get_snapshot_data_success_histogram_datapoint_1'
        datapointname2='test_get_snapshot_data_success_histogram_datapoint_2'
        datapointname3='test_get_snapshot_data_success_histogram_datapoint_3'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotdatasuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint1=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname1, color=color)
        color=libcolors.get_random_color()
        datapoint2=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname2, color=color)
        color=libcolors.get_random_color()
        datapoint3=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname3, color=color)
        for i in range(1,100):
            date=timeuuid.uuid1(seconds=i)
            value=i
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+1000),pid=datapoint1['pid'])
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+2000),pid=datapoint2['pid'])
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+3000),pid=datapoint3['pid'])
        widget=widgetapi.new_widget_histogram(username=username, widgetname=widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint1['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint2['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint3['pid']))
        interval_init=timeuuid.uuid1(seconds=10.5)
        interval_end=timeuuid.uuid1(seconds=30.5)
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        snapshot_data=snapshotapi.get_snapshot_data(nid=snapshot_config['nid'])
        self.assertEqual(sorted(list(snapshot_data.keys())),sorted([datapoint1['pid'],datapoint2['pid'],datapoint3['pid']]))
        self.assertEqual(len(snapshot_data[datapoint1['pid']]),20)
        self.assertEqual(len(snapshot_data[datapoint2['pid']]),20)
        self.assertEqual(len(snapshot_data[datapoint3['pid']]),20)
        for i in range(20,0):
            self.assertEqual(snapshot_data[datapoint1['pid']][i]['value'],Decimal(1010+i))
            self.assertEqual(snapshot_data[datapoint2['pid']][i]['value'],Decimal(2010+i))
            self.assertEqual(snapshot_data[datapoint3['pid']][i]['value'],Decimal(3010+i))

    def test_get_snapshot_data_success_linegraph(self):
        ''' get_snapshot_data should succeed and return the linegraph content '''
        username='test_get_snapshot_data_success_linegraph_user'
        agentname='test_get_snapshot_data_success_linegraph_agent'
        datasourcename='test_get_snapshot_data_success_linegraph_datasource'
        widgetname='test_get_snapshot_data_success_linegraph_widget'
        datapointname1='test_get_snapshot_data_success_linegraph_datapoint_1'
        datapointname2='test_get_snapshot_data_success_linegraph_datapoint_2'
        datapointname3='test_get_snapshot_data_success_linegraph_datapoint_3'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotdatasuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint1=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname1, color=color)
        color=libcolors.get_random_color()
        datapoint2=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname2, color=color)
        color=libcolors.get_random_color()
        datapoint3=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname3, color=color)
        for i in range(1,100):
            date=timeuuid.uuid1(seconds=i)
            value=i
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+1000),pid=datapoint1['pid'])
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+2000),pid=datapoint2['pid'])
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+3000),pid=datapoint3['pid'])
        widget=widgetapi.new_widget_linegraph(username=username, widgetname=widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint1['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint2['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint3['pid']))
        interval_init=timeuuid.uuid1(seconds=10.5)
        interval_end=timeuuid.uuid1(seconds=30.5)
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        snapshot_data=snapshotapi.get_snapshot_data(nid=snapshot_config['nid'])
        self.assertEqual(sorted(list(snapshot_data.keys())),sorted([datapoint1['pid'],datapoint2['pid'],datapoint3['pid']]))
        self.assertEqual(len(snapshot_data[datapoint1['pid']]),20)
        self.assertEqual(len(snapshot_data[datapoint2['pid']]),20)
        self.assertEqual(len(snapshot_data[datapoint3['pid']]),20)
        for i in range(20,0):
            self.assertEqual(snapshot_data[datapoint1['pid']][i]['value'],Decimal(1010+i))
            self.assertEqual(snapshot_data[datapoint2['pid']][i]['value'],Decimal(2010+i))
            self.assertEqual(snapshot_data[datapoint3['pid']][i]['value'],Decimal(3010+i))

    def test_get_snapshot_data_success_table(self):
        ''' get_snapshot_data should succeed and return the table content '''
        username='test_get_snapshot_data_success_table_user'
        agentname='test_get_snapshot_data_success_table_agent'
        datasourcename='test_get_snapshot_data_success_table_datasource'
        widgetname='test_get_snapshot_data_success_table_widget'
        datapointname1='test_get_snapshot_data_success_table_datapoint_1'
        datapointname2='test_get_snapshot_data_success_table_datapoint_2'
        datapointname3='test_get_snapshot_data_success_table_datapoint_3'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetsnapshotdatasuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint1=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname1, color=color)
        color=libcolors.get_random_color()
        datapoint2=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname2, color=color)
        color=libcolors.get_random_color()
        datapoint3=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname3, color=color)
        for i in range(1,100):
            date=timeuuid.uuid1(seconds=i)
            value=i
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+1000),pid=datapoint1['pid'])
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+2000),pid=datapoint2['pid'])
            cassapidatapoint.insert_datapoint_data(date=date,value=Decimal(value+3000),pid=datapoint3['pid'])
        widget=widgetapi.new_widget_table(username=username, widgetname=widgetname)
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint1['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint2['pid']))
        self.assertTrue(widgetapi.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint3['pid']))
        interval_init=timeuuid.uuid1(seconds=10.5)
        interval_end=timeuuid.uuid1(seconds=30.5)
        snapshot=snapshotapi.new_snapshot(username=username, wid=widget['wid'], interval_init=interval_init, interval_end=interval_end)
        snapshot_config=snapshotapi.get_snapshot_config(nid=snapshot['nid'])
        snapshot_data=snapshotapi.get_snapshot_data(nid=snapshot_config['nid'])
        self.assertEqual(sorted(list(snapshot_data.keys())),sorted([datapoint1['pid'],datapoint2['pid'],datapoint3['pid']]))
        self.assertEqual(len(snapshot_data[datapoint1['pid']]),20)
        self.assertEqual(len(snapshot_data[datapoint2['pid']]),20)
        self.assertEqual(len(snapshot_data[datapoint3['pid']]),20)
        for i in range(20,0):
            self.assertEqual(snapshot_data[datapoint1['pid']][i]['value'],Decimal(1010+i))
            self.assertEqual(snapshot_data[datapoint2['pid']][i]['value'],Decimal(2010+i))
            self.assertEqual(snapshot_data[datapoint3['pid']][i]['value'],Decimal(3010+i))

