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
    def __init__(self,nid,uid,wid,interval_init,interval_end,widgetname,creation_date,did):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.did=did
        super(SnapshotDs,self).__init__(nid,uid,types.DATASOURCE)

class SnapshotDp(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,pid):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.pid=pid
        super(SnapshotDp,self).__init__(nid,uid,types.DATAPOINT)

class SnapshotHistogram(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints
        self.colors=colors
        super(SnapshotHistogram,self).__init__(nid,uid,types.HISTOGRAM)

class SnapshotLinegraph(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints
        self.colors=colors
        super(SnapshotLinegraph,self).__init__(nid,uid,types.LINEGRAPH)

class SnapshotTable(Snapshot):
    def __init__(self,nid,uid,wid,interval_init, interval_end, widgetname,creation_date,datapoints,colors):
        self.wid=wid
        self.interval_init=interval_init
        self.interval_end=interval_end
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints
        self.colors=colors
        super(SnapshotTable,self).__init__(nid,uid,types.TABLE)

