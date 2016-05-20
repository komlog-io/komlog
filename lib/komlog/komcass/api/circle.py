'''
Created on 10/03/2015

@author: komlog crew
'''

from komlog.komcass.model.orm import circle as ormcircle
from komlog.komcass.model.statement import circle as stmtcircle
from komlog.komcass import connection, exceptions

@exceptions.ExceptionHandler
def get_circle(cid):
    row=connection.session.execute(stmtcircle.S_A_MSTCIRCLE_B_CID,(cid,))
    return ormcircle.Circle(**row[0]) if row else None

@exceptions.ExceptionHandler
def get_circles(uid, type=None):
    if type:
        row=connection.session.execute(stmtcircle.S_A_MSTCIRCLE_B_UID_TYPE,(uid,type))
    else:
        row=connection.session.execute(stmtcircle.S_A_MSTCIRCLE_B_UID,(uid,))
    circles=[]
    if row:
        for c in row:
            circle=ormcircle.Circle(**c)
            circles.append(circle)
    return circles

@exceptions.ExceptionHandler
def get_circles_cids(uid, type=None):
    if type:
        row=connection.session.execute(stmtcircle.S_CID_MSTCIRCLE_B_UID_TYPE,(uid,type))
    else:
        row=connection.session.execute(stmtcircle.S_CID_MSTCIRCLE_B_UID,(uid,))
    cids=[]
    if row:
        for r in row:
            cids.append(r['cid'])
    return cids

@exceptions.ExceptionHandler
def get_number_of_circles(uid,type=None):
    if type:
        row=connection.session.execute(stmtcircle.S_COUNT_MSTCIRCLE_B_UID_TYPE,(uid,type))
    else:
        row=connection.session.execute(stmtcircle.S_COUNT_MSTCIRCLE_B_UID,(uid,))
    return row[0]['count'] if row else 0

@exceptions.ExceptionHandler
def delete_circle(cid):
    row=connection.session.execute(stmtcircle.D_A_MSTCIRCLE_B_CID,(cid,))
    return True

@exceptions.ExceptionHandler
def new_circle(circle):
    if not isinstance(circle, ormcircle.Circle):
        return False
    resp=connection.session.execute(stmtcircle.I_A_MSTCIRCLE_INE,(circle.cid,circle.uid,circle.type,circle.creation_date,circle.circlename,circle.members))
    return resp[0]['[applied]'] if resp else False

@exceptions.ExceptionHandler
def insert_circle(circle):
    if not isinstance(circle, ormcircle.Circle):
        return False
    connection.session.execute(stmtcircle.I_A_MSTCIRCLE,(circle.cid,circle.uid,circle.type,circle.creation_date,circle.circlename,circle.members))
    return True

@exceptions.ExceptionHandler
def add_member_to_circle(cid, member):
    circle=get_circle(cid=cid)
    if not circle:
        return False
    if member in circle.members:
        return True
    circle.members.add(member)
    connection.session.execute(stmtcircle.U_MEMBERS_MSTCIRCLE_B_CID,(circle.members,cid))
    return True

@exceptions.ExceptionHandler
def delete_member_from_circle(cid, member):
    connection.session.execute(stmtcircle.D_MEMBER_MSTCIRCLE_B_MEMBER_CID,(member,cid))
    return True

