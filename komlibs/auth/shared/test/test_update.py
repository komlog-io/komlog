import unittest
import uuid
from komcass.api import snapshot as cassapisnapshot
from komcass.model.orm import snapshot as ormsnapshot
from komlibs.auth import operations, permissions
from komlibs.auth.shared import update, authorization
from komlibs.general.time import timeuuid

class AuthSharedUpdateTest(unittest.TestCase):
    ''' komlog.auth.shared.update tests '''
    
    def test_get_update_funcs_success(self):
        ''' test_update_funcs should return a list of functions '''
        operation=operations.NEW_SNAPSHOT
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, list))
        self.assertEqual(update_funcs,['new_snapshot'])

    def test_get_update_funcs_success_empty_list(self):
        '''test_update_funcs should return an empty list of functions if operation does not exist'''
        operation='234234234'
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, list))
        self.assertEqual(update_funcs, [])

    def test_new_snapshot_no_uid(self):
        ''' new_snapshot should fail if no nid is passed'''
        params={}
        self.assertFalse(update.new_snapshot(params))

    def test_new_snapshot_success_snapshot_ds(self):
        ''' new_snapshot should succeed if graph relations can be set correctly '''
        uid=uuid.uuid4()
        shared_with_uid1=uuid.uuid4()
        shared_with_uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        did=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        creation_date=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_ds'
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={shared_with_uid1,shared_with_uid2},shared_with_cids=None)
        self.assertTrue(cassapisnapshot.new_snapshot(snapshot=snapshot))
        params={'nid':nid}
        self.assertTrue(update.new_snapshot(params))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid1, nid=nid))
        self.assertTrue(authorization.authorize_get_datasource_config(uid=shared_with_uid1, did=did))
        self.assertTrue(authorization.authorize_get_datasource_data(uid=shared_with_uid1, did=did,ii=interval_init, ie=interval_end))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid2, nid=nid))
        self.assertTrue(authorization.authorize_get_datasource_config(uid=shared_with_uid2, did=did))
        self.assertTrue(authorization.authorize_get_datasource_data(uid=shared_with_uid2, did=did,ii=interval_init, ie=interval_end))

    def test_new_snapshot_success_snapshot_dp(self):
        ''' new_snapshot should succeed if graph relations can be set correctly '''
        uid=uuid.uuid4()
        shared_with_uid1=uuid.uuid4()
        shared_with_uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        creation_date=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_dp'
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid,shared_with_uids={shared_with_uid1,shared_with_uid2},shared_with_cids=None)
        self.assertTrue(cassapisnapshot.new_snapshot(snapshot=snapshot))
        params={'nid':nid}
        self.assertTrue(update.new_snapshot(params))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid1, nid=nid))
        self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid1, pid=pid))
        self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid1, pid=pid,ii=interval_init, ie=interval_end))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid2, nid=nid))
        self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid2, pid=pid))
        self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid2, pid=pid,ii=interval_init, ie=interval_end))

    def test_new_snapshot_success_snapshot_histogram(self):
        ''' new_snapshot should succeed if graph relations can be set correctly '''
        uid=uuid.uuid4()
        shared_with_uid1=uuid.uuid4()
        shared_with_uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        pids=[uuid.uuid4() for i in range(0,5)]
        color='#FFEEDD'
        colors={}
        for pid in pids:
            colors[pid]=color
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        creation_date=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_histogram'
        snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=pids,colors=colors,shared_with_uids={shared_with_uid1,shared_with_uid2},shared_with_cids=None)
        self.assertTrue(cassapisnapshot.new_snapshot(snapshot=snapshot))
        params={'nid':nid}
        self.assertTrue(update.new_snapshot(params))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid1, nid=nid))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid2, nid=nid))
        for pid in pids:
            self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid1, pid=pid))
            self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid1, pid=pid,ii=interval_init, ie=interval_end))
            self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid2, pid=pid))
            self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid2, pid=pid,ii=interval_init, ie=interval_end))

    def test_new_snapshot_success_snapshot_linegraph(self):
        ''' new_snapshot should succeed if graph relations can be set correctly '''
        uid=uuid.uuid4()
        shared_with_uid1=uuid.uuid4()
        shared_with_uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        pids=[uuid.uuid4() for i in range(0,5)]
        color='#FFEEDD'
        colors={}
        for pid in pids:
            colors[pid]=color
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        creation_date=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_linegraph'
        snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=pids,colors=colors,shared_with_uids={shared_with_uid1,shared_with_uid2},shared_with_cids=None)
        self.assertTrue(cassapisnapshot.new_snapshot(snapshot=snapshot))
        params={'nid':nid}
        self.assertTrue(update.new_snapshot(params))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid1, nid=nid))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid2, nid=nid))
        for pid in pids:
            self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid1, pid=pid))
            self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid1, pid=pid,ii=interval_init, ie=interval_end))
            self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid2, pid=pid))
            self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid2, pid=pid,ii=interval_init, ie=interval_end))

    def test_new_snapshot_success_snapshot_table(self):
        ''' new_snapshot should succeed if graph relations can be set correctly '''
        uid=uuid.uuid4()
        shared_with_uid1=uuid.uuid4()
        shared_with_uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        pids=[uuid.uuid4() for i in range(0,5)]
        color='#FFEEDD'
        colors={}
        for pid in pids:
            colors[pid]=color
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        creation_date=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_table'
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=pids,colors=colors,shared_with_uids={shared_with_uid1,shared_with_uid2},shared_with_cids=None)
        self.assertTrue(cassapisnapshot.new_snapshot(snapshot=snapshot))
        params={'nid':nid}
        self.assertTrue(update.new_snapshot(params))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid1, nid=nid))
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=shared_with_uid2, nid=nid))
        for pid in pids:
            self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid1, pid=pid))
            self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid1, pid=pid,ii=interval_init, ie=interval_end))
            self.assertTrue(authorization.authorize_get_datapoint_config(uid=shared_with_uid2, pid=pid))
            self.assertTrue(authorization.authorize_get_datapoint_data(uid=shared_with_uid2, pid=pid,ii=interval_init, ie=interval_end))

