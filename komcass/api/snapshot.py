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
    return ormsnapshot.Snapshot(**row[0]) if row else None

def get_snapshots(uid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_UID,(uid,))
    snapshots=[]
    if row:
        for n in row:
            snapshot=ormsnapshot.Snapshot(**n)
            snapshots.append(snapshot)
    return snapshots

def get_snapshots_nids(uid):
    row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOT_B_UID,(uid,))
    nids=[]
    if row:
        for r in row:
            nids.append(r['nid'])
    return nids

def get_number_of_snapshots_by_uid(uid):
    row=connection.session.execute(stmtsnapshot.S_COUNT_MSTSNAPSHOT_B_UID,(uid,))
    return row[0]['count'] if row else 0

def get_snapshots_ds_nids(wid):
    data=[]
    row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOTDS_B_WID,(wid,))
    if row:
        for r in row:
            data.append(r['nid'])
    return data

def get_snapshots_dp_nids(wid):
    data=[]
    row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOTDP_B_WID,(wid,))
    if row:
        for r in row:
            data.append(r['nid'])
    return data

def get_snapshots_histogram_nids(wid):
    data=[]
    row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOTHISTOGRAM_B_WID,(wid,))
    if row:
        for r in row:
            data.append(r['nid'])
    return data

def get_snapshots_linegraph_nids(wid):
    data=[]
    row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOTLINEGRAPH_B_WID,(wid,))
    if row:
        for r in row:
            data.append(r['nid'])
    return data

def get_snapshots_table_nids(wid):
    data=[]
    row=connection.session.execute(stmtsnapshot.S_NID_MSTSNAPSHOTTABLE_B_WID,(wid,))
    if row:
        for r in row:
            data.append(r['nid'])
    return data

def delete_snapshot(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
    if row:
        snapshot=ormsnapshot.Snapshot(**row[0])
        if snapshot.type == prmwidget.types.DATASOURCE:
            _delete_snapshot_ds(nid)
        elif snapshot.type == prmwidget.types.DATAPOINT:
            _delete_snapshot_dp(nid)
        elif snapshot.type == prmwidget.types.HISTOGRAM:
            _delete_snapshot_histogram(nid)
        elif snapshot.type == prmwidget.types.LINEGRAPH:
            _delete_snapshot_linegraph(nid)
        elif snapshot.type == prmwidget.types.TABLE:
            _delete_snapshot_table(nid)
        connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOT_B_NID,(nid,))
    return True

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
    elif snapshot.type==prmwidget.types.HISTOGRAM:
        _insert_snapshot_histogram(snapshot)
    elif snapshot.type==prmwidget.types.LINEGRAPH:
        _insert_snapshot_linegraph(snapshot)
    elif snapshot.type==prmwidget.types.TABLE:
        _insert_snapshot_table(snapshot)
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOT,(snapshot.nid,snapshot.uid,snapshot.type))
    return True

def get_snapshot_ds(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDS_B_NID,(nid,))
    return ormsnapshot.SnapshotDs(**row[0]) if row else None

def get_snapshot_dp(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDP_B_NID,(nid,))
    return ormsnapshot.SnapshotDp(**row[0]) if row else None

def get_snapshot_histogram(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTHISTOGRAM_B_NID,(nid,))
    return ormsnapshot.SnapshotHistogram(**row[0]) if row else None

def get_snapshot_linegraph(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTLINEGRAPH_B_NID,(nid,))
    return ormsnapshot.SnapshotLinegraph(**row[0]) if row else None

def get_snapshot_table(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTTABLE_B_NID,(nid,))
    return ormsnapshot.SnapshotTable(**row[0]) if row else None

def _delete_snapshot_ds(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTDS_B_NID,(nid,))
    return True

def _insert_snapshot_ds(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTDS,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date,snapshot.did,snapshot.shared_with_uids,snapshot.shared_with_cids))
    return True

def _delete_snapshot_dp(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTDP_B_NID,(nid,))
    return True

def _insert_snapshot_dp(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTDP,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date,snapshot.pid,snapshot.shared_with_uids,snapshot.shared_with_cids))
    return True

def _delete_snapshot_histogram(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTHISTOGRAM_B_NID,(nid,))
    return True

def _insert_snapshot_histogram(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTHISTOGRAM,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date,snapshot.datapoints,snapshot.colors,snapshot.shared_with_uids,snapshot.shared_with_cids))
    return True

def _delete_snapshot_linegraph(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTLINEGRAPH_B_NID,(nid,))
    return True

def _insert_snapshot_linegraph(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTLINEGRAPH,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date,snapshot.datapoints,snapshot.colors,snapshot.shared_with_uids,snapshot.shared_with_cids))
    return True

def _delete_snapshot_table(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTTABLE_B_NID,(nid,))
    return True

def _insert_snapshot_table(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTTABLE,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date,snapshot.datapoints,snapshot.colors,snapshot.shared_with_uids,snapshot.shared_with_cids))
    return True

