import unittest
import uuid
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi 
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api, types
from komlog.komlibs.gestaccount.widget import visualization_types as vistypes
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komcass.model.orm import widget as ormwidget
from komlog.komlibs.general.crypto import crypto

class GestaccountWidgetApiTest(unittest.TestCase):
    ''' komlog.gestaccount.widget.api tests '''

    def test_get_widget_config_non_existent_widget(self):
        ''' get_widget_config should fail if wid is not in system '''
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, api.get_widget_config, wid=wid)

    def test_get_widget_config_success_DATASOURCE(self):
        ''' get_widget_config should succeed if wid exists and is DATASOURCE type '''
        username='test_get_widget_config_success_ds_widget_user'
        agentname='test_get_widget_config_success_datasource_agent'
        datasourcename='test_get_widget_config_success_datasource_datasource'
        datapointname='test_get_widget_config_success_datasource_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATASOURCE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['did'],widget['did'])

    def test_get_widget_config_success_DATAPOINT(self):
        ''' get_widget_config should succeed if wid exists and is DATAPOINT type '''
        username='test_get_widget_config_success_dp_widget_user'
        agentname='test_get_widget_config_success_datapoint_agent'
        datasourcename='test_get_widget_config_success_datapoint_datasource'
        datapointname='test_get_widget_config_success_datapoint_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATAPOINT)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['pid'],widget['pid'])

    def test_get_widget_config_success_MULTIDP(self):
        ''' get_widget_config should succeed if wid exists and is MULTIDP type '''
        username='test_get_widget_config_success_multidp_user'
        agentname='test_get_widget_config_success_multidp_agent'
        widgetname='test_get_widget_config_success_multidp_widget'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widgetname)
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)

    def test_get_widgets_config_non_existent_uid(self):
        ''' get_widgets_config should fail if uid is not in system '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.get_widgets_config, uid=uid)

    def test_get_widgets_config_success_no_widgets(self):
        ''' get_widgets_config should succeed if username exists in system '''
        username='test_get_widgets_config_success_no_widgets_user'
        agentname='test_get_widgets_config_success_no_widgets_agent'
        datasourcename='test_get_widgets_config_success_no_widgets_datasource'
        datapointname='test_get_widgets_config_success_no_widgets_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        data=api.get_widgets_config(uid=user['uid'])
        self.assertEqual(data, [])

    def test_get_widgets_config_success_some_widgets(self):
        ''' get_widgets_config should succeed if username exists in system '''
        username='test_get_widgets_config_success_some_widgets_user'
        agentname='test_get_widgets_config_success_some_widgets_agent'
        datasourcename='test_get_widgets_config_success_some_widgets_datasource'
        datapointname='test_get_widgets_config_success_some_widgets_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget_dp=api.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        widget_ds=api.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        data=api.get_widgets_config(uid=user['uid'])
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

    def test_new_widget_datasource_non_existent_username(self):
        ''' new_widget_datasource should fail if username does not exist '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_datasource, uid=uid, did=did)

    def test_new_widget_datasource_non_existent_datasource(self):
        ''' new_widget_datasource should fail if datasource does not exist '''
        username='test_new_widget_datasource_non_existent_datasource_user'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.new_widget_datasource,uid=user['uid'], did=did)

    def test_new_widget_datasource_success(self):
        ''' new_widget_datasource should succeed if datasource exists and user too '''
        username='test_new_widget_datasource_success_user'
        agentname='test_new_widget_datasource_success_agent'
        datasourcename='test_new_widget_datasource_success_datasource'
        datapointname='test_new_widget_datasource_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        uid=user['uid']
        did=datasource['did']
        widget=api.new_widget_datasource(uid=uid, did=did)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['did'], did)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DATASOURCE)
        self.assertEqual(widget['widgetname'],datasourcename)
        self.assertEqual(len(widget.keys()),5)

    def test_new_widget_datapoint_non_existent_username(self):
        ''' new_widget_datapoint should fail if username does not exist '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_datapoint,uid=uid, pid=pid)

    def test_new_widget_datapoint_non_existent_datapoint(self):
        ''' new_widget_datapoint should fail if datapoint does not exist '''
        username='test_new_widget_datapoint_non_existent_datapoint_user'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.new_widget_datapoint,uid=user['uid'], pid=pid)

    def test_new_widget_datapoint_success(self):
        ''' new_widget_datapoint should succeed if datapoint exists and user too '''
        username='test_new_widget_datapoint_success_user'
        agentname='test_new_widget_datapoint_success_agent'
        datasourcename='test_new_widget_datapoint_success_datasource'
        datapointname='test_new_widget_datapoint_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        uid=user['uid']
        pid=datapoint['pid']
        widget=api.new_widget_datapoint(uid=uid, pid=pid)
        self.assertIsInstance(widget, dict)
        self.assertEqual(widget['pid'], pid)
        self.assertEqual(widget['uid'], uid)
        self.assertEqual(widget['type'], types.DATAPOINT)
        self.assertEqual(widget['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(len(widget.keys()),5)

    def test_new_widget_linegraph_failure_invalid_username(self):
        ''' new_widget_linegraph should fail if username is invalid '''
        uids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_new_widget_linegraph_failure_invalid_username'
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_linegraph, uid=uid, widgetname=widgetname)

    def test_new_widget_linegraph_failure_invalid_widgetname(self):
        ''' new_widget_linegraph should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_linegraph, uid=uid, widgetname=widgetname)

    def test_new_widget_linegraph_failure_non_existent_user(self):
        ''' new_widget_linegraph should fail if user does not exist '''
        uid=uuid.uuid4()
        widgetname='test_new_widget_failure_non_existent_user'
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_linegraph, uid=uid, widgetname=widgetname)

    def test_new_widget_linegraph_success(self):
        ''' new_widget_linegraph should succeed if user exists '''
        username='test_new_widget_linegraph_success'
        widgetname='test_new_widget_linegraph_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_linegraph_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_new_widget_linegraph_success_datasource'
        datapointname='test_new_widget_linegraph_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_linegraph_success_datasource'
        datapointname='test_add_datapoint_to_widget_linegraph_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_linegraph_success_datasource'
        datapointname='test_delete_datapoint_from_widget_linegraph_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        uids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_new_widget_table_failure_invalid_username'
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_table, uid=uid, widgetname=widgetname)

    def test_new_widget_table_failure_invalid_widgetname(self):
        ''' new_widget_table should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_table, uid=uid, widgetname=widgetname)

    def test_new_widget_table_failure_non_existent_user(self):
        ''' new_widget_table should fail if user does not exist '''
        uid=uuid.uuid4()
        widgetname='test_new_widget_failure_non_existent_user'
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_table, uid=uid, widgetname=widgetname)

    def test_new_widget_table_success(self):
        ''' new_widget_table should succeed if user exists '''
        username='test_new_widget_table_success'
        widgetname='test_new_widget_table_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_table_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_new_widget_table_success_datasource'
        datapointname='test_new_widget_table_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_table_success_datasource'
        datapointname='test_add_datapoint_to_widget_table_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_table_success_datasource'
        datapointname='test_delete_datapoint_from_widget_table_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        uids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_new_widget_histogram_failure_invalid_username'
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_histogram, uid=uid, widgetname=widgetname)

    def test_new_widget_histogram_failure_invalid_widgetname(self):
        ''' new_widget_histogram should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        for widgetname in widgetnames:
            self.assertRaises(exceptions.BadParametersException, api.new_widget_histogram, uid=uid, widgetname=widgetname)

    def test_new_widget_histogram_failure_non_existent_user(self):
        ''' new_widget_table should fail if user does not exist '''
        uid=uuid.uuid4()
        widgetname='test_new_widget_histogram_failure_invalid_username'
        self.assertRaises(exceptions.UserNotFoundException, api.new_widget_histogram, uid=uid, widgetname=widgetname)

    def test_new_widget_histogram_success(self):
        ''' new_widget_histogram should succeed if user exists '''
        username='test_new_widget_histogram_success'
        widgetname='test_new_widget_histogram_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_histogram_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_new_widget_histogram_success_datasource'
        datapointname='test_new_widget_histogram_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.HISTOGRAM)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['colors'],{})

    def test_new_widget_multidp_failure_invalid_username(self):
        ''' new_widget_multidp should fail if username is invalid '''
        uids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_new_widget_multidp_failure_invalid_username'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.new_widget_multidp(uid=uid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, Errors.E_GWA_NWMP_IU)

    def test_new_widget_multidp_failure_invalid_widgetname(self):
        ''' new_widget_multidp should fail if widgetname is invalid '''
        widgetnames=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        for widgetname in widgetnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.new_widget_multidp(uid=uid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, Errors.E_GWA_NWMP_IWN)

    def test_new_widget_multidp_failure_non_existent_user(self):
        ''' new_widget_multidp should fail if user does not exist '''
        uid=uuid.uuid4()
        widgetname='test_new_widget_failure_non_existent_user'
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            api.new_widget_multidp( uid=uid, widgetname=widgetname)
        self.assertEqual(cm.exception.error, Errors.E_GWA_NWMP_UNF)

    def test_new_widget_multidp_success(self):
        ''' new_widget_multidp should succeed if user exists '''
        username='test_new_widget_multidp_success'
        widgetname='test_new_widget_multidp_success'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_new_widget_multidp_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_new_widget_multidp_success_datasource'
        datapointname='test_new_widget_multidp_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)

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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_histogram_success_datasource'
        datapointname='test_add_datapoint_to_widget_histogram_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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

    def test_add_datapoint_to_widget_success_widget_multidp(self):
        ''' add_datapoint_to_widget should succeed if widget is of type multidp '''
        username='test_add_datapoint_to_widget_success_widget_multidp'
        widgetname='test_add_datapoint_to_widget_success_widget_multidp'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_add_datapoint_to_widget_multidp_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_add_datapoint_to_widget_multidp_success_datasource'
        datapointname='test_add_datapoint_to_widget_multidp_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)

    def test_add_datapoint_to_widget_failure_unsupported_operation(self):
        ''' add_datapoint_to_widget should fail if widget type does not support the operation '''
        username='test_add_datapoint_to_widget_user'
        agentname='test_add_datapoint_to_widget_agent'
        datasourcename='test_add_datapoint_to_widget_datasource'
        datapointname='test_add_datapoint_to_widget_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_histogram_success_datasource'
        datapointname='test_delete_datapoint_from_widget_histogram_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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

    def test_delete_datapoint_from_widget_success_widget_multidp(self):
        ''' delete_datapoint_from_widget should succeed if widget is of type multidp '''
        username='test_delete_datapoint_from_widget_success_widget_multidp'
        widgetname='test_delete_datapoint_from_widget_success_widget_multidp'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_delete_datapoint_from_widget_multidp_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        datasourcename='test_delete_datapoint_from_widget_multidp_success_datasource'
        datapointname='test_delete_datapoint_from_widget_multidp_success_datapoint'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        pid=datapoint['pid']
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],{pid})
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        self.assertTrue(api.delete_datapoint_from_widget(wid=widget['wid'],pid=pid))
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.MULTIDP)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['widgetname'],widget['widgetname'])
        self.assertEqual(data['uid'],widget['uid'])
        self.assertEqual(data['datapoints'],set())
        self.assertEqual(data['active_visualization'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)

    def test_delete_datapoint_from_widget_failure_unsupported_operation(self):
        ''' delete_datapoint_from_widget should fail if widget type does not support the operation '''
        username='test_delete_datapoint_from_widget_user'
        agentname='test_delete_datapoint_from_widget_agent'
        datasourcename='test_delete_datapoint_from_widget_datasource'
        datapointname='test_delete_datapoint_from_widget_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        data=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(data['type'],types.DATASOURCE)
        self.assertEqual(data['wid'],widget['wid'])
        self.assertEqual(data['did'],widget['did'])
        self.assertRaises(exceptions.WidgetUnsupportedOperationException, api.delete_datapoint_from_widget, wid=widget['wid'], pid=datapoint['pid'])

    def test_update_widget_config_failure_invalid_wid(self):
        ''' update_widget_config_should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_datasource_failure_invalid_wid'
        for wid in wids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_widget_config(wid=wid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, Errors.E_GWA_UWC_IW)

    def test_update_widget_config_failure_invalid_colors(self):
        ''' update_widget_config_should fail if colors is invalid '''
        colores=[123123, 12313.1231, ('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        for colors in colores:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_widget_config(wid=wid,colors=colors)
            self.assertEqual(cm.exception.error, Errors.E_GWA_UWC_IC)

    def test_update_widget_config_failure_invalid_active_visualization(self):
        ''' update_widget_config_should fail if active_visualization is invalid '''
        actives=[12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        for active in actives:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_widget_config(wid=wid,active_visualization=active)
            self.assertEqual(cm.exception.error, Errors.E_GWA_UWC_IAV)

    def test_update_widget_config_failure_widget_not_found(self):
        ''' update_widget_config_should fail if active_visualization is invalid '''
        wid=uuid.uuid4()
        widgetname='test_update_widget_config_failure_widget_not_found'
        with self.assertRaises(exceptions.WidgetNotFoundException) as cm:
            api.update_widget_config(wid=wid, widgetname=widgetname)
        self.assertEqual(cm.exception.error, Errors.E_GWA_UWC_WNF)

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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        widget=api.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
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
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widget=api.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], '.'.join((datasourcename,datapointname)))
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
        datasourcename='test_update_widget_histogram_success_datasource'
        datapointname='test_update_widget_histogram_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_histogram_success'
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_histogram_success_only_widgetname_datasource'
        datapointname='test_update_widget_histogram_success_only_widgetname_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_histogram_success_only_widgetname'
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_histogram_success_only_colors_datasource'
        datapointname='test_update_widget_histogram_success_only_colors_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_histogram_success_only_colors'
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_histogram_failure_non_existent_pid_datasource'
        datapointname='test_update_widget_histogram_failure_non_existent_pid_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_histogram_failure_non_existent_pid'
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_histogram_failure_invalid_color_datasource'
        datapointname='test_update_widget_histogram_failure_invalid_color_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_histogram_failure_invalid_color'
        widget=api.new_widget_histogram(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_linegraph_success_datasource'
        datapointname='test_update_widget_linegraph_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_linegraph_success'
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_linegraph_success_only_widgetname_datasource'
        datapointname='test_update_widget_linegraph_success_only_widgetname_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_linegraph_success_only_widgetname'
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_linegraph_success_only_colors_datasource'
        datapointname='test_update_widget_linegraph_success_only_colors_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_linegraph_success_only_colors'
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_linegraph_failure_non_existent_pid_datasource'
        datapointname='test_update_widget_linegraph_failure_non_existent_pid_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_linegraph_failure_non_existent_pid'
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_linegraph_failure_invalid_color_datasource'
        datapointname='test_update_widget_linegraph_failure_invalid_color_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_linegraph_failure_invalid_color'
        widget=api.new_widget_linegraph(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_table_success_datasource'
        datapointname='test_update_widget_table_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_table_success'
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_table_success_only_widgetname_datasource'
        datapointname='test_update_widget_table_success_only_widgetname_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_table_success_only_widgetname'
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_table_success_only_colors_datasource'
        datapointname='test_update_widget_table_success_only_colors_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_table_success_only_colors'
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_table_failure_non_existent_pid_datasource'
        datapointname='test_update_widget_table_failure_non_existent_pid_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_table_failure_non_existent_pid'
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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
        datasourcename='test_update_widget_table_failure_invalid_color_datasource'
        datapointname='test_update_widget_table_failure_invalid_color_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_table_failure_invalid_color'
        widget=api.new_widget_table(uid=user['uid'], widgetname=widgetname)
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

    def test_update_widget_multidp_failure_invalid_wid(self):
        ''' update_widget_multidp should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        widgetname='test_update_widget_multidp_failure_invalid_wid'
        for wid in wids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_widget_multidp(wid=wid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, Errors.E_GWA_UWMP_IW)

    def test_update_widget_multidp_failure_invalid_widgetname(self):
        ''' update_widget_multidp should fail if widgetname is invalid '''
        widgetnames=[123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        for widgetname in widgetnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_widget_multidp(wid=wid, widgetname=widgetname)
            self.assertEqual(cm.exception.error, Errors.E_GWA_UWMP_IWN)

    def test_update_widget_multidp_failure_invalid_colors(self):
        ''' update_widget_multidp should fail if colors is invalid '''
        actives=[12313.1231, ('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4()
        widgetname='test_update_widget_multidp_failure_invalid_visualization'
        for visualization in actives:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_widget_multidp(wid=wid, widgetname=widgetname, active_visualization=visualization)
            self.assertEqual(cm.exception.error, Errors.E_GWA_UWMP_IAV)

    def test_update_widget_multidp_failure_non_existent_wid(self):
        ''' update_widget_multidp should fail if wid does not exist '''
        wid=uuid.uuid4()
        widgetname='test_update_widget_multidp_failure_non_existent_wid'
        with self.assertRaises(exceptions.WidgetNotFoundException) as cm:
            api.update_widget_multidp(wid=wid, widgetname=widgetname)
        self.assertEqual(cm.exception.error, Errors.E_GWA_UWMP_WNF)

    def test_update_widget_multidp_success(self):
        ''' update_widget_multidp should succeed if wid exists and data is correct '''
        username='test_update_widget_multidp_success'
        agentname='test_update_widget_multidp_success'
        datasourcename='test_update_widget_multidp_success_datasource'
        datapointname='test_update_widget_multidp_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_multidp_success'
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertEqual(widget['active_visualization'], vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        self.assertNotEqual(widget['active_visualization'], vistypes.VISUALIZATION_TABLE)
        new_widgetname='A new title for the widget'
        new_visualization=vistypes.VISUALIZATION_TABLE
        self.assertTrue(api.update_widget_multidp(wid=widget['wid'], widgetname=new_widgetname,active_visualization=new_visualization))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])
        self.assertEqual(new_visualization,widget_config['active_visualization'])

    def test_update_widget_multidp_failure_not_available_visualization_type(self):
        ''' update_widget_multidp should fail if we try to set a visualization type not supported '''
        username='test_update_widget_multidp_failure_vis_not_supp'
        agentname='test_update_widget_multidp_failure_vis_not_supp'
        datasourcename='test_update_widget_multidp_failure_vis_not_supp_datasource'
        datapointname='test_update_widget_multidp_failure_vis_not_supp_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='Widgetname does not need to be a uri style'
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertEqual(widget['active_visualization'], vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        new_visualization=11000000
        with self.assertRaises(exceptions.WidgetUnsupportedOperationException) as cm:
            api.update_widget_multidp(wid=widget['wid'], active_visualization=new_visualization)
        self.assertEqual(cm.exception.error, Errors.E_GWA_UWMP_IAVT)

    def test_update_widget_multidp_success_only_widgetname(self):
        ''' update_widget_multidp should succeed if wid exists and data is correct '''
        username='test_update_widget_multidp_success_only_widgetname'
        agentname='test_update_widget_multidp_success_only_widgetname'
        datasourcename='test_update_widget_multidp_success_only_widgetname_datasource'
        datapointname='test_update_widget_multidp_success_only_widgetname_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_multidp success only widgetnames'
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertEqual(widget['active_visualization'], vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        new_widgetname='test_update_widget_multidp success 2'
        self.assertTrue(api.update_widget_multidp(wid=widget['wid'], widgetname=new_widgetname))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_widgetname,widget_config['widgetname'])

    def test_update_widget_multidp_success_only_active_visualization(self):
        ''' update_widget_multidp should succeed if wid exists and data is correct '''
        username='test_update_widget_multidp_success_only_active_visualization'
        agentname='test_update_widget_multidp_success_only_active_visualization'
        datasourcename='test_update_widget_multidp_success_only_active_visualization_datasource'
        datapointname='test_update_widget_multidp_success_only_active_visualization_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        widgetname='test_update_widget_multidp_success_only_active_visualization'
        widget=api.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertTrue(api.add_datapoint_to_widget(wid=widget['wid'],pid=datapoint['pid']))
        widget=api.get_widget_config(wid=widget['wid'])
        self.assertTrue(isinstance(widget['wid'],uuid.UUID))
        self.assertEqual(widget['widgetname'], widgetname)
        self.assertEqual(widget['uid'],user['uid'])
        self.assertEqual(sorted(widget['datapoints']),sorted([datapoint['pid']]))
        self.assertEqual(widget['type'], types.MULTIDP)
        self.assertEqual(widget['active_visualization'], vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        self.assertNotEqual(widget['active_visualization'], vistypes.VISUALIZATION_TABLE)
        new_visualization=vistypes.VISUALIZATION_TABLE
        self.assertTrue(api.update_widget_multidp(wid=widget['wid'], active_visualization=new_visualization))
        widget_config=api.get_widget_config(wid=widget['wid'])
        self.assertEqual(widget['uid'],widget_config['uid'])
        self.assertEqual(widget['wid'],widget_config['wid'])
        self.assertEqual(widget['datapoints'],widget_config['datapoints'])
        self.assertEqual(widget['type'],widget_config['type'])
        self.assertEqual(new_visualization,widget_config['active_visualization'])

    def test_get_related_widgets_failure_invalid_wid(self):
        ''' get_related_widgets should fail if wid is invalid '''
        wids=[None, 123123, 12313.1231, {'a':'dict'},('a','tuple'), ['a','list'],{'set','set1'},uuid.uuid4().hex, uuid.uuid1()]
        for wid in wids: 
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_related_widgets(wid=wid)
            self.assertEqual(cm.exception.error, Errors.E_GWA_GRW_IW)

    def test_get_related_widgets_success(self):
        ''' get_related_widgets should return an array with the related widgets '''
        username='test_get_related_widgets_success_user'
        agentname='test_get_related_widgets_success_agent'
        datasourcename='test_get_related_widgets_success_datasource'
        datapointname='test_get_related_widgets_success_datapoint'
        email=username+'@komlog.org'
        password='password'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        user=userapi.create_user(username=username, password=password, email=email)
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        dswidget=api.new_widget_datasource(uid=user['uid'], did=datasource['did']) 
        wdsdata=api.get_widget_config(wid=dswidget['wid'])
        self.assertEqual(wdsdata['type'],types.DATASOURCE)
        self.assertEqual(wdsdata['wid'],dswidget['wid'])
        self.assertEqual(wdsdata['did'],dswidget['did'])
        dpwidget=api.new_widget_datapoint(uid=user['uid'], pid=datapoint['pid']) 
        wdpdata=api.get_widget_config(wid=dpwidget['wid'])
        self.assertEqual(wdpdata['type'],types.DATAPOINT)
        self.assertEqual(wdpdata['wid'],dpwidget['wid'])
        self.assertEqual(wdpdata['pid'],dpwidget['pid'])
        related=api.get_related_widgets(wid=dpwidget['wid'])
        self.assertEqual(len(related),1)
        self.assertEqual(related[0]['wid'],wdsdata['wid'])
        self.assertEqual(related[0]['type'],wdsdata['type'])
        self.assertEqual(related[0]['widgetname'],wdsdata['widgetname'])

