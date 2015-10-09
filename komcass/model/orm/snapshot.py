'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.parametrization.widget import types

class Snapshot(object):
    def __init__(self,nid,uid,wid,type,interval_init, interval_end, widgetname, creation_date, shared_with_uids=None, shared_with_cids=None):
        self.nid=nid
        self.uid=uid
        self.wid=wid
        self.type=type
        self.widgetname=widgetname
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.creation_date=creation_date
        self.shared_with_uids=shared_with_uids if shared_with_uids else set()
        self.shared_with_cids=shared_with_cids if shared_with_cids else set()

class SnapshotDatapointConfig:
    def __init__(self, pid, datapointname, color):
        self.pid=pid
        self.datapointname=datapointname
        self.color=color

class SnapshotDatasourceConfig:
    def __init__(self, did, datasourcename):
        self.did=did
        self.datasourcename=datasourcename

class SnapshotDs(Snapshot):
    def __init__(self, nid, uid, wid, interval_init, interval_end, widgetname, creation_date, did, datasource_config, datapoints_config, shared_with_uids=None, shared_with_cids=None):
        self.did=did
        self.datasource_config=datasource_config
        self.datapoints_config=datapoints_config if datapoints_config else []
        super(SnapshotDs,self).__init__(nid=nid,uid=uid,wid=wid,type=types.DATASOURCE,interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)

class SnapshotDp(Snapshot):
    def __init__(self, nid, uid, wid, interval_init, interval_end, widgetname, creation_date, pid, datapoint_config, shared_with_uids=None, shared_with_cids=None):
        self.pid=pid
        self.datapoint_config=datapoint_config
        super(SnapshotDp,self).__init__(nid=nid,uid=uid,wid=wid,type=types.DATAPOINT,interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)

class SnapshotHistogram(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors,shared_with_uids=None,shared_with_cids=None):
        self.datapoints=datapoints
        self.colors=colors
        super(SnapshotHistogram,self).__init__(nid=nid,uid=uid,wid=wid,type=types.HISTOGRAM,interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)

class SnapshotLinegraph(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors,shared_with_uids=None,shared_with_cids=None):
        self.datapoints=datapoints
        self.colors=colors
        super(SnapshotLinegraph,self).__init__(nid=nid,uid=uid,wid=wid,type=types.LINEGRAPH,interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)

class SnapshotTable(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors,shared_with_uids=None,shared_with_cids=None):
        self.datapoints=datapoints
        self.colors=colors
        super(SnapshotTable,self).__init__(nid=nid,uid=uid,wid=wid,type=types.TABLE,interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)

class SnapshotMultidp(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,active_visualization,datapoints,datapoints_config,shared_with_uids=None,shared_with_cids=None):
        self.active_visualization=active_visualization
        self.datapoints=datapoints
        self.datapoints_config=datapoints_config
        super(SnapshotMultidp,self).__init__(nid=nid,uid=uid,wid=wid,type=types.MULTIDP,interval_init=interval_init, interval_end=interval_end, widgetname=widgetname, creation_date=creation_date, shared_with_uids=shared_with_uids, shared_with_cids=shared_with_cids)

