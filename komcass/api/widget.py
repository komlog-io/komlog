#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import widget as ormwidget
from komcass.model.statement import widget as stmtwidget
from komcass.model.parametrization import widget as prmwidget
from komcass.exception import widget as excpwidget

def get_widget(session, wid):
    row=session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.Widget(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='get_widget',field='wid',value=wid)

def get_widgets(session, uid):
    row=session.execute(stmtwidget.S_A_MSTWIDGET_B_UID,(uid,))
    widgets=[]
    if row:
        for w in row:
            widget=ormwidget.Widget(**w)
            widgets.append(widget)
    return widgets

def get_number_of_widgets_by_uid(session, uid):
    row=session.execute(stmtwidget.S_COUNT_MSTWIDGET_B_UID,(uid,))
    return row[0]['count']

def delete_widget(session, wid):
    row=session.execute(stmtwidget.S_A_MSTWIDGET_B_WID,(wid,))
    if not row:
        return True
    elif len(row)>1:
        raise excpwidget.DataConsistencyException(function='delete_widget',field='wid',value=wid)
    else:
        widget=ormwidget.Widget(**row[0])
        if widget.type == prmwidget.types.WIDGET_DS:
            _delete_widget_ds(session,wid)
        elif widget.type == prmwidget.types.WIDGET_DP:
            _delete_widget_dp(session,wid)
        session.execute(stmtwidget.D_A_MSTWIDGET_B_WID,(wid,))
        return True

def new_widget(session, widget):
    if widget:
        existingwidget=get_widget(session,widget.wid)
        if existingwidget:
            return False
        session.execute(stmtwidget.I_A_MSTWIDGET,(widget.wid,widget.uid,widget.type))
        if widget.type==prmwidget.types.WIDGET_DS:
            _insert_widget_ds(session, widget)
        elif widget.type==prmwidget.types.WIDGET_DP:
            _insert_widget_dp(session, widget)
        return True
    else:
        return False

def insert_widget(session, widget):
    if widget:
        session.execute(stmtwidget.I_A_MSTWIDGET,(widget.wid,widget.uid,widget.type))
        if widget.type==prmwidget.types.WIDGET_DS:
            _insert_widget_ds(session, widget)
        elif widget.type==prmwidget.types.WIDGET_DP:
            _insert_widget_dp(session, widget)
        return True
    else:
        return False
            
def get_widget_ds(session, wid):
    row=session.execute(stmtwidget.S_A_MSTWIDGETDS_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetDs(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='_get_widget_ds',field='wid',value=wid)

def get_widget_dp(session, wid):
    row=session.execute(stmtwidget.S_A_MSTWIDGETDP_B_WID,(wid,))
    if not row:
        return None
    elif len(row)==1:
        return ormwidget.WidgetDp(**row[0])
    else:
        raise excpwidget.DataConsistencyException(function='_get_widget_dp',field='wid',value=wid)

def _delete_widget_ds(session, wid):
    session.execute(stmtwidget.D_A_MSTWIDGETDS_B_WID,(wid,))
    return True

def _delete_widget_dp(session, wid):
    session.execute(stmtwidget.D_A_MSTWIDGETDP_B_WID,(wid,))
    return True

def _insert_widget_ds(session, widget):
    session.execute(stmtwidget.I_A_MSTWIDGETDS,(widget.wid,widget.uid,widget.creation_date,widget.did))
    return True

def _insert_widget_dp(session, widget):
    session.execute(stmtwidget.I_A_MSTWIDGETDP,(widget.wid,widget.uid,widget.creation_date,widget.pid))
    return True

