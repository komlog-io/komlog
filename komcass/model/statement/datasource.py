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
            20003:'select did from mst_datasource where aid=?',
            20004:'select did from mst_datasource where uid=?',
            20005:'select count(*) from mst_datasource where aid=?',
            20100:'select * from mst_datasource_stats where did=?',
            20200:'select * from dat_datasource where did=? and date=?',
            20201:'select * from dat_datasource where did=? and date>=? and date<=? order by date desc',
            20300:'select variables from dat_datasource_map where did=? and date=?',
            20301:'select datapoints from dat_datasource_map where did=? and date=?',
            20302:'select * from dat_datasource_map where did=? and date=?',
            20303:'select * from dat_datasource_map where did=? and date>=? and date<=? order by date desc',
            20304:'select date from dat_datasource_map where did=? and date>=? and date<=? order by date desc',
            20400:'select * from dat_datasource_text_summary where did=? and date=?',
            20401:'select * from dat_datasource_text_summary where did=? and date>=? and date<=? order by date desc',
            20500:'select * from dat_datasource_novelty_detector_datapoint where did=? and pid=? order by date desc limit 1',
            20501:'select * from dat_datasource_novelty_detector_datapoint where did=? and pid=?',
            25000:'insert into mst_datasource (did,aid,uid,datasourcename,state,creation_date) values (?,?,?,?,?,?)',
            25001:'insert into mst_datasource (did,aid,uid,datasourcename,state,creation_date) values (?,?,?,?,?,?) if not exists',
            25100:'insert into mst_datasource_stats (did,last_received) values (?,?)',
            25101:'insert into mst_datasource_stats (did,last_mapped) values (?,?)',
            25200:'insert into dat_datasource (did,date,content) values (?,?,?)',
            25300:'insert into dat_datasource_map (did,date,content,variables,datapoints) values (?,?,?,?,?)',
            25400:'insert into dat_datasource_text_summary (did,date,content_length,num_lines, num_words, word_frecuency) values (?,?,?,?,?,?)',
            25500:'insert into dat_datasource_novelty_detector_datapoint (did,pid,date,nd,features) values (?,?,?,?,?)',
            27000:'delete from mst_datasource where did=?',
            27100:'delete from mst_datasource_stats where did=?',
            27200:'delete from dat_datasource where did=?',
            27201:'delete from dat_datasource where did=? and date=?',
            27300:'delete from dat_datasource_map where did=?',
            27301:'delete from dat_datasource_map where did=? and date=?',
            27302:'delete datapoints[?] from dat_datasource_map where did=? and date=?',
            27400:'delete from dat_datasource_text_summary where did=?',
            27401:'delete from dat_datasource_text_summary where did=? and date=?',
            27500:'delete from dat_datasource_novelty_detector_datapoint where did=?',
            27501:'delete from dat_datasource_novelty_detector_datapoint where did=? and pid=?',
            27502:'delete from dat_datasource_novelty_detector_datapoint where did=? and pid=? and date=?',
            29300:'update dat_datasource_map set variables[?]=? where did=? and date=?',
            29301:'update dat_datasource_map set datapoints[?]=? where did=? and date=?'
           }

# selects (20000 - 24999)

# mst_datasource

S_A_MSTDATASOURCE_B_DID=20000
S_A_MSTDATASOURCE_B_AID=20001
S_A_MSTDATASOURCE_B_UID=20002
S_DID_MSTDATASOURCE_B_AID=20003
S_DID_MSTDATASOURCE_B_UID=20004
S_COUNT_MSTDATASOURCE_B_AID=20005

# mst_datasource_stats

S_A_MSTDATASOURCESTATS_B_DID=20100

# dat_datasource

S_A_DATDATASOURCE_B_DID_DATE=20200
S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE=20201

# dat_datasource_map

S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=20300
S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=20301
S_A_DATDATASOURCEMAP_B_DID_DATE=20302
S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE=20303
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE=20304

# dat_datasource_text_summary

S_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE=20400
S_A_DATDATASOURCETEXTSUMMARY_B_DID_INITDATE_ENDDATE=20401

# dat_datasource_novelty_detector_datapoint


S_LAST_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=20500
S_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=20501

# Inserts (25000 - 26999)

# mst_datasource

I_A_MSTDATASOURCE=25000
I_A_MSTDATASOURCE_INE=25001

# mst_datasource_stats

I_LASTRECEIVED_MSTDATASOURCESTATS_B_DID=25100
I_LASTMAPPED_MSTDATASOURCESTATS_B_DID=25101

# dat_datasource

I_A_DATDATASOURCE_B_DID_DATE=25200

# dat_datasource_map

I_A_DATDATASOURCEMAP_B_DID_DATE=25300

# dat_datasource_text_summary

I_A_DATDATASOURCETEXTSUMMARY=25400

# dat_datasource_novelty_detector_datapoint

I_A_DATDATASOURCENOVELTYDETECTORDATAPOINT=25500

# Deletes (27000 - 28999)

# mst_datasource

D_A_MSTDATASOURCE_B_DID=27000

# mst_datasource_stats

D_A_MSTDATASOURCESTATS_B_DID=27100

# dat_datasource

D_A_DATDATASOURCE_B_DID=27200
D_A_DATDATASOURCE_B_DID_DATE=27201

# dat_datasource_map

D_A_DATDATASOURCEMAP_B_DID=27300
D_A_DATDATASOURCEMAP_B_DID_DATE=27301
D_DATAPOINT_DATDATASOURCEMAP_B_PID_DID_DATE=27302

# dat_datasource_text_summary

D_A_DATDATASOURCETEXTSUMMARY_B_DID=27400
D_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE=27401

# dat_datasource_novelty_detector_datapoint

D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID=27500
D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=27501
D_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID_DATE=27502

# Updates (29000 - 29999)

# mst_datasource

# mst_datasource_stats

# dat_datasource

# dat_datasource_map

U_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=29300
U_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=29301

# dat_datasource_text_summary

# dat_datasource_novelty_detector_datapoint

