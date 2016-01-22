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
    return _get_widget(ormwidget.Widget(**row[0])) if row else None

def get_widgets(uid):
    widgets=[]
    row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_UID,(uid,))
    if row:
        for w in row:
            widget=_get_widget(ormwidget.Widget(**w))
            if widget:
                widgets.append(widget)
    return widgets

def _get_widget(widget):
    if not isinstance(widget, ormwidget.Widget):
        return None
    else:
        if widget.type==prmwidget.types.DATASOURCE:
            widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETDS_B_WID,(widget.wid,))
            if widget_config:
                return ormwidget.WidgetDs(wid=widget.wid, uid=widget.uid, widgetname=widget.widgetname, creation_date=widget.creation_date, did=widget_config[0]['did'])
            else:
                return None
        elif widget.type==prmwidget.types.DATAPOINT:
            widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETDP_B_WID,(widget.wid,))
            if widget_config:
                return ormwidget.WidgetDp(wid=widget.wid, uid=widget.uid, widgetname=widget.widgetname, creation_date=widget.creation_date, pid=widget_config[0]['pid'])
            else:
                return None
        elif widget.type==prmwidget.types.MULTIDP:
            widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETMULTIDP_B_WID,(widget.wid,))
            if widget_config:
                return ormwidget.WidgetMultidp(wid=widget.wid, uid=widget.uid, widgetname=widget.widgetname, creation_date=widget.creation_date, datapoints=widget_config[0]['datapoints'],active_visualization=widget_config[0]['active_visualization'])
            else:
                return None
        elif widget.type==prmwidget.types.HISTOGRAM:
            widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETHISTOGRAM_B_WID,(widget.wid,))
            if widget_config:
                return ormwidget.WidgetHistogram(wid=widget.wid, uid=widget.uid, widgetname=widget.widgetname, creation_date=widget.creation_date, datapoints=widget_config[0]['datapoints'],colors=widget_config[0]['colors'])
            else:
                return None
        elif widget.type==prmwidget.types.LINEGRAPH:
            widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETLINEGRAPH_B_WID,(widget.wid,))
            if widget_config:
                return ormwidget.WidgetLinegraph(wid=widget.wid, uid=widget.uid, widgetname=widget.widgetname, creation_date=widget.creation_date, datapoints=widget_config[0]['datapoints'],colors=widget_config[0]['colors'])
            else:
                return None
        elif widget.type==prmwidget.types.TABLE:
            widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETTABLE_B_WID,(widget.wid,))
            if widget_config:
                return ormwidget.WidgetTable(wid=widget.wid, uid=widget.uid, widgetname=widget.widgetname, creation_date=widget.creation_date, datapoints=widget_config[0]['datapoints'],colors=widget_config[0]['colors'])
            else:
                return None
        else:
            return None

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
        elif widget.type == prmwidget.types.MULTIDP:
            _delete_widget_multidp(wid)
        connection.session.execute(stmtwidget.D_A_MSTWIDGET_B_WID,(wid,))
        return True

def new_widget(widget):
    if not isinstance(widget, ormwidget.Widget):
        return False
    resp=connection.session.execute(stmtwidget.I_A_MSTWIDGET_INE,(widget.wid,widget.uid,widget.type,widget.creation_date, widget.widgetname))
    if resp[0]['[applied]']:
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
        elif widget.type==prmwidget.types.MULTIDP:
            _insert_widget_multidp(widget)
        return True
    else:
        return False

def insert_widget(widget):
    if not isinstance(widget, ormwidget.Widget):
        return False
    connection.session.execute(stmtwidget.I_A_MSTWIDGET,(widget.wid,widget.uid,widget.type,widget.creation_date, widget.widgetname))
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
    elif widget.type==prmwidget.types.MULTIDP:
        _insert_widget_multidp(widget)
    return True

def insert_widget_widgetname(wid, widgetname):
    widget=get_widget(wid=wid)
    if not widget:
        return False
    connection.session.execute(stmtwidget.U_WIDGETNAME_MSTWIDGET_B_WID,(widgetname,wid))
    return True

def insert_widget_multidp_active_visualization(wid, active_visualization):
    widget=get_widget_multidp(wid=wid)
    if not widget:
        return False
    else:
        connection.session.execute(stmtwidget.U_ACTIVEVISUALIZATION_MSTWIDGETMULTIDP_B_WID,(active_visualization,wid))
        return True

def get_widget_ds(wid=None, did=None):
    if wid:
        widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETDS_B_WID,(wid,))
    elif did:
        widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETDS_B_DID,(did,))
    else:
        return None
    if widget_config:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(widget_config[0]['wid'],))
        if row:
            return ormwidget.WidgetDs(wid=row[0]['wid'], uid=row[0]['uid'], widgetname=row[0]['widgetname'], creation_date=row[0]['creation_date'], did=widget_config[0]['did'])
    return None

def get_widget_dp(wid=None, pid=None):
    if wid:
        widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETDP_B_WID,(wid,))
    elif pid:
        widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETDP_B_PID,(pid,))
    else:
        return None
    if widget_config:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(widget_config[0]['wid'],))
        if row:
            return ormwidget.WidgetDp(wid=row[0]['wid'], uid=row[0]['uid'], widgetname=row[0]['widgetname'], creation_date=row[0]['creation_date'], pid=widget_config[0]['pid'])
    return None

def get_widget_histogram(wid):
    widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETHISTOGRAM_B_WID,(wid,))
    if widget_config:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(widget_config[0]['wid'],))
        if row:
            return ormwidget.WidgetHistogram(wid=row[0]['wid'], uid=row[0]['uid'], widgetname=row[0]['widgetname'], creation_date=row[0]['creation_date'], datapoints=widget_config[0]['datapoints'], colors=widget_config[0]['colors'])
    return None

def get_wids_histograms_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETHISTOGRAM_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def get_widget_linegraph(wid):
    widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETLINEGRAPH_B_WID,(wid,))
    if widget_config:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(widget_config[0]['wid'],))
        if row:
            return ormwidget.WidgetLinegraph(wid=row[0]['wid'], uid=row[0]['uid'], widgetname=row[0]['widgetname'], creation_date=row[0]['creation_date'], datapoints=widget_config[0]['datapoints'], colors=widget_config[0]['colors'])
    return None

def get_wids_linegraphs_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETLINEGRAPH_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def get_widget_table(wid):
    widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETTABLE_B_WID,(wid,))
    if widget_config:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(widget_config[0]['wid'],))
        if row:
            return ormwidget.WidgetTable(wid=row[0]['wid'], uid=row[0]['uid'], widgetname=row[0]['widgetname'], creation_date=row[0]['creation_date'], datapoints=widget_config[0]['datapoints'], colors=widget_config[0]['colors'])
    return None

def get_wids_tables_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETTABLE_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def get_widget_multidp(wid):
    widget_config=connection.session.execute(stmtwidget.S_A_MSTWIDGETMULTIDP_B_WID,(wid,))
    if widget_config:
        row=connection.session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(widget_config[0]['wid'],))
        if row:
            return ormwidget.WidgetMultidp(wid=row[0]['wid'], uid=row[0]['uid'], widgetname=row[0]['widgetname'], creation_date=row[0]['creation_date'], datapoints=widget_config[0]['datapoints'],active_visualization=widget_config[0]['active_visualization'])
    return None

def get_wids_multidp_with_pid(pid):
    row=connection.session.execute(stmtwidget.S_WID_MSTWIDGETMULTIDP_B_PID,(pid,))
    if not row:
        return None
    else:
        return [wid['wid'] for wid in row]

def _delete_widget_ds(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETDS_B_WID,(wid,))
    return True

def _insert_widget_ds(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETDS,(widget.wid,widget.did))
    return True

def _delete_widget_dp(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETDP_B_WID,(wid,))
    return True

def _insert_widget_dp(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETDP,(widget.wid,widget.pid))
    return True

def _insert_widget_histogram(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETHISTOGRAM,(widget.wid,widget.datapoints, widget.colors))
    return True

def _delete_widget_histogram(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETHISTOGRAM_B_WID,(wid,))
    return True

def _insert_widget_linegraph(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETLINEGRAPH,(widget.wid, widget.datapoints, widget.colors))
    return True

def _delete_widget_linegraph(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETLINEGRAPH_B_WID,(wid,))
    return True

def _insert_widget_table(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETTABLE,(widget.wid, widget.datapoints, widget.colors))
    return True

def _delete_widget_table(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETTABLE_B_WID,(wid,))
    return True

def _insert_widget_multidp(widget):
    connection.session.execute(stmtwidget.I_A_MSTWIDGETMULTIDP,(widget.wid, widget.active_visualization, widget.datapoints))
    return True

def _delete_widget_multidp(wid):
    connection.session.execute(stmtwidget.D_A_MSTWIDGETMULTIDP_B_WID,(wid,))
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

def add_datapoint_to_multidp(wid, pid):
    multidp=get_widget_multidp(wid=wid)
    if not multidp:
        return False
    multidp.datapoints.add(pid)
    connection.session.execute(stmtwidget.U_PIDS_MSTWIDGETMULTIDP_B_WID,(multidp.datapoints,wid))
    return True

def delete_datapoint_from_multidp(wid, pid):
    connection.session.execute(stmtwidget.D_PID_MSTWIDGETMULTIDP_B_PID_WID,(pid,wid))
    return True

