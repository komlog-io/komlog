import unittest
import uuid
import json
from komlibs.auth import operations
from komlibs.gestaccount.widget import types
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.api import agent as agentapi 
from komlibs.interface.web.api import datasource as datasourceapi 
from komlibs.interface.web.api import widget as widgetapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions
from komlibs.general.validation import arguments as args
from komlibs.interface.imc.model import messages
from komlibs.interface.imc.api import rescontrol, gestconsole
from komimc import bus, routing
from komimc import api as msgapi


class InterfaceWebApiWidgetTest(unittest.TestCase):
    ''' komlibs.interface.web.api.widget tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        username = 'test_komlibs.interface.web.api.widget_user'
        userresponse=userapi.get_user_config_request(username=username)
        if userresponse.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username+'@komlog.org'
            response = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            userresponse = userapi.get_user_config_request(username=username)
            self.assertEqual(userresponse.status, status.WEB_STATUS_OK)
        self.userinfo=userresponse.data
        agentname='test_komlibs.interface.web.api.widget_agent'
        pubkey='TESTKOMLIBSINTERFACEWEBAPIWIDGETAGENT'
        version='test library vX.XX'
        response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            aid=response.data['aid']
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response.data['aid'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
                self.assertIsNotNone(msg)
                if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response.data['aid'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_RESAUTH(msg)
        userresponse=userapi.get_user_config_request(username=username)
        self.userinfo=userresponse.data

    def test_get_widget_config_request_success_widget_ds(self):
        ''' get_widget_config_request should succeed returning the widget_ds config '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_widget_config_request_success_widget_ds'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_DS_WIDGET_MESSAGE or msg.did.hex!=response.data['did']:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        msg_result=gestconsole.process_message_NEWDSW(message=msg)
        msgapi.process_msg_result(msg_result)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_RESAUTH(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                rescontrol.process_message_UPDQUO(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                rescontrol.process_message_RESAUTH(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DS_WIDGET and widget['did']==response.data['did']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.DS_WIDGET)
        self.assertEqual(response3.data['did'],response.data['did'])
        self.assertEqual(response3.data['wid'],wid)

    def test_get_widget_config_request_failure_invalid_username(self):
        ''' get_widget_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        wid=uuid.uuid4().hex
        for username in usernames:
            response=widgetapi.get_widget_config_request(username=username, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_widget_config_request_failure_invalid_wid(self):
        ''' get_widget_config_request should fail if wid is invalid '''
        wids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_get_widget_config_request_failure_invalid_wid'
        for wid in wids:
            response=widgetapi.get_widget_config_request(username=username, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_widget_config_request_failure_non_existent_username(self):
        ''' get_widget_config_request should fail if username does not exist '''
        username='test_get_widget_config_request_failure_non_existent_username'
        wid=uuid.uuid4().hex
        response=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_widget_config_request_failure_non_existent_widget(self):
        ''' get_widget_config_request should fail if widget does not exist '''
        username=self.userinfo['username']
        wid=uuid.uuid4().hex
        response=widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_widget_config_request_failure_no_permission_over_this_widget(self):
        ''' get_widget_config_request should fail if user does not have permission over widget '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_widget_config_request_success_widget_ds'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_DS_WIDGET_MESSAGE or msg.did.hex!=response.data['did']:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        msg_result=gestconsole.process_message_NEWDSW(message=msg)
        msgapi.process_msg_result(msg_result)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            self.assertIsNotNone(msg)
            if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_RESAUTH(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                rescontrol.process_message_UPDQUO(message=msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                rescontrol.process_message_RESAUTH(message=msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DS_WIDGET and widget['did']==response.data['did']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(username=username, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.DS_WIDGET)
        self.assertEqual(response3.data['did'],response.data['did'])
        self.assertEqual(response3.data['wid'],wid)
        new_username = 'test_get_widget_config_request_failure_no_permission_over_widget_user'
        password = 'password'
        new_email = new_username+'@komlog.org'
        response = userapi.new_user_request(username=new_username, password=password, email=new_email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        widgetinfo = widgetapi.get_widget_config_request(username=new_username, wid=wid)
        self.assertEqual(widgetinfo.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(widgetinfo.data, None)

    def test_get_widgets_config_request_success(self):
        ''' get_widgets_config_request should succeed if username exists and return the widgets config '''
        username=self.userinfo['username']
        aid=self.userinfo['agents'][0]['aid']
        datasourcename='test_get_widget_config_request_success_widget_ds'
        response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_DS_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_DS_WIDGET_MESSAGE or msg.did.hex!=response.data['did']:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        msg_result=gestconsole.process_message_NEWDSW(message=msg)
        msgapi.process_msg_result(msg_result)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_RESAUTH(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                rescontrol.process_message_UPDQUO(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                rescontrol.process_message_RESAUTH(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response2.data)>=1)
        found=0
        for widget in response2.data:
            if 'did' in widget and widget['did']==response.data['did']:
                found+=1
        self.assertEqual(found,1)

    def test_get_widgets_config_request_failure_invalid_username(self):
        ''' get_widgets_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for username in usernames:
            response=widgetapi.get_widgets_config_request(username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_widgets_config_request_failure_non_existent_username(self):
        ''' get_widgets_config_request should fail if username does not exist '''
        username='test_get_widgets_config_request_failure_non_existent_username'
        response=widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_widgets_config_request_success_no_widgets(self):
        ''' get_widgets_config_request should succeed but should return an empty array '''
        username = 'test_get_widgets_config_success_no_widgets'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response2=widgetapi.get_widgets_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_delete_widget_request_failure_invalid_username(self):
        ''' delete_widget_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4().hex
        for username in usernames:
            response=widgetapi.delete_widget_request(username=username, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_invalid_wid(self):
        ''' delete_widget_request should fail if wid is invalid '''
        wids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_widget_request_failure_invalid_wid'
        for wid in wids:
            response=widgetapi.delete_widget_request(username=username, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

