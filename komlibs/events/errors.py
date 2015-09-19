'''
In this file we define the different error codes that will be
added to the exceptions in the events modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for errors in this module is 150000 - 200000 

'''


#events api user

E_EAU_GEVS_IU=150000
E_EAU_GEVS_ITD=150001
E_EAU_GEVS_IFD=150002
E_EAU_GEVS_ICNT=150003

E_EAU_GEV_IU=150050
E_EAU_GEV_IDT=150051
E_EAU_GEV_EVNF=150052

E_EAU_ACE_IU=150100
E_EAU_ACE_ID=150101
E_EAU_ACE_EVNF=150102

E_EAU_DACE_IU=150200
E_EAU_DACE_ID=150201
E_EAU_DACE_EVNF=150202

E_EAU_DEV_IU=150300

E_EAU_INUE_IU=150400
E_EAU_INUE_IUS=150401

E_EAU_INAE_IU=150500
E_EAU_INAE_IA=150501
E_EAU_INAE_IAN=150502

E_EAU_INDSE_IU=150600
E_EAU_INDSE_IA=150601
E_EAU_INDSE_IDID=150602
E_EAU_INDSE_IDSN=150603

E_EAU_INDPE_IU=150700
E_EAU_INDPE_IA=150701
E_EAU_INDPE_IDID=150702
E_EAU_INDPE_IPID=150703
E_EAU_INDPE_IDSN=150704
E_EAU_INDPE_IDPN=150705

E_EAU_INWGE_IU=150800
E_EAU_INWGE_IWID=150801
E_EAU_INWGE_IWN=150802

E_EAU_INDBE_IU=150900
E_EAU_INDBE_IBID=150901
E_EAU_INDBE_IDBN=150902

E_EAU_INCE_IU=151000
E_EAU_INCE_ICID=151001
E_EAU_INCE_ICN=151002

E_EAU_NEWE_NUIU=151100
E_EAU_NEWE_NAID=151101
E_EAU_NEWE_NAIA=151102
E_EAU_NEWE_NDIA=151103
E_EAU_NEWE_NDID=151104
E_EAU_NEWE_NDIN=151105
E_EAU_NEWE_NPID=151106
E_EAU_NEWE_NPIP=151107
E_EAU_NEWE_NPIN=151108
E_EAU_NEWE_NPIM=151109
E_EAU_NEWE_NWIW=151110
E_EAU_NEWE_NWIN=151111
E_EAU_NEWE_NBIB=151112
E_EAU_NEWE_NBIN=151113
E_EAU_NEWE_NCIC=151114
E_EAU_NEWE_NCIN=151115
E_EAU_NEWE_UIDIID=151116
E_EAU_NEWE_UIDIIDT=151117
E_EAU_NEWE_UIDIIDO=151118
E_EAU_NEWE_UIDIIDI=151119
E_EAU_NEWE_UIDIIDOP=151120
E_EAU_NEWE_UIDIIDIP=151121
E_EAU_NEWE_EVTNF=151122
E_EAU_NEWE_IEVT=151123

E_EAU_INEUIDI_IUID=151200
E_EAU_INEUIDI_IDID=151201
E_EAU_INEUIDI_IDT=151202
E_EAU_INEUIDI_IDOU=151203
E_EAU_INEUIDI_IDIS=151204
E_EAU_INEUIDI_IDOUP=151205
E_EAU_INEUIDI_IDISP=151206

E_EAU_PEVRP_IUID=151300
E_EAU_PEVRP_IDT=151301
E_EAU_PEVRP_IDAT=151302
E_EAU_PEVRP_EVNF=151303


# events api user_responses

E_EAUR_PEVRP_IUID=160000 #process_event_response invalid uid
E_EAUR_PEVRP_IDT=160001 #process_event_response invalid date
E_EAUR_PEVRP_IDAT=160002 #process_event_response data is not dict
E_EAUR_PEVRP_EVNF=160003 #process_event_response event not found

E_EAUR_PEVRPUEIDI_IRD=160100 #_process_event_response_user_event_intervention_datapoint_identification data is not dict
E_EAUR_PEVRPUEIDI_IIDP=160101 #_process_event_response_user_event_intervention_datapoint_identification invalid identified data parameter
E_EAUR_PEVRPUEIDI_IMSP=160102 #_process_event_response_user_event_intervention_datapoint_identification invalid missing data parameter
E_EAUR_PEVRPUEIDI_IIDI=160103 #_process_event_response_user_event_intervention_datapoint_identification invalid identified item type
E_EAUR_PEVRPUEIDI_IDPI=160104 #_process_event_response_user_event_intervention_datapoint_identification invalid datapoint item parameter
E_EAUR_PEVRPUEIDI_IPI=160105 #_process_event_response_user_event_intervention_datapoint_identification invalid position item parameter
E_EAUR_PEVRPUEIDI_ILI=160106 #_process_event_response_user_event_intervention_datapoint_identification invalid length item parameter
E_EAUR_PEVRPUEIDI_IMSI=160107 #_process_event_response_user_event_intervention_datapoint_identification invalid missing item
