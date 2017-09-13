'''
This file contains the statements to operate with datasource tables
Statements range (20000-29999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    20000:'select did,aid,uid,datasourcename,creation_date from mst_datasource where did=?',
    20001:'select did,aid,uid,datasourcename,creation_date from mst_datasource where aid=?',
    20002:'select did,aid,uid,datasourcename,creation_date from mst_datasource where uid=?',
    20003:'select did from mst_datasource where aid=?',
    20004:'select did from mst_datasource where uid=?',
    20005:'select count(*) from mst_datasource where aid=?',
    20100:'select did,last_received,last_mapped from mst_datasource_stats where did=?',
    20200:'select did,date,content from dat_datasource where did=? and date=?',
    20201:'select did,date,content from dat_datasource where did=? and date>=? and date<=? limit ?',
    20202:'select did,date,content from dat_datasource where did=? and date>=? and date<=?',
    20203:'select did,date,content from dat_datasource where did=? and date>=? limit ?',
    20204:'select did,date,content from dat_datasource where did=? and date>=?',
    20205:'select did,date,content from dat_datasource where did=? and date<=? limit ?',
    20206:'select did,date,content from dat_datasource where did=? and date<=?',
    20207:'select did,date,content from dat_datasource where did=? limit ?',
    20208:'select did,date,content from dat_datasource where did=?',
    20300:'select variables from dat_datasource_map where did=? and date=?',
    20301:'select datapoints from dat_datasource_map where did=? and date=?',
    20302:'select date from dat_datasource_map where did=? and date>=? and date<=?',
    20303:'select did,date,variables,datapoints from dat_datasource_map where did=? and date=?',
    20304:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=? and date<=? limit ?',
    20305:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=? and date<=?',
    20306:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=? limit ?',
    20307:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=?',
    20308:'select did,date,variables,datapoints from dat_datasource_map where did=? and date<=? limit ?',
    20309:'select did,date,variables,datapoints from dat_datasource_map where did=? and date<=?',
    20310:'select did,date,variables,datapoints from dat_datasource_map where did=? limit ?',
    20311:'select did,date,variables,datapoints from dat_datasource_map where did=?',
    20400:'select did,date,content_length,num_lines,num_words,word_frecuency from dat_datasource_text_summary where did=? and date=?',
    20401:'select did,date,content_length,num_lines,num_words,word_frecuency from dat_datasource_text_summary where did=? and date>=? and date<=?',
    20500:'select did,pid,date,nd,features from dat_datasource_novelty_detector_datapoint where did=? and pid=? limit 1',
    20501:'select did,pid,date,nd,features from dat_datasource_novelty_detector_datapoint where did=? and pid=?',
    20600:'select did,date,content from dat_datasource_hash where did=? and date=?',
    20601:'select did,date,content from dat_datasource_hash where did=? and date>=? and date<=?',
    20602:'select did,date,content from dat_datasource_hash where did=? and date>=? and date<=? limit ?',
    20700:'select did,date,size from dat_datasource_metadata where did=? and date=?',
    20701:'select size from dat_datasource_metadata where did=? and date=?',
    20702:'select did,date,size from dat_datasource_metadata where did=? and date>=? and date<=?',
    20703:'select did,date,size from dat_datasource_metadata where did=? and date>=? and date<=? limit ?',
    20800:'select sid from mst_datasource_hooks where did=?',
    20900:'select did,date,supplies from dat_datasource_supplies where did=? and date=?',
    20901:'select did,date,supplies from dat_datasource_supplies where did=? and date>=? and date<=?',
    20902:'select did,date,supplies from dat_datasource_supplies where did=? limit ?',
    21000:'select did,date,features from dat_datasource_features where did=? and date=?',
    21001:'select date,features from dat_datasource_features where did=? limit ?',
    21100:'select features from mst_datasource_features where did=?',
    21150:'select features from mst_datasource_supply_features where did=? and supply=?',
    21200:'select supplies from mst_datasource_supplies_guessed where did=?',
    21300:'select did from mst_datasource_by_feature where feature=? limit ?',
    21400:'select did from mst_datasource_by_supply_feature where feature=? and supply=? limit ?',
    25000:'insert into mst_datasource (did,aid,uid,datasourcename,creation_date) values (?,?,?,?,?)',
    25001:'insert into mst_datasource (did,aid,uid,datasourcename,creation_date) values (?,?,?,?,?) if not exists',
    25100:'insert into mst_datasource_stats (did,last_received) values (?,?)',
    25101:'insert into mst_datasource_stats (did,last_mapped) values (?,?)',
    25200:'insert into dat_datasource (did,date,content) values (?,?,?)',
    25300:'insert into dat_datasource_map (did,date,variables,datapoints) values (?,?,?,?)',
    25400:'insert into dat_datasource_text_summary (did,date,content_length,num_lines, num_words, word_frecuency) values (?,?,?,?,?,?)',
    25500:'insert into dat_datasource_novelty_detector_datapoint (did,pid,date,nd,features) values (?,?,?,?,?)',
    25600:'insert into dat_datasource_hash (did,date,content) values (?,?,?)',
    25700:'insert into dat_datasource_metadata (did,date,size) values (?,?,?)',
    25800:'insert into mst_datasource_hooks (did,sid) values (?,?)',
    25900:'insert into dat_datasource_supplies (did,date,supplies) values (?,?,?)',
    26000:'insert into dat_datasource_features (did,date,features) values (?,?,?)',
    26100:'insert into mst_datasource_features (did,features) values (?,?)',
    26150:'insert into mst_datasource_supply_features (did,supply,features) values (?,?,?)',
    26200:'insert into mst_datasource_supplies_guessed (did,supplies) values (?,?)',
    26300:'insert into mst_datasource_by_feature (feature, did) values (?,?)',
    26400:'insert into mst_datasource_by_supply_feature (feature, supply, did) values (?,?,?)',
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
    27600:'delete from dat_datasource_hash where did=? and date=?',
    27601:'delete from dat_datasource_hash where did=?',
    27700:'delete from dat_datasource_metadata where did=?',
    27701:'delete from dat_datasource_metadata where did=? and date=?',
    27800:'delete from mst_datasource_hooks where did=?',
    27801:'delete from mst_datasource_hooks where did=? and sid=?',
    27900:'delete from dat_datasource_supplies where did=?',
    27901:'delete from dat_datasource_supplies where did=? and date=?',
    28000:'delete from dat_datasource_features where did=?',
    28001:'delete from dat_datasource_features where did=? and date=?',
    28100:'delete from mst_datasource_features where did=?',
    28150:'delete from mst_datasource_supply_features where did=?',
    28151:'delete from mst_datasource_supply_features where did=? and supply=?',
    28200:'delete from mst_datasource_supplies_guessed where did=?',
    28300:'delete from mst_datasource_by_feature where feature=? and did=?',
    28400:'delete from mst_datasource_by_supply_feature where feature=? and supply=? and did=?',
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
S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE_COUNT=20201
S_A_DATDATASOURCE_B_DID_INITDATE_ENDDATE=20202
S_A_DATDATASOURCE_B_DID_INITDATE_COUNT=20203
S_A_DATDATASOURCE_B_DID_INITDATE=20204
S_A_DATDATASOURCE_B_DID_ENDDATE_COUNT=20205
S_A_DATDATASOURCE_B_DID_ENDDATE=20206
S_A_DATDATASOURCE_B_DID_COUNT=20207
S_A_DATDATASOURCE_B_DID=20208

# dat_datasource_map

S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=20300
S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=20301
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE=20302
S_A_DATDATASOURCEMAP_B_DID_DATE=20303
S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE_COUNT=20304
S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE=20305
S_A_DATDATASOURCEMAP_B_DID_INITDATE_COUNT=20306
S_A_DATDATASOURCEMAP_B_DID_INITDATE=20307
S_A_DATDATASOURCEMAP_B_DID_ENDDATE_COUNT=20308
S_A_DATDATASOURCEMAP_B_DID_ENDDATE=20309
S_A_DATDATASOURCEMAP_B_DID_COUNT=20310
S_A_DATDATASOURCEMAP_B_DID=20311

# dat_datasource_text_summary

S_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE=20400
S_A_DATDATASOURCETEXTSUMMARY_B_DID_INITDATE_ENDDATE=20401

# dat_datasource_novelty_detector_datapoint

S_LAST_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=20500
S_A_DATDATASOURCENOVELTYDETECTORDATAPOINT_B_DID_PID=20501

# dat_datasource_hash

S_A_DATDATASOURCEHASH_B_DID_DATE=20600
S_A_DATDATASOURCEHASH_B_DID_INITDATE_ENDDATE=20601
S_A_DATDATASOURCEHASH_B_DID_INITDATE_ENDDATE_COUNT=20602

# dat_datasource_metadata

S_A_DATDATASOURCEMETADATA_B_DID_DATE=20700
S_SIZE_DATDATASOURCEMETADATA_B_DID_DATE=20701
S_A_DATDATASOURCEMETADATA_B_DID_INITDATE_ENDDATE=20702
S_A_DATDATASOURCEMETADATA_B_DID_INITDATE_ENDDATE_COUNT=20703

# mst_datasource_hooks

S_SID_MSTDATASOURCEHOOKS_B_DID  =   20800

# dat_datasource_supplies

S_A_DATDATASOURCESUPPLIES_B_DID_DATE                =   20900
S_A_DATDATASOURCESUPPLIES_B_DID_INITDATE_ENDDATE    =   20901
S_A_DATDATASOURCESUPPLIES_B_DID_COUNT               =   20902

# dat_datasource_features

S_A_DATDATASOURCEFEATURES_B_DID_DATE                =   21000
S_DATEFEATURES_DATDATASOURCEFEATURES_B_DID_COUNT    =   21001

# mst_datasource_features

S_FEATURES_MSTDATASOURCEFEATURES_B_DID              =   21100

# mst_datasource_supply_features

S_FEATURES_MSTDATASOURCESUPPLYFEATURES_B_DID_SUPPLY =   21150
# mst_datasource_supplies_guessed

S_SUPPLIES_MSTDATASOURCESUPPLIESGUESSED_B_DID       =   21200

# mst_datasource_by_feature

S_DID_MSTDATASOURCEBYFEATURE_B_FEATURE_COUNT        =   21300

# mst_datasource_by_supply_feature

S_DID_MSTDATASOURCEBYSUPPLYFEATURE_B_FEATURE_SUPPLY_COUNT   =   21400

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

# dat_datasource_hash

I_A_DATDATASOURCEHASH=25600

# dat_datasource_metadata

I_A_DATDATASOURCEMETADATA=25700

# mst_datasource_hooks

I_A_MSTDATASOURCEHOOKS  =   25800

# dat_datasource_supplies

I_A_DATDATASOURCESUPPLIES   =   25900

# dat_datasource_features

I_A_DATDATASOURCEFEATURES   =   26000

# mst_datasource_features

I_A_MSTDATASOURCEFEATURES   =   26100

# mst_datasource_supply_features

I_A_MSTDATASOURCESUPPLYFEATURES   =   26150

# mst_datasource_supplies_guessed

I_A_MSTDATASOURCESUPPLIESGUESSED    = 26200

# mst_datasource_by_feature

I_A_MSTDATASOURCEBYFEATURE  =   26300

# mst_datasource_by_supply_feature

I_A_MSTDATASOURCEBYSUPPLYFEATURE    = 26400

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

# dat_datasource_hash

D_A_DATDATASOURCEHASH_B_DID_DATE=27600
D_A_DATDATASOURCEHASH_B_DID=27601

# dat_datasource_metadata

D_A_DATDATASOURCEMETADATA_B_DID=27700
D_A_DATDATASOURCEMETADATA_B_DID_DATE=27701

# mst_datasource_hooks

D_A_MSTDATASOURCEHOOKS_B_DID        =   27800
D_A_MSTDATASOURCEHOOKS_B_DID_SID    =   27801

# dat_datasource_supplies

D_A_DATDATASOURCESUPPLIES_B_DID     =   27900
D_A_DATDATASOURCESUPPLIES_B_DID_DATE=   27901

# dat_datasource_features

D_A_DATDATASOURCEFEATURES_B_DID     =   28000
D_A_DATDATASOURCEFEATURES_B_DID_DATE=   28001

# mst_datasource_features

D_A_MSTDATASOURCEFEATURES_B_DID     =   28100

# mst_datasource_supply_features

D_A_MSTDATASOURCESUPPLYFEATURES_B_DID       = 28150
D_A_MSTDATASOURCESUPPLYFEATURES_B_DID_SUPPLY= 28151

# mst_datasource_supplies_guessed

D_A_MSTDATASOURCESUPPLIESGUESSED_B_DID      = 28200

# mst_datasource_by_feature

D_A_MSTDATASOURCEBYFEATURE_B_FEATURE_DID    = 28300

# mst_datasource_by_supply_feature

D_A_MSTDATASOURCEBYSUPPLYFEATURE_B_FEATURE_SUPPLY_DID   = 28400

# Updates (29000 - 29999)

# mst_datasource

# mst_datasource_stats

# dat_datasource

# dat_datasource_map

U_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=29300
U_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=29301

# dat_datasource_text_summary

# dat_datasource_novelty_detector_datapoint

# dat_datasource_hash

# dat_datasource_metadata

# mst_datasource_hooks

# dat_datasource_supplies

# dat_datasource_features

# mst_datasource_features

# mst_datasource_supply_features

# mst_datasource_supplies_guessed

# mst_datasource_by_feature

# mst_datasource_by_supply_feature

