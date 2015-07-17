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

E_EAU_ACE_IU=150100
E_EAU_ACE_ID=150101

E_EAU_DACE_IU=150200
E_EAU_DACE_ID=150201

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

