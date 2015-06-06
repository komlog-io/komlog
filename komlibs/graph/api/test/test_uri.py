import unittest
import uuid
from komlibs.graph.api import uri as graphuri
from komlibs.graph.relations import edge, vertex
from komlibs.general.time import timeuuid
from komfig import logger

class GraphApiUriTest(unittest.TestCase):
    ''' komlog.graph.api.uri tests '''

    def test_get_id_failure_invalid_ido(self):
        ''' get_id should fail if ido is not valid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uri='test.uri'
        for ido in idos:
            self.assertIsNone(graphuri.get_id(ido=ido, uri=uri))

    def test_get_id_failure_invalid_uri(self):
        ''' get_id should fail if uri is not valid '''
        uris=[234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'},'uri.with.three...consecutive.separators']
        ido=uuid.uuid4()
        for uri in uris:
            self.assertIsNone(graphuri.get_id(ido=ido, uri=uri))

    def test_get_id_success_non_existent_uri(self):
        ''' get_id should return None if uri does not exist '''
        ido=uuid.uuid4()
        uri='non.existent.uri'
        self.assertIsNone(graphuri.get_id(ido=ido,uri=uri))

    def test_get_id_success_existent_uri_one_level(self):
        ''' get_id should return the id associated with the uri passed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        uri_id=graphuri.get_id(ido=ido, uri=uri)
        self.assertIsNotNone(uri_id)
        self.assertEqual(uri_id['id'],idd)
        self.assertEqual(uri_id['type'],vertex.DATASOURCE)

    def test_get_id_success_existent_uri_two_levels(self):
        ''' get_id should return the id associated with the uri passed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri.two_levels'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        uri_id=graphuri.get_id(ido=ido, uri=uri)
        self.assertIsNotNone(uri_id)
        self.assertEqual(uri_id['id'],idd)
        self.assertEqual(uri_id['type'],vertex.DATASOURCE)
        void_uri_id=graphuri.get_id(ido=ido, uri=uri.split('.')[0])
        self.assertIsNotNone(void_uri_id)
        self.assertTrue(isinstance(void_uri_id['id'],uuid.UUID))
        self.assertEqual(void_uri_id['type'],vertex.VOID)

    def test_get_id_success_existent_uri_five_levels(self):
        ''' get_id should return the id associated with the uri passed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri.level_one.level_two.level_three.level_4.level_5'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        uri_id=graphuri.get_id(ido=ido, uri=uri)
        self.assertIsNotNone(uri_id)
        self.assertEqual(uri_id['id'],idd)
        self.assertEqual(uri_id['type'],vertex.DATASOURCE)

    def test_get_id_success_existent_uri_five_levels_last_level_up(self):
        ''' get_id should return the id associated with the uri passed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri.level_one.level_two.level_three.level_4.level_5'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        uri_id=graphuri.get_id(ido=ido, uri=uri)
        self.assertIsNotNone(uri_id)
        self.assertEqual(uri_id['id'],idd)
        self.assertEqual(uri_id['type'],vertex.DATASOURCE)
        same_uri='.'.join((uri,'.level_5','level_5'))
        logger.logger.debug('same_uri: '+same_uri)
        uri_id=graphuri.get_id(ido=ido, uri=same_uri)
        logger.logger.debug('uri_id: '+str(uri_id))
        self.assertIsNotNone(uri_id)
        self.assertEqual(uri_id['id'],idd)
        self.assertEqual(uri_id['type'],vertex.DATASOURCE)

    def test_get_id_adjacents_failure_invalid_ido(self):
        ''' get_id_adjacents should return None if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for ido in idos:
            self.assertIsNone(graphuri.get_id_adjacents(ido=ido))

    def test_get_id_adjacents_success_ido_has_only_descendants(self):
        ''' get_id_adjacents should succeed and return adjacents array '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri.level_one.level_two.level_three.level_4.level_5'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        adjacents=graphuri.get_id_adjacents(ido=ido)
        self.assertIsNotNone(adjacents)
        self.assertEqual(len(adjacents),1)
        self.assertEqual(adjacents[0]['path'],'test_uri')
        self.assertEqual(adjacents[0]['type'],vertex.VOID)

    def test_get_id_adjacents_success_ido_has_only_parents(self):
        ''' get_id_adjacents should succeed and return adjacents array '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri.level_one.level_two.level_three.level_4.level_5'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        adjacents=graphuri.get_id_adjacents(ido=idd)
        self.assertIsNotNone(adjacents)
        self.assertEqual(len(adjacents),1)
        self.assertEqual(adjacents[0]['path'],'.level_5')
        self.assertEqual(adjacents[0]['type'],vertex.VOID)

    def test_get_id_adjacents_success_ido_has_both_descendants_and_parents(self):
        ''' get_id_adjacents should succeed and return adjacents array '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_uri.level_one.level_two.level_three.level_4.level_5'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        vertex_uri='.'.join(uri.split('.')[:-1])
        vertex_id=graphuri.get_id(ido=ido, uri=vertex_uri)
        self.assertIsNotNone(vertex_id)
        adjacents=graphuri.get_id_adjacents(ido=vertex_id['id'])
        self.assertIsNotNone(adjacents)
        self.assertEqual(len(adjacents),2)
        counter=0
        for adjacent in adjacents:
            if adjacent['type']==vertex.VOID:
                self.assertEqual(adjacent['path'],'.level_4')
                self.assertEqual(adjacent['type'],vertex.VOID)
                counter+=1
            if adjacent['type']==vertex.DATASOURCE:
                self.assertEqual(adjacent['path'],'level_5')
                self.assertEqual(adjacent['type'],vertex.DATASOURCE)
                counter+=1
        self.assertEqual(counter,2)

    def test_get_id_adjacents_success_ido_has_no_descendants_nor_parents(self):
        ''' get_id_adjacents should succeed and return and empty array '''
        ido=uuid.uuid4()
        adjacents=graphuri.get_id_adjacents(ido=ido)
        self.assertEqual(adjacents,[])

    def test_new_uri_failure_invalid_ido(self):
        ''' new_uri should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        idd=uuid.uuid4()
        uri='test_new_uri_failure_invalid_ido'
        type=vertex.USER_DATASOURCE_RELATION
        for ido in idos:
            self.assertFalse(graphuri.new_uri(ido=ido, idd=idd, uri=uri, type=type))

    def test_new_uri_failure_invalid_idd(self):
        ''' new_uri should fail if idd is invalid '''
        idds=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        uri='test_new_uri_failure_invalid_idd'
        type=vertex.USER_DATASOURCE_RELATION
        for idd in idds:
            self.assertFalse(graphuri.new_uri(ido=ido, idd=idd, uri=uri, type=type))

    def test_new_uri_failure_invalid_uris(self):
        ''' new_uri should fail if uri is invalid '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uris=[None,234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        type=vertex.USER_DATASOURCE_RELATION
        for uri in uris:
            self.assertFalse(graphuri.new_uri(ido=ido, idd=idd, uri=uri, type=type))

    def test_new_uri_failure_invalid_type(self):
        ''' new_uri should fail if type is invalid '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_new_uri_failure_invalid_type'
        types=[None,234234, 234234.234234, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for type in types:
            self.assertFalse(graphuri.new_uri(ido=ido, idd=idd, uri=uri, type=type))

    def test_new_uri_failure_already_existing_uri(self):
        ''' new_uri should fail if the uri already exists '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_new_uri.failure_tests.already_existing_uri'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        self.assertFalse(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))

    def test_new_uri_success_one_level(self):
        ''' new_uri should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_new_uri'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        existing_uri=graphuri.get_id(ido=ido,uri=uri)
        self.assertIsNotNone(existing_uri)
        self.assertEqual(existing_uri['type'],vertex.DATASOURCE)
        self.assertEqual(existing_uri['id'],idd)

    def test_new_uri_success_two_levels(self):
        ''' new_uri should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_new_uri.success_two_levels'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        existing_uri=graphuri.get_id(ido=ido,uri=uri)
        self.assertIsNotNone(existing_uri)
        self.assertEqual(existing_uri['type'],vertex.DATASOURCE)
        self.assertEqual(existing_uri['id'],idd)
        void_uri_id=graphuri.get_id(ido=ido, uri=uri.split('.')[0])
        self.assertIsNotNone(void_uri_id)
        self.assertTrue(isinstance(void_uri_id['id'],uuid.UUID))
        self.assertEqual(void_uri_id['type'],vertex.VOID)

    def test_new_uri_success_five_levels(self):
        ''' new_uri should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_new_uri.success.five.wait_a_minute.levels'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        existing_uri=graphuri.get_id(ido=ido,uri=uri)
        self.assertIsNotNone(existing_uri)
        self.assertEqual(existing_uri['type'],vertex.DATASOURCE)
        self.assertEqual(existing_uri['id'],idd)

    def test_new_uri_success_multiple_nodes_in_five_levels(self):
        ''' new_uri should succeed '''
        ido=uuid.uuid4()
        idd=uuid.uuid4()
        uri='test_new_uri.success.five.levels.node'
        type=vertex.USER_DATASOURCE_RELATION
        self.assertTrue(graphuri.new_uri(ido=ido,idd=idd,uri=uri,type=type))
        for i in range(1,100):
            new_idd=uuid.uuid4()
            self.assertTrue(graphuri.new_uri(ido=ido,idd=new_idd,uri=uri+str(i),type=type))
        existing_uri=graphuri.get_id(ido=ido,uri=uri)
        self.assertIsNotNone(existing_uri)
        self.assertEqual(existing_uri['type'],vertex.DATASOURCE)
        self.assertEqual(existing_uri['id'],idd)

    def test_new_datasource_uri_failure_invalid_uid(self):
        ''' new_datasource_uri should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        did=uuid.uuid4()
        uri='test_new_datasource_uri_failure_invalid_uid'
        for uid in uids:
            self.assertFalse(graphuri.new_datasource_uri(uid=uid, did=did, uri=uri))

    def test_new_datasource_uri_failure_invalid_did(self):
        ''' new_datasource_uri should fail if did is invalid '''
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        uri='test_new_datasource_uri_failure_invalid_did'
        for did in dids:
            self.assertFalse(graphuri.new_datasource_uri(uid=uid, did=did, uri=uri))

    def test_new_datasource_uri_failure_invalid_uri(self):
        ''' new_datasource_uri should fail if uri is invalid '''
        uris=[None,234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        did=uuid.uuid4()
        uri='test_new_datasource_uri_failure_invalid_uri'
        for uri in uris:
            self.assertFalse(graphuri.new_datasource_uri(uid=uid, did=did, uri=uri))

    def test_new_datasource_uri_success_non_existent_uri_previously(self):
        ''' new_datasource_uri should succeed if the uri did not exist previously '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        uri='test_new_datasource_uri_success_non_existent_uri_previously'
        self.assertTrue(graphuri.new_datasource_uri(uid=uid, did=did, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],did)
        self.assertEqual(db_uri_vertex['type'],vertex.DATASOURCE)

    def test_new_datasource_uri_success_replace_void_vertex(self):
        ''' new_datasource_uri should succeed if the uri belongs to a void vertex, replacing it with the did '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        uri='test_new_datasource_uri_success.void_vertex.datasource'
        self.assertTrue(graphuri.new_datasource_uri(uid=uid, did=did, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],did)
        self.assertEqual(db_uri_vertex['type'],vertex.DATASOURCE)
        void_uri='.'.join(uri.split('.')[:-1])
        void_uri_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.VOID)
        new_did=uuid.uuid4()
        self.assertTrue(graphuri.new_datasource_uri(uid=uid, did=new_did, uri=void_uri))
        void_uri_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.DATASOURCE)
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],did)
        self.assertEqual(db_uri_vertex['type'],vertex.DATASOURCE)

    def test_new_datasource_uri_failure_already_existent_uri(self):
        ''' new_datasource_uri should fail if the uri did exist already and its vertex is not void '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        uri='test_new_datasource_uri_failure.datasource_vertex'
        self.assertTrue(graphuri.new_datasource_uri(uid=uid, did=did, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],did)
        self.assertEqual(db_uri_vertex['type'],vertex.DATASOURCE)
        new_did=uuid.uuid4()
        self.assertFalse(graphuri.new_datasource_uri(uid=uid, did=new_did, uri=uri))

    def test_new_datapoint_uri_failure_invalid_uid(self):
        ''' new_datapoint_uri should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure_invalid_uid'
        for uid in uids:
            self.assertFalse(graphuri.new_datapoint_uri(uid=uid, pid=pid, uri=uri))

    def test_new_datapoint_uri_failure_invalid_did(self):
        ''' new_datapoint_uri should fail if did is invalid '''
        dids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure_invalid_did'
        for did in dids:
            self.assertFalse(graphuri.new_datapoint_uri(did=did, pid=did, uri=uri))

    def test_new_datapoint_uri_failure_invalid_pid(self):
        ''' new_datapoint_uri should fail if pid is invalid '''
        pids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure_invalid_pid'
        for pid in pids:
            self.assertFalse(graphuri.new_datapoint_uri(uid=uid, pid=pid, uri=uri))

    def test_new_datapoint_uri_failure_invalid_uri(self):
        ''' new_datapoint_uri should fail if uri is invalid '''
        uris=[None,234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure_invalid_uri'
        for uri in uris:
            self.assertFalse(graphuri.new_datapoint_uri(uid=uid, pid=pid, uri=uri))

    def test_new_datapoint_uri_failure_no_uid_nor_did_passed(self):
        ''' new_datapoint_uri should fail if not uid nor did is passed '''
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure_invalid_uri'
        self.assertFalse(graphuri.new_datapoint_uri(pid=pid, uri=uri))

    def test_new_datapoint_uri_success_non_existent_uid_uri_previously(self):
        ''' new_datapoint_uri should succeed if the uri did not exist previously '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_success_non_existent_uid_uri_previously'
        self.assertTrue(graphuri.new_datapoint_uri(uid=uid, pid=pid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)

    def test_new_datapoint_uri_success_non_existent_did_uri_previously(self):
        ''' new_datapoint_uri should succeed if the uri did not exist previously '''
        pid=uuid.uuid4()
        did=uuid.uuid4()
        uri='test_new_datapoint_uri_success_non_existent_did_uri_previously'
        self.assertTrue(graphuri.new_datapoint_uri(pid=pid, did=did, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=did, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)

    def test_new_datapoint_uri_success_replace_void_vertex_uid_uri(self):
        ''' new_datapoint_uri should succeed if the uri belongs to a void vertex, replacing it with the pid '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_success.void_vertex.datapoint'
        self.assertTrue(graphuri.new_datapoint_uri(uid=uid, pid=pid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)
        void_uri='.'.join(uri.split('.')[:-1])
        void_uri_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.VOID)
        new_pid=uuid.uuid4()
        self.assertTrue(graphuri.new_datapoint_uri(uid=uid, pid=new_pid, uri=void_uri))
        void_uri_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.DATAPOINT)
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)

    def test_new_datapoint_uri_success_replace_void_vertex_did_uri(self):
        ''' new_datapoint_uri should succeed if the uri belongs to a void vertex, replacing it with the pid '''
        did=uuid.uuid4()
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_success.void_vertex.datapoint'
        self.assertTrue(graphuri.new_datapoint_uri(did=did, pid=pid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=did, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)
        void_uri='.'.join(uri.split('.')[:-1])
        void_uri_vertex=graphuri.get_id(ido=did, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.VOID)
        new_pid=uuid.uuid4()
        self.assertTrue(graphuri.new_datapoint_uri(did=did, pid=new_pid, uri=void_uri))
        void_uri_vertex=graphuri.get_id(ido=did, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.DATAPOINT)
        db_uri_vertex=graphuri.get_id(ido=did, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)

    def test_new_datapoint_uri_failure_already_existent_uid_uri(self):
        ''' new_datapoint_uri should fail if the uri did exist already and its vertex is not void '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure.datapoint_vertex'
        self.assertTrue(graphuri.new_datapoint_uri(uid=uid, pid=pid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)
        new_pid=uuid.uuid4()
        self.assertFalse(graphuri.new_datapoint_uri(uid=uid, pid=new_pid, uri=uri))

    def test_new_datapoint_uri_failure_already_existent_did_uri(self):
        ''' new_datapoint_uri should fail if the uri did exist already and its vertex is not void '''
        did=uuid.uuid4()
        pid=uuid.uuid4()
        uri='test_new_datapoint_uri_failure.datapoint_vertex'
        self.assertTrue(graphuri.new_datapoint_uri(did=did, pid=pid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=did, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],pid)
        self.assertEqual(db_uri_vertex['type'],vertex.DATAPOINT)
        new_pid=uuid.uuid4()
        self.assertFalse(graphuri.new_datapoint_uri(did=did, pid=new_pid, uri=uri))

    def test_new_widget_uri_failure_invalid_uid(self):
        ''' new_widget_uri should fail if uid is invalid '''
        uids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        wid=uuid.uuid4()
        uri='test_new_widget_uri_failure_invalid_uid'
        for uid in uids:
            self.assertFalse(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))

    def test_new_widget_uri_failure_invalid_wid(self):
        ''' new_widget_uri should fail if wid is invalid '''
        wids=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        uri='test_new_widget_uri_failure_invalid_wid'
        for wid in wids:
            self.assertFalse(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))

    def test_new_widget_uri_failure_invalid_uri(self):
        ''' new_widget_uri should fail if uri is invalid '''
        uris=[None,234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        uri='test_new_widget_uri_failure_invalid_uri'
        for uri in uris:
            self.assertFalse(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))

    def test_new_widget_uri_success_non_existent_uri_previously(self):
        ''' new_widget_uri should succeed if the uri wid not exist previously '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        uri='test_new_widget_uri_success_non_existent_uri_previously'
        self.assertTrue(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],wid)
        self.assertEqual(db_uri_vertex['type'],vertex.WIDGET)

    def test_new_widget_uri_success_replace_void_vertex(self):
        ''' new_widget_uri should succeed if the uri belongs to a void vertex, replacing it with the wid '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        uri='test_new_widget_uri_success.void_vertex.widget'
        self.assertTrue(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],wid)
        self.assertEqual(db_uri_vertex['type'],vertex.WIDGET)
        void_uri='.'.join(uri.split('.')[:-1])
        void_uri_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.VOID)
        new_wid=uuid.uuid4()
        self.assertTrue(graphuri.new_widget_uri(uid=uid, wid=new_wid, uri=void_uri))
        void_uri_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_uri_vertex)
        self.assertTrue(isinstance(void_uri_vertex['id'],uuid.UUID))
        self.assertEqual(void_uri_vertex['type'],vertex.WIDGET)
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],wid)
        self.assertEqual(db_uri_vertex['type'],vertex.WIDGET)

    def test_new_widget_uri_failure_already_existent_uri(self):
        ''' new_widget_uri should fail if the uri wid exist already and its vertex is not void '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        uri='test_new_widget_uri_failure.widget_vertex'
        self.assertTrue(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],wid)
        self.assertEqual(db_uri_vertex['type'],vertex.WIDGET)
        new_wid=uuid.uuid4()
        self.assertFalse(graphuri.new_widget_uri(uid=uid, wid=new_wid, uri=uri))

    def test_dissociate_uri_failure_invalid_ido(self):
        ''' dissociate_uri should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        uri='test_dissociate_uri_failure_invalid_ido'
        for ido in idos:
            self.assertFalse(graphuri.dissociate_uri(ido=ido, uri=uri))

    def test_dissociate_uri_failure_invalid_uri(self):
        ''' dissociate_uri should fail if uri is invalid '''
        uris=[None,234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        ido=uuid.uuid4()
        for uri in uris:
            self.assertFalse(graphuri.dissociate_uri(ido=ido, uri=uri))

    def test_dissociate_uri_failure_non_existent_uri(self):
        ''' dissociate_uri should return False if uri does not exist '''
        ido=uuid.uuid4()
        uri='test_dissociate_uri_failure_non_existent_uri'
        self.assertFalse(graphuri.dissociate_uri(ido=ido, uri=uri))

    def test_dissociate_uri_success_already_void_vertex_uri(self):
        ''' dissociate_uri should return True if we try to dissociate a vertex whose type is VOID already '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        uri='test_dissociate_uri.success.widget_uri'
        self.assertTrue(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],wid)
        self.assertEqual(db_uri_vertex['type'],vertex.WIDGET)
        void_uri='.'.join(uri.split('.')[:-1])
        void_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_vertex)
        self.assertTrue(isinstance(void_vertex['id'],uuid.UUID))
        self.assertEqual(void_vertex['type'],vertex.VOID)
        self.assertTrue(graphuri.dissociate_uri(ido=uid, uri=void_uri))
        void_vertex2=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_vertex2)
        self.assertEqual(void_vertex2['id'],void_vertex['id'])
        self.assertEqual(void_vertex2['type'],vertex.VOID)
        widget_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(widget_vertex)
        self.assertEqual(widget_vertex['id'],wid)
        self.assertEqual(widget_vertex['type'],vertex.WIDGET)

    def test_dissociate_uri_success_previous_vertex_uri_non_void(self):
        ''' dissociate_uri should return True and replace the non void vertex with a void one '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        did_uri='test_dissociate_uri.success.datasource_y'
        pid_uri='datapoint_x'
        self.assertTrue(graphuri.new_datasource_uri(uid=uid, did=did, uri=did_uri))
        self.assertTrue(graphuri.new_datapoint_uri(did=did, pid=pid, uri=pid_uri))
        did_vertex=graphuri.get_id(ido=uid, uri=did_uri)
        self.assertIsNotNone(did_vertex)
        self.assertEqual(did_vertex['id'],did)
        self.assertEqual(did_vertex['type'],vertex.DATASOURCE)
        pid_vertex=graphuri.get_id(ido=did, uri=pid_uri)
        self.assertIsNotNone(pid_vertex)
        self.assertEqual(pid_vertex['id'],pid)
        self.assertEqual(pid_vertex['type'],vertex.DATAPOINT)
        self.assertTrue(graphuri.dissociate_uri(ido=uid, uri=did_uri))
        void_vertex=graphuri.get_id(ido=uid, uri=did_uri)
        self.assertIsNotNone(void_vertex)
        self.assertTrue(isinstance(void_vertex['id'],uuid.UUID))
        self.assertEqual(void_vertex['type'],vertex.VOID)
        pid_abs_uri='.'.join((did_uri,pid_uri))
        pid_vertex2=graphuri.get_id(ido=uid, uri=pid_abs_uri)
        self.assertIsNotNone(pid_vertex2)
        self.assertEqual(pid_vertex2['id'],pid)
        self.assertEqual(pid_vertex2['type'],vertex.DATAPOINT)

    def test_dissociate_vertex_failure_invalid_ido(self):
        ''' dissociate_vertex should fail if ido is invalid '''
        idos=[None,234234, 234234.234234, 'astring',uuid.uuid4().hex, uuid.uuid1().hex, uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'}]
        for ido in idos:
            self.assertFalse(graphuri.dissociate_vertex(ido=ido))

    def test_dissociate_vertex_success_already_void_vertex_uri(self):
        ''' dissociate_vertex should return True if we try to dissociate a vertex whose type is VOID already, replacing with the new vertex id '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        uri='test_dissociate_vertex.success.widget_uri'
        self.assertTrue(graphuri.new_widget_uri(uid=uid, wid=wid, uri=uri))
        db_uri_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(db_uri_vertex)
        self.assertEqual(db_uri_vertex['id'],wid)
        self.assertEqual(db_uri_vertex['type'],vertex.WIDGET)
        void_uri='.'.join(uri.split('.')[:-1])
        void_vertex=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_vertex)
        self.assertTrue(isinstance(void_vertex['id'],uuid.UUID))
        self.assertEqual(void_vertex['type'],vertex.VOID)
        self.assertTrue(graphuri.dissociate_vertex(ido=void_vertex['id']))
        void_vertex2=graphuri.get_id(ido=uid, uri=void_uri)
        self.assertIsNotNone(void_vertex2)
        self.assertNotEqual(void_vertex2['id'],void_vertex['id'])
        self.assertEqual(void_vertex2['type'],vertex.VOID)
        widget_vertex=graphuri.get_id(ido=uid, uri=uri)
        self.assertIsNotNone(widget_vertex)
        self.assertEqual(widget_vertex['id'],wid)
        self.assertEqual(widget_vertex['type'],vertex.WIDGET)

    def test_dissociate_vertex_success_previous_vertex_uri_non_void(self):
        ''' dissociate_vertex should return True and replace the non void vertex with a void one '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        did_uri='test_dissociate_vertex.success.datasource_y'
        pid_uri='datapoint_x'
        self.assertTrue(graphuri.new_datasource_uri(uid=uid, did=did, uri=did_uri))
        self.assertTrue(graphuri.new_datapoint_uri(did=did, pid=pid, uri=pid_uri))
        did_vertex=graphuri.get_id(ido=uid, uri=did_uri)
        self.assertIsNotNone(did_vertex)
        self.assertEqual(did_vertex['id'],did)
        self.assertEqual(did_vertex['type'],vertex.DATASOURCE)
        pid_vertex=graphuri.get_id(ido=did, uri=pid_uri)
        self.assertIsNotNone(pid_vertex)
        self.assertEqual(pid_vertex['id'],pid)
        self.assertEqual(pid_vertex['type'],vertex.DATAPOINT)
        self.assertTrue(graphuri.dissociate_vertex(ido=did))
        void_vertex=graphuri.get_id(ido=uid, uri=did_uri)
        self.assertIsNotNone(void_vertex)
        self.assertTrue(isinstance(void_vertex['id'],uuid.UUID))
        self.assertEqual(void_vertex['type'],vertex.VOID)
        pid_abs_uri='.'.join((did_uri,pid_uri))
        pid_vertex2=graphuri.get_id(ido=uid, uri=pid_abs_uri)
        self.assertIsNotNone(pid_vertex2)
        self.assertEqual(pid_vertex2['id'],pid)
        self.assertEqual(pid_vertex2['type'],vertex.DATAPOINT)

    def test_get_joined_uri_failure_invalid_base_uri(self):
        ''' get_joined_uri should fail if base uri is not valid '''
        uris=[234234, 234234.234234, 'a invalid string', uuid.uuid1(), {'a':'dict'},['a','list'],('a','tuple'),{'set'},'uri.with.three...consecutive.separators']
        for uri in uris:
            self.assertFalse(graphuri.get_joined_uri(base=uri))

    def test_get_joined_uri_success_no_path(self):
        ''' get_joined_uri should succeed '''
        #same result
        uris=['','test_one_level','test.two_levels','test.five.levels.and.up','test.with..relative.uris','test..with..two.relative.uris']
        for uri in uris:
            self.assertEqual(graphuri.get_joined_uri(base=uri),uri)
        #simplifying uris
        uri_pairs=[('test_uri..test_uri',''),
                  ('test.uri..simplified.simplified.uri','test.uri.uri'),
                  ('test.uri..uri..test',''),
                  ('test.uri..previous.continue..other_path..other_path.other_path','test.uri..previous.continue..other_path'),
                  ]
        for uri in uri_pairs:
            self.assertEqual(graphuri.get_joined_uri(base=uri[0]),uri[1])

    def test_get_joined_uri_success_with_path(self):
        ''' get_joined_uri should succeed '''
        uri_path_result=[('test_uri..test_uri','',''),
                         ('test.uri..simplified.simplified.uri','thepath','test.uri.uri.thepath'),
                         ('test.uri..uri..test','path','path'),
                         ('test.uri..previous.continue..other_path..other_path.other_path','.up_level','test.uri..previous.continue..other_path..up_level'),
                        ]
        for uri in uri_path_result:
            self.assertEqual(graphuri.get_joined_uri(base=uri[0],path=uri[1]),uri[2])

