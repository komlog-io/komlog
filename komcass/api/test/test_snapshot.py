import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.api import snapshot as snapshotapi
from komcass.model.orm import snapshot as ormsnapshot


class KomcassApiSnapshotTest(unittest.TestCase):
    ''' komlog.komcass.api.snapshot tests '''

    def test_get_snapshot_existing_nid(self):
        ''' get_snapshot should succeed if we pass an existing wid '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_existing_nid'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshotds=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshotds))
        snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(snapshotds.nid,snapshot.nid)
        self.assertEqual(snapshotds.uid,snapshot.uid)
        self.assertEqual(snapshotds.type,snapshot.type)

    def test_get_snapshot_non_existing_nid(self):
        ''' get_snapshot should return None if we pass a non existing wid '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))

    def test_get_snapshots_existing_uid(self):
        ''' get_snapshots should succeed if we pass an existing uid '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_existing_uid_1'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshotds=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshotds))
        snapshots=snapshotapi.get_snapshots(uid=uid)
        self.assertEqual(len(snapshots),1)
        snapshot=snapshots[0]
        self.assertEqual(snapshotds.nid,snapshot.nid)
        self.assertEqual(snapshotds.uid,snapshot.uid)
        self.assertEqual(snapshotds.type,snapshot.type)

    def test_get_snapshots_non_existing_uid(self):
        ''' get_snapshots should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        snapshots=snapshotapi.get_snapshots(uid=uid)
        self.assertTrue(isinstance(snapshots,list))
        self.assertEqual(len(snapshots),0)

    def test_get_snapshots_nids_existing_uid(self):
        ''' get_snapshots_nids should succeed if we pass an existing uid '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_existing_uid_1'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshotds=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshotds))
        nids=snapshotapi.get_snapshots_nids(uid=uid)
        self.assertEqual(len(nids),1)
        nid=nids[0]
        self.assertEqual(snapshotds.nid,nid)

    def test_get_snapshots_nids_non_existing_uid(self):
        ''' get_snapshots should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        nids=snapshotapi.get_snapshots_nids(uid=uid)
        self.assertTrue(isinstance(nids,list))
        self.assertEqual(len(nids),0)

    def test_get_number_of_snapshots_by_uid_no_snapshots(self):
        ''' get_number_of_snapshots_by_uid should return the number of snapshots belonging to a uid '''
        uid=uuid.uuid4()
        num=snapshotapi.get_number_of_snapshots_by_uid(uid)
        self.assertEqual(num, 0)

    def test_get_snapshots_ds_nids_existing_nids(self):
        ''' get_snapshots_ds_nids should return a list with the snapshots nids '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshots_ds_nids_existing_nids'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        nids=snapshotapi.get_snapshots_ds_nids(wid=wid)
        self.assertEqual(nids,[nid])

    def test_get_snapshots_dp_nids_existing_nids(self):
        ''' get_snapshots_dp_nids should return a list with the snapshots nids '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshots_dp_nids_existing_nids'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        nids=snapshotapi.get_snapshots_dp_nids(wid=wid)
        self.assertEqual(nids,[nid])

    def test_get_snapshots_histogram_nids_existing_nids(self):
        ''' get_snapshots_histogram_nids should return a list with the snapshots nids '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshots_histogram_nids_existing_nids'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AABBDD',uuid.uuid4():'#BBDDCC'}
        snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        nids=snapshotapi.get_snapshots_histogram_nids(wid=wid)
        self.assertEqual(nids,[nid])

    def test_get_snapshots_linegraph_nids_existing_nids(self):
        ''' get_snapshots_linegraph_nids should return a list with the snapshots nids '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshots_linegraph_nids_existing_nids'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AABBDD',uuid.uuid4():'#BBDDCC'}
        snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        nids=snapshotapi.get_snapshots_linegraph_nids(wid=wid)
        self.assertEqual(nids,[nid])

    def test_get_snapshots_table_nids_existing_nids(self):
        ''' get_snapshots_table_nids should return a list with the snapshots nids '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshots_table_nids_existing_nids'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AABBDD',uuid.uuid4():'#BBDDCC'}
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        nids=snapshotapi.get_snapshots_table_nids(wid=wid)
        self.assertEqual(nids,[nid])

    def test_get_snapshots_multidp_nids_existing_nids(self):
        ''' get_snapshots_multidp_nids should return a list with the snapshots nids '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshots_table_nids_existing_nids'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        active_visualization=0
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, active_visualization=active_visualization, shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        nids=snapshotapi.get_snapshots_multidp_nids(wid=wid)
        self.assertEqual(nids,[nid])

    def test_delete_snapshot_non_existing_nid(self):
        ''' delete_snapshot should return True even if nid does not exist '''
        nid=uuid.uuid4()
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))

    def test_delete_snapshot_existing_nid_snapshot_ds(self):
        ''' delete_snapshot should return True and delete the snapshot ds '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_delete_snapshot_existing_nid_snapshot_ds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_ds(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.did,snapshot.did)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot_ds(nid=nid))

    def test_delete_snapshot_existing_nid_snapshot_dp(self):
        ''' delete_snapshot should return True and delete the snapshot dp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_delete_snapshot_existing_nid_snapshot_dp'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_dp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.pid,snapshot.pid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot_dp(nid=nid))

    def test_delete_snapshot_existing_nid_snapshot_histogram(self):
        ''' delete_snapshot should return True and delete the snapshot histogram '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_delete_snapshot_existing_nid_snapshot_histogram'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_histogram(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot_histogram(nid=nid))

    def test_delete_snapshot_existing_nid_snapshot_linegraph(self):
        ''' delete_snapshot should return True and delete the snapshot linegraph '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_delete_snapshot_existing_nid_snapshot_linegraph'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_linegraph(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot_linegraph(nid=nid))

    def test_delete_snapshot_existing_nid_snapshot_table(self):
        ''' delete_snapshot should return True and delete the snapshot table '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_delete_snapshot_existing_nid_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_table(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot_table(nid=nid))

    def test_delete_snapshot_existing_nid_snapshot_multidp(self):
        ''' delete_snapshot should return True and delete the snapshot multidp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_delete_snapshot_existing_nid_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        active_visualization=0
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, active_visualization=active_visualization, datapoints=datapoints,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_multidp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.active_visualization,snapshot.active_visualization)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertTrue(snapshotapi.delete_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot(nid=nid))
        self.assertIsNone(snapshotapi.get_snapshot_multidp(nid=nid))

    def test_new_snapshot_success_snapshot_ds(self):
        ''' new_snapshot should return True and create the snapshot ds '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_ds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_ds(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.did,snapshot.did)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_new_snapshot_success_snapshot_dp(self):
        ''' new_snapshot should return True and create the snapshot dp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_ds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_dp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.pid,snapshot.pid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_new_snapshot_success_snapshot_histogram(self):
        ''' new_snapshot should return True and create the snapshot histogram'''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_histogram'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#BBDDAA'}
        snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_histogram(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)

    def test_new_snapshot_success_snapshot_linegraph(self):
        ''' new_snapshot should return True and create the snapshot linegraph '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_linegraph'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#BBDDAA'}
        snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_linegraph(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)

    def test_new_snapshot_success_snapshot_table(self):
        ''' new_snapshot should return True and create the snapshot table'''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#BBDDAA'}
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_table(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)

    def test_new_snapshot_success_snapshot_multidp(self):
        ''' new_snapshot should return True and create the snapshot multidp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        active_visualization=0
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, active_visualization=active_visualization, datapoints=datapoints, shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_multidp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.active_visualization,snapshot.active_visualization)

    def test_new_snapshot_failure_already_existing_snapshot(self):
        ''' new_snapshot should fail if snapshot already exist '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_success_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB',uuid.uuid4():'#BBDDAA'}
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        self.assertFalse(snapshotapi.new_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_table(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertFalse(snapshotapi.new_snapshot(snapshot=snapshot))

    def test_insert_snapshot_success_snapshot_ds(self):
        ''' insert_snapshot should return True and insert the snapshot ds '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_insert_snapshot_success_snapshot_ds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_ds(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.did,snapshot.did)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_insert_snapshot_success_snapshot_dp(self):
        ''' insert_snapshot should return True and insert the snapshot dp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_insert_snapshot_success_snapshot_dp'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_dp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.pid,snapshot.pid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_insert_snapshot_success_snapshot_histogram(self):
        ''' insert_snapshot should return True and insert the snapshot histogram '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_insert_snapshot_success_snapshot_histogram'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB', uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_histogram(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_insert_snapshot_success_snapshot_linegraph(self):
        ''' insert_snapshot should return True and insert the snapshot linegraph'''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_insert_snapshot_success_snapshot_linegraph'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB', uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_linegraph(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_insert_snapshot_success_snapshot_table(self):
        ''' insert_snapshot should return True and insert the snapshot table '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_insert_snapshot_success_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB', uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_table(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_insert_snapshot_success_snapshot_multidp(self):
        ''' insert_snapshot should return True and insert the snapshot multidp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_insert_snapshot_success_snapshot_table'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        active_visualization=0
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, active_visualization=active_visualization, datapoints=datapoints,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_multidp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.active_visualization,snapshot.active_visualization)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_insert_snapshot_failure_non_snapshot_instance(self):
        ''' insert_snapshot should return False if snapshot argument is not a Snapshot object '''
        snapshots=[None, 'a',{'a':'dict'},{'a','set'},['a','list'],('a','tuple'),uuid.uuid4(), uuid.uuid1(), 234234, 234234.234234]
        for snapshot in snapshots:
            self.assertFalse(snapshotapi.insert_snapshot(snapshot=snapshot))

    def test_get_snapshot_ds_non_existent_nid(self):
        ''' get_snapshot_ds should return None if nid is not found '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot_ds(nid=nid))

    def test_get_snapshot_dp_non_existent_nid(self):
        ''' get_snapshot_dp should return None if nid is not found '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot_dp(nid=nid))

    def test_get_snapshot_histogram_non_existent_nid(self):
        ''' get_snapshot_histogram should return None if nid is not found '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot_histogram(nid=nid))

    def test_get_snapshot_linegraph_non_existent_nid(self):
        ''' get_snapshot_linegraph should return None if nid is not found '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot_linegraph(nid=nid))

    def test_get_snapshot_table_non_existent_nid(self):
        ''' get_snapshot_table should return None if nid is not found '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot_table(nid=nid))

    def test_get_snapshot_multidp_non_existent_nid(self):
        ''' get_snapshot_multidp should return None if nid is not found '''
        nid=uuid.uuid4()
        self.assertIsNone(snapshotapi.get_snapshot_multidp(nid=nid))

    def test_get_snapshot_ds_success(self):
        ''' get_snapshot_ds should return snapshot ds if its nid is passed '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_ds_success_snapshot_ds_nid'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_ds(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.did,snapshot.did)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_get_snapshot_dp_success(self):
        ''' get_snapshot_dp should return snapshot ds if its nid is passed '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_ds_success_snapshot_ds_nid'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_dp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.pid,snapshot.pid)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_get_snapshot_histogram_success(self):
        ''' get_snapshot_histogram should return the snapshot histogram '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_histogram_success'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB', uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotHistogram(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_histogram(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_get_snapshot_linegraph_success(self):
        ''' get_snapshot_linegraph should return the snapshot linegraph'''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_linegraph_success'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB', uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotLinegraph(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_linegraph(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_get_snapshot_table_success(self):
        ''' get_snapshot_table should return the snapshot table '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_table_success'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        colors={uuid.uuid4():'#AADDBB', uuid.uuid4():'#AABBDD'}
        snapshot=ormsnapshot.SnapshotTable(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, colors=colors,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_table(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.colors,snapshot.colors)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

    def test_get_snapshot_multidp_success(self):
        ''' get_snapshot_multidp should return the snapshot multidp '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        nid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_get_snapshot_table_success'
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(), uuid.uuid4()}
        active_visualization=0
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date,active_visualization=active_visualization, datapoints=datapoints,shared_with_uids={},shared_with_cids={})
        self.assertTrue(snapshotapi.insert_snapshot(snapshot=snapshot))
        resp_snapshot=snapshotapi.get_snapshot(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.type,snapshot.type)
        resp_snapshot=snapshotapi.get_snapshot_multidp(nid=nid)
        self.assertEqual(resp_snapshot.nid,snapshot.nid)
        self.assertEqual(resp_snapshot.uid,snapshot.uid)
        self.assertEqual(resp_snapshot.wid,snapshot.wid)
        self.assertEqual(resp_snapshot.datapoints,snapshot.datapoints)
        self.assertEqual(resp_snapshot.active_visualization,snapshot.active_visualization)
        self.assertEqual(resp_snapshot.interval_init,snapshot.interval_init)
        self.assertEqual(resp_snapshot.interval_end,snapshot.interval_end)
        self.assertEqual(resp_snapshot.creation_date,snapshot.creation_date)
        self.assertEqual(resp_snapshot.widgetname,snapshot.widgetname)

