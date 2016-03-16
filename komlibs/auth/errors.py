'''
In this file we define the different error codes that will be
added to the exceptions in the auth modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for errors in this module is 50000 - 100000

'''

#auth authorization

E_AA_AR_BP      = 50000
E_AA_AR_RNF     = 50001
E_AA_AR_FBP     = 50002

# auth.quotes.authorization

E_AQA_ANA_QE    = 51000      #: authorize_new_agent quotes exception
E_AQA_ANDS_QE   = 51010      #: authorize_new_datasource quotes exception
E_AQA_ANDS_IA   = 51011      #: authorize_new_datasource invalid aid
E_AQA_ANDP_DSNF = 51020      #: authorize_new_datapoint datasource not found exception
E_AQA_ANDP_QE   = 51030      #: authorize_new_datapoint quotes exception
E_AQA_ANW_QE    = 51040      #: authorize_new_widget quotes exception
E_AQA_ANDB_QE   = 51050      #: authorize_new_dashboard quotes exception
E_AQA_ANS_QE    = 51060      #: authorize_new_snapshot quotes exception
E_AQA_ANC_QE    = 51070      #: authorize_new_circle quotes exception
E_AQA_AAMTC_QE  = 51080      #: authorize_add_member_to_circle quotes exception


# auth.resources.authorization


E_ARA_AGAC_RE   = 52000      #: authorize_get_agent_config exception
E_ARA_AGDSC_RE  = 52010      #: authorize_get_datasource_config exception
E_ARA_APDSC_RE  = 52020      #: authorize_put_datasource_config exception
E_ARA_AGDSD_RE  = 52030      #: authorize_get_datasource_data exception
E_ARA_ATDSD_RE  = 52040      #: authorize_post_datasource_data exception
E_ARA_ATDSD_ANF = 52041      #: authorize_post_datasource_data invalid agent exception
E_ARA_ANDS_RE   = 52050      #: authorize_new_datasource exception
E_ARA_ANDS_ANF  = 52051      #: authorize_post_datasource_data invalid agent exception
E_ARA_AGDPD_RE  = 52060      #: authorize_get_datapoint_data exception
E_ARA_AGDPC_RE  = 52070      #: authorize_get_datapoint_config exception
E_ARA_APDPC_RE  = 52080      #: authorize_put_datapoint_config exception
E_ARA_ANDP_RE   = 52090      #: authorize_new_datapoint exception
E_ARA_APAC_RE   = 52100      #: authorize_put_agent_config exception
E_ARA_AGWC_RE   = 52110      #: authorize_get_widget_config exception
E_ARA_APWC_RE   = 52120      #: authorize_put_widget_config exception
E_ARA_AGDBC_RE  = 52130      #: authorize_get_dashboard_config exception
E_ARA_APDBC_RE  = 52140      #: authorize_put_dashboard_config exception
E_ARA_AMPOSV_RE = 52150      #: authorize_mark_positive_variable exception
E_ARA_AMNEGV_RE = 52160      #: authorize_mark_negative_variable exception
E_ARA_AAWTDB_RE = 52170      #: authorize_add_widget_to_dashboard exception
E_ARA_ADWFDB_RE = 52180      #: authorize_delete_widget_from_dashboard exception
E_ARA_ADA_RE    = 52190      #: authorize_delete_agent exception
E_ARA_ADDS_RE   = 52200      #: authorize_delete_datasource exception
E_ARA_ADDP_RE   = 52210      #: authorize_delete_datapoint exception
E_ARA_ADW_RE    = 52220      #: authorize_delete_widget exception
E_ARA_ADDB_RE   = 52230      #: authorize_delete_dashboard exception
E_ARA_AADPTW_RE = 52240      #: authorize_add_datapoint_to_widget exception
E_ARA_ADDPFW_RE = 52250      #: authorize_delete_datapoint_from_widget exception
E_ARA_ANS_RE    = 52260      #: authorize_new_snapshot exception
E_ARA_AGSD_RE   = 52270      #: authorize_get_snapshot_data exception
E_ARA_AGSC_RE   = 52280      #: authorize_get_snapshot_config exception
E_ARA_ADS_RE    = 52290      #: authorize_delete_snapshot exception
E_ARA_AGCC_RE   = 52300      #: authorize_get_circle_config exception
E_ARA_ADC_RE    = 52310      #: authorize_delete_circle exception
E_ARA_AUCC_RE   = 52320      #: authorize_update_circle_config exception
E_ARA_AAMTC_RE  = 52330      #: authorize_add_member_to_circle exception
E_ARA_ADMFC_RE  = 52340      #: authorize_delete_member_from_circle exception

# auth.passport

E_AP_CC_ID      = 53000      #: Cookie class. invalid dict cookie passed
E_AP_CC_IU      = 53001      #: Cookie class. invalid user
E_AP_CC_IA      = 53002      #: Cookie class. invalid aid
E_AP_CC_IS      = 53003      #: Cookie class. invalid sequence

E_AP_PC_IU      = 53010      #: Passport class. invalid uid
E_AP_PC_IA      = 53011      #: Passport class. invalid aid

E_AP_GUP_UNF    = 53100      #: get_user_passport. User not found exception
E_AP_GUP_IUS    = 53101      #: get_user_passport. Invalid user state

E_AP_GAP_ANF    = 53200      #: get_agent_passport. Agent not found exception
E_AP_GAP_IAS    = 53201      #: get_agent_passport. Invalid agent state
E_AP_GAP_CANF   = 53202      #: get_agent_passport. Cookie has no aid

# auth.tickets.provision

E_ATP_NST_IUID   = 56000      #: new_snapshot_ticket invalid uid
E_ATP_NST_INID   = 56001      #: new_snapshot_ticket invalid nid
E_ATP_NST_IEXP   = 56002      #: new_snapshot_ticket invalid expires date
E_ATP_NST_ISHT   = 56003      #: new_snapshot_ticket invalid share type
E_ATP_NST_SNF    = 56004      #: new_snapshot_ticket snapshot not found
E_ATP_NST_EIDB   = 56005      #: new_snapshot_ticket error inserting database
E_ATP_NST_USTF   = 56006      #: new_snapshot_ticket error unknown snapshot type found
E_ATP_NST_IUIDS  = 56007      #: new_snapshot_ticket invalid allowed_uids type
E_ATP_NST_ICIDS  = 56008      #: new_snapshot_ticket invalid allowed_cids type
E_ATP_NST_IUIDSI = 56009      #: new_snapshot_ticket invalid allowed_uids item
E_ATP_NST_ICIDSI = 56010      #: new_snapshot_ticket invalid allowed_cids item
E_ATP_NST_NSL    = 56011      #: new_snapshot_ticket no sharing list passed or zero length

# auth tickets authorization

E_ATA_AGDSD_IUID = 57000      #: authorize_get_datasource_data invalid uid
E_ATA_AGDSD_ITID = 57001      #: authorize_get_datasource_data invalid tid
E_ATA_AGDSD_IDID = 57002      #: authorize_get_datasource_data invalid did
E_ATA_AGDSD_III  = 57003      #: authorize_get_datasource_data invalid interval init
E_ATA_AGDSD_IIE  = 57004      #: authorize_get_datasource_data invalid interval end
E_ATA_AGDSD_TNF  = 57005      #: authorize_get_datasource_data ticket not found
E_ATA_AGDSD_EXPT = 57006      #: authorize_get_datasource_data ticket expired
E_ATA_AGDSD_UNA  = 57007      #: authorize_get_datasource_data user not allowed
E_ATA_AGDSD_DNA  = 57008      #: authorize_get_datasource_data did not allowed
E_ATA_AGDSD_IINT = 57009      #: authorize_get_datasource_data invalid interval
E_ATA_AGDSD_INSP = 57010      #: authorize_get_datasource_data insufficient permissions

E_ATA_AGDPD_IUID = 57050      #: authorize_get_datapoint_data invalid uid
E_ATA_AGDPD_ITID = 57051      #: authorize_get_datapoint_data invalid tid
E_ATA_AGDPD_IPID = 57052      #: authorize_get_datapoint_data invalid pid
E_ATA_AGDPD_III  = 57053      #: authorize_get_datapoint_data invalid interval init
E_ATA_AGDPD_IIE  = 57054      #: authorize_get_datapoint_data invalid interval end
E_ATA_AGDPD_TNF  = 57055      #: authorize_get_datapoint_data ticket not found
E_ATA_AGDPD_EXPT = 57056      #: authorize_get_datapoint_data ticket expired
E_ATA_AGDPD_UNA  = 57057      #: authorize_get_datapoint_data user not allowed
E_ATA_AGDPD_DNA  = 57058      #: authorize_get_datapoint_data pid not allowed
E_ATA_AGDPD_IINT = 57059      #: authorize_get_datapoint_data invalid interval
E_ATA_AGDPD_INSP = 57060      #: authorize_get_datapoint_data insufficient permissions

E_ATA_AGSNC_IUID = 57100      #: authorize_get_snapshot_config invalid uid
E_ATA_AGSNC_ITID = 57101      #: authorize_get_snapshot_config invalid tid
E_ATA_AGSNC_INID = 57102      #: authorize_get_snapshot_config invalid nid
E_ATA_AGSNC_TNF  = 57103      #: authorize_get_snapshot_config ticket not found
E_ATA_AGSNC_EXPT = 57104      #: authorize_get_snapshot_config ticket expired
E_ATA_AGSNC_UNA  = 57105      #: authorize_get_snapshot_config user not allowed
E_ATA_AGSNC_DNA  = 57106      #: authorize_get_snapshot_config nid not allowed
E_ATA_AGSNC_INSP = 57107      #: authorize_get_snapshot_config insufficient permissions

