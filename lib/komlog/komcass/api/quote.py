#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komfig import logging
from komlog.komcass.model.orm import quote as ormquote
from komlog.komcass.model.statement import quote as stmtquote
from komlog.komcass import connection, exceptions

@exceptions.ExceptionHandler
def get_user_quotes(uid):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUOUSER_B_UID,(uid,))
    if rows:
        for r in rows:
            quotes.append(ormquote.UserQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_user_quote(uid, quote):
    row=connection.session.execute(stmtquote.S_A_QUOUSER_B_UID_QUOTE,(uid,quote))
    if row:
        return ormquote.UserQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_user_quote(uid, quote, value):
    connection.session.execute(stmtquote.I_A_QUOUSER,(uid,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_user_quote(uid, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUOUSER_INE,(uid, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUOUSER_I_VALUE,(n_val,uid,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_user_quote(uid, quote):
    connection.session.execute(stmtquote.D_A_QUOUSER_B_UID_QUOTE,(uid,quote))
    return True

@exceptions.ExceptionHandler
def delete_user_quotes(uid):
    connection.session.execute(stmtquote.D_A_QUOUSER_B_UID,(uid,))
    return True

@exceptions.ExceptionHandler
def get_agent_quotes(aid):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUOAGENT_B_AID,(aid,))
    if rows:
        for r in rows:
            quotes.append(ormquote.AgentQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_agent_quote(aid, quote):
    row=connection.session.execute(stmtquote.S_A_QUOAGENT_B_AID_QUOTE,(aid,quote))
    if row:
        return ormquote.AgentQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_agent_quote(aid, quote, value):
    connection.session.execute(stmtquote.I_A_QUOAGENT,(aid,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_agent_quote(aid, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUOAGENT_INE,(aid, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUOAGENT_I_VALUE,(n_val,aid,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_agent_quote(aid, quote):
    connection.session.execute(stmtquote.D_A_QUOAGENT_B_AID_QUOTE,(aid,quote))
    return True

@exceptions.ExceptionHandler
def delete_agent_quotes(aid):
    connection.session.execute(stmtquote.D_A_QUOAGENT_B_AID,(aid,))
    return True

@exceptions.ExceptionHandler
def get_datasource_quotes(did):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUODATASOURCE_B_DID,(did,))
    if rows:
        for r in rows:
            quotes.append(ormquote.DatasourceQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_datasource_quote(did, quote):
    row=connection.session.execute(stmtquote.S_A_QUODATASOURCE_B_DID_QUOTE,(did,quote))
    if row:
        return ormquote.DatasourceQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_datasource_quote(did, quote, value):
    connection.session.execute(stmtquote.I_A_QUODATASOURCE,(did,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_datasource_quote(did, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUODATASOURCE_INE,(did, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUODATASOURCE_I_VALUE,(n_val,did,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_datasource_quote(did, quote):
    connection.session.execute(stmtquote.D_A_QUODATASOURCE_B_DID_QUOTE,(did,quote))
    return True

@exceptions.ExceptionHandler
def delete_datasource_quotes(did):
    connection.session.execute(stmtquote.D_A_QUODATASOURCE_B_DID,(did,))
    return True

@exceptions.ExceptionHandler
def get_datapoint_quotes(pid):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUODATAPOINT_B_PID,(pid,))
    if rows:
        for r in rows:
            quotes.append(ormquote.DatapointQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_datapoint_quote(pid, quote):
    row=connection.session.execute(stmtquote.S_A_QUODATAPOINT_B_PID_QUOTE,(pid,quote))
    if row:
        return ormquote.DatapointQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_datapoint_quote(pid, quote, value):
    connection.session.execute(stmtquote.I_A_QUODATAPOINT,(pid,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_datapoint_quote(pid, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUODATAPOINT_INE,(pid, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUODATAPOINT_I_VALUE,(n_val,pid,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_datapoint_quote(pid, quote):
    connection.session.execute(stmtquote.D_A_QUODATAPOINT_B_PID_QUOTE,(pid,quote))
    return True

@exceptions.ExceptionHandler
def delete_datapoint_quotes(pid):
    connection.session.execute(stmtquote.D_A_QUODATAPOINT_B_PID,(pid,))
    return True

@exceptions.ExceptionHandler
def get_widget_quotes(wid):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUOWIDGET_B_WID,(wid,))
    if rows:
        for r in rows:
            quotes.append(ormquote.WidgetQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_widget_quote(wid, quote):
    row=connection.session.execute(stmtquote.S_A_QUOWIDGET_B_WID_QUOTE,(wid,quote))
    if row:
        return ormquote.WidgetQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_widget_quote(wid, quote, value):
    connection.session.execute(stmtquote.I_A_QUOWIDGET,(wid,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_widget_quote(wid, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUOWIDGET_INE,(wid, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUOWIDGET_I_VALUE,(n_val,wid,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_widget_quote(wid, quote):
    connection.session.execute(stmtquote.D_A_QUOWIDGET_B_WID_QUOTE,(wid,quote))
    return True

@exceptions.ExceptionHandler
def delete_widget_quotes(wid):
    connection.session.execute(stmtquote.D_A_QUOWIDGET_B_WID,(wid,))
    return True

@exceptions.ExceptionHandler
def get_dashboard_quotes(bid):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUODASHBOARD_B_BID,(bid,))
    if rows:
        for r in rows:
            quotes.append(ormquote.DashboardQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_dashboard_quote(bid, quote):
    row=connection.session.execute(stmtquote.S_A_QUODASHBOARD_B_BID_QUOTE,(bid,quote))
    if row:
        return ormquote.DashboardQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_dashboard_quote(bid, quote, value):
    connection.session.execute(stmtquote.I_A_QUODASHBOARD,(bid,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_dashboard_quote(bid, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUODASHBOARD_INE,(bid, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUODASHBOARD_I_VALUE,(n_val,bid,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_dashboard_quote(bid, quote):
    connection.session.execute(stmtquote.D_A_QUODASHBOARD_B_BID_QUOTE,(bid,quote))
    return True

@exceptions.ExceptionHandler
def delete_dashboard_quotes(bid):
    connection.session.execute(stmtquote.D_A_QUODASHBOARD_B_BID,(bid,))
    return True

@exceptions.ExceptionHandler
def get_circle_quotes(cid):
    quotes=[]
    rows=connection.session.execute(stmtquote.S_A_QUOCIRCLE_B_CID,(cid,))
    if rows:
        for r in rows:
            quotes.append(ormquote.CircleQuo(**r))
    return quotes

@exceptions.ExceptionHandler
def get_circle_quote(cid, quote):
    row=connection.session.execute(stmtquote.S_A_QUOCIRCLE_B_CID_QUOTE,(cid,quote))
    if row:
        return ormquote.CircleQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def set_circle_quote(cid, quote, value):
    connection.session.execute(stmtquote.I_A_QUOCIRCLE,(cid,quote,value))
    return True

@exceptions.ExceptionHandler
def increment_circle_quote(cid, quote, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUOCIRCLE_INE,(cid, quote, value))
    if not resp:
        return False
    elif resp[0]['[applied]'] is True:
        return True
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUOCIRCLE_I_VALUE,(n_val,cid,quote,cur_val))
            if not resp:
                return False
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return False
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return True

@exceptions.ExceptionHandler
def delete_circle_quote(cid, quote):
    connection.session.execute(stmtquote.D_A_QUOCIRCLE_B_CID_QUOTE,(cid,quote))
    return True

@exceptions.ExceptionHandler
def delete_circle_quotes(cid):
    connection.session.execute(stmtquote.D_A_QUOCIRCLE_B_CID,(cid,))
    return True

@exceptions.ExceptionHandler
def get_user_ts_quotes(uid, quote=None, count=None):
    data=[]
    if quote:
        if count:
            rows=connection.session.execute(stmtquote.S_A_QUOTSUSER_B_UID_QUOTE_COUNT, (uid, quote, count))
        else:
            rows=connection.session.execute(stmtquote.S_A_QUOTSUSER_B_UID_QUOTE, (uid, quote))
    else:
        rows=connection.session.execute(stmtquote.S_A_QUOTSUSER_B_UID, (uid,))
    if rows:
        for row in rows:
            data.append(ormquote.UserTsQuo(**row))
    return data

@exceptions.ExceptionHandler
def get_user_ts_quote(uid, quote, ts):
    row=connection.session.execute(stmtquote.S_A_QUOTSUSER_B_UID_QUOTE_TS, (uid, quote, ts))
    if row:
        return ormquote.UserTsQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def get_user_ts_quote_interval(uid, quote, its, ets):
    data=[]
    rows=connection.session.execute(stmtquote.S_A_QUOTSUSER_B_UID_QUOTE_ITS_ETS, (uid, quote, its, ets))
    if rows:
        for row in rows:
            data.append(ormquote.UserTsQuo(**row))
    return data

@exceptions.ExceptionHandler
def get_user_ts_quote_value_sum(uid, quote):
    resp=connection.session.execute(stmtquote.S_SUMVALUE_QUOTSUSER_B_UID_QUOTE, (uid, quote))
    return resp[0]['system.sum(value)'] if resp else None

@exceptions.ExceptionHandler
def insert_user_ts_quote(uid, quote, ts, value):
    connection.session.execute(stmtquote.I_A_QUOTSUSER, (uid, quote, ts, value))
    return True

@exceptions.ExceptionHandler
def new_user_ts_quote(uid, quote, ts, value):
    resp=connection.session.execute(stmtquote.I_A_QUOTSUSER_INE, (uid, quote, ts, value))
    if not resp:
        return False
    else:
        return resp[0]['[applied]']

@exceptions.ExceptionHandler
def delete_user_ts_quotes(uid):
    connection.session.execute(stmtquote.D_A_QUOTSUSER_B_UID, (uid,))
    return True

@exceptions.ExceptionHandler
def delete_user_ts_quote(uid, quote, ts=None):
    if ts:
        connection.session.execute(stmtquote.D_A_QUOTSUSER_B_UID_QUOTE_TS, (uid, quote, ts))
    else:
        connection.session.execute(stmtquote.D_A_QUOTSUSER_B_UID_QUOTE, (uid, quote))
    return True

@exceptions.ExceptionHandler
def delete_user_ts_quote_interval(uid, quote, its, ets):
    connection.session.execute(stmtquote.D_A_QUOTSUSER_B_UID_QUOTE_ITS_ETS, (uid, quote, its, ets))
    return True

@exceptions.ExceptionHandler
def increment_user_ts_quote(uid, quote, ts, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUOTSUSER_INE,(uid, quote, ts, value))
    if not resp:
        return None
    elif resp[0]['[applied]'] is True:
        return value
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUOTSUSER_I_VALUE,(n_val,uid,quote,ts,cur_val))
            if not resp:
                return None
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return None
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return n_val

@exceptions.ExceptionHandler
def get_datasource_ts_quotes(did, quote=None, count=None):
    data=[]
    if quote:
        if count:
            rows=connection.session.execute(stmtquote.S_A_QUOTSDATASOURCE_B_DID_QUOTE_COUNT, (did, quote, count))
        else:
            rows=connection.session.execute(stmtquote.S_A_QUOTSDATASOURCE_B_DID_QUOTE, (did, quote))
    else:
        rows=connection.session.execute(stmtquote.S_A_QUOTSDATASOURCE_B_DID, (did,))
    if rows:
        for row in rows:
            data.append(ormquote.DatasourceTsQuo(**row))
    return data

@exceptions.ExceptionHandler
def get_datasource_ts_quote(did, quote, ts):
    row=connection.session.execute(stmtquote.S_A_QUOTSDATASOURCE_B_DID_QUOTE_TS, (did, quote, ts))
    if row:
        return ormquote.DatasourceTsQuo(**row[0])
    else:
        return None

@exceptions.ExceptionHandler
def get_datasource_ts_quote_interval(did, quote, its, ets):
    data=[]
    rows=connection.session.execute(stmtquote.S_A_QUOTSDATASOURCE_B_DID_QUOTE_ITS_ETS, (did, quote, its, ets))
    if rows:
        for row in rows:
            data.append(ormquote.DatasourceTsQuo(**row))
    return data

@exceptions.ExceptionHandler
def get_datasource_ts_quote_value_sum(did, quote):
    resp=connection.session.execute(stmtquote.S_SUMVALUE_QUOTSDATASOURCE_B_DID_QUOTE, (did, quote))
    return resp[0]['system.sum(value)'] if resp else None

@exceptions.ExceptionHandler
def insert_datasource_ts_quote(did, quote, ts, value):
    connection.session.execute(stmtquote.I_A_QUOTSDATASOURCE, (did, quote, ts, value))
    return True

@exceptions.ExceptionHandler
def new_datasource_ts_quote(did, quote, ts, value):
    resp=connection.session.execute(stmtquote.I_A_QUOTSDATASOURCE_INE, (did, quote, ts, value))
    if not resp:
        return False
    else:
        return resp[0]['[applied]']

@exceptions.ExceptionHandler
def delete_datasource_ts_quotes(did):
    connection.session.execute(stmtquote.D_A_QUOTSDATASOURCE_B_DID, (did,))
    return True

@exceptions.ExceptionHandler
def delete_datasource_ts_quote(did, quote, ts=None):
    if ts:
        connection.session.execute(stmtquote.D_A_QUOTSDATASOURCE_B_DID_QUOTE_TS, (did, quote, ts))
    else:
        connection.session.execute(stmtquote.D_A_QUOTSDATASOURCE_B_DID_QUOTE, (did, quote))
    return True

@exceptions.ExceptionHandler
def delete_datasource_ts_quote_interval(did, quote, its, ets):
    connection.session.execute(stmtquote.D_A_QUOTSDATASOURCE_B_DID_QUOTE_ITS_ETS, (did, quote, its, ets))
    return True

@exceptions.ExceptionHandler
def increment_datasource_ts_quote(did, quote, ts, value):
    ''' we use lightweight transactions to increment quote values '''
    resp=connection.session.execute(stmtquote.I_A_QUOTSDATASOURCE_INE,(did, quote, ts, value))
    if not resp:
        return None
    elif resp[0]['[applied]'] is True:
        return value
    else:
        cur_val = resp[0]['value']
        n_val=cur_val + value
        applied = False
        retries=0
        while applied != True:
            resp=connection.session.execute(stmtquote.U_VALUE_QUOTSDATASOURCE_I_VALUE,(n_val,did,quote,ts,cur_val))
            if not resp:
                return None
            applied=resp[0]['[applied]']
            if not applied:
                if retries>100:
                    return None
                retries+=1
                cur_val=resp[0]['value']
                n_val=cur_val+value
        return n_val

