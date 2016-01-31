#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import quote as ormquote
from komcass.model.statement import quote as stmtquote
from komcass.exception import quote as excpquote
from komcass import connection

def get_user_quotes(uid):
    row=connection.session.execute(stmtquote.S_A_QUOUSER_B_UID,(uid,))
    if not row:
        return None
    else:
        return ormquote.UserQuo(**row[0])

def set_user_quotes(uid, quotes):
    connection.session.execute(stmtquote.I_A_QUOUSER,(uid,quotes))
    return True

def set_user_quote(uid, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUOUSER_B_UID,(quote,value,uid))
    return True

def delete_user_quote(uid, quote):
    connection.session.execute(stmtquote.D_Q_QUOUSER_B_UID,(quote,uid))
    return True

def delete_user_quotes(uid):
    connection.session.execute(stmtquote.D_A_QUOUSER_B_UID,(uid,))
    return True

def get_agent_quotes(aid):
    row=connection.session.execute(stmtquote.S_A_QUOAGENT_B_AID,(aid,))
    if not row:
        return None
    else:
        return ormquote.AgentQuo(**row[0])

def set_agent_quotes(aid, quotes):
    connection.session.execute(stmtquote.I_A_QUOAGENT,(aid,quotes))
    return True

def set_agent_quote(aid, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUOAGENT_B_AID,(quote,value,aid))
    return True

def delete_agent_quote(aid, quote):
    connection.session.execute(stmtquote.D_Q_QUOAGENT_B_AID,(quote,aid))
    return True

def delete_agent_quotes(aid):
    connection.session.execute(stmtquote.D_A_QUOAGENT_B_AID,(aid,))
    return True

def get_datasource_quotes(did):
    row=connection.session.execute(stmtquote.S_A_QUODATASOURCE_B_DID,(did,))
    if not row:
        return None
    else:
        return ormquote.DatasourceQuo(**row[0])

def set_datasource_quotes(did, quotes):
    connection.session.execute(stmtquote.I_A_QUODATASOURCE,(did,quotes))
    return True

def set_datasource_quote(did, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUODATASOURCE_B_DID,(quote,value,did))
    return True

def delete_datasource_quote(did, quote):
    connection.session.execute(stmtquote.D_Q_QUODATASOURCE_B_DID,(quote,did))
    return True

def delete_datasource_quotes(did):
    connection.session.execute(stmtquote.D_A_QUODATASOURCE_B_DID,(did,))
    return True

def get_datapoint_quotes(pid):
    row=connection.session.execute(stmtquote.S_A_QUODATAPOINT_B_PID,(pid,))
    if not row:
        return None
    else:
        return ormquote.DatapointQuo(**row[0])

def set_datapoint_quotes(pid, quotes):
    connection.session.execute(stmtquote.I_A_QUODATAPOINT,(pid,quotes))
    return True

def set_datapoint_quote(pid, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUODATAPOINT_B_PID,(quote,value,pid))
    return True

def delete_datapoint_quote(pid, quote):
    connection.session.execute(stmtquote.D_Q_QUODATAPOINT_B_PID,(quote,pid))
    return True

def delete_datapoint_quotes(pid):
    connection.session.execute(stmtquote.D_A_QUODATAPOINT_B_PID,(pid,))
    return True

def get_widget_quotes(wid):
    row=connection.session.execute(stmtquote.S_A_QUOWIDGET_B_WID,(wid,))
    if not row:
        return None
    else:
        return ormquote.WidgetQuo(**row[0])

def set_widget_quotes(wid, quotes):
    connection.session.execute(stmtquote.I_A_QUOWIDGET,(wid,quotes))
    return True

def set_widget_quote(wid, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUOWIDGET_B_WID,(quote,value,wid))
    return True

def delete_widget_quote(wid, quote):
    connection.session.execute(stmtquote.D_Q_QUOWIDGET_B_WID,(quote,wid))
    return True

def delete_widget_quotes(wid):
    connection.session.execute(stmtquote.D_A_QUOWIDGET_B_WID,(wid,))
    return True

def get_dashboard_quotes(bid):
    row=connection.session.execute(stmtquote.S_A_QUODASHBOARD_B_BID,(bid,))
    if not row:
        return None
    else:
        return ormquote.DashboardQuo(**row[0])

def set_dashboard_quotes(bid, quotes):
    connection.session.execute(stmtquote.I_A_QUODASHBOARD,(bid,quotes))
    return True

def set_dashboard_quote(bid, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUODASHBOARD_B_BID,(quote,value,bid))
    return True

def delete_dashboard_quote(bid, quote):
    connection.session.execute(stmtquote.D_Q_QUODASHBOARD_B_BID,(quote,bid))
    return True

def delete_dashboard_quotes(bid):
    connection.session.execute(stmtquote.D_A_QUODASHBOARD_B_BID,(bid,))
    return True

def get_circle_quotes(cid):
    row=connection.session.execute(stmtquote.S_A_QUOCIRCLE_B_CID,(cid,))
    if not row:
        return None
    else:
        return ormquote.CircleQuo(**row[0])

def set_circle_quotes(cid, quotes):
    connection.session.execute(stmtquote.I_A_QUOCIRCLE,(cid,quotes))
    return True

def set_circle_quote(cid, quote, value):
    connection.session.execute(stmtquote.U_QUOTE_QUOCIRCLE_B_CID,(quote,value,cid))
    return True

def delete_circle_quote(cid, quote):
    connection.session.execute(stmtquote.D_Q_QUOCIRCLE_B_CID,(quote,cid))
    return True

def delete_circle_quotes(cid):
    connection.session.execute(stmtquote.D_A_QUOCIRCLE_B_CID,(cid,))
    return True

