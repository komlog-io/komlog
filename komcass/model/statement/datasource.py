'''
This file contains the statements to operate with datasource tables
Statements range (20000-29999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={20000:'select * from mst_datasource where did=?',
            20001:'select * from mst_datasource where aid=?',
            20002:'select * from mst_datasource where uid=?',
            20003:'select * from mst_datasource_stats where did=?',
            20004:'select * from dat_datasource where did=? and date=?',
            20005:'select did from mst_datasource where aid=?',
            20006:'select did from mst_datasource where uid=?',
            20007:'select count(*) from mst_datasource where aid=?',
            20008:'select variables from dat_datasource_map where did=? and date=?',
            20009:'select datapoints from dat_datasource_map where did=? and date=?',
            20010:'select * from dat_datasource_map where did=? and date=?',
            20011:'select * from dat_datasource_map where did=? and date>=? and date<=? order by date desc',
            20012:'select * from dat_datasource where did=? and date>=? and date<=? order by date desc',
            20013:'select date from dat_datasource_map where did=? and date>=? and date<=? order by date desc',
            20014:'select * from dat_datasource_text_summary where did=? and date=?',
            20015:'select * from dat_datasource_text_summary where did=? and date>=? and date<=? order by date desc',
            20016:'select * from dat_datasource_novelty_detector_datapoint where did=? and pid=? order by date desc limit 1',
            20017:'select * from dat_datasource_novelty_detector_datapoint where did=? and pid=?',
            21000:'insert into mst_datasource (did,aid,uid,datasourcename,state,creation_date) values (?,?,?,?,?,?)',
            21001:'insert into mst_datasource_stats (did,last_received) values (?,?)',
            21002:'insert into mst_datasource_stats (did,last_mapped) values (?,?)',
            21003:'insert into dat_datasource (did,date,content) values (?,?,?)',
            21004:'insert into dat_datasource_map (did,date,content,variables,datapoints) values (?,?,?,?,?)',
            21005:'insert into dat_datasource_text_summary (did,date,content_length,num_lines, num_words, word_frecuency) values (?,?,?,?,?,?)',
            21006:'insert into dat_datasource_novelty_detector_datapoint (did,pid,date,nd,features) values (?,?,?,?,?)',
            22000:'delete from mst_datasource where did=?',
            22001:'delete from mst_datasource_stats where did=?',
            22002:'delete from dat_datasource where did=?',
            22003:'delete from dat_datasource_map where did=?',
            22004:'delete from dat_datasource where did=? and date=?',
            22005:'delete from dat_datasource_map where did=? and date=?',
            22006:'delete datapoints[?] from dat_datasource_map where did=? and date=?',
            22007:'delete from dat_datasource_text_summary where did=?',
            22008:'delete from dat_datasource_text_summary where did=? and date=?',
            22009:'delete from dat_datasource_novelty_detector_datapoint where did=?',
            22010:'delete from dat_datasource_novelty_detector_datapoint where did=? and pid=?',
            22011:'delete from dat_datasource_novelty_detector_datapoint where did=? and pid=? and date=?',
            23000:'update dat_datasource_map set variables[?]=? where did=? and date=?',
            23001:'update dat_datasource_map set datapoints[?]=? where did=? and date=?'
           }

# selects

S_A_MSTDATASOURCE_B_DID=20000
S_A_MSTDATASOURCE_B_AID=20001
S_A_MSTDATASOURCE_B_UID=20002
S_A_MSTDATASOURCESTATS_B_DID=20003
S_A_DATDATASOURCE_B_DID_DATE=20004
S_DID_MSTDATASOURCE_B_AID=20005
S_DID_MSTDATASOURCE_B_UID=20006
S_COUNT_MSTDATASOURCE_B_AID=20007
S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=20008
S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=20009
S_A_DATDATASOURCEMAP_B_DID_DATE=20010
S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE=20011
S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE=20012
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE=20013
S_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE=20014
S_A_DATDATASOURCETEXTSUMMARY_B_DID_INITDATE_ENDDATE=20015
S_LAST_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=20016
S_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=20017

# Inserts

I_A_MSTDATASOURCE=21000
I_LASTRECEIVED_MSTDATASOURCESTATS_B_DID=21001
I_LASTMAPPED_MSTDATASOURCESTATS_B_DID=21002
I_A_DATDATASOURCE_B_DID_DATE=21003
I_A_DATDATASOURCEMAP_B_DID_DATE=21004
I_A_DATDATASOURCETEXTSUMMARY=21005
I_A_DATDATASOURCENOVELTYDETECTORDATAPOINT=21006

# Deletes

D_A_MSTDATASOURCE_B_DID=22000
D_A_MSTDATASOURCESTATS_B_DID=22001
D_A_DATDATASOURCE_B_DID=22002
D_A_DATDATASOURCEMAP_B_DID=22003
D_A_DATDATASOURCE_B_DID_DATE=22004
D_A_DATDATASOURCEMAP_B_DID_DATE=22005
D_DATAPOINT_DATDATASOURCEMAP_B_PID_DID_DATE=22006
D_A_DATDATASOURCETEXTSUMMARY_B_DID=22007
D_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE=22008
D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID=22009
D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=22010
D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID_DATE=22011

# Updates

U_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=23000
U_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=23001
