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
    20303:'select did,date,variables,datapoints from dat_datasource_map where did=? and date=?',
    20304:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=? and date<=? limit ?',
    20305:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=? and date<=?',
    20306:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=? limit ?',
    20307:'select did,date,variables,datapoints from dat_datasource_map where did=? and date>=?',
    20308:'select did,date,variables,datapoints from dat_datasource_map where did=? and date<=? limit ?',
    20309:'select did,date,variables,datapoints from dat_datasource_map where did=? and date<=?',
    20310:'select did,date,variables,datapoints from dat_datasource_map where did=? limit ?',
    20311:'select did,date,variables,datapoints from dat_datasource_map where did=?',
    20312:'select date from dat_datasource_map where did=? and date=?',
    20313:'select date from dat_datasource_map where did=? and date>=? and date<=? limit ?',
    20314:'select date from dat_datasource_map where did=? and date>=? and date<=?',
    20315:'select date from dat_datasource_map where did=? and date>=? limit ?',
    20316:'select date from dat_datasource_map where did=? and date>=?',
    20317:'select date from dat_datasource_map where did=? and date<=? limit ?',
    20318:'select date from dat_datasource_map where did=? and date<=?',
    20319:'select date from dat_datasource_map where did=? limit ?',
    20320:'select date from dat_datasource_map where did=?',
    20400:'select did,date,content_length,num_lines,num_words,word_frecuency from dat_datasource_text_summary where did=? and date=?',
    20401:'select did,date,content_length,num_lines,num_words,word_frecuency from dat_datasource_text_summary where did=? and date>=? and date<=?',
    20600:'select did,date,content from dat_datasource_hash where did=? and date=?',
    20601:'select did,date,content from dat_datasource_hash where did=? and date>=? and date<=? limit ?',
    20602:'select did,date,content from dat_datasource_hash where did=? and date>=? and date<=?',
    20603:'select did,date,content from dat_datasource_hash where did=? and date>=? limit ?',
    20604:'select did,date,content from dat_datasource_hash where did=? and date>=?',
    20605:'select did,date,content from dat_datasource_hash where did=? and date<=? limit ?',
    20606:'select did,date,content from dat_datasource_hash where did=? and date<=?',
    20607:'select did,date,content from dat_datasource_hash where did=? limit ?',
    20608:'select did,date,content from dat_datasource_hash where did=?',
    20700:'select did,date,size from dat_datasource_metadata where did=? and date=?',
    20701:'select size from dat_datasource_metadata where did=? and date=?',
    20702:'select did,date,size from dat_datasource_metadata where did=? and date>=? and date<=?',
    20703:'select did,date,size from dat_datasource_metadata where did=? and date>=? and date<=? limit ?',
    20800:'select sid from mst_datasource_hooks where did=?',
    20900:'select did,date,supplies from dat_datasource_supplies where did=? and date=?',
    20901:'select did,date,supplies from dat_datasource_supplies where did=? and date>=? and date<=?',
    20902:'select did,date,supplies from dat_datasource_supplies where did=? limit ?',
    21000:'select date,features from mst_datasource_features where did=?',
    21100:'select did,weight from mst_datasource_by_feature where feature=? limit ?',
    21200:'select dtree from mst_datapoint_classifier_dtree where did=?',
    25000:'insert into mst_datasource (did,aid,uid,datasourcename,creation_date) values (?,?,?,?,?)',
    25001:'insert into mst_datasource (did,aid,uid,datasourcename,creation_date) values (?,?,?,?,?) if not exists',
    25100:'insert into mst_datasource_stats (did,last_received) values (?,?)',
    25101:'insert into mst_datasource_stats (did,last_mapped) values (?,?)',
    25200:'insert into dat_datasource (did,date,content) values (?,?,?)',
    25300:'insert into dat_datasource_map (did,date,variables,datapoints) values (?,?,?,?)',
    25400:'insert into dat_datasource_text_summary (did,date,content_length,num_lines, num_words, word_frecuency) values (?,?,?,?,?,?)',
    25600:'insert into dat_datasource_hash (did,date,content) values (?,?,?)',
    25700:'insert into dat_datasource_metadata (did,date,size) values (?,?,?)',
    25800:'insert into mst_datasource_hooks (did,sid) values (?,?)',
    25900:'insert into dat_datasource_supplies (did,date,supplies) values (?,?,?)',
    26000:'insert into mst_datasource_features (did,date,features) values (?,?,?)',
    26100:'insert into mst_datasource_by_feature (feature, did, weight) values (?,?,?)',
    26200:'insert into mst_datapoint_classifier_dtree (did,dtree) values (?,?)',
    27000:'delete from mst_datasource where did=?',
    27100:'delete from mst_datasource_stats where did=?',
    27200:'delete from dat_datasource where did=?',
    27201:'delete from dat_datasource where did=? and date=?',
    27300:'delete from dat_datasource_map where did=?',
    27301:'delete from dat_datasource_map where did=? and date=?',
    27302:'delete datapoints[?] from dat_datasource_map where did=? and date=?',
    27400:'delete from dat_datasource_text_summary where did=?',
    27401:'delete from dat_datasource_text_summary where did=? and date=?',
    27600:'delete from dat_datasource_hash where did=? and date=?',
    27601:'delete from dat_datasource_hash where did=?',
    27700:'delete from dat_datasource_metadata where did=?',
    27701:'delete from dat_datasource_metadata where did=? and date=?',
    27800:'delete from mst_datasource_hooks where did=?',
    27801:'delete from mst_datasource_hooks where did=? and sid=?',
    27900:'delete from dat_datasource_supplies where did=?',
    27901:'delete from dat_datasource_supplies where did=? and date=?',
    28000:'delete from mst_datasource_features where did=?',
    28100:'delete from mst_datasource_by_feature where feature=? and did=?',
    28200:'delete from mst_datapoint_classifier_dtree where did=?',
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

S_VARIABLES_DATDATASOURCEMAP_B_DID_DATE                 = 20300
S_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE                = 20301
S_A_DATDATASOURCEMAP_B_DID_DATE                         = 20303
S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE_COUNT       = 20304
S_A_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE             = 20305
S_A_DATDATASOURCEMAP_B_DID_INITDATE_COUNT               = 20306
S_A_DATDATASOURCEMAP_B_DID_INITDATE                     = 20307
S_A_DATDATASOURCEMAP_B_DID_ENDDATE_COUNT                = 20308
S_A_DATDATASOURCEMAP_B_DID_ENDDATE                      = 20309
S_A_DATDATASOURCEMAP_B_DID_COUNT                        = 20310
S_A_DATDATASOURCEMAP_B_DID                              = 20311
S_DATE_DATDATASOURCEMAP_B_DID_DATE                      = 20312
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE_COUNT    = 20313
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_ENDDATE          = 20314
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE_COUNT            = 20315
S_DATE_DATDATASOURCEMAP_B_DID_INITDATE                  = 20316
S_DATE_DATDATASOURCEMAP_B_DID_ENDDATE_COUNT             = 20317
S_DATE_DATDATASOURCEMAP_B_DID_ENDDATE                   = 20318
S_DATE_DATDATASOURCEMAP_B_DID_COUNT                     = 20319
S_DATE_DATDATASOURCEMAP_B_DID                           = 20320

# dat_datasource_text_summary

S_A_DATDATASOURCETEXTSUMMARY_B_DID_DATE=20400
S_A_DATDATASOURCETEXTSUMMARY_B_DID_INITDATE_ENDDATE=20401

# dat_datasource_hash

S_A_DATDATASOURCEHASH_B_DID_DATE                    = 20600
S_A_DATDATASOURCEHASH_B_DID_INITDATE_ENDDATE_COUNT  = 20601
S_A_DATDATASOURCEHASH_B_DID_INITDATE_ENDDATE        = 20602
S_A_DATDATASOURCEHASH_B_DID_INITDATE_COUNT          = 20603
S_A_DATDATASOURCEHASH_B_DID_INITDATE                = 20604
S_A_DATDATASOURCEHASH_B_DID_ENDDATE_COUNT           = 20605
S_A_DATDATASOURCEHASH_B_DID_ENDDATE                 = 20606
S_A_DATDATASOURCEHASH_B_DID_COUNT                   = 20607
S_A_DATDATASOURCEHASH_B_DID                         = 20608

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

# mst_datasource_features

S_DATEFEATURES_MSTDATASOURCEFEATURES_B_DID          =   21000

# mst_datasource_by_feature

S_DIDWEIGHT_MSTDATASOURCEBYFEATURE_B_FEATURE_COUNT  =   21100

# mst_datapoint_classifier_dtree

S_DTREE_MSTDATAPOINTCLASSIFIERDTREE_B_DID           =   21200

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

# dat_datasource_hash

I_A_DATDATASOURCEHASH=25600

# dat_datasource_metadata

I_A_DATDATASOURCEMETADATA=25700

# mst_datasource_hooks

I_A_MSTDATASOURCEHOOKS  =   25800

# dat_datasource_supplies

I_A_DATDATASOURCESUPPLIES   =   25900

# mst_datasource_features

I_A_MSTDATASOURCEFEATURES   =   26000

# mst_datasource_by_feature

I_A_MSTDATASOURCEBYFEATURE  =   26100

# mst_datapoint_classifier_dtree

I_A_MSTDATAPOINTCLASSIFIERDTREE =   26200

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

# mst_datasource_features

D_A_MSTDATASOURCEFEATURES_B_DID     =   28000

# mst_datasource_by_feature

D_A_MSTDATASOURCEBYFEATURE_B_FEATURE_DID    = 28100

# mst_datapoint_classifier_dtree

D_A_MSTDATAPOINTCLASSIFIERDTREE_B_DID   =   28200

# Updates (29000 - 29999)

# mst_datasource

# mst_datasource_stats

# dat_datasource

# dat_datasource_map

U_VARIABLES_DATDATASOURCEMAP_B_DID_DATE=29300
U_DATAPOINTS_DATDATASOURCEMAP_B_DID_DATE=29301

# dat_datasource_text_summary

# dat_datasource_hash

# dat_datasource_metadata

# mst_datasource_hooks

# dat_datasource_supplies

# mst_datasource_features

# mst_datasource_by_feature

# mst_datapoint_classifier_dtree

