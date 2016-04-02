import unittest
import uuid
import json
from komlog.komlibs.auth import errors as autherrors
from komlog.komlibs.auth import passport
from komlog.komlibs.gestaccount import errors as gesterrors
from komlog.komlibs.gestaccount.user import api as gestuserapi
from komlog.komlibs.gestaccount.user.states import *
from komlog.komlibs.interface.web.api import user as userapi 
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web import status, errors
from komlog.komlibs.interface.web import exceptions
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi


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
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
            response=userapi.new_user_request(username=username, password=password, email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_user_request_failure_invalid_password(self):
        ''' new_user_request should fail if password is invalid'''
        username = 'test_new_user_request_failure_invalid_password_user'
        passwords = [None, 23423424, {'a':'dict'},['a list',],'short',{'set'}]
        email = username+'@komlog.org'
        for password in passwords:
            response=userapi.new_user_request(username=username, password=password, email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_user_request_failure_invalid_email(self):
        ''' new_user_request should fail if email is invalid'''
        username = 'test_new_user_request_failure_invalid_email_user'
        password = 'password'
        emails = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for email in emails:
            response=userapi.new_user_request(username=username, password=password, email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_user_request_failure_invalid_invitation(self):
        ''' new_user_request should fail if invitation is invalid and require_invitation is True '''
        username = 'test_new_user_request_failure_invalid_invitation_user'
        password = 'password'
        email = username+'@komlog.org'
        invitations = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        for invitation in invitations:
            response=userapi.new_user_request(username=username, password=password, email=email, invitation=invitation, require_invitation=True)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_user_request_failure_non_existent_invitation(self):
        ''' new_user_request should fail if invitation does not exist '''
        username = 'test_new_user_request_failure_non_existent_invitation_user'
        password = 'password'
        email = username+'@komlog.org'
        invitation=uuid.uuid4().hex
        response=userapi.new_user_request(username=username, password=password, email=email, invitation=invitation, require_invitation=True)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_user_request_success_with_invitation(self):
        ''' new_user_request should succeed if invitation_request is True and invitation exists and is unused '''
        username = 'test_new_user_request_success_with_invitation_user'
        password = 'password'
        email = username+'@komlog.org'
        invitation=gestuserapi.generate_user_invitations(email=email)
        invitation=invitation[0]['inv_id'].hex
        response=userapi.new_user_request(username=username, password=password, email=email, invitation=invitation, require_invitation=True)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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

    def test_new_user_request_failure_already_used_invitation(self):
        ''' new_user_request should fail if invitation passed is already used '''
        username = 'test_new_user_request_failure_already_used_invitation'
        password = 'password'
        email = username+'@komlog.org'
        invitation=gestuserapi.generate_user_invitations(email=email)
        invitation=invitation[0]['inv_id'].hex
        response=userapi.new_user_request(username=username, password=password, email=email, invitation=invitation, require_invitation=True)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        username = 'test_new_user_request_failure_already_used_invitation_2'
        password = 'password'
        email = username+'@komlog.org'
        response=userapi.new_user_request(username=username, password=password, email=email, invitation=invitation, require_invitation=True)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.data, {'message':'Invitation Already Used'})

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
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response3 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response3.data['uid'])
        self.assertEqual(username,response3.data['username'])
        self.assertEqual(email,response3.data['email'])
        self.assertEqual(UserStates.ACTIVE,response3.data['state'])

    def test_confirm_user_request_failure_invalid_email(self):
        ''' new_user_request should fail if email is invalid/malformed'''
        code='ACODE'
        emails = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for email in emails:
            response=userapi.confirm_user_request(code=code, email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_confirm_user_request_failure_invalid_code(self):
        ''' new_user_request should fail if email is invalid/malformed'''
        email='user@komlog.org'
        codes = ['@@æ¶đu@ser@komlog.org', 'invaliæßðđd_code','my coæßðđde',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for code in codes:
            response=userapi.confirm_user_request(code=code, email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

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
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response3 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response3.data['uid'])
        self.assertEqual(username,response3.data['username'])
        self.assertEqual(email,response3.data['email'])
        self.assertEqual(UserStates.ACTIVE,response3.data['state'])
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
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])

    def test_get_user_config_request_failure_invalid_passport(self):
        ''' get_user_config_request should fail if passport is invalid'''
        passports = [None, 23423424, {'a':'dict'},['a list',],'asdfaesf$·@·ññ','/asdfa','my user']
        for psp in passports:
            response=userapi.get_user_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_config_request_failure_non_existent_user(self):
        ''' get_user_config_request should return an error if user does not exists '''
        psp = passport.Passport(uid=uuid.uuid4())
        response = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GUA_GUC_UNF)

    def test_update_user_config_request_success(self):
        ''' update_user_config_request should succeed if user exists, parameters are allowed and authorization succeeds '''
        username = 'test_update_user_config_request_success'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        new_email=username+'2@komlog.org'
        old_password=password
        new_password='password2'
        data={'email':new_email, 'old_password':old_password, 'new_password':new_password}
        response2 = userapi.update_user_config_request(passport=psp, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        response3 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response3.data['uid'])
        self.assertEqual(username,response3.data['username'])
        self.assertEqual(new_email,response3.data['email'])

    def test_update_user_config_request_failure_invalid_passport(self):
        ''' update_user_config_request should fail if username is invalid '''
        passports=['Invalid User','invalidUser',None, 23423423, 'user@user',{'a':'dict'},['a','list'],json.dumps('username')]
        data={}
        for psp in passports:
            response=userapi.update_user_config_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_invalid_data(self):
        ''' update_user_config_request should fail if data is invalid '''
        datas=['Invalid User','invalidUser',None, 23423423, 'user@user','validuser',['a','list'],json.dumps('username')]
        psp = passport.Passport(uid=uuid.uuid4())
        for data in datas:
            response=userapi.update_user_config_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_invalid_email(self):
        ''' update_user_config_request should fail if email is invalid '''
        data={}
        psp = passport.Passport(uid=uuid.uuid4())
        emails=['Wrong@email.com','.@mail.com','invalid@email@email.com','@|invalid.email@email.com',json.dumps('valid@email.com'),{'a':'dict'},['a','list'],None,23423423423,23423.23234]
        for email in emails:
            data['email']=email
            response=userapi.update_user_config_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_invalid_new_password(self):
        ''' update_user_config_request should fail if new_password is invalid '''
        data={}
        psp = passport.Passport(uid=uuid.uuid4())
        passwords=[{'a':'dict'},['a','list'],None,23423423423,23423.23234,'short']
        data['old_password']='validpassword'
        for password in passwords:
            data['new_password']=password
            response=userapi.update_user_config_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_invalid_old_password(self):
        ''' update_user_config_request should fail if old_password is invalid '''
        data={}
        psp = passport.Passport(uid=uuid.uuid4())
        passwords=[{'a':'dict'},['a','list'],None,23423423423,23423.23234,'short']
        data['new_password']='validpassword'
        for password in passwords:
            data['old_password']=password
            response=userapi.update_user_config_request(passport=psp, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_old_password_authorization_error(self):
        ''' update_user_config_request should fail if old_password is invalid '''
        username = 'test_update_user_config_request_failure_old_password_authorization_error'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        data={}
        data['old_password']='validpassword'
        data['new_password']=password
        response2 = userapi.update_user_config_request(passport=psp, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_user_config_request_failure_only_old_password(self):
        ''' update_user_config_request should fail if only old_password is passed '''
        username = 'test_update_user_config_request_failure_only_old_password'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        data={}
        data['old_password']=password
        response2 = userapi.update_user_config_request(passport=psp, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_only_new_password(self):
        ''' update_user_config_request should fail if only new_password is passed '''
        username = 'test_update_user_config_request_failure_only_new_password'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        data={}
        data['new_password']=password
        response2 = userapi.update_user_config_request(passport=psp, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_user_config_request_failure_new_password_same_as_old_password(self):
        ''' update_user_config_request should fail if new_password is equal that old_password '''
        username = 'test_update_user_config_request_failure_new_password_same_as_old_password'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        data={}
        data['new_password']=password
        response2 = userapi.update_user_config_request(passport=psp, data=data)
        self.assertEqual(response2.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_user_request_failure_invalid_passport(self):
        ''' delete_user_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        for psp in passports:
            response=userapi.delete_user_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_register_invitation_request_failure_invalid_email(self):
        ''' register_invitation_request should fail if email is invalid'''
        emails = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for email in emails:
            response=userapi.register_invitation_request(email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_RIR_IEMAIL)

    def test_register_invitation_request_success_non_previously_registered(self):
        ''' register_invitation_request should succeed if the request was not registered previously '''
        email='test_register_invitation_request_success_non_previosly_registered@komlog.org'
        response=userapi.register_invitation_request(email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {'email':email})

    def test_register_invitation_request_success_previously_registered(self):
        ''' register_invitation_request should succeed if the request was registered previously '''
        email='test_register_invitation_request_success_previosly_registered@komlog.org'
        response=userapi.register_invitation_request(email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {'email':email})
        response=userapi.register_invitation_request(email=email)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {'email':email})

    def test_check_invitation_request_failure_invalid_invitation(self):
        ''' check_invitation_request should fail if invitation is invalid '''
        invitations = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        for invitation in invitations:
            response=userapi.check_invitation_request(invitation=invitation)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_CIR_IINV)

    def test_check_invitation_request_failure_invitation_not_found(self):
        ''' check_invitation_request should fail if invitation is not found'''
        invitation=uuid.uuid4().hex
        response=userapi.check_invitation_request(invitation=invitation)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, errors.E_IWAU_CIR_INVNF)

    def test_check_invitation_request_failure_invitation_already_used(self):
        ''' check_invitation_request should fail if invitation is not found'''
        username = 'test_check_invitation_request_failure_already_used_invitation'
        password = 'password'
        email = username+'@komlog.org'
        invitation=gestuserapi.generate_user_invitations(email=email)
        invitation=invitation[0]['inv_id'].hex
        response=userapi.new_user_request(username=username, password=password, email=email, invitation=invitation, require_invitation=True)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        response=userapi.check_invitation_request(invitation=invitation)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_CIR_INVAU)

    def test_check_invitation_request_success(self):
        ''' check_invitation_request should succeed if invitation exists and is unused '''
        username = 'test_check_invitation_request_success'
        password = 'password'
        email = username+'@komlog.org'
        invitation=gestuserapi.generate_user_invitations(email=email)
        invitation=invitation[0]['inv_id'].hex
        response=userapi.check_invitation_request(invitation=invitation)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.error, None)
        self.assertEqual(response.data, {'invitation':invitation})

    def test_send_invitation_request_failure_invalid_email(self):
        ''' send_invitation_request should fail if email is invalid'''
        emails = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,{'a':'dict'}, ['a list',],('a','tuple')]
        for email in emails:
            response=userapi.send_invitation_request(email=email)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_SIR_IEMAIL)

    def test_send_invitation_request_failure_invalid_num(self):
        ''' send_invitation_request should fail if num is invalid'''
        email='test_send_invitation_request_failure_invalid_num@komlog.org'
        nums= ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',uuid.uuid4(), uuid.uuid1(), 234234.342,None,{'a':'dict'}, ['a list',],('a','tuple')]
        for num in nums:
            response=userapi.send_invitation_request(email=email, num=num)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_SIR_INUM)

    def test_send_invitation_request_success(self):
        ''' send_invitation_request should succeed and send the mail '''
        username = 'test_send_invitation_request_success'
        email = username+'@komlog.org'
        response = userapi.send_invitation_request(email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(isinstance(response.data[0],tuple))
        self.assertEqual(response.data[0][0], email)
        msg_addr=routing.get_address(type=messages.NEW_INV_MAIL_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.NEW_INV_MAIL_MESSAGE or msg.email!=email:
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(msg.email, email)
        self.assertEqual(msg.inv_id, uuid.UUID(response.data[0][1]))
        self.assertTrue(args.is_valid_uuid(msg.inv_id))

    def test_register_forget_request_failure_invalid_account(self):
        ''' register_forget_request should fail if account is not an email nor username '''
        accounts = ['u@ser@komlog.org', 'invalid_email_ñ@domain.com','email@.com','.@domain.com','my email@domain.com','email . @email.com',234234,None,{'a':'dict'}, ['a list',],('a','tuple'),'userÑameInvalid']
        for account in accounts:
            response=userapi.register_forget_request(account=account)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_RFR_IACCOUNT)

    def test_register_forget_request_failure_non_existent_email(self):
        ''' register_forget_request should fail if email passed does not belong to any user '''
        email='test_register_forget_request_failure_non_existent_email@komlog.org'
        response=userapi.register_forget_request(account=email)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_RFR_UNF)

    def test_register_forget_request_failure_non_existent_username(self):
        ''' register_forget_request should fail if username passed does not belong to any user '''
        username='test_register_forget_request_failure_non_existent_email'
        response=userapi.register_forget_request(account=username)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_RFR_UNF)

    def test_register_forget_request_success_passing_user_email(self):
        ''' register_forget_request should succeed if we pass an existing email '''
        username = 'test_register_forget_request_success_passing_user_email'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        response3=userapi.register_forget_request(account=email)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['username'], username)
        self.assertEqual(response3.data['email'],email)
        msg_addr=routing.get_address(type=messages.FORGET_MAIL_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.FORGET_MAIL_MESSAGE or msg.email!=email:
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(response3.data['code'],msg.code.hex)

    def test_register_forget_request_success_passing_user_username(self):
        ''' register_forget_request should succeed if we pass an existing username '''
        username = 'test_register_forget_request_success_passing_user_username'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        response3=userapi.register_forget_request(account=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['username'], username)
        self.assertEqual(response3.data['email'],email)
        msg_addr=routing.get_address(type=messages.FORGET_MAIL_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.FORGET_MAIL_MESSAGE or msg.email!=email:
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(response3.data['code'],msg.code.hex)

    def test_check_forget_code_request_failure_invalid_code(self):
        ''' check_forget_code_request should fail if code is invalid '''
        codes= ['u@ser@komlog.orgæðđ', 'invalid_email_ñ@domain.com','email@.c@ðlom',234234,None,{'a':'dict'}, ['a list',],('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        for code in codes:
            response=userapi.check_forget_code_request(code=code)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_CFR_ICODE)

    def test_check_forget_code_request_failure_non_existent_code(self):
        ''' check_forget_code_request should fail if code is invalid '''
        code=uuid.uuid4().hex
        response=userapi.check_forget_code_request(code=code)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_CFR_CNF)

    def test_check_forget_code_request_failure_already_used_code(self):
        ''' check_forget_code_request should fail if code is already used '''
        username = 'test_check_forget_request_failure_already_used_code'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        response3=userapi.register_forget_request(account=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['username'], username)
        self.assertEqual(response3.data['email'],email)
        msg_addr=routing.get_address(type=messages.FORGET_MAIL_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.FORGET_MAIL_MESSAGE or msg.email!=email:
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(response3.data['code'],msg.code.hex)
        code=response3.data['code']
        password='newpassword'
        response=userapi.reset_password_request(code=code, password=password)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        response=userapi.check_forget_code_request(code=code)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_CFR_CODEAU)

    def test_check_forget_code_request_success(self):
        ''' check_forget_code_request should succeed '''
        username = 'test_check_forget_code_request_succeed'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        response3=userapi.register_forget_request(account=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['username'], username)
        self.assertEqual(response3.data['email'],email)
        msg_addr=routing.get_address(type=messages.FORGET_MAIL_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.FORGET_MAIL_MESSAGE or msg.email!=email:
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(response3.data['code'],msg.code.hex)
        code=response3.data['code']
        response=userapi.check_forget_code_request(code=code)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {'code':code})

    def test_reset_password_request_failure_invalid_code(self):
        ''' reset_password_request should fail if code is invalid '''
        codes = ['u@ser@komlog.org', 'invalid_code','my code',234234,None,{'a':'dict'}, ['a list',],('a','tuple')]
        password='temporal'
        for code in codes:
            response=userapi.reset_password_request(code=code, password=password)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_RPR_ICODE)

    def test_reset_password_request_failure_invalid_password(self):
        ''' reset_password_request should fail if code is invalid '''
        passwords = [None, 23423424, {'a':'dict'},['a list',],'short']
        code=uuid.uuid4().hex
        for password in passwords:
            response=userapi.reset_password_request(code=code, password=password)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAU_RPR_IPWD)

    def test_reset_password_request_failure_code_not_found(self):
        ''' reset_password_request should fail if code is not found '''
        code=uuid.uuid4().hex
        password='temporal'
        response=userapi.reset_password_request(code=code, password=password)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_RPR_CNF)

    def test_reset_password_request_failure_code_already_used(self):
        ''' reset_password_request should fail if code is already used'''
        username = 'test_reset_password_request_failure_code_already_used'
        password = 'password'
        email = username+'@komlog.org'
        response = userapi.new_user_request(username=username, password=password, email=email)
        self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['uid']), uuid.UUID))
        cookie = {'user':username, 'aid':None, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
        psp = passport.get_user_passport(cookie)
        response2 = userapi.get_user_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data['uid'],response2.data['uid'])
        self.assertEqual(username,response2.data['username'])
        self.assertEqual(email,response2.data['email'])
        self.assertEqual(UserStates.PREACTIVE,response2.data['state'])
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
        response3=userapi.register_forget_request(account=username)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['username'], username)
        self.assertEqual(response3.data['email'],email)
        msg_addr=routing.get_address(type=messages.FORGET_MAIL_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=5)
            self.assertIsNotNone(msg)
            if msg.type!=messages.FORGET_MAIL_MESSAGE or msg.email!=email:
                count+=1
                if count>=1000:
                    break
            else:
                break
        self.assertEqual(response3.data['code'],msg.code.hex)
        code=response3.data['code']
        password='newpassword'
        response=userapi.reset_password_request(code=code, password=password)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        password='newpassword2'
        response=userapi.reset_password_request(code=code, password=password)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAU_RPR_CODEAU)

