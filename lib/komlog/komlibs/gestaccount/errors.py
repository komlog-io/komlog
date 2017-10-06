'''
In this file we define the different error codes that will be
added to the exceptions in the gestaccount modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for Errors.in this module is 1 - 49999

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

#gestaccount user api

    E_GUA_GHP_IU    = 100
    E_GUA_GHP_IP    = 101

    E_GUA_AUU_IU    = 200
    E_GUA_AUU_IP    = 201
    E_GUA_AUU_UNF   = 202
    E_GUA_AUU_HPNF  = 203
    E_GUA_AUU_UNA   = 204 #: user not in active state

    E_GUA_CRU_IU            = 300
    E_GUA_CRU_IP            = 301
    E_GUA_CRU_IE            = 302
    E_GUA_CRU_UAEU          = 303
    E_GUA_CRU_UAEE          = 304
    E_GUA_CRU_HPNF          = 305
    E_GUA_CRU_ISID          = 306 #: invalid sid
    E_GUA_CRU_ITOK          = 307 #: invalid token
    E_GUA_CRU_SEGNF         = 308 #: segment not found
    E_GUA_CRU_TOKNEED       = 309 #: token needed
    E_GUA_CRU_ECREPAY       = 310 #: error creating payment profile
    E_GUA_CRU_IINV          = 311 #: invalid invitation id
    E_GUA_CRU_INVNF         = 312 #: invitation not found
    E_GUA_CRU_INVMXCNTRCH   = 313 #: invitation used max count reached
    E_GUA_CRU_OUTINVINT     = 314 #: out of invitation active interval

    E_GUA_COU_IE    = 400
    E_GUA_COU_IC    = 401
    E_GUA_COU_CNF   = 402
    E_GUA_COU_CMM   = 403
    E_GUA_COU_CAU   = 404
    E_GUA_COU_UNF   = 405
    E_GUA_COU_IUE   = 406

    E_GUA_UPDSEG_IUID       = 450 #: invalid uid
    E_GUA_UPDSEG_ISID       = 451 #: invalid segment
    E_GUA_UPDSEG_ITOK       = 452 #: invalid token
    E_GUA_UPDSEG_UNF        = 453 #: user not found
    E_GUA_UPDSEG_SEGNF      = 454 #: segment not found
    E_GUA_UPDSEG_TRNTAL     = 455 #: transition not allowed
    E_GUA_UPDSEG_TOKNEED    = 456 #: token needed
    E_GUA_UPDSEG_EUPAY      = 457 #: error updating payment profile
    E_GUA_UPDSEG_EUDB       = 458 #: error updating database

    E_GUA_UUC_IU    = 500
    E_GUA_UUC_UNF   = 501
    E_GUA_UUC_EMP   = 502
    E_GUA_UUC_ONP   = 503
    E_GUA_UUC_IP    = 504
    E_GUA_UUC_PNM   = 505
    E_GUA_UUC_EQP   = 506
    E_GUA_UUC_HPNF  = 507
    E_GUA_UUC_IE    = 508
    E_GUA_UUC_EAE   = 509

    E_GUA_GUC_IU    = 600
    E_GUA_GUC_UNF   = 601

    E_GUA_DU_IU     = 700
    E_GUA_DU_UNF    = 701

    E_GUA_GUID_IU   = 800
    E_GUA_GUID_UNF  = 801

    E_GUA_RIR_IEMAIL= 900 #: register invitation request. Invalid Email
    E_GUA_RIR_UAUAI = 901 #: register invitation request. user already used an invitation

    E_GUA_GUI_IEMAIL= 950 #: generate user invitations. Invalid Email
    E_GUA_GUI_ECINV = 951 #: generate user invitations. Error creating invitation info
    E_GUA_GUI_UAUAI = 952 #: generate user invitations. user already used an invitation

    E_GUA_CUI_IINV          = 1400 #: check_unused_invitation. invalid invitation.
    E_GUA_CUI_INVNF         = 1401 #: check_unused_invitation. invitation not found.
    E_GUA_CUI_INVMXCNTRCH   = 1402 #: check_unused_invitation. invitation max used count reached.
    E_GUA_CUI_OUTINVINT     = 1403 #: check_unused_invitation. out of invitation active interval

    E_GUA_RFR_IU    = 1500 #: register_forget_request. invalid username.
    E_GUA_RFR_IEMAIL= 1501 #: register_forget_request. invalid email.
    E_GUA_RFR_NPP   = 1502 #: register_forget_request. no param passed.
    E_GUA_RFR_DBE   = 1503 #: register_forget_request. database error.
    E_GUA_RFR_UNF   = 1504 #: register_forget_request. user not found.

    E_GUA_CUFC_ICODE    = 1600 #: check_unused_forget_code. invalid code.
    E_GUA_CUFC_CNF      = 1601 #: check_unused_forget_code. code not found.
    E_GUA_CUFC_CODEAU   = 1602 #: check_unused_forget_code. code already used.

    E_GUA_RP_ICODE  = 1700 #: reset_password. invalid code.
    E_GUA_RP_IPWD   = 1701 #: reset_password. invalid password.
    E_GUA_RP_CNF    = 1702 #: reset_password. code not found.
    E_GUA_RP_CODEAU = 1703 #: reset_password. code already used.
    E_GUA_RP_UNF    = 1704 #: reset_password. user not found.
    E_GUA_RP_EUDB   = 1705 #: reset_password. error updating database.
    E_GUA_RP_EGPWD  = 1706 #: reset_password. error generating new password.

    E_GUA_RPH_IUID  = 1800 #: register_pending_hook. invalid uid
    E_GUA_RPH_IURI  = 1801 #: register_pending_hook. invalid uri
    E_GUA_RPH_ISID  = 1802 #: register_pending_hook. invalid sid
    E_GUA_RPH_UNF   = 1803 #: register_pending_hook. user not found

    E_GUA_GUPH_IUID  = 1820 #: get_uri_pending_hooks. invalid uid
    E_GUA_GUPH_IURI  = 1821 #: get_uri_pending_hooks. invalid uri

    E_GUA_DSPH_ISID  = 1850 #: delete_session_pending_hooks. invalid sid

    E_GUA_DUPH_IUID  = 1900 #: delete_uri_pending_hooks. invalid uid
    E_GUA_DUPH_IURI  = 1901 #: delete_uri_pending_hooks. invalid uri

    E_GUA_DPH_IUID   = 1950 #: delete_pending_hook. invalid uid
    E_GUA_DPH_IURI   = 1951 #: delete_pending_hook. invalid uri
    E_GUA_DPH_ISID   = 1952 #: delete_pending_hook. invalid sid

    E_GUA_GUSEGINF_IUID = 2000 #: get_user_segment_info. invalid uid
    E_GUA_GUSEGINF_UNF  = 2001 #: get_user_segment_info. user not found

#gestaccount agent api

    E_GAA_AUA_IA    = 3000
    E_GAA_AUA_IPK   = 3001
    E_GAA_AUA_ANF   = 3002

    E_GAA_CRA_IU    = 3100
    E_GAA_CRA_IA    = 3101
    E_GAA_CRA_IPK   = 3102
    E_GAA_CRA_IV    = 3103
    E_GAA_CRA_AAE   = 3104
    E_GAA_CRA_EIA   = 3105
    E_GAA_CRA_UNF   = 3106

    E_GAA_ACA_IA    = 3200
    E_GAA_ACA_EIA   = 3201
    E_GAA_ACA_ANF   = 3202
    E_GAA_ACA_APKNF = 3203 #: activate_agent: agent public key not found

    E_GAA_SPA_IA    = 3250
    E_GAA_SPA_EIA   = 3251
    E_GAA_SPA_ANF   = 3252
    E_GAA_SPA_APKNF = 3253 #: suspend_agent: agent public key not found

    E_GAA_GACFG_IA  = 3300
    E_GAA_GACFG_IF  = 3301
    E_GAA_GACFG_ANF = 3302

    E_GAA_GASC_IU   = 3400
    E_GAA_GASC_IF   = 3401
    E_GAA_GASC_UNF  = 3402

    E_GAA_UAC_IU    = 3500
    E_GAA_UAC_IA    = 3501
    E_GAA_UAC_IAN   = 3502
    E_GAA_UAC_ANF   = 3503
    E_GAA_UAC_IAE   = 3504

    E_GAA_DA_IA     = 3600
    E_GAA_DA_ANF    = 3601

    E_GAA_GAC_IU    = 3700 #: generate_auth_challenge: invalid user
    E_GAA_GAC_IPK   = 3701 #: generate_auth_challenge: invalid public key
    E_GAA_GAC_UNF   = 3702 #: generate_auth_challenge: user not found
    E_GAA_GAC_ANF   = 3703 #: generate_auth_challenge: agent not found
    E_GAA_GAC_EGC   = 3704 #: generate_auth_challenge: error generating challenge
    E_GAA_GAC_EIDB  = 3705 #: generate_auth_challenge: error inserting challenge in database
    E_GAA_GAC_IAS   = 3706 #: generate_auth_challenge: invalid agent state

    E_GAA_VAC_IU    = 3800 #: validate_auth_challenge: invalid user
    E_GAA_VAC_IPK   = 3801 #: validate_auth_challenge: invalid public key
    E_GAA_VAC_ICH   = 3802 #: validate_auth_challenge: invalid challenge_hash
    E_GAA_VAC_ISG   = 3803 #: validate_auth_challenge: invalid signature
    E_GAA_VAC_UNF   = 3804 #: validate_auth_challenge: user not found
    E_GAA_VAC_ANF   = 3805 #: validate_auth_challenge: agent not found
    E_GAA_VAC_CHNF  = 3806 #: validate_auth_challenge: challenge not found
    E_GAA_VAC_CHAU  = 3807 #: validate_auth_challenge: challenge already used
    E_GAA_VAC_CHEX  = 3808 #: validate_auth_challenge: challenge expired
    E_GAA_VAC_EIDB  = 3809 #: validate_auth_challenge: error inserting in database
    E_GAA_VAC_EVS   = 3810 #: validate_auth_challenge: error validating signature
    E_GAA_VAC_IAS   = 3811 #: validate_auth_challenge: invalid agent state

# gestaccount datasource api

    E_GDA_CRD_IU    = 4400
    E_GDA_CRD_IA    = 4401
    E_GDA_CRD_IDN   = 4402
    E_GDA_CRD_UNF   = 4403
    E_GDA_CRD_ANF   = 4404
    E_GDA_CRD_IDE   = 4405
    E_GDA_CRD_ADU   = 4406

    E_GDA_UDD_ID    = 4420
    E_GDA_UDD_IDC   = 4421
    E_GDA_UDD_IDD   = 4422
    E_GDA_UDD_IFD   = 4423
    E_GDA_UDD_ESD   = 4424
    E_GDA_UDD_DNF   = 4425

    E_GDA_GDD_ID    = 4430  #: get_datasource_data. invalid did
    E_GDA_GDD_IFD   = 4431  #: get_datasource_data. invalid fromdate
    E_GDA_GDD_ITD   = 4432  #: get_datasource_data. invalid todate
    E_GDA_GDD_ICNT  = 4433  #: get_datasource_data. invalid count
    E_GDA_GDD_DDNF  = 4434  #: get_datasource_data. datasource data not found

    E_GDA_GMDD_ID   = 4435  #: get_mapped_datasource_data. invalid did
    E_GDA_GMDD_IFD  = 4436  #: get_mapped_datasource_data. invalid fromdate
    E_GDA_GMDD_ITD  = 4437  #: get_mapped_datasource_data. invalid todate
    E_GDA_GMDD_ICNT = 4438  #: get_mapped_datasource_data. invalid count
    E_GDA_GMDD_DDNF = 4439  #: get_mapped_datasource_data. datasource data not found

    E_GDA_GDC_ID    = 4440
    E_GDA_GDC_DNF   = 4441

    E_GDA_GDSC_IU   = 4450
    E_GDA_GDSC_UNF  = 4451

    E_GDA_UDS_ID    = 4460
    E_GDA_UDS_IDN   = 4461
    E_GDA_UDS_IDE   = 4462
    E_GDA_UDS_DNF   = 4463

    E_GDA_GDM_ID    = 4470
    E_GDA_GDM_IDT   = 4471
    E_GDA_GDM_DDNF  = 4472

    E_GDA_DD_ID     = 4480
    E_GDA_DD_DNF    = 4481

    E_GDA_HTDS_IDID     =   4500    #: hook_to_datasource. invalid did
    E_GDA_HTDS_ISID     =   4501    #: hook_to_datasource. invalid sid
    E_GDA_HTDS_DSNF     =   4502    #: hook_to_datasource. datasource not found

    E_GDA_UHFDS_IDID    =   4550    #: unhook_from_datasource. invalid did
    E_GDA_UHFDS_ISID    =   4551    #: unhook_from_datasource. invalid sid

    E_GDA_GDSH_IDID     =   4600    #: get_datasource_hooks. invalid sid
    E_GDA_GDSH_DSNF     =   4601    #: get_datasource_hooks. datasource not found

    E_GDA_UDSSUP_IDID   =   4650    #: update_datasource_supplies. invalid did
    E_GDA_UDSSUP_ISUPT  =   4651    #: update_datasource_supplies. invalid supplies type
    E_GDA_UDSSUP_ISUPI  =   4652    #: update_datasource_supplies. invalid supplies item
    E_GDA_UDSSUP_DSNF   =   4653    #: update_datasource_supplies. datasource not found

    E_GDA_GDSSUP_IDID   =   4700    #: get_datasource_supplies. invalid did
    E_GDA_GDSSUP_ICNT   =   4701    #: get_datasource_supplies. invalid count

    E_GDA_UDDSF_IDID    =   4725    #: update_datasource_features. invalid did

# gestaccount datapoint api


    E_GPA_CRUD_IU   = 6000 #: invalid uid
    E_GPA_CRUD_IDU  = 6001 #: invalid datapoint uri
    E_GPA_CRUD_UNF  = 6002 #: user not found
    E_GPA_CRUD_UAE  = 6003 #: uri already used
    E_GPA_CRUD_IDE  = 6004 #: error inserting to database

    E_GPA_GDTS_ID   = 6050
    E_GPA_GDTS_IDT  = 6051
    E_GPA_GDTS_DDNF = 6052

    E_GPA_GDNDFD_IP     = 6100
    E_GPA_GDNDFD_DNF    = 6101
    E_GPA_GDNDFD_NDF    = 6102
    E_GPA_GDNDFD_DSDNF  = 6103
    E_GPA_GDNDFD_DSNF   = 6104 #: datapoint is not associated to a datasource

    E_GPA_SDAIS_IP      = 6150
    E_GPA_SDAIS_IDT     = 6151
    E_GPA_SDAIS_DNF     = 6152
    E_GPA_SDAIS_DSNDNF  = 6153
    E_GPA_SDAIS_DSTSNF  = 6154
    E_GPA_SDAIS_DSNF    = 6155 #: datapoint is not associated to a datasource

    E_GPA_CMDIS_ID      = 6200
    E_GPA_CMDIS_IDT     = 6201
    E_GPA_CMDIS_DSMNF   = 6202
    E_GPA_CMDIS_DSTSNF  = 6203

    E_GPA_GDD_IP    = 6250
    E_GPA_GDD_ITD   = 6251
    E_GPA_GDD_IFD   = 6252
    E_GPA_GDD_DDNF  = 6253
    E_GPA_GDD_ICNT  = 6254 #: Invalid count parameter

    E_GPA_CRD_ID    = 6300
    E_GPA_CRD_IDU   = 6301 #: Invalid datapoint uri
    E_GPA_CRD_DNF   = 6302
    E_GPA_CRD_IDE   = 6303
    E_GPA_CRD_ADU   = 6304 #: Uri selected already used
    E_GPA_CRD_AAD   = 6305 #: Datapoint already associated to a datasource
    E_GPA_CRD_UDE   = 6306 #: Error updating datapoint row in database
    E_GPA_CRD_INF   = 6307 #: Data inconsistency found

    E_GPA_GDC_IP    = 6350
    E_GPA_GDC_DNF   = 6351

    E_GPA_UDC_IP    = 6400
    E_GPA_UDC_IDN   = 6401
    E_GPA_UDC_IC    = 6402
    E_GPA_UDC_EMP   = 6403
    E_GPA_UDC_IDE   = 6404
    E_GPA_UDC_DNF   = 6405

    E_GPA_MNV_IP    = 6450
    E_GPA_MNV_IDT   = 6451
    E_GPA_MNV_IPO   = 6452
    E_GPA_MNV_IL    = 6453
    E_GPA_MNV_DNF   = 6454
    E_GPA_MNV_DMNF  = 6455
    E_GPA_MNV_VLNF  = 6456
    E_GPA_MNV_VPNF  = 6457
    E_GPA_MNV_DSNF  = 6458 #: Datapoint is not associated to a datasource

    E_GPA_MPV_IP    = 6500
    E_GPA_MPV_IDT   = 6501
    E_GPA_MPV_IPO   = 6502
    E_GPA_MPV_IL    = 6503
    E_GPA_MPV_DNF   = 6504
    E_GPA_MPV_DMNF  = 6505
    E_GPA_MPV_VLNF  = 6506
    E_GPA_MPV_VPNF  = 6507
    E_GPA_MPV_VAE   = 6508
    E_GPA_MPV_DSNF  = 6509 #: datapoint is not associated to a datasource

    E_GPA_GDT_IDID  = 6550 #: generate_decision_tree: invalid did
    E_GPA_GDT_DSNF  = 6551 #: generate_decision_tree: datasource not found
    E_GPA_GDT_ETS   = 6552 #: generate_decision_tree: empty training set
    E_GPA_GDT_EGDT  = 6554 #: generate_decision_tree: error generating decision tree

    E_GPA_GIDT_IP   = 6600
    E_GPA_GIDT_DNF  = 6601
    E_GPA_GIDT_ETS  = 6602
    E_GPA_GIDT_DSNF = 6603 #: generate_inverse_decision_tree: datapoint not associated to a ds
    E_GPA_GIDT_EGDT = 6604 #: generate_inverse_decision_tree: error generating decision tree

    E_GPA_MND_ID    = 6650
    E_GPA_MND_IDT   = 6651
    E_GPA_MND_IPO   = 6652
    E_GPA_MND_IL    = 6653
    E_GPA_MND_IDN   = 6654
    E_GPA_MND_DTE   = 6655  #: monitor new datapoint: error generating datasource dtree

    E_GPA_SDPV_IP   = 6700
    E_GPA_SDPV_IDT  = 6701
    E_GPA_SDPV_DNF  = 6702
    E_GPA_SDPV_DTNF = 6703
    E_GPA_SDPV_IDDE = 6704
    E_GPA_SDPV_DSNF = 6705 #: datapoint is not associated to a datasource

    E_GPA_SDSV_ID   = 6750
    E_GPA_SDSV_IDT  = 6751
    E_GPA_SDSV_DSNF = 6752  #: store_datasource_values. datasource not found

    E_GPA_DDP_IP    = 6800
    E_GPA_DDP_DNF   = 6801

    E_GPA_SDMSV_IP      = 6850
    E_GPA_SDMSV_IDT     = 6851
    E_GPA_SDMSV_DNF     = 6852
    E_GPA_SDMSV_DPDTNF  = 6853
    E_GPA_SDMSV_DSMNF   = 6854
    E_GPA_SDMSV_DSNF    = 6855 #: datapoint is not associated to a datasource

    E_GPA_MMDP_IP   = 6900
    E_GPA_MMDP_IDT  = 6901
    E_GPA_MMDP_DNF  = 6902
    E_GPA_MMDP_DMNF = 6903
    E_GPA_MMDP_DSNF = 6904 #: datapoint is not associated to a datasource

    E_GPA_GDH_IDID  = 6950 #: generate_datasource_hash. invalid datasource id
    E_GPA_GDH_IDT   = 6951 #: generate_datasource_hash. invalid date
    E_GPA_GDH_DDNF  = 6952 #: generate_datasource_hash. datasource data not found
    E_GPA_GDH_EIDB  = 6953 #: generate_datasource_hash. error inserting in database
    E_GPA_GDH_NHO   = 6954 #: generate_datasource_hash. no hashed obtained

    E_GPA_SDPSV_IP   = 7000 #: store_user_datapoint_value. Invalid pid
    E_GPA_SDPSV_IDT  = 7001 #: store_user_datapoint_value. Invalid date
    E_GPA_SDPSV_IC   = 7002 #: store_user_datapoint_value. Invalid content
    E_GPA_SDPSV_CVNN = 7003 #: store_user_datapoint_value. content value not numeric
    E_GPA_SDPSV_DNF  = 7004 #: store_user_datapoint_value. datapoint not found
    E_GPA_SDPSV_IDDE = 7005 #: store_user_datapoint_value. insert datapoint data error

    E_GPA_HTDP_IPID     =   7050    #: hook_to_datapoint. invalid pid
    E_GPA_HTDP_ISID     =   7051    #: hook_to_datapoint. invalid sid
    E_GPA_HTDP_DPNF     =   7052    #: hook_to_datapoint. datapoint not found

    E_GPA_UHFDP_IPID    =   7100    #: unhook_from_datapoint. invalid pid
    E_GPA_UHFDP_ISID    =   7101    #: unhook_from_datapoint. invalid sid

    E_GPA_GDPH_IPID     =   7150    #: get_datapoint_hooks. invalid pid
    E_GPA_GDPH_DPNF     =   7151    #: get_datapoint_hooks. datapoint not found

    E_GPA_MIU_IDID      =   7200    #: monitor_identified_uris. invalid did
    E_GPA_MIU_IDATE     =   7201    #: monitor_identified_uris. invalid date
    E_GPA_MIU_DSNF      =   7202    #: monitor_identified_uris. datasource not found
    E_GPA_MIU_DTRNF     =   7203    #: monitor_identified_uris. dtree not found

    E_GPA_SDTDS_IDID    =   7250    #: select_dtree_for_datasource. invalid did
    E_GPA_SDTDS_DSNF    =   7251    #: select_dtree_for_datasource. datasource not found

# gestaccount widget api

    E_GWA_GWC_IW    = 8900
    E_GWA_GWC_WNF   = 8901

    E_GWA_GWSC_IU   = 8910
    E_GWA_GWSC_UNF  = 8911

    E_GWA_DW_IW     = 8920
    E_GWA_DW_WNF    = 8921

    E_GWA_NWDS_IU   = 8930
    E_GWA_NWDS_ID   = 8931
    E_GWA_NWDS_UNF  = 8932
    E_GWA_NWDS_DNF  = 8933
    E_GWA_NWDS_WAE  = 8934
    E_GWA_NWDS_IWE  = 8935

    E_GWA_NWDP_IU   = 8940
    E_GWA_NWDP_ID   = 8941
    E_GWA_NWDP_UNF  = 8942
    E_GWA_NWDP_DNF  = 8943
    E_GWA_NWDP_WAE  = 8944
    E_GWA_NWDP_IWE  = 8945
    E_GWA_NWDP_DSNF = 8946

    E_GWA_NWH_IU    = 8950
    E_GWA_NWH_IWN   = 8951
    E_GWA_NWH_UNF   = 8952
    E_GWA_NWH_IWE   = 8953

    E_GWA_NWL_IU    = 8960
    E_GWA_NWL_IWN   = 8961
    E_GWA_NWL_UNF   = 8962
    E_GWA_NWL_IWE   = 8963

    E_GWA_NWT_IU    = 8970
    E_GWA_NWT_IWN   = 8971
    E_GWA_NWT_UNF   = 8972
    E_GWA_NWT_IWE   = 8973

    E_GWA_NWMP_IU   = 8975 #new_widget_multidp invalid uid
    E_GWA_NWMP_IWN  = 8976 #new_widget_multidp invalid widgetname
    E_GWA_NWMP_UNF  = 8977 #new_widget_multidp user not found
    E_GWA_NWMP_IWE  = 8978 #new_widget_multidp error inserting widget in db

    E_GWA_ADTW_IW   = 8980
    E_GWA_ADTW_IP   = 8981
    E_GWA_ADTW_WNF  = 8982
    E_GWA_ADTW_DNF  = 8983
    E_GWA_ADTW_IDHE = 8984
    E_GWA_ADTW_IDLE = 8985
    E_GWA_ADTW_IDTE = 8986
    E_GWA_ADTW_WUO  = 8987
    E_GWA_ADTW_IDMPE= 8988 #add_datapoint_to_widget error in db adding to widget multidp

    E_GWA_DDFW_IW   = 8000
    E_GWA_DDFW_IP   = 8001
    E_GWA_DDFW_WNF  = 8002
    E_GWA_DDFW_DNF  = 8003
    E_GWA_DDFW_IDHE = 8004
    E_GWA_DDFW_IDLE = 8005
    E_GWA_DDFW_IDTE = 8006
    E_GWA_DDFW_WUO  = 8007
    E_GWA_DDFW_IDMPE= 8008 #delete_datapoint_from_widget error in db deleting dp from multidp

    E_GWA_UWC_IW    = 8020
    E_GWA_UWC_IWN   = 8021
    E_GWA_UWC_IC    = 8022
    E_GWA_UWC_WNF   = 8023
    E_GWA_UWC_WUO   = 8024
    E_GWA_UWC_IAV   = 8025 #update_widget_config error in active_visualization parameter validation

    E_GWA_UWDS_IW   = 8030
    E_GWA_UWDS_IWN  = 8031
    E_GWA_UWDS_WNF  = 8032

    E_GWA_UWDP_IW   = 8040
    E_GWA_UWDP_IWN  = 8041
    E_GWA_UWDP_WNF  = 8042

    E_GWA_UWH_IW    = 8050
    E_GWA_UWH_IWN   = 8051
    E_GWA_UWH_ICD   = 8052
    E_GWA_UWH_WNF   = 8053
    E_GWA_UWH_DNF   = 8054
    E_GWA_UWH_IC    = 8055

    E_GWA_UWL_IW    = 8060
    E_GWA_UWL_IWN   = 8061
    E_GWA_UWL_ICD   = 8062
    E_GWA_UWL_WNF   = 8063
    E_GWA_UWL_DNF   = 8064
    E_GWA_UWL_IC    = 8065

    E_GWA_UWT_IW    = 8070
    E_GWA_UWT_IWN   = 8071
    E_GWA_UWT_ICD   = 8072
    E_GWA_UWT_WNF   = 8073
    E_GWA_UWT_DNF   = 8074
    E_GWA_UWT_IC    = 8075

    E_GWA_UWMP_IW   = 8080 #update_widget_multidp invalid wid parameter
    E_GWA_UWMP_IWN  = 8081 #update_widget_multidp invalid widgetname parameter
    E_GWA_UWMP_IAV  = 8082 #update_widget_multidp invalid active_visualization parameter
    E_GWA_UWMP_WNF  = 8083 #update_widget_multidp widget not found
    E_GWA_UWMP_IAVT = 8084 #update_widget_multidp non available visualization type for widget

    E_GWA_GRW_IW    = 8090

# gestaccount dashboard api

    E_GBA_GDSC_IU   = 10300
    E_GBA_GDSC_UNF  = 10301

    E_GBA_GDC_IB    = 10310
    E_GBA_GDC_DNF   = 10311

    E_GBA_DD_IB     = 10320
    E_GBA_DD_DNF    = 10321

    E_GBA_CRD_IU    = 10330
    E_GBA_CRD_IDN   = 10331
    E_GBA_CRD_UNF   = 10332
    E_GBA_CRD_IDE   = 10333

    E_GBA_UDC_IB    = 10340
    E_GBA_UDC_IDN   = 10341
    E_GBA_UDC_DNF   = 10342
    E_GBA_UDC_IDE   = 10343

    E_GBA_AWTD_IB   = 10350
    E_GBA_AWTD_IW   = 10351
    E_GBA_AWTD_DNF  = 10352
    E_GBA_AWTD_WNF  = 10353

    E_GBA_DWFD_IB   = 10360
    E_GBA_DWFD_IW   = 10361
    E_GBA_DWFD_DNF  = 10362

# gestaccount snapshot api

    E_GSA_GSC_IN    = 12500
    E_GSA_GSC_SNF   = 12501

    E_GSA_GSSC_IU   = 12510
    E_GSA_GSSC_UNF  = 12511

    E_GSA_GSD_IN    = 12520

    E_GSA_DS_IN     = 12530
    E_GSA_DS_SNF    = 12531

    E_GSA_NS_IU     = 12540
    E_GSA_NS_IW     = 12541
    E_GSA_NS_III    = 12542
    E_GSA_NS_IIE    = 12543
    E_GSA_NS_IIO    = 12544 #  new_snapshot invalid interval order. interval_init > interval_end
    E_GSA_NS_ISWU   = 12545 #: new_snapshot. Invalid shared_with_users parameter. (DEPRECATED)
    E_GSA_NS_ISWC   = 12546 #: new_snapshot. Invalid shared_with_uids parameter. (DEPRECATED)
    E_GSA_NS_UNF    = 12547
    E_GSA_NS_WNF    = 12548
    E_GSA_NS_SCE    = 12549
    E_GSA_NS_ESL    = 12550 #: new_snapshot. Empty sharing list error. (DEPRECATED)

    E_GSA_NSDS_WNF  = 12560
    E_GSA_NSDS_SCE  = 12561
    E_GSA_NSDS_DNF  = 12562 #new_snapshot_datasource datasource info not found

    E_GSA_NSDP_WNF  = 12570
    E_GSA_NSDP_SCE  = 12571
    E_GSA_NSDP_PNF  = 12572 #new_snapshot_datapoint datapoint info not found

    E_GSA_NSH_WNF   = 12580
    E_GSA_NSH_ZDP   = 12581
    E_GSA_NSH_SCE   = 12582

    E_GSA_NSL_WNF   = 12590
    E_GSA_NSL_ZDP   = 12591
    E_GSA_NSL_SCE   = 12592

    E_GSA_NST_WNF   = 12600
    E_GSA_NST_ZDP   = 12601
    E_GSA_NST_SCE   = 12602

    E_GSA_NSMP_WNF  = 12610
    E_GSA_NSMP_ZDP  = 12611
    E_GSA_NSMP_SCE  = 12612
    E_GSA_NSMP_ZDPF = 12613

# gestaccount circle api

    E_GCA_GUCC_IC   = 14800
    E_GCA_GUCC_CNF  = 14801

    E_GCA_GUCSC_IU  = 14810
    E_GCA_GUCSC_UNF = 14811

    E_GCA_DC_IC     = 14820
    E_GCA_DC_CNF    = 14821

    E_GCA_NUC_IU    = 14830
    E_GCA_NUC_ICN   = 14831
    E_GCA_NUC_IML   = 14832
    E_GCA_NUC_UNF   = 14833
    E_GCA_NUC_ICE   = 14834

    E_GCA_UC_IC     = 14840
    E_GCA_UC_ICN    = 14841
    E_GCA_UC_CNF    = 14842
    E_GCA_UC_ICE    = 14843

    E_GCA_AUTC_IC   = 14850
    E_GCA_AUTC_IU   = 14851
    E_GCA_AUTC_CNF  = 14852
    E_GCA_AUTC_UNF  = 14853
    E_GCA_AUTC_AME  = 14854

    E_GCA_DUFC_IC   = 14860
    E_GCA_DUFC_IU   = 14861
    E_GCA_DUFC_CNF  = 14862
    E_GCA_DUFC_UNF  = 14863
    E_GCA_DUFC_AME  = 14864


#gestaccount common delete

    E_GCD_DU_IU       = 16000 #delete_user invalid uid parameter
    E_GCD_DU_UNF      = 16001 #delete_user user not found

    E_GCD_DA_IA       = 16100 #delete_agent invalid aid parameter

    E_GCD_DDS_ID      = 16200 #delete_datasource invalid did parameter

    E_GCD_DDP_IP      = 16300 #delete_datapoint invalid pid parameter

    E_GCD_DW_IW       = 16400 #delete_widget invalid wid parameter

    E_GCD_DDB_IB      = 16500 #delete_dashboard invalid bid parameter

    E_GCD_DC_IC       = 16600 #delete_circle invalid cid parameter

    E_GCD_DN_IN       = 16700 #delete_snapshot invalid nid parameter

    E_GCD_DDPFDS_IP   = 16800 #: dissociate_datapoint_from_datasource: invalid pid
    E_GCD_DDPFDS_DPNF = 16801 #: dissociate_datapoint_from_datasource: datapoint not found

    E_GCD_DDPDA_IPID  = 16900 #: delete_datapoint_data_at: invalid pid
    E_GCD_DDPDA_IDATE = 16901 #: delete_datapoint_data_at: invalid date

    E_GCD_DDSDA_IDID  = 16950 #: delete_datasource_data_at: invalid did
    E_GCD_DDSDA_IDATE = 16951 #: delete_datasource_data_at: invalid date

