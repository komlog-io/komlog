import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.model.orm import ticket as ormticket
from komcass.model.orm import snapshot as ormsnapshot
from komcass.model.orm import circle as ormcircle
from komcass.api import snapshot as snapshotapi
from komcass.api import ticket as ticketapi
from komcass.api import circle as circleapi
from komlibs.auth.tickets import provision
from komlibs.auth.tickets import authorization
from komlibs.auth.tickets.types import share
from komlibs.auth import exceptions, errors, permissions
from komfig import logger


class AuthTicketsAuthorizationTest(unittest.TestCase):
    ''' komlog.komlibs.auth.tickets.authorization tests '''

    def setUp(self):
        pass

    def test_authorize_get_datasource_data_failure_invalid_uid(self):
        ''' authorize_get_datasource_data should fail if uid is invalid '''
        uids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        tid=uuid.uuid4()
        did=uuid.uuid4()
        ie=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datasource_data(uid=uid, tid=tid, did=did, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IUID)

    def test_authorize_get_datasource_data_failure_invalid_tid(self):
        ''' authorize_get_datasource_data should fail if tid is invalid '''
        tids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        did=uuid.uuid4()
        ie=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        for tid in tids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datasource_data(uid=uid, tid=tid, did=did, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_ITID)

    def test_authorize_get_datasource_data_failure_invalid_did(self):
        ''' authorize_get_datasource_data should fail if did is invalid '''
        dids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        ie=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datasource_data(uid=uid, tid=tid, did=did, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IDID)

    def test_authorize_get_datasource_data_failure_invalid_ii(self):
        ''' authorize_get_datasource_data should fail if ii is invalid '''
        iis=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1().hex, 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        did=uuid.uuid4()
        ie=timeuuid.uuid1()
        for ii in iis:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datasource_data(uid=uid, tid=tid, did=did, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_III)

    def test_authorize_get_datasource_data_failure_invalid_ie(self):
        ''' authorize_get_datasource_data should fail if ie is invalid '''
        ies=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1().hex, 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.uuid1()
        for ie in ies:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datasource_data(uid=uid, tid=tid, did=did, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IIE)

    def test_authorize_get_datasource_data_failure_non_existent_ticket(self):
        ''' authorize_get_datasource_data should fail if ticket does not exist '''
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        did=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid, tid=tid, did=did, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_TNF)

    def test_authorize_get_datasource_data_failure_expired_ticket(self):
        ''' authorize_get_datasource_data should fail if ticket has expired '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        expires=timeuuid.uuid1(seconds=1)
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, expires=expires, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_EXPT)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_TNF)

    def test_authorize_get_datasource_data_failure_not_shared_with_uid(self):
        ''' authorize_get_datasource_data should fail if uid is not allowed in ticket '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids=set()
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids={uuid.uuid4()})
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_UNA)

    def test_authorize_get_datasource_data_failure_shared_with_uid_but_invalid_did(self):
        ''' authorize_get_datasource_data should fail if uid is listed in ticket allowed uids, but did is different '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        did2=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did2, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_DNA)

    def test_authorize_get_datasource_data_failure_shared_with_cid_but_invalid_did(self):
        ''' authorize_get_datasource_data should fail if uid belongs to a listed ticket allowed cids, but did is different '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        cid=uuid.uuid4()
        circle=ormcircle.Circle(cid=cid, uid=uid1, circlename='circlename', type='u',creation_date=timeuuid.uuid1(),members={uid2})
        self.assertTrue(circleapi.new_circle(circle))
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids=set()
        shared_with_cids={cid}
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        did2=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did2, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_DNA)

    def test_authorize_get_datasource_data_failure_interval_init_out_of_bounds(self):
        ''' authorize_get_datasource_data should fail if interval_init is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_init=timeuuid.uuid1(seconds=999)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=new_interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IINT)

    def test_authorize_get_datasource_data_failure_interval_init_out_of_bounds_2(self):
        ''' authorize_get_datasource_data should fail if interval_init is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_init=timeuuid.uuid1(seconds=2001)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=new_interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IINT)

    def test_authorize_get_datasource_data_failure_interval_end_out_of_bounds(self):
        ''' authorize_get_datasource_data should fail if interval_end is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_end=timeuuid.uuid1(seconds=999)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=new_interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IINT)

    def test_authorize_get_datasource_data_failure_interval_end_out_of_bounds_2(self):
        ''' authorize_get_datasource_data should fail if interval_end is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_end=timeuuid.uuid1(seconds=2001)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=new_interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_IINT)

    def test_authorize_get_datasource_data_failure_insufficient_privileges(self):
        ''' authorize_get_datasource_data should fail if user has insufficient privileges to acomplish requested operation '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        ticket.permissions=dict(ticket.permissions)
        ticket.permissions[did]=0
        self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDSD_INSP)

    def test_authorize_get_datasource_data_success(self):
        ''' authorize_get_datasource_data should succeed '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=did, datasourcename=did.hex)
        datapoints_config=[]
        snapshot=ormsnapshot.SnapshotDs(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, did=did, datasource_config=datasource_config, datapoints_config=datapoints_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        self.assertTrue(authorization.authorize_get_datasource_data(uid=uid2, tid=tid['tid'], did=did, ii=interval_init, ie=interval_end))

    def test_authorize_get_datapoint_data_failure_invalid_uid(self):
        ''' authorize_get_datapoint_data should fail if uid is invalid '''
        uids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        tid=uuid.uuid4()
        pid=uuid.uuid4()
        ie=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datapoint_data(uid=uid, tid=tid, pid=pid, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IUID)

    def test_authorize_get_datapoint_data_failure_invalid_tid(self):
        ''' authorize_get_datapoint_data should fail if tid is invalid '''
        tids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        ie=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        for tid in tids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datapoint_data(uid=uid, tid=tid, pid=pid, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_ITID)

    def test_authorize_get_datapoint_data_failure_invalid_pid(self):
        ''' authorize_get_datapoint_data should fail if pid is invalid '''
        pids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        ie=timeuuid.uuid1()
        ii=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datapoint_data(uid=uid, tid=tid, pid=pid, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IPID)

    def test_authorize_get_datapoint_data_failure_invalid_ii(self):
        ''' authorize_get_datapoint_data should fail if ii is invalid '''
        iis=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1().hex, 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        pid=uuid.uuid4()
        ie=timeuuid.uuid1()
        for ii in iis:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datapoint_data(uid=uid, tid=tid, pid=pid, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_III)

    def test_authorize_get_datapoint_data_failure_invalid_ie(self):
        ''' authorize_get_datapoint_data should fail if ie is invalid '''
        ies=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4(), uuid.uuid1().hex, 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        pid=uuid.uuid4()
        ii=timeuuid.uuid1()
        for ie in ies:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_datapoint_data(uid=uid, tid=tid, pid=pid, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IIE)

    def test_authorize_get_datapoint_data_failure_non_existent_ticket(self):
        ''' authorize_get_datapoint_data should fail if ticket does not exist '''
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        pid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid, tid=tid, pid=pid, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_TNF)

    def test_authorize_get_datapoint_data_failure_expired_ticket(self):
        ''' authorize_get_datapoint_data should fail if ticket has expired '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        expires=timeuuid.uuid1(seconds=1)
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, expires=expires, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_EXPT)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_TNF)

    def test_authorize_get_datapoint_data_failure_not_shared_with_uid(self):
        ''' authorize_get_datapoint_data should fail if uid is not allowed in ticket '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids=set()
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids={uuid.uuid4()}, allowed_cids=shared_with_cids)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_UNA)

    def test_authorize_get_datapoint_data_failure_shared_with_uid_but_invalid_pid(self):
        ''' authorize_get_datapoint_data should fail if uid is listed in ticket allowed uids, but pid is different '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        pid2=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid2, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_DNA)

    def test_authorize_get_datapoint_data_failure_shared_with_cid_but_invalid_pid(self):
        ''' authorize_get_datapoint_data should fail if uid belongs to a listed ticket allowed cids, but pid is different '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        cid=uuid.uuid4()
        circle=ormcircle.Circle(cid=cid, uid=uid1, circlename='circlename', type='u',creation_date=timeuuid.uuid1(),members={uid2})
        self.assertTrue(circleapi.new_circle(circle))
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids=set()
        shared_with_cids={cid}
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        pid2=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid2, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_DNA)

    def test_authorize_get_datapoint_data_failure_interval_init_out_of_bounds(self):
        ''' authorize_get_datapoint_data should fail if interval_init is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_init=timeuuid.uuid1(seconds=999)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=new_interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IINT)

    def test_authorize_get_datapoint_data_failure_interval_init_out_of_bounds_2(self):
        ''' authorize_get_datapoint_data should fail if interval_init is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_init=timeuuid.uuid1(seconds=2001)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=new_interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IINT)

    def test_authorize_get_datapoint_data_failure_interval_end_out_of_bounds(self):
        ''' authorize_get_datapoint_data should fail if interval_end is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_end=timeuuid.uuid1(seconds=999)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=new_interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IINT)

    def test_authorize_get_datapoint_data_failure_interval_end_out_of_bounds_2(self):
        ''' authorize_get_datapoint_data should fail if interval_end is out of allowed interval '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        new_interval_end=timeuuid.uuid1(seconds=2001)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=new_interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_IINT)

    def test_authorize_get_datapoint_data_failure_insufficient_privileges(self):
        ''' authorize_get_datapoint_data should fail if user has insufficient privileges to acomplish requested operation '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        ticket.permissions=dict(ticket.permissions)
        ticket.permissions[pid]=0
        self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=interval_end)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGDPD_INSP)

    def test_authorize_get_datapoint_data_success(self):
        ''' authorize_get_datapoint_data should succeed '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        self.assertTrue(authorization.authorize_get_datapoint_data(uid=uid2, tid=tid['tid'], pid=pid, ii=interval_init, ie=interval_end))

    def test_authorize_get_snapshot_config_failure_invalid_uid(self):
        ''' authorize_get_snapshot_config should fail if uid is invalid '''
        uids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        tid=uuid.uuid4()
        nid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_snapshot_config(uid=uid, tid=tid, nid=nid)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_IUID)

    def test_authorize_get_snapshot_config_failure_invalid_tid(self):
        ''' authorize_get_snapshot_config should fail if tid is invalid '''
        tids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        for tid in tids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_snapshot_config(uid=uid, tid=tid, nid=nid)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_ITID)

    def test_authorize_get_snapshot_config_failure_invalid_nid(self):
        ''' authorize_get_snapshot_config should fail if nid is invalid '''
        nids=[None, 24232, 2342.23423, {'a':'dict'},['a','list'],('a','tuple'),{'set'},uuid.uuid4().hex, uuid.uuid1(), 'Usernames','user name']
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        for nid in nids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_snapshot_config(uid=uid, tid=tid, nid=nid)
            self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_INID)

    def test_authorize_get_snapshot_config_failure_non_existent_ticket(self):
        ''' authorize_get_snapshot_config should fail if ticket does not exist '''
        uid=uuid.uuid4()
        tid=uuid.uuid4()
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid, tid=tid, nid=nid)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_TNF)

    def test_authorize_get_snapshot_config_failure_expired_ticket(self):
        ''' authorize_get_snapshot_config should fail if ticket has expired '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        expires=timeuuid.uuid1(seconds=1)
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, expires=expires,allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_EXPT)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_TNF)

    def test_authorize_get_snapshot_config_failure_not_shared_with_uid(self):
        ''' authorize_get_snapshot_config should fail if uid is not allowed in ticket '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uuid.uuid4()}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_UNA)

    def test_authorize_get_snapshot_config_failure_shared_with_uid_but_invalid_nid(self):
        ''' authorize_get_snapshot_config should fail if uid is listed in ticket allowed uids, but nid is different '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        nid2=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid2)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_DNA)

    def test_authorize_get_snapshot_config_failure_shared_with_cid_but_invalid_nid(self):
        ''' authorize_get_snapshot_config should fail if uid belongs to a listed ticket allowed cids, but nid is different '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        cid=uuid.uuid4()
        circle=ormcircle.Circle(cid=cid, uid=uid1, circlename='circlename', type='u',creation_date=timeuuid.uuid1(),members={uid2})
        self.assertTrue(circleapi.new_circle(circle))
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1()
        interval_end=timeuuid.uuid1()
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids=set()
        shared_with_cids={cid}
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        nid2=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid2)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_DNA)

    def test_authorize_get_snapshot_config_failure_insufficient_privileges(self):
        ''' authorize_get_snapshot_config should fail if user has insufficient privileges to acomplish requested operation '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        ticket=ticketapi.get_ticket(tid=tid['tid'])
        ticket.permissions=dict(ticket.permissions)
        ticket.permissions[nid]=0
        self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid)
        self.assertEqual(cm.exception.error, errors.E_ATA_AGSNC_INSP)

    def test_authorize_get_snapshot_config_success(self):
        ''' authorize_get_snapshot_config should succeed '''
        uid1=uuid.uuid4()
        uid2=uuid.uuid4()
        nid=uuid.uuid4()
        wid=uuid.uuid4()
        interval_init=timeuuid.uuid1(seconds=1000)
        interval_end=timeuuid.uuid1(seconds=2000)
        widgetname='test_new_snapshot_ticket_success_snapshotds'
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        shared_with_uids={uid2}
        shared_with_cids=set()
        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=pid, datapointname=pid.hex, color=str(pid))
        snapshot=ormsnapshot.SnapshotDp(nid=nid, uid=uid1, wid=wid, interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, pid=pid, datapoint_config=datapoint_config)
        self.assertTrue(snapshotapi.new_snapshot(snapshot=snapshot))
        tid=provision.new_snapshot_ticket(uid=uid1, nid=nid, allowed_uids=shared_with_uids, allowed_cids=shared_with_cids)
        self.assertTrue(authorization.authorize_get_snapshot_config(uid=uid2, tid=tid['tid'], nid=nid))

