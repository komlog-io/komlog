import unittest
import uuid
import json
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import circle as circleapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.interface.imc import status as msgstatus
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc.api import rescontrol, gestconsole
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi


class InterfaceWebApiCircleTest(unittest.TestCase):
    ''' komlibs.interface.web.api.circle tests '''

    def setUp(self):
        ''' In this module, we need an user '''
        self.username = 'test_komlibs.interface.web.api.circle_user'
        self.password = 'password'
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
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
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        self.passport = passport.get_user_passport(cookie)

    def test_get_users_circles_config_request_failure_invalid_passport(self):
        ''' get_users_circles_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=circleapi.get_users_circles_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_users_circles_config_request_failure_user_not_found(self):
        ''' get_users_circles_config_request should fail if username is not found '''
        psp = passport.Passport(uid=uuid.uuid4())
        response=circleapi.get_users_circles_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_users_circles_config_request_success(self):
        ''' get_users_circles_config_request should succeed '''
        psp = self.passport
        response=circleapi.get_users_circles_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)

    def test_get_users_circle_config_request_failure_invalid_passport(self):
        ''' get_users_circle_config_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        for psp in passports:
            response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_users_circle_config_request_failure_invalid_cid(self):
        ''' get_users_circle_config_request should fail if cid is invalid '''
        cids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for cid in cids:
            response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_users_circle_config_request_failure_non_existent_user(self):
        ''' get_users_circle_config should fail if user does not exist '''
        psp = self.passport
        cid=uuid.uuid4().hex
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGCC_RE.value)

    def test_get_users_circle_config_request_failure_non_existent_cid(self):
        ''' get_users_circle_config should fail if cid does not exist '''
        psp = self.passport
        cid=uuid.uuid4().hex
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AGCC_RE.value)

    def test_get_users_circle_config_request_failure_no_permissions_over_cid(self):
        ''' get_users_circle_request should fail if user has no permissions over cid '''
        psp = self.passport
        circlename='test_get_users_circle_config_request_failure_no_permissions_over_cid'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        username='test_get_users_circle_config_request_failure_no_permissions_over_cid'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
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
        response, cookie = loginapi.login_request(username=username, password=password)
        psp2 = passport.get_user_passport(cookie)
        response=circleapi.get_users_circle_config_request(passport=psp2, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_users_circle_config_request_success(self):
        ''' get_users_circle_request should succeed and return circle info '''
        psp = self.passport
        circlename='test_get_users_circle_config_request_success'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['cid'],cid)
        self.assertEqual(response.data['circlename'],circlename)
        self.assertEqual(response.data['members'],[])

    def test_delete_circle_request_failure_invalid_passport(self):
        ''' delete_circle_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        for psp in passports:
            response=circleapi.delete_circle_request(passport=psp, cid=cid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_circle_request_failure_invalid_cid(self):
        ''' delete_circle_request should fail if cid is invalid '''
        cids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(), uuid.uuid4(), uuid.uuid1().hex]
        psp = self.passport
        for cid in cids:
            response=circleapi.delete_circle_request(passport=psp, cid=cid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_circle_request_failure_non_existent_user(self):
        ''' delete_circle_request should fail if username does not exist '''
        psp = self.passport
        cid=uuid.uuid4().hex
        response=circleapi.delete_circle_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADC_RE.value)

    def test_delete_circle_request_failure_no_permissions_over_cid(self):
        ''' delete_circle_request should fail if user has no permissions over cid '''
        psp = self.passport
        circlename='test_delete_circle_request_failure_no_permissions_over_cid'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        username='test_delete_circle_request_failure_no_permissions_over_cid'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
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
        response, cookie = loginapi.login_request(username=username, password=password)
        psp2 = passport.get_user_passport(cookie)
        response=circleapi.delete_circle_request(passport=psp2, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_circle_request_success(self):
        ''' delete_circle_request should succeed '''
        psp = self.passport
        circlename='test_delete_circle_request_succeess'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=circleapi.delete_circle_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_new_users_circle_request_failure_invalid_passport(self):
        ''' new_users_circle_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        circlename='test_new_users_circle_request_failure_invalid_username'
        for psp in passports:
            response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_users_circle_request_failure_invalid_circlename(self):
        ''' new_users_circle_request should fail if circlename is invalid '''
        circlenames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'circleñame']
        psp = self.passport
        for circlename in circlenames:
            response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_users_circle_request_failure_invalid_members_list(self):
        ''' new_users_circle_request should fail if members_list is invalid '''
        circlename='test_new_users_circle_request_failure_invalid_members_list'
        psp = self.passport
        members_lists=[32423, 023423.23423, {'a':'dict'},('a','tuple'),'circleñame',uuid.uuid1(), uuid.uuid4(), uuid.uuid4().hex]
        for members_list in members_lists:
            response=circleapi.new_users_circle_request(passport=psp, circlename=circlename,members_list=members_list)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_users_circle_request_failure_non_existent_user(self):
        ''' new_users_circle_request should fail if user does not exist '''
        psp = passport.Passport(uid=uuid.uuid4())
        circlename='test_new_users_circle_request_failure_non_existent_user'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GCA_NUC_UNF.value)

    def test_new_users_circle_request_success(self):
        ''' new_users_circle_request should succeed and return the circle id '''
        psp = self.passport
        circlename='test_new_users_circle_request_success'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break

    def test_update_circle_request_failure_invalid_passport(self):
        ''' update_circle_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        circlename='test_update_circle_request_failure_invalid_username'
        data={'circlename':circlename}
        for psp in passports:
            response=circleapi.update_circle_request(passport=psp, cid=cid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_circle_request_failure_invalid_cid(self):
        ''' update_circle_request should fail if cid is invalid '''
        cids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        circlename='test_update_circle_request_failure_invalid_username'
        data={'circlename':circlename}
        for cid in cids:
            response=circleapi.update_circle_request(passport=psp, cid=cid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_circle_request_failure_invalid_data(self):
        ''' update_circle_request should fail if data is invalid '''
        datas=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',{'circlename':'invalid circle Ñame'}]
        cid=uuid.uuid4().hex
        psp = self.passport
        for data in datas:
            response=circleapi.update_circle_request(passport=psp, cid=cid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_circle_request_failure_non_existent_user(self):
        ''' update_circle_request should fail if user does not exist '''
        cid=uuid.uuid4().hex
        psp = passport.Passport(uid=uuid.uuid4())
        circlename='test_update_circle_request_failure_non_existent_user'
        data={'circlename':circlename}
        response=circleapi.update_circle_request(passport=psp, cid=cid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AUCC_RE.value)

    def test_update_circle_request_failure_no_permissions_over_cid(self):
        ''' update_circle_request should fail if user has no permissions over cid '''
        psp = self.passport
        circlename='test_update_circle_request_failure_no_permissions_over_cid'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        username='test_update_circle_request_failure_no_permissions_over_cid'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
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
        data={'circlename':circlename}
        response, cookie = loginapi.login_request(username=username, password=password)
        psp2= passport.get_user_passport(cookie)
        response=circleapi.update_circle_request(passport=psp2, cid=cid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_circle_request_success(self):
        ''' update_circle_request should fail if user has no permissions over cid '''
        psp = self.passport
        circlename='test_update_circle_request_success'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        new_circlename='test_update_circle_request_success_updated'
        data={'circlename':new_circlename}
        response=circleapi.update_circle_request(passport=psp, cid=cid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['cid'],cid)
        self.assertEqual(response.data['circlename'],new_circlename)
        self.assertEqual(response.data['members'],[])

    def test_add_user_to_circle_request_failure_invalid_passport(self):
        ''' add_user_to_circle_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        member='test_add_user_to_circle_request_failure_invalid_username'
        for psp in passports:
            response=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_user_to_circle_request_failure_invalid_cid(self):
        ''' add_user_to_circle_request should fail if cid is invalid '''
        cids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(), uuid.uuid4(), uuid.uuid1().hex]
        psp = self.passport
        member='test_add_user_to_circle_request_failure_invalid_cid_member'
        for cid in cids:
            response=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_user_to_circle_request_failure_invalid_member(self):
        ''' add_user_to_circle_request should fail if member is invalid '''
        members=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        psp = self.passport
        for member in members:
            response=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_add_user_to_circle_request_failure_non_existent_user(self):
        ''' add_user_to_circle_request should fail if user does not exist '''
        cid=uuid.uuid4().hex
        psp = passport.Passport(uid=uuid.uuid4())
        member='test_add_user_to_circle_request_failure_non_existent_user_member'
        response=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AAMTC_RE.value)

    def test_add_user_to_circle_request_failure_non_existent_circle(self):
        ''' add_user_to_circle_request should fail if circle does not exist '''
        cid=uuid.uuid4().hex
        psp = self.passport
        member='test_add_user_to_circle_request_failure_non_existent_circle_member'
        response=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_AAMTC_RE.value)

    def test_add_user_to_circle_request_failure_non_existent_member(self):
        ''' add_user_to_circle_request should fail if member does not exist '''
        psp = self.passport
        circlename='test_add_user_to_circle_request_failure_non_existent_member'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['cid'],cid)
        self.assertEqual(response.data['circlename'],circlename)
        self.assertEqual(response.data['members'],[])
        member='test_add_user_to_circle_request_failure_non_existent_member'
        response2=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response2.status, status.WEB_STATUS_NOT_FOUND)

    def test_add_user_to_circle_request_success(self):
        ''' add_user_to_circle_request should succeed '''
        psp = self.passport
        circlename='test_add_user_to_circle_request_succees'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['cid'],cid)
        self.assertEqual(response.data['circlename'],circlename)
        self.assertEqual(response.data['members'],[])
        member='test_add_user_to_circle_request_success'
        password = 'password'
        email = member+'@komlog.org'
        response2 = userapi.new_user_request(username=member, password=password, email=email)
        self.assertTrue(isinstance(response2, webresp.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response3=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response4=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        self.assertEqual(response4.data['cid'],cid)
        self.assertEqual(response4.data['circlename'],circlename)
        self.assertEqual(response4.data['members'],[{'username':member,'uid':response2.data['uid']}])
    def test_delete_user_from_circle_request_failure_invalid_passport(self):
        ''' delete_user_from_circle_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        member='test_delete_user_from_circle_request_failure_invalid_username'
        for psp in passport:
            response=circleapi.delete_user_from_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_user_from_circle_request_failure_invalid_cid(self):
        ''' delete_user_from_circle_request should fail if cid is invalid '''
        cids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(), uuid.uuid4(), uuid.uuid1().hex]
        psp = self.passport
        member='test_delete_user_from_circle_request_failure_invalid_cid_member'
        for cid in cids:
            response=circleapi.delete_user_from_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_user_from_circle_request_failure_invalid_member(self):
        ''' delete_user_from_circle_request should fail if member is invalid '''
        members=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        psp = self.passport
        for member in members:
            response=circleapi.delete_user_from_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_user_from_circle_request_failure_non_existent_user(self):
        ''' delete_user_from_circle_request should fail if user does not exist '''
        cid=uuid.uuid4().hex
        psp = self.passport
        member='test_delete_user_from_circle_request_failure_non_existent_user_member'
        response=circleapi.delete_user_from_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADMFC_RE.value)

    def test_delete_user_from_circle_request_failure_non_existent_circle(self):
        ''' delete_user_from_circle_request should fail if circle does not exist '''
        cid=uuid.uuid4().hex
        psp = self.passport
        member='test_delete_user_from_circle_request_failure_non_existent_circle_member'
        response=circleapi.delete_user_from_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADMFC_RE.value)

    def test_delete_user_from_circle_request_failure_non_existent_member(self):
        ''' delete_user_from_circle_request should fail if member does not exist '''
        psp = self.passport
        circlename='test_delete_user_from_circle_request_failure_non_existent_member'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['cid'],cid)
        self.assertEqual(response.data['circlename'],circlename)
        self.assertEqual(response.data['members'],[])
        member='test_delete_user_from_circle_request_failure_non_existent_member'
        response2=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response2.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_user_from_circle_request_success(self):
        ''' delete_user_from_circle_request should succeed '''
        psp = self.passport
        circlename='test_delete_user_from_circle_request_success'
        response=circleapi.new_users_circle_request(passport=psp, circlename=circlename)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('cid' in response.data)
        cid=response.data['cid']
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['cid'],cid)
        self.assertEqual(response.data['circlename'],circlename)
        self.assertEqual(response.data['members'],[])
        member='test_delete_user_from_circle_request_success'
        password = 'password'
        email = member+'@komlog.org'
        response2 = userapi.new_user_request(username=member, password=password, email=email)
        self.assertTrue(isinstance(response2, webresp.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response3=circleapi.add_user_to_circle_request(passport=psp, cid=cid, member=member)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response4=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        self.assertEqual(response4.data['cid'],cid)
        self.assertEqual(response4.data['circlename'],circlename)
        self.assertEqual(response4.data['members'],[{'username':member,'uid':response2.data['uid']}])
        response5=circleapi.delete_user_from_circle_request(passport=psp,cid=cid,member=member)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                msg_result=msgapi.process_message(msg)
                self.assertEqual(msg_result.status,msgstatus.IMC_STATUS_OK)
                if msg_result:
                    msgapi.process_msg_result(msg_result)
            else:
                break
        response6=circleapi.get_users_circle_config_request(passport=psp, cid=cid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertEqual(response6.data['cid'],cid)
        self.assertEqual(response6.data['circlename'],circlename)
        self.assertEqual(response6.data['members'],[])

    def test_delete_user_from_circle_request_failure_invalid_passport(self):
        ''' delete_user_from_circle_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        cid=uuid.uuid4().hex
        member='test_delete_user_from_circle_request_failure_invalid_username'
        for psp in passports:
            response=circleapi.delete_user_from_circle_request(passport=psp, cid=cid, member=member)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

