import unittest
import uuid
import stripe
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.user.states import *
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komcass.api import user as cassapiuser

class GestaccountUserApiTest(unittest.TestCase):
    ''' komlog.gestaccount.user.api tests '''

    def setUp(self):
        self.username = 'test_komlog.gestaccount.user.api_user'
        self.password = 'test_password'
        self.email = self.username+'@komlog.org'
        try:
            uid=userapi.get_uid(username=self.username)
        except Exception:
            user=userapi.create_user(username=self.username, password=self.password, email=self.email)
            uid=user['uid']
        finally:
            self.userinfo=userapi.get_user_config(uid=uid)

    def test_create_user(self):
        ''' create_user should insert the user in the database '''
        username = 'test_create_user_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])

    def test_create_user_failure_invalid_sid(self):
        ''' create_user should fail if sid is invalid '''
        username = 'test_create_user_failure_invalid_sid'
        password = 'password'
        email = username+'@komlog.org'
        sids=[2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.create_user(username=username, password=password, email=email, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_CRU_ISID)

    def test_create_user_failure_invalid_token(self):
        ''' create_user should fail if token is invalid '''
        username = 'test_create_user_failure_invalid_sid'
        password = 'password'
        email = username+'@komlog.org'
        tokens=[231213, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), uuid.uuid4(), uuid.uuid1()]
        for token in tokens:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.create_user(username=username, password=password, email=email, token=token)
            self.assertEqual(cm.exception.error, Errors.E_GUA_CRU_ITOK)

    def test_create_user_failure_non_existent_segment(self):
        ''' create_user should fail if sid segment does not exist '''
        username = 'test_create_user_failure_non_existent_segment'
        password = 'password'
        email = username+'@komlog.org'
        sid = 93921942
        with self.assertRaises(exceptions.BadParametersException) as cm:
            userapi.create_user(username=username, password=password, email=email, sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CRU_SEGNF)

    def test_create_user_failure_token_needed_for_segment_with_cost(self):
        ''' create_user should fail if segment has cost and we dont pass token '''
        username = 'test_create_user_failure_token_needed_for_segment_with_cost'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        with self.assertRaises(exceptions.BadParametersException) as cm:
            userapi.create_user(username=username, password=password, email=email, sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CRU_TOKNEED)

    def test_create_user_success_in_segment_with_cost(self):
        ''' create_user should succeed creating a user in a segment with cost '''
        username = 'test_create_user_success_in_segment_with_cost'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        user=userapi.create_user(username=username, password=password, email=email, sid=sid, token=token.id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['segment'], sid)

    def test_create_user_failure_token_used_twice(self):
        ''' create_user should fail if we use a token twice '''
        username = 'test_create_user_failure_token_used_twice_first_try'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        user=userapi.create_user(username=username, password=password, email=email, sid=sid, token=token.id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['segment'], sid)
        username = 'test_create_user_failure_token_used_twice_second_try'
        password = 'password'
        email = username+'@komlog.org'
        with self.assertRaises(exceptions.UserCreationException) as cm:
            userapi.create_user(username=username, password=password, email=email, sid=sid, token=token.id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CRU_ECREPAY)

    def test_auth_user(self):
        ''' auth_user should authenticate the user '''
        username = 'test_auth_user_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        result=userapi.auth_user(username, password)
        self.assertTrue(result)

    def test_confirm_user_valid_code(self):
        ''' confirm_user should modify user state if we pass a valid email and code '''
        username = 'test_confirm_user_valid_code_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(userapi.confirm_user(email=userinfo['email'], code=userinfo['code']))

    def test_confirm_user_invalid_code(self):
        ''' confirm_user should fail if code is not valid or not found '''
        username = 'test_confirm_user_invalid_code_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertRaises(exceptions.UserConfirmationException, userapi.confirm_user, email=userinfo['email'], code='TEST8CONFIRM8USER8INVALID8CODE')

    def test_confirm_user_invalid_email(self):
        ''' confirm_user should fail if email is not the one used to create the user '''
        username = 'test_confirm_user_invalid_email_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        email = username+'_fake@komlog.org'
        self.assertRaises(exceptions.UserNotFoundException, userapi.confirm_user, email=email, code=userinfo['code'])

    def test_confirm_user_failure_already_used_code(self):
        ''' confirm_user should modify user state if we pass a valid email and code '''
        username = 'test_confirm_user_failure_already_used_code_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(userapi.confirm_user(email=userinfo['email'], code=userinfo['code']))
        self.assertRaises(exceptions.UserConfirmationException, userapi.confirm_user, email=userinfo['email'], code=userinfo['code'])

    def test_update_user_config_no_params(self):
        ''' update_user_config shoud fail if no params is passed'''
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, uid=self.userinfo['uid'])

    def test_update_user_config_empty_only_old_password_param(self):
        ''' update_user_config shoud fail if only old_password is passed '''
        old_password=self.password
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config,uid=self.userinfo['uid'], old_password=old_password)

    def test_update_user_config_empty_only_new_password_param(self):
        ''' update_user_config shoud fail if only new_password is received '''
        new_password='new_password'
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, uid=self.userinfo['uid'], new_password=new_password)

    def test_update_user_config_same_passwords(self):
        ''' update_user_config shoud fail if old_password is equal to new_password '''
        old_password=self.password
        new_password=self.password
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, uid=self.userinfo['uid'], old_password=old_password, new_password=new_password)

    def test_update_user_config_already_existing_email(self):
        ''' update_user_config shoud fail if email is already on system '''
        username2='test_update_user_config_already_existing_email'
        password2='password_2'
        email2='test_update_user_config_already_existing_email@komlog.org'
        user2 = userapi.create_user(username=username2,password=password2,email=email2)
        email=email2
        self.assertRaises(exceptions.EmailAlreadyExistsException, userapi.update_user_config, uid=self.userinfo['uid'], new_email=email)

    def test_update_user_config_success_different_passwords(self):
        ''' update_user_config shoud succeed if old_password is different to new_password and old_password is correct'''
        old_password=self.password
        new_password='the_new_pass'
        self.assertTrue(userapi.update_user_config(uid=self.userinfo['uid'], old_password=old_password, new_password=new_password))

    def test_get_user_config_success(self):
        ''' get_user_config should return user data '''
        data=userapi.get_user_config(uid=self.userinfo['uid'])
        self.assertIsNotNone(data)
        self.assertEqual(self.username, data['username'])
        self.assertEqual(self.email, data['email'])

    def test_get_user_config_non_existing_username(self):
        ''' get_user_config should fail if username does not exist '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, userapi.get_user_config,uid=uid)

    def test_get_uid_failure_invalid_username(self):
        ''' get_uid should fail if username is invalid '''
        usernames=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4(), uuid.uuid1()]
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, userapi.get_uid, username=username)

    def test_get_uid_failure_non_existent_username(self):
        ''' get_uid should fail if username does not exist '''
        username='test_get_uid_failure_non_existent_username'
        self.assertRaises(exceptions.UserNotFoundException, userapi.get_uid, username=username)

    def test_get_uid_success(self):
        ''' get_uid should return the user's uid '''
        username=self.username
        uid=userapi.get_uid(username=username)
        self.assertTrue(isinstance(uid, uuid.UUID))
        self.assertEqual(uid, self.userinfo['uid'])

    def test_register_invitation_request_failure_invalid_email(self):
        ''' register_invitation_request should fail if email is invalid '''
        emails=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4(), uuid.uuid1(),'email@fake','@badmail','fake@']
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.register_invitation_request(email=email)
            self.assertEqual(cm.exception.error,Errors.E_GUA_RIR_IEMAIL)

    def test_register_invitation_request_success(self):
        ''' register_invitation_request should insert the request in db '''
        email='test_register_invitation_request_success@komlog.org'
        self.assertTrue(userapi.register_invitation_request(email=email))

    def test_generate_user_invitations_failure_invalid_email(self):
        ''' generate_user_invitations should fail if num=1 and email is in invalid '''
        emails=[34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4(), uuid.uuid1(),'email@fake','@badmail','fake@']
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.generate_user_invitations(email=email)
            self.assertEqual(cm.exception.error, Errors.E_GUA_GUI_IEMAIL)

    def test_generate_user_invitations_success_non_requested_previously(self):
        ''' generate_user_invitations should succeed and generate the invitation even if the request was not registered previously '''
        email='test_generate_user_invitations_success_non_requested_previously@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        self.assertEqual(len(invitations),1)
        self.assertEqual(invitations[0]['email'],email)
        self.assertTrue(isinstance(invitations[0]['inv_id'],uuid.UUID))

    def test_generate_user_invitations_success_previously_requested_invitation(self):
        ''' generate_user_invitations should succeed if invitation was requested previously '''
        email='test_generate_user_invitations_success_previously_requested_invitation@komlog.org'
        self.assertTrue(userapi.register_invitation_request(email=email))
        invitations=userapi.generate_user_invitations(email=email)
        self.assertEqual(len(invitations),1)
        self.assertEqual(invitations[0]['email'],email)
        self.assertTrue(isinstance(invitations[0]['inv_id'],uuid.UUID))

    def test_generate_user_invitations_success_previously_requested_multiple_invitations(self):
        ''' generate_user_invitations should succeed if invitation was requested previously,
            and generate the number of invitations requested (if that number of requests
            was registered previously, of course) '''
        email1='test_generate_user_invitations_success_previously_requested_invitation1@komlog.org'
        email2='test_generate_user_invitations_success_previously_requested_invitation2@komlog.org'
        email3='test_generate_user_invitations_success_previously_requested_invitation3@komlog.org'
        email4='test_generate_user_invitations_success_previously_requested_invitation4@komlog.org'
        email5='test_generate_user_invitations_success_previously_requested_invitation5@komlog.org'
        self.assertTrue(userapi.register_invitation_request(email=email1))
        self.assertTrue(userapi.register_invitation_request(email=email2))
        self.assertTrue(userapi.register_invitation_request(email=email3))
        self.assertTrue(userapi.register_invitation_request(email=email4))
        self.assertTrue(userapi.register_invitation_request(email=email5))
        invitations=userapi.generate_user_invitations(num=5)
        self.assertEqual(len(invitations),5)
        for invitation in invitations:
            self.assertTrue(args.is_valid_email(invitation['email']))
            self.assertTrue(isinstance(invitation['inv_id'],uuid.UUID))

    def test_create_user_by_invitation_failure_non_existent_invitation(self):
        username='username'
        password='password'
        email=username+'@komlog.org'
        inv_id=uuid.uuid4()
        with self.assertRaises(exceptions.InvitationNotFoundException) as cm:
            userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_SIP_INVNF)

    def test_create_user_by_invitation_success(self):
        username='test_create_user_by_invitation_success'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        user_info=userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id)
        self.assertEqual(user_info['username'],username)
        self.assertEqual(user_info['email'],email)
        self.assertTrue('uid' in user_info)
        self.assertTrue('code' in user_info)

    def test_create_user_by_invitation_failure_already_used_invitation(self):
        username='test_create_user_by_invitation_failure_already_used_invitation'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        user_info=userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id)
        self.assertEqual(user_info['username'],username)
        self.assertEqual(user_info['email'],email)
        self.assertTrue('uid' in user_info)
        self.assertTrue('code' in user_info)
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_SIP_INVAU)

    def test_create_user_by_invitation_success_in_segment_with_cost(self):
        ''' create_user_by_invitation should succeed creating a user in a segment with cost '''
        username = 'test_create_user_by_invitation_success_in_segment_with_cost'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        user=userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id, sid=sid, token=token.id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['segment'], sid)

    def test_create_user_by_invitation_success_in_second_try_in_segment_with_cost(self):
        ''' create_user_by_invitation should succeed creating a user in a segment with cost. If first try failed, the invitation should be reseted to allow more tries. '''
        username = 'test_create_user_by_invitation_success_in_second_try_in_segment_with_cost'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id, sid=sid, token=None)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CRU_TOKNEED)
        #now use the token
        user=userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id, sid=sid, token=token.id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        self.assertEqual(user['segment'], sid)

    def test_start_invitation_process_failure_invalid_invitation_id(self):
        ''' start_invitation_process should fail if inv_id is invalid '''
        inv_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        for inv_id in inv_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.start_invitation_process(inv_id=inv_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_SIP_IINV)

    def test_start_invitation_process_failure_invitation_not_found(self):
        ''' start_invitation_process should fail if inv_id is not found '''
        inv_id=uuid.uuid4()
        with self.assertRaises(exceptions.InvitationNotFoundException) as cm:
            userapi.start_invitation_process(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_SIP_INVNF)

    def test_start_invitation_process_failure_already_used_invitation(self):
        username='test_start_invitation_process_failure_already_used_invitation'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        user_info=userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id)
        self.assertEqual(user_info['username'],username)
        self.assertEqual(user_info['email'],email)
        self.assertTrue('uid' in user_info)
        self.assertTrue('code' in user_info)
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.start_invitation_process(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_SIP_INVAU)

    def test_start_invitation_process_failure_invitation_state_not_expected(self):
        username='test_start_invitation_process_failure_already_used_invitation'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        invitation_info[0].tran_id=uuid.uuid4()
        self.assertTrue(cassapiuser.insert_invitation_info(invitation_info[0]))
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.start_invitation_process(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_SIP_ISNE)

    def test_start_invitation_process_success(self):
        username='test_start_invitation_process_success'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        tran_id=userapi.start_invitation_process(inv_id=inv_id)
        self.assertTrue(isinstance(tran_id,uuid.UUID))
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        found=False
        for reg in invitation_info:
            if reg.state==InvitationStates.USING and reg.tran_id==tran_id:
                found=True
        self.assertTrue(found)

    def test_end_invitation_process_failure_invalid_invitation_id(self):
        ''' end_invitation_process should fail if inv_id is invalid '''
        inv_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        tran_id=uuid.uuid4()
        for inv_id in inv_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_EIP_IINV)

    def test_end_invitation_process_failure_invalid_transaction_id(self):
        ''' end_invitation_process should fail if transaction id is invalid '''
        tran_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        inv_id=uuid.uuid4()
        for tran_id in tran_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_EIP_ITRN)

    def test_end_invitation_process_failure_invitation_not_found(self):
        ''' end_invitation_process should fail if invitation does not exist '''
        tran_id=uuid.uuid4()
        inv_id=uuid.uuid4()
        with self.assertRaises(exceptions.InvitationNotFoundException) as cm:
            userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_EIP_INVNF)

    def test_end_invitation_process_failure_invitation_not_used(self):
        ''' end_invitation_process should fail if invitation is unused '''
        email='test_end_invitation_process_failure_invitation_not_used@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        tran_id=uuid.uuid4()
        inv_id=invitations[0]['inv_id']
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_EIP_INUE)

    def test_end_invitation_process_failure_race_condition_found(self):
        ''' end_invitation_process should fail if invitation is being used already by other process '''
        email='test_end_invitation_process_failure_race_condition_found@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        tran_id=uuid.uuid4()
        inv_id=invitations[0]['inv_id']
        other_transaction=userapi.start_invitation_process(inv_id=inv_id)
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_EIP_RCF)

    def test_end_invitation_process_failure_no_using_state_found(self):
        ''' end_invitation_process should fail if invitation is inconsistent and no using state is found '''
        email='test_end_invitation_process_failure_no_using_state_found@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        tran_id=uuid.uuid4()
        inv_id=invitations[0]['inv_id']
        other_transaction=userapi.start_invitation_process(inv_id=inv_id)
        userapi.end_invitation_process(inv_id=inv_id,tran_id=other_transaction)
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(invitation_info),3)
        for reg in invitation_info:
            if reg.state==InvitationStates.USING:
                cassapiuser.delete_invitation_info(inv_id=inv_id, date=reg.date)
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_EIP_SNF)

    def test_end_invitation_process_success(self):
        ''' end_invitation_process should succeed '''
        email='test_end_invitation_process_success@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        tran_id=userapi.start_invitation_process(inv_id=inv_id)
        self.assertTrue(userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id))

    def test_undo_invitation_transactions_failure_invalid_inv_id(self):
        ''' undo_invitation_transactions should fail if inv_id is invalid '''
        inv_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        tran_id=uuid.uuid4()
        for inv_id in inv_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.undo_invitation_transactions(inv_id=inv_id,tran_id=tran_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_UIT_IINV)

    def test_undo_invitation_transactions_failure_invalid_transaction_id(self):
        ''' undo_invitation_transactions should fail if transaction id is invalid '''
        tran_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        inv_id=uuid.uuid4()
        for tran_id in tran_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.undo_invitation_transactions(inv_id=inv_id,tran_id=tran_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_UIT_ITRN)

    def test_undo_invitation_transaction_failure_invitation_info_not_found(self):
        ''' undo_invitation_transaction should fail if invitation info is not found '''
        tran_id=uuid.uuid4()
        inv_id=uuid.uuid4()
        with self.assertRaises(exceptions.InvitationNotFoundException) as cm:
            userapi.undo_invitation_transactions(inv_id=inv_id,tran_id=tran_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_UIT_INVNF)

    def test_undo_invitation_transactions_success(self):
        ''' undo_invitation_transactions should succeed '''
        email='test_undo_invitation_transactions_success@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        tran_id=userapi.start_invitation_process(inv_id=inv_id)
        userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(invitation_info),3)
        self.assertTrue(userapi.undo_invitation_transactions(inv_id=inv_id, tran_id=tran_id))
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(invitation_info),1)

    def test_initialize_invitation_failure_invalid_inv_id(self):
        ''' initialize_invitation should fail if inv_id is invalid '''
        inv_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        for inv_id in inv_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.initialize_invitation(inv_id=inv_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_II_IINV)

    def test_initialize_invitation_failure_invitation_info_not_found(self):
        ''' initialize_invitation should fail if invitation info is not found '''
        inv_id=uuid.uuid4()
        with self.assertRaises(exceptions.InvitationNotFoundException) as cm:
            userapi.initialize_invitation(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_II_INVNF)

    def test_initialize_invitation_success(self):
        ''' initialize_invitation should succeed '''
        email='test_initialize_invitation_success@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        tran_id=userapi.start_invitation_process(inv_id=inv_id)
        userapi.end_invitation_process(inv_id=inv_id,tran_id=tran_id)
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(invitation_info),3)
        self.assertTrue(userapi.initialize_invitation(inv_id=inv_id))
        invitation_info_2=cassapiuser.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(invitation_info_2),1)
        self.assertEqual(invitation_info_2[0].state, InvitationStates.UNUSED)

    def test_check_unused_invitation_failure_invalid_invitation_id(self):
        ''' check_unused_invitation should fail if inv_id is invalid '''
        inv_ids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        for inv_id in inv_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.check_unused_invitation(inv_id=inv_id)
            self.assertEqual(cm.exception.error, Errors.E_GUA_CUI_IINV)

    def test_check_unused_invitation_failure_invitation_not_found(self):
        ''' check_unused_invitation should fail if inv_id is not found '''
        inv_id=uuid.uuid4()
        with self.assertRaises(exceptions.InvitationNotFoundException) as cm:
            userapi.check_unused_invitation(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CUI_INVNF)

    def test_check_unused_invitation_failure_invitation_already_used(self):
        ''' check_unused_invitation should fail if inv_id is already used '''
        username='test_check_unused_invitation_failure_already_used_invitation'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        user_info=userapi.create_user_by_invitation(username=username, password=password, email=email, inv_id=inv_id)
        self.assertEqual(user_info['username'],username)
        self.assertEqual(user_info['email'],email)
        self.assertTrue('uid' in user_info)
        self.assertTrue('code' in user_info)
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.check_unused_invitation(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CUI_INVAU)

    def test_check_unused_invitation_failure_invitation_state_invalid(self):
        ''' check_unused_invitation should fail if invitation state is invalid '''
        username='test_check_unused_invitation_failure_invitation_state_invalid'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        invitation_info=cassapiuser.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(invitation_info),1)
        for reg in invitation_info:
            if reg.state==InvitationStates.UNUSED:
                cassapiuser.delete_invitation_info(inv_id=inv_id, date=reg.date)
                reg.state=InvitationStates.USING
                cassapiuser.insert_invitation_info(reg)
        with self.assertRaises(exceptions.InvitationProcessException) as cm:
            userapi.check_unused_invitation(inv_id=inv_id)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CUI_INVIS)

    def test_check_unused_invitation_success(self):
        ''' check_unused_invitation should succeed '''
        username='test_check_unused_invitation_success'
        password='temporal'
        email=username+'@komlog.org'
        invitations=userapi.generate_user_invitations(email=email)
        inv_id=invitations[0]['inv_id']
        self.assertTrue(userapi.check_unused_invitation(inv_id=inv_id))

    def test_register_forget_request_failure_invalid_username(self):
        ''' register_forget_request should fail if username is invalid '''
        usernames=[34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4(), uuid.uuid1(),'email@fake','@badmail','fake@']
        for username in usernames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.register_forget_request(username=username)
            self.assertEqual(cm.exception.error,Errors.E_GUA_RFR_IU)

    def test_register_forget_request_failure_invalid_email(self):
        ''' register_forget_request should fail if email is invalid '''
        emails=[34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4(), uuid.uuid1(),'email@fake','@badmail','fake@']
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.register_forget_request(email=email)
            self.assertEqual(cm.exception.error,Errors.E_GUA_RFR_IEMAIL)

    def test_register_forget_request_failure_no_parameter_passed(self):
        ''' register_forget_request should fail if username and email are None '''
        with self.assertRaises(exceptions.BadParametersException) as cm:
            userapi.register_forget_request()
        self.assertEqual(cm.exception.error,Errors.E_GUA_RFR_NPP)

    def test_register_forget_request_failure_non_existing_user(self):
        ''' register_forget_request should fail if user does not exist '''
        username='test_register_forget_request_failure_non_existing_user'
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            userapi.register_forget_request(username=username)
        self.assertEqual(cm.exception.error,Errors.E_GUA_RFR_UNF)

    def test_register_forget_request_success_passing_username(self):
        ''' register_forget_request should succeed if we pass username '''
        username = 'test_register_forget_request_success_passing_username'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        forget_request=userapi.register_forget_request(username=username)
        self.assertTrue('code' in forget_request)
        self.assertTrue('username' in forget_request)
        self.assertTrue('email' in forget_request)
        self.assertTrue('uid' in forget_request)
        self.assertTrue(isinstance(forget_request['code'], uuid.UUID))
        self.assertEqual(forget_request['username'], username)
        self.assertEqual(forget_request['email'], email)
        self.assertEqual(forget_request['uid'],userinfo['uid'])

    def test_register_forget_request_success_passing_email(self):
        ''' register_forget_request should succeed if we pass username '''
        username = 'test_register_forget_request_success_passing_email'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        forget_request=userapi.register_forget_request(email=email)
        self.assertTrue('code' in forget_request)
        self.assertTrue('username' in forget_request)
        self.assertTrue('email' in forget_request)
        self.assertTrue('uid' in forget_request)
        self.assertTrue(isinstance(forget_request['code'], uuid.UUID))
        self.assertEqual(forget_request['username'], username)
        self.assertEqual(forget_request['email'], email)
        self.assertEqual(forget_request['uid'],userinfo['uid'])

    def test_check_unused_forget_code_failure_invalid_code(self):
        ''' check_unused_forget_code should fail if code is invalid '''
        codes=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        for code in codes:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.check_unused_forget_code(code=code)
            self.assertEqual(cm.exception.error, Errors.E_GUA_CUFC_ICODE)

    def test_check_unused_forget_code_failure_non_existent_code(self):
        ''' check_unused_forget_code should fail if code does not exist '''
        code=uuid.uuid4()
        with self.assertRaises(exceptions.ForgetRequestNotFoundException) as cm:
            userapi.check_unused_forget_code(code=code)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CUFC_CNF)

    def test_check_unused_forget_code_failure_used_code(self):
        ''' check_unused_forget_code should fail if code is already used '''
        username = 'test_check_unused_forget_code_failure_already_used_code'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        forget_request=userapi.register_forget_request(username=username)
        self.assertTrue('code' in forget_request)
        self.assertTrue('username' in forget_request)
        self.assertTrue('email' in forget_request)
        self.assertTrue('uid' in forget_request)
        self.assertTrue(isinstance(forget_request['code'], uuid.UUID))
        self.assertEqual(forget_request['username'], username)
        self.assertEqual(forget_request['email'], email)
        self.assertEqual(forget_request['uid'],userinfo['uid'])
        code=forget_request['code']
        self.assertTrue(cassapiuser.update_forget_request_state(code=code, new_state=ForgetRequestStates.USED))
        with self.assertRaises(exceptions.ForgetRequestException) as cm:
            userapi.check_unused_forget_code(code=code)
        self.assertEqual(cm.exception.error, Errors.E_GUA_CUFC_CODEAU)

    def test_check_unused_forget_code_success(self):
        ''' check_unused_forget_code should succeed '''
        username = 'test_check_unused_forget_code_success'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        forget_request=userapi.register_forget_request(username=username)
        self.assertTrue('code' in forget_request)
        self.assertTrue('username' in forget_request)
        self.assertTrue('email' in forget_request)
        self.assertTrue('uid' in forget_request)
        self.assertTrue(isinstance(forget_request['code'], uuid.UUID))
        self.assertEqual(forget_request['username'], username)
        self.assertEqual(forget_request['email'], email)
        self.assertEqual(forget_request['uid'],userinfo['uid'])
        code=forget_request['code']
        self.assertTrue(userapi.check_unused_forget_code(code=code))

    def test_reset_password_failure_invalid_code(self):
        ''' reset_password should fail if code is not valid '''
        codes=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'userÑame', uuid.uuid4().hex, uuid.uuid1(),'email@fake','@badmail','fake@']
        password = 'password'
        for code in codes:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.reset_password(code=code, password=password)
            self.assertEqual(cm.exception.error, Errors.E_GUA_RP_ICODE)

    def test_reset_password_failure_invalid_password(self):
        ''' reset_password should fail if password is not valid '''
        passwords=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), uuid.uuid4(), uuid.uuid1(),'short']
        code=uuid.uuid4()
        for password in passwords:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.reset_password(code=code, password=password)
            self.assertEqual(cm.exception.error, Errors.E_GUA_RP_IPWD)

    def test_reset_password_failure_code_not_found(self):
        ''' reset_password should fail if code does not exist on system '''
        code=uuid.uuid4()
        password='temporal'
        with self.assertRaises(exceptions.ForgetRequestNotFoundException) as cm:
            userapi.reset_password(code=code, password=password)
        self.assertEqual(cm.exception.error, Errors.E_GUA_RP_CNF)

    def test_reset_password_failure_code_already_used(self):
        ''' reset_password should fail if code is already used '''
        username = 'test_reset_password_failure_code_already_used'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        forget_request=userapi.register_forget_request(username=username)
        self.assertTrue('code' in forget_request)
        self.assertTrue('username' in forget_request)
        self.assertTrue('email' in forget_request)
        self.assertTrue('uid' in forget_request)
        self.assertTrue(isinstance(forget_request['code'], uuid.UUID))
        self.assertEqual(forget_request['username'], username)
        self.assertEqual(forget_request['email'], email)
        self.assertEqual(forget_request['uid'],userinfo['uid'])
        new_password='temporal2'
        code=forget_request['code']
        self.assertTrue(userapi.reset_password(code=code, password=new_password))
        self.assertTrue(userapi.auth_user(username, new_password))
        new_password='temporal3'
        with self.assertRaises(exceptions.ForgetRequestException) as cm:
            userapi.reset_password(code=code, password=new_password)
        self.assertEqual(cm.exception.error, Errors.E_GUA_RP_CODEAU)
        self.assertFalse(userapi.auth_user(username, new_password))

    def test_reset_password_success(self):
        ''' reset_password should succeed '''
        username = 'test_reset_password_failure_success'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        forget_request=userapi.register_forget_request(username=username)
        self.assertTrue('code' in forget_request)
        self.assertTrue('username' in forget_request)
        self.assertTrue('email' in forget_request)
        self.assertTrue('uid' in forget_request)
        self.assertTrue(isinstance(forget_request['code'], uuid.UUID))
        self.assertEqual(forget_request['username'], username)
        self.assertEqual(forget_request['email'], email)
        self.assertEqual(forget_request['uid'],userinfo['uid'])
        new_password='temporal2'
        code=forget_request['code']
        self.assertTrue(userapi.reset_password(code=code, password=new_password))
        self.assertTrue(userapi.auth_user(username, new_password))

    def test_register_pending_hook_failure_invalid_uid(self):
        ''' register_pending_hook should fail if uid is invalid '''
        uids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uri='uri'
        sid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.register_pending_hook(uid=uid, uri=uri, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_RPH_IUID)

    def test_register_pending_hook_failure_invalid_uri(self):
        ''' register_pending_hook should fail if uri is invalid '''
        uris=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), ' invalid uri ', uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        sid=uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.register_pending_hook(uid=uid, uri=uri, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_RPH_IURI)

    def test_register_pending_hook_failure_invalid_sid(self):
        ''' register_pending_hook should fail if sid is invalid '''
        sids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uri='uri'
        uid=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.register_pending_hook(uid=uid, uri=uri, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_RPH_ISID)

    def test_register_pending_hook_failure_non_existent_user(self):
        ''' register_pending_hook should fail if user does not exist '''
        uri='uri'
        uid=uuid.uuid4()
        sid=uuid.uuid4()
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            userapi.register_pending_hook(uid=uid, uri=uri, sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_GUA_RPH_UNF)

    def test_register_pending_hook_success(self):
        ''' register_pending_hook should succeed and insert the pending hook successfully '''
        uri='uri'
        uid=self.userinfo['uid']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=uri, sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [sid])

    def test_get_uri_pending_hooks_failure_invalid_uid(self):
        ''' get_uri_pending_hooks should fail if uid is invalid '''
        uids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uri='uri'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.get_uri_pending_hooks(uid=uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_GUA_GUPH_IUID)

    def test_get_uri_pending_hooks_failure_invalid_uri(self):
        ''' get_uri_pending_hooks should fail if uri is invalid '''
        uris=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'invalid uri ', uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.get_uri_pending_hooks(uid=uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_GUA_GUPH_IURI)

    def test_get_uri_pending_hooks_success_none_found(self):
        ''' get_uri_pending_hooks should return an empty list if no pending hooks are found '''
        uid=uuid.uuid4()
        uri='test_get_uri_pending_hooks_success_none_found'
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid, uri=uri),[])

    def test_get_uri_pending_hooks_success_some_found(self):
        ''' get_uri_pending_hooks should return a list with the pending hooks sids '''
        username = 'test_get_uri_pending_hooks_success_some_found'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        uri='uri'
        uid=userinfo['uid']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=uri, sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [sid])

    def test_delete_session_pending_hooks_failure_invalid_sid(self):
        ''' delete_session_pending_hooks should fail if sid is invalid '''
        sids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.delete_session_pending_hooks(sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_DSPH_ISID)

    def test_delete_session_pending_hooks_success_no_previous_hook_existed(self):
        ''' delete_session_pending_hooks should succeed even if no previous hook existed '''
        sid=uuid.uuid4()
        self.assertTrue(userapi.delete_session_pending_hooks(sid=sid))

    def test_delete_session_pending_hooks_success_previous_hook_existed(self):
        ''' delete_session_pending_hooks should succeed if hook existed '''
        username = 'test_delete_session_pending_hooks_success_previous_hook_existed'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        uri='uri'
        uid=userinfo['uid']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=uri, sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [sid])
        self.assertTrue(userapi.delete_session_pending_hooks(sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [])

    def test_delete_uri_pending_hooks_failure_invalid_uid(self):
        ''' delete_uri_pending_hooks should fail if uid is invalid '''
        uids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uri='uri'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.delete_uri_pending_hooks(uid=uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_GUA_DUPH_IUID)

    def test_delete_uri_pending_hooks_failure_invalid_uri(self):
        ''' delete_uri_pending_hooks should fail if uri is invalid '''
        uris=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'invalid uri', uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.delete_uri_pending_hooks(uid=uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_GUA_DUPH_IURI)

    def test_delete_uri_pending_hooks_success_no_previous_hook_existed(self):
        ''' delete_uri_pending_hooks should succeed even if no previous hook existed '''
        uid=uuid.uuid4()
        uri='test_delete_uri_pending_hooks_success_no_previous_hook_existed'
        self.assertTrue(userapi.delete_uri_pending_hooks(uid=uid, uri=uri))

    def test_delete_uri_pending_hooks_success_previous_hook_existed(self):
        ''' delete_uri_pending_hooks should succeed if previous hook existed '''
        username = 'test_delete_uri_pending_hooks_success_previous_hook_existed'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        uri='test_delete_uri_pending_hooks_success_previous_hook_existed'
        uid=userinfo['uid']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=uri, sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [sid])
        self.assertTrue(userapi.delete_uri_pending_hooks(uid=uid, uri=uri))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [])

    def test_delete_pending_hook_failure_invalid_uid(self):
        ''' delete_uri_pending_hooks should fail if uid is invalid '''
        uids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uri='uri'
        sid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.delete_pending_hook(uid=uid, uri=uri, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_DPH_IUID)

    def test_delete_pending_hook_failure_invalid_uri(self):
        ''' delete_uri_pending_hooks should fail if uri is invalid '''
        uris=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'invalid uri', uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        sid=uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.delete_pending_hook(uid=uid, uri=uri, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_DPH_IURI)

    def test_delete_pending_hook_failure_invalid_sid(self):
        ''' delete_uri_pending_hooks should fail if sid is invalid '''
        sids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uri='uri'
        uid=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.delete_pending_hook(uid=uid, uri=uri, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_DPH_ISID)

    def test_delete_pending_hook_success_no_previous_hook_existed(self):
        ''' delete_pending_hook should succeed even if no previous hook existed '''
        uid=uuid.uuid4()
        sid=uuid.uuid4()
        uri='test_delete_pending_hook_success_no_previous_hook_existed'
        self.assertTrue(userapi.delete_pending_hook(uid=uid, uri=uri, sid=sid))

    def test_delete_pending_hook_success_previous_hook_existed(self):
        ''' delete_pending_hook should succeed if previous hook existed '''
        username = 'test_delete_pending_hook_success_previous_hook_existed'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['code'])
        uri='test_delete_pending_hook_success_previous_hook_existed'
        uid=userinfo['uid']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=uri, sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [sid])
        self.assertTrue(userapi.delete_pending_hook(uid=uid, uri=uri, sid=sid))
        pending_hooks=userapi.get_uri_pending_hooks(uid=uid, uri=uri)
        self.assertEqual(pending_hooks, [])

    def test_update_segment_failure_invalid_uid(self):
        ''' update_segment should fail if uid is not valid '''
        uids=[None, 34234, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        sid = 0
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.update_segment(uid=uid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_UPDSEG_IUID)

    def test_update_segment_failure_invalid_sid(self):
        ''' update_segment should fail if sid is not valid '''
        sids=[None, 2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), 'username', uuid.uuid4().hex, uuid.uuid1()]
        uid = uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.update_segment(uid=uid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GUA_UPDSEG_ISID)

    def test_update_segment_failure_invalid_token(self):
        ''' update_segment should fail if token is not valid '''
        tokens=[2342.234234, {'a':'dict'}, ['a','list'], {'set'}, ('a','tuple'), uuid.uuid4(), uuid.uuid1()]
        uid = uuid.uuid4()
        sid = 0
        for token in tokens:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                userapi.update_segment(uid=uid, sid=sid, token=token)
            self.assertEqual(cm.exception.error, Errors.E_GUA_UPDSEG_ITOK)

    def test_update_segment_failure_user_not_found(self):
        ''' update_segment should fail if user does not exist '''
        uid = uuid.uuid4()
        sid = 0
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            userapi.update_segment(uid=uid, sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_GUA_UPDSEG_UNF)

    def test_update_segment_failure_segment_not_found(self):
        ''' update_segment should fail if segment does not exist '''
        username = 'test_update_segment_failure_segment_not_found'
        password = 'password'
        email = username+'@komlog.org'
        sid = 0
        userinfo = userapi.create_user(username=username, password=password, email=email, sid=sid)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        new_sid = 99239243
        with self.assertRaises(exceptions.BadParametersException) as cm:
            userapi.update_segment(uid=userinfo['uid'], sid=new_sid)
        self.assertEqual(cm.exception.error, Errors.E_GUA_UPDSEG_SEGNF)

    def test_update_segment_failure_token_needed(self):
        ''' update_segment should fail if user transitions to a paid segment and has no payment info '''
        username = 'test_update_segment_failure_token_needed'
        password = 'password'
        email = username+'@komlog.org'
        sid = 0
        userinfo = userapi.create_user(username=username, password=password, email=email, sid=sid)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        new_sid = 1
        with self.assertRaises(exceptions.BadParametersException) as cm:
            userapi.update_segment(uid=userinfo['uid'], sid=new_sid)
        self.assertEqual(cm.exception.error, Errors.E_GUA_UPDSEG_TOKNEED)

    def test_update_segment_success_creating_customer_with_token(self):
        ''' update_segment should succeed modifying the user's segment. If user has no payment info before, the new info should be created. '''
        username = 'test_update_segment_success_creating_customer_with_token'
        password = 'password'
        email = username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        self.assertTrue(userapi.update_segment(uid=user['uid'], sid=sid, token=token.id))
        new_user_config = userapi.get_user_config(uid=user['uid'])
        self.assertEqual(new_user_config['segment'], sid)

    def test_update_segment_success_without_token_keeping_customer_info(self):
        ''' update_segment should succeed modifying the user's segment. If user has already payment info and no token is passed, then keep that info. '''
        username = 'test_update_segment_success_without_token_keeping_customer_info'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        user=userapi.create_user(username=username, password=password, email=email, sid=sid, token=token.id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        new_sid = 2
        for new_sid in [2,3,0]:
            self.assertTrue(userapi.update_segment(uid=user['uid'], sid=new_sid))
            new_user_config = userapi.get_user_config(uid=user['uid'])
            self.assertEqual(new_user_config['segment'], new_sid)

    def test_update_segment_success_with_token_updating_customer_info(self):
        ''' update_segment should succeed modifying the user's segment. If user has already payment info and token is passed, then update customer info. '''
        username = 'test_update_segment_success_with_token_updating_customer_info'
        password = 'password'
        email = username+'@komlog.org'
        sid = 1
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        user=userapi.create_user(username=username, password=password, email=email, sid=sid, token=token.id)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['username'], username)
        new_sid = 2
        for new_sid in [2,3,0]:
            token = stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 12,
                    "exp_year": 2017,
                    "cvc": '123'
                },
            )
            self.assertTrue(userapi.update_segment(uid=user['uid'], sid=new_sid, token=token.id))
            new_user_config = userapi.get_user_config(uid=user['uid'])
            self.assertEqual(new_user_config['segment'], new_sid)

