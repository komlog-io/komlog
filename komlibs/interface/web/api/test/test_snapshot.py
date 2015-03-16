import unittest
import uuid
import json
from komlibs.auth import operations
from komlibs.gestaccount.widget import types
from komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlibs.interface.web.api import user as userapi
from komlibs.interface.web.api import agent as agentapi
from komlibs.interface.web.api import datasource as datasourceapi
from komlibs.interface.web.api import datapoint as datapointapi
from komlibs.interface.web.api import widget as widgetapi
from komlibs.interface.web.api import snapshot as snapshotapi
from komlibs.interface.web.api import circle as circleapi
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.interface.imc.model import messages
from komlibs.interface.imc.api import rescontrol, gestconsole
from komimc import bus, routing
from komimc import api as msgapi


class InterfaceWebApiSnapshotTest(unittest.TestCase):
    ''' komlibs.interface.web.api.snapshot tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        username = 'test_komlibs.interface.web.api.snapshot_user'
        userresponse=userapi.get_user_config_request(username=username)
        if userresponse.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username+'@komlog.org'
            response = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
            userresponse = userapi.get_user_config_request(username=username)
            self.assertEqual(userresponse.status, status.WEB_STATUS_OK)
        self.userinfo=userresponse.data
        agentname='test_komlibs.interface.web.api.snapshot_agent'
        pubkey='TESTKOMLIBSINTERFACEWEBAPISNAPSHOTAGENT'
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            aid=response.data['aid']
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
        userresponse=userapi.get_user_config_request(username=username)
        self.userinfo=userresponse.data
        username_to_share='test_komlibs.interface.web.api.snapshot_user_to_share'
        userresponse=userapi.get_user_config_request(username=username_to_share)
        if userresponse.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username_to_share+'@komlog.org'
            response = userapi.new_user_request(username=username_to_share, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
            userresponse = userapi.get_user_config_request(username=username_to_share)
            self.assertEqual(userresponse.status, status.WEB_STATUS_OK)
        self.userinfo_to_share=userresponse.data

    def test_get_snapshots_config_request_failure_invalid_username(self):
        ''' get_snapshots_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for username in usernames:
            response=snapshotapi.get_snapshots_config_request(username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_snapshots_config_request_failure_non_existent_username(self):
        ''' get_snapshots_config_request should fail if username does not exist '''
        username='test_get_snapshots_config_request_failure_non_existent_username'
        response=snapshotapi.get_snapshots_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_snapshots_config_request_success_no_matter_how_much_snapshots(self):
        ''' get_snapshots_config_request should succeed and return a list '''
        username=self.userinfo['username']
        response=snapshotapi.get_snapshots_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(response.data,list))

    def test_get_snapshot_config_request_failure_invalid_username(self):
        ''' get_snapshot_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        nid=uuid.uuid4().hex
        for username in usernames:
            response=snapshotapi.get_snapshot_config_request(username=username,nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_snapshot_config_request_failure_invalid_nid(self):
        ''' get_snapshot_config_request should fail if nid is invalid '''
        nids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(), uuid.uuid4(), uuid.uuid1().hex]
        username='test_get_snapshot_config_request_failure_invalid_nid'
        for nid in nids:
            response=snapshotapi.get_snapshot_config_request(username=username,nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_snapshot_config_request_failure_non_existent_nid(self):
        ''' get_snapshot_config_request should fail if nid does not exist '''
        nid=uuid.uuid4().hex
        username='test_get_snapshot_config_request_failure_non_existent_nid'
        response=snapshotapi.get_snapshot_config_request(username=username,nid=nid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_snapshot_config_request_success_snapshot_linegraph(self):
        ''' get_snapshot_config_request should succeed  '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_get_snapshot_config_request_success_snapshot_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_get_snapshot_config_request_success_snapshot_linegraph'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_linegraph'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])

    def test_get_snapshot_config_request_success_snapshot_histogram(self):
        ''' get_snapshot_config_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_get_snapshot_config_request_success_snapshot_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_get_snapshot_config_request_success_snapshot_histogram'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_histogram'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])

    def test_get_snapshot_config_request_success_snapshot_table(self):
        ''' get_snapshot_config_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_get_snapshot_config_request_success_snapshot_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_get_snapshot_config_request_success_snapshot_table'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_table'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])

    def test_get_snapshot_config_request_success_snapshot_datasource(self):
        ''' get_snapshot_config_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_snapshot_config_request_success_snapshot_datasource'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['sequence']
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['iseq'],sequence)
        self.assertEqual(response7.data['eseq'],sequence)
        self.assertEqual(response7.data['did'],did)

    def test_get_snapshot_config_request_success_snapshot_datasource_shared_to_circle(self):
        ''' new_snapshot_request should succeed and accesses from circle members granted '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_snapshot_config_request_success_snapshot_datasource_shared_to_circle'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['sequence']
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        #we create a circle with the member username_to_share
        username_to_share=self.userinfo_to_share['username']
        circlename='test_get_snapshot_config_request_success_snapshot_datasource_shared_with_circle'
        circle_response=circleapi.new_users_circle_request(username=username,circlename=circlename,members_list=[username_to_share])
        self.assertEqual(circle_response.status, status.WEB_STATUS_OK)
        cid=circle_response.data['cid']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,cid_list=[cid],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        #username_to_share should have access to the snapshot and datapoints
        response7=snapshotapi.get_snapshot_config_request(username=username_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['its'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['ets'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['did'],did)
        response8=datasourceapi.get_datasource_config_request(username=username_to_share, did=did)
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        self.assertEqual(response8.data['did'],did)
        self.assertEqual(response8.data['datasourcename'],datasourcename)
        response9=datasourceapi.get_datasource_data_request(username=username_to_share, did=did, seq=response7.data['iseq'])
        self.assertEqual(response9.status, status.WEB_STATUS_OK)
        self.assertEqual(response9.data['content'],datasourcecontent)
        self.assertEqual(response9.data['did'],did)
        response9=datasourceapi.get_datasource_data_request(username=username_to_share, did=did)
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        username_to_deny='username_to_deny'
        response10=snapshotapi.get_snapshot_config_request(username=username_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datasourceapi.get_datasource_config_request(username=username_to_deny, did=did)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_snapshot_config_request_success_snapshot_datapoint(self):
        ''' get_snapshot_config_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_snapshot_config_request_success_snapshot_datapoint'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_datapoint'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        pid=None
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                datapointconfig=datapointapi.get_datapoint_config_request(username=username,pid=widget['pid'])
                self.assertEqual(datapointconfig.status,status.WEB_STATUS_OK)
                if datapointconfig.data['datapointname']==datapointname:
                    wid=widget['wid']
                    pid=widget['pid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATAPOINT)
        self.assertEqual(response5.data['widgetname'],datapointname)
        self.assertEqual(response5.data['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'],datapointname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['pid'],pid)

    def test_delete_snapshot_request_failure_invalid_username(self):
        ''' delete_snapshot_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1()]
        nid=uuid.uuid4().hex
        for username in usernames:
            response=snapshotapi.delete_snapshot_request(username=username, nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_snapshot_request_failure_invalid_nid(self):
        ''' delete_snapshot_request should fail if nid is invalid '''
        nids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        username='test_delete_snapshot_request_failure_invalid_nid'
        for nid in nids:
            response=snapshotapi.delete_snapshot_request(username=username, nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_snapshot_request_failure_non_existent_username(self):
        ''' delete_snapshot_request should fail if username does not exist '''
        username='test_delete_snapshot_request_failure_non_existent_username'
        nid=uuid.uuid4().hex
        response=snapshotapi.delete_snapshot_request(username=username, nid=nid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_snapshot_request_failure_non_existent_nid(self):
        ''' delete_snapshot_request should fail if username does not exist '''
        username=self.userinfo['username']
        nid=uuid.uuid4().hex
        response=snapshotapi.delete_snapshot_request(username=username, nid=nid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_snapshot_request_success_snapshot_linegraph(self):
        ''' delete_snapshot_request should succeed and delete the snapshot '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_delete_snapshot_request_success_snapshot_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_snapshot_request_success_snapshot_linegraph'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_linegraph'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8 = snapshotapi.delete_snapshot_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_histogram(self):
        ''' delete_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_delete_snapshot_request_success_snapshot_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_snapshot_request_success_snapshot_histogram'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_histogram'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8 = snapshotapi.delete_snapshot_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_table(self):
        ''' delete_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_delete_snapshot_request_success_snapshot_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_snapshot_request_success_snapshot_table'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_table'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,its=its,user_list=[username_to_share],ets=ets,wid=wid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8 = snapshotapi.delete_snapshot_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_datasource(self):
        ''' delete_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_delete_snapshot_request_success_snapshot_datasource'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['sequence']
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['iseq'],sequence)
        self.assertEqual(response7.data['eseq'],sequence)
        self.assertEqual(response7.data['did'],did)
        response8 = snapshotapi.delete_snapshot_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_datapoint(self):
        ''' delete_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_delete_snapshot_request_success_snapshot_datapoint'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_datapoint'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        pid=None
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                datapointconfig=datapointapi.get_datapoint_config_request(username=username,pid=widget['pid'])
                self.assertEqual(datapointconfig.status,status.WEB_STATUS_OK)
                if datapointconfig.data['datapointname']==datapointname:
                    wid=widget['wid']
                    pid=widget['pid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATAPOINT)
        self.assertEqual(response5.data['widgetname'],datapointname)
        self.assertEqual(response5.data['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response7 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'],datapointname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['pid'],pid)
        response8 = snapshotapi.delete_snapshot_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(username=username, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_new_snapshot_request_failure_invalid_username(self):
        ''' new_snapshot_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        wid=uuid.uuid4().hex
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        username_to_share=self.userinfo_to_share['username']
        for username in usernames:
            response=snapshotapi.new_snapshot_request(username=username, wid=wid,user_list=[username_to_share],seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_invalid_wid(self):
        ''' new_snapshot_request should fail if data is invalid '''
        wids=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        username='test_new_snapshot_request_failure_invalid_wid'
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        username_to_share=self.userinfo_to_share['username']
        for wid in wids:
            response=snapshotapi.new_snapshot_request(username=username, wid=wid, user_list=[username_to_share],seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_no_sequence(self):
        ''' new_snapshot_request should fail if no sequence is passed or is invalid '''
        username=self.userinfo['username']
        wid=uuid.uuid4().hex
        seqs=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(),uuid.uuid4().hex,uuid.uuid1().hex]
        username_to_share=self.userinfo_to_share['username']
        for seq in seqs:
            response=snapshotapi.new_snapshot_request(username=username, wid=wid, user_list=[username_to_share],seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_no_timestamps(self):
        ''' new_snapshot_request should fail if no timestamps are passed or are invalid  '''
        username=self.userinfo['username']
        wid=uuid.uuid4().hex
        tss=[None, ['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(),uuid.uuid4().hex,uuid.uuid1().hex]
        username_to_share=self.userinfo_to_share['username']
        for ts in tss:
            its=ts
            ets=ts
            response=snapshotapi.new_snapshot_request(username=username, wid=wid,user_list=[username_to_share],its=its,ets=ets)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_non_existent_widget(self):
        ''' new_snapshot_request should fail if widget does not exist '''
        username=self.userinfo['username']
        wid=uuid.uuid4().hex
        username_to_share=self.userinfo_to_share['username']
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        response=snapshotapi.new_snapshot_request(username=username, wid=wid,user_list=[username_to_share],seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_linegraph_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the linegraph widget has no datapoints '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_new_snapshot_request_failure_widget_linegraph_has_no_datapoints'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=3
        username_to_share=self.userinfo_to_share['username']
        new_snapshot_resp = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_linegraph(self):
        ''' new_snapshot_request should succeed  '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_new_snapshot_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_new_snapshot_request_success_widget_linegraph'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_linegraph'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']==datapointname:
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        #username_to_share should have access to the snapshot and datapoints
        response7=snapshotapi.get_snapshot_config_request(username=username_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8=datapointapi.get_datapoint_config_request(username=username_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        self.assertEqual(response8.data['pid'],pid)
        self.assertEqual(response8.data['color'],response5.data['datapoints'][0]['color'])
        self.assertEqual(response8.data['datapointname'],datapointname)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2',iseq=response7.data['iseq'],eseq=response7.data['eseq'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        username_to_deny='username_to_deny'
        response10=snapshotapi.get_snapshot_config_request(username=username_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(username=username_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_histogram_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the histogram widget has no datapoints '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_new_snapshot_request_failure_widget_histogram_has_no_datapoints'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        new_snapshot_resp = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_histogram(self):
        ''' new_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_new_snapshot_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_new_snapshot_request_success_widget_histogram'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_histogram'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']==datapointname:
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        #username_to_share should have access to the snapshot and datapoints
        response7=snapshotapi.get_snapshot_config_request(username=username_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8=datapointapi.get_datapoint_config_request(username=username_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        self.assertEqual(response8.data['pid'],pid)
        self.assertEqual(response8.data['color'],response5.data['datapoints'][0]['color'])
        self.assertEqual(response8.data['datapointname'],datapointname)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2',iseq=response7.data['iseq'],eseq=response7.data['eseq'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        username_to_deny='username_to_deny'
        response10=snapshotapi.get_snapshot_config_request(username=username_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(username=username_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_table_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the table widget has no datapoints '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_new_snapshot_request_failure_widget_table_has_no_datapoints'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        new_snapshot_resp = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_table(self):
        ''' new_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        widgetname='test_new_snapshot_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(username=username, data=data)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_new_snapshot_request_success_widget_table'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_table'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']==datapointname:
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=widgetapi.add_datapoint_request(username=username, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],ets=ets,its=its)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        #username_to_share should have access to the snapshot and datapoints
        response7=snapshotapi.get_snapshot_config_request(username=username_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8=datapointapi.get_datapoint_config_request(username=username_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        self.assertEqual(response8.data['pid'],pid)
        self.assertEqual(response8.data['color'],response5.data['datapoints'][0]['color'])
        self.assertEqual(response8.data['datapointname'],datapointname)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2',iseq=response7.data['iseq'],eseq=response7.data['eseq'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        username_to_deny='username_to_deny'
        response10=snapshotapi.get_snapshot_config_request(username=username_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(username=username_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_success_widget_datasource(self):
        ''' new_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_new_snapshot_request_success_widget_datasource'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['sequence']
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        #username_to_share should have access to the snapshot and datapoints
        response7=snapshotapi.get_snapshot_config_request(username=username_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['its'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['ets'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['did'],did)
        response8=datasourceapi.get_datasource_config_request(username=username_to_share, did=did)
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        self.assertEqual(response8.data['did'],did)
        self.assertEqual(response8.data['datasourcename'],datasourcename)
        response9=datasourceapi.get_datasource_data_request(username=username_to_share, did=did, seq=response7.data['iseq'])
        self.assertEqual(response9.status, status.WEB_STATUS_OK)
        self.assertEqual(response9.data['content'],datasourcecontent)
        self.assertEqual(response9.data['did'],did)
        response9=datasourceapi.get_datasource_data_request(username=username_to_share, did=did)
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        username_to_deny='username_to_deny'
        response10=snapshotapi.get_snapshot_config_request(username=username_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datasourceapi.get_datasource_config_request(username=username_to_deny, did=did)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_success_widget_datapoint(self):
        ''' new_snapshot_request should succeed '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_new_snapshot_request_success_widget_datapoint'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_datapoint'
        sequence=datasourcedata.data['sequence']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        pid=None
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                datapointconfig=datapointapi.get_datapoint_config_request(username=username,pid=widget['pid'])
                self.assertEqual(datapointconfig.status,status.WEB_STATUS_OK)
                if datapointconfig.data['datapointname']==datapointname:
                    wid=widget['wid']
                    pid=widget['pid']
        response5=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATAPOINT)
        self.assertEqual(response5.data['widgetname'],datapointname)
        self.assertEqual(response5.data['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.userinfo_to_share['username']
        response6 = snapshotapi.new_snapshot_request(username=username,wid=wid,user_list=[username_to_share],ets=ets,its=its)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        #username_to_share should have access to the snapshot and datapoints
        response7=snapshotapi.get_snapshot_config_request(username=username_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'],datapointname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['pid'],pid)
        response8=datapointapi.get_datapoint_config_request(username=username_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        self.assertEqual(response8.data['pid'],pid)
        self.assertEqual(response8.data['datapointname'],datapointname)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1',end_date='2',iseq=response7.data['iseq'],eseq=response7.data['eseq'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(username=username_to_share, pid=pid, start_date='1', end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        username_to_deny='username_to_deny'
        response10=snapshotapi.get_snapshot_config_request(username=username_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(username=username_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

