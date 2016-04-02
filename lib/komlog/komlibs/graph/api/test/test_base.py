import unittest
import uuid
from komlog.komlibs.graph.api import base as graphbase
from komlog.komlibs.graph.relations import edge, vertex
from komlog.komlibs.general.time import timeuuid

class GraphApiBaseTest(unittest.TestCase):
    ''' komlog.graph.api.base tests '''

    def test_delete_edge_failure_invalid_ido(self):
        ''' delete_edge should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        edge_type=edge.URI_RELATION
        for ido in idos:
            self.assertFalse(graphbase.delete_edge(ido=ido, idd=idd, edge_type=edge_type))

    def test_delete_edge_failure_invalid_idd(self):
        ''' delete_edge should fail if idd is not valid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        edge_type=edge.URI_RELATION
        for idd in idds:
            self.assertFalse(graphbase.delete_edge(ido=ido, idd=idd, edge_type=edge_type))

    def test_delete_edge_failure_invalid_edge_type(self):
        ''' delete_edge should fail if edge_type is not valid '''
        edges=[None, 9999999, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        for edge_type in edges:
            self.assertFalse(graphbase.delete_edge(ido=ido, idd=idd, edge_type=edge_type))

    def test_delete_edge_success_uri_edge(self):
        ''' delete_edge should succeed if parameters are valid '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        edge_type=edge.URI_RELATION
        uri='test_uri'
        self.assertTrue(graphbase.set_uri_edge(ido=ido, idd=idd, vertex_type=vertex_type, uri=uri))
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        relations=[rel for rel in graphbase.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(len(relations),1)
        self.assertTrue(graphbase.delete_edge(ido=ido, idd=idd, edge_type=edge_type))
        relations=[rel for rel in graphbase.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(relations,[])
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(relations,[])

    def test_delete_edge_success_kin_edge(self):
        ''' delete_edge should succeed if parameters are valid '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        edge_type=edge.KIN_RELATION
        params={'test':'test_param'}
        self.assertTrue(graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type, params=params))
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        relations=[rel for rel in graphbase.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(len(relations),1)
        self.assertTrue(graphbase.delete_edge(ido=ido, idd=idd, edge_type=edge_type))
        relations=[rel for rel in graphbase.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(relations,[])
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(relations,[])

    def test_set_uri_edge_failure_invalid_ido(self):
        ''' set_uri_edge should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        uri='test_uri'
        for ido in idos:
            self.assertFalse(graphbase.set_uri_edge(ido=ido, idd=idd, vertex_type=vertex_type, uri=uri))

    def test_set_uri_edge_failure_invalid_idd(self):
        ''' set_uri_edge should fail if idd is invalid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        uri='test_uri'
        for idd in idds:
            self.assertFalse(graphbase.set_uri_edge(ido=ido, idd=idd, vertex_type=vertex_type, uri=uri))

    def test_set_uri_edge_failure_invalid_vertex_type(self):
        ''' set_uri_edge should fail if vertex_type is invalid '''
        vertex=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri'
        for vertex_type in vertex:
            self.assertFalse(graphbase.set_uri_edge(ido=ido, idd=idd, vertex_type=vertex_type, uri=uri))

    def test_set_uri_edge_failure_invalid_uri(self):
        ''' set_uri_edge should fail if interval_init is invalid '''
        uris=[None, 234234.234234, uuid.uuid4(), uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'},'string with spaces','string_with_symbols_#$/%']
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        for uri in uris:
            self.assertFalse(graphbase.set_uri_edge(ido=ido, idd=idd, vertex_type=vertex_type, uri=uri))

    def test_set_uri_edge_success(self):
        ''' set_uri_edge should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        uri='test_uri'
        self.assertTrue(graphbase.set_uri_edge(ido=ido, idd=idd, vertex_type=vertex_type, uri=uri))
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
            self.assertEqual(relation.uri,uri)
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
            self.assertEqual(relation.uri,uri)

    def test_set_kin_edge_failure_invalid_ido(self):
        ''' set_kin_edge should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        params=dict()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        for ido in idos:
            self.assertFalse(graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type, params=params))

    def test_set_uri_edge_failure_invalid_idd(self):
        ''' set_kin_edge should fail if idd is invalid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        params=dict()
        for idd in idds:
            self.assertFalse(graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type, params=params))

    def test_set_uri_edge_failure_invalid_vertex_type(self):
        ''' set_kin_edge should fail if vertex_type is invalid '''
        vertex=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        params=dict()
        for vertex_type in vertex:
            self.assertFalse(graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type,params=params))

    def test_set_uri_edge_failure_invalid_params(self):
        ''' set_kin_edge should fail if params is invalid '''
        paramss=[None, 234234.234234, uuid.uuid4(), uuid.uuid1(), ['a','list'],('a','tuple'),{'set'},'string with spaces','string_with_symbols_#$/%']
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        for params in paramss:
            self.assertFalse(graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type,params=params))

    def test_set_kin_edge_success(self):
        ''' set_kin_edge should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        params=dict()
        self.assertTrue(graphbase.set_kin_edge(ido=ido, idd=idd, vertex_type=vertex_type, params=params))
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
            self.assertEqual(relation.params,params)
        relations=[rel for rel in graphbase.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
            self.assertEqual(relation.params,params)

    def test_gen_get_outgoing_relations_from_failure_invalid_ido(self):
        ''' gen_get_outgoing_relations_from should not return any element if ido is invalid '''
        ido=uuid.uuid4().hex
        edge_type_list=[edge.URI_RELATION]
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=ido, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_outgoing_relations_from_failure_invalid_edge_type_list(self):
        ''' gen_get_outgoing_relations_from should not return any element if ido is invalid '''
        ido=uuid.uuid4()
        edge_type_list='a'
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=ido, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_outgoing_relations_from_success_kin_relation_depth_level_1(self):
        ''' gen_get_outgoing_relations_from should return five uri relations with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        for level1id in level_1_ids:
            graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),5)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type, 'u2a')
            self.assertTrue(relation.idd in level_1_ids)
            level_1_ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_uri_relations_depth_level_1(self):
        ''' gen_get_outgoing_relations_from should return 5 uri relations with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        for level1id in level_1_ids:
            graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),5)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type, 'u2a')
            self.assertTrue(relation.idd in level_1_ids)
            level_1_ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_all_relations_depth_level_1(self):
        ''' gen_get_outgoing_relations_from should return 10 relations with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        for level1id in level_1_ids:
            graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION,edge.KIN_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),10)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type, 'u2a')
            self.assertTrue(relation.idd in level_1_ids)

    def test_gen_get_outgoing_relations_from_success_kin_relations_depth_level_2(self):
        ''' gen_get_outgoing_relations_from should return 6 kin relations with depth level 2 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1id=None
        mylevel2ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                mylevel1id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            for level2id in level_2_ids:
                if index==0:
                    graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                    mylevel2ids.append(level2id)
                else:
                    graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.KIN_RELATION],depth_level=2):
            relations.append(relation)
        self.assertEqual(len(relations),6)
        for relation in relations:
            if relation.type =='u2a':
                self.assertEqual(relation.ido,origin_id)
            elif relation.type =='a2d':
                self.assertEqual(relation.ido,mylevel1id)
                self.assertTrue(relation.idd in mylevel2ids)
                mylevel2ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_kin_uri_depth_level_2(self):
        ''' gen_get_outgoing_relations_from should return 4 uri relations with depth level 2 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.KIN_RELATION],depth_level=2):
            relations.append(relation)
        self.assertEqual(len(relations),4)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type,'u2a')
            self.assertEqual(relation.uri,'uri')
            self.assertTrue(relation.idd in mylevel1ids)
            mylevel1ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_kin_uri_depth_level_unlimited(self):
        ''' gen_get_outgoing_relations_from should return 4 uri relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION],path_edge_type_list=[edge.KIN_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),4)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type,'u2a')
            self.assertEqual(relation.uri,'uri')
            self.assertTrue(relation.idd in mylevel1ids)
            mylevel1ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_all_uri_depth_level_unlimited(self):
        ''' gen_get_outgoing_relations_from should return 4 kin relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),4)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type,'u2a')
            self.assertEqual(relation.uri,'uri')
            self.assertTrue(relation.idd in mylevel1ids)
            mylevel1ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_all_all_depth_level_unlimited(self):
        ''' gen_get_outgoing_relations_from should return 30 relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.URI_RELATION,edge.KIN_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),30)

    def test_gen_get_outgoing_relations_from_success_path_all_all_depth_level_unlimited_avoid_loops(self):
        ''' gen_get_outgoing_relations_from should return 31 relations with depth level unlimited and avoid repeated vertices found '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        level1_origin_id=None
        level1_dest_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                level1_origin_id=level1id
            elif index==1:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                level1_dest_id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
        graphbase.set_kin_edge(ido=level1_origin_id,idd=level1_dest_id,vertex_type='a2a',params={})
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.KIN_RELATION,edge.URI_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),31)

    def test_gen_get_outgoing_relations_from_success_path_kin_kin_depth_level_unlimited_avoid_loops(self):
        ''' gen_get_outgoing_relations_from should return 12 relations with depth level unlimited and avoid repeated vertices found '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        level1_origin_id=None
        level1_dest_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                level1_origin_id=level1id
            elif index==1:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                level1_dest_id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
        graphbase.set_kin_edge(ido=level1_origin_id,idd=level1_dest_id,vertex_type='a2a',params={})
        relations=[]
        for relation in graphbase.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.KIN_RELATION],path_edge_type_list=[edge.KIN_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),12)

    def test_gen_get_incoming_relations_at_failure_invalid_idd(self):
        ''' gen_get_incoming_relations_at should not return any element if idd is invalid '''
        idd=uuid.uuid4().hex
        edge_type_list=[edge.URI_RELATION]
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=idd, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_incoming_relations_at_failure_invalid_edge_type_list(self):
        ''' gen_get_incoming_relations_at should not return any element if edge_type_list is invalid '''
        idd=uuid.uuid4()
        edge_type_list='a'
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=idd, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_incoming_relations_at_success_kin_relation_depth_level_1(self):
        ''' gen_get_incoming_relations_at should return one kin relation with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a', params={})
                my_level1_id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
                else:
                    graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.KIN_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertTrue(relation.ido in level_1_ids)
            self.assertEqual(relation.idd,my_level2_id)
            self.assertEqual(relation.type, 'a2d')

    def test_gen_get_incoming_relations_at_success_kin_relation_depth_level_2(self):
        ''' gen_get_incoming_relations_at should return two kin relations with depth level 2 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                my_level1_id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
                else:
                    graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.KIN_RELATION],depth_level=2):
            relations.append(relation)
        self.assertEqual(len(relations),2)
        for relation in relations:
            self.assertTrue(relation.ido in [origin_id,my_level1_id])
            self.assertTrue(relation.idd in [my_level1_id,my_level2_id])
            self.assertTrue(relation.type in ['a2d','u2a'])

    def test_gen_get_incoming_relations_at_success_kin_relation_depth_level_unlimited(self):
        ''' gen_get_incoming_relations_at should return two kin relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                my_level1_id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
                else:
                    graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.KIN_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),2)
        for relation in relations:
            self.assertTrue(relation.ido in [origin_id,my_level1_id])
            self.assertTrue(relation.idd in [my_level1_id,my_level2_id])
            self.assertTrue(relation.type in ['a2d','u2a'])

    def test_gen_get_incoming_relations_at_success_kin_relation_depth_level_unlimited_path_uri(self):
        ''' gen_get_incoming_relations_at should return only one kin relation with depth level unlimited and path uri '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                my_level1_id=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
                else:
                    graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.KIN_RELATION],path_edge_type_list=[edge.URI_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,my_level1_id)
            self.assertEqual(relation.idd,my_level2_id)
            self.assertEqual(relation.type,'a2d')

    def test_gen_get_incoming_relations_at_success_kin_relation_depth_level_unlimited_avoid_loops(self):
        ''' gen_get_incoming_relations_at should return six kin relations with depth level unlimited and avoid loops '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        my_level2_bro=None
        my_level1_bro=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                my_level1_id=level1id
            elif index==4:
                graphbase.set_kin_edge(ido=origin_id,idd=level1id,vertex_type='u2a',params={})
                my_level1_bro=level1id
            else:
                graphbase.set_uri_edge(ido=origin_id,idd=level1id,vertex_type='u2a',uri='uri')
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphbase.set_uri_edge(ido=level1id,idd=level2id,vertex_type='u2a',uri='uri')
                else:
                    graphbase.set_kin_edge(ido=level1id,idd=level2id,vertex_type='a2d',params={})
                    if index==0 and index2==3:
                        my_level2_id=level2id
                    if index==4 and index2==0:
                        my_level2_bro=level2id
        graphbase.set_kin_edge(ido=my_level2_bro,idd=my_level2_id,vertex_type='d2d',params={})
        graphbase.set_kin_edge(ido=my_level1_bro,idd=my_level1_id,vertex_type='a2a',params={})
        relations=[]
        for relation in graphbase.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.KIN_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),6)

    def test_replace_vertex_failure_invalid_actual_vertex(self):
        ''' replace_vertex should fail if actual_vertex is invalid '''
        actual_vertexs=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        new_vertex=uuid.uuid4()
        new_type=vertex.DATASOURCE
        edge_type_list=[edge.URI_RELATION]
        for actual_vertex in actual_vertexs:
            self.assertFalse(graphbase.replace_vertex(actual_vertex=actual_vertex, new_vertex=new_vertex, new_vertex_type=new_type, edge_type_list=edge_type_list))

    def test_replace_vertex_failure_invalid_new_vertex(self):
        ''' replace_vertex should fail if new_vertex is invalid '''
        new_vertexs=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        actual_vertex=uuid.uuid4()
        new_type=vertex.DATASOURCE
        edge_type_list=[edge.URI_RELATION]
        for new_vertex in new_vertexs:
            self.assertFalse(graphbase.replace_vertex(actual_vertex=actual_vertex, new_vertex=new_vertex, new_vertex_type=new_type, edge_type_list=edge_type_list))

    def test_replace_vertex_failure_invalid_new_type(self):
        ''' replace_vertex should fail if new_type is invalid '''
        new_types=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        actual_vertex=uuid.uuid4()
        new_vertex=uuid.uuid4()
        edge_type_list=[edge.URI_RELATION]
        for new_type in new_types:
            self.assertFalse(graphbase.replace_vertex(actual_vertex=actual_vertex, new_vertex=new_vertex, new_vertex_type=new_type, edge_type_list=edge_type_list))

    def test_replace_vertex_failure_invalid_edge_type_list(self):
        ''' replace_vertex should fail if edge_type_list is invalid '''
        edge_type_lists=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},('a','tuple'),{'set'}]
        actual_vertex=uuid.uuid4()
        new_vertex=uuid.uuid4()
        new_type=vertex.DATASOURCE
        for edge_type_list in edge_type_lists:
            self.assertFalse(graphbase.replace_vertex(actual_vertex=actual_vertex, new_vertex=new_vertex, new_vertex_type=new_type, edge_type_list=edge_type_list))

    def test_replace_vertex_success_two_graphs_one_level(self):
        ''' replace_vertex should succeed in the simplest case of two independent graphs with no colissions '''
        ido1=uuid.uuid4()
        ido2=uuid.uuid4()
        idd1=uuid.uuid4()
        idd2=uuid.uuid4()
        uri1='uri1'
        uri2='uri2'
        self.assertTrue(graphbase.set_uri_edge(ido=ido1, idd=idd1, vertex_type=vertex.USER_DATASOURCE_RELATION, uri=uri1))
        self.assertTrue(graphbase.set_uri_edge(ido=ido2, idd=idd2, vertex_type=vertex.USER_DATASOURCE_RELATION, uri=uri2))
        ido1_relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido1):
            ido1_relations.append(rel)
        self.assertEqual(len(ido1_relations),1)
        self.assertEqual(ido1_relations[0].ido,ido1)
        self.assertEqual(ido1_relations[0].idd,idd1)
        self.assertEqual(ido1_relations[0].uri,uri1)
        ido2_relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido2):
            ido2_relations.append(rel)
        self.assertEqual(len(ido2_relations),1)
        self.assertEqual(ido2_relations[0].ido,ido2)
        self.assertEqual(ido2_relations[0].idd,idd2)
        self.assertEqual(ido2_relations[0].uri,uri2)
        self.assertTrue(graphbase.replace_vertex(actual_vertex=idd1, new_vertex=idd2, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))
        idd1_relations=[]
        for rel in graphbase.gen_get_incoming_relations_at(idd=idd1):
            idd1_relations.append(rel)
        self.assertEqual(len(idd1_relations),0)
        idd2_relations=[]
        for rel in graphbase.gen_get_incoming_relations_at(idd=idd2):
            idd2_relations.append(rel)
        self.assertEqual(len(idd2_relations),2)
        for rel in idd2_relations:
            if rel.ido==ido1:
                self.assertTrue(rel.ido, ido1)
                self.assertEqual(rel.idd,idd2)
                self.assertEqual(rel.uri,uri1)
            elif rel.ido==ido2:
                self.assertTrue(rel.ido, ido2)
                self.assertEqual(rel.idd,idd2)
                self.assertEqual(rel.uri,uri2)

    def test_replace_vertex_success_two_graphs_two_levels(self):
        ''' replace_vertex should succeed '''
        ido1=uuid.uuid4()
        ido2=uuid.uuid4()
        idd_level1_1=uuid.uuid4()
        idd_level1_2=uuid.uuid4()
        idd_level2_1=uuid.uuid4()
        idd_level2_2=uuid.uuid4()
        uri_level1_1='level1_uri1'
        uri_level1_2='level1_uri2'
        uri_level2_1='level2_uri1'
        uri_level2_2='level2_uri2'
        self.assertTrue(graphbase.set_uri_edge(ido=ido1, idd=idd_level1_1, vertex_type=vertex.USER_DATASOURCE_RELATION, uri=uri_level1_1))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_1, idd=idd_level2_1, vertex_type=vertex.DATASOURCE_DATAPOINT_RELATION, uri=uri_level2_1))
        self.assertTrue(graphbase.set_uri_edge(ido=ido2, idd=idd_level1_2, vertex_type=vertex.USER_VOID_RELATION, uri=uri_level1_2))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_2, idd=idd_level2_2, vertex_type=vertex.VOID_DATASOURCE_RELATION, uri=uri_level2_2))
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido1)
        self.assertEqual(relations[0].idd,idd_level1_1)
        self.assertEqual(relations[0].uri,uri_level1_1)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido2)
        self.assertEqual(relations[0].idd,idd_level1_2)
        self.assertEqual(relations[0].uri,uri_level1_2)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_1)
        self.assertEqual(relations[0].idd,idd_level2_1)
        self.assertEqual(relations[0].uri,uri_level2_1)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_2)
        self.assertEqual(relations[0].idd,idd_level2_2)
        self.assertEqual(relations[0].uri,uri_level2_2)
        self.assertTrue(graphbase.replace_vertex(actual_vertex=idd_level1_2, new_vertex=idd_level1_1, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))
        relations=[]
        for rel in graphbase.gen_get_incoming_relations_at(idd=idd_level1_2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),0)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),0)
        relations=[]
        for rel in graphbase.gen_get_incoming_relations_at(idd=idd_level1_1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),2)
        for rel in relations:
            if rel.ido==ido1:
                self.assertTrue(rel.ido, ido1)
                self.assertEqual(rel.idd,idd_level1_1)
                self.assertEqual(rel.uri,uri_level1_1)
            elif rel.ido==ido2:
                self.assertTrue(rel.ido, ido2)
                self.assertEqual(rel.idd,idd_level1_1)
                self.assertEqual(rel.uri,uri_level1_2)
        relations=[]
        counter=0
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),2)
        for rel in relations:
            if rel.idd==idd_level2_1:
                counter+=1
                self.assertTrue(rel.ido, idd_level1_1)
                self.assertEqual(rel.idd,idd_level2_1)
                self.assertEqual(rel.uri,uri_level2_1)
            elif rel.idd==idd_level2_2:
                counter+=1
                self.assertTrue(rel.ido, idd_level1_1)
                self.assertEqual(rel.idd,idd_level2_2)
                self.assertEqual(rel.uri,uri_level2_2)
        self.assertEqual(counter,2)

    def test_replace_vertex_failure_conflict_in_incoming_relation(self):
        ''' replace_vertex should fail if a conflict in incoming relation is detected'''
        ido1=uuid.uuid4()
        ido2=uuid.uuid4()
        idd_level1_1=uuid.uuid4()
        idd_level1_2=uuid.uuid4()
        idd_level2_1=uuid.uuid4()
        idd_level2_2=uuid.uuid4()
        uri_level1_1='level1_uri1'
        uri_level1_2='level1_uri2'
        uri_level2_1='level2_uri1'
        uri_level2_2='level2_uri2'
        self.assertTrue(graphbase.set_uri_edge(ido=ido1, idd=idd_level1_1, vertex_type=vertex.USER_DATASOURCE_RELATION, uri=uri_level1_1))
        self.assertTrue(graphbase.set_uri_edge(ido=ido1, idd=idd_level1_2, vertex_type=vertex.USER_VOID_RELATION, uri=uri_level1_2))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_1, idd=idd_level2_1, vertex_type=vertex.DATASOURCE_DATAPOINT_RELATION, uri=uri_level2_1))
        self.assertTrue(graphbase.set_uri_edge(ido=ido2, idd=idd_level1_2, vertex_type=vertex.USER_VOID_RELATION, uri=uri_level1_2))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_2, idd=idd_level2_2, vertex_type=vertex.VOID_DATASOURCE_RELATION, uri=uri_level2_2))
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),2)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido2)
        self.assertEqual(relations[0].idd,idd_level1_2)
        self.assertEqual(relations[0].uri,uri_level1_2)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_1)
        self.assertEqual(relations[0].idd,idd_level2_1)
        self.assertEqual(relations[0].uri,uri_level2_1)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_2)
        self.assertEqual(relations[0].idd,idd_level2_2)
        self.assertEqual(relations[0].uri,uri_level2_2)
        self.assertFalse(graphbase.replace_vertex(actual_vertex=idd_level1_2, new_vertex=idd_level1_1, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))
        self.assertFalse(graphbase.replace_vertex(actual_vertex=idd_level1_1, new_vertex=idd_level1_2, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))

    def test_replace_vertex_failure_conflict_in_outgoing_relation_uri(self):
        ''' replace_vertex should fail if there is a conflict in outgoing relations '''
        ido1=uuid.uuid4()
        ido2=uuid.uuid4()
        idd_level1_1=uuid.uuid4()
        idd_level1_2=uuid.uuid4()
        idd_level2_1=uuid.uuid4()
        idd_level2_2=uuid.uuid4()
        uri_level1_1='level1_uri1'
        uri_level1_2='level1_uri2'
        uri_level2_1='level2_uri1'
        uri_level2_2=uri_level2_1 #this causes the conflict
        self.assertTrue(graphbase.set_uri_edge(ido=ido1, idd=idd_level1_1, vertex_type=vertex.USER_DATASOURCE_RELATION, uri=uri_level1_1))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_1, idd=idd_level2_1, vertex_type=vertex.DATASOURCE_DATAPOINT_RELATION, uri=uri_level2_1))
        self.assertTrue(graphbase.set_uri_edge(ido=ido2, idd=idd_level1_2, vertex_type=vertex.USER_VOID_RELATION, uri=uri_level1_2))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_2, idd=idd_level2_2, vertex_type=vertex.VOID_DATASOURCE_RELATION, uri=uri_level2_2))
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido1)
        self.assertEqual(relations[0].idd,idd_level1_1)
        self.assertEqual(relations[0].uri,uri_level1_1)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido2)
        self.assertEqual(relations[0].idd,idd_level1_2)
        self.assertEqual(relations[0].uri,uri_level1_2)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_1)
        self.assertEqual(relations[0].idd,idd_level2_1)
        self.assertEqual(relations[0].uri,uri_level2_1)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_2)
        self.assertEqual(relations[0].idd,idd_level2_2)
        self.assertEqual(relations[0].uri,uri_level2_2)
        self.assertFalse(graphbase.replace_vertex(actual_vertex=idd_level1_2, new_vertex=idd_level1_1, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))
        self.assertFalse(graphbase.replace_vertex(actual_vertex=idd_level1_1, new_vertex=idd_level1_2, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))

    def test_replace_vertex_failure_conflict_in_outgoing_relation_same_idd(self):
        ''' replace_vertex should fail if there is a conflict in outgoing relations '''
        ido1=uuid.uuid4()
        ido2=uuid.uuid4()
        idd_level1_1=uuid.uuid4()
        idd_level1_2=uuid.uuid4()
        idd_level2=uuid.uuid4()
        uri_level1_1='level1_uri1'
        uri_level1_2='level1_uri2'
        uri_level2='level2_uri'
        self.assertTrue(graphbase.set_uri_edge(ido=ido1, idd=idd_level1_1, vertex_type=vertex.USER_DATASOURCE_RELATION, uri=uri_level1_1))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_1, idd=idd_level2, vertex_type=vertex.DATASOURCE_DATAPOINT_RELATION, uri=uri_level2))
        self.assertTrue(graphbase.set_uri_edge(ido=ido2, idd=idd_level1_2, vertex_type=vertex.USER_VOID_RELATION, uri=uri_level1_2))
        self.assertTrue(graphbase.set_uri_edge(ido=idd_level1_2, idd=idd_level2, vertex_type=vertex.VOID_DATAPOINT_RELATION, uri=uri_level2))
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido1)
        self.assertEqual(relations[0].idd,idd_level1_1)
        self.assertEqual(relations[0].uri,uri_level1_1)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=ido2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,ido2)
        self.assertEqual(relations[0].idd,idd_level1_2)
        self.assertEqual(relations[0].uri,uri_level1_2)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_1, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_1)
        self.assertEqual(relations[0].idd,idd_level2)
        self.assertEqual(relations[0].uri,uri_level2)
        relations=[]
        for rel in graphbase.gen_get_outgoing_relations_from(ido=idd_level1_2, depth_level=1):
            relations.append(rel)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0].ido,idd_level1_2)
        self.assertEqual(relations[0].idd,idd_level2)
        self.assertEqual(relations[0].uri,uri_level2)
        self.assertFalse(graphbase.replace_vertex(actual_vertex=idd_level1_2, new_vertex=idd_level1_1, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))
        self.assertFalse(graphbase.replace_vertex(actual_vertex=idd_level1_1, new_vertex=idd_level1_2, new_vertex_type=vertex.DATASOURCE, edge_type_list=[edge.URI_RELATION]))

