import unittest
import uuid
import json
from komimc import bus, routing
from komimc import api as msgapi
from komlibs.interface.imc.model import messages
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.api import dashboard as dashboardapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions


class InterfaceWebApiDashboardTest(unittest.TestCase):
    ''' komlibs.interface.web.api.dashboard tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        username = 'test_komlibs.interface.web.api.dashboard_user'
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

    def test_get_dashboard_config_request_failure_invalid_username(self):
        ''' get_dashboard_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        bid=uuid.uuid4().hex
        for username in usernames:
            response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_dashboard_config_request_failure_invalid_bid(self):
        ''' get_dashboard_config_request should fail if bid is invalid '''
        bids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_get_dashboard_config_request_failure_invalid_bid'
        for bid in bids:
            response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_dashboard_config_request_failure_non_existent_username(self):
        ''' get_dashboard_config_request should fail if username does not exist '''
        username='test_get_dashboard_config_request_failure_non_existent_username'
        bid=uuid.uuid4().hex
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_dashboard_config_request_success(self):
        ''' get_dashboard_config_request should return the dashboard info '''
        username=self.userinfo['username']
        dashboardname='test_get_dashboard_config_request_success'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

    def test_get_dashboard_config_request_failure_non_existent_dashboard(self):
        ''' get_dashboard_config_request should fail if dashboard does not exist '''
        username=self.userinfo['username']
        bid=uuid.uuid4().hex
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_dashboards_config_request_failure_invalid_username(self):
        ''' get_dashboards_config_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for username in usernames:
            response=dashboardapi.get_dashboards_config_request(username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_dashboards_config_request_failure_non_existent_username(self):
        ''' get_dashboards_config_request should fail if username does not exist '''
        username='test_get_dashboards_config_request_failure_non_existent_username'
        response=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_dashboards_config_request_success_no_dashboards(self):
        ''' get_dashboards_config_request should succeed but should return an empty array '''
        username = 'test_get_dashboards_config_success_no_dashboards'
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
        response2=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_get_dashboards_config_request_success_some_dashboards(self):
        ''' get_dashboard_config_request should return the dashboard info '''
        username = 'test_get_dashboards_config_request_success_some_dashboards'
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
        response2=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])
        dashboardname='test_get_dashboard_config_request_success'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        dashboard1=response.data
        dashboardname='test_get_dashboard_config_request_success_2'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        dashboard2=response.data
        response=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        count=0
        for data in response.data:
            count+=1
            if data['bid']==dashboard1['bid']:
                self.assertEqual(data['bid'],dashboard1['bid'])
                self.assertEqual(data['dashboardname'],dashboard1['dashboardname'])
                self.assertEqual(data['wids'],dashboard1['wids'])
            elif data['bid']==dashboard2['bid']:
                self.assertEqual(data['bid'],dashboard2['bid'])
                self.assertEqual(data['dashboardname'],dashboard2['dashboardname'])
                self.assertEqual(data['wids'],dashboard2['wids'])
        self.assertEqual(count,2)

    def test_delete_dashboard_request_failure_invalid_username(self):
        ''' delete_dashboard_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        for username in usernames:
            response=dashboardapi.delete_dashboard_request(username=username, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_dashboard_request_failure_invalid_bid(self):
        ''' delete_dashboard_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_dashboard_request_failure_invalid_bid'
        for bid in bids:
            response=dashboardapi.delete_dashboard_request(username=username, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_dashboard_request_failure_non_existent_user(self):
        ''' delete_dashboard_request should fail if user does not exist '''
        username='test_delete_dashboard_request_failure_no_permission'
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_dashboard_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_dashboard_request_success(self):
        ''' delete_dashboard_request should delete the dashboard info '''
        username = 'test_delete_dashboard_request_success'
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
        response2=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])
        dashboardname='test_delete_dashboard_request_success_1'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        dashboard1=response.data
        dashboardname='test_delete_dashboard_request_success_2'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        dashboard2=response.data
        response=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        count=0
        for data in response.data:
            count+=1
            if data['bid']==dashboard1['bid']:
                self.assertEqual(data['bid'],dashboard1['bid'])
                self.assertEqual(data['dashboardname'],dashboard1['dashboardname'])
                self.assertEqual(data['wids'],dashboard1['wids'])
            elif data['bid']==dashboard2['bid']:
                self.assertEqual(data['bid'],dashboard2['bid'])
                self.assertEqual(data['dashboardname'],dashboard2['dashboardname'])
                self.assertEqual(data['wids'],dashboard2['wids'])
        self.assertEqual(count,2)
        response=dashboardapi.delete_dashboard_request(username=username, bid=dashboard1['bid'])
        self.assertTrue(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.DELETE_DASHBOARD_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        count=0
        for data in response.data:
            count+=1
            if data['bid']==dashboard2['bid']:
                self.assertEqual(data['bid'],dashboard2['bid'])
                self.assertEqual(data['dashboardname'],dashboard2['dashboardname'])
        self.assertEqual(count,1)
        response=dashboardapi.get_dashboard_config_request(username=username, bid=dashboard1['bid'])
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_update_dashboard_config_request_failure_invalid_username(self):
        ''' update_dashboard_config_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        data={'dashboardname':'new_dashboard_name'}
        for username in usernames:
            response=dashboardapi.update_dashboard_config_request(username=username, bid=bid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_dashboard_config_request_failure_invalid_bid(self):
        ''' update_dashboard_config_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_update_dashboard_config_request_failure_invalid_bid'
        data={'dashboardname':'new_dashboard_name'}
        for bid in bids:
            response=dashboardapi.update_dashboard_config_request(username=username, bid=bid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_dashboard_config_request_failure_invalid_data(self):
        ''' update_dashboard_config_request should fail if data is invalid '''
        datas=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        username='test_update_dashboard_config_request_failure_invalid_data'
        for data in datas:
            response=dashboardapi.update_dashboard_config_request(username=username, bid=bid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_dashboard_config_request_failure_non_existent_user(self):
        ''' update_dashboard_config_request should fail if user does not exist '''
        username='test_update_dashboard_config_request_failure_no_permission'
        bid=uuid.uuid4().hex
        data={'dashboardname':'new_dashboard_name'}
        response=dashboardapi.update_dashboard_config_request(username=username, bid=bid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_update_dashboard_config_request_success(self):
        ''' update_dashboard_config_request should succeed '''
        username=self.userinfo['username']
        dashboardname='test_update_dashboard_config_request_success'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        new_dashboardname='test_update_dashboard_config_request_success_new_dashboardname'
        data={'dashboardname':new_dashboardname}
        response=dashboardapi.update_dashboard_config_request(username=username, bid=bid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],new_dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

    def test_add_widget_request_failure_invalid_username(self):
        ''' add_widget_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        wid=uuid.uuid4().hex
        for username in usernames:
            response=dashboardapi.add_widget_request(username=username, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_widget_request_failure_invalid_bid(self):
        ''' add_widget_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_add_widget_request_failure_invalid_bid'
        wid=uuid.uuid4().hex
        for bid in bids:
            response=dashboardapi.add_widget_request(username=username, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_widget_request_failure_invalid_wid(self):
        ''' add_widget_request should fail if wid is invalid '''
        wids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_add_widget_request_failure_invalid_bid'
        bid=uuid.uuid4().hex
        for wid in wids:
            response=dashboardapi.add_widget_request(username=username, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_widget_request_failure_non_existing_username(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        username='test_add_widget_request_failure_no_access'
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.add_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_add_widget_request_failure_no_existing_bid(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        username=self.userinfo['username']
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.add_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_add_widget_request_failure_no_existing_wid(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        username=self.userinfo['username']
        dashboardname='test_add_widget_request_failure_no_existing_wid'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        wid=uuid.uuid4().hex
        response=dashboardapi.add_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_widget_request_failure_invalid_username(self):
        ''' delete_widget_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        wid=uuid.uuid4().hex
        for username in usernames:
            response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_invalid_bid(self):
        ''' delete_widget_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_widget_request_failure_invalid_bid'
        wid=uuid.uuid4().hex
        for bid in bids:
            response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_invalid_wid(self):
        ''' delete_widget_request should fail if wid is invalid '''
        wids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_widget_request_failure_invalid_bid'
        bid=uuid.uuid4().hex
        for wid in wids:
            response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_non_existent_user(self):
        ''' delete_widget_request should fail if user has no access over bid or wid '''
        username='test_delete_widget_request_failure_no_access'
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_widget_request_failure_no_existing_bid(self):
        ''' delete_widget_request should fail if user has no access over bid '''
        username=self.userinfo['username']
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_widget_request_success_no_previous_widgets(self):
        ''' delete_widget_request should succeed even if dashboard has no previous widgets '''
        username=self.userinfo['username']
        dashboardname='test_delete_widget_request_success_no_previous_widgets'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        wid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

    def test_new_dashboard_request_failure_invalid_username(self):
        ''' new_dashboard_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        dashboardname='test_new_dashboard_request_failure_invalid_username'
        for username in usernames:
            response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_dashboard_request_failure_invalid_dashboardname(self):
        ''' new_dashboard_request should fail if username is invalid '''
        dashboardnames=['userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_new_dashboard_request_failure_invalid_dashboardname'
        for dashboardname in dashboardnames:
            response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_dashboard_request_failure_non_existent_user(self):
        ''' new_dashboard_request should fail if user does not exist '''
        username='test_new_dashboard_request_failure_non_existent_user'
        dashboardname='test_new_dashboard_request_failure_non_existent_user'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_new_dashboard_request_success(self):
        ''' new_dashboard_request should fail if user does not exist '''
        username=self.userinfo['username']
        dashboardname='test_new_dashboard_request_success'
        response=dashboardapi.new_dashboard_request(username=username, dashboardname=dashboardname)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=dashboardapi.get_dashboard_config_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

