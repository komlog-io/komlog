'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import widget as ormwidget
from komcass.model.statement import widget as stmtwidget
from komcass.model.parametrization import widget as prmwidget
from komcass.exception import widget as excpwidget
from komcass import connection

def get_widget(wid):
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.Widget(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='get_widget',field='wid',value=wid)

def get_widgets(uid):
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_UID,(uid,))
    widgets=[]
    if row:
        for w in row:
            widget=ormwidget.Widget(**w)
            widgets.append(widget)
    return widgets

def get_widgets_wids(uid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGET_B_UID,(uid,))
    wids=[]
    if row:
        for r in row:
            wids.append(r['wid'])
    return wids

def get_number_of_widgets_by_uid(uid):
    row=connection.session.execute(stmtwidget.S_COUNT_MSTWIDGET_B_UID,(uid,))
    return row[0]['count'] if row else 0

def delete_widget(wid):
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(wid,))
    if not row:
        return True
    elif len(row)>1:
        raise excpwidget.DataConsistencyException(function='delete_widget',field='wid',value=wid)
    else:
        widget=ormwidget.Widget(**row[0])
        if widget.type == prmwidget.types.DATASOURCE:
            _delete_widget_ds(wid)
        elif widget.type == prmwidget.types.DATAPOINT:
            _delete_widget_dp(wid)
        elif widget.type == prmwidget.types.HISTOGRAM:
            _delete_widget_histogram(wid)
        elif widget.type == prmwidget.types.LINEGRAPH:
            _delete_widget_linegraph(wid)
        elif widget.type == prmwidget.types.TABLE:
            _delete_widget_table(wid)
        connection.session.execute(stmtwidget.D_A_MSTWIDGET_B_WID,(wid,))
        return True

def new_widget(widget):
    if not isinstance(widget, ormwidget.Widget):
        return False
    existingwidget=get_widget(widget.wid)
    if existingwidget:
        return False
    connection.session.execute(stmtwidget.I_A_MSTWIDGET,(widget.wid,widget.uid,widget.type))
    if widget.type==prmwidget.types.DATASOURCE:
        _insert_widget_ds(widget)
    elif widget.type==prmwidget.types.DATAPOINT:
        _insert_widget_dp(widget)
    elif widget.type==prmwidget.types.HISTOGRAM:
        _insert_widget_histogram(widget)
    elif widget.type==prmwidget.types.LINEGRAPH:
        _insert_widget_linegraph(widget)
    elif widget.type==prmwidget.types.TABLE:
        _insert_widget_table(widget)
    return True

def insert_widget(widget):
    if not isinstance(widget, ormwidget.Widget):
        return False
    connection.session.execute(stmtwidget.I_A_MSTWIDGET,(widget.wid,widget.uid,widget.type))
    if widget.type==prmwidget.types.DATASOURCE:
        _insert_widget_ds(widget)
    elif widget.type==prmwidget.types.DATAPOINT:
        _insert_widget_dp(widget)
    elif widget.type==prmwidget.types.HISTOGRAM:
        _insert_widget_histogram(widget)
    elif widget.type==prmwidget.types.LINEGRAPH:
        _insert_widget_linegraph(widget)
    elif widget.type==prmwidget.types.TABLE:
        _insert_widget_table(widget)
    return True
            
def insert_widget_widgetname(wid, widgetname):
    widget=get_widget(wid=wid)
    if not widget:
        return False
    if widget.type==prmwidget.types.DATASOURCE:
        connection.session.execute(stmtwidget.U_WIDGETNAME_MSTWIDGETDATASOURCE_B_WID,(widgetname,wid))
    elif widget.type==prmwidget.types.DATAPOINT:
        connection.session.execute(stmtwidget.U_WIDGETNAME_MSTWIDGETDATAPOINT_B_WID,(widgetname,wid))
    elif widget.type==prmwidget.types.HISTOGRAM:
        connection.session.execute(stmtwidget.U_WIDGETNAME_MSTWIDGETHISTOGRAM_B_WID,(widgetname,wid))
    elif widget.type==prmwidget.types.LINEGRAPH:
        connection.session.execute(stmtwidget.U_WIDGETNAME_MSTWIDGETLINEGRAPH_B_WID,(widgetname,wid))
    elif widget.type==prmwidget.types.TABLE:
        connection.session.execute(stmtwidget.U_WIDGETNAME_MSTWIDGETTABLE_B_WID,(widgetname,wid))
    else:
        return False
    return True

def get_widget_ds(wid=None, did=None):
    if wid:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGETDS_B_WID,(wid,))
    elif did:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGETDS_B_DID,(did,))
    else:
        return None
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetDs(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='_get_widget_ds',field='wid',value=wid)

def get_widget_dp(wid=None, pid=None):
    if wid:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGETDP_B_WID,(wid,))
    elif pid:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGETDP_B_PID,(pid,))
    else:
        return None
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetDp(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='_get_widget_dp',field='wid',value=wid)

def get_widget_histogram(wid):
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGETHISTOGRAM_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetHistogram(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='get_widget_histogram',field='wid',value=wid)

def get_wids_histograms_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETHISTOGRAM_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def get_widget_linegraph(wid):
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGETLINEGRAPH_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetLinegraph(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='get_widget_linegraph',field='wid',value=wid)

def get_wids_linegraphs_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETLINEGRAPH_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def get_widget_table(wid):
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGETTABLE_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetTable(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='get_widget_table',field='wid',value=wid)

def get_wids_tables_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETTABLE_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def _delete_widget_ds(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETDS_B_WID,(wid,))
    return True

def _insert_widget_ds(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETDS,(widget.wid,widget.uid,widget.widgetname,widget.creation_date,widget.did))
    return True

def _delete_widget_dp(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETDP_B_WID,(wid,))
    return True

def _insert_widget_dp(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETDP,(widget.wid,widget.uid,widget.widgetname,widget.creation_date,widget.pid))
    return True

def _insert_widget_histogram(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETHISTOGRAM,(widget.wid,widget.uid,widget.widgetname,widget.creation_date, widget.datapoints, widget.colors))
    return True

def _delete_widget_histogram(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETHISTOGRAM_B_WID,(wid,))
    return True

def _insert_widget_linegraph(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETLINEGRAPH,(widget.wid,widget.uid,widget.widgetname,widget.creation_date, widget.datapoints, widget.colors))
    return True

def _delete_widget_linegraph(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETLINEGRAPH_B_WID,(wid,))
    return True

def _insert_widget_table(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETTABLE,(widget.wid,widget.uid,widget.widgetname,widget.creation_date, widget.datapoints, widget.colors))
    return True

def _delete_widget_table(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETTABLE_B_WID,(wid,))
    return True

def add_datapoint_to_histogram(wid, pid, color):
    histogram=get_widget_histogram(wid=wid)
    if not histogram:
        return False
    histogram.datapoints.add(pid)
    connection.session.execute(stmtwidget.U_DATAPOINTS_MSTWIDGETHISTOGRAM_B_WID,(histogram.datapoints,wid))
    connection.session.execute(stmtwidget.U_COLOR_MSTWIDGETHISTOGRAM_B_WID,(pid,color,wid))
    return True

def delete_datapoint_from_histogram(wid, pid):
    connection.session.execute(stmtwidget.D_DATAPOINT_MSTWIDGETHISTOGRAM_B_PID_WID,(pid,wid))
    connection.session.execute(stmtwidget.D_COLOR_MSTWIDGETHISTOGRAM_B_PID_WID,(pid,wid))
    return True

def add_datapoint_to_linegraph(wid, pid, color):
    linegraph=get_widget_linegraph(wid=wid)
    if not linegraph:
        return False
    linegraph.datapoints.add(pid)
    connection.session.execute(stmtwidget.U_DATAPOINTS_MSTWIDGETLINEGRAPH_B_WID,(linegraph.datapoints,wid))
    connection.session.execute(stmtwidget.U_COLOR_MSTWIDGETLINEGRAPH_B_WID,(pid,color,wid))
    return True

def delete_datapoint_from_linegraph(wid, pid):
    connection.session.execute(stmtwidget.D_DATAPOINT_MSTWIDGETLINEGRAPH_B_PID_WID,(pid,wid))
    connection.session.execute(stmtwidget.D_COLOR_MSTWIDGETLINEGRAPH_B_PID_WID,(pid,wid))
    return True

def add_datapoint_to_table(wid, pid, color):
    table=get_widget_table(wid=wid)
    if not table:
        return False
    table.datapoints.add(pid)
    connection.session.execute(stmtwidget.U_DATAPOINTS_MSTWIDGETTABLE_B_WID,(table.datapoints,wid))
    connection.session.execute(stmtwidget.U_COLOR_MSTWIDGETTABLE_B_WID,(pid,color,wid))
    return True

def delete_datapoint_from_table(wid, pid):
    connection.session.execute(stmtwidget.D_DATAPOINT_MSTWIDGETTABLE_B_PID_WID,(pid,wid))
    connection.session.execute(stmtwidget.D_COLOR_MSTWIDGETTABLE_B_PID_WID,(pid,wid))
    return True

