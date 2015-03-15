import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.api import circle as circleapi
from komcass.model.orm import circle as ormcircle
from komfig import logger


class KomcassApiCircleTest(unittest.TestCase):
    ''' komlog.komcass.api.circle tests '''

    def test_get_circle_non_existent_cid(self):
        ''' get_circle should return None if cid does not exist '''
        cid=uuid.uuid4()
        self.assertIsNone(circleapi.get_circle(cid=cid))

    def test_get_circle_existent_cid(self):
        ''' get_circle should return the Circle object if cid exists '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)

    def test_get_circles_non_existent_uid(self):
        ''' get_circle should return None if cid does not exist '''
        uid=uuid.uuid4()
        self.assertEqual(circleapi.get_circles(uid=uid),[])

    def test_get_circles_non_existent_type(self):
        ''' get_circles should return an empty array if no circle is of specified type '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        circles=circleapi.get_circles(uid=uid,type='a_non_existent_type')
        self.assertEqual(circles,[])

    def test_get_circles_success(self):
        ''' get_circles should return the Circle object array of the user '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        circles=circleapi.get_circles(uid=uid)
        num_circles=0
        cids=[cid,cid2]
        for db_circle in circles:
            self.assertTrue(db_circle.cid in cids)
            self.assertEqual(uid,db_circle.uid)
            self.assertEqual(type,db_circle.type)
            self.assertEqual(creation_date,db_circle.creation_date)
            self.assertEqual(circlename,db_circle.circlename)
            self.assertEqual(members,db_circle.members)
            cids.remove(db_circle.cid)
            num_circles+=1
        self.assertEqual(num_circles,2)

    def test_get_circles_cids_non_existent_uid(self):
        ''' get_circles_cids should return an empty array if uid does not exist '''
        uid=uuid.uuid4()
        self.assertEqual(circleapi.get_circles_cids(uid=uid),[])

    def test_get_circles_cids_non_existent_type(self):
        ''' get_circles_cids should return an empty array if no circle matchs the type '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        db_cids=circleapi.get_circles_cids(uid=uid,type='a_new_type')
        self.assertEqual(db_cids,[])

    def test_get_circles_cids_success(self):
        ''' get_circles_cids should return the cids array of the user '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        cids=[cid,cid2]
        db_cids=circleapi.get_circles_cids(uid=uid)
        self.assertEqual(sorted(cids),sorted(db_cids))

    def test_get_number_of_circles_non_existent_uid(self):
        ''' get_number_of_circles should return 0 if uid does not exist '''
        uid=uuid.uuid4()
        self.assertEqual(circleapi.get_number_of_circles(uid=uid),0)

    def test_get_number_of_circles_non_existent_type(self):
        ''' get_number_of_circles should return 0 if no circle matchs the type '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        db_cids=circleapi.get_number_of_circles(uid=uid,type='a_new_type')
        self.assertEqual(db_cids,0)

    def test_get_number_of_circles_success(self):
        ''' get_circles_cids should return the number of circles of the user '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        db_cids=circleapi.get_number_of_circles(uid=uid)
        self.assertEqual(db_cids,2)

    def test_delete_circle_no_cid(self):
        ''' delete_circle should return True even if circle does not exist '''
        cid=uuid.uuid4()
        self.assertTrue(circleapi.delete_circle(cid=cid))

    def test_delete_circle_success(self):
        ''' delete_circle should delete the circle successfully '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        cid2=uuid.uuid4()
        circle2=ormcircle.Circle(cid=cid2,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle2))
        db_cids=circleapi.get_number_of_circles(uid=uid)
        self.assertEqual(db_cids,2)
        self.assertTrue(circleapi.delete_circle(cid=cid2))
        db_cids=circleapi.get_number_of_circles(uid=uid)
        self.assertEqual(db_cids,1)
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(cid,db_circle.cid)
        self.assertEqual(uid,db_circle.uid)
        self.assertEqual(type,db_circle.type)
        self.assertEqual(creation_date,db_circle.creation_date)
        self.assertEqual(circlename,db_circle.circlename)
        self.assertEqual(members,db_circle.members)

    def test_new_circle_failure_invalid_circle_object(self):
        ''' new_circle_should fail if circle object is invalid '''
        circles=['asdsadf',234234,23423.234234,{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), timeuuid.uuid1()]
        for circle in circles:
            self.assertFalse(circleapi.new_circle(circle=circle))

    def test_new_circle_failure_already_existing_circle(self):
        ''' new_circle should fail if the circle already exists '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)
        self.assertFalse(circleapi.new_circle(circle=circle))

    def test_new_circle_success(self):
        ''' new_circle should succeed if circle does not exist '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.new_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)

    def test_insert_circle_failure_invalid_circle_object(self):
        ''' insert_circle_should fail if circle object is invalid '''
        circles=['asdsadf',234234,23423.234234,{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), timeuuid.uuid1()]
        for circle in circles:
            self.assertFalse(circleapi.insert_circle(circle=circle))

    def test_insert_circle_success_already_existing_circle(self):
        ''' insert_circle should succeed even if the circle already exists '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)
        new_circlename='new_circlename'
        member4=uuid.uuid4()
        members.add(member4)
        db_circle.circlename=new_circlename
        db_circle.members=members
        self.assertTrue(circleapi.insert_circle(circle=db_circle))
        db_circle2=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle2.cid)
        self.assertEqual(circle.uid,db_circle2.uid)
        self.assertEqual(circle.type,db_circle2.type)
        self.assertEqual(circle.creation_date,db_circle2.creation_date)
        self.assertEqual(new_circlename,db_circle2.circlename)
        self.assertEqual(members,db_circle2.members)

    def test_insert_circle_success_non_existing_circle(self):
        ''' insert_circle should succeed if the circle did not exist previously '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)

    def test_add_member_to_circle_failure_non_existent_cid(self):
        ''' add_member_to_circle should fail if cid does not exist '''
        cid=uuid.uuid4()
        member=uuid.uuid4()
        self.assertFalse(circleapi.add_member_to_circle(cid=cid, member=member))

    def test_add_member_to_circle_success(self):
        ''' add_member_to_circle should succeed if the circle exists previously '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.new_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)
        self.assertTrue(circleapi.add_member_to_circle(cid=circle.cid,member=member1))
        members.add(member1)
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(members,db_circle.members)
        self.assertTrue(circleapi.add_member_to_circle(cid=circle.cid,member=member2))
        members.add(member2)
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(members,db_circle.members)
        self.assertTrue(circleapi.add_member_to_circle(cid=circle.cid,member=member2))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(members,db_circle.members)

    def test_delete_member_from_circle_success_no_cid(self):
        ''' delete_member_from_circle should succeed, even if circle does not exist previously '''
        cid=uuid.uuid4()
        member=uuid.uuid4()
        self.assertTrue(circleapi.delete_member_from_circle(cid=cid,member=member))
    
    def test_delete_member_from_circle_success_existing_cid(self):
        ''' delete_member_from_circle should delete member successfully '''
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        type='type'
        creation_date=timeuuid.uuid1()
        circlename='circlename'
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        members=set()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        circle=ormcircle.Circle(cid=cid,uid=uid,type=type,creation_date=creation_date,circlename=circlename,members=members)
        self.assertTrue(circleapi.insert_circle(circle=circle))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(circle.members,db_circle.members)
        self.assertTrue(circleapi.delete_member_from_circle(cid=cid,member=member1))
        members.remove(member1)
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(members,db_circle.members)
        self.assertTrue(circleapi.delete_member_from_circle(cid=cid,member=member3))
        members.remove(member3)
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(members,db_circle.members)
        self.assertTrue(circleapi.delete_member_from_circle(cid=cid,member=member2))
        members.remove(member2)
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(set(),db_circle.members)
        self.assertTrue(circleapi.delete_member_from_circle(cid=cid,member=member2))
        db_circle=circleapi.get_circle(cid=cid)
        self.assertEqual(circle.cid,db_circle.cid)
        self.assertEqual(circle.uid,db_circle.uid)
        self.assertEqual(circle.type,db_circle.type)
        self.assertEqual(circle.creation_date,db_circle.creation_date)
        self.assertEqual(circle.circlename,db_circle.circlename)
        self.assertEqual(set(),db_circle.members)

