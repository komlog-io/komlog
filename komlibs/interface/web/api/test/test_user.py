import unittest
import uuid
import json
from komlibs.gestaccount.user import states as userstates
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status
from komlibs.interface.web import exceptions
from komlibs.interface.imc.model import messages
from komlibs.general.validation import arguments as args
from komimc import bus, routing
from komimc import api as msgapi


class InterfaceWebApiUserTest(unittest.TestCase):
    ''' komlibs.interface.web.api.user tests '''

    def test_new_user_request_success(self):
        ''' new_user_request should succeed if arguments are valid and return the user uid '''
        username = 'test_new_user_request_success'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        response2 = userapi.get_user_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(userstates.PREACTIVE,response2.data['state'])
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_USR_NOTIF_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email, email)
        self.assertTrue(args.is_valid_code(msg.code))

    def test_new_user_request_failure_already_existing_user(self):
        ''' new_user_request should succeed if arguments are valid and return the user uid '''
        username = 'test_new_user_request_failure_already_existing_user'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        response2 = userapi.get_user_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(userstates.PREACTIVE,response2.data['state'])
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_USR_NOTIF_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email,email)
        self.assertTrue(args.is_valid_code(msg.code))
        response3 = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response3, webmodel.WebInterfaceResponse))
        self.assertEqual(response3.status, status.WEB_STATUS_ACCESS_DENIED)
        #TODO: en el mensaje de respuesta hay que indicar el motivo del fallo

    def test_new_user_request_failure_invalid_username(self):
        ''' new_user_request should fail if username is invalid'''
        usernames = [None, 23423424, {'a':'dict'},['a list',],'asdfaesf$·@·ññ','/asdfa','my user']
        password = 'password'
        email = 'user@komlog.org'
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, userapi.new_user_request, username=username, password=password, email=email)

    def test_new_user_request_failure_invalid_password(self):
        ''' new_user_request should fail if password is invalid'''
        username = 'test_new_user_request_failure_invalid_password_user'
        passwords = [None, 23423424, {'a':'dict'},['a list',],'asdfaesf$·@·ññ','short']
        email = username+'@komlog.org'
        for password in passwords:
            self.assertRaises(exceptions.BadParametersException, userapi.new_user_request, username=username, password=password, email=email)

    def test_new_user_request_failure_invalid_email(self):
        ''' new_user_request should fail if email is invalid'''
        username = 'test_new_user_request_failure_invalid_email_user'
        password = 'password'
        emails = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for email in emails:
            self.assertRaises(exceptions.BadParametersException, userapi.new_user_request, username=username, password=password, email=email)

    def test_confirm_user_request_success(self):
        ''' confirm_user_request should succeed if arguments are valid and the user state is set to activated '''
        username = 'test_confirm_user_request_success'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_USR_NOTIF_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email, email)
        self.assertTrue(args.is_valid_code(msg.code))
        response2=userapi.confirm_user_request(email=msg.email, code=msg.code)
        self.assertTrue(isinstance(response2, webmodel.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        response3 = userapi.get_user_config_request(username=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response3.data['uid'])
        self.assertEqual(username,response3.data['username'])
        self.assertEqual(email,response3.data['email'])
        self.assertEqual(userstates.ACTIVE,response3.data['state'])

    def test_confirm_user_request_failure_invalid_email(self):
        ''' new_user_request should fail if email is invalid/malformed'''
        code='ACODE'
        emails = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for email in emails:
            self.assertRaises(exceptions.BadParametersException, userapi.confirm_user_request, code=code, email=email)

    def test_confirm_user_request_failure_invalid_code(self):
        ''' new_user_request should fail if email is invalid/malformed'''
        email='user@komlog.org'
        codes = ['u@ser@komlog.org', 'invalid_code','my code',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for code in codes:
            self.assertRaises(exceptions.BadParametersException, userapi.confirm_user_request, code=code, email=email)

    def test_confirm_user_request_failure_wrong_email(self):
        ''' confirm_user_request should fail if email is not in the system or is not associated with the code given '''
        username = 'test_confirm_user_request_failure_wrong_email'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_USR_NOTIF_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email, email)
        self.assertTrue(args.is_valid_code(msg.code))
        email2='test_confirm_user_request_failure_wrong_email_2@komlog.org'
        response2=userapi.confirm_user_request(email=email2, code=msg.code)
        self.assertTrue(isinstance(response2, webmodel.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_NOT_FOUND)
        #TODO: falta hacer tratamiento de la excepcion para mostrar mensaje concreto de error

    def test_confirm_user_request_failure_wrong_code(self):
        ''' confirm_user_request should fail if code is not associated with the email given '''
        username = 'test_confirm_user_request_failure_wrong_code'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_USR_NOTIF_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email, email)
        self.assertTrue(args.is_valid_code(msg.code))
        response2=userapi.confirm_user_request(email=email, code='CUSTOMCODE')
        self.assertTrue(isinstance(response2, webmodel.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_INTERNAL_ERROR)
        #TODO: falta hacer tratamiento de la excepcion para mostrar mensaje concreto de error

    def test_confirm_user_request_failure_already_confirmed_user(self):
        ''' confirm_user_request should fail if confirmation was already done '''
        username = 'test_confirm_user_request_failure_already_confirmed_user'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_USR_NOTIF_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email, email)
        self.assertTrue(args.is_valid_code(msg.code))
        response2=userapi.confirm_user_request(email=msg.email, code=msg.code)
        self.assertTrue(isinstance(response2, webmodel.WebInterfaceResponse))
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        response3 = userapi.get_user_config_request(username=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response3.data['uid'])
        self.assertEqual(username,response3.data['username'])
        self.assertEqual(email,response3.data['email'])
        self.assertEqual(userstates.ACTIVE,response3.data['state'])
        response4=userapi.confirm_user_request(email=email, code=msg.code)
        self.assertTrue(isinstance(response4, webmodel.WebInterfaceResponse))
        self.assertEqual(response4.status, status.WEB_STATUS_INTERNAL_ERROR)
        #TODO: falta hacer tratamiento de la excepcion para mostrar mensaje concreto de error

    def test_get_user_config_request_success(self):
        ''' get_user_config_request should succeed if username is correct and exists '''
        username = 'test_get_user_config_request_success'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response2 = userapi.get_user_config_request(username=username)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual([],response2.data['agents'])

    def test_get_user_config_request_failure_invalid_username(self):
        ''' get_user_config_request should fail if username is invalid'''
        usernames = [None, 23423424, {'a':'dict'},['a list',],'asdfaesf$·@·ññ','/asdfa','my user']
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, userapi.get_user_config_request, username=username)

    def test_get_user_config_request_failure_non_existent_user(self):
        ''' get_user_config_request should return an error if user does not exists '''
        username = 'test_get_user_config_request_failure_non_existent_user'
        response = userapi.get_user_config_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_update_user_config_request_success(self):
        ''' update_user_config_request should succeed if user exists, parameters are allowed and authorization succeeds '''
        username = 'test_update_user_config_request_success'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        new_email=username+'2@komlog.org'
        old_password=password
        new_password='password2'
        data={'email':new_email, 'old_password':old_password, 'new_password':new_password}
        response2 = userapi.update_user_config_request(username=username, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        response3 = userapi.get_user_config_request(username=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response3.data['uid'])
        self.assertEqual(username,response3.data['username'])
        self.assertEqual(new_email,response3.data['email'])
        self.assertEqual([],response3.data['agents'])

    def test_update_user_config_request_failure_invalid_username(self):
        ''' update_user_config_request should fail if username is invalid '''
        users=['Invalid User','invalidUser',None, 23423423, 'user@user',{'a':'dict'},['a','list'],json.dumps('username')]
        data={}
        for username in users:
            self.assertRaises(exceptions.BadParametersException, userapi.update_user_config_request, username=username, data=data)

    def test_update_user_config_request_failure_invalid_data(self):
        ''' update_user_config_request should fail if data is invalid '''
        datas=['Invalid User','invalidUser',None, 23423423, 'user@user','validuser',['a','list'],json.dumps('username')]
        username='username'
        for data in datas:
            self.assertRaises(exceptions.BadParametersException, userapi.update_user_config_request, username=username, data=data)

    def test_update_user_config_request_failure_invalid_email(self):
        ''' update_user_config_request should fail if email is invalid '''
        data={}
        username='username'
        emails=['Wrong@email.com','.@mail.com','invalid@email@email.com','@|invalid.email@email.com',json.dumps('valid@email.com'),{'a':'dict'},['a','list'],None,23423423423,23423.23234]
        for email in emails:
            data['email']=email
            self.assertRaises(exceptions.BadParametersException, userapi.update_user_config_request, username=username, data=data)

    def test_update_user_config_request_failure_invalid_new_password(self):
        ''' update_user_config_request should fail if new_password is invalid '''
        data={}
        username='username'
        passwords=[{'a':'dict'},['a','list'],None,23423423423,23423.23234,'short']
        data['old_password']='validpassword'
        for password in passwords:
            data['new_password']=password
            self.assertRaises(exceptions.BadParametersException, userapi.update_user_config_request, username=username, data=data)

    def test_update_user_config_request_failure_invalid_old_password(self):
        ''' update_user_config_request should fail if old_password is invalid '''
        data={}
        username='username'
        passwords=[{'a':'dict'},['a','list'],None,23423423423,23423.23234,'short']
        data['new_password']='validpassword'
        for password in passwords:
            data['old_password']=password
            self.assertRaises(exceptions.BadParametersException, userapi.update_user_config_request, username=username, data=data)

    def test_update_user_config_request_failure_old_password_authorization_error(self):
        ''' update_user_config_request should fail if old_password is invalid '''
        username = 'test_update_user_config_request_failure_old_password_authorization_error'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        data={}
        data['old_password']='validpassword'
        data['new_password']=password
        response2 = userapi.update_user_config_request(username=username, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_user_config_request_failure_only_old_password(self):
        ''' update_user_config_request should fail if only old_password is passed '''
        username = 'test_update_user_config_request_failure_only_old_password'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        data={}
        data['old_password']=password
        response2 = userapi.update_user_config_request(username=username, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_only_new_password(self):
        ''' update_user_config_request should fail if only new_password is passed '''
        username = 'test_update_user_config_request_failure_only_new_password'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        data={}
        data['new_password']=password
        response2 = userapi.update_user_config_request(username=username, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_new_password_same_as_old_password(self):
        ''' update_user_config_request should fail if new_password is equal that old_password '''
        username = 'test_update_user_config_request_failure_new_password_same_as_old_password'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        data={}
        data['new_password']=password
        response2 = userapi.update_user_config_request(username=username, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_BAD_PARAMETERS)

