#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

from komcass.model.orm import interface as ormiface
from komcass.model.statement import interface as stmtiface
from komcass.exception import interface as excpiface


def get_user_iface_deny(session, uid, iface):
    row=session.execute(stmtiface.S_A_IFUSERDENY_B_UID_INTERFACE,(uid,iface))
    if not row:
        return None
    elif len(row)==1:
        return ormiface.UserIfaceDeny(**row[0])
    else:
        raise excpiface.DataConsistencyException(function='get_userifacedeny',field='iface',value=iface)

def get_user_ifaces_deny(session, uid):
    ifaces=[]
    row=session.execute(stmtiface.S_A_IFUSERDENY_B_UID,(uid,))
    ifaces=[]
    if row:
        for iface in row:
            ifaces.append(ormiface.UserIfaceDeny(**iface))
    return ifaces

def insert_user_iface_deny(session, uid, iface, perm):
    session.execute(stmtiface.I_A_IFUSERDENY,(uid,iface,perm))
    return True

def delete_user_iface_deny(session, uid, iface):
    session.execute(stmtiface.D_I_IFUSERDENY_B_UID_IFACE,(uid,iface))
    return True

def delete_user_ifaces_deny(session, uid):
    session.execute(stmtiface.D_I_IFUSERDENY_B_UID,(uid,))
    return True

