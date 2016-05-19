'''
Created on 25/09/2015

@author: komlog crew
'''

from komlog.komcass.model.orm import ticket as ormticket
from komlog.komcass.model.statement import ticket as stmtticket
from komlog.komcass import connection


def get_ticket(tid):
    row=connection.session.execute(stmtticket.S_A_AUTHTICKET_B_TID,(tid,))
    if row:
        return ormticket.Ticket(**row[0])
    else:
        return None

def get_tickets_by_uid(uid):
    row=connection.session.execute(stmtticket.S_A_AUTHTICKET_B_UID,(uid,))
    data=[]
    if row:
        for r in row:
            data.append(ormticket.Ticket(**r))
    return data

def get_expired_ticket(tid):
    row=connection.session.execute(stmtticket.S_A_AUTHTICKETEXPIRED_B_TID,(tid,))
    if row:
        return ormticket.Ticket(**row[0])
    else:
        return None

def get_expired_tickets_by_uid(uid):
    row=connection.session.execute(stmtticket.S_A_AUTHTICKETEXPIRED_B_UID,(uid,))
    data=[]
    if row:
        for r in row:
            data.append(ormticket.Ticket(**r))
    return data

def new_ticket(ticket):
    if not isinstance(ticket, ormticket.Ticket):
        return False
    else:
        resp=connection.session.execute(stmtticket.I_A_AUTHTICKET_INE,(ticket.tid,ticket.date,ticket.uid,ticket.expires,ticket.allowed_uids,ticket.allowed_cids,ticket.resources,ticket.permissions,ticket.interval_init,ticket.interval_end))
        return resp[0]['[applied]'] if resp else False

def insert_ticket(ticket):
    if not isinstance(ticket, ormticket.Ticket):
        return False
    else:
        connection.session.execute(stmtticket.I_A_AUTHTICKET,(ticket.tid,ticket.date,ticket.uid,ticket.expires,ticket.allowed_uids,ticket.allowed_cids,ticket.resources,ticket.permissions,ticket.interval_init,ticket.interval_end))
        return True

def insert_expired_ticket(ticket):
    if not isinstance(ticket, ormticket.Ticket):
        return False
    else:
        connection.session.execute(stmtticket.I_A_AUTHTICKETEXPIRED,(ticket.tid,ticket.date,ticket.uid,ticket.expires,ticket.allowed_uids,ticket.allowed_cids,ticket.resources,ticket.permissions,ticket.interval_init,ticket.interval_end))
        return True

def delete_ticket(tid):
    connection.session.execute(stmtticket.D_A_AUTHTICKET_B_TID,(tid,))
    return True

def delete_expired_ticket(tid):
    connection.session.execute(stmtticket.D_A_AUTHTICKETEXPIRED_B_TID,(tid,))
    return True

