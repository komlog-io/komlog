import unittest
import uuid
import json
from base64 import b64encode, b64decode
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.widget import types
from komlog.komlibs.gestaccount.widget import visualization_types as vistypes
from komlog.komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import agent as agentapi
from komlog.komlibs.interface.web.api import datasource as datasourceapi
from komlog.komlibs.interface.web.api import datapoint as datapointapi
from komlog.komlibs.interface.web.api import widget as widgetapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc.api import rescontrol, gestconsole
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi


class InterfaceWebApiWidgetTest(unittest.TestCase):
    ''' komlibs.interface.web.api.widget tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.widget_user'
        self.password = 'password'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        self.passport = passport.get_user_passport(cookie)
        agentname='test_komlibs.interface.web.api.widget_agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
        agents_info=agentapi.get_agents_config_request(passport=self.passport)
        self.agents=agents_info.data
        aid = response.data['aid']
        cookie = {'user':self.username, 'sid':uuid.uuid4().hex, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        self.agent_passport = passport.get_agent_passport(cookie)

    def test_get_widget_config_request_success_widget_ds(self):
        ''' get_widget_config_request should succeed returning the widget_ds config '''
        psp = self.agent_passport
        datasourcename='test_get_widget_config_request_success_widget_ds'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==response.data['did']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.DATASOURCE)
        self.assertEqual(response3.data['widgetname'],datasourcename)
        self.assertEqual(response3.data['did'],response.data['did'])
        self.assertEqual(response3.data['wid'],wid)

    def test_get_widget_config_request_success_widget_linegraph(self):
        ''' get_widget_config_request should succeed returning the widget_linegraph config '''
        psp = self.passport
        widgetname='test_get_widget_config_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.LINEGRAPH and widget['wid']==response.data['wid']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_get_widget_config_request_success_widget_histogram(self):
        ''' get_widget_config_request should succeed returning the widget_histogram config '''
        psp = self.passport
        widgetname='test_get_widget_config_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.HISTOGRAM and widget['wid']==response.data['wid']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_get_widget_config_request_success_widget_table(self):
        ''' get_widget_config_request should succeed returning the widget_table config '''
        psp = self.passport
        widgetname='test_get_widget_config_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.TABLE and widget['wid']==response.data['wid']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_get_widget_config_request_success_widget_multidp(self):
        ''' get_widget_config_request should succeed returning the widget multidp config '''
        psp = self.passport
        widgetname='test_get_widget_config_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.MULTIDP and widget['wid']==response.data['wid']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_get_widget_config_request_failure_invalid_passport(self):
        ''' get_widget_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        wid=uuid.uuid4().hex
        for psp in passports:
            response=widgetapi.get_widget_config_request(passport=psp, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_widget_config_request_failure_invalid_wid(self):
        ''' get_widget_config_request should fail if wid is invalid '''
        wids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for wid in wids:
            response=widgetapi.get_widget_config_request(passport=psp, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_widget_config_request_failure_non_existent_username(self):
        ''' get_widget_config_request should fail if username does not exist '''
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        wid=uuid.uuid4().hex
        response=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGWC_RE.value)

    def test_get_widget_config_request_failure_non_existent_widget(self):
        ''' get_widget_config_request should fail if widget does not exist '''
        psp = self.passport
        wid=uuid.uuid4().hex
        response=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGWC_RE.value)

    def test_get_widget_config_request_failure_no_permission_over_this_widget(self):
        ''' get_widget_config_request should fail if user does not have permission over widget '''
        psp = self.agent_passport
        datasourcename='test_get_widget_config_request_failure_no_permission_over_this_widget_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==Operations.NEW_DATASOURCE or not (msg.params['uid']==psp.uid and msg.params['aid']==psp.aid and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==Operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid:
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
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==Operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid: 
                rescontrol.process_message_RESAUTH(message=msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==response.data['did']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.DATASOURCE)
        self.assertEqual(response3.data['did'],response.data['did'])
        self.assertEqual(response3.data['wid'],wid)
        new_username = 'test_get_widget_config_request_failure_no_permission_over_widget_user'
        password = 'password'
        new_email = new_username+'@komlog.org'
        response = userapi.new_user_request(username=new_username, password=password, email=new_email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response = loginapi.login_request(username=new_username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp2 = passport.get_user_passport(cookie)
        widgetinfo = widgetapi.get_widget_config_request(passport=psp2, wid=wid)
        self.assertEqual(widgetinfo.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(widgetinfo.error,autherrors.E_ARA_AGWC_RE.value)

    def test_get_widgets_config_request_success(self):
        ''' get_widgets_config_request should succeed if username exists and return the widgets config '''
        psp = self.agent_passport
        datasourcename='test_get_widgets_config_request_success'
        response = datasourceapi.new_datasource_request(passport=psp,datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==Operations.NEW_DATASOURCE or not (msg.params['uid']==psp.uid and msg.params['aid']==psp.aid and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=2)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==Operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid:
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
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==Operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid: 
                rescontrol.process_message_RESAUTH(msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response2.data)>=1)
        found=0
        for widget in response2.data:
            if 'did' in widget and widget['did']==response.data['did']:
                found+=1
        self.assertEqual(found,1)

    def test_get_widgets_config_request_failure_invalid_passport(self):
        ''' get_widgets_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=widgetapi.get_widgets_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_widgets_config_request_failure_non_existent_username(self):
        ''' get_widgets_config_request should fail if username does not exist '''
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response=widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GWA_GWSC_UNF.value)

    def test_get_widgets_config_request_success_no_widgets(self):
        ''' get_widgets_config_request should succeed but should return an empty array '''
        username = 'test_get_widgets_config_success_no_widgets'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        response2=widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_delete_widget_request_failure_invalid_passport(self):
        ''' delete_widget_request should fail if username is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4().hex
        for psp in passports:
            response=widgetapi.delete_widget_request(passport=psp, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_invalid_wid(self):
        ''' delete_widget_request should fail if wid is invalid '''
        wids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        for wid in wids:
            response=widgetapi.delete_widget_request(passport=psp, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_no_permission_over_wid(self):
        ''' delete_widget_request should fail if user has no permission over wid '''
        psp = self.passport
        wid=uuid.uuid4().hex
        response=widgetapi.delete_widget_request(passport=psp, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_widget_request_failure_widget_cant_be_deleted(self):
        ''' delete_widget_request should fail if widget cant be deleted (by default DATASOURCE widgets cant be deleted '''
        psp = self.agent_passport
        datasourcename='test_delete_widget_request_success_widget_ds'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==response.data['did']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.DATASOURCE)
        self.assertEqual(response3.data['did'],response.data['did'])
        self.assertEqual(response3.data['wid'],wid)
        response = widgetapi.delete_widget_request(passport=psp, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_widget_request_success_widget_linegraph(self):
        ''' delete_widget should delete the linegraph widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_widget_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        response4=widgetapi.delete_widget_request(passport=psp, wid=wid)
        self.assertEqual(response4.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.DELETE_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response5 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_widget_request_success_widget_histogram(self):
        ''' delete_widget should delete the histogram widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_widget_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        response4=widgetapi.delete_widget_request(passport=psp, wid=wid)
        self.assertEqual(response4.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.DELETE_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response5 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_widget_request_success_widget_table(self):
        ''' delete_widget should delete the table widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_widget_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        response4=widgetapi.delete_widget_request(passport=psp, wid=wid)
        self.assertEqual(response4.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.DELETE_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response5 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_widget_request_success_widget_multidp(self):
        ''' delete_widget should delete the table widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_widget_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        response4=widgetapi.delete_widget_request(passport=psp, wid=wid)
        self.assertEqual(response4.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.DELETE_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response5 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_NOT_FOUND)

    def test_new_widget_request_failure_invalid_passport(self):
        ''' new_widget_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        data={}
        for psp in passports:
            response=widgetapi.new_widget_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_widget_request_failure_invalid_data(self):
        ''' new_widget_request should fail if username is invalid '''
        datas=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame']
        data={}
        psp = self.passport
        for data in datas:
            response=widgetapi.new_widget_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_widget_request_failure_non_existing_user(self):
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        data={'type':'mp', 'widgetname':'widgetname'}
        response=widgetapi.new_widget_request(passport=psp, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GWA_NWMP_UNF.value)

    def test_new_widget_request_failure_no_widget_type(self):
        psp = self.passport
        data={}
        response=widgetapi.new_widget_request(passport=psp, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_widget_request_failure_non_valid_widget_type(self):
        psp = self.passport
        data={'type':'ds'}
        response=widgetapi.new_widget_request(passport=psp, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_widget_request_success_widget_linegraph(self):
        ''' new_widget should create the linegraph widget successfully '''
        psp = self.agent_passport
        widgetname='test_new_widget_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_new_widget_request_success_widget_histogram(self):
        ''' new_widget should create the histogram widget successfully '''
        psp = self.passport
        widgetname='test_new_widget_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_new_widget_request_success_widget_table(self):
        ''' new_widget should create the table widget successfully '''
        psp = self.agent_passport
        widgetname='test_new_widget_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_new_widget_request_success_widget_multidp(self):
        ''' new_widget should create the multidp widget successfully '''
        psp = self.agent_passport
        widgetname='test_new_widget_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)

    def test_add_datapoint_request_failure_invalid_passport(self):
        ''' add_datapoint_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4().hex
        pid=uuid.uuid4().hex
        for psp in passports:
            response=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_datapoint_request_failure_invalid_wid(self):
        ''' add_datapoint_request should fail if wid is invalid '''
        wids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        psp = self.passport
        pid=uuid.uuid4().hex
        for wid in wids:
            response=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_datapoint_request_failure_invalid_pid(self):
        ''' add_datapoint_request should fail if pid is invalid '''
        pids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        psp = self.passport
        wid=uuid.uuid4().hex
        for pid in pids:
            response=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_datapoint_request_failure_non_existent_username(self):
        ''' add_datapoint_request should fail if username does not exist '''
        psp = self.passport
        pid=uuid.uuid4().hex
        wid=uuid.uuid4().hex
        response=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AADPTW_RE.value)

    def test_add_datapoint_request_success_widget_linegraph(self):
        ''' add_datapoint_request should add the datapoint to the linegraph widget successfully '''
        psp = self.agent_passport
        widgetname='test_add_datapoint_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_add_datapoint_request_success_widget_linegraph_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_add_datapoint_request_success_widget_linegraph_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)

    def test_add_datapoint_request_success_widget_histogram(self):
        ''' add_datapoint_request should add the datapoint to the histogram widget successfully '''
        psp = self.agent_passport
        widgetname='test_add_datapoint_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_add_dataopint_request_success_widget_histogram_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_add_datapoint_request_success_widget_histogram_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)

    def test_add_datapoint_request_success_widget_table(self):
        ''' add_datapoint_request should add the datapoint to the table widget successfully '''
        psp = self.agent_passport
        widgetname='test_add_datapoint_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_add_dataopint_request_success_widget_table_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_add_datapoint_request_success_widget_table_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)

    def test_add_datapoint_request_success_widget_multidp(self):
        ''' add_datapoint_request should add the datapoint to the multidp widget successfully '''
        psp = self.agent_passport
        widgetname='test_add_datapoint_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['view'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_add_dataopint_request_success_widget_multidp_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_add_datapoint_request_success_widget_multidp_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.MULTIDP)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0],pid)
        self.assertEqual(response5.data['wid'],wid)

    def test_delete_datapoint_request_failure_invalid_passport(self):
        ''' delete_datapoint_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1()]
        wid=uuid.uuid4().hex
        pid=uuid.uuid4().hex
        for psp in passports:
            response=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_invalid_wid(self):
        ''' delete_datapoint_request should fail if wid is invalid '''
        wids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        psp = self.passport
        pid=uuid.uuid4().hex
        for wid in wids:
            response=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_invalid_pid(self):
        ''' delete_datapoint_request should fail if pid is invalid '''
        pids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        psp = self.passport
        wid=uuid.uuid4().hex
        for pid in pids:
            response=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_non_existent_username(self):
        ''' delete_datapoint_request should fail if username does not exist '''
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        pid=uuid.uuid4().hex
        wid=uuid.uuid4().hex
        response=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADDPFW_RE.value)

    def test_delete_datapoint_request_success_widget_linegraph(self):
        ''' delete_datapoint_request should delete the datapoint from the linegraph widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_datapoint_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_datapoint_request_success_widget_linegraph_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_datapoint_request_success_widget_linegraph_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        response6=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        response7=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['datapoints'],[])
        self.assertEqual(response7.data['wid'],wid)

    def test_delete_datapoint_request_success_widget_histogram(self):
        ''' delete_datapoint_request should delete the datapoint from the histogram widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_datapoint_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_dataopint_request_success_widget_histogram_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_datapoint_request_success_widget_histogram__datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        response6=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        response7=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['datapoints'],[])
        self.assertEqual(response7.data['wid'],wid)

    def test_delete_datapoint_request_success_widget_table(self):
        ''' delete_datapoint_request should delete the datapoint from the table widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_datapoint_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_dataopint_request_success_widget_table_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_datapoint_request_success_widget_table_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        response6=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        response7=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['datapoints'],[])
        self.assertEqual(response7.data['wid'],wid)

    def test_delete_datapoint_request_success_widget_multidp(self):
        ''' delete_datapoint_request should delete the datapoint from the multidp widget successfully '''
        psp = self.agent_passport
        widgetname='test_delete_datapoint_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['view'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_delete_dataopint_request_success_widget_multidp_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_datapoint_request_success_widget_multidp_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.MULTIDP)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0],pid)
        self.assertEqual(response5.data['wid'],wid)
        self.assertEqual(response5.data['view'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        response6=widgetapi.delete_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        response7=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['type'],types.MULTIDP)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['datapoints'],[])
        self.assertEqual(response7.data['wid'],wid)
        self.assertEqual(response7.data['view'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)

    def test_update_widget_config_request_failure_invalid_passport(self):
        ''' update_widget_config_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        wid=uuid.uuid4().hex
        data={}
        for psp in passports:
            response=widgetapi.update_widget_config_request(passport=psp, wid=wid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_widget_config_request_failure_invalid_wid(self):
        ''' update_widget_config_request should fail if wid is invalid '''
        wids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        data={}
        for wid in wids:
            response=widgetapi.update_widget_config_request(passport=psp, wid=wid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_widget_config_request_failure_invalid_data(self):
        ''' update_widget_config_request should fail if wid is invalid '''
        datas=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', {'widgetname':None},{'widgetname':'widgetname','datapoints':[]}, {'colors':{'pid':uuid.uuid4(), 'color':None}},{'view':'hola que tal'}]
        psp = self.passport
        wid=uuid.uuid4().hex
        for data in datas:
            response=widgetapi.update_widget_config_request(passport=psp, wid=wid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_widget_config_request_failure_username_does_not_exist(self):
        ''' update_widget_config_request should fail if wid is invalid '''
        data={'widgetname':'test_update_widget_config_request_failure',
              'colors':[{'pid':uuid.uuid4().hex,'color':'#AAAAAA'}]}
        psp = self.passport
        wid=uuid.uuid4().hex
        response=widgetapi.update_widget_config_request(passport=psp, wid=wid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APWC_RE.value)

    def test_update_widget_config_request_success_widget_histogram(self):
        ''' update_widget_config_request should update successfylly the widget configuration '''
        psp = self.agent_passport
        widgetname='test_update_widget_config_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_update_widget_config_request_success'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_update_widget_config_request_success_widget_histogram'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        new_widgetname='test_update_widget_config_request_success_histogram_widget_2'
        new_color={'pid':pid,'color':'#CCDDEE'}
        data={'widgetname':new_widgetname,'datapoints':[new_color]}
        response6=widgetapi.update_widget_config_request(passport=psp, wid=wid, data=data)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        response7=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],new_widgetname)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':'#CCDDEE'}])
        self.assertEqual(response7.data['wid'],wid)

    def test_update_widget_config_request_success_widget_multidp(self):
        ''' update_widget_config_request should update successfylly the widget configuration '''
        psp = self.agent_passport
        widgetname='test_update_widget_config_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        self.assertEqual(response3.data['view'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        datasourcename='test_update_widget_config_request_success_widget_multidp'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_update_widget_config_request_success_widget_multidp'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.MULTIDP)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0],pid)
        self.assertEqual(response5.data['wid'],wid)
        self.assertEqual(response5.data['view'],vistypes.WIDGET_MULTIDP_DEFAULT_VISUALIZATION)
        new_widgetname='test_update_widget_config_request_success_multidp_widget_2'
        new_view=vistypes.VISUALIZATION_HISTOGRAM
        data={'widgetname':new_widgetname,'view':new_view}
        response6=widgetapi.update_widget_config_request(passport=psp, wid=wid, data=data)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        response7=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['type'],types.MULTIDP)
        self.assertEqual(response7.data['widgetname'],new_widgetname)
        self.assertEqual(len(response7.data['datapoints']),1)
        self.assertEqual(response7.data['datapoints'][0],pid)
        self.assertEqual(response7.data['wid'],wid)
        self.assertEqual(response7.data['view'],vistypes.VISUALIZATION_HISTOGRAM)

    def test_get_related_widgets_request_failure_invalid_passport(self):
        ''' get_related_widgets_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        wid=uuid.uuid4().hex
        for psp in passports:
            response=widgetapi.get_related_widgets_request(passport=psp, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_related_widgets_request_failure_invalid_wid(self):
        ''' get_related_widgets_request should fail if wid is invalid '''
        wids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for wid in wids:
            response=widgetapi.get_related_widgets_request(passport=psp, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_related_widgets_request_failure_non_existent_username(self):
        ''' get_related_widgets_request should fail if username does not exist '''
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        wid=uuid.uuid4().hex
        response=widgetapi.get_related_widgets_request(passport=psp, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGWC_RE.value)

    def test_get_related_widgets_request_failure_non_existent_widget(self):
        ''' get_related_widgets_request should fail if widget does not exist '''
        psp = self.passport
        wid=uuid.uuid4().hex
        response=widgetapi.get_related_widgets_request(passport=psp, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGWC_RE.value)

    def test_get_related_widgets_request_failure_no_permission_over_this_widget(self):
        '''get_related_widgets_request should fail if user does not have permission over widget '''
        psp = self.agent_passport
        datasourcename='test_get_related_widgets_request_failure_no_permission_over_this_widget_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
            if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==Operations.NEW_DATASOURCE or not (msg.params['uid']==psp.uid and msg.params['aid']==psp.aid and msg.params['did']==uuid.UUID(response.data['did'])):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertFalse(count>=1000)
        rescontrol.process_message_UPDQUO(msg)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if not msg:
                break
            if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==Operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid:
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
            if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==Operations.NEW_WIDGET_SYSTEM and msg.params['uid']==psp.uid: 
                rescontrol.process_message_RESAUTH(message=msg)
            else:
                msgapi.send_message(msg)
                count+=1
                if count>=100:
                    break
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==response.data['did']:
                num_widgets+=1
                wid=widget['wid']
        self.assertEqual(num_widgets,1)
        self.assertIsNotNone(wid)
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.DATASOURCE)
        self.assertEqual(response3.data['did'],response.data['did'])
        self.assertEqual(response3.data['wid'],wid)
        new_username = 'test_get_related_widgets_request_failure_no_permission_over_widget_user'
        password = 'password'
        new_email = new_username+'@komlog.org'
        response = userapi.new_user_request(username=new_username, password=password, email=new_email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response = loginapi.login_request(username=new_username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp2 = passport.get_user_passport(cookie)
        widgetrelated = widgetapi.get_related_widgets_request(passport=psp2, wid=wid)
        self.assertEqual(widgetrelated.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(widgetrelated.error , autherrors.E_ARA_AGWC_RE.value)

    def test_get_related_widgets_request_success(self):
        ''' get_releated_widgets_request should succeed '''
        psp = self.agent_passport
        widgetname='test_get_related_widgets_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_get_related_widgets_requests_success_datasource'
        response = datasourceapi.new_datasource_request(passport=psp, datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
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
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_related_widgets_request_success_datapoint'
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
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
        msg_addr=routing.get_address(type=messages.NEW_DP_WIDGET_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
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
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        wid_dp=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
                wid_dp=widget['wid']
        self.assertTrue(num_widgets==1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        response6=widgetapi.get_related_widgets_request(passport=psp, wid=wid_dp)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response6.data),2)


