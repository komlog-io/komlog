'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.parametrization.widget import types

class Widget(object):
    def __init__(self,wid,uid,type,creation_date,widgetname):
        self.wid=wid
        self.uid=uid
        self.type=type
        self.creation_date=creation_date
        self.widgetname=widgetname

class WidgetDs(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,did):
        self.did=did
        super(WidgetDs,self).__init__(wid,uid,types.DATASOURCE,creation_date,widgetname)

class WidgetDp(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,pid):
        self.pid=pid
        super(WidgetDp,self).__init__(wid,uid,types.DATAPOINT,creation_date,widgetname)


class WidgetHistogram(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,datapoints=None,colors=None):
        self.datapoints=datapoints if datapoints else set()
        self.colors=colors if colors else dict()
        super(WidgetHistogram,self).__init__(wid,uid,types.HISTOGRAM,creation_date,widgetname)

class WidgetLinegraph(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,datapoints=None,colors=None):
        self.datapoints=datapoints if datapoints else set()
        self.colors=colors if colors else dict()
        super(WidgetLinegraph,self).__init__(wid,uid,types.LINEGRAPH,creation_date,widgetname)

class WidgetTable(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,datapoints=None,colors=None):
        self.datapoints=datapoints if datapoints else set()
        self.colors=colors if colors else dict()
        super(WidgetTable,self).__init__(wid,uid,types.TABLE,creation_date,widgetname)

class WidgetMultidp(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,active_visualization,datapoints=None):
        self.datapoints=datapoints if datapoints else set()
        self.active_visualization=active_visualization
        super(WidgetMultidp,self).__init__(wid,uid,types.MULTIDP,creation_date,widgetname)

