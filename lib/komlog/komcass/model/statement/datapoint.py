'''
This file contains the statements to operate with datapoint tables
Statements range (30000-39999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    30000:'select pid,did,uid,datapointname,color,creation_date from mst_datapoint where pid=?',
    30001:'select pid,did,uid,datapointname,color,creation_date from mst_datapoint where did=?',
    30002:'select pid,did,uid,datapointname,color,creation_date from mst_datapoint where uid=?',
    30003:'select count(*) from mst_datapoint where did=?',
    30004:'select count(*) from mst_datapoint where uid=?',
    30005:'select pid from mst_datapoint where did=?',
    30006:'select pid from mst_datapoint where uid=?',
    30100:'select pid,decimal_separator,last_received from mst_datapoint_stats where pid=?',
    30200:'select pid,date,value from dat_datapoint  where pid=? and date=?',
    30201:'select pid,date,value from dat_datapoint where pid=? and date>=? and date<=? limit ?',
    30202:'select pid,date,value from dat_datapoint where pid=? and date>=? and date<=?',
    30203:'select date,value from dat_datapoint where pid=? and date>=? and date<=? limit ?',
    30204:'select date,value from dat_datapoint where pid=? and date>=? and date<=?',
    30300:'select pid,date,position,length from dat_datapoint_dtree_positives where pid=?',
    30301:'select pid,date,position,length from dat_datapoint_dtree_positives where pid=? and date=?',
    30400:'select pid,date,position,length from dat_datapoint_dtree_negatives where pid=?',
    30401:'select pid,date,position,length from dat_datapoint_dtree_negatives where pid=? and date=?',
    30500:'select sid from mst_datapoint_hooks where pid=?',
    35000:'insert into mst_datapoint (pid,did,uid,datapointname,color,creation_date) values (?,?,?,?,?,?)',
    35001:'insert into mst_datapoint (pid,did,uid,datapointname,color,creation_date) values (?,?,?,?,?,?) if not exists',
    35200:'insert into dat_datapoint (pid,date,value) values (?,?,?)',
    35300:'insert into dat_datapoint_dtree_positives (pid, date, position, length) values (?,?,?,?) if not exists',
    35400:'insert into dat_datapoint_dtree_negatives (pid, date, position, length) values (?,?,?,?) if not exists',
    35500:'insert into mst_datapoint_hooks (pid,sid) values (?,?)',
    37000:'delete from mst_datapoint where pid=?',
    37100:'delete from mst_datapoint_stats where pid=?',
    37200:'delete from dat_datapoint where pid=?',
    37201:'delete from dat_datapoint where pid=? and date=?',
    37300:'delete from dat_datapoint_dtree_positives where pid=?',
    37301:'delete from dat_datapoint_dtree_positives where pid=? and date=? if exists',
    37302:'delete from dat_datapoint_dtree_positives where pid=? and date=? if position = ?',
    37400:'delete from dat_datapoint_dtree_negatives where pid=?',
    37401:'delete from dat_datapoint_dtree_negatives where pid=? and date=?',
    37402:'delete from dat_datapoint_dtree_negatives where pid=? and date=? and position = ? if exists',
    37500:'delete from mst_datapoint_hooks where pid=?',
    37501:'delete from mst_datapoint_hooks where pid=? and sid=?',
    39000:'update mst_datapoint set did=? where pid=?',
    39100:'update mst_datapoint_stats set decimal_separator=? where pid=?',
    39102:'update mst_datapoint_stats set last_received=? where pid=?',
    39300:'update dat_datapoint_dtree_positives set position=?,length=? where pid=? and date=?',
    39301:'update dat_datapoint_dtree_positives set position=? where pid=? and date=? if position != ?',
    39302:'update dat_datapoint_dtree_positives set length=? where pid=? and date=? if length != ?',
    39400:'update dat_datapoint_dtree_negatives set length = ? where pid=? and date=? and position = ?',
    39401:'update dat_datapoint_dtree_negatives set length = ? where pid=? and date=? and position = ? if length != ?',
}

# selects (30000 - 34999)

# mst_datapoint

S_A_MSTDATAPOINT_B_PID=30000
S_A_MSTDATAPOINT_B_DID=30001
S_A_MSTDATAPOINT_B_UID=30002
S_COUNT_MSTDATAPOINT_B_DID=30003
S_COUNT_MSTDATAPOINT_B_UID=30004
S_PID_MSTDATAPOINT_B_DID=30005
S_PID_MSTDATAPOINT_B_UID=30006

# mst_datapoint_stats

S_A_MSTDATAPOINTSTATS_B_PID=30100

# dat_datapoint

S_A_DATDATAPOINT_B_PID_DATE=30200
S_A_DATDATAPOINT_B_PID_INITDATE_ENDDATE_COUNT=30201
S_A_DATDATAPOINT_B_PID_INITDATE_ENDDATE=30202
S_DATEVALUE_DATDATAPOINT_B_PID_INITDATE_ENDDATE_COUNT=30203
S_DATEVALUE_DATDATAPOINT_B_PID_INITDATE_ENDDATE=30204

# dat_datapoint_dtree_positives

S_A_DATDATAPOINTDTREEPOSITIVES_B_PID=30300
S_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE=30301

# dat_datapoint_dtree_negatives

S_A_DATDATAPOINTDTREENEGATIVES_B_PID=30400
S_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE=30401

# mst_datapoint_hooks

S_SID_MSTDATAPOINTHOOKS_B_PID   =   30500

# Inserts (35000 - 36999)

# mst_datapoint

I_A_MSTDATAPOINT=35000
I_A_MSTDATAPOINT_INE=35001

# mst_datapoint_stats

# dat_datapoint

I_A_DATDATAPOINT=35200

# dat_datapoint_dtree_positives

I_A_DATDATAPOINTDTREEPOSITIVES_INE = 35300

# dat_datapoint_dtree_negatives

I_A_DATDATAPOINTDTREENEGATIVES_INE = 35400

# mst_datapoint_hooks

I_A_MSTDATAPOINTHOOKS   =   35500

# Deletes (37000 - 38999)

# mst_datapoint

D_A_MSTDATAPOINT_B_PID=37000

# mst_datapoint_stats

D_A_MSTDATAPOINTSTATS_B_PID=37100

# dat_datapoint

D_A_DATDATAPOINT_B_PID=37200
D_A_DATDATAPOINT_B_PID_DATE=37201

# dat_datapoint_stats_dtree_positives

D_A_DATDATAPOINTDTREEPOSITIVES_B_PID=37300
D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_IE=37301
D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_POSITION=37302

# dat_datapoint_stats_dtree_negatives

D_A_DATDATAPOINTDTREENEGATIVES_B_PID=37400
D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE=37401
D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE_POSITION_IE=37402

# mst_datapoint_hooks

D_A_MSTDATAPOINTHOOKS_B_PID     =   37500
D_A_MSTDATAPOINTHOOKS_B_PID_SID =   37501

# Updates (39000 - 39999)

# mst_datapoint

U_DID_MSTDATAPOINT = 39000

# mst_datapoint_stats

U_DECIMALSEPARATOR_MSTDATAPOINTSTATS=39100
U_LASTRECEIVED_MSTDATAPOINTSTATS=39102

# dat_datapoint

# dat_datapoint_dtree_positives

U_POSITIONLENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE=39300
U_POSITION_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_POSITION_INEQ=39301
U_LENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE_LENGTH_INEQ=39302

# dat_datapoint_dtree_negatives

U_LENGTH_DATDATAPOINTDTREENEGATIVES_B_PID_DATE_POSITION=39400
U_LENGTH_DATDATAPOINTDTREENEGATIVES_B_PID_DATE_POSITION_LENGTH_INEQ=39401


