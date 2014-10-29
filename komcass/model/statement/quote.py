#coding: utf-8
'''
This file contains the statements to operate with quote tables
Statements range (60000-69999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={60000:'select * from quo_user where uid=?',
            60001:'select * from quo_agent where aid=?',
            60002:'select * from quo_datasource where did=?',
            60003:'select * from quo_datapoint where pid=?',
            60004:'select * from quo_widget where wid=?',
            60005:'select * from quo_dashboard where bid=?',
            61000:'insert into quo_user (uid,quotes) values (?,?)',
            61001:'insert into quo_agent (aid,quotes) values (?,?)',
            61002:'insert into quo_datasource (did,quotes) values (?,?)',
            61003:'insert into quo_datapoint (pid,quotes) values (?,?)',
            61004:'insert into quo_widget (wid,quotes) values (?,?)',
            61005:'insert into quo_dashboard (bid,quotes) values (?,?)',
            62000:'delete quotes [?] from quo_user where uid=?',
            62001:'delete quotes [?] from quo_agent where aid=?',
            62002:'delete quotes [?] from quo_datasource where did=?',
            62003:'delete quotes [?] from quo_datapoint where pid=?',
            62004:'delete quotes [?] from quo_widget where wid=?',
            62005:'delete quotes [?] from quo_dashboard where bid=?',
            62006:'delete from quo_user where uid=?',
            62007:'delete from quo_agent where aid=?',
            62008:'delete from quo_datasource where did=?',
            62009:'delete from quo_datapoint where pid=?',
            62010:'delete from quo_widget where wid=?',
            62011:'delete from quo_dashboard where bid=?',
            63000:'update quo_user set quotes [?] = ? where uid=?',
            63001:'update quo_agent set quotes [?] = ? where aid=?',
            63002:'update quo_datasource set quotes [?] = ? where did=?',
            63003:'update quo_datapoint set quotes [?] = ? where pid=?',
            63004:'update quo_widget set quotes [?] = ? where wid=?',
            63005:'update quo_dashboard set quotes [?] = ? where bid=?'
           }

# selects

S_A_QUOUSER_B_UID=60000
S_A_QUOAGENT_B_AID=60001
S_A_QUODATASOURCE_B_DID=60002
S_A_QUODATAPOINT_B_PID=60003
S_A_QUOWIDGET_B_WID=60004
S_A_QUODASHBOARD_B_BID=60005

# Inserts

I_A_QUOUSER=61000
I_A_QUOAGENT=61001
I_A_QUODATASOURCE=61002
I_A_QUODATAPOINT=61003
I_A_QUOWIDGET=61004
I_A_QUODASHBOARD=61005

# Deletes

D_Q_QUOUSER_B_UID=62000
D_Q_QUOAGENT_B_AID=62001
D_Q_QUODATSOURCE_B_DID=62002
D_Q_QUODATAPOINT_B_PID=62003
D_Q_QUOWIDGET_B_WID=62004
D_Q_QUODASHBOARD_B_BID=62005
D_A_QUOUSER_B_UID=62006
D_A_QUOAGENT_B_AID=62007
D_A_QUODATSOURCE_B_DID=62008
D_A_QUODATAPOINT_B_PID=62009
D_A_QUOWIDGET_B_WID=62010
D_A_QUODASHBOARD_B_BID=62011

# Updates

U_QUOTE_QUOUSER_B_UID=63000
U_QUOTE_QUOAGENT_B_AID=63001
U_QUOTE_QUODATASOURCE_B_DID=63002
U_QUOTE_QUODATAPOINT_B_PID=63003
U_QUOTE_QUOWIDGET_B_WID=63004
U_QUOTE_QUODASHBOARD_B_BID=63005

