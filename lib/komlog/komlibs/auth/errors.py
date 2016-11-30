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

The range reserved for Errors.in this module is 50000 - 100000

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

#auth authorization

    E_AA_AR_BP      = 50000
    E_AA_AR_RNF     = 50001
    E_AA_AR_FBP     = 50002

# auth.quotes.authorization

    E_AQA_ANA_QE      = 51000      #: authorize_new_agent quotes exception
    E_AQA_ANDS_QE     = 51010      #: authorize_new_datasource quotes exception
    E_AQA_ANDS_IA     = 51011      #: authorize_new_datasource invalid aid
    E_AQA_ANDSDP_DSNF = 51020      #: authorize_new_datasource_datapoint datasource not found exception
    E_AQA_ANDSDP_QE   = 51030      #: authorize_new_datasource_datapoint quotes exception
    E_AQA_ANUDP_IA    = 51035      #: authorize_new_user_datapoint invalid aid
    E_AQA_ANUDP_QE    = 51036      #: authorize_new_user_datapoint quotes exception
    E_AQA_ANW_QE      = 51040      #: authorize_new_widget quotes exception
    E_AQA_ANDB_QE     = 51050      #: authorize_new_dashboard quotes exception
    E_AQA_ANS_QE      = 51060      #: authorize_new_snapshot quotes exception
    E_AQA_ANC_QE      = 51070      #: authorize_new_circle quotes exception
    E_AQA_AAMTC_QE    = 51080      #: authorize_add_member_to_circle quotes exception
    E_AQA_APDSD_QE    = 51090      #: authorize_post_datasource_data quotes exception
    E_AQA_APDPD_QE    = 51095      #: authorize_post_datapoint_data quotes exception
    E_AQA_AGDSD_DSNF  = 51100      #: authorize_get_datasource_data datasource not found exception
    E_AQA_AGDSD_IBE   = 51101      #: authorize_get_datasource_data interval bounds exception
    E_AQA_AGDPD_DPNF  = 51110      #: authorize_get_datapoint_data datapoint not found exception
    E_AQA_AGDPD_DSNF  = 51111      #: authorize_get_datapoint_data datasource not found exception
    E_AQA_AGDPD_IBE   = 51112      #: authorize_get_datapoint_data interval bounds exception


# auth.resources.authorization


    E_ARA_AGAC_RE   = 52000      #: authorize_get_agent_config exception
    E_ARA_AGDSC_RE  = 52010      #: authorize_get_datasource_config exception
    E_ARA_APDSC_RE  = 52020      #: authorize_put_datasource_config exception
    E_ARA_AGDSD_RE  = 52030      #: authorize_get_datasource_data exception
    E_ARA_ATDSD_RE  = 52040      #: authorize_post_datasource_data exception
    E_ARA_ATDSD_ANF = 52041      #: authorize_post_datasource_data invalid agent exception
    E_ARA_ATDPD_RE  = 52045      #: authorize_post_datapoint_data exception
    E_ARA_ATDPD_ANF = 52046      #: authorize_post_datapoint_data invalid agent exception
    E_ARA_ANDS_RE   = 52050      #: authorize_new_datasource exception
    E_ARA_ANDS_ANF  = 52051      #: authorize_post_datasource_data invalid agent exception
    E_ARA_AGDPD_RE  = 52060      #: authorize_get_datapoint_data exception
    E_ARA_AGDPC_RE  = 52070      #: authorize_get_datapoint_config exception
    E_ARA_APDPC_RE  = 52080      #: authorize_put_datapoint_config exception
    E_ARA_ANDSDP_RE = 52090      #: authorize_new_datasource_datapoint exception
    E_ARA_ANUDP_IA  = 52095      #: authorize_new_user_datapoint exception invalid aid
    E_ARA_ANUDP_RE  = 52096      #: authorize_new_user_datapoint exception
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
    E_ARA_ADDPFDS_RE= 52350      #: authorize_dissociate_datapoint_from_datasource exception
    E_ARA_AHTDP_RE  = 52360      #: authorize_hook_to_datapoint exception
    E_ARA_AHTDS_RE  = 52370      #: authorize_hook_to_datasource exception
    E_ARA_AUHFDP_RE = 52380      #: authorize_unhook_from_datapoint exception
    E_ARA_AUHFDS_RE = 52390      #: authorize_unhook_from_datasource exception

# auth.passport

    E_AP_CC_ID      = 53000      #: Cookie class. invalid dict cookie passed
    E_AP_CC_IU      = 53001      #: Cookie class. invalid user
    E_AP_CC_IA      = 53002      #: Cookie class. invalid aid
    E_AP_CC_IS      = 53003      #: Cookie class. invalid session id
    E_AP_CC_ISQ     = 53004      #: Cookie class. invalid sequence
    E_AP_CC_IPV     = 53005      #: Cookie class. invalid protocol version

    E_AP_PC_IU      = 53010      #: Passport class. invalid uid
    E_AP_PC_IA      = 53011      #: Passport class. invalid aid
    E_AP_PC_IS      = 53012      #: Passport class. invalid session id
    E_AP_PC_IPV     = 53013      #: Passport class. invalid protocol version
    E_AP_PC_AIDORPV = 53014      #: Passport class. one of aid or pv is None

    E_AP_GUP_UNF    = 53100      #: get_user_passport. User not found exception
    E_AP_GUP_IUS    = 53101      #: get_user_passport. Invalid user state

    E_AP_GAP_ANF    = 53200      #: get_agent_passport. Agent not found exception
    E_AP_GAP_IAS    = 53201      #: get_agent_passport. Invalid agent state
    E_AP_GAP_CANF   = 53202      #: get_agent_passport. Cookie has no aid
    E_AP_GAP_CPVNF  = 53203      #: get_agent_passport. Cookie has no protocol version

    E_AP_CPV_IP     = 53300      #: check_agent_passport_validity. Invalid passport
    E_AP_CPV_IAID   = 53301      #: check_agent_passport_validity. Invalid aid
    E_AP_CPV_ANF    = 53302      #: check_agent_passport_validity. Agent not found
    E_AP_CPV_IAS    = 53303      #: check_agent_passport_validity. Invalid agent state

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

# auth.session

    E_AS_SAGS_ISID  =   58000       #: set_agent_session. invalid sid
    E_AS_SAGS_IAID  =   58001       #: set_agent_session. invalid aid
    E_AS_SAGS_IUID  =   58002       #: set_agent_session. invalid uid
    E_AS_SAGS_IMCNC =   58003       #: set_agent_session. imc address not configured
    E_AS_SAGS_IPV   =   58004       #: set_agent_session. invalid protocol version

    E_AS_USAGS_ISID =   58100       #: unset_agent_session. invalid sid
    E_AS_USAGS_ILU  =   58101       #: unset_agent_session. invalid last_update

    E_AS_DAGS_ISID  =   58200       #: delete_agent_session. invalid sid
    E_AS_DAGS_ILU   =   58201       #: delete_agent_session. invalid last_update

    E_AS_GASI_ISID  =   58300       #: get_agent_session_info. invalid sid
    E_AS_GASI_SNF   =   58301       #: get_agent_session_info. session not found

# auth.quotes.update

    E_AQU_QUTA_UIDNF    =   59000   #: quo_user_total_agents. uid not found.
    E_AQU_QUTA_USRNF    =   59001   #: quo_user_total_agents. user not found.

    E_AQU_QUTDS_UIDNF   =   59010   #: quo_user_total_datasources. uid not found.
    E_AQU_QUTDS_USRNF   =   59011   #: quo_user_total_datasources. user not found.

    E_AQU_QUTDP_UIDNF   =   59020   #: quo_user_total_datapoints. uid not found.
    E_AQU_QUTDP_USRNF   =   59021   #: quo_user_total_datapoints. user not found.

    E_AQU_QUTW_UIDNF    =   59030   #: quo_user_total_widgets. uid not found.
    E_AQU_QUTW_USRNF    =   59031   #: quo_user_total_widgets. user not found.

    E_AQU_QUTDB_UIDNF   =   59040   #: quo_user_total_dashboards. uid not found.
    E_AQU_QUTDB_USRNF   =   59041   #: quo_user_total_dashboards. user not found.

    E_AQU_QATDS_AIDNF   =   59050   #: quo_agent_total_datasources. aid not found.
    E_AQU_QATDS_AGNF    =   59051   #: quo_agent_total_datasources. agent not found.

    E_AQU_QATDP_AIDNF   =   59060   #: quo_agent_total_datapoints. aid not found.
    E_AQU_QATDP_AGNF    =   59061   #: quo_agent_total_datapoints. agent not found.

    E_AQU_QDSTDP_DIDNF  =   59070   #: quo_datasource_total_datapoints. did not found.
    E_AQU_QDSTDP_DSNF   =   59071   #: quo_datasource_total_datapoints. datasource not found.

    E_AQU_QUTSN_UIDNF   =   59080   #: quo_user_total_snapshots. uid not found.
    E_AQU_QUTSN_USRNF   =   59081   #: quo_user_total_snapshots. user not found.

    E_AQU_QUTC_UIDNF    =   59090   #: quo_user_total_circles. uid not found.
    E_AQU_QUTC_USRNF    =   59091   #: quo_user_total_circles. user not found.

    E_AQU_QCTM_CIDNF    =   59100   #: quo_circle_total_members. cid not found.
    E_AQU_QCTM_CRNF     =   59101   #: quo_circle_total_members. circle not found.

    E_AQU_QDDSO_PNF     =   59110   #: quo_daily_datasource_occupation. param not found.
    E_AQU_QDDSO_DSNF    =   59111   #: quo_daily_datasource_occupation. datasource not found.

    E_AQU_QDUDSO_PNF    =   59120   #: quo_daily_user_datasources_occupation. param not found.
    E_AQU_QDUDSO_DSNF   =   59121   #: quo_daily_user_datasources_occupation. datasource not found.
    E_AQU_QDUDSO_USRNF  =   59122   #: quo_daily_user_datasources_occupation. user not found.

    E_AQU_QUTO_DIDNF    =   59130   #: quo_user_total_occupation. did not found.
    E_AQU_QUTO_DSNF     =   59131   #: quo_user_total_occupation. datasource not found.
    E_AQU_QUTO_USRNF    =   59132   #: quo_user_total_occupation. user not found.

    E_AQU_QDUDPC_PNF    =   59140   #: quo_daily_user_data_post_counter invalid parameter
    E_AQU_QDUDPC_USRNF  =   59141   #: quo_daily_user_data_post_counter user not found

    E_AQU_QDDSDPC_PNF   =   59150   #: quo_daily_datasource_data_post_counter invalid parameter
    E_AQU_QDDSDPC_DSNF  =   59151   #: quo_daily_datasource_data_post_counter datasource not found

    E_AQU_QDDPDPC_PNF   =   59160   #: quo_daily_datapoint_data_post_counter invalid parameter
    E_AQU_QDDPDPC_DPNF  =   59161   #: quo_daily_datapoint_data_post_counter datapoint not found

# auth.quotes.compare

    E_AQC_QUTA_UIDNF    =   60000   #: quo_user_total_agents. uid not found.
    E_AQC_QUTA_USRNF    =   60001   #: quo_user_total_agents. user not found.

    E_AQC_QUTDS_UIDNF   =   60010   #: quo_user_total_datasources. uid not found.
    E_AQC_QUTDS_USRNF   =   60011   #: quo_user_total_datasources. user not found.

    E_AQC_QUTDP_UIDNF   =   60020   #: quo_user_total_datapoints. uid not found.
    E_AQC_QUTDP_USRNF   =   60021   #: quo_user_total_datapoints. user not found.

    E_AQC_QUTW_UIDNF    =   60030   #: quo_user_total_widgets. uid not found.
    E_AQC_QUTW_USRNF    =   60031   #: quo_user_total_widgets. user not found.

    E_AQC_QUTDB_UIDNF   =   60040   #: quo_user_total_dashboards. uid not found.
    E_AQC_QUTDB_USRNF   =   60041   #: quo_user_total_dashboards. user not found.

    E_AQC_QATDS_PNF     =   60050   #: quo_agent_total_datasources. param not found.
    E_AQC_QATDS_USRNF   =   60051   #: quo_agent_total_datasources. user not found.

    E_AQC_QATDP_PNF     =   60060   #: quo_agent_total_datapoints. param not found.
    E_AQC_QATDP_USRNF   =   60061   #: quo_agent_total_datapoints. user not found.

    E_AQC_QDSTDP_PNF    =   60070   #: quo_datasource_total_datapoints. param not found.
    E_AQC_QDSTDP_USRNF  =   60071   #: quo_datasource_total_datapoints. user not found.

    E_AQC_QUTSN_UIDNF   =   60080   #: quo_user_total_snapshots. uid not found.
    E_AQC_QUTSN_USRNF   =   60081   #: quo_user_total_snapshots. user not found.

    E_AQC_QUTC_UIDNF    =   60090   #: quo_user_total_circles. uid not found.
    E_AQC_QUTC_USRNF    =   60091   #: quo_user_total_circles. user not found.

    E_AQC_QCTM_PNF      =   60100   #: quo_circle_total_members. param not found.
    E_AQC_QCTM_USRNF    =   60101   #: quo_circle_total_members. user not found.

    E_AQC_QDDSO_PNF     =   60110   #: quo_daily_datasource_occupation. param not found.
    E_AQC_QDDSO_DSNF    =   60111   #: quo_daily_datasource_occupation. datasource not found.
    E_AQC_QDDSO_USRNF   =   60112   #: quo_daily_datasource_occupation. user not found.

    E_AQC_QDUDSO_PNF    =   60120   #: quo_daily_user_datasources_occupation. param not found.
    E_AQC_QDUDSO_DSNF   =   60121   #: quo_daily_user_datasources_occupation. datasource not found.
    E_AQC_QDUDSO_USRNF  =   60122   #: quo_daily_user_datasources_occupation. user not found.

    E_AQC_QUTO_DIDNF    =   60130   #: quo_user_total_occupation. did not found.
    E_AQC_QUTO_DSNF     =   60131   #: quo_user_total_occupation. datasource not found.
    E_AQC_QUTO_USRNF    =   60132   #: quo_user_total_occupation. user not found.

    E_AQC_QDUDPC_PNF    =   60140   #: quo_daily_user_data_post_counter invalid parameter
    E_AQC_QDUDPC_DSNF   =   60141   #: quo_daily_user_data_post_counter datasource not found
    E_AQC_QDUDPC_USRNF  =   60142   #: quo_daily_user_data_post_counter user not found

# auth.quotes.deny

    E_AQD_QUTA_UIDNF    =   61000   #: quo_user_total_agents. uid not found.

    E_AQD_QUTDS_UIDNF   =   61010   #: quo_user_total_datasources. uid not found.

    E_AQD_QUTDP_UIDNF   =   61020   #: quo_user_total_datapoints. uid not found.

    E_AQD_QUTW_UIDNF    =   61030   #: quo_user_total_widgets. uid not found.

    E_AQD_QUTDB_UIDNF   =   61040   #: quo_user_total_dashboards. uid not found.

    E_AQD_QATDS_PNF     =   61050   #: quo_agent_total_datasources. param not found.

    E_AQD_QATDP_PNF     =   61060   #: quo_agent_total_datapoints. param not found.

    E_AQD_QDSTDP_PNF    =   61070   #: quo_datasource_total_datapoints. param not found.

    E_AQD_QUTSN_UIDNF   =   61080   #: quo_user_total_snapshots. uid not found.

    E_AQD_QUTC_UIDNF    =   61090   #: quo_user_total_circles. uid not found.

    E_AQD_QCTM_PNF      =   61100   #: quo_circle_total_members. param not found.

    E_AQD_QDDSO_PNF     =   61110   #: quo_daily_datasource_occupation. param not found.
    E_AQD_QDDSO_DSNF    =   61111   #: quo_daily_datasource_occupation. datasource not found.

    E_AQD_QDUDSO_PNF    =   61120   #: quo_daily_user_datasources_occupation. param not found.
    E_AQD_QDUDSO_DSNF   =   61121   #: quo_daily_user_datasources_occupation. datasource not found.

    E_AQD_QUTO_DIDNF    =   61130   #: quo_user_total_occupation. did not found.
    E_AQD_QUTO_DSNF     =   61131   #: quo_user_total_occupation. datasource not found.
    E_AQD_QUTO_USRNF    =   61132   #: quo_user_total_occupation. user not found.

