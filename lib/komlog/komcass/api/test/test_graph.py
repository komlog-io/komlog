import unittest
import uuid
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import graph as graphapi
from komlog.komcass.model.orm import graph as ormgraph
from komlog.komfig import logging

class KomcassApiGraphTest(unittest.TestCase):
    ''' komlog.komcass.api.graph tests '''

    def test_get_uri_in_relations_non_existent_relations(self):
        ''' get_uri_in_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='v2u',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_uri_in_relations(idd=nodeid),[])

    def test_get_uri_in_relations_existent_relations(self):
        ''' get_uri_in_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.UriRelation(idd=nodeid,ido=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        relations=graphapi.get_uri_in_relations(idd=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.idd,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.ido,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            self.assertEqual(relation.uri,'test.uri')
            types.remove(int(relation.type))

    def test_get_uri_out_relations_non_existent_relations(self):
        ''' get_uri_out_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='v2v',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_uri_out_relations(ido=nodeid),[])

    def test_get_uri_out_relations_existent_relations(self):
        ''' get_uri_out_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=nodeid,idd=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        relations=graphapi.get_uri_out_relations(ido=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.ido,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.idd,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            self.assertEqual(relation.uri,'test.uri')
            types.remove(int(relation.type))

    def test_get_uri_in_relation_non_existent_relation(self):
        ''' get_uri_in_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_uri_in_relation(ido=ido,idd=idd))

    def test_get_uri_in_relation_existent_relation(self):
        ''' get_uri_in_relation should return the uri relation found '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2d',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        uri='test.uri.2'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
        self.assertTrue(graphapi.insert_uri_in_relation(relation))
        relation_db=graphapi.get_uri_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.uri,relation_db.uri)

    def test_get_uri_out_relation_non_existent_relation(self):
        ''' get_uri_out_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_uri_out_relation(ido=ido,idd=idd))

    def test_get_uri_out_relation_existent_relation(self):
        ''' get_uri_out_relation should return the uri relation found '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        uri='test.uri.2'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
        self.assertTrue(graphapi.insert_uri_out_relation(relation))
        relation_db=graphapi.get_uri_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.uri,relation_db.uri)

    def test_delete_uri_in_relation_existent_relation(self):
        ''' delete_uri_in_relation should delete the uri relation successfully '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        uri='test.uri.2'
        relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
        self.assertTrue(graphapi.insert_uri_in_relation(relation))
        relation_db=graphapi.get_uri_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.uri,relation_db.uri)
        self.assertTrue(graphapi.delete_uri_in_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_uri_in_relation(ido=ido,idd=idd))

    def test_delete_uri_out_relation_existent_relation(self):
        ''' delete_uri_out_relation should delete the uri relation successfully '''
        for i in range(1,10):
            relation=ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1(),uri='test.uri')
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        uri='test.uri.2'
        relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
        self.assertTrue(graphapi.insert_uri_out_relation(relation))
        relation_db=graphapi.get_uri_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.uri,relation_db.uri)
        self.assertTrue(graphapi.delete_uri_out_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_uri_out_relation(ido=ido,idd=idd))

    def test_insert_uri_in_relation_failure_invalid_relation(self):
        ''' insert_uri_in_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_uri_in_relation(relation))

    def test_insert_uri_in_relation_success(self):
        ''' insert_uri_in_relation should insert the uri relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        uri='test.uri'
        relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
        self.assertTrue(graphapi.insert_uri_in_relation(relation))
        relation_db=graphapi.get_uri_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.uri,relation_db.uri)

    def test_insert_uri_out_relation_failure_invalid_relation(self):
        ''' insert_uri_out_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_uri_out_relation(relation))

    def test_insert_uri_out_relation_success(self):
        ''' insert_uri_out_relation should insert the uri relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        uri='test.uri'
        relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
        self.assertTrue(graphapi.insert_uri_out_relation(relation))
        relation_db=graphapi.get_uri_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.uri,relation_db.uri)

    def test_get_uri_in_vertices_non_existent_vertices(self):
        ''' get_uri_in_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            ido=uuid.uuid4()
            idd=uuid.uuid4()
            type='u2d'
            creation_date=timeuuid.uuid1()
            uri='test.uri.'+str(i)
            relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_uri_in_vertices(idd=nodeid),[])

    def test_get_uri_in_vertices_existent_vertices(self):
        ''' get_uri_in_vertices should return an array with vertices found '''
        idd=uuid.uuid4()
        for i in range(1,11):
            ido=uuid.uuid4()
            type='u2a'
            creation_date=timeuuid.uuid1()
            uri='test.uri.'+str(i)
            relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
            self.assertTrue(graphapi.insert_uri_in_relation(relation))
        vertices=graphapi.get_uri_in_vertices(idd=idd)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

    def test_get_uri_out_vertices_non_existent_vertices(self):
        ''' get_uri_out_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            ido=uuid.uuid4()
            idd=uuid.uuid4()
            type='u2a'
            creation_date=timeuuid.uuid1()
            uri='test.uri.'+str(i)
            relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_uri_out_vertices(ido=nodeid),[])

    def test_get_uri_out_vertices_existent_vertices(self):
        ''' get_uri_out_vertices should return an array with vertices found '''
        ido=uuid.uuid4()
        for i in range(1,11):
            idd=uuid.uuid4()
            type='u2a'
            creation_date=timeuuid.uuid1()
            uri='test.uri.'+str(i)
            relation=ormgraph.UriRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,uri=uri)
            self.assertTrue(graphapi.insert_uri_out_relation(relation))
        vertices=graphapi.get_uri_out_vertices(ido=ido)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

    def test_get_kin_in_relations_non_existent_relations(self):
        ''' get_kin_in_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='v2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_kin_in_relations(idd=nodeid),[])

    def test_get_kin_in_relations_existent_relations(self):
        ''' get_kin_in_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.KinRelation(idd=nodeid,ido=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        relations=graphapi.get_kin_in_relations(idd=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.idd,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.ido,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            self.assertEqual(relation.params,dict())
            types.remove(int(relation.type))

    def test_get_kin_out_relations_non_existent_relations(self):
        ''' get_kin_out_relations should return an empty array if no existent relations are found '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='v2v',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_kin_out_relations(ido=nodeid),[])

    def test_get_kin_out_relations_existent_relations(self):
        ''' get_kin_out_relations should return an array with the found relations '''
        nodeid=uuid.uuid4()
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=nodeid,idd=uuid.uuid4(),type=str(i),creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        relations=graphapi.get_kin_out_relations(ido=nodeid)
        types=list(range(1,10))
        for relation in relations:
            self.assertEqual(relation.ido,nodeid)
            self.assertTrue(int(relation.type) in types)
            self.assertTrue(isinstance(relation.idd,uuid.UUID))
            self.assertTrue(isinstance(relation.creation_date,uuid.UUID))
            self.assertEqual(relation.params,dict())
            types.remove(int(relation.type))

    def test_get_kin_in_relation_non_existent_relation(self):
        ''' get_kin_in_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_kin_in_relation(ido=ido,idd=idd))

    def test_get_kin_in_relation_existent_relation(self):
        ''' get_kin_in_relation should return the kin relation found '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2d',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        params={'test':'test.kin.2'}
        creation_date=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,params=params)
        self.assertTrue(graphapi.insert_kin_in_relation(relation))
        relation_db=graphapi.get_kin_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.params,relation_db.params)

    def test_get_kin_out_relation_non_existent_relation(self):
        ''' get_kin_out_relation should return None if no existent relation is found '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertIsNone(graphapi.get_kin_out_relation(ido=ido,idd=idd))

    def test_get_kin_out_relation_existent_relation(self):
        ''' get_kin_out_relation should return the kin relation found '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        params={'test':'test.kin.2'}
        creation_date=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date,params=params)
        self.assertTrue(graphapi.insert_kin_out_relation(relation))
        relation_db=graphapi.get_kin_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertEqual(relation.params,relation_db.params)

    def test_delete_kin_in_relation_existent_relation(self):
        ''' delete_kin_in_relation should delete the kin relation successfully '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_kin_in_relation(relation))
        relation_db=graphapi.get_kin_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertTrue(graphapi.delete_kin_in_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_kin_in_relation(ido=ido,idd=idd))

    def test_delete_kin_out_relation_existent_relation(self):
        ''' delete_kin_out_relation should delete the kin relation successfully '''
        for i in range(1,10):
            relation=ormgraph.KinRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',creation_date=timeuuid.uuid1())
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_kin_out_relation(relation))
        relation_db=graphapi.get_kin_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)
        self.assertTrue(graphapi.delete_kin_out_relation(ido=ido,idd=idd))
        self.assertIsNone(graphapi.get_kin_out_relation(ido=ido,idd=idd))

    def test_insert_kin_in_relation_failure_invalid_relation(self):
        ''' insert_kin_in_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',uri='uri',creation_date=uuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_kin_in_relation(relation))

    def test_insert_kin_in_relation_success(self):
        ''' insert_kin_in_relation should insert the kin relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_kin_in_relation(relation))
        relation_db=graphapi.get_kin_in_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)

    def test_insert_kin_out_relation_failure_invalid_relation(self):
        ''' insert_kin_out_relation should fail if relation is invalid '''
        relations=[None,234234,234234.23423,'234234',{'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1(), timeuuid.uuid1(),ormgraph.UriRelation(ido=uuid.uuid4(),idd=uuid.uuid4(),type='u2u',uri='uri',creation_date=uuid.uuid1())]
        for relation in relations:
            self.assertFalse(graphapi.insert_kin_out_relation(relation))

    def test_insert_kin_out_relation_success(self):
        ''' insert_kin_out_relation should insert the kin relation successfully '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        type='u2a'
        creation_date=timeuuid.uuid1()
        relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
        self.assertTrue(graphapi.insert_kin_out_relation(relation))
        relation_db=graphapi.get_kin_out_relation(ido=ido,idd=idd)
        self.assertEqual(relation.ido,relation_db.ido)
        self.assertEqual(relation.idd,relation_db.idd)
        self.assertEqual(relation.type,relation_db.type)
        self.assertEqual(relation.creation_date,relation_db.creation_date)

    def test_get_kin_in_vertices_non_existent_vertices(self):
        ''' get_kin_in_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            ido=uuid.uuid4()
            idd=uuid.uuid4()
            type='u2d'
            creation_date=timeuuid.uuid1()
            relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_kin_in_vertices(idd=nodeid),[])

    def test_get_kin_in_vertices_existent_vertices(self):
        ''' get_kin_in_vertices should return an array with vertices found '''
        idd=uuid.uuid4()
        for i in range(1,11):
            ido=uuid.uuid4()
            type='u2a'
            creation_date=timeuuid.uuid1()
            relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
            self.assertTrue(graphapi.insert_kin_in_relation(relation))
        vertices=graphapi.get_kin_in_vertices(idd=idd)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

    def test_get_kin_out_vertices_non_existent_vertices(self):
        ''' get_kin_out_vertices should return an empty array if no existent vertices are found '''
        for i in range(1,11):
            ido=uuid.uuid4()
            idd=uuid.uuid4()
            type='u2a'
            creation_date=timeuuid.uuid1()
            relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        nodeid=uuid.uuid4()
        self.assertEqual(graphapi.get_kin_out_vertices(ido=nodeid),[])

    def test_get_kin_out_vertices_existent_vertices(self):
        ''' get_kin_out_vertices should return an array with vertices found '''
        ido=uuid.uuid4()
        for i in range(1,11):
            idd=uuid.uuid4()
            type='u2a'
            creation_date=timeuuid.uuid1()
            relation=ormgraph.KinRelation(ido=ido,idd=idd,type=type,creation_date=creation_date)
            self.assertTrue(graphapi.insert_kin_out_relation(relation))
        vertices=graphapi.get_kin_out_vertices(ido=ido)
        self.assertEqual(len(vertices),10)
        for vertex in vertices:
            self.assertTrue(isinstance(vertex,uuid.UUID))

