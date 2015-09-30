import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.model.orm import ticket as ormticket
from komcass.model.orm import snapshot as ormsnapshot
from komcass.api import snapshot as snapshotapi
from komcass.api import ticket as ticketapi
from komlibs.auth.tickets import provision
from komlibs.auth.tickets.types import share
from komlibs.auth import exceptions, errors, permissions
from komfig import logger


class AuthTicketsProvisionTest(unittest.TestCase):
    ''' komlog.komlibs.auth.tickets.provision tests '''

    def setUp(self):
        pass

    def test_new_snapshot_ticket_failure_invalid_uid(self):
        ''' new_snapshot_ticket should fail if uid is invalid '''
        uids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        nid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                provision.new_snapshot_ticket(uid=uid, nid=nid)
            self.assertEqual(cm.exception.error, errors.E_ATP_NST_IUID)

    def test_new_snapshot_ticket_failure_invalid_nid(self):
        ''' new_snapshot_ticket should fail if nid is invalid '''
        nids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        for nid in nids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                provision.new_snapshot_ticket(uid=uid, nid=nid)
            self.assertEqual(cm.exception.error, errors.E_ATP_NST_INID)

    def test_new_snapshot_ticket_failure_invalid_expires(self):
        ''' new_snapshot_ticket should fail if expires is invalid '''
        expires=[ 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid4(), 'Usernames','user name']
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        for expire in expires:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                provision.new_snapshot_ticket(uid=uid, nid=nid, expires=expire)
            self.assertEqual(cm.exception.error, errors.E_ATP_NST_IEXP)

    def test_new_snapshot_ticket_failure_invalid_share_type(self):
        ''' new_snapshot_ticket should fail if expires is invalid '''
        share_types=[ 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid4(), 'Usernames','user name']
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        expires=timeuuid.uuid1()
        for share_type in share_types:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                provision.new_snapshot_ticket(uid=uid, nid=nid, expires=expires, share_type=share_type)
            self.assertEqual(cm.exception.error, errors.E_ATP_NST_ISHT)

    def test_new_snapshot_ticket_failure_non_existent_snapshot(self):
        ''' new_snapshot_ticket should fail if snapshot does not exist '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.TicketCreationException) as cm:
            provision.new_snapshot_ticket(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, errors.E_ATP_NST_SNF)

    def test_new_snapshot_ticket_success_SnapshotDs(self):
        ''' new_snapshot_ticket should succeed if snapshot is a SnapshotDs object '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        shared_with_cids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid, nid=nid)
        self.assertTrue(isinstance(tid['tid'],uuid.UUID))
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        self.assertEqual(ticket.tid, tid['tid'])
        self.assertEqual(ticket.uid, uid)
        self.assertEqual(ticket.expires, timeuuid.HIGHEST_TIME_UUID)
        self.assertEqual(ticket.allowed_uids, set(sorted(shared_with_uids)))
        self.assertEqual(ticket.allowed_cids, set(sorted(shared_with_cids)))
        self.assertEqual(ticket.resources, set(sorted([did,nid])))
        self.assertEqual(ticket.permissions, {did:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,nid:permissions.CAN_READ_CONFIG})
        self.assertEqual(ticket.interval_init, interval_init)
        self.assertEqual(ticket.interval_end, interval_end)

    def test_new_snapshot_ticket_success_SnapshotDp(self):
        ''' new_snapshot_ticket should succeed if snapshot is a SnapshotDp object '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotdp'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        shared_with_cids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid, nid=nid)
        self.assertTrue(isinstance(tid['tid'],uuid.UUID))
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        self.assertEqual(ticket.tid, tid['tid'])
        self.assertEqual(ticket.uid, uid)
        self.assertEqual(ticket.expires, timeuuid.HIGHEST_TIME_UUID)
        self.assertEqual(ticket.allowed_uids, set(sorted(shared_with_uids)))
        self.assertEqual(ticket.allowed_cids, set(sorted(shared_with_cids)))
        self.assertEqual(ticket.resources, set(sorted([pid,nid])))
        self.assertEqual(ticket.permissions, {pid:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,nid:permissions.CAN_READ_CONFIG})
        self.assertEqual(ticket.interval_init, interval_init)
        self.assertEqual(ticket.interval_end, interval_end)

    def test_new_snapshot_ticket_success_SnapshotMultidp(self):
        ''' new_snapshot_ticket should succeed if snapshot is a SnapshotMultidp object '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotmultidp'
        creation_date=timeuuid.uuid1()
        datapoints=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        shared_with_uids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        shared_with_cids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids, active_visualization=0)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid, nid=nid)
        self.assertTrue(isinstance(tid['tid'],uuid.UUID))
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        self.assertEqual(ticket.tid, tid['tid'])
        self.assertEqual(ticket.uid, uid)
        self.assertEqual(ticket.expires, timeuuid.HIGHEST_TIME_UUID)
        self.assertEqual(ticket.allowed_uids, set(sorted(shared_with_uids)))
        self.assertEqual(ticket.allowed_cids, set(sorted(shared_with_cids)))
        resources=set(datapoints)
        resources.add(nid)
        self.assertEqual(ticket.resources, set(sorted(resources)))
        self.assertEqual(ticket.permissions, {datapoints[0]:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,datapoints[1]:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,datapoints[2]:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,nid:permissions.CAN_READ_CONFIG})
        self.assertEqual(ticket.interval_init, interval_init)
        self.assertEqual(ticket.interval_end, interval_end)

    def test_new_snapshot_ticket_success_SnapshotDs_with_expires_and_share_and_read(self):
        ''' new_snapshot_ticket should succeed if snapshot is a SnapshotDs object '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        shared_with_cids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        expires=timeuuid.uuid1()
        tid=provision.new_snapshot_ticket(uid=uid, nid=nid, expires=expires, share_type=share.NEW_SNAPSHOT_SHARE_READ_AND_SHARE)
        self.assertTrue(isinstance(tid['tid'],uuid.UUID))
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        self.assertEqual(ticket.tid, tid['tid'])
        self.assertEqual(ticket.uid, uid)
        self.assertEqual(ticket.expires, expires)
        self.assertEqual(ticket.allowed_uids, set(sorted(shared_with_uids)))
        self.assertEqual(ticket.allowed_cids, set(sorted(shared_with_cids)))
        self.assertEqual(ticket.resources, set(sorted([did,nid])))
        self.assertEqual(ticket.permissions, {did:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,nid:permissions.CAN_READ_CONFIG|permissions.CAN_SNAPSHOT})
        self.assertEqual(ticket.interval_init, interval_init)
        self.assertEqual(ticket.interval_end, interval_end)

    def test_new_snapshot_ticket_success_SnapshotDp_expires_and_share_and_read(self):
        ''' new_snapshot_ticket should succeed if snapshot is a SnapshotDp object '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotdp'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        shared_with_cids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        expires=timeuuid.uuid1()
        tid=provision.new_snapshot_ticket(uid=uid, nid=nid, expires=expires, share_type=share.NEW_SNAPSHOT_SHARE_READ_AND_SHARE)
        self.assertTrue(isinstance(tid['tid'],uuid.UUID))
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        self.assertEqual(ticket.tid, tid['tid'])
        self.assertEqual(ticket.uid, uid)
        self.assertEqual(ticket.expires, expires)
        self.assertEqual(ticket.allowed_uids, set(sorted(shared_with_uids)))
        self.assertEqual(ticket.allowed_cids, set(sorted(shared_with_cids)))
        self.assertEqual(ticket.resources, set(sorted([pid,nid])))
        self.assertEqual(ticket.permissions, {pid:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,nid:permissions.CAN_READ_CONFIG|permissions.CAN_SNAPSHOT})
        self.assertEqual(ticket.interval_init, interval_init)
        self.assertEqual(ticket.interval_end, interval_end)

    def test_new_snapshot_ticket_success_SnapshotMultidp_expires_and_share_and_read(self):
        ''' new_snapshot_ticket should succeed if snapshot is a SnapshotMultidp object '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotmultidp'
        creation_date=timeuuid.uuid1()
        datapoints=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        shared_with_uids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        shared_with_cids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        snapshot=ormsnapshot.SnapshotMultidp(nid=nid, uid=uid, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, datapoints=datapoints, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids, active_visualization=0)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        expires=timeuuid.uuid1()
        tid=provision.new_snapshot_ticket(uid=uid, nid=nid, expires=expires, share_type=share.NEW_SNAPSHOT_SHARE_READ_AND_SHARE)
        self.assertTrue(isinstance(tid['tid'],uuid.UUID))
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        self.assertEqual(ticket.tid, tid['tid'])
        self.assertEqual(ticket.uid, uid)
        self.assertEqual(ticket.expires, expires)
        self.assertEqual(ticket.allowed_uids, set(sorted(shared_with_uids)))
        self.assertEqual(ticket.allowed_cids, set(sorted(shared_with_cids)))
        resources=set(datapoints)
        resources.add(nid)
        self.assertEqual(ticket.resources, set(sorted(resources)))
        self.assertEqual(ticket.permissions, {datapoints[0]:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,datapoints[1]:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,datapoints[2]:permissions.CAN_READ_DATA|permissions.CAN_READ_CONFIG,nid:permissions.CAN_READ_CONFIG|permissions.CAN_SNAPSHOT})
        self.assertEqual(ticket.interval_init, interval_init)
        self.assertEqual(ticket.interval_end, interval_end)

