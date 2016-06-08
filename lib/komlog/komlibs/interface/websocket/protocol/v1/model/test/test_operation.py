import unittest
import time
import uuid
import json
from komlog.komfig import logging
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import operation
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Operations


class InterfaceWebSocketProtocolV1ModelOperationTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.model.operation tests '''

    def test_new_WSIFaceOperation_failure_non_allowed(self):
        ''' the instantiation of a WSIfaceOperation object is disallowed '''
        with self.assertRaises(exceptions.OperationValidationException) as cm:
            operation.WSIFaceOperation(uid=1)
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_WSIO_IC)

    def test_modify_oid_in_WSIFaceOperation_failure_non_allowed(self):
        ''' the modification of the params property in a WSIfaceOperation object is disallowed '''
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        did=uuid.uuid4()
        op=operation.NewDatasourceOperation(uid, aid=aid, did=did)
        self.assertTrue(isinstance(op, operation.NewDatasourceOperation))
        self.assertEqual(op.oid, Operations.NEW_DATASOURCE)
        self.assertEqual(op.uid, uid)
        self.assertEqual(op.aid, aid)
        self.assertEqual(op.did, did)
        with self.assertRaises(exceptions.OperationValidationException) as cm:
            op.oid=4
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_WSIO_OIDAI)

    def test_new_NewDatasourceOperation_failure_invalid_uid_type(self):
        ''' the creation of a NewDatasourceOperation object should fail if uid is not a UUID4 '''
        uids=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid1()]
        aid=uuid.uuid4()
        did=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.OperationValidationException) as cm:
                operation.NewDatasourceOperation(uid=uid, aid=aid, did=did)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_NDSO_IUT)

    def test_new_NewDatasourceOperation_failure_invalid_aid_type(self):
        ''' the creation of a NewDatasourceOperation object should fail if aid is not a UUID4 '''
        aids=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid1()]
        uid=uuid.uuid4()
        did=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.OperationValidationException) as cm:
                operation.NewDatasourceOperation(uid=uid, aid=aid, did=did)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_NDSO_IAT)

    def test_new_NewDatasourceOperation_failure_invalid_did_type(self):
        ''' the creation of a NewDatasourceOperation object should fail if did is not a UUID4 '''
        dids=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid1()]
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        for did in dids:
            with self.assertRaises(exceptions.OperationValidationException) as cm:
                operation.NewDatasourceOperation(uid=uid, aid=aid, did=did)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_NDSO_IDT)

    def test_new_NewDatasourceOperation_success_cannot_modify_params_property(self):
        ''' the creation of a NewDatasourceOperation object should succeed and params property cannot be modified directly'''
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        did=uuid.uuid4()
        op=operation.NewDatasourceOperation(uid, aid=aid, did=did)
        self.assertTrue(isinstance(op, operation.NewDatasourceOperation))
        self.assertEqual(op.oid, Operations.NEW_DATASOURCE)
        self.assertEqual(op.uid, uid)
        self.assertEqual(op.aid, aid)
        self.assertEqual(op.did, did)
        self.assertEqual(op.params, {'uid':uid, 'aid':aid, 'did':did})
        with self.assertRaises(exceptions.OperationValidationException) as cm:
            op.params={'uid':uuid.uuid4(),'what':'yes','number':3}
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_WSIO_PMNA)

    def test_new_NewDatasourceOperation_success(self):
        ''' the creation of a NewDatasourceOperation object should succeed '''
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        did=uuid.uuid4()
        op=operation.NewDatasourceOperation(uid, aid=aid, did=did)
        self.assertTrue(isinstance(op, operation.NewDatasourceOperation))
        self.assertEqual(op.oid, Operations.NEW_DATASOURCE)
        self.assertEqual(op.uid, uid)
        self.assertEqual(op.aid, aid)
        self.assertEqual(op.did, did)
        self.assertEqual(op.params, {'uid':uid, 'aid':aid, 'did':did})

    def test_new_NewUserDatapointOperation_failure_invalid_uid_type(self):
        ''' the creation of a NewUserDatapointOperation object should fail if uid is not a UUID4 '''
        uids=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid1()]
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.OperationValidationException) as cm:
                operation.NewUserDatapointOperation(uid=uid, aid=aid, pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_NUDPO_IUT)

    def test_new_NewUserDatapointOperation_failure_invalid_aid_type(self):
        ''' the creation of a NewUserDatapointOperation object should fail if aid is not a UUID4 '''
        aids=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid1()]
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.OperationValidationException) as cm:
                operation.NewUserDatapointOperation(uid=uid, aid=aid, pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_NUDPO_IAT)

    def test_new_NewUserDatapointOperation_failure_invalid_pid_type(self):
        ''' the creation of a NewUserDatapointOperation object should fail if pid is not a UUID4 '''
        pids=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],uuid.uuid1()]
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        for pid in pids:
            with self.assertRaises(exceptions.OperationValidationException) as cm:
                operation.NewUserDatapointOperation(uid=uid, aid=aid, pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_NUDPO_IPT)

    def test_new_NewUserDatapointOperation_success_cannot_modify_params_property(self):
        ''' the creation of a NewUserDatapointOperation object should succeed and params property cannot be modified directly'''
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        op=operation.NewUserDatapointOperation(uid, aid=aid, pid=pid)
        self.assertTrue(isinstance(op, operation.NewUserDatapointOperation))
        self.assertEqual(op.oid, Operations.NEW_USER_DATAPOINT)
        self.assertEqual(op.uid, uid)
        self.assertEqual(op.aid, aid)
        self.assertEqual(op.pid, pid)
        self.assertEqual(op.params, {'uid':uid, 'aid':aid, 'pid':pid})
        with self.assertRaises(exceptions.OperationValidationException) as cm:
            op.params={'uid':uuid.uuid4(),'what':'yes','number':3}
        self.assertEqual(cm.exception.error, Errors.E_IWSPV1MO_WSIO_PMNA)

    def test_new_NewUserDatapointOperation_success(self):
        ''' the creation of a NewUserDatapointOperation object should succeed '''
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        op=operation.NewUserDatapointOperation(uid, aid=aid, pid=pid)
        self.assertTrue(isinstance(op, operation.NewUserDatapointOperation))
        self.assertEqual(op.oid, Operations.NEW_USER_DATAPOINT)
        self.assertEqual(op.uid, uid)
        self.assertEqual(op.aid, aid)
        self.assertEqual(op.pid, pid)
        self.assertEqual(op.params, {'uid':uid, 'aid':aid, 'pid':pid})

