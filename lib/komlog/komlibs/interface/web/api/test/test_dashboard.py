import unittest
import uuid
import json
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.auth import passport
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.web.api import login as loginapi 
from komlog.komlibs.interface.web.api import user as userapi 
from komlog.komlibs.interface.web.api import dashboard as dashboardapi 
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions


class InterfaceWebApiDashboardTest(unittest.TestCase):
    ''' komlibs.interface.web.api.dashboard tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        self.username = 'test_komlibs.interface.web.api.dashboard_user'
        self.password = 'password'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            for msg in response.imc_messages['unrouted']:
                if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                    code = msg.code
                    userapi.confirm_user_request(email=email, code=code)
            for msg in response.imc_messages['unrouted']:
                msgresponse=msgapi.process_message(msg)
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        self.passport = passport.get_user_passport(cookie)

    def test_get_dashboard_config_request_failure_invalid_passport(self):
        ''' get_dashboard_config_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        bid=uuid.uuid4().hex
        for psp in passports:
            response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_dashboard_config_request_failure_invalid_bid(self):
        ''' get_dashboard_config_request should fail if bid is invalid '''
        bids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for bid in bids:
            response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_dashboard_config_request_failure_non_existent_username(self):
        ''' get_dashboard_config_request should fail if username does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        bid=uuid.uuid4().hex
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGDBC_RE.value)

    def test_get_dashboard_config_request_success(self):
        ''' get_dashboard_config_request should return the dashboard info '''
        psp = self.passport
        dashboardname='test_get_dashboard_config_request_success'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

    def test_get_dashboard_config_request_failure_non_existent_dashboard(self):
        ''' get_dashboard_config_request should fail if dashboard does not exist '''
        psp = self.passport
        bid=uuid.uuid4().hex
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_dashboards_config_request_failure_invalid_passport(self):
        ''' get_dashboards_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=dashboardapi.get_dashboards_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_dashboards_config_request_failure_non_existent_username(self):
        ''' get_dashboards_config_request should fail if username does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response=dashboardapi.get_dashboards_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_dashboards_config_request_success_no_dashboards(self):
        ''' get_dashboards_config_request should succeed but should return an empty array '''
        username = 'test_get_dashboards_config_success_no_dashboards'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.imc_messages['unrouted']:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        response2=dashboardapi.get_dashboards_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])

    def test_get_dashboards_config_request_success_some_dashboards(self):
        ''' get_dashboard_config_request should return the dashboard info '''
        username = 'test_get_dashboards_config_request_success_some_dashboards'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.imc_messages['unrouted']:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        response2=dashboardapi.get_dashboards_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])
        dashboardname='test_get_dashboard_config_request_success'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        dashboard1=response.data
        dashboardname='test_get_dashboard_config_request_success_2'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        dashboard2=response.data
        response=dashboardapi.get_dashboards_config_request(passport=psp)
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

    def test_delete_dashboard_request_failure_invalid_passport(self):
        ''' delete_dashboard_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        for psp in passports:
            response=dashboardapi.delete_dashboard_request(passport=psp, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_dashboard_request_failure_invalid_bid(self):
        ''' delete_dashboard_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        for bid in bids:
            response=dashboardapi.delete_dashboard_request(passport=psp, bid=bid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_dashboard_request_failure_non_existent_user(self):
        ''' delete_dashboard_request should fail if user does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_dashboard_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADDB_RE.value)

    def test_delete_dashboard_request_success(self):
        ''' delete_dashboard_request should delete the dashboard info '''
        username = 'test_delete_dashboard_request_success'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        for msg in response.imc_messages['unrouted']:
            if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                code = msg.code
                userapi.confirm_user_request(email=email, code=code)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            #self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response = loginapi.login_request(username=username, password=password)
        cookie=getattr(response, 'cookie',None)
        psp = passport.get_user_passport(cookie)
        response2=dashboardapi.get_dashboards_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response2.data, [])
        dashboardname='test_delete_dashboard_request_success_1'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        dashboard1=response.data
        dashboardname='test_delete_dashboard_request_success_2'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        dashboard2=response.data
        response=dashboardapi.get_dashboards_config_request(passport=psp)
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
        response=dashboardapi.delete_dashboard_request(passport=psp, bid=dashboard1['bid'])
        self.assertTrue(response.status, status.WEB_STATUS_RECEIVED)
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboards_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        count=0
        for data in response.data:
            count+=1
            if data['bid']==dashboard2['bid']:
                self.assertEqual(data['bid'],dashboard2['bid'])
                self.assertEqual(data['dashboardname'],dashboard2['dashboardname'])
        self.assertEqual(count,1)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=dashboard1['bid'])
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_update_dashboard_config_request_failure_invalid_passport(self):
        ''' update_dashboard_config_request should fail if username is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        data={'dashboardname':'new_dashboard_name'}
        for psp in passports:
            response=dashboardapi.update_dashboard_config_request(passport=psp, bid=bid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_dashboard_config_request_failure_invalid_bid(self):
        ''' update_dashboard_config_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        data={'dashboardname':'new_dashboard_name'}
        for bid in bids:
            response=dashboardapi.update_dashboard_config_request(passport=psp, bid=bid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_dashboard_config_request_failure_invalid_data(self):
        ''' update_dashboard_config_request should fail if data is invalid '''
        datas=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        psp = self.passport
        for data in datas:
            response=dashboardapi.update_dashboard_config_request(passport=psp, bid=bid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_dashboard_config_request_failure_non_existent_user(self):
        ''' update_dashboard_config_request should fail if user does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        bid=uuid.uuid4().hex
        data={'dashboardname':'new_dashboard_name'}
        response=dashboardapi.update_dashboard_config_request(passport=psp, bid=bid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDBC_RE.value)

    def test_update_dashboard_config_request_success(self):
        ''' update_dashboard_config_request should succeed '''
        psp = self.passport
        dashboardname='test_update_dashboard_config_request_success'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        new_dashboardname='test_update_dashboard_config_request_success_new_dashboardname'
        data={'dashboardname':new_dashboardname}
        response=dashboardapi.update_dashboard_config_request(passport=psp, bid=bid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],new_dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

    def test_add_widget_request_failure_invalid_passport(self):
        ''' add_widget_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        wid=uuid.uuid4().hex
        for psp in passports:
            response=dashboardapi.add_widget_request(passport=psp, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_widget_request_failure_invalid_bid(self):
        ''' add_widget_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        wid=uuid.uuid4().hex
        for bid in bids:
            response=dashboardapi.add_widget_request(passport=psp, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_widget_request_failure_invalid_wid(self):
        ''' add_widget_request should fail if wid is invalid '''
        wids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        bid=uuid.uuid4().hex
        for wid in wids:
            response=dashboardapi.add_widget_request(passport=psp, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_widget_request_failure_non_existing_username(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.add_widget_request(passport=psp, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AAWTDB_RE.value)

    def test_add_widget_request_failure_no_existing_bid(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        psp = self.passport
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.add_widget_request(passport=psp, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AAWTDB_RE.value)

    def test_add_widget_request_failure_no_existing_wid(self):
        ''' add_widget_request should fail if user has no access over bid or wid '''
        psp = self.passport
        dashboardname='test_add_widget_request_failure_no_existing_wid'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        wid=uuid.uuid4().hex
        response=dashboardapi.add_widget_request(passport=psp, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AAWTDB_RE.value)

    def test_delete_widget_request_failure_invalid_passport(self):
        ''' delete_widget_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        bid=uuid.uuid4().hex
        wid=uuid.uuid4().hex
        for psp in passports:
            response=dashboardapi.delete_widget_request(passport=psp, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_invalid_bid(self):
        ''' delete_widget_request should fail if bid is invalid '''
        bids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        wid=uuid.uuid4().hex
        for bid in bids:
            response=dashboardapi.delete_widget_request(passport=psp, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_invalid_wid(self):
        ''' delete_widget_request should fail if wid is invalid '''
        wids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        bid=uuid.uuid4().hex
        for wid in wids:
            response=dashboardapi.delete_widget_request(passport=psp, bid=bid, wid=wid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_widget_request_failure_non_existent_user(self):
        ''' delete_widget_request should fail if user has no access over bid or wid '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(passport=psp, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADWFDB_RE.value)

    def test_delete_widget_request_failure_no_existing_bid(self):
        ''' delete_widget_request should fail if user has no access over bid '''
        psp = self.passport
        wid=uuid.uuid4().hex
        bid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(passport=psp, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADWFDB_RE.value)

    def test_delete_widget_request_success_no_previous_widgets(self):
        ''' delete_widget_request should succeed even if dashboard has no previous widgets '''
        psp = self.passport
        dashboardname='test_delete_widget_request_success_no_previous_widgets'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])
        wid=uuid.uuid4().hex
        response=dashboardapi.delete_widget_request(passport=psp, bid=bid, wid=wid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

    def test_new_dashboard_request_failure_invalid_passport(self):
        ''' new_dashboard_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        dashboardname='test_new_dashboard_request_failure_invalid_username'
        data={'dashboardname':dashboardname}
        for psp in passports:
            response=dashboardapi.new_dashboard_request(passport=psp,data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_dashboard_request_failure_invalid_dashboardname(self):
        ''' new_dashboard_request should fail if username is invalid '''
        dashboardnames=['',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        for dashboardname in dashboardnames:
            data={'dashboardname':dashboardname}
            response=dashboardapi.new_dashboard_request(passport=psp,data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_dashboard_request_failure_non_existent_user(self):
        ''' new_dashboard_request should fail if user does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        dashboardname='test_new_dashboard_request_failure_non_existent_user'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GBA_CRD_UNF.value)

    def test_new_dashboard_request_success(self):
        ''' new_dashboard_request should fail if user does not exist '''
        psp = self.passport
        dashboardname='test_new_dashboard_request_success'
        data={'dashboardname':dashboardname}
        response=dashboardapi.new_dashboard_request(passport=psp,data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        bid=response.data['bid']
        self.assertTrue(isinstance(uuid.UUID(bid),uuid.UUID))
        for msg in response.imc_messages['unrouted']:
            msgresponse=msgapi.process_message(msg)
            self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=dashboardapi.get_dashboard_config_request(passport=psp, bid=bid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['dashboardname'],dashboardname)
        self.assertEqual(response.data['bid'],bid)
        self.assertEqual(response.data['wids'],[])

