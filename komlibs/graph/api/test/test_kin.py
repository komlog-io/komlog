import unittest
import uuid
from komlibs.graph.api import kin as graphkin
from komlibs.graph.relations import edge, vertex
from komlibs.general.time import timeuuid
from komfig import logger

class GraphApiKinTest(unittest.TestCase):
    ''' komlog.graph.api.kin tests '''

    def test_get_kin_relations_failure_invalid_ido(self):
        ''' get_kin_relations should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for ido in idos:
            self.assertIsNone(graphkin.get_kin_relations(ido=ido))

    def test_get_kin_relations_failure_invalid_depth_level(self):
        ''' get_kin_relations should fail if depth_level is not valid '''
        depth_levels=[None, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        for depth_level in depth_levels:
            self.assertIsNone(graphkin.get_kin_relations(ido=ido, depth_level=depth_level))

    def test_get_kin_relations_success_no_relations(self):
        ''' get_kin_relations should succeed but no relations '''
        ido=uuid.uuid4()
        self.assertEqual(graphkin.get_kin_relations(ido=ido),[])

    def test_get_kin_relations_success_one_relation(self):
        ''' get_kin_relations should succeed and return one relation '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        self.assertTrue(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['id'], idd)
        self.assertEqual(relations[0]['type'], vertex.WIDGET)
        self.assertEqual(relations[0]['params'], params)

    def test_set_kin_relation_failure_invalid_ido(self):
        ''' set_kin_relation should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        for ido in idos:
            self.assertFalse(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))

    def test_set_kin_relation_failure_invalid_idd(self):
        ''' set_kin_relation should fail if idd is not valid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        for idd in idds:
            self.assertFalse(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))

    def test_set_kin_relation_failure_invalid_vertex_type(self):
        ''' set_kin_relation should fail if vertex_type is not valid '''
        vertices=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        params=dict()
        for vertex in vertices:
            self.assertFalse(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex, params=params))

    def test_set_kin_relation_failure_invalid_params(self):
        ''' set_kin_relation should fail if params is not valid '''
        paramss=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        for params in paramss:
            self.assertFalse(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))

    def test_set_kin_relation_success(self):
        ''' set_kin_relation should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        self.assertTrue(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['id'], idd)
        self.assertEqual(relations[0]['type'], vertex.WIDGET)
        self.assertEqual(relations[0]['params'], params)

    def test_delete_kin_relations_failure_invalid_ido(self):
        ''' delete_kin_relations should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for ido in idos:
            self.assertFalse(graphkin.delete_kin_relations(ido=ido))

    def test_delete_kin_relations_success(self):
        ''' delete_kin_relations should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        self.assertTrue(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        self.assertTrue(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),2)
        self.assertTrue(graphkin.delete_kin_relations(ido=ido))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),0)

    def test_delete_kin_relation_failure_invalid_ido(self):
        ''' delete_kin_relation should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        for ido in idos:
            self.assertFalse(graphkin.delete_kin_relation(ido=ido,idd=idd))

    def test_delete_kin_relation_failure_invalid_idd(self):
        ''' delete_kin_relation should fail if idd is not valid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        for idd in idds:
            self.assertFalse(graphkin.delete_kin_relation(ido=ido,idd=idd))

    def test_delete_kin_relation_success(self):
        ''' delete_kin_relation should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        self.assertTrue(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))
        idd=uuid.uuid4()
        vertex_type=vertex.WIDGET_WIDGET_RELATION
        params=dict()
        self.assertTrue(graphkin.set_kin_relation(ido=ido,idd=idd, vertex_type=vertex_type, params=params))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),2)
        self.assertTrue(graphkin.delete_kin_relation(ido=ido,idd=idd))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),1)

    def test_kin_widgets_failure_invalid_ido(self):
        ''' kin_widgets should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        for ido in idos:
            self.assertFalse(graphkin.kin_widgets(ido=ido,idd=idd))

    def test_kin_widgets_failure_invalid_idd(self):
        ''' kin_widgets should fail if idd is not valid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        for idd in idds:
            self.assertFalse(graphkin.kin_widgets(ido=ido,idd=idd))

    def test_kin_widgets_failure_invalid_params(self):
        ''' kin_widgets should fail if idd is not valid '''
        paramss=[234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), ['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        for params in paramss:
            self.assertFalse(graphkin.kin_widgets(ido=ido,idd=idd, params=params))

    def test_kin_widgets_success(self):
        ''' kin_widgets should succeed and return one relation per widget '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertTrue(graphkin.kin_widgets(ido=ido,idd=idd))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['id'], idd)
        self.assertEqual(relations[0]['type'], vertex.WIDGET)
        self.assertEqual(relations[0]['params'],dict())
        relations=graphkin.get_kin_relations(ido=idd)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['id'], ido)
        self.assertEqual(relations[0]['type'], vertex.WIDGET)
        self.assertEqual(relations[0]['params'],dict())

    def test_unkin_widgets_failure_invalid_ido(self):
        ''' unkin_widgets should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        for ido in idos:
            self.assertFalse(graphkin.unkin_widgets(ido=ido,idd=idd))

    def test_unkin_widgets_failure_invalid_idd(self):
        ''' unkin_widgets should fail if idd is not valid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        for idd in idds:
            self.assertFalse(graphkin.unkin_widgets(ido=ido,idd=idd))

    def test_unkin_widgets_success(self):
        ''' unkin_widgets should succeed and delete relations '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertTrue(graphkin.kin_widgets(ido=ido,idd=idd))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['id'], idd)
        self.assertEqual(relations[0]['type'], vertex.WIDGET)
        self.assertEqual(relations[0]['params'],dict())
        relations=graphkin.get_kin_relations(ido=idd)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['id'], ido)
        self.assertEqual(relations[0]['type'], vertex.WIDGET)
        self.assertEqual(relations[0]['params'],dict())
        self.assertTrue(graphkin.unkin_widgets(ido=ido, idd=idd))
        relations=graphkin.get_kin_relations(ido=ido)
        self.assertEqual(len(relations),0)
        relations=graphkin.get_kin_relations(ido=idd)
        self.assertEqual(len(relations),0)

    def test_get_kin_widgets_failure_invalid_ido(self):
        ''' get_kin_widgets should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for ido in idos:
            self.assertEqual(graphkin.get_kin_widgets(ido=ido),[])

    def test_get_kin_widgets_success(self):
        ''' get_kin_widgets should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        self.assertTrue(graphkin.kin_widgets(ido=ido,idd=idd))
        relations=graphkin.get_kin_widgets(ido=ido)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['wid'], idd)
        self.assertEqual(relations[0]['params'],dict())
        relations=graphkin.get_kin_widgets(ido=idd)
        self.assertEqual(len(relations),1)
        self.assertEqual(relations[0]['wid'], ido)
        self.assertEqual(relations[0]['params'],dict())

