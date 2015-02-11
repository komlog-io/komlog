import unittest
import uuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi 
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api, types
from komlibs.gestaccount import exceptions
from komcass.model.orm import widget as ormwidget
from komlibs.general import colors as libcolors

class GestaccountWidgetApiTest(unittest.TestCase):
    ''' komlog.gestaccount.widget.api tests '''

    def test_get_widget_config_non_existent_widget(self):
        ''' get_widget_config should fail if wid is not in system '''
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.get_widget_config, wid=wid)

    def test_get_widget_config_success_DATASOURCE(self):
        ''' get_widget_config should succeed if wid exists and is DATASOURCE type '''
        username='test_get_widget_config_success_ds_widget_user'
        agentname='test_get_widget_config_success_DATASOURCE_agent'
        datasourcename='test_get_widget_config_success_DATASOURCE_datasource'
        datapointname='test_get_widget_config_success_DATASOURCE_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetconfigsuccessDSWIDGETpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_datasource(username=user['username'], did=datasource['did']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATASOURCE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['did'],widget['did'])

    def test_get_widget_config_success_DATAPOINT(self):
        ''' get_widget_config should succeed if wid exists and is DATAPOINT type '''
        username='test_get_widget_config_success_dp_widget_user'
        agentname='test_get_widget_config_success_DATAPOINT_agent'
        datasourcename='test_get_widget_config_success_DATAPOINT_datasource'
        datapointname='test_get_widget_config_success_DATAPOINT_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetconfigsuccessDPWIDGETpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_datapoint(username=user['username'], pid=datapoint['pid']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATAPOINT)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['pid'],widget['pid'])

    def test_get_widgets_config_non_existent_username(self):
        ''' get_widgets_config should fail if username is not in system '''
        username='test_get_widgets_config_non_existent_username'
        self.assertRaises(exceptions.UserNotFoundException, api.get_widgets_config, username=username)

    def test_get_widgets_config_success_no_widgets(self):
        ''' get_widgets_config should succeed if username exists in system '''
        username='test_get_widgets_config_success_no_widgets_user'
        agentname='test_get_widgets_config_success_no_widgets_agent'
        datasourcename='test_get_widgets_config_success_no_widgets_datasource'
        datapointname='test_get_widgets_config_success_no_widgets_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetsconfigssuccessnowidgetspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        data=api.get_widgets_config(username=user['username'])
        self.assertEqual(data, [])

    def test_get_widgets_config_success_some_widgets(self):
        ''' get_widgets_config should succeed if username exists in system '''
        username='test_get_widgets_config_success_some_widgets_user'
        agentname='test_get_widgets_config_success_some_widgets_agent'
        datasourcename='test_get_widgets_config_success_some_widgets_datasource'
        datapointname='test_get_widgets_config_success_some_widgets_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetsconfigsuccesssomewidgetspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget_dp=api.new_widget_datapoint(username=user['username'], pid=datapoint['pid']) 
        widget_ds=api.new_widget_datasource(username=user['username'], did=datasource['did']) 
        data=api.get_widgets_config(username=user['username'])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data),2)
        for widget in data:
            if widget['type']==types.DATASOURCE:
                self.assertEqual(widget['wid'],widget_ds['wid'])
                self.assertEqual(widget['did'],widget_ds['did'])
                self.assertEqual(widget['type'],widget_ds['type'])
            else:
                self.assertEqual(widget['wid'],widget_dp['wid'])
                self.assertEqual(widget['pid'],widget_dp['pid'])
                self.assertEqual(widget['type'],widget_dp['type'])

    def test_delete_widget_non_existent_widget(self):
        ''' delete_widget should fail if widget is not in system '''
        username='test_delete_widget_config_non_existent_widget_user'
        agentname='test_delete_widget_config_non_existent_widget_agent'
        datasourcename='test_delete_widget_config_non_existent_widget_datasource'
        datapointname='test_delete_widget_config_non_existent_widget_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testdeletewidgetnonexistentwidgetpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, wid=wid)

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
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        widget=api.new_widget_datasource(username=username, did=datasource['did']) 
        self.assertTrue(api.delete_widget(wid=widget['wid']))
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, wid=widget['wid'])

    def test_delete_widget_dp_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        username='test_delete_widget_dp_success_user'
        agentname='test_delete_widget_dp_success_agent'
        datasourcename='test_delete_widget_dp_success_datasource'
        datapointname='test_delete_widget_dp_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testdeletewidgetdpsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_datapoint(username=username, pid=datapoint['pid']) 
        self.assertTrue(api.delete_widget(wid=widget['wid']))
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, wid=widget['wid'])

    def test_new_widget_datasource_non_existent_username(self):
        ''' new_widget_datasource should fail if username does not exist '''
        username='test_new_widget_datasource_non_existent_username'
        did=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_datasource, username=username, did=did)

    def test_new_widget_datasource_non_existent_datasource(self):
        ''' new_widget_datasource should fail if datasource does not exist '''
        username='test_new_widget_datasource_non_existent_datasource_user'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.new_widget_datasource, username=username, did=did)

    def test_new_widget_datasource_success(self):
        ''' new_widget_datasource should succeed if datasource exists and user too '''
        username='test_new_widget_datasource_success_user'
        agentname='test_new_widget_datasource_success_agent'
        datasourcename='test_new_widget_datasource_success_datasource'
        datapointname='test_new_widget_datasource_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testnewwidgetdssuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        uid=user['uid']
        did=datasource['did']
        widget=api.new_widget_datasource(username=username, did=did)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], did)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DATASOURCE)
        self.assertEqual(widget['widgetname'],datasourcename)
        self.assertEqual(len(widget.keys()),5)

    def test_new_widget_datapoint_non_existent_username(self):
        ''' new_widget_datapoint should fail if username does not exist '''
        username='test_new_widget_datapoint_non_existent_username'
        pid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_datapoint, username=username, pid=pid)

    def test_new_widget_datapoint_non_existent_datapoint(self):
        ''' new_widget_datapoint should fail if datapoint does not exist '''
        username='test_new_widget_datapoint_non_existent_datapoint_user'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.new_widget_datapoint, username=username, pid=pid)

    def test_new_widget_datapoint_success(self):
        ''' new_widget_datapoint should succeed if datapoint exists and user too '''
        username='test_new_widget_datapoint_success_user'
        agentname='test_new_widget_datapoint_success_agent'
        datasourcename='test_new_widget_datapoint_success_datasource'
        datapointname='test_new_widget_datapoint_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testnewwidgetdpsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        uid=user['uid']
        pid=datapoint['pid']
        widget=api.new_widget_datapoint(username=username, pid=pid)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], pid)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DATAPOINT)
        self.assertEqual(widget['widgetname'], datapointname)
        self.assertEqual(len(widget.keys()),5)

    def test_new_widget_linegraph_failure_invalid_username(self):
        ''' new_widget_linegraph should fail if username is invalid '''
        usernames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        widgetname='test_new_widget_linegraph_failure_invalid_username'
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_linegraph, username=username, widgetname=widgetname)

    def test_new_widget_linegraph_failure_invalid_widgetname(self):
        ''' new_widget_linegraph should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        username='test_new_widget_linegraph_failure_invalid_widgetname'
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_linegraph, username=username, widgetname=widgetname)

    def test_new_widget_linegraph_failure_non_existent_user(self):
        ''' new_widget_linegraph should fail if user does not exist '''
        username='test_new_widget_failure_non_existent_user'
        widgetname='test_new_widget_failure_non_existent_user'
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_linegraph, username=username, widgetname=widgetname)

    def test_new_widget_linegraph_success(self):
        ''' new_widget_linegraph should succeed if user exists '''
        username='test_new_widget_linegraph_success'
        widgetname='test_new_widget_linegraph_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_linegraph_success_agent'
        pubkey='testnewwidgetlinegraphsuccessHISTOGRAMpubkey'
        version='Test Version'
        datasourcename='test_new_widget_linegraph_success_datasource'
        datapointname='test_new_widget_linegraph_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_linegraph(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.LINEGRAPH)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_add_datapoint_to_widget_success_widget_linegraph(self):
        ''' add_datapoint_to_widget should succeed if widget is of type linegraph '''
        username='test_add_datapoint_to_widget_success_widget_linegraph'
        widgetname='test_add_datapoint_to_widget_success_widget_linegraph'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_add_datapoint_to_widget_linegraph_success_agent'
        pubkey='testnewwidgetlinegraphsuccessHISTOGRAMpubkey'
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_linegraph_success_datasource'
        datapointname='test_add_datapoint_to_widget_linegraph_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_linegraph(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.LINEGRAPH)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.LINEGRAPH)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(list(data['colors'].keys()),[pid])

    def test_delete_datapoint_from_widget_success_widget_linegraph(self):
        ''' delete_datapoint_from_widget should succeed if widget is of type linegraph '''
        username='test_delete_datapoint_from_widget_success_widget_linegraph'
        widgetname='test_delete_datapoint_from_widget_success_widget_linegraph'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_delete_datapoint_from_widget_linegraph_success_agent'
        pubkey='testnewwidgetlinegraphsuccessHISTOGRAMpubkey'
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_linegraph_success_datasource'
        datapointname='test_delete_datapoint_from_widget_linegraph_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_linegraph(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.LINEGRAPH)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.LINEGRAPH)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(list(data['colors'].keys()),[pid])
        self.assertTrue(api.delete_datapoint_from_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.LINEGRAPH)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_new_widget_table_failure_invalid_username(self):
        ''' new_widget_table should fail if username is invalid '''
        usernames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        widgetname='test_new_widget_table_failure_invalid_username'
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_table, username=username, widgetname=widgetname)

    def test_new_widget_table_failure_invalid_widgetname(self):
        ''' new_widget_table should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        username='test_new_widget_table_failure_invalid_widgetname'
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_table, username=username, widgetname=widgetname)

    def test_new_widget_table_failure_non_existent_user(self):
        ''' new_widget_table should fail if user does not exist '''
        username='test_new_widget_failure_non_existent_user'
        widgetname='test_new_widget_failure_non_existent_user'
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_table, username=username, widgetname=widgetname)

    def test_new_widget_table_success(self):
        ''' new_widget_table should succeed if user exists '''
        username='test_new_widget_table_success'
        widgetname='test_new_widget_table_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_table_success_agent'
        pubkey='testnewwidgettablesuccessTABLEpubkey'
        version='Test Version'
        datasourcename='test_new_widget_table_success_datasource'
        datapointname='test_new_widget_table_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_table(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.TABLE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_add_datapoint_to_widget_success_widget_table(self):
        ''' add_datapoint_to_widget should succeed if widget is of type table '''
        username='test_add_datapoint_to_widget_success_widget_table'
        widgetname='test_add_datapoint_to_widget_success_widget_table'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_add_datapoint_to_widget_table_success_agent'
        pubkey='testnewwidgettablesuccessTABLEpubkey'
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_table_success_datasource'
        datapointname='test_add_datapoint_to_widget_table_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_table(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.TABLE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.TABLE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(list(data['colors'].keys()),[pid])

    def test_delete_datapoint_from_widget_success_widget_table(self):
        ''' delete_datapoint_from_widget should succeed if widget is of type table '''
        username='test_delete_datapoint_from_widget_success_widget_table'
        widgetname='test_delete_datapoint_from_widget_success_widget_table'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_delete_datapoint_from_widget_table_success_agent'
        pubkey='testnewwidgettablesuccessTABLEpubkey'
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_table_success_datasource'
        datapointname='test_delete_datapoint_from_widget_table_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_table(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.TABLE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.TABLE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(list(data['colors'].keys()),[pid])
        self.assertTrue(api.delete_datapoint_from_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.TABLE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_new_widget_histogram_failure_invalid_username(self):
        ''' new_widget_histogram should fail if username is invalid '''
        usernames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        widgetname='test_new_widget_histogram_failure_invalid_username'
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_histogram, username=username, widgetname=widgetname)

    def test_new_widget_histogram_failure_invalid_widgetname(self):
        ''' new_widget_histogram should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        username='test_new_widget_histogram_failure_invalid_username'
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_histogram, username=username, widgetname=widgetname)

    def test_new_widget_histogram_failure_non_existent_user(self):
        ''' new_widget_table should fail if user does not exist '''
        username='test_new_widget_failure_non_existent_user'
        widgetname='test_new_widget_histogram_failure_invalid_username'
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_histogram, username=username, widgetname=widgetname)

    def test_new_widget_histogram_success(self):
        ''' new_widget_histogram should succeed if user exists '''
        username='test_new_widget_histogram_success'
        widgetname='test_new_widget_histogram_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_histogram_success_agent'
        pubkey='testnewwidgethistogramsuccessHISTOGRAMpubkey'
        version='Test Version'
        datasourcename='test_new_widget_histogram_success_datasource'
        datapointname='test_new_widget_histogram_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_histogram(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_add_datapoint_to_widget_failure_invalid_wid(self):
        ''' add_datapoint_to_widget should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        pid=uuid.uuid4()
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.add_datapoint_to_widget, wid=wid, pid=pid)

    def test_add_datapoint_to_widget_failure_invalid_pid(self):
        ''' add_datapoint_to_widget should fail if pid is invalid '''
        pids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        wid=uuid.uuid4()
        for pid in pids:
            self.assertRaises(exceptions.BadParametersException, api.add_datapoint_to_widget, wid=wid, pid=pid)

    def test_add_datapoint_to_widget_failure_non_existent_wid(self):
        ''' add_datapoint_to_widget should fail if wid does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.add_datapoint_to_widget, wid=wid, pid=pid)

    def test_add_datapoint_to_widget_success_widget_histogram(self):
        ''' add_datapoint_to_widget should succeed if widget is of type histogram '''
        username='test_add_datapoint_to_widget_success_widget_histogram'
        widgetname='test_add_datapoint_to_widget_success_widget_histogram'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_add_datapoint_to_widget_histogram_success_agent'
        pubkey='testnewwidgethistogramsuccessHISTOGRAMpubkey'
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_histogram_success_datasource'
        datapointname='test_add_datapoint_to_widget_histogram_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_histogram(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(list(data['colors'].keys()),[pid])

    def test_add_datapoint_to_widget_failure_unsupported_operation(self):
        ''' add_datapoint_to_widget should fail if widget type does not support the operation '''
        username='test_add_datapoint_to_widget_user'
        agentname='test_add_datapoint_to_widget_agent'
        datasourcename='test_add_datapoint_to_widget_datasource'
        datapointname='test_add_datapoint_to_widget_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetconfigsuccessDSWIDGETpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_datasource(username=user['username'], did=datasource['did']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATASOURCE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['did'],widget['did'])
        self.assertRaises(exceptions.WidgetUnsupportedOperationException, api.add_datapoint_to_widget, wid=widget['wid'], pid=datapoint['pid'])

    def test_delete_datapoint_from_widget_failure_invalid_wid(self):
        ''' delete_datapoint_from_widget should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        pid=uuid.uuid4()
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.delete_datapoint_from_widget, wid=wid, pid=pid)

    def test_delete_datapoint_from_widget_failure_invalid_pid(self):
        ''' delete_datapoint_from_widget should fail if pid is invalid '''
        pids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        wid=uuid.uuid4()
        for pid in pids:
            self.assertRaises(exceptions.BadParametersException, api.delete_datapoint_from_widget, wid=wid, pid=pid)

    def test_delete_datapoint_from_widget_failure_non_existent_wid(self):
        ''' delete_datapoint_from_widget should fail if wid does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_datapoint_from_widget, wid=wid, pid=pid)

    def test_delete_datapoint_from_widget_success_widget_histogram(self):
        ''' delete_datapoint_from_widget should succeed if widget is of type histogram '''
        username='test_delete_datapoint_from_widget_success_widget_histogram'
        widgetname='test_delete_datapoint_from_widget_success_widget_histogram'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_delete_datapoint_from_widget_histogram_success_agent'
        pubkey='testnewwidgethistogramsuccessHISTOGRAMpubkey'
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_histogram_success_datasource'
        datapointname='test_delete_datapoint_from_widget_histogram_success_datapoint'
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_histogram(username=user['username'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(list(data['colors'].keys()),[pid])
        self.assertTrue(api.delete_datapoint_from_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_delete_datapoint_from_widget_failure_unsupported_operation(self):
        ''' delete_datapoint_from_widget should fail if widget type does not support the operation '''
        username='test_delete_datapoint_from_widget_user'
        agentname='test_delete_datapoint_from_widget_agent'
        datasourcename='test_delete_datapoint_from_widget_datasource'
        datapointname='test_delete_datapoint_from_widget_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetconfigsuccessDSWIDGETpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_datasource(username=user['username'], did=datasource['did']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATASOURCE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['did'],widget['did'])
        self.assertRaises(exceptions.WidgetUnsupportedOperationException, api.delete_datapoint_from_widget, wid=widget['wid'], pid=datapoint['pid'])

    def test_update_widget_datasource_failure_invalid_wid(self):
        ''' update_widget_datasource should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_datasource_failure_invalid_wid'
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_datasource, wid=wid, widgetname=widgetname)

    def test_update_widget_datasource_failure_invalid_widgetname(self):
        ''' update_widget_datasource should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_datasource, wid=wid, widgetname=widgetname)

    def test_update_widget_datasource_failure_non_existent_wid(self):
        ''' update_widget_datasource should fail if wid does not exist '''
        wid=uuid.uuid4()
        widgetname='test_update_widget_datasource_failure_non_existent_wid'
        self.assertRaises(exceptions.WidgetNotFoundException, api.update_widget_datasource, wid=wid, widgetname=widgetname)

    def test_update_widget_datasource_success(self):
        ''' update_widget_datasource should succeed if wid exists and data is correct '''
        username='test_update_widget_datasource_success'
        agentname='test_update_widget_datasource_success'
        datasourcename='test_update_widget_datasource_success'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetdatasourcesuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        widget=api.new_widget_datasource(username=username, did=datasource['did']) 
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], datasourcename)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['did'], datasource['did'])
        self.assertEqual(widget['type'], types.DATASOURCE)
        new_widgetname='test_update_widget_datasource_success_2'
        self.assertTrue(api.update_widget_datasource(wid=widget['wid'], widgetname=new_widgetname))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['did'],widget_config['did'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])

    def test_update_widget_datapoint_failure_invalid_wid(self):
        ''' update_widget_datapoint should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_datapoint_failure_invalid_wid'
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_datapoint, wid=wid, widgetname=widgetname)

    def test_update_widget_datapoint_failure_invalid_widgetname(self):
        ''' update_widget_datapoint should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_datapoint, wid=wid, widgetname=widgetname)

    def test_update_widget_datapoint_failure_non_existent_wid(self):
        ''' update_widget_datapoint should fail if wid does not exist '''
        wid=uuid.uuid4()
        widgetname='test_update_widget_datapoint_failure_non_existent_wid'
        self.assertRaises(exceptions.WidgetNotFoundException, api.update_widget_datapoint, wid=wid, widgetname=widgetname)

    def test_update_widget_datapoint_success(self):
        ''' update_widget_datapoint should succeed if wid exists and data is correct '''
        username='test_update_widget_datapoint_success'
        agentname='test_update_widget_datapoint_success'
        datasourcename='test_update_widget_datapoint_success'
        datapointname='test_update_widget_datapoint_success'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetdatapointsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widget=api.new_widget_datapoint(username=username, pid=datapoint['pid']) 
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], datapointname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['pid'], datapoint['pid'])
        self.assertEqual(widget['type'], types.DATAPOINT)
        new_widgetname='test_update_widget_datapoint_success_2'
        self.assertTrue(api.update_widget_datapoint(wid=widget['wid'], widgetname=new_widgetname))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['pid'],widget_config['pid'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])

    def test_update_widget_histogram_failure_invalid_wid(self):
        ''' update_widget_histogram should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_histogram_failure_invalid_wid'
        colors={uuid.uuid4():'#AABB00'}
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_histogram, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_histogram_failure_invalid_widgetname(self):
        ''' update_widget_histogram should fail if widgetname is invalid '''
        widgetnames=[123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        colors={uuid.uuid4():'#AABB00'}
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_histogram, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_histogram_failure_invalid_colors(self):
        ''' update_widget_histogram should fail if colors is invalid '''
        colores=[123123, 12313.1231, ('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        widgetname='test_update_widget_histogram_failure_invalid_colors'
        for colors in colores:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_histogram, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_histogram_failure_non_existent_wid(self):
        ''' update_widget_histogram should fail if wid does not exist '''
        wid=uuid.uuid4()
        colors={uuid.uuid4():'#AABB00'}
        widgetname='test_update_widget_histogram_failure_non_existent_wid'
        self.assertRaises(exceptions.WidgetNotFoundException, api.update_widget_histogram, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_histogram_success(self):
        ''' update_widget_histogram should succeed if wid exists and data is correct '''
        username='test_update_widget_histogram_success'
        agentname='test_update_widget_histogram_success'
        datasourcename='test_update_widget_histogram_success'
        datapointname='test_update_widget_histogram_success'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgethistogramsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_histogram_success'
        widget=api.new_widget_histogram(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.HISTOGRAM)
        new_widgetname='test_update_widget_histogram_success_2'
        new_colors={datapoint['pid']:'#ABCDEF'}
        self.assertTrue(api.update_widget_histogram(wid=widget['wid'], widgetname=new_widgetname, colors=new_colors))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(new_colors,widget_config['colors'])

    def test_update_widget_histogram_success_only_widgetname(self):
        ''' update_widget_histogram should succeed if wid exists and we only want to update de widgetname '''
        username='test_update_widget_histogram_success_only_widgetname'
        agentname='test_update_widget_histogram_success_only_widgetname'
        datasourcename='test_update_widget_histogram_success_only_widgetname'
        datapointname='test_update_widget_histogram_success_only_widgetname'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgethistogramsuccesspubkeyonlywidgetname'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_histogram_success_only_widgetname'
        widget=api.new_widget_histogram(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.HISTOGRAM)
        new_widgetname='test_update_widget_histogram_success_2'
        self.assertTrue(api.update_widget_histogram(wid=widget['wid'], widgetname=new_widgetname))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(widget['colors'],widget_config['colors'])

    def test_update_widget_histogram_success_only_colors(self):
        ''' update_widget_histogram should succeed if wid exists and we only want to update colors '''
        username='test_update_widget_histogram_success_only_colors'
        agentname='test_update_widget_histogram_success_only_colors'
        datasourcename='test_update_widget_histogram_success_only_colors'
        datapointname='test_update_widget_histogram_success_only_colors'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgethistogramsuccesspubkeyonlycolors'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_histogram_success_only_colors'
        widget=api.new_widget_histogram(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.HISTOGRAM)
        new_colors={datapoint['pid']:'#ABCDEF'}
        self.assertTrue(api.update_widget_histogram(wid=widget['wid'], colors=new_colors))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(widget['widgetname'],widget_config['widgetname'])
        self.assertEqual(new_colors,widget_config['colors'])

    def test_update_widget_histogram_failure_non_existent_pid(self):
        ''' update_widget_histogram should fail if we try to update a pid that does not belong to widget '''
        username='test_update_widget_histogram_failure_non_existent_pid'
        agentname='test_update_widget_histogram_failure_non_existent_pid'
        datasourcename='test_update_widget_histogram_failure_non_existent_pid'
        datapointname='test_update_widget_histogram_failure_non_existent_pid'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgethistogramfailurenonexistentpid'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_histogram_failure_non_existent_pid'
        widget=api.new_widget_histogram(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.HISTOGRAM)
        new_colors={uuid.uuid4():'#ABCDEF'}
        self.assertRaises(exceptions.DatapointNotFoundException, api.update_widget_histogram, wid=widget['wid'], colors=new_colors)

    def test_update_widget_histogram_failure_invalid_color(self):
        ''' update_widget_histogram should fail if we try to update a pid with an invalid color '''
        username='test_update_widget_histogram_failure_invalid_color'
        agentname='test_update_widget_histogram_failure_invalid_color'
        datasourcename='test_update_widget_histogram_failure_invalid_color'
        datapointname='test_update_widget_histogram_failure_invalid_color'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgethistogramfailureinvalidcolor'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_histogram_failure_invalid_color'
        widget=api.new_widget_histogram(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.HISTOGRAM)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.HISTOGRAM)
        colors=[None, 23423, 2323.23423, 'AADDEE','aasd98','#AAcdFP',{'a':'dict'},('a','tuple'),['a','list'],{'set','aset'},uuid.uuid4(), uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex]
        for color in colors:
            new_colors={datapoint['pid']:color}
            self.assertRaises(exceptions.BadParametersException, api.update_widget_histogram, wid=widget['wid'], colors=new_colors)

    def test_update_widget_linegraph_failure_invalid_wid(self):
        ''' update_widget_linegraph should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_linegraph_failure_invalid_wid'
        colors={uuid.uuid4():'#AABB00'}
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_linegraph, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_linegraph_failure_invalid_widgetname(self):
        ''' update_widget_linegraph should fail if widgetname is invalid '''
        widgetnames=[123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        colors={uuid.uuid4():'#AABB00'}
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_linegraph, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_linegraph_failure_invalid_colors(self):
        ''' update_widget_linegraph should fail if colors is invalid '''
        colores=[123123, 12313.1231, ('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        widgetname='test_update_widget_linegraph_failure_invalid_colors'
        for colors in colores:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_linegraph, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_linegraph_failure_non_existent_wid(self):
        ''' update_widget_linegraph should fail if wid does not exist '''
        wid=uuid.uuid4()
        colors={uuid.uuid4():'#AABB00'}
        widgetname='test_update_widget_linegraph_failure_non_existent_wid'
        self.assertRaises(exceptions.WidgetNotFoundException, api.update_widget_linegraph, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_linegraph_success(self):
        ''' update_widget_linegraph should succeed if wid exists and data is correct '''
        username='test_update_widget_linegraph_success'
        agentname='test_update_widget_linegraph_success'
        datasourcename='test_update_widget_linegraph_success'
        datapointname='test_update_widget_linegraph_success'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetlinegraphsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_linegraph_success'
        widget=api.new_widget_linegraph(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.LINEGRAPH)
        new_widgetname='test_update_widget_linegraph_success_2'
        new_colors={datapoint['pid']:'#ABCDEF'}
        self.assertTrue(api.update_widget_linegraph(wid=widget['wid'], widgetname=new_widgetname, colors=new_colors))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(new_colors,widget_config['colors'])

    def test_update_widget_linegraph_success_only_widgetname(self):
        ''' update_widget_linegraph should succeed if wid exists and we only want to update de widgetname '''
        username='test_update_widget_linegraph_success_only_widgetname'
        agentname='test_update_widget_linegraph_success_only_widgetname'
        datasourcename='test_update_widget_linegraph_success_only_widgetname'
        datapointname='test_update_widget_linegraph_success_only_widgetname'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetlinegraphsuccesspubkeyonlywidgetname'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_linegraph_success_only_widgetname'
        widget=api.new_widget_linegraph(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.LINEGRAPH)
        new_widgetname='test_update_widget_linegraph_success_2'
        self.assertTrue(api.update_widget_linegraph(wid=widget['wid'], widgetname=new_widgetname))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(widget['colors'],widget_config['colors'])

    def test_update_widget_linegraph_success_only_colors(self):
        ''' update_widget_linegraph should succeed if wid exists and we only want to update colors '''
        username='test_update_widget_linegraph_success_only_colors'
        agentname='test_update_widget_linegraph_success_only_colors'
        datasourcename='test_update_widget_linegraph_success_only_colors'
        datapointname='test_update_widget_linegraph_success_only_colors'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetlinegraphsuccesspubkeyonlycolors'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_linegraph_success_only_colors'
        widget=api.new_widget_linegraph(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.LINEGRAPH)
        new_colors={datapoint['pid']:'#ABCDEF'}
        self.assertTrue(api.update_widget_linegraph(wid=widget['wid'], colors=new_colors))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(widget['widgetname'],widget_config['widgetname'])
        self.assertEqual(new_colors,widget_config['colors'])

    def test_update_widget_linegraph_failure_non_existent_pid(self):
        ''' update_widget_linegraph should fail if we try to update a pid that does not belong to widget '''
        username='test_update_widget_linegraph_failure_non_existent_pid'
        agentname='test_update_widget_linegraph_failure_non_existent_pid'
        datasourcename='test_update_widget_linegraph_failure_non_existent_pid'
        datapointname='test_update_widget_linegraph_failure_non_existent_pid'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetlinegraphfailurenonexistentpid'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_linegraph_failure_non_existent_pid'
        widget=api.new_widget_linegraph(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.LINEGRAPH)
        new_colors={uuid.uuid4():'#ABCDEF'}
        self.assertRaises(exceptions.DatapointNotFoundException, api.update_widget_linegraph, wid=widget['wid'], colors=new_colors)

    def test_update_widget_linegraph_failure_invalid_color(self):
        ''' update_widget_linegraph should fail if we try to update a pid with an invalid color '''
        username='test_update_widget_linegraph_failure_invalid_color'
        agentname='test_update_widget_linegraph_failure_invalid_color'
        datasourcename='test_update_widget_linegraph_failure_invalid_color'
        datapointname='test_update_widget_linegraph_failure_invalid_color'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgetlinegraphfailureinvalidcolor'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_linegraph_failure_invalid_color'
        widget=api.new_widget_linegraph(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.LINEGRAPH)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.LINEGRAPH)
        colors=[None, 23423, 2323.23423, 'AADDEE','aasd98','#AAcdFP',{'a':'dict'},('a','tuple'),['a','list'],{'set','aset'},uuid.uuid4(), uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex]
        for color in colors:
            new_colors={datapoint['pid']:color}
            self.assertRaises(exceptions.BadParametersException, api.update_widget_linegraph, wid=widget['wid'], colors=new_colors)

    def test_update_widget_table_failure_invalid_wid(self):
        ''' update_widget_table should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_table_failure_invalid_wid'
        colors={uuid.uuid4():'#AABB00'}
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_table, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_table_failure_invalid_widgetname(self):
        ''' update_widget_table should fail if widgetname is invalid '''
        widgetnames=[123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        colors={uuid.uuid4():'#AABB00'}
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_table, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_table_failure_invalid_colors(self):
        ''' update_widget_table should fail if colors is invalid '''
        colores=[123123, 12313.1231, ('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        widgetname='test_update_widget_table_failure_invalid_colors'
        for colors in colores:
            self.assertRaises(exceptions.BadParametersException, api.update_widget_table, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_table_failure_non_existent_wid(self):
        ''' update_widget_table should fail if wid does not exist '''
        wid=uuid.uuid4()
        colors={uuid.uuid4():'#AABB00'}
        widgetname='test_update_widget_table_failure_non_existent_wid'
        self.assertRaises(exceptions.WidgetNotFoundException, api.update_widget_table, wid=wid, widgetname=widgetname, colors=colors)

    def test_update_widget_table_success(self):
        ''' update_widget_table should succeed if wid exists and data is correct '''
        username='test_update_widget_table_success'
        agentname='test_update_widget_table_success'
        datasourcename='test_update_widget_table_success'
        datapointname='test_update_widget_table_success'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgettablesuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_table_success'
        widget=api.new_widget_table(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.TABLE)
        new_widgetname='test_update_widget_table_success_2'
        new_colors={datapoint['pid']:'#ABCDEF'}
        self.assertTrue(api.update_widget_table(wid=widget['wid'], widgetname=new_widgetname, colors=new_colors))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(new_colors,widget_config['colors'])

    def test_update_widget_table_success_only_widgetname(self):
        ''' update_widget_table should succeed if wid exists and we only want to update de widgetname '''
        username='test_update_widget_table_success_only_widgetname'
        agentname='test_update_widget_table_success_only_widgetname'
        datasourcename='test_update_widget_table_success_only_widgetname'
        datapointname='test_update_widget_table_success_only_widgetname'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgettablesuccesspubkeyonlywidgetname'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_table_success_only_widgetname'
        widget=api.new_widget_table(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.TABLE)
        new_widgetname='test_update_widget_table_success_2'
        self.assertTrue(api.update_widget_table(wid=widget['wid'], widgetname=new_widgetname))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(widget['colors'],widget_config['colors'])

    def test_update_widget_table_success_only_colors(self):
        ''' update_widget_table should succeed if wid exists and we only want to update colors '''
        username='test_update_widget_table_success_only_colors'
        agentname='test_update_widget_table_success_only_colors'
        datasourcename='test_update_widget_table_success_only_colors'
        datapointname='test_update_widget_table_success_only_colors'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgettablesuccesspubkeyonlycolors'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_table_success_only_colors'
        widget=api.new_widget_table(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.TABLE)
        new_colors={datapoint['pid']:'#ABCDEF'}
        self.assertTrue(api.update_widget_table(wid=widget['wid'], colors=new_colors))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(widget['widgetname'],widget_config['widgetname'])
        self.assertEqual(new_colors,widget_config['colors'])

    def test_update_widget_table_failure_non_existent_pid(self):
        ''' update_widget_table should fail if we try to update a pid that does not belong to widget '''
        username='test_update_widget_table_failure_non_existent_pid'
        agentname='test_update_widget_table_failure_non_existent_pid'
        datasourcename='test_update_widget_table_failure_non_existent_pid'
        datapointname='test_update_widget_table_failure_non_existent_pid'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgettablefailurenonexistentpid'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_table_failure_non_existent_pid'
        widget=api.new_widget_table(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.TABLE)
        new_colors={uuid.uuid4():'#ABCDEF'}
        self.assertRaises(exceptions.DatapointNotFoundException, api.update_widget_table, wid=widget['wid'], colors=new_colors)

    def test_update_widget_table_failure_invalid_color(self):
        ''' update_widget_table should fail if we try to update a pid with an invalid color '''
        username='test_update_widget_table_failure_invalid_color'
        agentname='test_update_widget_table_failure_invalid_color'
        datasourcename='test_update_widget_table_failure_invalid_color'
        datapointname='test_update_widget_table_failure_invalid_color'
        email=username+'@komlog.org'
        password='password'
        pubkey='testupdatewidgettablefailureinvalidcolor'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        color=libcolors.get_random_color()
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        widgetname='test_update_widget_table_failure_invalid_color'
        widget=api.new_widget_table(username=username, widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.TABLE)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(len(widget['colors']),1)
        self.assertEqual(widget['type'], types.TABLE)
        colors=[None, 23423, 2323.23423, 'AADDEE','aasd98','#AAcdFP',{'a':'dict'},('a','tuple'),['a','list'],{'set','aset'},uuid.uuid4(), uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex]
        for color in colors:
            new_colors={datapoint['pid']:color}
            self.assertRaises(exceptions.BadParametersException, api.update_widget_table, wid=widget['wid'], colors=new_colors)

