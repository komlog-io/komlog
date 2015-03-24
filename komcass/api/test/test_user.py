import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.api import user as userapi
from komcass.model.orm import user as ormuser
from komcass.model.statement import user as stmtuser
from komcass import connection


class KomcassApiUserTest(unittest.TestCase):
    ''' komlog.komcass.api.user tests '''

    def setUp(self):
        username='test_komlog.komcass.api.user_user'
        password='password'
        email=username+'@komlog.org'
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        code='test_komlog.komcass.api.user_code'
        self.user=ormuser.User(username=username, password=password, email=email, uid=uid, creation_date=creation_date)
        self.signup_info=ormuser.SignUp(username=username, signup_code=code, email=email, creation_date=creation_date)
        userapi.insert_user(self.user)
        userapi.insert_signup_info(self.signup_info)

    def test_get_user_no_arguments(self):
        ''' get_user should return None if no argument is passed '''
        self.assertIsNone(userapi.get_user())

    def test_get_user_existing_username(self):
        ''' get_user should succeed if we pass an existing username '''
        username=self.user.username
        user=userapi.get_user(username=username)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.password, self.user.password)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.uid, self.user.uid)

    def test_get_user_non_existing_username(self):
        ''' get_user should return None if we pass a non existing username '''
        username='test_get_user_non_existing_username'
        self.assertIsNone(userapi.get_user(username=username))

    def test_get_user_existing_uid(self):
        ''' get_user should succeed if we pass an existing uid '''
        uid=self.user.uid
        user=userapi.get_user(uid=uid)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.password, self.user.password)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.uid, self.user.uid)

    def test_get_user_non_existing_uid(self):
        ''' get_user should return None if we pass a non existing uid '''
        uid=uuid.uuid4()
        self.assertIsNone(userapi.get_user(uid=uid))

    def test_get_user_existing_email(self):
        ''' get_user should succeed if we pass an existing email '''
        email=self.user.email
        user=userapi.get_user(email=email)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.password, self.user.password)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.uid, self.user.uid)

    def test_get_user_non_existing_email(self):
        ''' get_user should return None if we pass a non existing email '''
        email='test_get_user_non_existing_email@komlog.org'
        self.assertIsNone(userapi.get_user(email=email))

    def test_new_user_no_user_object(self):
        '''' new_user should fail if no user Object is passed as argument '''
        users=[None,234234,'a',{'a':'dict'},['a','list']]
        for user in users:
            self.assertFalse(userapi.new_user(user))

    def test_new_user_success(self):
        '''' new_user should succeed if user is created successfully '''
        username='test_new_user_success_user'
        password='password'
        email=username+'@komlog.org'
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        user=ormuser.User(username=username, password=password, email=email, uid=uid, creation_date=creation_date)
        self.assertTrue(userapi.new_user(user))

    def test_new_user_already_existing_user(self):
        '''' new_user should fail if user is already created '''
        user=self.user
        self.assertFalse(userapi.new_user(user))

    def test_insert_user_no_user_object(self):
        '''' insert_user should fail if no user Object is passed as argument '''
        users=[None,234234,'a',{'a':'dict'},['a','list']]
        for user in users:
            self.assertFalse(userapi.insert_user(user))

    def test_insert_user_success(self):
        '''' new_user should succeed if user is created successfully '''
        username='test_insert_user_success_user'
        password='password'
        email=username+'@komlog.org'
        uid=uuid.uuid4()
        for i in range(1,10):
            creation_date=timeuuid.uuid1()
            user=ormuser.User(username=username, password=password, email=email, uid=uid, creation_date=creation_date)
            self.assertTrue(userapi.insert_user(user))

    def test_delete_user_sucess_by_username(self):
        ''' delete_user should succeed always the query can be executed, independently the user exists or not '''
        username=self.user.username
        self.assertTrue(userapi.delete_user(username=username))
        self.assertIsNone(userapi.get_user(username=username))

    def test_get_signup_info_no_arguments(self):
        ''' get_signup_info should return None if no argument is passed '''
        self.assertIsNone(userapi.get_signup_info())

    def test_get_signup_info_existing_username(self):
        ''' get_signup_info should succeed if we pass an existing username '''
        username=self.signup_info.username
        signup_info=userapi.get_signup_info(username=username)
        self.assertEqual(signup_info.username, self.signup_info.username)
        self.assertEqual(signup_info.email, self.signup_info.email)
        self.assertEqual(signup_info.signup_code, self.signup_info.signup_code)

    def test_get_signup_info_non_existing_username(self):
        ''' get_user should return None if we pass a non existing username '''
        username='test_get_signup_info_non_existing_username'
        self.assertIsNone(userapi.get_signup_info(username=username))

    def test_get_signup_info_existing_code(self):
        ''' get_signup_info should succeed if we pass an existing code '''
        code=self.signup_info.signup_code
        signup_info=userapi.get_signup_info(signup_code=code)
        self.assertEqual(signup_info.username, self.signup_info.username)
        self.assertEqual(signup_info.email, self.signup_info.email)
        self.assertEqual(signup_info.signup_code, self.signup_info.signup_code)

    def test_get_signup_info_non_existing_code(self):
        ''' get_user should return None if we pass a non existing code '''
        code='test_get_signup_info_non_existing_code'
        self.assertIsNone(userapi.get_signup_info(signup_code=code))

    def test_get_signup_info_existing_email(self):
        ''' get_signup_info should succeed if we pass an existing email '''
        email=self.signup_info.email
        signup_info=userapi.get_signup_info(email=email)
        self.assertEqual(signup_info.username, self.signup_info.username)
        self.assertEqual(signup_info.email, self.signup_info.email)
        self.assertEqual(signup_info.signup_code, self.signup_info.signup_code)

    def test_get_signup_info_non_existing_email(self):
        ''' get_user should return None if we pass a non existing email '''
        email='test_get_signup_info_non_existing_email@komlog.org'
        self.assertIsNone(userapi.get_signup_info(email=email))

    def test_insert_signup_info_no_signup_object(self):
        ''' insert_signup_info should return False is signup_info is not a SignUp object '''
        signups=[None, 123123, '2123123123', {'a':'dict'},['a','list']]
        for signup in signups:
            self.assertFalse(userapi.insert_signup_info(signup))

    def test_insert_signup_info_success(self):
        ''' insert_signup_info should succeed if signup object is passed '''
        signup=self.signup_info
        for i in range(1,10):
            signup.creation_date=timeuuid.uuid1()
            self.assertTrue(userapi.insert_signup_info(signup))

    def test_delete_signup_info_sucess_by_username(self):
        ''' delete_signup_info should succeed always, independently the user exists or not, and if exists, delete the user info properly '''
        username=self.signup_info.username
        self.assertTrue(userapi.delete_signup_info(username=username))
        self.assertIsNone(userapi.get_signup_info(username=username))

    def test_get_uid_non_existing_username(self):
        ''' get_uid should return None if username does not exist on system '''
        username='test_get_uid_non_existing_username'
        self.assertIsNone(userapi.get_uid(username=username))

    def test_get_uid_existing_username(self):
        ''' get_uid should return the username's uid if it exists on system '''
        username=self.user.username
        uid=userapi.get_uid(username=username)
        self.assertTrue(isinstance(uid, uuid.UUID))

