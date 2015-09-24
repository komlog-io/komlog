'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import snapshot as ormsnapshot
from komcass.model.statement import snapshot as stmtsnapshot
from komcass.model.parametrization import widget as prmwidget
from komcass import exceptions, connection

def get_snapshot(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
    return _get_snapshot(ormsnapshot.Snapshot(**row[0])) if row else None

def get_snapshots(uid):
    snapshots=[]
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_UID,(uid,))
    if row:
        for n in row:
            snapshot=_get_snapshot(ormsnapshot.Snapshot(**n))
            if snapshot:
                snapshots.append(snapshot)
    return snapshots

def _get_snapshot(snapshot):
    if not isinstance(snapshot,ormsnapshot.Snapshot):
        return None
    else:
        if snapshot.type==prmwidget.types.DATASOURCE:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDS_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotDs(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, did=snap_conf[0]['did'], shared_with_uids=snapshot.shared_with_uids, shared_with_cids=snapshot.shared_with_cids) if snap_conf else None
        elif snapshot.type==prmwidget.types.DATAPOINT:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDP_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotDp(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, pid=snap_conf[0]['pid'], shared_with_uids=snapshot.shared_with_uids, shared_with_cids=snapshot.shared_with_cids) if snap_conf else None
        elif snapshot.type==prmwidget.types.MULTIDP:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTMULTIDP_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotMultidp(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, active_visualization=snap_conf[0]['active_visualization'], datapoints=snap_conf[0]['datapoints'], shared_with_uids=snapshot.shared_with_uids, shared_with_cids=snapshot.shared_with_cids) if snap_conf else None
        elif snapshot.type==prmwidget.types.HISTOGRAM:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTHISTOGRAM_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotHistogram(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, datapoints=snap_conf[0]['datapoints'], colors=snap_conf[0]['colors'], shared_with_uids=snapshot.shared_with_uids, shared_with_cids=snapshot.shared_with_cids) if snap_conf else None
        elif snapshot.type==prmwidget.types.LINEGRAPH:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTLINEGRAPH_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotLinegraph(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, datapoints=snap_conf[0]['datapoints'], colors=snap_conf[0]['colors'], shared_with_uids=snapshot.shared_with_uids, shared_with_cids=snapshot.shared_with_cids) if snap_conf else None
        elif snapshot.type==prmwidget.types.TABLE:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTTABLE_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotTable(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, datapoints=snap_conf[0]['datapoints'], colors=snap_conf[0]['colors'], shared_with_uids=snapshot.shared_with_uids, shared_with_cids=snapshot.shared_with_cids) if snap_conf else None
        else:
            return None

def get_snapshots_nids(uid=None, wid=None):
    row=None
    if uid:
        row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOT_B_UID,(uid,))
    elif wid:
        row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOT_B_WID,(wid,))
    nids=[]
    if row:
        for r in row:
            nids.append(r['nid'])
    return nids

def get_number_of_snapshots(uid=None, wid=None):
    row=None
    if uid:
        row=connection.session.execute(stmtsnapshot.S_COUNT_MSTSNAPSHOT_B_UID,(uid,))
    elif wid:
        row=connection.session.execute(stmtsnapshot.S_COUNT_MSTSNAPSHOT_B_WID,(wid,))
    return row[0]['count'] if row else 0

def new_snapshot(snapshot):
    if not isinstance(snapshot, ormsnapshot.Snapshot):
        return False
    existingsnapshot=get_snapshot(snapshot.nid)
    if existingsnapshot:
        return False
    else:
        return insert_snapshot(snapshot)

def insert_snapshot(snapshot):
    if not isinstance(snapshot, ormsnapshot.Snapshot):
        return False
    if snapshot.type==prmwidget.types.DATASOURCE:
        _insert_snapshot_ds(snapshot)
    elif snapshot.type==prmwidget.types.DATAPOINT:
        _insert_snapshot_dp(snapshot)
    elif snapshot.type==prmwidget.types.MULTIDP:
        _insert_snapshot_multidp(snapshot)
    elif snapshot.type==prmwidget.types.HISTOGRAM:
        _insert_snapshot_histogram(snapshot)
    elif snapshot.type==prmwidget.types.LINEGRAPH:
        _insert_snapshot_linegraph(snapshot)
    elif snapshot.type==prmwidget.types.TABLE:
        _insert_snapshot_table(snapshot)
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOT,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.type,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date,snapshot.shared_with_uids,snapshot.shared_with_cids))
    return True

def get_snapshot_ds(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDS_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotDs(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],did=snap_conf[0]['did'],shared_with_uids=row[0]['shared_with_uids'],shared_with_cids=row[0]['shared_with_cids'])
    return None

def get_snapshot_dp(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDP_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotDp(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],pid=snap_conf[0]['pid'],shared_with_uids=row[0]['shared_with_uids'],shared_with_cids=row[0]['shared_with_cids'])
    return None

def get_snapshot_histogram(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTHISTOGRAM_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotHistogram(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],colors=snap_conf[0]['colors'],shared_with_uids=row[0]['shared_with_uids'],shared_with_cids=row[0]['shared_with_cids'])
    return None

def get_snapshot_linegraph(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTLINEGRAPH_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotLinegraph(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],colors=snap_conf[0]['colors'],shared_with_uids=row[0]['shared_with_uids'],shared_with_cids=row[0]['shared_with_cids'])
    return None

def get_snapshot_table(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTTABLE_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotTable(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],colors=snap_conf[0]['colors'],shared_with_uids=row[0]['shared_with_uids'],shared_with_cids=row[0]['shared_with_cids'])
    return None

def get_snapshot_multidp(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTMULTIDP_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotMultidp(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],active_visualization=snap_conf[0]['active_visualization'],shared_with_uids=row[0]['shared_with_uids'],shared_with_cids=row[0]['shared_with_cids'])
    return None

def delete_snapshot(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
    if row:
        snapshot=ormsnapshot.Snapshot(**row[0])
        if snapshot.type == prmwidget.types.DATASOURCE:
            _delete_snapshot_ds(nid)
        elif snapshot.type == prmwidget.types.DATAPOINT:
            _delete_snapshot_dp(nid)
        elif snapshot.type == prmwidget.types.MULTIDP:
            _delete_snapshot_multidp(nid)
        elif snapshot.type == prmwidget.types.HISTOGRAM:
            _delete_snapshot_histogram(nid)
        elif snapshot.type == prmwidget.types.LINEGRAPH:
            _delete_snapshot_linegraph(nid)
        elif snapshot.type == prmwidget.types.TABLE:
            _delete_snapshot_table(nid)
        connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOT_B_NID,(nid,))
    return True

def _delete_snapshot_ds(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTDS_B_NID,(nid,))
    return True

def _insert_snapshot_ds(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTDS,(snapshot.nid,snapshot.did))
    return True

def _delete_snapshot_dp(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTDP_B_NID,(nid,))
    return True

def _insert_snapshot_dp(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTDP,(snapshot.nid,snapshot.pid))
    return True

def _delete_snapshot_histogram(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTHISTOGRAM_B_NID,(nid,))
    return True

def _insert_snapshot_histogram(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTHISTOGRAM,(snapshot.nid,snapshot.datapoints,snapshot.colors))
    return True

def _delete_snapshot_linegraph(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTLINEGRAPH_B_NID,(nid,))
    return True

def _insert_snapshot_linegraph(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTLINEGRAPH,(snapshot.nid,snapshot.datapoints,snapshot.colors))
    return True

def _delete_snapshot_table(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTTABLE_B_NID,(nid,))
    return True

def _insert_snapshot_table(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTTABLE,(snapshot.nid,snapshot.datapoints,snapshot.colors))
    return True

def _delete_snapshot_multidp(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTMULTIDP_B_NID,(nid,))
    return True

def _insert_snapshot_multidp(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTMULTIDP,(snapshot.nid,snapshot.active_visualization, snapshot.datapoints))
    return True

