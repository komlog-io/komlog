#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komlog.komcass.model.orm import interface as ormiface
from komlog.komcass.model.statement import interface as stmtiface
from komlog.komcass.exception import interface as excpiface
from komlog.komcass import connection


def get_user_iface_deny(uid, iface):
    row=connection.session.execute(stmtiface.S_A_IFUSERDENY_B_UID_INTERFACE,(uid,iface))
    if not row:
        return None
    else:
        return ormiface.UserIfaceDeny(**row[0])

def get_user_ifaces_deny(uid):
    ifaces=[]
    row=connection.session.execute(stmtiface.S_A_IFUSERDENY_B_UID,(uid,))
    ifaces=[]
    if row:
        for iface in row:
            ifaces.append(ormiface.UserIfaceDeny(**iface))
    return ifaces

def insert_user_iface_deny(uid, iface, perm):
    connection.session.execute(stmtiface.I_A_IFUSERDENY,(uid,iface,perm))
    return True

def delete_user_iface_deny(uid, iface):
    connection.session.execute(stmtiface.D_I_IFUSERDENY_B_UID_IFACE,(uid,iface))
    return True

def delete_user_ifaces_deny(uid):
    connection.session.execute(stmtiface.D_I_IFUSERDENY_B_UID,(uid,))
    return True

def get_user_ts_ifaces_deny(uid, iface=None):
    data=[]
    if iface:
        rows=connection.session.execute(stmtiface.S_A_IFTSUSERDENY_B_UID_INTERFACE, (uid, iface))
    else:
        rows=connection.session.execute(stmtiface.S_A_IFTSUSERDENY_B_UID, (uid,))
    if rows:
        for row in rows:
            data.append(ormiface.UserIfaceTsDeny(**row))
    return data

def get_user_ts_iface_deny(uid, iface, ts):
    row=connection.session.execute(stmtiface.S_A_IFTSUSERDENY_B_UID_INTERFACE_TS, (uid, iface, ts))
    if row:
        return ormiface.UserIfaceTsDeny(**row[0])
    else:
        return None

def get_user_ts_iface_deny_interval(uid, iface, its, ets):
    data=[]
    rows=connection.session.execute(stmtiface.S_A_IFTSUSERDENY_B_UID_INTERFACE_ITS_ETS, (uid, iface, its, ets))
    if rows:
        for row in rows:
            data.append(ormiface.UserIfaceTsDeny(**row))
    return data

def insert_user_ts_iface_deny(uid, iface, ts, perm):
    connection.session.execute(stmtiface.I_A_IFTSUSERDENY, (uid, iface, ts, perm))
    return True

def new_user_ts_iface_deny(uid, iface, ts, perm):
    resp=connection.session.execute(stmtiface.I_A_IFTSUSERDENY_INE, (uid, iface, ts, perm))
    if not resp:
        return False
    else:
        return resp[0]['[applied]']

def delete_user_ts_ifaces_deny(uid):
    connection.session.execute(stmtiface.D_A_IFTSUSERDENY_B_UID, (uid,))
    return True

def delete_user_ts_iface_deny(uid, iface, ts=None):
    if ts:
        connection.session.execute(stmtiface.D_A_IFTSUSERDENY_B_UID_INTERFACE_TS, (uid, iface, ts))
    else:
        connection.session.execute(stmtiface.D_A_IFTSUSERDENY_B_UID_INTERFACE, (uid, iface))
    return True

def delete_user_ts_iface_deny_interval(uid, iface, its, ets):
    connection.session.execute(stmtiface.D_A_IFTSUSERDENY_B_UID_INTERFACE_ITS_ETS, (uid, iface, its, ets))
    return True

