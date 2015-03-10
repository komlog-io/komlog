import unittest
import uuid
from komlibs.auth import permissions
from komlibs.auth.shared import authorization
from komlibs.graph import api as graphapi
from komlibs.graph.relations import edge, vertex
from komlibs.general.time import timeuuid
from komfig import logger


class AuthSharedAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.shared.authorization tests '''

    def test_authorize_get_datasource_config_success(self):
        ''' authorize_get_datasource_config should succeed if permission is found and granted '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        self.assertTrue(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_config_failure_no_read_permission(self):
        ''' authorize_get_datasource_config should fail if no read permission is found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.NONE, interval_init=ii, interval_end=ie))
        self.assertFalse(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_config_failure_no_bounded_share_relation_on_user(self):
        ''' authorize_get_datasource_config should fail if no bounded_share relation is found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_data_success(self):
        ''' authorize_get_datasource_data should succeed if permission is found and granted '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        self.assertTrue(authorization.authorize_get_datasource_data(uid=uid, did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_failure_no_read_permission(self):
        ''' authorize_get_datasource_data should fail if no read permission is found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.NONE, interval_init=ii, interval_end=ie))
        self.assertFalse(authorization.authorize_get_datasource_data(uid=uid, did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_failure_different_interval_init(self):
        ''' authorize_get_datasource_data should fail if no equal interval_init is found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        ii=timeuuid.uuid1()
        self.assertFalse(authorization.authorize_get_datasource_data(uid=uid, did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_failure_different_interval_end(self):
        ''' authorize_get_datasource_data should fail if no equal interval_end is found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        ie=timeuuid.uuid1()
        self.assertFalse(authorization.authorize_get_datasource_data(uid=uid, did=did, ii=ii, ie=ie))

    def test_authorize_get_datasource_data_failure_no_bounded_share_relation_on_user(self):
        ''' authorize_get_datasource_data should fail if no bounded_share relation is found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=did,idd=nid,vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datasource_data(uid=uid, did=did, ii=ii, ie=ie))

    def test_authorize_get_datapoint_config_success(self):
        ''' authorize_get_datapoint_config should succeed if permission is found and granted '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        self.assertTrue(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_get_datapoint_config_failure_no_read_permission(self):
        ''' authorize_get_datapoint_config should fail if no read permission is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.NONE, interval_init=ii, interval_end=ie))
        self.assertFalse(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_get_datapoint_config_failure_no_bounded_share_relation_on_user(self):
        ''' authorize_get_datapoint_config should fail if no bounded_share relation is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_get_datapoint_data_success(self):
        ''' authorize_get_datapoint_data should succeed if permission is found and granted '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        self.assertTrue(authorization.authorize_get_datapoint_data(uid=uid, pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_failure_no_read_permission(self):
        ''' authorize_get_datapoint_data should fail if no read permission is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.NONE, interval_init=ii, interval_end=ie))
        self.assertFalse(authorization.authorize_get_datapoint_data(uid=uid, pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_failure_different_interval_init(self):
        ''' authorize_get_datapoint_data should fail if no equal interval_init is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        ii=timeuuid.uuid1()
        self.assertFalse(authorization.authorize_get_datapoint_data(uid=uid, pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_failure_different_interval_end(self):
        ''' authorize_get_datapoint_data should fail if no equal interval_end is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        ie=timeuuid.uuid1()
        self.assertFalse(authorization.authorize_get_datapoint_data(uid=uid, pid=pid, ii=ii, ie=ie))

    def test_authorize_get_datapoint_data_failure_no_bounded_share_relation_on_user(self):
        ''' authorize_get_datapoint_data should fail if no bounded_share relation is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_datapoint_data(uid=uid, pid=pid, ii=ii, ie=ie))

    def test_authorize_get_snapshot_config_success(self):
        ''' authorize_get_snapshot_config should succeed if permission is found and granted '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=uid, nid=nid))

    def test_authorize_get_snapshot_config_failure_no_read_permission(self):
        ''' authorize_get_snapshot_config should fail if no read permission is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.NONE, interval_init=ii, interval_end=ie))
        self.assertFalse(authorization.authorize_get_snapshot_config(uid=uid, nid=nid))

    def test_authorize_get_snapshot_config_failure_no_bounded_share_relation_on_user(self):
        ''' authorize_get_snapshot_config should fail if no bounded_share relation is found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        nid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        self.assertTrue(graphapi.set_member_edge(ido=pid,idd=nid,vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION))
        self.assertTrue(graphapi.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=permissions.CAN_READ, interval_init=ii, interval_end=ie))
        uid=uuid.uuid4()
        self.assertFalse(authorization.authorize_get_snapshot_config(uid=uid, nid=nid))

