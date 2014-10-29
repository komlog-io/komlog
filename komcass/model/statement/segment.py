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
            111000:'insert into prm_user_segment (sid,segmentname,params) values (?,?,?)',
            111001:'insert into prm_user_segment (sid,params) values (?,?)',
            112000:'delete params [?] from prm_user_segment where sid=?',
            112001:'delete from prm_user_segment where sid=?',
            113000:'update prm_user_segment set params [?] = ? where sid=?'
           }

# selects

S_A_PRMUSERSEGMENT_B_SID=110000

# inserts

I_A_PRMUSERSEGMENT=111000
I_PARAMS_PRMUSERSEGMENT_B_PARAMS_SID=111001

# deletes

D_PARAM_PRMUSERSEGMENT_B_PARAM_SID=112000
D_A_PRMUSERSEGMENT_B_SID=112001

# updates

U_PARAM_PRMUSERSEGMENT_B_PARAM_SID=113000
