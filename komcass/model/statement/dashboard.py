#coding: utf-8
'''
This file contains the statements to operate with dashboard tables
Statements range (100000-109999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={100000:'select * from mst_dashboard where bid=?',
            100001:'select * from mst_dashboard where uid=?',
            100002:'select count(*) from mst_dashboard where uid=?',
            100003:'select widgets from mst_dashboard where bid=?',
            100004:'select bid from mst_dashboard where uid=?',
            101000:'insert into mst_dashboard (bid,uid,dashboardname,creation_date,widgets) values (?,?,?,?,?)',
            102000:'delete from mst_dashboard where bid=?',
            102001:'delete widgets[?] from mst_dashboard where bid=?',
            103000:'update mst_dashboard set widgets=? where bid=?',
           }

# selects

S_A_MSTDASHBOARD_B_BID=100000
S_A_MSTDASHBOARD_B_UID=100001
S_COUNT_MSTDASHBOARD_B_UID=100002
S_WIDGETS_MSTDASHBOARD_B_BID=100003
S_BID_MSTDASHBOARD_B_UID=100004

# Inserts

I_A_MSTDASHBOARD=101000

# Deletes

D_A_MSTDASHBOARD_B_BID=102000
D_WID_MSTDASHBOARD_B_WID_BID=102001

# Updates

U_WIDGETS_MSTDASHBOARD_B_BID=103000


