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
            105000:'insert into mst_dashboard (bid,uid,dashboardname,creation_date,widgets) values (?,?,?,?,?)',
            105001:'insert into mst_dashboard (bid,uid,dashboardname,creation_date,widgets) values (?,?,?,?,?) if not exists',
            107000:'delete from mst_dashboard where bid=?',
            107001:'delete widgets[?] from mst_dashboard where bid=?',
            109000:'update mst_dashboard set widgets=? where bid=?',
           }

# selects (100000 - 104999)

# mst_dashboard

S_A_MSTDASHBOARD_B_BID=100000
S_A_MSTDASHBOARD_B_UID=100001
S_COUNT_MSTDASHBOARD_B_UID=100002
S_WIDGETS_MSTDASHBOARD_B_BID=100003
S_BID_MSTDASHBOARD_B_UID=100004

# Inserts (105000 - 106999)

# mst_dashboard

I_A_MSTDASHBOARD=105000
I_A_MSTDASHBOARD_INE=105001

# Deletes (107000 - 108999)

# mst_dashboard

D_A_MSTDASHBOARD_B_BID=107000
D_WID_MSTDASHBOARD_B_WID_BID=107001

# Updates (109000 - 109999)

# mst_dashboard

U_WIDGETS_MSTDASHBOARD_B_BID=109000


