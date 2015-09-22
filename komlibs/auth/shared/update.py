#coding: utf-8
'''
update.py 

This file implements functions to update authorization to shared elements

@author: jcazor
@date: 2015/03/08

'''

from komcass.api import snapshot as cassapisnapshot
from komcass.model.parametrization.widget import types as snapshottypes
from komlibs.auth import operations, permissions
from komlibs.graph.api import base as graphbase
from komlibs.graph.relations import vertex

update_funcs = {
                operations.NEW_SNAPSHOT: ['new_snapshot'],
}

def get_update_funcs(operation):
    try:
        return update_funcs[operation]
    except KeyError:
        return []

def new_snapshot(params):
    if not 'nid' in params:
        return False
    nid=params['nid']
    snapshot=cassapisnapshot.get_snapshot(nid=nid)
    if snapshot:
        if snapshot.type==snapshottypes.DATASOURCE:
            snapshot=cassapisnapshot.get_snapshot_ds(nid=nid)
            if not snapshot:
                return False
            graphbase.set_member_edge(ido=snapshot.did, idd=nid, vertex_type=vertex.DATASOURCE_SNAPSHOT_RELATION)
        elif snapshot.type==snapshottypes.DATAPOINT:
            snapshot=cassapisnapshot.get_snapshot_dp(nid=nid)
            if not snapshot:
                return False
            graphbase.set_member_edge(ido=snapshot.pid, idd=nid, vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION)
        elif snapshot.type==snapshottypes.MULTIDP:
            snapshot=cassapisnapshot.get_snapshot_multidp(nid=nid)
            if not snapshot:
                return False
            for pid in snapshot.datapoints:
                graphbase.set_member_edge(ido=pid, idd=nid, vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION)
        elif snapshot.type==snapshottypes.HISTOGRAM:
            snapshot=cassapisnapshot.get_snapshot_histogram(nid=nid)
            if not snapshot:
                return False
            for pid in snapshot.datapoints:
                graphbase.set_member_edge(ido=pid, idd=nid, vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION)
        elif snapshot.type==snapshottypes.LINEGRAPH:
            snapshot=cassapisnapshot.get_snapshot_linegraph(nid=nid)
            if not snapshot:
                return False
            for pid in snapshot.datapoints:
                graphbase.set_member_edge(ido=pid, idd=nid, vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION)
        elif snapshot.type==snapshottypes.TABLE:
            snapshot=cassapisnapshot.get_snapshot_table(nid=nid)
            if not snapshot:
                return False
            for pid in snapshot.datapoints:
                graphbase.set_member_edge(ido=pid, idd=nid, vertex_type=vertex.DATAPOINT_SNAPSHOT_RELATION)
        else:
            return False
        ii=snapshot.interval_init
        ie=snapshot.interval_end
        perm=permissions.CAN_READ
        for uid in snapshot.shared_with_uids:
            graphbase.set_bounded_share_edge(ido=nid, idd=uid, vertex_type=vertex.SNAPSHOT_USER_RELATION, perm=perm, interval_init=ii, interval_end=ie)
        for cid in snapshot.shared_with_cids:
            graphbase.set_bounded_share_edge(ido=nid, idd=cid, vertex_type=vertex.SNAPSHOT_CIRCLE_RELATION, perm=perm, interval_init=ii, interval_end=ie)
        return True
    else:
        #nothing to do
        return True

