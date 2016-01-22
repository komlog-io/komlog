#coding: utf-8
'''
This file contains the statements to operate with segment tables
Statements range (110000-119999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={110000:'select * from prm_user_segment where sid=?',
            115000:'insert into prm_user_segment (sid,segmentname,params) values (?,?,?)',
            115001:'insert into prm_user_segment (sid,params) values (?,?)',
            117000:'delete params [?] from prm_user_segment where sid=?',
            117001:'delete from prm_user_segment where sid=?',
            119000:'update prm_user_segment set params [?] = ? where sid=?'
           }

# selects (110000 - 114999)

# prm_user_segment

S_A_PRMUSERSEGMENT_B_SID=110000

# inserts (115000 - 116999)

# prm_user_segment

I_A_PRMUSERSEGMENT=115000
I_PARAMS_PRMUSERSEGMENT_B_PARAMS_SID=115001

# deletes (117000 - 118999)

# prm_user_segment

D_PARAM_PRMUSERSEGMENT_B_PARAM_SID=117000
D_A_PRMUSERSEGMENT_B_SID=117001

# updates (119000 - 119999)

# prm_user_segment

U_PARAM_PRMUSERSEGMENT_B_PARAM_SID=119000

