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
            60100:'select * from quo_agent where aid=?',
            60200:'select * from quo_datasource where did=?',
            60300:'select * from quo_datapoint where pid=?',
            60400:'select * from quo_widget where wid=?',
            60500:'select * from quo_dashboard where bid=?',
            60600:'select * from quo_circle where cid=?',
            65000:'insert into quo_user (uid,quotes) values (?,?)',
            65100:'insert into quo_agent (aid,quotes) values (?,?)',
            65200:'insert into quo_datasource (did,quotes) values (?,?)',
            65300:'insert into quo_datapoint (pid,quotes) values (?,?)',
            65400:'insert into quo_widget (wid,quotes) values (?,?)',
            65500:'insert into quo_dashboard (bid,quotes) values (?,?)',
            65600:'insert into quo_circle (cid,quotes) values (?,?)',
            67000:'delete quotes [?] from quo_user where uid=?',
            67001:'delete from quo_user where uid=?',
            67100:'delete quotes [?] from quo_agent where aid=?',
            67101:'delete from quo_agent where aid=?',
            67200:'delete quotes [?] from quo_datasource where did=?',
            67201:'delete from quo_datasource where did=?',
            67300:'delete quotes [?] from quo_datapoint where pid=?',
            67301:'delete from quo_datapoint where pid=?',
            67400:'delete quotes [?] from quo_widget where wid=?',
            67401:'delete from quo_widget where wid=?',
            67500:'delete quotes [?] from quo_dashboard where bid=?',
            67501:'delete from quo_dashboard where bid=?',
            67600:'delete quotes [?] from quo_circle where cid=?',
            67601:'delete from quo_circle where cid=?',
            69000:'update quo_user set quotes [?] = ? where uid=?',
            69100:'update quo_agent set quotes [?] = ? where aid=?',
            69200:'update quo_datasource set quotes [?] = ? where did=?',
            69300:'update quo_datapoint set quotes [?] = ? where pid=?',
            69400:'update quo_widget set quotes [?] = ? where wid=?',
            69500:'update quo_dashboard set quotes [?] = ? where bid=?',
            69600:'update quo_circle set quotes [?] = ? where cid=?',
           }

# selects (60000 - 64999)

# quo_user

S_A_QUOUSER_B_UID=60000

# quo_agent

S_A_QUOAGENT_B_AID=60100

# quo_datasource

S_A_QUODATASOURCE_B_DID=60200

# quo_datapoint

S_A_QUODATAPOINT_B_PID=60300

# quo_widget

S_A_QUOWIDGET_B_WID=60400

# quo_dashboard

S_A_QUODASHBOARD_B_BID=60500

# quo_circle

S_A_QUOCIRCLE_B_CID=60600

# Inserts (65000 - 66999)


# quo_user

I_A_QUOUSER=65000

# quo_agent

I_A_QUOAGENT=65100

# quo_datasource

I_A_QUODATASOURCE=65200

# quo_datapoint

I_A_QUODATAPOINT=65300

# quo_widget

I_A_QUOWIDGET=65400

# quo_dashboard

I_A_QUODASHBOARD=65500

# quo_circle

I_A_QUOCIRCLE=65600

# Deletes (67000 - 68999)


# quo_user

D_Q_QUOUSER_B_UID=67000
D_A_QUOUSER_B_UID=67001

# quo_agent

D_Q_QUOAGENT_B_AID=67100
D_A_QUOAGENT_B_AID=67101

# quo_datasource

D_Q_QUODATASOURCE_B_DID=67200
D_A_QUODATASOURCE_B_DID=67201

# quo_datapoint

D_Q_QUODATAPOINT_B_PID=67300
D_A_QUODATAPOINT_B_PID=67301

# quo_widget

D_Q_QUOWIDGET_B_WID=67400
D_A_QUOWIDGET_B_WID=67401

# quo_dashboard

D_Q_QUODASHBOARD_B_BID=67500
D_A_QUODASHBOARD_B_BID=67501

# quo_circle

D_Q_QUOCIRCLE_B_CID=67600
D_A_QUOCIRCLE_B_CID=67601

# Updates (69000 - 69999)


# quo_user

U_QUOTE_QUOUSER_B_UID=69000

# quo_agent

U_QUOTE_QUOAGENT_B_AID=69100

# quo_datasource

U_QUOTE_QUODATASOURCE_B_DID=69200

# quo_datapoint

U_QUOTE_QUODATAPOINT_B_PID=69300

# quo_widget

U_QUOTE_QUOWIDGET_B_WID=69400

# quo_dashboard

U_QUOTE_QUODASHBOARD_B_BID=69500

# quo_circle

U_QUOTE_QUOCIRCLE_B_CID=69600

