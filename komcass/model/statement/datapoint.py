'''
This file contains the statements to operate with datapoint tables
Statements range (30000-39999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={30000:'select * from mst_datapoint where pid=?',
            30001:'select * from mst_datapoint where did=?',
            30002:'select * from mst_datapoint_stats where pid=?',
            30003:'select * from dat_datapoint  where pid=? and date=?',
            30004:'select * from dat_datapoint where pid=? and date>=? and date<=? order by date desc limit ?',
            30005:'select * from dat_datapoint_dtree_positives where pid=?',
            30006:'select * from dat_datapoint_dtree_positives where pid=? and date=?',
            30007:'select * from dat_datapoint_dtree_negatives where pid=?',
            30008:'select * from dat_datapoint_dtree_negatives where pid=? and date=?',
            30009:'select count(*) from mst_datapoint where did=?',
            30010:'select pid from mst_datapoint where did=?',
            31000:'insert into mst_datapoint (pid,did,datapointname,color,creation_date) values (?,?,?,?,?)',
            31001:'insert into dat_datapoint (pid,date,value) values (?,?,?)',
            31002:'insert into dat_datapoint_dtree_positives (position,length) values (?,?) where pid=? and date=?',
            32000:'delete from mst_datapoint where pid=?',
            32001:'delete from mst_datapoint_stats where pid=?',
            32002:'delete from dat_datapoint_dtree_positives where pid=?',
            32003:'delete from dat_datapoint_dtree_negatives where pid=?',
            32004:'delete from dat_datapoint where pid=?',
            32005:'delete coordinates[?] from dat_datapoint_dtree_negatives where pid=? and date=?',
            32006:'delete from dat_datapoint_dtree_positives where pid=? and date=?',
            32007:'delete from dat_datapoint_dtree_negatives where pid=? and date=?',
            32008:'delete from dat_datapoint where pid=? and date=?',
            33000:'update dat_datapoint_dtree_negatives set coordinates[?]=? where pid=? and date=?',
            33001:'update mst_datapoint_stats set dtree=? where pid=?',
            33002:'update mst_datapoint_stats set decimal_separator=? where pid=?',
            33003:'update mst_datapoint_stats set last_received=? where pid=?',
            33004:'update dat_datapoint_dtree_positives set position=?,length=? where pid=? and date=?'
           }

# selects

S_A_MSTDATAPOINT_B_PID=30000
S_A_MSTDATAPOINT_B_DID=30001
S_A_MSTDATAPOINTSTATS_B_PID=30002
S_A_DATDATAPOINT_B_PID_DATE=30003
S_A_DATDATAPOINT_B_PID_INITDATE_ENDDATE_NUMREGS=30004
S_A_DATDATAPOINTDTREEPOSITIVES_B_PID=30005
S_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE=30006
S_A_DATDATAPOINTDTREENEGATIVES_B_PID=30007
S_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE=30008
S_COUNT_MSTDATAPOINT_B_DID=30009
S_PID_MSTDATAPOINT_B_DID=30010

# Inserts

I_A_MSTDATAPOINT=31000
I_A_DATDATAPOINT=31001

# Deletes

D_A_MSTDATAPOINT_B_PID=32000
D_A_MSTDATAPOINTSTATS_B_PID=32001
D_A_DATDATAPOINTDTREEPOSITIVES_B_PID=32002
D_A_DATDATAPOINTDTREENEGATIVES_B_PID=32003
D_A_DATDATAPOINT_B_PID=32004
D_R_DATDATAPOINTDTREENEGATIVES_B_POS_PID_DATE=32005
D_A_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE=32006
D_A_DATDATAPOINTDTREENEGATIVES_B_PID_DATE=32007
D_A_DATDATAPOINT_B_PID_DATE=32008

# Updates

U_R_DATDATAPOINTDTREENEGATIVES_B_POS_LEN_PID_DATE=33000
U_DTREE_MSTDATAPOINTSTATS=33001
U_DECIMALSEPARATOR_MSTDATAPOINTSTATS=33002
U_LASTRECEIVED_MSTDATAPOINTSTATS=33003
U_POSITIONLENGTH_DATDATAPOINTDTREEPOSITIVES_B_PID_DATE=33004


