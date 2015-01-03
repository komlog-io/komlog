import unittest
import uuid
from komlibs.general.time import timeuuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi 
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.widget import api, types
from komlibs.gestaccount import exceptions
from komcass.model.orm import widget as ormwidget

class GestaccountWidgetApiTest(unittest.TestCase):
    ''' komlog.gestaccount.widget.api tests '''

    def setUp(self):
        username='test_gestaccount.widget.api_user'
        password='password'
        email='test_gestaccount.widget.api_user@komlog.org'
        self.user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_gestaccount.widget.api_agent'
        pubkey='pubkey'
        version='Test Version'
        self.agent=agentapi.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test_gestaccount.widget.api_datasource'
        self.datasource=datasourceapi.create_datasource(username=self.user.username, aid=self.agent.aid, datasourcename=datasourcename)
        datapointname='test_create_datapoint_success'
        position='1'
        length='1'
        date=timeuuid.uuid1()
        self.datapoint=datapointapi.create_datapoint(did=self.datasource.did,datapointname=datapointname,position=position,length=length, date=date)

    def test_get_widget_config_non_existent_widget(self):
        ''' get_widget_config should fail if wid is not in system '''
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.get_widget_config, wid=wid)

    def test_get_widget_config_success_DS_WIDGET(self):
        ''' get_widget_config should succeed if wid exists and is DS_WIDGET type '''
        widget=api.new_widget_ds(username=self.user.username, did=self.datasource.did) 
        data=api.get_widget_config(wid=widget.wid)
        self.assertEqual(data['type'],types.DS_WIDGET)

    def test_get_widget_config_success_DP_WIDGET(self):
        ''' get_widget_config should succeed if wid exists and is DP_WIDGET type '''
        widget=api.new_widget_dp(username=self.user.username, pid=self.datapoint.pid) 
        data=api.get_widget_config(wid=widget.wid)
        self.assertEqual(data['type'],types.DP_WIDGET)

    def test_get_widgets_config_non_existent_username(self):
        ''' get_widgets_config should fail if username is not in system '''
        username='test_get_widgets_config_non_existent_username'
        self.assertRaises(exceptions.UserNotFoundException, api.get_widgets_config, username=username)

    def test_get_widgets_config_success_no_widgets(self):
        ''' get_widgets_config should succeed if username exists in system '''
        data=api.get_widgets_config(username=self.user.username)
        self.assertIsInstance(data, list)

    def test_get_widgets_config_success_some_widgets(self):
        ''' get_widgets_config should succeed if username exists in system '''
        widget_dp=api.new_widget_dp(username=self.user.username, pid=self.datapoint.pid) 
        widget_ds=api.new_widget_ds(username=self.user.username, did=self.datasource.did) 
        data=api.get_widgets_config(username=self.user.username)
        self.assertIsInstance(data, list)
        self.assertNotEqual(len(data),0)

    def test_delete_widget_non_existent_username(self):
        ''' delete_widget should fail if username is not in system '''
        username='test_delete_widget_non_existent_username'
        wid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.delete_widget, username=username, wid=wid)

    def test_delete_widget_non_existent_widget(self):
        ''' delete_widget should fail if widget is not in system '''
        username=self.user.username
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.delete_widget, username=username, wid=wid)

    def test_delete_widget_ds_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        username=self.user.username
        widget=api.new_widget_ds(username=self.user.username, did=self.datasource.did) 
        self.assertTrue(api.delete_widget(username=username, wid=widget.wid))

    def test_delete_widget_dp_success(self):
        ''' delete_widget should succeed if wid and user exist '''
        username=self.user.username
        widget=api.new_widget_dp(username=self.user.username, pid=self.datapoint.pid) 
        self.assertTrue(api.delete_widget(username=username, wid=widget.wid))

    def test_new_widget_ds_non_existent_username(self):
        ''' new_widget_ds should fail if username does not exist '''
        username='test_new_widget_ds_non_existent_username'
        did=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_ds, username=username, did=did)

    def test_new_widget_ds_non_existent_datasource(self):
        ''' new_widget_ds should fail if datasource does not exist '''
        username=self.user.username
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.new_widget_ds, username=username, did=did)

    def test_new_widget_ds_success(self):
        ''' new_widget_ds should succeed if datasource exists and user too '''
        username=self.user.username
        did=self.datasource.did
        widget=api.new_widget_ds(username=username, did=did)
        self.assertIsInstance(widget, ormwidget.WidgetDs)

    def test_new_widget_dp_non_existent_username(self):
        ''' new_widget_dp should fail if username does not exist '''
        username='test_new_widget_dp_non_existent_username'
        pid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_dp, username=username, pid=pid)

    def test_new_widget_dp_non_existent_datapoint(self):
        ''' new_widget_dp should fail if datapoint does not exist '''
        username=self.user.username
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.new_widget_dp, username=username, pid=pid)

    def test_new_widget_dp_success(self):
        ''' new_widget_dp should succeed if datapoint exists and user too '''
        username=self.user.username
        pid=self.datapoint.pid
        widget=api.new_widget_dp(username=username, pid=pid)
        self.assertIsInstance(widget, ormwidget.WidgetDp)

