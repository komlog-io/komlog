'''
Created on 25/09/2015

@author: komlog crew
'''

from komcass.model.orm import ticket as ormticket
from komcass.model.statement import ticket as stmtticket
from komcass import connection


def get_ticket(tid):
    row=connection.session.execute(stmtticket.S_A_AUTHTICKET_B_TID,(tid,))
    if row:
        return ormticket.Ticket(**row[0])
    else:
        return None

def get_expired_ticket(tid):
    row=connection.session.execute(stmtticket.S_A_AUTHTICKETEXPIRED_B_TID,(tid,))
    if row:
        return ormticket.Ticket(**row[0])
    else:
        return None

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

