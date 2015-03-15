import unittest
import uuid
from komlibs.gestaccount.circle import types
from komcass.api import circle as cassapicircle
from komcass.model.orm import circle as ormcircle
from komlibs.auth import operations, permissions
from komlibs.auth.membership import update
from komlibs.general.time import timeuuid
from komlibs.graph import api as graphapi
from komlibs.graph.relations import vertex,edge

class AuthMembershipUpdateTest(unittest.TestCase):
    ''' komlog.auth.membership.update tests '''
    
    def test_get_update_funcs_success(self):
        ''' test_update_funcs should return a list of functions '''
        operation=operations.NEW_CIRCLE
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, list))
        self.assertEqual(update_funcs,['new_circle'])

    def test_get_update_funcs_success_empty_list(self):
        '''test_update_funcs should return an empty list of functions if operation does not exist'''
        operation='234234234'
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, list))
        self.assertEqual(update_funcs, [])

    def test_new_circle_no_cid(self):
        ''' new_circle should fail if no cid is passed'''
        params={}
        self.assertFalse(update.new_circle(params))

    def test_new_circle_success(self):
        ''' new_circle should succeed if graph relations can be set correctly '''
        circlename='test_new_circle_success'
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        members=set()
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        member4=uuid.uuid4()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        members.add(member4)
        circle=ormcircle.Circle(uid=uid,cid=cid,circlename=circlename,creation_date=creation_date,members=members,type=types.USERS_CIRCLE)
        cassapicircle.insert_circle(circle)
        params={'cid':cid}
        self.assertTrue(update.new_circle(params))
        for relation in graphapi.gen_get_incoming_relations_at(idd=cid,edge_type_list=[edge.MEMBER_RELATION], depth_level=1):
            self.assertTrue(relation.ido in members)
            self.assertEqual(relation.idd,cid)
            self.assertEqual(relation.type, vertex.USER_CIRCLE_RELATION)
            members.remove(relation.ido)

    def test_update_circle_members_no_cid(self):
        ''' update_circle_members should fail if no cid is passed'''
        params={}
        self.assertFalse(update.update_circle_members(params))

    def test_update_circle_members_success_adding_an_element(self):
        ''' update_circle_members should succeed if graph relations can be set correctly to the new element '''
        circlename='test_update_circle_members_success_adding_an_element'
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        members=set()
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        member4=uuid.uuid4()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        members.add(member4)
        circle=ormcircle.Circle(uid=uid,cid=cid,circlename=circlename,creation_date=creation_date,members=members,type=types.USERS_CIRCLE)
        cassapicircle.insert_circle(circle)
        params={'cid':cid}
        self.assertTrue(update.new_circle(params))
        member_num=0
        for relation in graphapi.gen_get_incoming_relations_at(idd=cid,edge_type_list=[edge.MEMBER_RELATION], depth_level=1):
            self.assertTrue(relation.ido in members)
            self.assertEqual(relation.idd,cid)
            self.assertEqual(relation.type, vertex.USER_CIRCLE_RELATION)
            members.remove(relation.ido)
            member_num+=1
        self.assertEqual(member_num,4)
        member5=uuid.uuid4()
        circle=cassapicircle.get_circle(cid=cid)
        circle.members.add(member5)
        members=circle.members
        member_num=0
        cassapicircle.insert_circle(circle)
        self.assertTrue(update.update_circle_members(params=params))
        for relation in graphapi.gen_get_incoming_relations_at(idd=cid,edge_type_list=[edge.MEMBER_RELATION], depth_level=1):
            self.assertTrue(relation.ido in members)
            self.assertEqual(relation.idd,cid)
            self.assertEqual(relation.type, vertex.USER_CIRCLE_RELATION)
            members.remove(relation.ido)
            member_num+=1
        self.assertEqual(member_num,5)

    def test_update_circle_members_success_deleting_an_element(self):
        ''' update_circle_members should succeed if graph relations can be removed correctly to the deleted element '''
        circlename='test_update_circle_members_success_deleting_an_element'
        cid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        members=set()
        member1=uuid.uuid4()
        member2=uuid.uuid4()
        member3=uuid.uuid4()
        member4=uuid.uuid4()
        members.add(member1)
        members.add(member2)
        members.add(member3)
        members.add(member4)
        circle=ormcircle.Circle(uid=uid,cid=cid,circlename=circlename,creation_date=creation_date,members=members,type=types.USERS_CIRCLE)
        cassapicircle.insert_circle(circle)
        params={'cid':cid}
        self.assertTrue(update.new_circle(params))
        member_num=0
        for relation in graphapi.gen_get_incoming_relations_at(idd=cid,edge_type_list=[edge.MEMBER_RELATION], depth_level=1):
            self.assertTrue(relation.ido in members)
            self.assertEqual(relation.idd,cid)
            self.assertEqual(relation.type, vertex.USER_CIRCLE_RELATION)
            members.remove(relation.ido)
            member_num+=1
        self.assertEqual(member_num,4)
        circle=cassapicircle.get_circle(cid=cid)
        circle.members.remove(member4)
        members=circle.members
        member_num=0
        cassapicircle.insert_circle(circle)
        self.assertTrue(update.update_circle_members(params=params))
        for relation in graphapi.gen_get_incoming_relations_at(idd=cid,edge_type_list=[edge.MEMBER_RELATION], depth_level=1):
            self.assertTrue(relation.ido in members)
            self.assertEqual(relation.idd,cid)
            self.assertEqual(relation.type, vertex.USER_CIRCLE_RELATION)
            members.remove(relation.ido)
            member_num+=1
        self.assertEqual(member_num,3)

