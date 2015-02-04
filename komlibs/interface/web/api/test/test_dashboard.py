import unittest
import uuid
import json
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
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

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
        response2=dashboardapi.get_dashboards_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

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

    def test_delete_dashboard_request_failure_no_permission(self):
        ''' delete_dashboard_request should fail if user has no access '''
        username='test_delete_dashboard_request_failure_no_permission'
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_dashboard_request(username=username, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

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

    def test_update_dashboard_config_request_failure_no_permission(self):
        ''' update_dashboard_config_request should fail if user has no access '''
        username='test_update_dashboard_config_request_failure_no_permission'
        bid=uuid.uuid4().hex
        data={'dashboardname':'new_dashboard_name'}
        response=dashboardapi.update_dashboard_config_request(username=username, bid=bid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

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

    def test_add_widget_request_failure_no_access(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        username='test_add_widget_request_failure_no_access'
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
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

    def test_delete_widget_request_failure_no_access(self):
        ''' delete_widget_request should fail if user has no access over bid or wid '''
        username='test_delete_widget_request_failure_no_access'
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(username=username, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

