import unittest
import uuid
import random
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import user as userapi
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.statement import user as stmtuser
from komlog.komcass import connection


class KomcassApiUserTest(unittest.TestCase):
    ''' komlog.komcass.api.user tests '''

    def setUp(self):
        username='test_komlog.komcass.api.user_user'
        password=b'password'
        email=username+'@komlog.org'
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        code='test_komlog.komcass.api.user_code'
        self.user=ormuser.User(username=username, password=password, email=email, uid=uid, creation_date=creation_date)
        self.signup_info=ormuser.SignUp(username=username, code=code, email=email, creation_date=creation_date)
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
        ''' new_user should fail if no user Object is passed as argument '''
        users=[None,234234,'a',{'a':'dict'},['a','list']]
        for user in users:
            self.assertFalse(userapi.new_user(user))

    def test_new_user_success(self):
        ''' new_user should succeed if user is created successfully '''
        username='test_new_user_success_user'
        password=b'password'
        email=username+'@komlog.org'
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        user=ormuser.User(username=username, password=password, email=email, uid=uid, creation_date=creation_date)
        self.assertTrue(userapi.new_user(user))

    def test_new_user_already_existing_user(self):
        ''' new_user should fail if user is already created '''
        user=self.user
        self.assertFalse(userapi.new_user(user))

    def test_insert_user_no_user_object(self):
        ''' insert_user should fail if no user Object is passed as argument '''
        users=[None,234234,'a',{'a':'dict'},['a','list']]
        for user in users:
            self.assertFalse(userapi.insert_user(user))

    def test_insert_user_success(self):
        ''' new_user should succeed if user is created successfully '''
        username='test_insert_user_success_user'
        password=b'password'
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
        self.assertEqual(signup_info.code, self.signup_info.code)

    def test_get_signup_info_non_existing_username(self):
        ''' get_user should return None if we pass a non existing username '''
        username='test_get_signup_info_non_existing_username'
        self.assertIsNone(userapi.get_signup_info(username=username))

    def test_get_signup_info_existing_code(self):
        ''' get_signup_info should succeed if we pass an existing code '''
        code=self.signup_info.code
        signup_info=userapi.get_signup_info(code=code)
        self.assertEqual(signup_info.username, self.signup_info.username)
        self.assertEqual(signup_info.email, self.signup_info.email)
        self.assertEqual(signup_info.code, self.signup_info.code)

    def test_get_signup_info_non_existing_code(self):
        ''' get_user should return None if we pass a non existing code '''
        code='test_get_signup_info_non_existing_code'
        self.assertIsNone(userapi.get_signup_info(code=code))

    def test_get_signup_info_existing_email(self):
        ''' get_signup_info should succeed if we pass an existing email '''
        email=self.signup_info.email
        signup_info=userapi.get_signup_info(email=email)
        self.assertEqual(signup_info.username, self.signup_info.username)
        self.assertEqual(signup_info.email, self.signup_info.email)
        self.assertEqual(signup_info.code, self.signup_info.code)

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

    def test_get_invitation_info_non_existing_info(self):
        ''' get_invitation_info should return an empty array is no info is found '''
        inv_id=uuid.uuid4()
        self.assertEqual(userapi.get_invitation_info(inv_id=inv_id),[])

    def test_get_invitation_info_existing_info(self):
        ''' get_invitation_info should return an array with the found info '''
        info1=ormuser.Invitation(inv_id=uuid.uuid4(),date=timeuuid.uuid1(),state=0)
        info2=ormuser.Invitation(inv_id=uuid.uuid4(),date=timeuuid.uuid1(),state=0)
        info3=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=uuid.uuid4())
        info4=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        info5=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        info6=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info3))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info6))
        info_found=userapi.get_invitation_info(inv_id=info1.inv_id)
        self.assertEqual(len(info_found),5)
        info_found=userapi.get_invitation_info(inv_id=info2.inv_id)
        self.assertEqual(len(info_found),1)

    def test_insert_invitation_info_success(self):
        ''' insert_invitation_info should insert the info successfully '''
        info1=ormuser.Invitation(inv_id=uuid.uuid4(),date=timeuuid.uuid1(),state=0)
        info2=ormuser.Invitation(inv_id=uuid.uuid4(),date=timeuuid.uuid1(),state=0)
        info3=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=uuid.uuid4())
        info4=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        info5=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        info6=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info3))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info6))
        info_found=userapi.get_invitation_info(inv_id=info1.inv_id)
        self.assertEqual(len(info_found),5)
        info_found=userapi.get_invitation_info(inv_id=info2.inv_id)
        self.assertEqual(len(info_found),1)

    def test_insert_invitation_info_failure_non_Invitation_instance(self):
        ''' insert_invitation_info should fail if info is not a Invitation instance '''
        infos=[None, 123123, '2123123123', {'a':'dict'},['a','list']]
        for info in infos:
            self.assertFalse(userapi.insert_invitation_info(info))

    def test_delete_invitation_info_success(self):
        ''' delete_invitation_info should delete the info successfully '''
        info1=ormuser.Invitation(inv_id=uuid.uuid4(),date=timeuuid.uuid1(),state=0)
        info2=ormuser.Invitation(inv_id=uuid.uuid4(),date=timeuuid.uuid1(),state=0)
        info3=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=uuid.uuid4())
        info4=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        info5=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        info6=ormuser.Invitation(inv_id=info1.inv_id,date=timeuuid.uuid1(),state=1,tran_id=info3.tran_id)
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info1))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info2))
        self.assertTrue(userapi.insert_invitation_info(info3))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info4))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info5))
        self.assertTrue(userapi.insert_invitation_info(info6))
        info_found=userapi.get_invitation_info(inv_id=info1.inv_id)
        self.assertEqual(len(info_found),5)
        info_found=userapi.get_invitation_info(inv_id=info2.inv_id)
        self.assertEqual(len(info_found),1)
        self.assertTrue(userapi.delete_invitation_info(inv_id=info1.inv_id, date=info1.date))
        self.assertTrue(userapi.delete_invitation_info(inv_id=info2.inv_id, date=info2.date))
        info_found=userapi.get_invitation_info(inv_id=info1.inv_id)
        self.assertEqual(len(info_found),4)
        info_found=userapi.get_invitation_info(inv_id=info2.inv_id)
        self.assertEqual(len(info_found),0)

    def test_delete_invitation_info_success_all_inv_id_deleted(self):
        ''' delete_invitation_info should delete the info successfully '''
        inv_id=uuid.uuid4()
        for i in range(1,101):
            info=ormuser.Invitation(inv_id=inv_id,date=timeuuid.uuid1(),state=i)
            self.assertTrue(userapi.insert_invitation_info(info))
        info_found=userapi.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(info_found),100)
        self.assertTrue(userapi.delete_invitation_info(inv_id=inv_id))
        info_found=userapi.get_invitation_info(inv_id=inv_id)
        self.assertEqual(len(info_found),0)

    def test_delete_invitation_info_success_even_if_does_not_exist(self):
        ''' delete_invitation_info should delete the info successfully even if it does not exist '''
        inv_id=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(userapi.delete_invitation_info(inv_id=inv_id, date=date))

    def test_get_invitation_request_none_found(self):
        ''' get_invitation_request should return None if no request is found '''
        email='test@email.com'
        self.assertIsNone(userapi.get_invitation_request(email=email))

    def test_get_invitation_request_success(self):
        ''' get_invitation_request should return the request '''
        request1=ormuser.InvitationRequest(email='get_invitation_request1_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request2=ormuser.InvitationRequest(email='get_invitation_request2_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request3=ormuser.InvitationRequest(email='get_invitation_request3_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request4=ormuser.InvitationRequest(email='get_invitation_request4_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request1))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request2))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request3))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request4))
        self.assertEqual(userapi.get_invitation_request(email=request1.email).__dict__,request1.__dict__)
        self.assertEqual(userapi.get_invitation_request(email=request2.email).__dict__,request2.__dict__)
        self.assertEqual(userapi.get_invitation_request(email=request3.email).__dict__,request3.__dict__)
        self.assertEqual(userapi.get_invitation_request(email=request4.email).__dict__,request4.__dict__)

    def test_get_invitation_requests_success(self):
        ''' get_invitation_request should return the requests with the associated state '''
        request1=ormuser.InvitationRequest(email='get_invitation_request1_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request2=ormuser.InvitationRequest(email='get_invitation_request2_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request3=ormuser.InvitationRequest(email='get_invitation_request3_success@komlog.org',date=timeuuid.uuid1(),state=1,inv_id=uuid.uuid4())
        request4=ormuser.InvitationRequest(email='get_invitation_request4_success@komlog.org',date=timeuuid.uuid1(),state=1,inv_id=uuid.uuid4())
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request1))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request2))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request3))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request4))
        requests_found=userapi.get_invitation_requests(state=0)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_invitation_requests(state=1)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_invitation_requests(state=200)
        self.assertEqual(len(requests_found),0)

    def test_insert_invitation_request_success(self):
        ''' insert_invitation_request should insert the object successfully '''
        request1=ormuser.InvitationRequest(email='get_invitation_request1_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request2=ormuser.InvitationRequest(email='get_invitation_request2_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request3=ormuser.InvitationRequest(email='get_invitation_request3_success@komlog.org',date=timeuuid.uuid1(),state=1,inv_id=uuid.uuid4())
        request4=ormuser.InvitationRequest(email='get_invitation_request4_success@komlog.org',date=timeuuid.uuid1(),state=1,inv_id=uuid.uuid4())
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request1))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request2))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request3))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request4))
        requests_found=userapi.get_invitation_requests(state=0)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_invitation_requests(state=1)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_invitation_requests(state=200)
        self.assertEqual(len(requests_found),0)

    def test_insert_invitation_request_failure_non_InvitationRequest_instance(self):
        ''' insert_invitation_request should fail if info is not a InvitationRequest instance '''
        requests=[None, 123123, '2123123123', {'a':'dict'},['a','list']]
        for request in requests:
            self.assertFalse(userapi.insert_invitation_request(request))

    def test_delete_invitation_request_success(self):
        ''' delete_invitation_request should delete the object successfully '''
        request1=ormuser.InvitationRequest(email='get_invitation_request1_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request2=ormuser.InvitationRequest(email='get_invitation_request2_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        request3=ormuser.InvitationRequest(email='get_invitation_request3_success@komlog.org',date=timeuuid.uuid1(),state=1,inv_id=uuid.uuid4())
        request4=ormuser.InvitationRequest(email='get_invitation_request4_success@komlog.org',date=timeuuid.uuid1(),state=1,inv_id=uuid.uuid4())
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request1))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request2))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request3))
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request4))
        request=userapi.get_invitation_request(email=request1.email)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_invitation_request(email=request.email))
        request=userapi.get_invitation_request(email=request1.email)
        self.assertIsNone(request)
        request=userapi.get_invitation_request(email=request2.email)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_invitation_request(email=request.email))
        request=userapi.get_invitation_request(email=request2.email)
        self.assertIsNone(request)
        request=userapi.get_invitation_request(email=request3.email)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_invitation_request(email=request.email))
        request=userapi.get_invitation_request(email=request3.email)
        self.assertIsNone(request)
        request=userapi.get_invitation_request(email=request4.email)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_invitation_request(email=request.email))
        request=userapi.get_invitation_request(email=request4.email)
        self.assertIsNone(request)

    def test_update_invitation_request_state_success(self):
        ''' update_invitation_request_state should update the state of the request '''
        request1=ormuser.InvitationRequest(email='get_invitation_request1_success@komlog.org',date=timeuuid.uuid1(),state=0,inv_id=uuid.uuid4())
        self.assertTrue(userapi.insert_invitation_request(invitation_request=request1))
        request=userapi.get_invitation_request(email=request1.email)
        self.assertIsNotNone(request)
        self.assertEqual(request.state,0)
        self.assertTrue(userapi.update_invitation_request_state(email=request.email, new_state=1))
        request=userapi.get_invitation_request(email=request1.email)
        self.assertIsNotNone(request)
        self.assertEqual(request.state,1)

    def test_update_invitation_request_state_failed(self):
        ''' update_invitation_request_state should fail if invitation_request does not exist '''
        self.assertFalse(userapi.update_invitation_request_state(email='nonexistent', new_state=1))

    def test_get_forget_request_none_found(self):
        ''' get_forget_request should return None if no request is found '''
        code=uuid.uuid4()
        self.assertIsNone(userapi.get_forget_request(code=code))

    def test_get_forget_request_success(self):
        ''' get_forget_request should return the request '''
        request1=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request2=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request3=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request4=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        self.assertTrue(userapi.insert_forget_request(forget_request=request1))
        self.assertTrue(userapi.insert_forget_request(forget_request=request2))
        self.assertTrue(userapi.insert_forget_request(forget_request=request3))
        self.assertTrue(userapi.insert_forget_request(forget_request=request4))
        self.assertEqual(userapi.get_forget_request(code=request1.code).__dict__,request1.__dict__)
        self.assertEqual(userapi.get_forget_request(code=request2.code).__dict__,request2.__dict__)
        self.assertEqual(userapi.get_forget_request(code=request3.code).__dict__,request3.__dict__)
        self.assertEqual(userapi.get_forget_request(code=request4.code).__dict__,request4.__dict__)

    def test_get_forget_requests_success(self):
        ''' get_forget_request should return the requests with the associated state '''
        request1=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request2=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request3=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=1,uid=uuid.uuid4())
        request4=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=1,uid=uuid.uuid4())
        self.assertTrue(userapi.insert_forget_request(forget_request=request1))
        self.assertTrue(userapi.insert_forget_request(forget_request=request2))
        self.assertTrue(userapi.insert_forget_request(forget_request=request3))
        self.assertTrue(userapi.insert_forget_request(forget_request=request4))
        requests_found=userapi.get_forget_requests(state=0)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_forget_requests(state=1)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_forget_requests(state=200)
        self.assertEqual(len(requests_found),0)

    def test_get_forget_requests_by_uid_success(self):
        ''' get_forget_requests_by_uid should return the uid forget requests '''
        uid=uuid.uuid4()
        for i in range(1,101):
            request=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uid)
            self.assertTrue(userapi.insert_forget_request(forget_request=request))
        requests_found=userapi.get_forget_requests_by_uid(uid=uid)
        self.assertTrue(len(requests_found),100)
        uid=uuid.uuid4()
        requests_found=userapi.get_forget_requests_by_uid(uid=uid)
        self.assertEqual(len(requests_found),0)

    def test_insert_forget_request_success(self):
        ''' insert_forget_request should insert the object successfully '''
        request1=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request2=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request3=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=1,uid=uuid.uuid4())
        request4=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=1,uid=uuid.uuid4())
        self.assertTrue(userapi.insert_forget_request(forget_request=request1))
        self.assertTrue(userapi.insert_forget_request(forget_request=request2))
        self.assertTrue(userapi.insert_forget_request(forget_request=request3))
        self.assertTrue(userapi.insert_forget_request(forget_request=request4))
        requests_found=userapi.get_forget_requests(state=0)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_forget_requests(state=1)
        self.assertTrue(len(requests_found)>1)
        requests_found=userapi.get_forget_requests(state=200)
        self.assertEqual(len(requests_found),0)

    def test_insert_forget_request_failure_non_ForgetRequest_instance(self):
        ''' insert_forget_request should fail if info is not a ForgetRequest instance '''
        requests=[None, 123123, '2123123123', {'a':'dict'},['a','list']]
        for request in requests:
            self.assertFalse(userapi.insert_forget_request(request))

    def test_delete_forget_request_success(self):
        ''' delete_forget_request should delete the object successfully '''
        request1=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request2=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        request3=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=1,uid=uuid.uuid4())
        request4=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=1,uid=uuid.uuid4())
        self.assertTrue(userapi.insert_forget_request(forget_request=request1))
        self.assertTrue(userapi.insert_forget_request(forget_request=request2))
        self.assertTrue(userapi.insert_forget_request(forget_request=request3))
        self.assertTrue(userapi.insert_forget_request(forget_request=request4))
        request=userapi.get_forget_request(code=request1.code)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_forget_request(code=request.code))
        request=userapi.get_forget_request(code=request1.code)
        self.assertIsNone(request)
        request=userapi.get_forget_request(code=request2.code)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_forget_request(code=request.code))
        request=userapi.get_forget_request(code=request2.code)
        self.assertIsNone(request)
        request=userapi.get_forget_request(code=request3.code)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_forget_request(code=request.code))
        request=userapi.get_forget_request(code=request3.code)
        self.assertIsNone(request)
        request=userapi.get_forget_request(code=request4.code)
        self.assertIsNotNone(request)
        self.assertTrue(userapi.delete_forget_request(code=request.code))
        request=userapi.get_forget_request(code=request4.code)
        self.assertIsNone(request)

    def test_update_forget_request_state_success(self):
        ''' update_forget_request_state should update the state of the request '''
        request1=ormuser.ForgetRequest(code=uuid.uuid4(),date=timeuuid.uuid1(),state=0,uid=uuid.uuid4())
        self.assertTrue(userapi.insert_forget_request(forget_request=request1))
        request=userapi.get_forget_request(code=request1.code)
        self.assertIsNotNone(request)
        self.assertEqual(request.state,0)
        self.assertTrue(userapi.update_forget_request_state(code=request.code, new_state=1))
        request=userapi.get_forget_request(code=request1.code)
        self.assertIsNotNone(request)
        self.assertEqual(request.state,1)

    def test_update_forget_request_state_failed(self):
        ''' update_forget_request_state should fail if forget_request does not exist '''
        self.assertFalse(userapi.update_forget_request_state(code=uuid.uuid4(), new_state=1))

    def test_update_user_password_success(self):
        ''' update_user_password should update the password successfully '''
        username='test_update_user_password_success'
        password=b'password'
        email=username+'@komlog.org'
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        user=ormuser.User(username=username, password=password, email=email, uid=uid, creation_date=creation_date)
        self.assertTrue(userapi.new_user(user))
        new_password=b'temporal'
        self.assertTrue(userapi.update_user_password(username=username, password=new_password))

    def test_update_user_password_failed_user_not_found(self):
        ''' update_forget_request_state should fail if forget_request does not exist '''
        username='test_update_user_password_failed_user_not_found'
        password=b'temporal'
        self.assertFalse(userapi.update_user_password(username=username, password=password))

    def test_get_pending_hooks_by_uid_no_hook_found(self):
        ''' get_pending_hooks should return an empty array if no hook is found '''
        uid=uuid.uuid4()
        self.assertEqual(userapi.get_pending_hooks(uid=uid),[])

    def test_get_pending_hooks_by_uid_and_uri_no_hook_found(self):
        ''' get_pending_hooks should return an empty array if no hook is found '''
        uid=uuid.uuid4()
        uri='uri'
        self.assertEqual(userapi.get_pending_hooks(uid=uid,uri=uri),[])

    def test_get_pending_hooks_some_hooks_found(self):
        ''' get_pending_hooks should return an array with the hooks found '''
        uid=uuid.uuid4()
        for uri in ('uri.ds','uri.dp'):
            for i in range(1,11):
                sid=uuid.uuid4()
                pendinghook=ormuser.PendingHook(uid,uri,sid)
                self.assertTrue(userapi.insert_pending_hook(pendinghook))
        hooks_found=userapi.get_pending_hooks(uid=uid)
        self.assertEqual(len(hooks_found),20)
        hooks_found=userapi.get_pending_hooks(uid=uid,uri='uri.ds')
        self.assertEqual(len(hooks_found),10)
        hooks_found=userapi.get_pending_hooks(uid=uid,uri='uri.dp')
        self.assertEqual(len(hooks_found),10)
        hooks_found=userapi.get_pending_hooks(uid=uuid.uuid4(),uri='uri.dp')
        self.assertEqual(len(hooks_found),0)

    def test_get_pending_hooks_by_sid_no_hook_found(self):
        ''' get_pending_hooks should return an empty array if no hook is found '''
        sid=uuid.uuid4()
        self.assertEqual(userapi.get_pending_hooks_by_sid(sid=sid),[])

    def test_get_pending_hooks_by_sid_some_hooks_found(self):
        ''' get_pending_hooks should return an array with the hooks found '''
        sid1=uuid.uuid4()
        for uid in (uuid.uuid4(),uuid.uuid4(),uuid.uuid4()):
            for uri in ('uri.ds','uri.dp'):
                for i in range(1,11):
                    sid=uuid.uuid4()
                    pendinghook=ormuser.PendingHook(uid,uri,sid)
                    self.assertTrue(userapi.insert_pending_hook(pendinghook))
                pendinghook=ormuser.PendingHook(uid,uri,sid1)
                self.assertTrue(userapi.insert_pending_hook(pendinghook))
        hooks_found=userapi.get_pending_hooks_by_sid(sid=sid1)
        self.assertEqual(len(hooks_found),6)

    def test_get_pending_hook_no_hook_found(self):
        ''' get_pending_hook should return None if no hook is found '''
        uid=uuid.uuid4()
        uri='uri'
        sid=uuid.uuid4()
        self.assertIsNone(userapi.get_pending_hook(uid=uid, uri=uri, sid=sid))

    def test_get_pending_hook_found(self):
        ''' get_pending_hook should return the PendingHook object if found '''
        uids=[uuid.uuid4() for i in range(1,10)]
        sids=[uuid.uuid4() for i in range(1,10)]
        uris=['.'.join(('uri',str(i))) for i in range(1,10)]
        for uid in uids:
            for uri in uris:
                for sid in sids:
                    pendinghook=ormuser.PendingHook(uid,uri,sid)
                    self.assertTrue(userapi.insert_pending_hook(pendinghook))
        uid_i=random.randint(0,8)
        uri_i=random.randint(0,8)
        sid_i=random.randint(0,8)
        hook=userapi.get_pending_hook(uid=uids[uid_i],uri=uris[uri_i], sid=sids[sid_i])
        self.assertIsNotNone(hook)
        self.assertTrue(isinstance(hook,ormuser.PendingHook))
        self.assertEqual(hook.uid, uids[uid_i])
        self.assertEqual(hook.uri, uris[uri_i])
        self.assertEqual(hook.sid, sids[sid_i])

    def test_insert_pending_hook_failure_non_PendingHook_instance(self):
        ''' insert_pending_hook should fail if pending_hook is not a PendingHook instance '''
        hooks=[None, 123123, '2123123123', {'a':'dict'},['a','list']]
        for hook in hooks:
            self.assertFalse(userapi.insert_pending_hook(hook))

    def test_insert_pending_hook_success(self):
        ''' insert_pending_hook should succeed and return True '''
        uid=uuid.uuid4()
        uri='uri'
        sid=uuid.uuid4()
        pendinghook=ormuser.PendingHook(uid,uri,sid)
        self.assertTrue(userapi.insert_pending_hook(pendinghook))
        hook=userapi.get_pending_hook(uid=uid,uri=uri, sid=sid)
        self.assertIsNotNone(hook)
        self.assertTrue(isinstance(hook,ormuser.PendingHook))
        self.assertEqual(hook.uid, uid)
        self.assertEqual(hook.uri, uri)
        self.assertEqual(hook.sid, sid)

    def test_delete_pending_hooks_by_uid_no_previous_existing_hook(self):
        ''' delete_pending_hooks should return true if no previous hook existed '''
        uid=uuid.uuid4()
        self.assertTrue(userapi.delete_pending_hooks(uid=uid))

    def test_delete_pending_hooks_by_uid_and_uri_no_previous_existing_hook(self):
        ''' delete_pending_hooks should return true if no previous hook existed '''
        uid=uuid.uuid4()
        uri='uri'
        self.assertTrue(userapi.delete_pending_hooks(uid=uid, uri=uri))

    def test_delete_pending_hooks_some_found(self):
        ''' delete_pending_hooks should return True and delete the hooks requested '''
        uids=[uuid.uuid4() for i in range(1,10)]
        sids=[uuid.uuid4() for i in range(1,10)]
        uris=['.'.join(('uri',str(i))) for i in range(1,10)]
        for uid in uids:
            for uri in uris:
                for sid in sids:
                    pendinghook=ormuser.PendingHook(uid,uri,sid)
                    self.assertTrue(userapi.insert_pending_hook(pendinghook))
        uid_i=random.randint(0,8)
        hooks=userapi.get_pending_hooks(uid=uids[uid_i])
        self.assertEqual(len(hooks),9*9)
        uri_i=random.randint(0,8)
        self.assertTrue(userapi.delete_pending_hooks(uid=uids[uid_i],uri=uris[uri_i]))
        hooks=userapi.get_pending_hooks(uid=uids[uid_i])
        self.assertEqual(len(hooks),9*8)
        self.assertTrue(userapi.delete_pending_hooks(uid=uids[uid_i]))
        hooks=userapi.get_pending_hooks(uid=uids[uid_i])
        self.assertEqual(len(hooks),0)

    def test_delete_pending_hook_no_previous_existing_hook(self):
        ''' delete_pending_hook should return true if no previous hook existed '''
        uid=uuid.uuid4()
        uri='uri'
        sid=uuid.uuid4()
        self.assertTrue(userapi.delete_pending_hook(uid=uid, uri=uri, sid=sid))

    def test_delete_pending_hook_found(self):
        ''' delete_pending_hook should return True and delete the hook requested '''
        uids=[uuid.uuid4() for i in range(1,10)]
        sids=[uuid.uuid4() for i in range(1,10)]
        uris=['.'.join(('uri',str(i))) for i in range(1,10)]
        for uid in uids:
            for uri in uris:
                for sid in sids:
                    pendinghook=ormuser.PendingHook(uid,uri,sid)
                    self.assertTrue(userapi.insert_pending_hook(pendinghook))
        uid_i=random.randint(0,8)
        hooks=userapi.get_pending_hooks(uid=uids[uid_i])
        self.assertEqual(len(hooks),9*9)
        uri_i=random.randint(0,8)
        sid_i=random.randint(0,8)
        self.assertTrue(userapi.delete_pending_hook(uid=uids[uid_i],uri=uris[uri_i],sid=sids[sid_i]))
        hooks=userapi.get_pending_hooks(uid=uids[uid_i])
        self.assertEqual(len(hooks),(9*9)-1)
        self.assertIsNone(userapi.get_pending_hook(uid=uids[uid_i],uri=uris[uri_i],sid=sids[sid_i]))

    def test_get_user_billing_info_non_existent(self):
        ''' get_user_billing_info should return None if no info exists '''
        uid=uuid.uuid4()
        self.assertIsNone(userapi.get_user_billing_info(uid=uid))

    def test_get_user_billing_info_existent(self):
        ''' get_user_billing_info should return a BillingInfo object if info exists '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.insert_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_insert_user_billing_info_success(self):
        ''' insert_user_billing_info should return True and set the information '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.insert_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_billing_day = 10
        new_last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.insert_user_billing_info(uid=uid, billing_day=new_billing_day, last_billing = new_last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, new_billing_day)
        self.assertEqual(info.last_billing, new_last_billing)

    def test_new_user_billing_info_success_previously_did_not_exist(self):
        ''' new_user_billing_info should return True and set the information if info did not exist previously '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_new_user_billing_info_failure_previously_did_exist(self):
        ''' new_user_billing_info should return False if user existed previously '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_billing_day = 64
        new_last_billing = timeuuid.uuid1()
        self.assertFalse(userapi.new_user_billing_info(uid=uid, billing_day=new_billing_day, last_billing = new_last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_delete_user_billing_info_success_previously_did_exist(self):
        ''' delete_user_billing_info should return True if user existed previously and delete it '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        self.assertTrue(userapi.delete_user_billing_info(uid=uid))
        self.assertIsNone(userapi.get_user_billing_info(uid=uid))

    def test_delete_user_billing_info_failure_previously_did_not_exist(self):
        ''' delete_user_billing_info should return False if user did not exist previously '''
        uid=uuid.uuid4()
        self.assertFalse(userapi.delete_user_billing_info(uid=uid))
        self.assertIsNone(userapi.get_user_billing_info(uid=uid))

    def test_update_user_billing_day_success_current_value_equals_expected(self):
        ''' update_user_billing_day should update the value if current billing day is as expected'''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_billing_day = 31
        self.assertTrue(userapi.update_user_billing_day(uid=uid, billing_day=new_billing_day,  current_billing_day = billing_day))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, new_billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_update_user_billing_day_failure_current_value_not_equal_expected(self):
        ''' update_user_billing_day should fail if current billing day value is not as expected'''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_billing_day = 31
        self.assertFalse(userapi.update_user_billing_day(uid=uid, billing_day=new_billing_day,  current_billing_day = new_billing_day))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_update_user_billing_day_success_no_current_value_condition(self):
        ''' update_user_billing_day should succeed if no current value condition is set '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_billing_day = 31
        self.assertTrue(userapi.update_user_billing_day(uid=uid, billing_day=new_billing_day))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, new_billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_update_user_last_billing_success_current_value_equals_expected(self):
        ''' update_user_billing_day should update the value if current billing day is as expected'''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.update_user_last_billing(uid=uid, last_billing=new_last_billing,  current_last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, new_last_billing)

    def test_update_user_billing_day_failure_current_value_not_equal_expected(self):
        ''' update_user_billing_day should fail if current billing day value is not as expected'''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_last_billing = timeuuid.uuid1()
        self.assertFalse(userapi.update_user_last_billing(uid=uid, last_billing=new_last_billing,  current_last_billing = new_last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)

    def test_update_user_billing_day_success_no_current_value_condition(self):
        ''' update_user_billing_day should succeed if no current value condition is set '''
        uid=uuid.uuid4()
        billing_day = 20
        last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.new_user_billing_info(uid=uid, billing_day=billing_day, last_billing = last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, last_billing)
        new_last_billing = timeuuid.uuid1()
        self.assertTrue(userapi.update_user_last_billing(uid=uid, last_billing=new_last_billing))
        info=userapi.get_user_billing_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.billing_day, billing_day)
        self.assertEqual(info.last_billing, new_last_billing)

    def test_get_user_stripe_info_non_existent(self):
        ''' get_user_stripe_info should return None if no info exists '''
        uid=uuid.uuid4()
        self.assertIsNone(userapi.get_user_stripe_info(uid=uid))

    def test_get_user_stripe_info_existent(self):
        ''' get_user_stripe_info should return a StripeInfo object if info exists '''
        uid=uuid.uuid4()
        stripe_id = 'some text' 
        self.assertTrue(userapi.insert_user_stripe_info(uid=uid, stripe_id=stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, stripe_id)

    def test_insert_user_stripe_info_success(self):
        ''' insert_user_stripe_info should return True and set the information '''
        uid=uuid.uuid4()
        stripe_id = 'some text' 
        self.assertTrue(userapi.insert_user_stripe_info(uid=uid, stripe_id=stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, stripe_id)
        new_stripe_id  = 'some other id'
        self.assertTrue(userapi.insert_user_stripe_info(uid=uid, stripe_id=new_stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, new_stripe_id)

    def test_new_user_stripe_info_success_previously_did_not_exist(self):
        ''' new_user_stripe_info should return True and set the information if info did not exist previously '''
        uid=uuid.uuid4()
        stripe_id = 'some text' 
        self.assertTrue(userapi.new_user_stripe_info(uid=uid, stripe_id=stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, stripe_id)

    def test_new_user_stripe_info_failure_previously_did_exist(self):
        ''' new_user_stripe_info should return False if user existed previously '''
        uid=uuid.uuid4()
        stripe_id = 'some text' 
        self.assertTrue(userapi.new_user_stripe_info(uid=uid, stripe_id=stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, stripe_id)
        new_stripe_id = 'some new text' 
        self.assertFalse(userapi.new_user_stripe_info(uid=uid, stripe_id=new_stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, stripe_id)

    def test_delete_user_stripe_info_success_previously_did_exist(self):
        ''' delete_user_stripe_info should return True if user existed previously and delete it '''
        uid=uuid.uuid4()
        stripe_id = 'some text' 
        self.assertTrue(userapi.new_user_stripe_info(uid=uid, stripe_id=stripe_id))
        info=userapi.get_user_stripe_info(uid=uid)
        self.assertEqual(info.uid, uid)
        self.assertEqual(info.stripe_id, stripe_id)
        self.assertTrue(userapi.delete_user_stripe_info(uid=uid))
        self.assertIsNone(userapi.get_user_stripe_info(uid=uid))

    def test_delete_user_stripe_info_failure_previously_did_not_exist(self):
        ''' delete_user_stripe_info should return False if user did not exist previously '''
        uid=uuid.uuid4()
        self.assertFalse(userapi.delete_user_stripe_info(uid=uid))
        self.assertIsNone(userapi.get_user_stripe_info(uid=uid))

