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

The range reserved for errors in this module is 1 - 49999

'''

#gestaccount user api

E_GUA_GHP_IU=10
E_GUA_GHP_IP=11

E_GUA_AUU_IU=20
E_GUA_AUU_IP=21
E_GUA_AUU_UNF=22
E_GUA_AUU_HPNF=23

E_GUA_CRU_IU=30
E_GUA_CRU_IP=31
E_GUA_CRU_IE=32
E_GUA_CRU_UAEU=33
E_GUA_CRU_UAEE=34
E_GUA_CRU_HPNF=35

E_GUA_COU_IE=40
E_GUA_COU_IC=41
E_GUA_COU_CNF=42
E_GUA_COU_CMM=43
E_GUA_COU_CAU=44
E_GUA_COU_UNF=45
E_GUA_COU_IUE=46

E_GUA_UUC_IU=50
E_GUA_UUC_UNF=51
E_GUA_UUC_EMP=52
E_GUA_UUC_ONP=53
E_GUA_UUC_IP=54
E_GUA_UUC_PNM=55
E_GUA_UUC_EQP=56
E_GUA_UUC_HPNF=57
E_GUA_UUC_IE=58
E_GUA_UUC_EAE=59

E_GUA_GUC_IU=70
E_GUA_GUC_UNF=71

E_GUA_DU_IU=80
E_GUA_DU_UNF=81

#gestaccount agent api

E_GAA_AUA_IA=200
E_GAA_AUA_IPK=201
E_GAA_AUA_ANF=202

E_GAA_CRA_IU=210
E_GAA_CRA_IA=211
E_GAA_CRA_IPK=212
E_GAA_CRA_IV=213
E_GAA_CRA_AAE=214
E_GAA_CRA_EIA=215
E_GAA_CRA_UNF=216

E_GAA_ACA_IA=220
E_GAA_ACA_EIA=221
E_GAA_ACA_ANF=222

E_GAA_GAC_IA=230
E_GAA_GAC_IF=231
E_GAA_GAC_ANF=232

E_GAA_GASC_IU=240
E_GAA_GASC_IF=241
E_GAA_GASC_UNF=242

E_GAA_UAC_IU=250
E_GAA_UAC_IA=251
E_GAA_UAC_IAN=252
E_GAA_UAC_ANF=253
E_GAA_UAC_IAE=254

E_GAA_DA_IA=260
E_GAA_DA_ANF=261

# gestaccount datasource api

E_GDA_CRD_IU=400
E_GDA_CRD_IA=401
E_GDA_CRD_IDN=402
E_GDA_CRD_UNF=403
E_GDA_CRD_ANF=404
E_GDA_CRD_IDE=405

E_GDA_GLPD_ID=410
E_GDA_GLPD_DDNF=411
E_GDA_GLPD_DNF=412

E_GDA_UDD_ID=420
E_GDA_UDD_IDC=421
E_GDA_UDD_IDD=422
E_GDA_UDD_IFD=423
E_GDA_UDD_ESD=424
E_GDA_UDD_DNF=425

E_GDA_GDD_ID=430
E_GDA_GDD_IDT=431
E_GDA_GDD_DDNF=432

E_GDA_GDC_ID=440
E_GDA_GDC_DNF=441

E_GDA_GDSC_IU=450
E_GDA_GDSC_UNF=451

E_GDA_UDS_ID=460
E_GDA_UDS_IDN=461
E_GDA_UDS_IDE=462
E_GDA_UDS_DNF=463

E_GDA_GDM_ID=470
E_GDA_GDM_IDT=471
E_GDA_GDM_DDNF=472

E_GDA_DD_ID=480
E_GDA_DD_DNF=481

# gestaccount datapoint api

E_GPA_GDD_IP=600
E_GPA_GDD_ITD=601
E_GPA_GDD_IFD=602
E_GPA_GDD_DDNF=603

E_GPA_CRD_ID=610
E_GPA_CRD_IDN=611
E_GPA_CRD_IC=612
E_GPA_CRD_DNF=613
E_GPA_CRD_IDE=614

E_GPA_GDC_IP=620
E_GPA_GDC_DNF=621

E_GPA_UDC_IP=630
E_GPA_UDC_IDN=631
E_GPA_UDC_IC=632
E_GPA_UDC_EMP=633
E_GPA_UDC_IDE=634
E_GPA_UDC_DNF=635

E_GPA_MNV_IP=640
E_GPA_MNV_IDT=641
E_GPA_MNV_IPO=642
E_GPA_MNV_IL=643
E_GPA_MNV_DNF=644
E_GPA_MNV_DMNF=645
E_GPA_MNV_VLNF=646
E_GPA_MNV_VPNF=647

E_GPA_MPV_IP=660
E_GPA_MPV_IDT=661
E_GPA_MPV_IPO=662
E_GPA_MPV_IL=663
E_GPA_MPV_DNF=664
E_GPA_MPV_DMNF=665
E_GPA_MPV_VLNF=666
E_GPA_MPV_VPNF=667
E_GPA_MPV_VAE=668

E_GPA_GDT_IP=680
E_GPA_GDT_DNF=681
E_GPA_GDT_ETS=682

E_GPA_MND_ID=690
E_GPA_MND_IDT=691
E_GPA_MND_IPO=692
E_GPA_MND_IL=693
E_GPA_MND_IDN=694

E_GPA_SDPV_IP=700
E_GPA_SDPV_IDT=701
E_GPA_SDPV_DNF=702
E_GPA_SDPV_DTNF=703
E_GPA_SDPV_DMNF=704
E_GPA_SDPV_IDDE=705

E_GPA_SDSV_ID=710
E_GPA_SDSV_IDT=711
E_GPA_SDSV_DMNF=712

E_GPA_DDP_IP=720
E_GPA_DDP_DNF=721

# gestaccount widget api

E_GWA_GWC_IW=900
E_GWA_GWC_WNF=901

E_GWA_GWSC_IU=910
E_GWA_GWSC_UNF=911

E_GWA_DW_IW=920
E_GWA_DW_WNF=921

E_GWA_NWDS_IU=930
E_GWA_NWDS_ID=931
E_GWA_NWDS_UNF=932
E_GWA_NWDS_DNF=933
E_GWA_NWDS_WAE=934
E_GWA_NWDS_IWE=935

E_GWA_NWDP_IU=940
E_GWA_NWDP_ID=941
E_GWA_NWDP_UNF=942
E_GWA_NWDP_DNF=943
E_GWA_NWDP_WAE=944
E_GWA_NWDP_IWE=945

E_GWA_NWH_IU=950
E_GWA_NWH_IWN=951
E_GWA_NWH_UNF=952
E_GWA_NWH_IWE=953

E_GWA_NWL_IU=960
E_GWA_NWL_IWN=961
E_GWA_NWL_UNF=962
E_GWA_NWL_IWE=963

E_GWA_NWT_IU=970
E_GWA_NWT_IWN=971
E_GWA_NWT_UNF=972
E_GWA_NWT_IWE=973

E_GWA_ADTW_IW=980
E_GWA_ADTW_IP=981
E_GWA_ADTW_WNF=982
E_GWA_ADTW_DNF=983
E_GWA_ADTW_IDHE=984
E_GWA_ADTW_IDLE=985
E_GWA_ADTW_IDTE=986
E_GWA_ADTW_WUO=987

E_GWA_DDFW_IW=1000
E_GWA_DDFW_IP=1001
E_GWA_DDFW_WNF=1002
E_GWA_DDFW_DNF=1003
E_GWA_DDFW_IDHE=1004
E_GWA_DDFW_IDLE=1005
E_GWA_DDFW_IDTE=1006
E_GWA_DDFW_WUO=1007

E_GWA_UWC_IW=1020
E_GWA_UWC_IWN=1021
E_GWA_UWC_IC=1022
E_GWA_UWC_WNF=1023
E_GWA_UWC_WUO=1024

E_GWA_UWDS_IW=1030
E_GWA_UWDS_IWN=1031
E_GWA_UWDS_WNF=1032

E_GWA_UWDP_IW=1040
E_GWA_UWDP_IWN=1041
E_GWA_UWDP_WNF=1042

E_GWA_UWH_IW=1050
E_GWA_UWH_IWN=1051
E_GWA_UWH_ICD=1052
E_GWA_UWH_WNF=1053
E_GWA_UWH_DNF=1054
E_GWA_UWH_IC=1055

E_GWA_UWL_IW=1060
E_GWA_UWL_IWN=1061
E_GWA_UWL_ICD=1062
E_GWA_UWL_WNF=1063
E_GWA_UWL_DNF=1064
E_GWA_UWL_IC=1065

E_GWA_UWT_IW=1070
E_GWA_UWT_IWN=1071
E_GWA_UWT_ICD=1072
E_GWA_UWT_WNF=1073
E_GWA_UWT_DNF=1074
E_GWA_UWT_IC=1075

# gestaccount dashboard api

E_GBA_GDSC_IU=1300
E_GBA_GDSC_UNF=1301

E_GBA_GDC_IB=1310
E_GBA_GDC_DNF=1311

E_GBA_DD_IB=1320
E_GBA_DD_DNF=1321

E_GBA_CRD_IU=1330
E_GBA_CRD_IDN=1331
E_GBA_CRD_UNF=1332
E_GBA_CRD_IDE=1333

E_GBA_UDC_IB=1340
E_GBA_UDC_IDN=1341
E_GBA_UDC_DNF=1342
E_GBA_UDC_IDE=1343

E_GBA_AWTD_IB=1350
E_GBA_AWTD_IW=1351
E_GBA_AWTD_DNF=1352
E_GBA_AWTD_WNF=1353

E_GBA_DWFD_IB=1360
E_GBA_DWFD_IW=1361
E_GBA_DWFD_DNF=1362

# gestaccount snapshot api

E_GSA_GSC_IN=1500
E_GSA_GSC_SNF=1501

E_GSA_GSSC_IU=1510
E_GSA_GSSC_UNF=1511

E_GSA_GSD_IN=1520

E_GSA_DS_IN=1530
E_GSA_DS_SNF=1531

E_GSA_NS_IU=1540
E_GSA_NS_IW=1541
E_GSA_NS_III=1542
E_GSA_NS_IIE=1543
E_GSA_NS_IIO=1544
E_GSA_NS_ISWU=1545
E_GSA_NS_ISWC=1546
E_GSA_NS_UNF=1547
E_GSA_NS_WNF=1548
E_GSA_NS_SCE=1549

E_GSA_NSDS_WNF=1560
E_GSA_NSDS_SCE=1561

E_GSA_NSDP_WNF=1570
E_GSA_NSDP_SCE=1571

E_GSA_NSH_WNF=1580
E_GSA_NSH_ZDP=1581
E_GSA_NSH_SCE=1582

E_GSA_NSL_WNF=1590
E_GSA_NSL_ZDP=1591
E_GSA_NSL_SCE=1592

E_GSA_NST_WNF=1600
E_GSA_NST_ZDP=1601
E_GSA_NST_SCE=1602

# gestaccount circle api

E_GCA_GUCC_IC=1800
E_GCA_GUCC_CNF=1801

E_GCA_GUCSC_IU=1810
E_GCA_GUCSC_UNF=1811

E_GCA_DC_IC=1820
E_GCA_DC_CNF=1821

E_GCA_NUC_IU=1830
E_GCA_NUC_ICN=1831
E_GCA_NUC_IML=1832
E_GCA_NUC_UNF=1833
E_GCA_NUC_ICE=1834

E_GCA_UC_IC=1840
E_GCA_UC_ICN=1841
E_GCA_UC_CNF=1842
E_GCA_UC_ICE=1843

E_GCA_AUTC_IC=1850
E_GCA_AUTC_IU=1851
E_GCA_AUTC_CNF=1852
E_GCA_AUTC_UNF=1853
E_GCA_AUTC_AME=1854

E_GCA_DUFC_IC=1860
E_GCA_DUFC_IU=1861
E_GCA_DUFC_CNF=1862
E_GCA_DUFC_UNF=1863
E_GCA_DUFC_AME=1864

