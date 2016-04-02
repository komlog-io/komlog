import unittest
import uuid
from komlog.komcass.api import circle as cassapicircle
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.circle import api as circleapi
from komlog.komlibs.gestaccount.circle import types
from komlog.komlibs.gestaccount import exceptions
from komlog.komcass.model.orm import circle as ormcircle
from komlog.komlibs.general.time import timeuuid

class GestaccountCircleApiTest(unittest.TestCase):
    ''' komlog.gestaccount.circle.api tests '''

    def test_new_users_circle_failure_invalid_username(self):
        ''' new_users_circle should fail if username is invalid '''
        uids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        circlename='circlename'
        members_list=['user1','user2']
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, circleapi.new_users_circle, uid=uid, circlename=circlename, members_list=members_list)

    def test_new_users_circle_failure_invalid_circlename(self):
        ''' new_users_circle should fail if circlename is invalid '''
        circlenames=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1()]
        uid=uuid.uuid4()
        members_list=['user1','user2']
        for circlename in circlenames:
            self.assertRaises(exceptions.BadParametersException, circleapi.new_users_circle, uid=uid, circlename=circlename, members_list=members_list)

    def test_new_users_circle_failure_invalid_members_list(self):
        ''' new_users_circle should fail if members_list is invalid '''
        members_lists=[24232, 2342.23423, {'a':'dict'},('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        circlename='circlename'
        for members_list in members_lists:
            self.assertRaises(exceptions.BadParametersException, circleapi.new_users_circle, uid=uid, circlename=circlename, members_list=members_list)

    def test_new_users_circle_failure_non_existent_username(self):
        ''' new_users_circle should fail if username does not exist '''
        uid=uuid.uuid4()
        circlename='circlename'
        members_list=['user1','user2']
        self.assertRaises(exceptions.UserNotFoundException, circleapi.new_users_circle, uid=uid, circlename=circlename, members_list=members_list)

    def test_new_users_circle_success_empty_members_list(self):
        ''' new_users_circle should succeed if user exists and parameters are correct. if no member is passed the circle should be created successfully without members '''
        username='test_new_users_circle_success_empty_members_list'
        email=username+'@komlog.org'
        password='password'
        circlename='test_new_users_circle_success_empty_members_list_circlename'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])

    def test_new_users_circle_success_non_existent_members_list(self):
        ''' new_users_circle should succeed if user exists and parameters are correct. if no member in the members_list exists then the circle will be created with no members. '''
        username='test_new_users_circle_success_non_existent_members_list'
        email=username+'@komlog.org'
        password='password'
        circlename='test_new_users_circle_success_non_existent_members_list_circlename'
        members_list=['a_member','other_member','a non valid username']
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename,members_list=members_list)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])

    def test_new_users_circle_success_only_some_members_exist(self):
        ''' new_users_circle should succeed if user exists and parameters are correct. if only some members in the members_list exist then the circle will be created with only the existing members. '''
        username='test_new_users_circle_success_only_some_members_exist'
        email=username+'@komlog.org'
        password='password'
        circlename='test_new_users_circle_success_only_some_members_exist_circlename'
        user=userapi.create_user(username=username, password=password, email=email)
        member1='test_new_users_circle_success_only_some_members_exist_member1'
        email=member1+'@komlog.org'
        password='password'
        member1_user=userapi.create_user(username=member1, password=password, email=email)
        member2='test_new_users_circle_success_only_some_members_exist_member2'
        email=member2+'@komlog.org'
        password='password'
        member2_user=userapi.create_user(username=member2, password=password, email=email)
        members_list=[member1,member2,'a_non_existent_username','a non valid username',234234]
        valid_members=[]
        valid_members.append({'username':member1,'uid':member1_user['uid']})
        valid_members.append({'username':member2,'uid':member2_user['uid']})
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename,members_list=members_list)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(sorted(db_circle['members'], key=lambda x: x['username']),sorted(valid_members, key=lambda x: x['username']))

    def test_get_users_circle_config_failure_invalid_cid(self):
        ''' get_users_circle_config should fail if cid is invalid '''
        cids=[None,23234,23423.23423,'adfasdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4().hex]
        for cid in cids:
            self.assertRaises(exceptions.BadParametersException, circleapi.get_users_circle_config, cid=cid)

    def test_get_users_circle_config_failure_non_existent_circle(self):
        ''' get_users_circle_config should fail if cid does not exist '''
        cid=uuid.uuid4()
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.get_users_circle_config, cid=cid)

    def test_get_users_circle_config_failure_non_users_circle_type(self):
        ''' get_users_circle_config should fail if cid exists but is not USERS_CIRCLE type '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='OTHER NON EXISTENT TYPE'
        creation_date=timeuuid.uuid1()
        circlename='test_get_users_circle_config_failure_non_users_circle_type'
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=None)
        self.assertTrue(cassapicircle.new_circle(circle=circle))
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.get_users_circle_config, cid=cid)

    def test_get_users_circle_config_success(self):
        ''' get_users_circle should succeed if circle exists '''
        username='test_get_users_circle_success'
        email=username+'@komlog.org'
        password='password'
        circlename='test_get_users_circle_success'
        user=userapi.create_user(username=username, password=password, email=email)
        member1='test_get_users_circle_success_member1'
        email=member1+'@komlog.org'
        password='password'
        member1_user=userapi.create_user(username=member1, password=password, email=email)
        member2='test_get_users_circle_success_member2'
        email=member2+'@komlog.org'
        password='password'
        member2_user=userapi.create_user(username=member2, password=password, email=email)
        members_list=[member1,member2]
        valid_members=[]
        valid_members.append({'username':member1,'uid':member1_user['uid']})
        valid_members.append({'username':member2,'uid':member2_user['uid']})
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename,members_list=members_list)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(sorted(db_circle['members'], key=lambda x: x['username']),sorted(valid_members, key= lambda x: x['username']))

    def test_get_users_circles_config_failure_invalid_username(self):
        ''' get_users_circles_config should fail if username is invalid '''
        uids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, circleapi.get_users_circles_config, uid=uid)

    def test_get_users_circles_config_failure_non_existent_user(self):
        ''' get_users_circles_config should fail if user does not exist '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, circleapi.get_users_circles_config, uid=uid)

    def test_get_users_circles_config_success_user_has_no_circles(self):
        ''' get_users_circles should succeed if user exist. if no circle is found, then no data is returned '''
        username='test_get_users_circles_success_user_has_no_circles'
        email=username+'@komlog.org'
        password='password'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertEqual(circleapi.get_users_circles_config(uid=user['uid']),[])

    def test_get_users_circles_config_success_one_circle_only(self):
        ''' get_users_circles should succeed. in this case will return an array with one circle '''
        username='test_get_users_circles_success_one_circle_only'
        email=username+'@komlog.org'
        password='password'
        circlename='test_get_users_circles_success_one_circle_only'
        user=userapi.create_user(username=username, password=password, email=email)
        member1='test_get_users_circles_success_one_circle_only_member1'
        email=member1+'@komlog.org'
        password='password'
        member1_user=userapi.create_user(username=member1, password=password, email=email)
        member2='test_get_users_circles_success_one_circle_only_member2'
        email=member2+'@komlog.org'
        password='password'
        member2_user=userapi.create_user(username=member2, password=password, email=email)
        members_list=[member1,member2]
        valid_members=[]
        valid_members.append({'username':member1,'uid':member1_user['uid']})
        valid_members.append({'username':member2,'uid':member2_user['uid']})
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename,members_list=members_list)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circles=circleapi.get_users_circles_config(uid=user['uid'])
        self.assertTrue(len(db_circles),1)
        db_circle=db_circles[0]
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(sorted(db_circle['members'], key=lambda x: x['username']),sorted(valid_members, key= lambda x: x['username']))

    def test_get_users_circles_config_success_some_circles(self):
        ''' get_users_circles should succeed. in this case will return an array with three circles '''
        username='test_get_users_circles_success_some_circles'
        email=username+'@komlog.org'
        password='password'
        circlename1='test_get_users_circles_success_some_circles_1'
        circlename2='test_get_users_circles_success_some_circles_2'
        circlename3='test_get_users_circles_success_some_circles_3'
        user=userapi.create_user(username=username, password=password, email=email)
        circle1=circleapi.new_users_circle(uid=user['uid'], circlename=circlename1)
        circle2=circleapi.new_users_circle(uid=user['uid'], circlename=circlename2)
        circle3=circleapi.new_users_circle(uid=user['uid'], circlename=circlename3)
        db_circles=circleapi.get_users_circles_config(uid=user['uid'])
        self.assertTrue(len(db_circles),3)

    def test_get_users_circles_config_success_some_circles_avoiding_non_users_circles(self):
        ''' get_users_circles should succeed. in this case will return an array with three circles avoiding the circles that are not USERS_CIRCLES '''
        username='test_get_users_circles_success_some_circles_avoiding_non_users_circles'
        email=username+'@komlog.org'
        password='password'
        circlename1='test_get_users_circles_success_some_circles_1_avoiding_non_users_circles'
        circlename2='test_get_users_circles_success_some_circles_2_avoiding_non_users_circles'
        circlename3='test_get_users_circles_success_some_circles_3_avoiding_non_users_circles'
        user=userapi.create_user(username=username, password=password, email=email)
        circle1=circleapi.new_users_circle(uid=user['uid'], circlename=circlename1)
        circle2=circleapi.new_users_circle(uid=user['uid'], circlename=circlename2)
        circle3=circleapi.new_users_circle(uid=user['uid'], circlename=circlename3)
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        circlename4='test_get_users_circles_success_some_circles_3_avoiding_non_users_circles'
        type='OTHER NON EXISTENT TYPE'
        creation_date=timeuuid.uuid1()
        circle4=ormcircle.Circle(cid=cid,uid=user['uid'],type=type,creation_date=creation_date,circlename=circlename4,members=None)
        self.assertTrue(cassapicircle.new_circle(circle=circle4))
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.get_users_circle_config, cid=cid)
        db_circles=circleapi.get_users_circles_config(uid=user['uid'])
        self.assertTrue(len(db_circles),3)

    def test_update_circle_failure_invalid_cid(self):
        ''' update_circle should fail if cid is invalid '''
        cids=[None,23234,23423.23423,'adfasdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4().hex]
        circlename='circlename'
        for cid in cids:
            self.assertRaises(exceptions.BadParametersException, circleapi.update_circle, cid=cid, circlename=circlename)

    def test_update_circle_failure_invalid_circlename(self):
        ''' update_circle should fail if circlename is invalid '''
        circlenames=[None,23234,23423.23423,['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4(),'ñoño']
        cid=uuid.uuid4()
        for circlename in circlenames:
            self.assertRaises(exceptions.BadParametersException, circleapi.update_circle, cid=cid, circlename=circlename)

    def test_update_circle_failure_non_existent_circle(self):
        ''' update_circle should fail if circle does not exist '''
        cid=uuid.uuid4()
        circlename='test_update_circle_failure_non_existent_circle'
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.update_circle, cid=cid, circlename=circlename)

    def test_update_circle_success(self):
        ''' update_circle should succeed '''
        username='test_update_circle_success_user'
        email=username+'@komlog.org'
        password='password'
        circlename='test_update_circle_success_circlename_initial'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_circlename='test_update_circle_success_circlename_end'
        self.assertTrue(circleapi.update_circle(cid=cid,circlename=new_circlename))
        db_circle2=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle2['cid'],circle['cid'])
        self.assertEqual(db_circle2['circlename'],new_circlename)
        self.assertEqual(db_circle2['uid'],user['uid'])
        self.assertEqual(db_circle2['members'],[])

    def test_add_user_to_circle_failure_invalid_cid(self):
        ''' add_user_to_circle should fail if cid is invalid '''
        cids=[None,23234,23423.23423,'adfasdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4().hex]
        username='username'
        for cid in cids:
            self.assertRaises(exceptions.BadParametersException, circleapi.add_user_to_circle, cid=cid, username=username)

    def test_add_user_to_circle_failure_invalid_username(self):
        ''' add_user_to_circle should fail if username is invalid '''
        usernames=[None,23234,23423.23423,['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4(),'ñoño']
        cid=uuid.uuid4()
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, circleapi.add_user_to_circle, cid=cid, username=username)

    def test_add_user_to_circle_failure_non_existent_circle(self):
        ''' add_user_to_circle should fail if circle does not exist '''
        cid=uuid.uuid4()
        username='test_add_user_to_circle_failure_non_existent_circle'
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.add_user_to_circle, cid=cid, username=username)

    def test_add_user_to_circle_failure_non_users_circle_type(self):
        ''' add_user_to_circle should fail if circle is not of type USERS_CIRCLE '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='OTHER NON EXISTENT TYPE'
        creation_date=timeuuid.uuid1()
        circlename='test_add_user_to_circle_failure_non_users_circle_type'
        username='test_add_user_to_circle_failure_non_users_circle_type_username'
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=None)
        self.assertTrue(cassapicircle.new_circle(circle=circle))
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.add_user_to_circle, cid=cid, username=username)

    def test_add_user_to_circle_failure_new_member_does_not_exist(self):
        ''' add_user_to_circle should fail if new member does not exist '''
        username='test_add_user_to_circle_failure_new_member_does_not_exist'
        email=username+'@komlog.org'
        password='password'
        circlename='test_add_user_to_circle_failure_new_member_does_not_exist_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username='test_add_user_to_circle_failure_new_member_does_not_exist_new_member'
        self.assertRaises(exceptions.UserNotFoundException, circleapi.add_user_to_circle, cid=cid, username=new_username)

    def test_add_user_to_circle_success(self):
        ''' add_user_to_circle should succeed '''
        username='test_add_user_to_circle_success'
        email=username+'@komlog.org'
        password='password'
        circlename='test_add_user_to_circle_success_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username='test_add_user_to_circle_success_circle_new_member'
        email=new_username+'@komlog.org'
        password='password'
        new_user=userapi.create_user(username=new_username, password=password, email=email)
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[{'username':new_username,'uid':new_user['uid']}])

    def test_add_user_to_circle_success_even_if_added_twice(self):
        ''' add_user_to_circle should succeed even if it is added twice '''
        username='test_add_user_to_circle_success_even_if_added_twice'
        email=username+'@komlog.org'
        password='password'
        circlename='test_add_user_to_circle_success_even_if_added_twice_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username='test_add_user_to_circle_success_even_if_added_twice_new_member'
        email=new_username+'@komlog.org'
        password='password'
        new_user=userapi.create_user(username=new_username, password=password, email=email)
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[{'username':new_username,'uid':new_user['uid']}])
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[{'username':new_username,'uid':new_user['uid']}])

    def test_add_user_to_circle_success_some_members(self):
        ''' add_user_to_circle should succeed and add two members in this case '''
        username='test_add_user_to_circle_success_some_members'
        email=username+'@komlog.org'
        password='password'
        circlename='test_add_user_to_circle_success_some_members_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username1='test_add_user_to_circle_success_some_members_new_member1'
        email=new_username1+'@komlog.org'
        password='password'
        new_user1=userapi.create_user(username=new_username1, password=password, email=email)
        new_username2='test_add_user_to_circle_success_some_members_new_member2'
        email=new_username2+'@komlog.org'
        password='password'
        new_user2=userapi.create_user(username=new_username2, password=password, email=email)
        members=[]
        members.append({'username':new_username1,'uid':new_user1['uid']})
        members.append({'username':new_username2,'uid':new_user2['uid']})
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username1))
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username2))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(sorted(db_circle['members'], key=lambda x: x['username']),sorted(members, key=lambda x: x['username']))

    def test_delete_user_from_circle_failure_invalid_cid(self):
        ''' delete_user_from_circle should fail if cid is invalid '''
        cids=[None,23234,23423.23423,'adfasdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4().hex]
        username='username'
        for cid in cids:
            self.assertRaises(exceptions.BadParametersException, circleapi.delete_user_from_circle, cid=cid, username=username)

    def test_delete_user_from_circle_failure_invalid_username(self):
        ''' delete_user_from_circle should fail if username is invalid '''
        usernames=[None,23234,23423.23423,'adf asdf',['a','list'],{'a':'dict'},('a','tuple'),{'set'},uuid.uuid1(), timeuuid.uuid1(), uuid.uuid4()]
        cid=uuid.uuid4()
        for username in usernames:
            self.assertRaises(exceptions.BadParametersException, circleapi.delete_user_from_circle, cid=cid, username=username)

    def test_delete_user_from_circle_failure_non_existent_circle(self):
        ''' delete_user_from_circle should fail if circle does not exist '''
        cid=uuid.uuid4()
        username='test_delete_user_from_circle_failure_non_existent_circle'
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.delete_user_from_circle, cid=cid, username=username)

    def test_delete_user_from_circle_failure_non_users_circle_type(self):
        ''' add_user_to_circle should fail if circle is not of type USERS_CIRCLE '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='OTHER NON EXISTENT TYPE'
        creation_date=timeuuid.uuid1()
        circlename='test_delete_user_from_circle_failure_non_users_circle_type'
        username='test_delete_user_from_circle_failure_non_users_circle_type_username'
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=None)
        self.assertTrue(cassapicircle.new_circle(circle=circle))
        self.assertRaises(exceptions.CircleNotFoundException, circleapi.delete_user_from_circle, cid=cid, username=username)

    def test_delete_user_from_circle_failure_member_does_not_exist(self):
        ''' delete_user_from_circle should fail if member does not exist '''
        username='test_delete_user_from_circle_failure_member_does_not_exist'
        email=username+'@komlog.org'
        password='password'
        circlename='test_delete_user_from_circle_failure_member_does_not_exist_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username='test_delete_user_from_circle_failure_member_does_not_exist_member'
        self.assertRaises(exceptions.UserNotFoundException, circleapi.delete_user_from_circle, cid=cid, username=new_username)

    def test_delete_user_from_circle_success(self):
        ''' delete_user_from_circle should succeed '''
        username='test_delete_user_from_circle_success'
        email=username+'@komlog.org'
        password='password'
        circlename='test_delete_user_from_circle_success_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username='test_delete_user_from_circle_success_circle_new_member'
        email=new_username+'@komlog.org'
        password='password'
        new_user=userapi.create_user(username=new_username, password=password, email=email)
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[{'username':new_username,'uid':new_user['uid']}])
        self.assertTrue(circleapi.delete_user_from_circle(cid=cid, username=new_username))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])

    def test_delete_user_from_circle_success_no_previous_members(self):
        ''' delete_user_from_circle should succeed even if no previous member was in circle '''
        username='test_delete_user_from_circle_success_no_previous_members'
        email=username+'@komlog.org'
        password='password'
        circlename='test_delete_user_from_circle_success_no_previous_members_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username='test_delete_user_from_circle_success_no_previous_members_circle_new_member'
        email=new_username+'@komlog.org'
        password='password'
        new_user=userapi.create_user(username=new_username, password=password, email=email)
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        self.assertTrue(circleapi.delete_user_from_circle(cid=cid, username=new_username))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])

    def test_delete_user_from_circle_success_some_members_left(self):
        ''' delete_user_from_circle should succeed and delete only the requested member '''
        username='test_delete_user_from_circle_success_some_members_left'
        email=username+'@komlog.org'
        password='password'
        circlename='test_delete_user_from_circle_success_some_members_left_circle'
        user=userapi.create_user(username=username, password=password, email=email)
        circle=circleapi.new_users_circle(uid=user['uid'], circlename=circlename)
        self.assertIsNotNone(circle)
        self.assertTrue(isinstance(circle['cid'],uuid.UUID))
        cid=circle['cid']
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(db_circle['members'],[])
        new_username1='test_delete_user_from_circle_success_some_members_left_new_member1'
        email=new_username1+'@komlog.org'
        password='password'
        new_user1=userapi.create_user(username=new_username1, password=password, email=email)
        new_username2='test_delete_user_from_circle_success_some_members_left_new_member2'
        email=new_username2+'@komlog.org'
        password='password'
        new_user2=userapi.create_user(username=new_username2, password=password, email=email)
        members=[]
        members.append({'username':new_username1,'uid':new_user1['uid']})
        members.append({'username':new_username2,'uid':new_user2['uid']})
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username1))
        self.assertTrue(circleapi.add_user_to_circle(cid=cid, username=new_username2))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(sorted(db_circle['members'], key=lambda x: x['username']),sorted(members, key=lambda x: x['username']))
        members=[]
        members.append({'username':new_username1,'uid':new_user1['uid']})
        self.assertTrue(circleapi.delete_user_from_circle(cid=cid, username=new_username2))
        db_circle=circleapi.get_users_circle_config(cid=cid)
        self.assertEqual(db_circle['cid'],circle['cid'])
        self.assertEqual(db_circle['circlename'],circlename)
        self.assertEqual(db_circle['uid'],user['uid'])
        self.assertEqual(len(db_circle['members']),1)
        self.assertEqual(db_circle['members'],members)

