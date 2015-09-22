'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.parametrization.widget import types

class Widget(object):
    def __init__(self,wid,uid,type):
        self.wid=wid
        self.uid=uid
        self.type=type

class WidgetDs(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,did):
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.did=did
        super(WidgetDs,self).__init__(wid,uid,types.DATASOURCE)

class WidgetDp(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,pid):
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.pid=pid
        super(WidgetDp,self).__init__(wid,uid,types.DATAPOINT)


class WidgetHistogram(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,datapoints=None,colors=None):
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints if datapoints else set()
        self.colors=colors if colors else dict()
        super(WidgetHistogram,self).__init__(wid,uid,types.HISTOGRAM)

class WidgetLinegraph(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,datapoints=None,colors=None):
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints if datapoints else set()
        self.colors=colors if colors else dict()
        super(WidgetLinegraph,self).__init__(wid,uid,types.LINEGRAPH)

class WidgetTable(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,datapoints=None,colors=None):
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints if datapoints else set()
        self.colors=colors if colors else dict()
        super(WidgetTable,self).__init__(wid,uid,types.TABLE)

class WidgetMultidp(Widget):
    def __init__(self,wid,uid,widgetname,creation_date,active_visualization,datapoints=None):
        self.widgetname=widgetname
        self.creation_date=creation_date
        self.datapoints=datapoints if datapoints else set()
        self.active_visualization=active_visualization
        super(WidgetMultidp,self).__init__(wid,uid,types.MULTIDP)

