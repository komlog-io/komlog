import unittest
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount import exceptions

class GestaccountUserApiTest(unittest.TestCase):
    ''' komlog.gestaccount.user.api tests '''

    def setUp(self):
        self.username = 'test_komlog.gestaccount.user.api_user'
        self.password = 'test_password'
        self.email = self.username+'@komlog.org'
        try:
            self.userinfo=userapi.get_user_config(username=self.username)
        except Exception:
            self.userinfo=userapi.create_user(username=self.username, password=self.password, email=self.email)
        code = 'RANDOMCODE'

    def test_create_user(self):
        ''' create_user should insert the user in the database '''
        username = 'test_create_user_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(username, userinfo['username'])
        self.assertEqual(email, userinfo['email'])
        self.assertIsNotNone(userinfo['signup_code'])

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
        self.assertTrue(userapi.confirm_user(email=userinfo['email'], code=userinfo['signup_code']))

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
        self.assertRaises(exceptions.UserNotFoundException, userapi.confirm_user, email=email, code=userinfo['signup_code'])

    def test_confirm_user_failure_already_used_code(self):
        ''' confirm_user should modify user state if we pass a valid email and code '''
        username = 'test_confirm_user_failure_already_used_code_user'
        password = 'password'
        email = username+'@komlog.org'
        userinfo = userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(userapi.confirm_user(email=userinfo['email'], code=userinfo['signup_code']))
        self.assertRaises(exceptions.UserConfirmationException, userapi.confirm_user, email=userinfo['email'], code=userinfo['signup_code'])

    def test_update_user_config_no_params(self):
        ''' update_user_config shoud fail if no params is passed'''
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, username=self.username)

    def test_update_user_config_empty_only_old_password_param(self):
        ''' update_user_config shoud fail if only old_password is passed '''
        old_password=self.password
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, username=self.username, old_password=old_password)

    def test_update_user_config_empty_only_new_password_param(self):
        ''' update_user_config shoud fail if only new_password is received '''
        new_password='new_password'
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, username=self.username, new_password=new_password)

    def test_update_user_config_same_passwords(self):
        ''' update_user_config shoud fail if old_password is equal to new_password '''
        old_password=self.password
        new_password=self.password
        self.assertRaises(exceptions.BadParametersException, userapi.update_user_config, username=self.username, old_password=old_password, new_password=new_password)

    def test_update_user_config_already_existing_email(self):
        ''' update_user_config shoud fail if email is already on system '''
        username2='test_update_user_config_already_existing_email'
        password2='password_2'
        email2='test_update_user_config_already_existing_email@komlog.org'
        user2 = userapi.create_user(username=username2,password=password2,email=email2)
        email=email2
        self.assertRaises(exceptions.EmailAlreadyExistsException, userapi.update_user_config, username=self.username, new_email=email)

    def test_update_user_config_success_different_passwords(self):
        ''' update_user_config shoud succeed if old_password is different to new_password and old_password is correct'''
        old_password=self.password
        new_password='the_new_pass'
        self.assertTrue(userapi.update_user_config(username=self.username, old_password=old_password, new_password=new_password))

    def test_get_user_config_success(self):
        ''' get_user_config should return user data '''
        data=userapi.get_user_config(username=self.username)
        self.assertIsNotNone(data)
        self.assertEqual(self.username, data['username'])
        self.assertEqual(self.email, data['email'])

    def test_get_user_config_non_existing_username(self):
        ''' get_user_config should fail if username does not exist '''
        username='test_get_user_config_non_existing_username_user'
        self.assertRaises(exceptions.UserNotFoundException, userapi.get_user_config, username=username)

