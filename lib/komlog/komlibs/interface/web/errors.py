'''
In this file we define the different error codes that will be
added to the exceptions in the interface web modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for Errors.in this module is 100000 - 150000 

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

#interface web api user

    E_IWAU_NUSR_IU      = 100000
    E_IWAU_NUSR_IP      = 100001
    E_IWAU_NUSR_IE      = 100002
    E_IWAU_NUSR_IINV    = 100003 #: new_user_request invalid (malformed) invitation
    E_IWAU_NUSR_INVNF   = 100004 #: new_user_request invitation not found
    E_IWAU_NUSR_INVAU   = 100005 #: new_user_request invitation already used
    E_IWAU_NUSR_UAEU    = 100006 #: new_user_request user already exists (username)
    E_IWAU_NUSR_UAEE    = 100007 #: new_user_request user already exists (email)

    E_IWAU_CUSR_IE      = 100010
    E_IWAU_CUSR_IC      = 100011

    E_IWAU_GUSCR_IPSP   = 100015

    E_IWAU_UUSCR_IPSP   = 100020
    E_IWAU_UUSCR_ID     = 100021
    E_IWAU_UUSCR_IE     = 100022
    E_IWAU_UUSCR_INP    = 100023
    E_IWAU_UUSCR_IOP    = 100024
    E_IWAU_UUSCR_ONPR   = 100025 #: only new_password received
    E_IWAU_UUSCR_OOPR   = 100026 #: only old_password received
    E_IWAU_UUSCR_NPEOP  = 100027 #: new_password equals old_password

    E_IWAU_DUSR_IPSP=100030

    E_IWAU_RIR_IEMAIL=100040

    E_IWAU_CIR_IINV=100050
    E_IWAU_CIR_INVNF=100051
    E_IWAU_CIR_INVAU=100052

    E_IWAU_SIR_IEMAIL=100060
    E_IWAU_SIR_INUM=100061

    E_IWAU_RFR_IACCOUNT=100070 #: register_forget_request: invalid account received
    E_IWAU_RFR_UNF=100071 #: register_forget_request: user not found

    E_IWAU_CFR_ICODE=100080 #: check_forget_code_request: invalid code
    E_IWAU_CFR_CNF=100081 #: check_forget_code_request: code not found
    E_IWAU_CFR_CODEAU=100082 #: check_forget_code_request: code already used

    E_IWAU_RPR_ICODE=100090 #: reset_password_request: invalid code
    E_IWAU_RPR_IPWD=100091 #: reset_password_request: invalid password
    E_IWAU_RPR_UNF=100092 #: reset_password_request: user not found.
    E_IWAU_RPR_CNF=100093 #: reset_password_request: code not found
    E_IWAU_RPR_CODEAU=100094 #: reset_password_request: code already used.

#interface web api agent

    E_IWAA_NAGR_IPSP=100200
    E_IWAA_NAGR_IAN=100201
    E_IWAA_NAGR_IPK=100202
    E_IWAA_NAGR_IV=100203
    E_IWAA_NAGR_AUTHERR=100204 #new_agent_request error in update_resources

    E_IWAA_GAGSCR_IPSP=100210

    E_IWAA_GAGCR_IPSP=100215
    E_IWAA_GAGCR_IA=100216

    E_IWAA_UAGCR_IPSP=100220
    E_IWAA_UAGCR_IA=100221
    E_IWAA_UAGCR_ID=100222
    E_IWAA_UAGCR_IAN=100223

    E_IWAA_DAGR_IPSP=100230
    E_IWAA_DAGR_IA=100231


#interface web api datasource

    E_IWADS_GDSDR_IPSP = 100400
    E_IWADS_GDSDR_ID   = 100401
    E_IWADS_GDSDR_IS   = 100402
    E_IWADS_GDSDR_IT   = 100403
    E_IWADS_GDSDR_LDBL = 100404  #: get_datasource_data_request. Last date retrieved is before allowed limit.

    E_IWADS_UDSDR_IPSP=100410
    E_IWADS_UDSDR_IA=100411
    E_IWADS_UDSDR_ID=100412
    E_IWADS_UDSDR_IDC=100413
    E_IWADS_UDSDR_IDST=100414

    E_IWADS_GDSSCR_IPSP=100420

    E_IWADS_GDSCR_IPSP=100425
    E_IWADS_GDSCR_ID=100426

    E_IWADS_UDSCR_IPSP=100430
    E_IWADS_UDSCR_ID=100431
    E_IWADS_UDSCR_IDA=100432
    E_IWADS_UDSCR_IDN=100433

    E_IWADS_NDSR_IPSP=100440
    E_IWADS_NDSR_IA=100441
    E_IWADS_NDSR_IDN=100442
    E_IWADS_NDSR_AUTHERR=100443 #new_datasource_request error in update_resources

    E_IWADS_DDSR_IPSP=100450
    E_IWADS_DDSR_ID=100451


#interface web api datapoint

    E_IWADP_GDPDR_IPSP=100700
    E_IWADP_GDPDR_IP=100701
    E_IWADP_GDPDR_ISD=100702
    E_IWADP_GDPDR_IED=100703
    E_IWADP_GDPDR_IIS=100704
    E_IWADP_GDPDR_IES=100705
    E_IWADP_GDPDR_OOS=100706
    E_IWADP_GDPDR_IT=100707

    E_IWADP_GDPCR_IPSP=100715
    E_IWADP_GDPCR_IP=100716

    E_IWADP_UDPCR_IPSP=100725
    E_IWADP_UDPCR_IP=100726
    E_IWADP_UDPCR_ID=100727
    E_IWADP_UDPCR_EMP=100728
    E_IWADP_UDPCR_IDN=100729
    E_IWADP_UDPCR_IC=100730

    E_IWADP_NDPR_IPSP=100740
    E_IWADP_NDPR_ID=100741
    E_IWADP_NDPR_IS=100742
    E_IWADP_NDPR_IPO=100743
    E_IWADP_NDPR_IL=100744
    E_IWADP_NDPR_IDN=100745

    E_IWADP_MPVR_IPSP=100755
    E_IWADP_MPVR_IS=100756
    E_IWADP_MPVR_IPO=100757
    E_IWADP_MPVR_IL=100758
    E_IWADP_MPVR_IP=100759

    E_IWADP_MNVR_IPSP=100765
    E_IWADP_MNVR_IS=100766
    E_IWADP_MNVR_IPO=100767
    E_IWADP_MNVR_IL=100768
    E_IWADP_MNVR_IP=100769

    E_IWADP_DDPR_IPSP=100775
    E_IWADP_DDPR_IP=100776

    E_IWADP_DDPFDS_IPSP      = 100800  #: dissociate_datapoint_from_datasource_request invalid psp 
    E_IWADP_DDPFDS_IP        = 100801  #: dissociate_datapoint_from_datasource_request invalid pid

#interface web api widget

    E_IWAW_GWSCR_IPSP=101000

    E_IWAW_GWCR_IPSP=101005
    E_IWAW_GWCR_IW=101006

    E_IWAW_DWR_IPSP=101010
    E_IWAW_DWR_IW=101011

    E_IWAW_NWR_IPSP     = 101020
    E_IWAW_NWR_ID       = 101021
    E_IWAW_NWR_IT       = 101022
    E_IWAW_NWR_IWN      = 101023
    E_IWAW_NWR_AUTHERR  = 101024 #: new_widget_request error in update_resources
    E_IWAW_NWR_WCE      = 101025 #: new_widget_request widget creation error

    E_IWAW_ADPR_IPSP    = 101030
    E_IWAW_ADPR_IW      = 101031
    E_IWAW_ADPR_IP      = 101032
    E_IWAW_ADPR_OE      = 101033 #: add_datapoint_request. Operation error.

    E_IWAW_DDPR_IPSP    = 101040
    E_IWAW_DDPR_IW      = 101041
    E_IWAW_DDPR_IP      = 101042
    E_IWAW_DDPR_OE      = 101043 #: delete_datapoint_request. Operation error.

    E_IWAW_UWCR_IPSP    = 101050
    E_IWAW_UWCR_IW      = 101051
    E_IWAW_UWCR_ID      = 101052
    E_IWAW_UWCR_EMP     = 101053
    E_IWAW_UWCR_IWN     = 101054
    E_IWAW_UWCR_IDP     = 101055
    E_IWAW_UWCR_EMDP    = 101056
    E_IWAW_UWCR_IDPE    = 101057
    E_IWAW_UWCR_EPNF    = 101058
    E_IWAW_UWCR_ECNF    = 101059
    E_IWAW_UWCR_IEP     = 101060
    E_IWAW_UWCR_IEC     = 101061
    E_IWAW_UWCR_IVW     = 101062 #: update_widget_config_request invalid view parameter
    E_IWAW_UWCR_OE      = 101063 #: update_widget_config_request. Operation error.

    E_IWAW_GRWR_IPSP=101080
    E_IWAW_GRWR_IW=101081

#interface web api dashboard

    E_IWADB_GDBSCR_IPSP=101300

    E_IWADB_GDBCR_IPSP=101310
    E_IWADB_GDBCR_IB=101311

    E_IWADB_NDBR_IPSP=101320
    E_IWADB_NDBR_IDN=101321
    E_IWADB_NDBR_ID=101322
    E_IWADB_NDBR_AUTHERR=101323 #new_dashboard_request error in update_resources

    E_IWADB_DDBR_IPSP=101330
    E_IWADB_DDBR_IB=101331

    E_IWADB_UDBCR_IPSP=101340
    E_IWADB_UDBCR_IB=101341
    E_IWADB_UDBCR_ID=101342
    E_IWADB_UDBCR_IDN=101343

    E_IWADB_AWR_IPSP=101350
    E_IWADB_AWR_IB=101351
    E_IWADB_AWR_IW=101352

    E_IWADB_DWR_IPSP=101360
    E_IWADB_DWR_IB=101361
    E_IWADB_DWR_IW=101362


#interface web api snapshot

    E_IWASN_GSNSCR_IPSP=101500

    E_IWASN_GSNCR_IPSP=101505
    E_IWASN_GSNCR_IN=101506
    E_IWASN_GSNCR_IT=101507

    E_IWASN_DSNR_IPSP=101510
    E_IWASN_DSNR_IN=101511

    E_IWASN_NSNR_IPSP=101520
    E_IWASN_NSNR_IW=101521
    E_IWASN_NSNR_IUL=101522
    E_IWASN_NSNR_ICL=101523
    E_IWASN_NSNR_IULE=101524
    E_IWASN_NSNR_ICLE=101525
    E_IWASN_NSNR_NSNTS=101526
    E_IWASN_NSNR_ESL=101527
    E_IWADB_NSNR_AUTHERR=101528 #new_snapshot_request error in update_resources
    E_IWADB_NSNR_TCKCE=101529 #new_snapshot_request error provisioning ticket
    E_IWADB_NSNR_SCE=101530 #new_snapshot_request error creating snapshot in gestaccount

    E_IWASN_GSNDR_IPSP=101540
    E_IWASN_GSNDR_IN=101541

#interface web api circle

    E_IWACI_GUCSCR_IPSP=101800

    E_IWACI_GUCCR_IPSP=101805
    E_IWACI_GUCCR_IC=101806

    E_IWACI_DCR_IPSP=101815
    E_IWACI_DCR_IC=101816

    E_IWACI_NUCR_IPSP=101820
    E_IWACI_NUCR_ICN=101821
    E_IWACI_NUCR_IML=101822
    E_IWACI_NUCR_AUTHERR=101823 #new_users_circle_request error in update_resources
    E_IWACI_NUCR_CCE=101824 #new_users_circle_request error creating circle in gestaccount 

    E_IWACI_UCR_IPSP=101830
    E_IWACI_UCR_IC=101831
    E_IWACI_UCR_ID=101832
    E_IWACI_UCR_ICN=101833

    E_IWACI_AUTCR_IPSP=101840
    E_IWACI_AUTCR_IC=101841
    E_IWACI_AUTCR_IM=101842

    E_IWACI_DUFCR_IPSP=101850
    E_IWACI_DUFCR_IC=101851
    E_IWACI_DUFCR_IM=101852


# interface web api uri

    E_IWAUR_GUR_IPSP=103000  #get_uri_request invalid user
    E_IWAUR_GUR_IUR=103001  #get_uri_request invalid uri
    E_IWAUR_GUR_IID=103002  #get_uri_request invalid id


# interface web api events

    E_IWAEV_GEVR_IPSP=104000
    E_IWAEV_GEVR_IETS=104001
    E_IWAEV_GEVR_IITS=104002

    E_IWAEV_DEVR_IPSP=104100 #disable_event_request invalid username
    E_IWAEV_DEVR_ISEQ=104101 #disable_event_request invalid sequence

    E_IWAEV_EVRPR_IPSP=104200 #event_response_request invalid username
    E_IWAEV_EVRPR_ISEQ=104201 #event_response_request invalid sequence
    E_IWAEV_EVRPR_IDAT=104202 #event_response_request invalid data
    E_IWAEV_EVRPR_IMSF=104203 #event_response_request invalid missing parameter
    E_IWAEV_EVRPR_IIDF=104204 #event_response_request invalid identified parameter
    E_IWAEV_EVRPR_IMSIT=104205 #event_response_request invalid missing item
    E_IWAEV_EVRPR_IIDIT=104206 #event_response_request invalid identified item
    E_IWAEV_EVRPR_IEVT=104207 #event_response_request non supported event type


# interface web api login

    E_IWAL_LR_IPRM = 105000 #: login_request: invalid parameters


    E_IWAL_ULR_IU      = 105100 #: user_login_request: invalid username
    E_IWAL_ULR_IPWD    = 105101 #: user_login_request: invalid password
    E_IWAL_ULR_AUTHERR = 105102 #: user_login_request: invalid password

    E_IWAL_ALGCR_IU    = 105200 #: agent_login_generate_challenge_request: invalid username
    E_IWAL_ALGCR_IPK   = 105201 #: agent_login_generate_challenge_request: invalid pubkey

    E_IWAL_ALVCR_IU    = 105300 #: agent_login_validate_challenge_request: invalid username
    E_IWAL_ALVCR_IPK   = 105301 #: agent_login_validate_challenge_request: invalid pubkey
    E_IWAL_ALVCR_ICH   = 105302 #: agent_login_validate_challenge_request: invalid challenge
    E_IWAL_ALVCR_ISG   = 105303 #: agent_login_validate_challenge_request: invalid signature

