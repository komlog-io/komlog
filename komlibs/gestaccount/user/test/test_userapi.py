import unittest
from komlibs.gestaccount.user import api
from komlibs.gestaccount import exceptions

class GestaccountUserApiTest(unittest.TestCase):
    ''' komlog.gestaccount.user.api tests '''

    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.email = 'test_user@komlog.org'
        self.code = 'RANDOMCODE'
        self.user = None

    def test_create_user(self):
        ''' create_user should insert the user in the database '''
        if not self.user:
            self.user = api.create_user(username=self.username, password=self.password, email=self.email)
        self.assertEqual(self.username, self.user.username)
        self.assertEqual(api.get_hpassword(self.user.uid,self.password), self.user.password)
        self.assertEqual(self.email, self.user.email)

    def test_auth_user(self):
        ''' auth_user should authenticate the user '''
        if not self.user:
            self.user = api.create_user(username=self.username, password=self.password, email=self.email)
        result=api.auth_user(self.username, self.password)
        self.assertTrue(result)

    def test_update_user_profile_empty_email_param(self):
        ''' update_user_profile shoud fail if email received is None'''
        params={'email':None}
        self.assertRaises(exceptions.BadParametersException, api.update_user_profile, username=self.username, params=params)

    def test_update_user_profile_empty_new_password_param(self):
        ''' update_user_profile shoud fail if new_password received is None '''
        params={'new_password':None, 'old_password':self.password}
        self.assertRaises(exceptions.BadParametersException, api.update_user_profile, username=self.username, params=params)

    def test_update_user_profile_empty_old_password_param(self):
        ''' update_user_profile shoud fail if old_password received is None'''
        params={'old_password':None, 'new_password':self.password}
        self.assertRaises(exceptions.BadParametersException, api.update_user_profile, username=self.username, params=params)

    def test_update_user_profile_only_new_password_param(self):
        ''' update_user_profile shoud fail if only new_password is received '''
        params={'new_password':'the new password'}
        self.assertRaises(exceptions.BadParametersException, api.update_user_profile, username=self.username, params=params)

    def test_update_user_profile_only_old_password_param(self):
        ''' update_user_profile shoud fail if only old_password is received '''
        params={'old_password':'the old password'}
        self.assertRaises(exceptions.BadParametersException, api.update_user_profile, username=self.username, params=params)

    def test_update_user_profile_same_passwords(self):
        ''' update_user_profile shoud fail if old_password is equal to new_password '''
        params={'old_password':self.password, 'new_password':self.password}
        self.assertRaises(exceptions.BadParametersException, api.update_user_profile, username=self.username, params=params)

    def test_update_user_profile_already_existing_email(self):
        ''' update_user_profile shoud fail if email is already on system '''
        username2='test_update_user_profile_already_existing_email'
        password2='password_2'
        email2='test_update_user_profile_already_existing_email@komlog.org'
        user2 = api.create_user(username=username2,password=password2,email=email2)
        params={'email':email2}
        self.assertRaises(exceptions.EmailAlreadyExistsException, api.update_user_profile, username=self.username, params=params)

    def test_get_user_profile(self):
        ''' get_user_profile should return user data '''
        if not self.user:
            self.user=api.create_user(username=self.username, password=self.password, email=self.email)
        self.assertIsNotNone(api.get_user_profile(username=self.username))

    def test_get_user_profile_non_existing_username(self):
        ''' get_user_profile should fail if username does not exist '''
        username='This_user_3423_shouLD_nOt_exist'
        self.assertRaises(exceptions.UserNotFoundException, api.get_user_profile, username=username)
