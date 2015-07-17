'''
This file contains the statements to operate with event tables
Statements range (150000-159999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
            150000:'select * from dat_user_events where uid=? and date>=? and date<=? order by date desc',
            150001:'select * from dat_user_events where uid=? and date=?',
            150002:'select * from dat_user_events where uid=? and date<=? order by date desc limit ?',
            150003:'select * from dat_user_events where uid=? and date<=? and date>=? order by date desc',
            150004:'select * from dat_user_events where uid=? and date>=? order by date desc',
            151000:'insert into dat_user_events (uid,date,active,priority,type,parameters) values (?,?,?,?,?,?)',
            152000:'delete from dat_user_events where uid=?',
            153000:'update dat_user_events set active=? where uid=? and date=?',
           }

# selects

S_A_DATUSEREVENTS_B_UID_INITDATE_ENDDATE=150000
S_A_DATUSEREVENTS_B_UID_DATE=150001
S_A_DATUSEREVENTS_B_UID_ENDDATE_COUNT=150002
S_A_DATUSEREVENTS_B_UID_ENDDATE_FROMDATE=150003
S_A_DATUSEREVENTS_B_UID_FROMDATE=150004

# Inserts

I_A_DATUSEREVENTS=151000

# Deletes

D_A_DATUSEREVENTS_B_UID=152000

# Updates

U_ACTIVE_DATUSEREVENTS_B_UID_DATE=153000

