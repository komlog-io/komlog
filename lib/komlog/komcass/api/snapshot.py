'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import snapshot as ormsnapshot
from komlog.komcass.model.statement import snapshot as stmtsnapshot
from komlog.komcass.model.parametrization import widget as prmwidget
from komlog.komcass import exceptions, connection

@exceptions.ExceptionHandler
def get_snapshot(nid):
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
    return _get_snapshot(ormsnapshot.Snapshot(**row[0])) if row else None

@exceptions.ExceptionHandler
def get_snapshots(uid):
    snapshots=[]
    row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_UID,(uid,))
    if row:
        for n in row:
            snapshot=_get_snapshot(ormsnapshot.Snapshot(**n))
            if snapshot:
                snapshots.append(snapshot)
    return snapshots

@exceptions.ExceptionHandler
def _get_snapshot(snapshot):
    if not isinstance(snapshot,ormsnapshot.Snapshot):
        return None
    else:
        if snapshot.type==prmwidget.types.DATASOURCE:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDS_B_NID,(snapshot.nid,))
            if snap_conf:
                datapoints_config=[]
                if snap_conf[0]['datapoints_config']:
                    for datapoint in snap_conf[0]['datapoints_config']:
                        datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=datapoint.pid,datapointname=datapoint.datapointname,color=datapoint.color)
                        datapoints_config.append(datapoint_config)
                datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=snap_conf[0]['datasource_config'].did, datasourcename=snap_conf[0]['datasource_config'].datasourcename)
                return ormsnapshot.SnapshotDs(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, did=snap_conf[0]['did'], datasource_config=datasource_config, datapoints_config=datapoints_config)
            else:
                return None
        elif snapshot.type==prmwidget.types.DATAPOINT:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDP_B_NID,(snapshot.nid,))
            if snap_conf:
                datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=snap_conf[0]['datapoint_config'].pid, datapointname=snap_conf[0]['datapoint_config'].datapointname, color=snap_conf[0]['datapoint_config'].color)
                return ormsnapshot.SnapshotDp(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, pid=snap_conf[0]['pid'], datapoint_config=datapoint_config)
            else:
                return None
        elif snapshot.type==prmwidget.types.MULTIDP:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTMULTIDP_B_NID,(snapshot.nid,))
            if snap_conf:
                datapoints_config=[]
                for datapoint in snap_conf[0]['datapoints_config']:
                    datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=datapoint.pid,datapointname=datapoint.datapointname,color=datapoint.color)
                    datapoints_config.append(datapoint_config)
                return ormsnapshot.SnapshotMultidp(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, active_visualization=snap_conf[0]['active_visualization'], datapoints=snap_conf[0]['datapoints'], datapoints_config=datapoints_config)
            else:
                return None
        elif snapshot.type==prmwidget.types.HISTOGRAM:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTHISTOGRAM_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotHistogram(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, datapoints=snap_conf[0]['datapoints'], colors=snap_conf[0]['colors']) if snap_conf else None
        elif snapshot.type==prmwidget.types.LINEGRAPH:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTLINEGRAPH_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotLinegraph(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, datapoints=snap_conf[0]['datapoints'], colors=snap_conf[0]['colors']) if snap_conf else None
        elif snapshot.type==prmwidget.types.TABLE:
            snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTTABLE_B_NID,(snapshot.nid,))
            return ormsnapshot.SnapshotTable(nid=snapshot.nid, uid=snapshot.uid,wid=snapshot.wid,interval_init=snapshot.interval_init, interval_end=snapshot.interval_end, widgetname=snapshot.widgetname, creation_date=snapshot.creation_date, datapoints=snap_conf[0]['datapoints'], colors=snap_conf[0]['colors']) if snap_conf else None
        else:
            return None

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def get_number_of_snapshots(uid=None, wid=None):
    row=None
    if uid:
        row=connection.session.execute(stmtsnapshot.S_COUNT_MSTSNAPSHOT_B_UID,(uid,))
    elif wid:
        row=connection.session.execute(stmtsnapshot.S_COUNT_MSTSNAPSHOT_B_WID,(wid,))
    return row[0]['count'] if row else 0

@exceptions.ExceptionHandler
def new_snapshot(snapshot):
    if not isinstance(snapshot, ormsnapshot.Snapshot):
        return False
    resp=connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOT_INE,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.type,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date))
    if resp[0]['[applied]']:
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
        return True
    else:
        return False

@exceptions.ExceptionHandler
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
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOT,(snapshot.nid,snapshot.uid,snapshot.wid,snapshot.type,snapshot.interval_init,snapshot.interval_end,snapshot.widgetname,snapshot.creation_date))
    return True

@exceptions.ExceptionHandler
def get_snapshot_ds(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDS_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            datapoints_config=[]
            if snap_conf[0]['datapoints_config']:
                for datapoint in snap_conf[0]['datapoints_config']:
                    datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=datapoint.pid,datapointname=datapoint.datapointname,color=datapoint.color)
                    datapoints_config.append(datapoint_config)
            datasource_config=ormsnapshot.SnapshotDatasourceConfig(did=snap_conf[0]['datasource_config'].did,datasourcename=snap_conf[0]['datasource_config'].datasourcename)
            return ormsnapshot.SnapshotDs(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],did=snap_conf[0]['did'], datasource_config=datasource_config, datapoints_config=datapoints_config)
    return None

@exceptions.ExceptionHandler
def get_snapshot_dp(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTDP_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=snap_conf[0]['datapoint_config'].pid,datapointname=snap_conf[0]['datapoint_config'].datapointname, color=snap_conf[0]['datapoint_config'].color)
            return ormsnapshot.SnapshotDp(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],pid=snap_conf[0]['pid'], datapoint_config=datapoint_config)
    return None

@exceptions.ExceptionHandler
def get_snapshot_histogram(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTHISTOGRAM_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotHistogram(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],colors=snap_conf[0]['colors'])
    return None

@exceptions.ExceptionHandler
def get_snapshot_linegraph(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTLINEGRAPH_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotLinegraph(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],colors=snap_conf[0]['colors'])
    return None

@exceptions.ExceptionHandler
def get_snapshot_table(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTTABLE_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            return ormsnapshot.SnapshotTable(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],colors=snap_conf[0]['colors'])
    return None

@exceptions.ExceptionHandler
def get_snapshot_multidp(nid):
    snap_conf=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOTMULTIDP_B_NID,(nid,))
    if snap_conf:
        row=connection.session.execute(stmtsnapshot.S_A_MSTSNAPSHOT_B_NID,(nid,))
        if row:
            datapoints_config=[]
            for datapoint in snap_conf[0]['datapoints_config']:
                datapoint_config=ormsnapshot.SnapshotDatapointConfig(pid=datapoint.pid,datapointname=datapoint.datapointname,color=datapoint.color)
                datapoints_config.append(datapoint_config)
            return ormsnapshot.SnapshotMultidp(uid=row[0]['uid'],nid=row[0]['nid'],wid=row[0]['wid'],interval_init=row[0]['interval_init'],interval_end=row[0]['interval_end'],widgetname=row[0]['widgetname'],creation_date=row[0]['creation_date'],datapoints=snap_conf[0]['datapoints'],datapoints_config=datapoints_config, active_visualization=snap_conf[0]['active_visualization'])
    return None

@exceptions.ExceptionHandler
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

@exceptions.ExceptionHandler
def _delete_snapshot_ds(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTDS_B_NID,(nid,))
    return True

@exceptions.ExceptionHandler
def _insert_snapshot_ds(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTDS,(snapshot.nid, snapshot.did, snapshot.datasource_config, snapshot.datapoints_config))
    return True

@exceptions.ExceptionHandler
def _delete_snapshot_dp(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTDP_B_NID,(nid,))
    return True

@exceptions.ExceptionHandler
def _insert_snapshot_dp(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTDP,(snapshot.nid, snapshot.pid, snapshot.datapoint_config))
    return True

@exceptions.ExceptionHandler
def _delete_snapshot_histogram(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTHISTOGRAM_B_NID,(nid,))
    return True

@exceptions.ExceptionHandler
def _insert_snapshot_histogram(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTHISTOGRAM,(snapshot.nid,snapshot.datapoints,snapshot.colors))
    return True

@exceptions.ExceptionHandler
def _delete_snapshot_linegraph(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTLINEGRAPH_B_NID,(nid,))
    return True

@exceptions.ExceptionHandler
def _insert_snapshot_linegraph(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTLINEGRAPH,(snapshot.nid,snapshot.datapoints,snapshot.colors))
    return True

@exceptions.ExceptionHandler
def _delete_snapshot_table(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTTABLE_B_NID,(nid,))
    return True

@exceptions.ExceptionHandler
def _insert_snapshot_table(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTTABLE,(snapshot.nid,snapshot.datapoints,snapshot.colors))
    return True

@exceptions.ExceptionHandler
def _delete_snapshot_multidp(nid):
    connection.session.execute(stmtsnapshot.D_A_MSTSNAPSHOTMULTIDP_B_NID,(nid,))
    return True

@exceptions.ExceptionHandler
def _insert_snapshot_multidp(snapshot):
    connection.session.execute(stmtsnapshot.I_A_MSTSNAPSHOTMULTIDP,(snapshot.nid,snapshot.active_visualization, snapshot.datapoints,snapshot.datapoints_config))
    return True

