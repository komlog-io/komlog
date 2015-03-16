'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.parametrization.widget import types

class Snapshot(object):
    def __init__(self,nid,uid,type):
        self.nid=nid
        self.uid=uid
        self.type=type

class SnapshotDs(Snapshot):
    def __init__(self,nid,uid,wid,interval_init,interval_end,widgetname,creation_date,did,shared_with_uids,shared_with_cids):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.did=did
        self.shared_with_uids=shared_with_uids if shared_with_uids else set()
        self.shared_with_cids=shared_with_cids if shared_with_cids else set()
        super(SnapshotDs,self).__init__(nid,uid,types.DATASOURCE)

class SnapshotDp(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,pid,shared_with_uids,shared_with_cids):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.pid=pid
        self.shared_with_uids=shared_with_uids if shared_with_uids else set()
        self.shared_with_cids=shared_with_cids if shared_with_cids else set()
        super(SnapshotDp,self).__init__(nid,uid,types.DATAPOINT)

class SnapshotHistogram(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors,shared_with_uids,shared_with_cids):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints
        self.colors=colors
        self.shared_with_uids=shared_with_uids if shared_with_uids else set()
        self.shared_with_cids=shared_with_cids if shared_with_cids else set()
        super(SnapshotHistogram,self).__init__(nid,uid,types.HISTOGRAM)

class SnapshotLinegraph(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors,shared_with_uids,shared_with_cids):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints
        self.colors=colors
        self.shared_with_uids=shared_with_uids if shared_with_uids else set()
        self.shared_with_cids=shared_with_cids if shared_with_cids else set()
        super(SnapshotLinegraph,self).__init__(nid,uid,types.LINEGRAPH)

class SnapshotTable(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors,shared_with_uids,shared_with_cids):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints
        self.colors=colors
        self.shared_with_uids=shared_with_uids if shared_with_uids else set()
        self.shared_with_cids=shared_with_cids if shared_with_cids else set()
        super(SnapshotTable,self).__init__(nid,uid,types.TABLE)

