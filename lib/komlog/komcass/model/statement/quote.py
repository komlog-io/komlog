'''
This file contains the statements to operate with quote tables
Statements range (60000-69999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    60000:'select * from quo_user where uid=?',
    60001:'select * from quo_user where uid=? and quote=?',
    60100:'select * from quo_agent where aid=?',
    60101:'select * from quo_agent where aid=? and quote=?',
    60200:'select * from quo_datasource where did=?',
    60201:'select * from quo_datasource where did=? and quote=?',
    60300:'select * from quo_datapoint where pid=?',
    60301:'select * from quo_datapoint where pid=? and quote=?',
    60400:'select * from quo_widget where wid=?',
    60401:'select * from quo_widget where wid=? and quote=?',
    60500:'select * from quo_dashboard where bid=?',
    60501:'select * from quo_dashboard where bid=? and quote=?',
    60600:'select * from quo_circle where cid=?',
    60601:'select * from quo_circle where cid=? and quote=?',
    65000:'insert into quo_user (uid,quote,value) values (?,?,?)',
    65001:'insert into quo_user (uid,quote,value) values (?,?,?) if not exists',
    65100:'insert into quo_agent (aid,quote,value) values (?,?,?)',
    65101:'insert into quo_agent (aid,quote,value) values (?,?,?) if not exists',
    65200:'insert into quo_datasource (did,quote,value) values (?,?,?)',
    65201:'insert into quo_datasource (did,quote,value) values (?,?,?) if not exists',
    65300:'insert into quo_datapoint (pid,quote,value) values (?,?,?)',
    65301:'insert into quo_datapoint (pid,quote,value) values (?,?,?) if not exists',
    65400:'insert into quo_widget (wid,quote,value) values (?,?,?)',
    65401:'insert into quo_widget (wid,quote,value) values (?,?,?) if not exists',
    65500:'insert into quo_dashboard (bid,quote,value) values (?,?,?)',
    65501:'insert into quo_dashboard (bid,quote,value) values (?,?,?) if not exists',
    65600:'insert into quo_circle (cid,quote,value) values (?,?,?)',
    65601:'insert into quo_circle (cid,quote,value) values (?,?,?) if not exists',
    67000:'delete from quo_user where uid=?',
    67001:'delete from quo_user where uid=? and quote=?',
    67100:'delete from quo_agent where aid=?',
    67101:'delete from quo_agent where aid=? and quote=?',
    67200:'delete from quo_datasource where did=?',
    67201:'delete from quo_datasource where did=? and quote=?',
    67300:'delete from quo_datapoint where pid=?',
    67301:'delete from quo_datapoint where pid=? and quote=?',
    67400:'delete from quo_widget where wid=?',
    67401:'delete from quo_widget where wid=? and quote=?',
    67500:'delete from quo_dashboard where bid=?',
    67501:'delete from quo_dashboard where bid=? and quote=?',
    67600:'delete from quo_circle where cid=?',
    67601:'delete from quo_circle where cid=? and quote=?',
    69000:'update quo_user set value=? where uid=? and quote=? if value=?',
    69100:'update quo_agent set value=? where aid=? and quote=? if value=?',
    69200:'update quo_datasource set value=? where did=? and quote=? if value=?',
    69300:'update quo_datapoint set value=? where pid=? and quote=? if value=?',
    69400:'update quo_widget set value=? where wid=? and quote=? if value=?',
    69500:'update quo_dashboard set value=? where bid=? and quote=? if value=?',
    69600:'update quo_circle set value=? where cid=? and quote=? if value=?',
}

# selects (60000 - 64999)

# quo_user

S_A_QUOUSER_B_UID=60000
S_A_QUOUSER_B_UID_QUOTE=60001

# quo_agent

S_A_QUOAGENT_B_AID=60100
S_A_QUOAGENT_B_AID_QUOTE=60101

# quo_datasource

S_A_QUODATASOURCE_B_DID=60200
S_A_QUODATASOURCE_B_DID_QUOTE=60201

# quo_datapoint

S_A_QUODATAPOINT_B_PID=60300
S_A_QUODATAPOINT_B_PID_QUOTE=60301

# quo_widget

S_A_QUOWIDGET_B_WID=60400
S_A_QUOWIDGET_B_WID_QUOTE=60401

# quo_dashboard

S_A_QUODASHBOARD_B_BID=60500
S_A_QUODASHBOARD_B_BID_QUOTE=60501

# quo_circle

S_A_QUOCIRCLE_B_CID=60600
S_A_QUOCIRCLE_B_CID_QUOTE=60601

# Inserts (65000 - 66999)


# quo_user

I_A_QUOUSER=65000
I_A_QUOUSER_INE=65001

# quo_agent

I_A_QUOAGENT=65100
I_A_QUOAGENT_INE=65101

# quo_datasource

I_A_QUODATASOURCE=65200
I_A_QUODATASOURCE_INE=65201

# quo_datapoint

I_A_QUODATAPOINT=65300
I_A_QUODATAPOINT_INE=65301

# quo_widget

I_A_QUOWIDGET=65400
I_A_QUOWIDGET_INE=65401

# quo_dashboard

I_A_QUODASHBOARD=65500
I_A_QUODASHBOARD_INE=65501

# quo_circle

I_A_QUOCIRCLE=65600
I_A_QUOCIRCLE_INE=65601

# Deletes (67000 - 68999)


# quo_user

D_A_QUOUSER_B_UID=67000
D_A_QUOUSER_B_UID_QUOTE=67001

# quo_agent

D_A_QUOAGENT_B_AID=67100
D_A_QUOAGENT_B_AID_QUOTE=67101

# quo_datasource

D_A_QUODATASOURCE_B_DID=67200
D_A_QUODATASOURCE_B_DID_QUOTE=67201

# quo_datapoint

D_A_QUODATAPOINT_B_PID=67300
D_A_QUODATAPOINT_B_PID_QUOTE=67301

# quo_widget

D_A_QUOWIDGET_B_WID=67400
D_A_QUOWIDGET_B_WID_QUOTE=67401

# quo_dashboard

D_A_QUODASHBOARD_B_BID=67500
D_A_QUODASHBOARD_B_BID_QUOTE=67501

# quo_circle

D_A_QUOCIRCLE_B_CID=67600
D_A_QUOCIRCLE_B_CID_QUOTE=67601

# Updates (69000 - 69999)


# quo_user

U_VALUE_QUOUSER_I_VALUE=69000

# quo_agent

U_VALUE_QUOAGENT_I_VALUE=69100

# quo_datasource

U_VALUE_QUODATASOURCE_I_VALUE=69200

# quo_datapoint

U_VALUE_QUODATAPOINT_I_VALUE=69300

# quo_widget

U_VALUE_QUOWIDGET_I_VALUE=69400

# quo_dashboard

U_VALUE_QUODASHBOARD_I_VALUE=69500

# quo_circle

U_VALUE_QUOCIRCLE_I_VALUE=69600

