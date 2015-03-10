import unittest
import uuid
from komlibs.graph import api as graphapi
from komlibs.graph.relations import edge, vertex
from komlibs.general.time import timeuuid

class GraphApiTest(unittest.TestCase):
    ''' komlog.graph.api tests '''

    def test_delete_edge_failure_invalid_ido(self):
        ''' delete_edge should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        edge_type=edge.MEMBER_RELATION
        for ido in idos:
            self.assertFalse(graphapi.delete_edge(ido=ido, idd=idd, edge_type=edge_type))

    def test_delete_edge_failure_invalid_idd(self):
        ''' delete_edge should fail if idd is not valid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        edge_type=edge.MEMBER_RELATION
        for idd in idds:
            self.assertFalse(graphapi.delete_edge(ido=ido, idd=idd, edge_type=edge_type))

    def test_delete_edge_failure_invalid_edge_type(self):
        ''' delete_edge should fail if edge_type is not valid '''
        edges=[None, 9999999, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        for edge_type in edges:
            self.assertFalse(graphapi.delete_edge(ido=ido, idd=idd, edge_type=edge_type))

    def test_delete_edge_success_member_edge(self):
        ''' delete_edge should succeed if parameters are valid '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        edge_type=edge.MEMBER_RELATION
        self.assertTrue(graphapi.set_member_edge(ido=ido, idd=idd,vertex_type='d2d'))
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        relations=[rel for rel in graphapi.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(len(relations),1)
        self.assertTrue(graphapi.delete_edge(ido=ido, idd=idd, edge_type=edge_type))
        relations=[rel for rel in graphapi.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(relations,[])
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(relations,[])

    def test_delete_edge_success_bounded_share_edge(self):
        ''' delete_edge should succeed if parameters are valid '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        edge_type=edge.BOUNDED_SHARE_RELATION
        perm=1
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        self.assertTrue(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        relations=[rel for rel in graphapi.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(len(relations),1)
        self.assertTrue(graphapi.delete_edge(ido=ido, idd=idd, edge_type=edge_type))
        relations=[rel for rel in graphapi.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(relations,[])
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(relations,[])

    def test_set_member_edge_failure_invalid_ido(self):
        ''' set_member_edge should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        for ido in idos:
            self.assertFalse(graphapi.set_member_edge(ido=ido, idd=idd, vertex_type=vertex_type))

    def test_set_member_edge_failure_invalid_idd(self):
        ''' set_member_edge should fail if idd is invalid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        for idd in idds:
            self.assertFalse(graphapi.set_member_edge(ido=ido, idd=idd, vertex_type=vertex_type))

    def test_set_member_edge_failure_invalid_vertex_type(self):
        ''' set_member_edge should fail if vertex_type is invalid '''
        vertex=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        for vertex_type in vertex:
            self.assertFalse(graphapi.set_member_edge(ido=ido, idd=idd, vertex_type=vertex_type))

    def test_set_member_edge_success(self):
        ''' set_member_edge should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        self.assertTrue(graphapi.set_member_edge(ido=ido, idd=idd, vertex_type=vertex_type))
        relations=[rel for rel in graphapi.gen_get_outgoing_relations_from(ido=ido)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)

    def test_set_bounded_share_edge_failure_invalid_ido(self):
        ''' set_bounded_share_edge should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        perm=1
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        for ido in idos:
            self.assertFalse(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))

    def test_set_bounded_share_edge_failure_invalid_idd(self):
        ''' set_bounded_share_edge should fail if idd is invalid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        perm=1
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        for idd in idds:
            self.assertFalse(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))

    def test_set_bounded_share_edge_failure_invalid_vertex_type(self):
        ''' set_bounded_share_edge should fail if vertex_type is invalid '''
        vertex=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        perm=1
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        for vertex_type in vertex:
            self.assertFalse(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))

    def test_set_bounded_share_edge_failure_invalid_perm(self):
        ''' set_bounded_share_edge should fail if perm is invalid '''
        perms=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        for perm in perms:
            self.assertFalse(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))

    def test_set_bounded_share_edge_failure_invalid_interval_init(self):
        ''' set_bounded_share_edge should fail if interval_init is invalid '''
        interval_inits=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        perm=1
        interval_end=timeuuid.uuid1()
        for interval_init in interval_inits:
            self.assertFalse(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))

    def test_set_bounded_share_edge_failure_invalid_interval_end(self):
        ''' set_bounded_share_edge should fail if interval_end is invalid '''
        interval_ends=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid4(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        perm=1
        interval_init=timeuuid.uuid1()
        for interval_end in interval_ends:
            self.assertFalse(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))

    def test_set_bounded_share_edge_success(self):
        ''' set_bounded_share_edge should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.USER_AGENT_RELATION
        perm=1
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        self.assertTrue(graphapi.set_bounded_share_edge(ido=ido, idd=idd, vertex_type=vertex_type, perm=perm, interval_init=interval_init, interval_end=interval_end))
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
            self.assertEqual(relation.perm,perm)
            self.assertTrue(isinstance(relation.interval_init, uuid.UUID))
            self.assertTrue(isinstance(relation.interval_end, uuid.UUID))
        relations=[rel for rel in graphapi.gen_get_incoming_relations_at(idd=idd)]
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,ido)
            self.assertEqual(relation.idd,idd)
            self.assertEqual(relation.type,vertex.USER_AGENT_RELATION)
            self.assertEqual(relation.perm,perm)
            self.assertTrue(isinstance(relation.interval_init, uuid.UUID))
            self.assertTrue(isinstance(relation.interval_end, uuid.UUID))

    def test_gen_get_outgoing_relations_from_failure_invalid_ido(self):
        ''' gen_get_outgoing_relations_from should not return any element if ido is invalid '''
        ido=uuid.uuid4().hex
        edge_type_list=[edge.MEMBER_RELATION]
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=ido, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_outgoing_relations_from_failure_invalid_edge_type_list(self):
        ''' gen_get_outgoing_relations_from should not return any element if ido is invalid '''
        ido=uuid.uuid4()
        edge_type_list='a'
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=ido, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_outgoing_relations_from_success_member_relation_depth_level_1(self):
        ''' gen_get_outgoing_relations_from should return five member relations with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        for level1id in level_1_ids:
            graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.MEMBER_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),5)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type, 'u2a')
            self.assertTrue(relation.idd in level_1_ids)
            level_1_ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_bounded_share_relations_depth_level_1(self):
        ''' gen_get_outgoing_relations_from should return 5 bounded share relations with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        for level1id in level_1_ids:
            graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.BOUNDED_SHARE_RELATION],depth_level=1):
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
            graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.MEMBER_RELATION,edge.BOUNDED_SHARE_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),10)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type, 'u2a')
            self.assertTrue(relation.idd in level_1_ids)

    def test_gen_get_outgoing_relations_from_success_member_relations_depth_level_2(self):
        ''' gen_get_outgoing_relations_from should return 6 member relations with depth level 2 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1id=None
        mylevel2ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                mylevel1id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            for level2id in level_2_ids:
                if index==0:
                    graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                    mylevel2ids.append(level2id)
                else:
                    graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.MEMBER_RELATION],depth_level=2):
            relations.append(relation)
        self.assertEqual(len(relations),6)
        for relation in relations:
            if relation.type =='u2a':
                self.assertEqual(relation.ido,origin_id)
            elif relation.type =='a2d':
                self.assertEqual(relation.ido,mylevel1id)
                self.assertTrue(relation.idd in mylevel2ids)
                mylevel2ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_member_bounded_share_depth_level_2(self):
        ''' gen_get_outgoing_relations_from should return 4 bounded share relations with depth level 2 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION],depth_level=2):
            relations.append(relation)
        self.assertEqual(len(relations),4)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type,'u2a')
            self.assertEqual(relation.perm,1)
            self.assertTrue(relation.idd in mylevel1ids)
            mylevel1ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_member_bounded_share_depth_level_unlimited(self):
        ''' gen_get_outgoing_relations_from should return 4 bounded share relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.BOUNDED_SHARE_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),4)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type,'u2a')
            self.assertEqual(relation.perm,1)
            self.assertTrue(relation.idd in mylevel1ids)
            mylevel1ids.remove(relation.idd)

    def test_gen_get_outgoing_relations_from_success_path_all_bounded_share_depth_level_unlimited(self):
        ''' gen_get_outgoing_relations_from should return 4 member relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.BOUNDED_SHARE_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),4)
        for relation in relations:
            self.assertEqual(relation.ido,origin_id)
            self.assertEqual(relation.type,'u2a')
            self.assertEqual(relation.perm,1)
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
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.BOUNDED_SHARE_RELATION,edge.MEMBER_RELATION]):
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
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                level1_origin_id=level1id
            elif index==1:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                level1_dest_id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
        graphapi.set_member_edge(ido=level1_origin_id,idd=level1_dest_id,vertex_type='a2a')
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.BOUNDED_SHARE_RELATION,edge.MEMBER_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),31)

    def test_gen_get_outgoing_relations_from_success_path_member_member_depth_level_unlimited_avoid_loops(self):
        ''' gen_get_outgoing_relations_from should return 12 relations with depth level unlimited and avoid repeated vertices found '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        level_2_ids=[uuid.uuid4() for i in range(0,5)]
        mylevel1ids=[]
        level1_origin_id=None
        level1_dest_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                level1_origin_id=level1id
            elif index==1:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                level1_dest_id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                mylevel1ids.append(level1id)
            for level2id in level_2_ids:
                graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
        graphapi.set_member_edge(ido=level1_origin_id,idd=level1_dest_id,vertex_type='a2a')
        relations=[]
        for relation in graphapi.gen_get_outgoing_relations_from(ido=origin_id,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.MEMBER_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),12)

    def test_gen_get_incoming_relations_at_failure_invalid_idd(self):
        ''' gen_get_incoming_relations_at should not return any element if idd is invalid '''
        idd=uuid.uuid4().hex
        edge_type_list=[edge.MEMBER_RELATION]
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=idd, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_incoming_relations_at_failure_invalid_edge_type_list(self):
        ''' gen_get_incoming_relations_at should not return any element if edge_type_list is invalid '''
        idd=uuid.uuid4()
        edge_type_list='a'
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=idd, edge_type_list=edge_type_list):
            relations.append(relation)
        self.assertEqual(relations,[])

    def test_gen_get_incoming_relations_at_success_member_relation_depth_level_1(self):
        ''' gen_get_incoming_relations_at should return one member relation with depth level 1 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                my_level1_id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                else:
                    graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.MEMBER_RELATION],depth_level=1):
            relations.append(relation)
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertTrue(relation.ido in level_1_ids)
            self.assertEqual(relation.idd,my_level2_id)
            self.assertEqual(relation.type, 'a2d')

    def test_gen_get_incoming_relations_at_success_member_relation_depth_level_2(self):
        ''' gen_get_incoming_relations_at should return two member relations with depth level 2 '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                my_level1_id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                else:
                    graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.MEMBER_RELATION],depth_level=2):
            relations.append(relation)
        self.assertEqual(len(relations),2)
        for relation in relations:
            self.assertTrue(relation.ido in [origin_id,my_level1_id])
            self.assertTrue(relation.idd in [my_level1_id,my_level2_id])
            self.assertTrue(relation.type in ['a2d','u2a'])

    def test_gen_get_incoming_relations_at_success_member_relation_depth_level_unlimited(self):
        ''' gen_get_incoming_relations_at should return two member relations with depth level unlimited '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                my_level1_id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                else:
                    graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.MEMBER_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),2)
        for relation in relations:
            self.assertTrue(relation.ido in [origin_id,my_level1_id])
            self.assertTrue(relation.idd in [my_level1_id,my_level2_id])
            self.assertTrue(relation.type in ['a2d','u2a'])

    def test_gen_get_incoming_relations_at_success_member_relation_depth_level_unlimited_path_bounded_share(self):
        ''' gen_get_incoming_relations_at should return only one member relation with depth level unlimited and path bounded share '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                my_level1_id=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                else:
                    graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                    if index==0 and index2==3:
                        my_level2_id=level2id
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.MEMBER_RELATION],path_edge_type_list=[edge.BOUNDED_SHARE_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),1)
        for relation in relations:
            self.assertEqual(relation.ido,my_level1_id)
            self.assertEqual(relation.idd,my_level2_id)
            self.assertEqual(relation.type,'a2d')

    def test_gen_get_incoming_relations_at_success_member_relation_depth_level_unlimited_avoid_loops(self):
        ''' gen_get_incoming_relations_at should return six member relations with depth level unlimited and avoid loops '''
        origin_id=uuid.uuid4()
        level_1_ids=[uuid.uuid4() for i in range(0,5)]
        my_level2_id=None
        my_level1_id=None
        my_level2_bro=None
        my_level1_bro=None
        for index,level1id in enumerate(level_1_ids):
            if index==0:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                my_level1_id=level1id
            elif index==4:
                graphapi.set_member_edge(ido=origin_id,idd=level1id,vertex_type='u2a')
                my_level1_bro=level1id
            else:
                graphapi.set_bounded_share_edge(ido=origin_id,idd=level1id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
            level_2_ids=[uuid.uuid4() for i in range(0,5)]
            for index2,level2id in enumerate(level_2_ids):
                if index==3:
                    graphapi.set_bounded_share_edge(ido=level1id,idd=level2id,vertex_type='u2a',perm=1,interval_init=timeuuid.uuid1(), interval_end=timeuuid.uuid1())
                else:
                    graphapi.set_member_edge(ido=level1id,idd=level2id,vertex_type='a2d')
                    if index==0 and index2==3:
                        my_level2_id=level2id
                    if index==4 and index2==0:
                        my_level2_bro=level2id
        graphapi.set_member_edge(ido=my_level2_bro,idd=my_level2_id,vertex_type='d2d')
        graphapi.set_member_edge(ido=my_level1_bro,idd=my_level1_id,vertex_type='a2a')
        relations=[]
        for relation in graphapi.gen_get_incoming_relations_at(idd=my_level2_id,edge_type_list=[edge.MEMBER_RELATION]):
            relations.append(relation)
        self.assertEqual(len(relations),6)

