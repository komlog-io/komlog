#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import interface as ormiface
from komcass.model.statement import interface as stmtiface
from komcass.exception import interface as excpiface
from komcass import connection


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

