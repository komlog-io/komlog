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
    110200:'select * from dat_user_segment_transition where uid=? and date=?',
    110201:'select date,sid,previous_sid from dat_user_segment_transition where uid=?',
    110202:'select date,sid,previous_sid from dat_user_segment_transition where uid=? and date>=? and date<=?',
    110300:'select * from prm_user_segment_allowed_transitions where sid = ?',
    110400:'select * from prm_user_segment_fare where sid = ?',
    115000:'insert into prm_user_segment_quo (sid,quote,value) values (?,?,?)',
    115100:'insert into mst_user_segment (sid,description) values (?,?)',
    115200:'insert into dat_user_segment_transition (uid,date,sid,previous_sid) values (?,?,?,?)',
    115300:'insert into prm_user_segment_allowed_transitions (sid,sids) values (?,?)',
    115400:'insert into prm_user_segment_fare (sid,amount,currency,frequency) values (?,?,?,?)',
    117000:'delete from prm_user_segment_quo where sid=?',
    117001:'delete from prm_user_segment_quo where sid=? and quote=?',
    117100:'delete from mst_user_segment where sid=?',
    117200:'delete from dat_user_segment_transition where uid=?',
    117201:'delete from dat_user_segment_transition where uid=? and date = ?',
    117202:'delete from dat_user_segment_transition where uid=? and date>=? and date<=?',
    117300:'delete from prm_user_segment_allowed_transitions where sid = ?',
    117400:'delete from prm_user_segment_fare where sid = ?',
}

# selects (110000 - 114999)

# prm_user_segment_quo

S_A_PRMUSERSEGMENTQUO_B_SID=110000
S_A_PRMUSERSEGMENTQUO_B_SID_QUOTE=110001

# mst_user_segment

S_A_MSTUSERSEGMENT_B_SID = 110100

# dat_user_segment_transition

S_A_DATUSERSEGMENTTRANSITION_B_UID_DATE = 110200
S_DATESIDPSID_DATUSERSEGMENTTRANSITION_B_UID = 110201
S_DATESIDPSID_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE = 110202

# prm_user_segment_allowed_transitions

S_A_PRMUSERSEGMENTALLOWEDTRANSITIONS_B_SID = 110300

# prm_user_segment_fare

S_A_PRMUSERSEGMENTFARE_B_SID = 110400


# inserts (115000 - 116999)

# prm_user_segment_quo

I_A_PRMUSERSEGMENTQUO=115000

# mst_user_segment

I_A_MSTUSERSEGMENT = 115100

# dat_user_segment_transition

I_A_DATUSERSEGMENTTRANSITION = 115200

# prm_user_segment_allowed_transitions

I_A_PRMUSERSEGMENTALLOWEDTRANSITIONS = 115300

# prm_user_segment_fare

I_A_PRMUSERSEGMENTFARE = 115400


# deletes (117000 - 118999)

# prm_user_segment_quo

D_A_PRMUSERSEGMENTQUO_B_SID=117000
D_QUOTE_PRMUSERSEGMENTQUO_B_SID_QUOTE=117001

# mst_user_segment

D_A_MSTUSERSEGMENT_B_SID = 117100

# dat_user_segment_transition

D_A_DATUSERSEGMENTTRANSITION_B_UID = 117200
D_A_DATUSERSEGMENTTRANSITION_B_UID_DATE = 117201
D_A_DATUSERSEGMENTTRANSITION_B_UID_INITDATE_ENDDATE = 117202

# prm_user_segment_allowed_transitions

D_A_PRMUSERSEGMENTALLOWEDTRANSITIONS_B_SID = 117300

# prm_user_segment_fare

D_A_PRMUSERSEGMENTFARE_B_SID = 117400


# updates (119000 - 119999)

