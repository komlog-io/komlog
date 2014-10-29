#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import dashboard as ormdashboard
from komcass.model.statement import dashboard as stmtdashboard
from komcass.exception import dashboard as excpdashboard


def get_dashboard(session, bid):
    row=session.execute(stmtdashboard.S_A_MSTDASHBOARD_B_BID,(bid,))
    if not row:
        return None
    elif len(row)==1:
        return ormdashboard.Dashboard(**row[0])
    else:
        raise excpdashboard.ConsistencyDataException(function='get_dashboard',field='bid',value=bid)

def get_dashboards(session, uid):
    row=session.execute(stmtdashboard.S_A_MSTDASHBOARD_B_UID,(uid,))
    dashboards=[]
    if row:
        for d in row:
            dashboards.append(ormdashboard.Dashboard(**d))
    return dashboards

def get_number_of_dashboards_by_uid(session, uid):
    row=session.execute(stmtdashboard.S_COUNT_MSTDASHBOARD_B_UID,(uid,))
    return row[0]['count']

def get_dashboard_widgets(session, bid):
    row=session.execute(stmtdashboard.S_WIDGETS_MSTDASHBOARD_B_BID,(bid,))
    return row[0]['widgets']

def new_dashboard(session, dobj):
    db=session.execute(stmtdashboard.S_A_MSTDASHBOARD_B_BID,(dobj.bid,))
    if db:
        return False
    else:
        session.execute(stmtdashboard.I_A_MSTDASHBOARD,(dobj.bid,dobj.uid,dobj.dashboardname,dobj.creation_date,dobj.widgets))
        return True

def insert_dashboard(session, dobj):
    session.execute(stmtdashboard.I_A_MSTDASHBOARD,(dobj.bid,dobj.uid,dobj.dashboardname,dobj.creation_date,dobj.widgets))
    return True

def delete_dashboard(session, bid):
    session.execute(stmtdashboard.D_A_MSTDASHBOARD_B_BID,(bid,))
    return True

def add_widget_to_dashboard(session, wid, bid):
    widgets=get_dashboard_widgets(session, bid)
    if not widgets:
        widgets={wid}
        session.execute(stmtdashboard.U_WIDGETS_MSTDASHBOARD_B_BID,(widgets,bid))
        return True
    index=widgets.add(wid)
    session.execute(stmtdashboard.U_WIDGETS_MSTDASHBOARD_B_BID,(widgets,bid))
    return True

def delete_widget_from_dashboard(session, wid, bid):
    widgets=get_dashboard_widgets(session, bid)
    if not widgets:
        return True
    try:
        widgets.remove(wid)
    except KeyError:
        return True
    else:
        session.execute(stmtdashboard.U_WIDGETS_MSTDASHBOARD_B_BID,(widgets,bid))
        return True

