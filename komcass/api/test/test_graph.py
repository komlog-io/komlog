import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.api import graph as graphapi
from komcass.model.orm import graph as ormgraph
from komfig import logger

class KomcassApiGraphTest(unittest.TestCase):
    ''' komlog.komcass.api.graph tests '''

    def test_get_member_in_relations_non_existent_relations(self):
        ''' get_member_in_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_member_in_relations(idd=nodeid),[])

    def test_get_member_in_relations_existent_relations(self):
        ''' get_member_in_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.MemberRelation(idd=nodeid,ido=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        relations=graphapi.get_member_in_relations(idd=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.idd,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.ido,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            types.remove(int(relation.type))

    def test_get_member_out_relations_non_existent_relations(self):
        ''' get_member_out_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_member_out_relations(ido=nodeid),[])

    def test_get_member_out_relations_existent_relations(self):
        ''' get_member_out_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=nodeid,idd=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        relations=graphapi.get_member_out_relations(ido=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.ido,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.idd,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            types.remove(int(relation.type))

    def test_get_member_in_relation_non_existent_relation(self):
        ''' get_member_in_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_member_in_relation(ido=ido,idd=idd))

    def test_get_member_in_relation_existent_relation(self):
        ''' get_member_in_relation should return the member relation found '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_member_in_relation(relation))
        relation_db=graphapi.get_member_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)

    def test_get_member_out_relation_non_existent_relation(self):
        ''' get_member_out_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_member_out_relation(ido=ido,idd=idd))

    def test_get_member_out_relation_existent_relation(self):
        ''' get_member_out_relation should return the member relation found '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_member_out_relation(relation))
        relation_db=graphapi.get_member_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)

    def test_get_bounded_share_in_relations_non_existent_relations(self):
        ''' get_bounded_share_in_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_bounded_share_in_relations(idd=nodeid),[])

    def test_get_bounded_share_in_relations_existent_relations(self):
        ''' get_bounded_share_in_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(idd=nodeid,ido=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        relations=graphapi.get_bounded_share_in_relations(idd=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.idd,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.ido,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            self.assertTrue(isinstance(relation.interval_init,uuid.UUID))
            self.assertTrue(isinstance(relation.interval_end,uuid.UUID))
            self.assertEqual(relation.perm,1)
            types.remove(int(relation.type))

    def test_get_bounded_share_out_relations_non_existent_relations(self):
        ''' get_bounded_share_out_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_bounded_share_out_relations(ido=nodeid),[])

    def test_get_bounded_share_out_relations_existent_relations(self):
        ''' get_bounded_share_out_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=nodeid,idd=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        relations=graphapi.get_bounded_share_out_relations(ido=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.ido,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.idd,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            self.assertTrue(isinstance(relation.interval_init,uuid.UUID))
            self.assertTrue(isinstance(relation.interval_end,uuid.UUID))
            self.assertEqual(relation.perm,1)
            types.remove(int(relation.type))

    def test_get_bounded_share_in_relation_non_existent_relation(self):
        ''' get_bounded_share_in_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_bounded_share_in_relation(ido=ido,idd=idd))

    def test_get_bounded_share_in_relation_existent_relation(self):
        ''' get_bounded_share_in_relation should return the bounded_share relation found '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        perm=2
        creation_date=timeuuid.uuid1()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        relation_db=graphapi.get_bounded_share_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.perm,relation_db.perm)
        self.assertEqual(relation.interval_init,relation_db.interval_init)
        self.assertEqual(relation.interval_end,relation_db.interval_end)

    def test_get_bounded_share_out_relation_non_existent_relation(self):
        ''' get_bounded_share_out_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_bounded_share_out_relation(ido=ido,idd=idd))

    def test_get_bounded_share_out_relation_existent_relation(self):
        ''' get_bounded_share_out_relation should return the bounded_share relation found '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        perm=2
        creation_date=timeuuid.uuid1()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        relation_db=graphapi.get_bounded_share_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.perm,relation_db.perm)
        self.assertEqual(relation.interval_init,relation_db.interval_init)
        self.assertEqual(relation.interval_end,relation_db.interval_end)

    def test_delete_member_in_relation_existent_relation(self):
        ''' delete_member_in_relation should delete the member relation successfully '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_member_in_relation(relation))
        relation_db=graphapi.get_member_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertTrue(graphapi.delete_member_in_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_member_in_relation(ido=ido,idd=idd))

    def test_delete_member_out_relation_existent_relation(self):
        ''' delete_member_out_relation should delete the member relation successfully '''
        for i in range(1,10):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_member_out_relation(relation))
        relation_db=graphapi.get_member_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertTrue(graphapi.delete_member_out_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_member_out_relation(ido=ido,idd=idd))

    def test_delete_bounded_share_in_relation_existent_relation(self):
        ''' delete_bounded_share_in_relation should delete the bounded_share relation successfully '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        perm=2
        creation_date=timeuuid.uuid1()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        relation_db=graphapi.get_bounded_share_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.perm,relation_db.perm)
        self.assertEqual(relation.interval_init,relation_db.interval_init)
        self.assertEqual(relation.interval_end,relation_db.interval_end)
        self.assertTrue(graphapi.delete_bounded_share_in_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_bounded_share_in_relation(ido=ido,idd=idd))

    def test_delete_bounded_share_out_relation_existent_relation(self):
        ''' delete_bounded_share_out_relation should delete the bounded_share relation successfully '''
        for i in range(1,10):
            relation=ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),perm=1,interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        perm=2
        creation_date=timeuuid.uuid1()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        relation_db=graphapi.get_bounded_share_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.perm,relation_db.perm)
        self.assertEqual(relation.interval_init,relation_db.interval_init)
        self.assertEqual(relation.interval_end,relation_db.interval_end)
        self.assertTrue(graphapi.delete_bounded_share_out_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_bounded_share_out_relation(ido=ido,idd=idd))

    def test_insert_member_in_relation_failure_invalid_relation(self):
        ''' insert_member_in_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',perm=1,creation_date=timeuuid.uuid1(),interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_member_in_relation(relation))

    def test_insert_member_in_relation_success(self):
        ''' insert_member_in_relation should insert the member relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_member_in_relation(relation))
        relation_db=graphapi.get_member_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)

    def test_insert_member_out_relation_failure_invalid_relation(self):
        ''' insert_member_out_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.BoundedShareRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',perm=1,creation_date=timeuuid.uuid1(),interval_init=timeuuid.uuid1(),interval_end=timeuuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_member_out_relation(relation))

    def test_insert_member_out_relation_success(self):
        ''' insert_member_out_relation should insert the member relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.MemberRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_member_out_relation(relation))
        relation_db=graphapi.get_member_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)

    def test_insert_bounded_share_in_relation_failure_invalid_relation(self):
        ''' insert_bounded_share_in_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_bounded_share_in_relation(relation))

    def test_insert_bounded_share_in_relation_success(self):
        ''' insert_bounded_share_in_relation should insert the bounded_share relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        perm=2
        creation_date=timeuuid.uuid1()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        relation_db=graphapi.get_bounded_share_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.perm,relation_db.perm)
        self.assertEqual(relation.interval_init,relation_db.interval_init)
        self.assertEqual(relation.interval_end,relation_db.interval_end)

    def test_insert_bounded_share_out_relation_failure_invalid_relation(self):
        ''' insert_bounded_share_out_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_bounded_share_out_relation(relation))

    def test_insert_bounded_share_out_relation_success(self):
        ''' insert_bounded_share_out_relation should insert the bounded_share relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        perm=2
        creation_date=timeuuid.uuid1()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        relation_db=graphapi.get_bounded_share_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.perm,relation_db.perm)
        self.assertEqual(relation.interval_init,relation_db.interval_init)
        self.assertEqual(relation.interval_end,relation_db.interval_end)

    def test_get_member_in_vertices_non_existent_vertices(self):
        ''' get_member_in_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_member_in_vertices(idd=nodeid),[])

    def test_get_member_in_vertices_existent_vertices(self):
        ''' get_member_in_vertices should return an array with the found vertices '''
        nodeid=uuid.uuid4()
        for i in range(1,11):
            relation=ormgraph.MemberRelation(idd=nodeid,ido=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_in_relation(relation))
        vertices=graphapi.get_member_in_vertices(idd=nodeid)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

    def test_get_member_out_vertices_non_existent_vertices(self):
        ''' get_member_out_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            relation=ormgraph.MemberRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_member_out_vertices(ido=nodeid),[])

    def test_get_member_out_vertices_existent_vertices(self):
        ''' get_member_out_vertices should return an array with the found vertices '''
        nodeid=uuid.uuid4()
        for i in range(1,11):
            relation=ormgraph.MemberRelation(ido=nodeid,idd=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_member_out_relation(relation))
        vertices=graphapi.get_member_out_vertices(ido=nodeid)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

    def test_get_bounded_share_in_vertices_non_existent_vertices(self):
        ''' get_bounded_share_in_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            ido=uuid.uuid4()
            idd=uuid.uuid4()
            type='u2a'
            perm=2
            creation_date=timeuuid.uuid1()
            interval_init=timeuuid.uuid1()
            interval_end=timeuuid.uuid1()
            relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_bounded_share_in_vertices(idd=nodeid),[])

    def test_get_bounded_share_in_vertices_existent_vertices(self):
        ''' get_bounded_share_in_vertices should return an array with vertices found '''
        idd=uuid.uuid4()
        for i in range(1,11):
            ido=uuid.uuid4()
            type='u2a'
            perm=2
            creation_date=timeuuid.uuid1()
            interval_init=timeuuid.uuid1()
            interval_end=timeuuid.uuid1()
            relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
            self.assertTrue(graphapi.insert_bounded_share_in_relation(relation))
        vertices=graphapi.get_bounded_share_in_vertices(idd=idd)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

    def test_get_bounded_share_out_vertices_non_existent_vertices(self):
        ''' get_bounded_share_out_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            ido=uuid.uuid4()
            idd=uuid.uuid4()
            type='u2a'
            perm=2
            creation_date=timeuuid.uuid1()
            interval_init=timeuuid.uuid1()
            interval_end=timeuuid.uuid1()
            relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_bounded_share_out_vertices(ido=nodeid),[])

    def test_get_bounded_share_out_vertices_existent_vertices(self):
        ''' get_bounded_share_out_vertices should return an array with vertices found '''
        ido=uuid.uuid4()
        for i in range(1,11):
            idd=uuid.uuid4()
            type='u2a'
            perm=2
            creation_date=timeuuid.uuid1()
            interval_init=timeuuid.uuid1()
            interval_end=timeuuid.uuid1()
            relation=ormgraph.BoundedShareRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,perm=perm,interval_init=interval_init,interval_end=interval_end)
            self.assertTrue(graphapi.insert_bounded_share_out_relation(relation))
        vertices=graphapi.get_bounded_share_out_vertices(ido=ido)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

