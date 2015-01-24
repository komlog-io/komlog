import unittest
import uuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi 
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api, types
from komlibs.gestaccount import exceptions
from komcass.model.orm import widget as ormwidget

class GestaccountWidgetApiTest(unittest.TestCase):
    ''' komlog.gestaccount.widget.api tests '''

    def test_get_widget_config_non_existent_widget(self):
        ''' get_widget_config should fail if wid is not in system '''
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.get_widget_config, wid=wid)

    def test_get_widget_config_success_DS_WIDGET(self):
        ''' get_widget_config should succeed if wid exists and is DS_WIDGET type '''
        username='test_get_widget_config_success_ds_widget_user'
        agentname='test_get_widget_config_success_DS_WIDGET_agent'
        datasourcename='test_get_widget_config_success_DS_WIDGET_datasource'
        datapointname='test_get_widget_config_success_DS_WIDGET_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetconfigsuccessDSWIDGETpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname)
        widget=api.new_widget_ds(username=user['username'], did=datasource['did']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DS_WIDGET)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['did'],widget['did'])

    def test_get_widget_config_success_DP_WIDGET(self):
        ''' get_widget_config should succeed if wid exists and is DP_WIDGET type '''
        username='test_get_widget_config_success_dp_widget_user'
        agentname='test_get_widget_config_success_DP_WIDGET_agent'
        datasourcename='test_get_widget_config_success_DP_WIDGET_datasource'
        datapointname='test_get_widget_config_success_DP_WIDGET_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testgetwidgetconfigsuccessDPWIDGETpubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname)
        widget=api.new_widget_dp(username=user['username'], pid=datapoint['pid']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DP_WIDGET)
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
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname)
        widget_dp=api.new_widget_dp(username=user['username'], pid=datapoint['pid']) 
        widget_ds=api.new_widget_ds(username=user['username'], did=datasource['did']) 
        data=api.get_widgets_config(username=user['username'])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data),2)
        for widget in data:
            if widget['type']==types.DS_WIDGET:
                self.assertEqual(widget['wid'],widget_ds['wid'])
                self.assertEqual(widget['did'],widget_ds['did'])
                self.assertEqual(widget['type'],widget_ds['type'])
            else:
                self.assertEqual(widget['wid'],widget_dp['wid'])
                self.assertEqual(widget['pid'],widget_dp['pid'])
                self.assertEqual(widget['type'],widget_dp['type'])

    def test_delete_widget_non_existent_username(self):
        ''' delete_widget should fail if username is not in system '''
        username='test_delete_widget_non_existent_username'
        wid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.delete_widget, username=username, wid=wid)

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
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, username=username, wid=wid)

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
        widget=api.new_widget_ds(username=username, did=datasource['did']) 
        self.assertTrue(api.delete_widget(username=username, wid=widget['wid']))
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, username=username, wid=widget['wid'])

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
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname)
        widget=api.new_widget_dp(username=username, pid=datapoint['pid']) 
        self.assertTrue(api.delete_widget(username=username, wid=widget['wid']))
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, username=username, wid=widget['wid'])

    def test_new_widget_ds_non_existent_username(self):
        ''' new_widget_ds should fail if username does not exist '''
        username='test_new_widget_ds_non_existent_username'
        did=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_ds, username=username, did=did)

    def test_new_widget_ds_non_existent_datasource(self):
        ''' new_widget_ds should fail if datasource does not exist '''
        username='test_new_widget_ds_non_existent_datasource_user'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.new_widget_ds, username=username, did=did)

    def test_new_widget_ds_success(self):
        ''' new_widget_ds should succeed if datasource exists and user too '''
        username='test_new_widget_ds_success_user'
        agentname='test_new_widget_ds_success_agent'
        datasourcename='test_new_widget_ds_success_datasource'
        datapointname='test_new_widget_ds_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testnewwidgetdssuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        uid=user['uid']
        did=datasource['did']
        widget=api.new_widget_ds(username=username, did=did)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], did)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DS_WIDGET)
        self.assertEqual(len(widget.keys()),4)

    def test_new_widget_dp_non_existent_username(self):
        ''' new_widget_dp should fail if username does not exist '''
        username='test_new_widget_dp_non_existent_username'
        pid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_dp, username=username, pid=pid)

    def test_new_widget_dp_non_existent_datapoint(self):
        ''' new_widget_dp should fail if datapoint does not exist '''
        username='test_new_widget_dp_non_existent_datapoint_user'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.new_widget_dp, username=username, pid=pid)

    def test_new_widget_dp_success(self):
        ''' new_widget_dp should succeed if datapoint exists and user too '''
        username='test_new_widget_dp_success_user'
        agentname='test_new_widget_dp_success_agent'
        datasourcename='test_new_widget_dp_success_datasource'
        datapointname='test_new_widget_dp_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey='testnewwidgetdpsuccesspubkey'
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(username=user['username'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(username=user['username'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname)
        uid=user['uid']
        pid=datapoint['pid']
        widget=api.new_widget_dp(username=username, pid=pid)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], pid)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DP_WIDGET)
        self.assertEqual(len(widget.keys()),4)

