#auth authorization

E_AA_AR_UNF=50000
E_AA_AR_RNF=50001

E_AA_ANAC_QE=50005
E_AA_ANAC_RE=50006

E_AA_AGAC_QE=50010
E_AA_AGAC_RE=50011

E_AA_AGDSD_QE=50015
E_AA_AGDSD_TE=50016
E_AA_AGDSD_RE=50017

E_AA_APDSD_QE=50020
E_AA_APDSD_RE=50021

E_AA_AGDSC_QE=50025
E_AA_AGDSC_RE=50026

E_AA_ADSUC_RE=50030

E_AA_ANDSC_QE=50035
E_AA_ANDSC_RE=50036

E_AA_AGDPD_QE=50040
E_AA_AGDPD_TE=50041
E_AA_AGDPD_RE=50042

E_AA_AGDPC_QE=50045
E_AA_AGDPC_RE=50046

E_AA_ANDPC_QE=50050
E_AA_ANDPC_RE=50051

E_AA_ADPUC_RE=50055

E_AA_AAGUC_RE=50060

E_AA_AGWC_QE=50065
E_AA_AGWC_RE=50066

E_AA_AWUC_RE=50070

E_AA_ANWC_QE=50075
E_AA_ANWC_RE=50076

E_AA_AGDBC_QE=50080
E_AA_AGDBC_RE=50081

E_AA_ADBUC_RE=50085

E_AA_ANDBC_QE=50090
E_AA_ANDBC_RE=50091

E_AA_AMPV_QE=50095
E_AA_AMPV_RE=50096

E_AA_AMNV_QE=50100
E_AA_AMNV_RE=50101

E_AA_AAWTDB_QE=50105
E_AA_AAWTDB_RE=50106

E_AA_ADWFDB_QE=50110
E_AA_ADWFDB_RE=50111

E_AA_ADAG_RE=50115

E_AA_ADDS_RE=50120

E_AA_ADDP_RE=50125

E_AA_ADW_RE=50130

E_AA_ADDB_RE=50135

E_AA_AADPTW_QE=50140
E_AA_AADPTW_RE=50141

E_AA_ADDPFW_QE=50145
E_AA_ADDPFW_RE=50146

E_AA_ANSCR_QE=50150
E_AA_ANSCR_RE=50151

E_AA_AGSD_QE=50160
E_AA_AGSD_RE=50161

E_AA_AGSC_QE=50165
E_AA_AGSC_RE=50166
E_AA_AGSC_TE=50167

E_AA_ADS_RE=50170

E_AA_ANCCR_QE=50175

E_AA_AGCC_RE=50180

E_AA_AUCC_RE=50185

E_AA_ADCR_RE=50190

E_AA_AAMTC_QE=50195
E_AA_AAMTC_RE=50196

E_AA_ADMFC_RE=50200

# auth quotes authorization

E_AQA_ANDP_DSNF=55000


# auth tickets provision

E_ATP_NST_IUID=56000 #new_snapshot_ticket invalid uid
E_ATP_NST_INID=56001 #new_snapshot_ticket invalid nid
E_ATP_NST_IEXP=56002 #new_snapshot_ticket invalid expires date
E_ATP_NST_ISHT=56003 #new_snapshot_ticket invalid share type
E_ATP_NST_SNF=56004 #new_snapshot_ticket snapshot not found
E_ATP_NST_EIDB=56005 #new_snapshot_ticket error inserting database
E_ATP_NST_USTF=56005 #new_snapshot_ticket error unknown snapshot type found

# auth tickets authorization

E_ATA_AGDSD_IUID=57000 #authorize_get_datasource_data invalid uid
E_ATA_AGDSD_ITID=57001 #authorize_get_datasource_data invalid tid
E_ATA_AGDSD_IDID=57002 #authorize_get_datasource_data invalid did
E_ATA_AGDSD_III=57003 #authorize_get_datasource_data invalid interval init
E_ATA_AGDSD_IIE=57004 #authorize_get_datasource_data invalid interval end
E_ATA_AGDSD_TNF=57005 #authorize_get_datasource_data ticket not found
E_ATA_AGDSD_EXPT=57006 #authorize_get_datasource_data ticket expired
E_ATA_AGDSD_UNA=57007 #authorize_get_datasource_data user not allowed
E_ATA_AGDSD_DNA=57008 #authorize_get_datasource_data did not allowed
E_ATA_AGDSD_IINT=57009 #authorize_get_datasource_data invalid interval
E_ATA_AGDSD_INSP=57010 #authorize_get_datasource_data insufficient permissions

E_ATA_AGDPD_IUID=57050 #authorize_get_datapoint_data invalid uid
E_ATA_AGDPD_ITID=57051 #authorize_get_datapoint_data invalid tid
E_ATA_AGDPD_IPID=57052 #authorize_get_datapoint_data invalid pid
E_ATA_AGDPD_III=57053 #authorize_get_datapoint_data invalid interval init
E_ATA_AGDPD_IIE=57054 #authorize_get_datapoint_data invalid interval end
E_ATA_AGDPD_TNF=57055 #authorize_get_datapoint_data ticket not found
E_ATA_AGDPD_EXPT=57056 #authorize_get_datapoint_data ticket expired
E_ATA_AGDPD_UNA=57057 #authorize_get_datapoint_data user not allowed
E_ATA_AGDPD_DNA=57058 #authorize_get_datapoint_data pid not allowed
E_ATA_AGDPD_IINT=57059 #authorize_get_datapoint_data invalid interval
E_ATA_AGDPD_INSP=57060 #authorize_get_datapoint_data insufficient permissions

E_ATA_AGSNC_IUID=57100 #authorize_get_snapshot_config invalid uid
E_ATA_AGSNC_ITID=57101 #authorize_get_snapshot_config invalid tid
E_ATA_AGSNC_INID=57102 #authorize_get_snapshot_config invalid nid
E_ATA_AGSNC_TNF=57103 #authorize_get_snapshot_config ticket not found
E_ATA_AGSNC_EXPT=57104 #authorize_get_snapshot_config ticket expired
E_ATA_AGSNC_UNA=57105 #authorize_get_snapshot_config user not allowed
E_ATA_AGSNC_DNA=57106 #authorize_get_snapshot_config nid not allowed
E_ATA_AGSNC_INSP=57107 #authorize_get_snapshot_config insufficient permissions

