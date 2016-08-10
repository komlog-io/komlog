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

    E_GUA_GHP_IU    = 10
    E_GUA_GHP_IP    = 11

    E_GUA_AUU_IU    = 20
    E_GUA_AUU_IP    = 21
    E_GUA_AUU_UNF   = 22
    E_GUA_AUU_HPNF  = 23

    E_GUA_CRU_IU    = 30
    E_GUA_CRU_IP    = 31
    E_GUA_CRU_IE    = 32
    E_GUA_CRU_UAEU  = 33
    E_GUA_CRU_UAEE  = 34
    E_GUA_CRU_HPNF  = 35

    E_GUA_COU_IE    = 40
    E_GUA_COU_IC    = 41
    E_GUA_COU_CNF   = 42
    E_GUA_COU_CMM   = 43
    E_GUA_COU_CAU   = 44
    E_GUA_COU_UNF   = 45
    E_GUA_COU_IUE   = 46

    E_GUA_UUC_IU    = 50
    E_GUA_UUC_UNF   = 51
    E_GUA_UUC_EMP   = 52
    E_GUA_UUC_ONP   = 53
    E_GUA_UUC_IP    = 54
    E_GUA_UUC_PNM   = 55
    E_GUA_UUC_EQP   = 56
    E_GUA_UUC_HPNF  = 57
    E_GUA_UUC_IE    = 58
    E_GUA_UUC_EAE   = 59

    E_GUA_GUC_IU    = 70
    E_GUA_GUC_UNF   = 71

    E_GUA_DU_IU     = 80
    E_GUA_DU_UNF    = 81

    E_GUA_GUID_IU   = 85
    E_GUA_GUID_UNF  = 86

    E_GUA_RIR_IEMAIL= 90 #: register invitation request. Invalid Email

    E_GUA_GUI_IEMAIL= 95 #: generate user invitation. Invalid Email

    E_GUA_SIP_IINV  = 110 #: start_invitation_process. invalid invitation.
    E_GUA_SIP_INVNF = 111 #: start_invitation_process. invitation not found.
    E_GUA_SIP_INVAU = 112 #: start_invitation_process. invitation already used
    E_GUA_SIP_EIII  = 113 #: start_invitation_process. error inserting invitation info.
    E_GUA_SIP_ISNE  = 114 #: start_invitation_process. invitation state not expected.

    E_GUA_EIP_IINV  = 120 #: end_invitation_process. invalid invitation.
    E_GUA_EIP_ITRN  = 121 #: end_invitation_process. invalid transaction id.
    E_GUA_EIP_INVNF = 122 #: end_invitation_process. invitation not found.
    E_GUA_EIP_INUE  = 123 #: end_invitation_process. invitation not used.
    E_GUA_EIP_RCF   = 124 #: end_invitation_process. race condition found.
    E_GUA_EIP_SNF   = 125 #: end_invitation_process. state found not valid.
    E_GUA_EIP_EIII  = 126 #: end_invitation_process. error inserting invitation info.

    E_GUA_UIT_IINV  = 130 #: undo_invitation_transactions. invalid invitation.
    E_GUA_UIT_ITRN  = 131 #: undo_invitation_transactions. invalid transaction id.
    E_GUA_UIT_INVNF = 132 #: undo_invitation_transactions. invitation info not found.

    E_GUA_II_IINV   = 135 #: initialize_invitation. invalid invitation.
    E_GUA_II_INVNF  = 136 #: initialize_invitation. invitation info not found.
    E_GUA_II_EIII   = 137 #: initialize_invitation. error inserting invitation info.

    E_GUA_CUI_IINV  = 145 #: check_unused_invitation. invalid invitation.
    E_GUA_CUI_INVNF = 146 #: check_unused_invitation. invitation not found.
    E_GUA_CUI_INVAU = 147 #: check_unused_invitation. invitation already used.
    E_GUA_CUI_INVIS = 148 #: check_unused_invitation. invitation state invalid.

    E_GUA_RFR_IU    = 155 #: register_forget_request. invalid username.
    E_GUA_RFR_IEMAIL= 156 #: register_forget_request. invalid email.
    E_GUA_RFR_NPP   = 157 #: register_forget_request. no param passed.
    E_GUA_RFR_DBE   = 158 #: register_forget_request. database error.
    E_GUA_RFR_UNF   = 159 #: register_forget_request. user not found.

    E_GUA_CUFC_ICODE    = 165 #: check_unused_forget_code. invalid code.
    E_GUA_CUFC_CNF      = 166 #: check_unused_forget_code. code not found.
    E_GUA_CUFC_CODEAU   = 167 #: check_unused_forget_code. code already used.

    E_GUA_RP_ICODE  = 175 #: reset_password. invalid code.
    E_GUA_RP_IPWD   = 176 #: reset_password. invalid password.
    E_GUA_RP_CNF    = 177 #: reset_password. code not found.
    E_GUA_RP_CODEAU = 178 #: reset_password. code already used.
    E_GUA_RP_UNF    = 179 #: reset_password. user not found.
    E_GUA_RP_EUDB   = 180 #: reset_password. error updating database.
    E_GUA_RP_EGPWD  = 181 #: reset_password. error generating new password.

    E_GUA_RPH_IUID  = 200 #: register_pending_hook. invalid uid
    E_GUA_RPH_IURI  = 201 #: register_pending_hook. invalid uri
    E_GUA_RPH_ISID  = 202 #: register_pending_hook. invalid sid
    E_GUA_RPH_UNF   = 203 #: register_pending_hook. user not found

    E_GUA_GUPH_IUID  = 210 #: get_uri_pending_hooks. invalid uid
    E_GUA_GUPH_IURI  = 211 #: get_uri_pending_hooks. invalid uri

    E_GUA_DSPH_ISID  = 220 #: delete_session_pending_hooks. invalid sid

    E_GUA_DUPH_IUID  = 230 #: delete_uri_pending_hooks. invalid uid
    E_GUA_DUPH_IURI  = 231 #: delete_uri_pending_hooks. invalid uri

    E_GUA_DPH_IUID   = 240 #: delete_pending_hook. invalid uid
    E_GUA_DPH_IURI   = 241 #: delete_pending_hook. invalid uri
    E_GUA_DPH_ISID   = 242 #: delete_pending_hook. invalid sid

#gestaccount agent api

    E_GAA_AUA_IA    = 2000
    E_GAA_AUA_IPK   = 2001
    E_GAA_AUA_ANF   = 2002

    E_GAA_CRA_IU    = 2100
    E_GAA_CRA_IA    = 2101
    E_GAA_CRA_IPK   = 2102
    E_GAA_CRA_IV    = 2103
    E_GAA_CRA_AAE   = 2104
    E_GAA_CRA_EIA   = 2105
    E_GAA_CRA_UNF   = 2106

    E_GAA_ACA_IA    = 2200
    E_GAA_ACA_EIA   = 2201
    E_GAA_ACA_ANF   = 2202
    E_GAA_ACA_APKNF = 2203 #: activate_agent: agent public key not found

    E_GAA_SPA_IA    = 2250
    E_GAA_SPA_EIA   = 2251
    E_GAA_SPA_ANF   = 2252
    E_GAA_SPA_APKNF = 2253 #: suspend_agent: agent public key not found

    E_GAA_GACFG_IA  = 2300
    E_GAA_GACFG_IF  = 2301
    E_GAA_GACFG_ANF = 2302

    E_GAA_GASC_IU   = 2400
    E_GAA_GASC_IF   = 2401
    E_GAA_GASC_UNF  = 2402

    E_GAA_UAC_IU    = 2500
    E_GAA_UAC_IA    = 2501
    E_GAA_UAC_IAN   = 2502
    E_GAA_UAC_ANF   = 2503
    E_GAA_UAC_IAE   = 2504

    E_GAA_DA_IA     = 2600
    E_GAA_DA_ANF    = 2601

    E_GAA_GAC_IU    = 2700 #: generate_auth_challenge: invalid user
    E_GAA_GAC_IPK   = 2701 #: generate_auth_challenge: invalid public key
    E_GAA_GAC_UNF   = 2702 #: generate_auth_challenge: user not found
    E_GAA_GAC_ANF   = 2703 #: generate_auth_challenge: agent not found
    E_GAA_GAC_EGC   = 2704 #: generate_auth_challenge: error generating challenge
    E_GAA_GAC_EIDB  = 2705 #: generate_auth_challenge: error inserting challenge in database

    E_GAA_VAC_IU    = 2800 #: validate_auth_challenge: invalid user
    E_GAA_VAC_IPK   = 2801 #: validate_auth_challenge: invalid public key
    E_GAA_VAC_ICH   = 2802 #: validate_auth_challenge: invalid challenge_hash
    E_GAA_VAC_ISG   = 2803 #: validate_auth_challenge: invalid signature
    E_GAA_VAC_UNF   = 2804 #: validate_auth_challenge: user not found
    E_GAA_VAC_ANF   = 2805 #: validate_auth_challenge: agent not found
    E_GAA_VAC_CHNF  = 2806 #: validate_auth_challenge: challenge not found
    E_GAA_VAC_CHAU  = 2807 #: validate_auth_challenge: challenge already used
    E_GAA_VAC_CHEX  = 2808 #: validate_auth_challenge: challenge expired
    E_GAA_VAC_EIDB  = 2809 #: validate_auth_challenge: error inserting in database
    E_GAA_VAC_EVS   = 2810 #: validate_auth_challenge: error validating signature

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

    E_GPA_GDD_IP    = 6600
    E_GPA_GDD_ITD   = 6601
    E_GPA_GDD_IFD   = 6602
    E_GPA_GDD_DDNF  = 6603
    E_GPA_GDD_ICNT  = 6604 #: Invalid count parameter

    E_GPA_CRD_ID    = 6610
    E_GPA_CRD_IDU   = 6611 #: Invalid datapoint uri
    E_GPA_CRD_DNF   = 6612
    E_GPA_CRD_IDE   = 6613
    E_GPA_CRD_ADU   = 6614 #: Uri selected already used
    E_GPA_CRD_AAD   = 6615 #: Datapoint already associated to a datasource
    E_GPA_CRD_UDE   = 6616 #: Error updating datapoint row in database
    E_GPA_CRD_INF   = 6617 #: Data inconsistency found

    E_GPA_GDC_IP    = 6620
    E_GPA_GDC_DNF   = 6621

    E_GPA_UDC_IP    = 6630
    E_GPA_UDC_IDN   = 6631
    E_GPA_UDC_IC    = 6632
    E_GPA_UDC_EMP   = 6633
    E_GPA_UDC_IDE   = 6634
    E_GPA_UDC_DNF   = 6635

    E_GPA_MNV_IP    = 6640
    E_GPA_MNV_IDT   = 6641
    E_GPA_MNV_IPO   = 6642
    E_GPA_MNV_IL    = 6643
    E_GPA_MNV_DNF   = 6644
    E_GPA_MNV_DMNF  = 6645
    E_GPA_MNV_VLNF  = 6646
    E_GPA_MNV_VPNF  = 6647
    E_GPA_MNV_DSNF  = 6648 #: Datapoint is not associated to a datasource

    E_GPA_MPV_IP    = 6660
    E_GPA_MPV_IDT   = 6661
    E_GPA_MPV_IPO   = 6662
    E_GPA_MPV_IL    = 6663
    E_GPA_MPV_DNF   = 6664
    E_GPA_MPV_DMNF  = 6665
    E_GPA_MPV_VLNF  = 6666
    E_GPA_MPV_VPNF  = 6667
    E_GPA_MPV_VAE   = 6668
    E_GPA_MPV_DSNF  = 6669 #: datapoint is not associated to a datasource

    E_GPA_GDT_IP    = 6680
    E_GPA_GDT_DNF   = 6681
    E_GPA_GDT_ETS   = 6682
    E_GPA_GDT_DSNF  = 6683 #: datapoint is not associated to a datasource

    E_GPA_GIDT_IP   = 6686
    E_GPA_GIDT_DNF  = 6687
    E_GPA_GIDT_ETS  = 6688
    E_GPA_GIDT_DSNF = 6689 #: datapoint is not associated to a datasource

    E_GPA_MND_ID    = 6690
    E_GPA_MND_IDT   = 6691
    E_GPA_MND_IPO   = 6692
    E_GPA_MND_IL    = 6693
    E_GPA_MND_IDN   = 6694

    E_GPA_SDPV_IP   = 6700
    E_GPA_SDPV_IDT  = 6701
    E_GPA_SDPV_DNF  = 6702
    E_GPA_SDPV_DTNF = 6703
    E_GPA_SDPV_DMNF = 6704
    E_GPA_SDPV_IDDE = 6705
    E_GPA_SDPV_DSNF = 6706 #: datapoint is not associated to a datasource

    E_GPA_SDSV_ID   = 6710
    E_GPA_SDSV_IDT  = 6711
    E_GPA_SDSV_DSNF = 6712  #: store_datasource_values. datasource not found

    E_GPA_DDP_IP    = 6720
    E_GPA_DDP_DNF   = 6721

    E_GPA_SDMSV_IP      = 6740
    E_GPA_SDMSV_IDT     = 6741
    E_GPA_SDMSV_DNF     = 6742
    E_GPA_SDMSV_DPDTNF  = 6743
    E_GPA_SDMSV_DSMNF   = 6744
    E_GPA_SDMSV_DSNF    = 6745 #: datapoint is not associated to a datasource

    E_GPA_MMDP_IP   = 6750
    E_GPA_MMDP_IDT  = 6751
    E_GPA_MMDP_DNF  = 6752
    E_GPA_MMDP_DMNF = 6753
    E_GPA_MMDP_DSNF = 6754 #: datapoint is not associated to a datasource

    E_GPA_GDH_IDID  = 6760 #: generate_datasource_hash. invalid datasource id
    E_GPA_GDH_IDT   = 6761 #: generate_datasource_hash. invalid date
    E_GPA_GDH_DDNF  = 6762 #: generate_datasource_hash. datasource data not found
    E_GPA_GDH_EIDB  = 6763 #: generate_datasource_hash. error inserting in database
    E_GPA_GDH_NHO   = 6764 #: generate_datasource_hash. no hashed obtained

    E_GPA_SDPSV_IP   = 6800 #: store_user_datapoint_value. Invalid pid
    E_GPA_SDPSV_IDT  = 6801 #: store_user_datapoint_value. Invalid date
    E_GPA_SDPSV_IC   = 6802 #: store_user_datapoint_value. Invalid content
    E_GPA_SDPSV_CVNN = 6803 #: store_user_datapoint_value. content value not numeric
    E_GPA_SDPSV_DNF  = 6804 #: store_user_datapoint_value. datapoint not found
    E_GPA_SDPSV_IDDE = 6805 #: store_user_datapoint_value. insert datapoint data error

    E_GPA_HTDP_IPID     =   6850    #: hook_to_datapoint. invalid pid
    E_GPA_HTDP_ISID     =   6851    #: hook_to_datapoint. invalid sid
    E_GPA_HTDP_DPNF     =   6852    #: hook_to_datapoint. datapoint not found

    E_GPA_UHFDP_IPID    =   6900    #: unhook_from_datapoint. invalid pid
    E_GPA_UHFDP_ISID    =   6901    #: unhook_from_datapoint. invalid sid

    E_GPA_GDPH_IPID     =   6950    #: get_datapoint_hooks. invalid pid
    E_GPA_GDPH_DPNF     =   6951    #: get_datapoint_hooks. datapoint not found

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

