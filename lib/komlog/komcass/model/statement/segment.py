'''
This file contains the statements to operate with segment tables
Statements range (110000-119999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    110000:'select * from prm_user_segment_quo where sid=?',
    110001:'select * from prm_user_segment_quo where sid=? and quote=?',
    110100:'select * from mst_user_segment where sid=?',
    115000:'insert into prm_user_segment_quo (sid,quote,value) values (?,?,?)',
    115100:'insert into mst_user_segment (sid,description) values (?,?)',
    117000:'delete from prm_user_segment_quo where sid=?',
    117001:'delete from prm_user_segment_quo where sid=? and quote=?',
    117100:'delete from mst_user_segment where sid=?',
}

# selects (110000 - 114999)

# prm_user_segment_quo

S_A_PRMUSERSEGMENTQUO_B_SID=110000
S_A_PRMUSERSEGMENTQUO_B_SID_QUOTE=110001

# mst_user_segment

S_A_MSTUSERSEGMENT_B_SID = 110100

# inserts (115000 - 116999)

# prm_user_segment_quo

I_A_PRMUSERSEGMENTQUO=115000

# mst_user_segment

I_A_MSTUSERSEGMENT = 115100

# deletes (117000 - 118999)

# prm_user_segment_quo

D_A_PRMUSERSEGMENTQUO_B_SID=117000
D_QUOTE_PRMUSERSEGMENTQUO_B_SID_QUOTE=117001

# mst_user_segment

D_A_MSTUSERSEGMENT_B_SID = 117100

# updates (119000 - 119999)

# prm_user_segment_quo

