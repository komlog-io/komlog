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

The range reserved for Errors.in this module is 150000 - 200000 

'''

from enum import Enum

class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

#events api user

    E_EAU_GEVS_IU=150000
    E_EAU_GEVS_ITD=150001
    E_EAU_GEVS_IFD=150002
    E_EAU_GEVS_ICNT=150003

    E_EAU_GEV_IU=150050
    E_EAU_GEV_IDT=150051
    E_EAU_GEV_EVNF=150052

    E_EAU_GEVD_EVNF=150060

    E_EAU_ENE_IU=150100
    E_EAU_ENE_ID=150101
    E_EAU_ENE_EVNF=150102

    E_EAU_DISE_IU=150200
    E_EAU_DISE_ID=150201
    E_EAU_DISE_EVNF=150202

    E_EAU_DEV_IU=150300

    E_EAU_NEWE_IEVT=151100
    E_EAU_NEWE_EVTNF=151101

    E_EAU_IENNU_IU=151200
    E_EAU_IENNU_IP=151201
    E_EAU_IENNU_UNF=151202
    E_EAU_IENNU_DBIE=151203

    E_EAU_IENNA_IU=151300
    E_EAU_IENNA_IP=151301
    E_EAU_IENNA_IPAID=151302
    E_EAU_IENNA_ANF=151303
    E_EAU_IENNA_DBIE=151304
    E_EAU_IENNA_UNF=151305

    E_EAU_IENNDS_IU=151400
    E_EAU_IENNDS_IP=151401
    E_EAU_IENNDS_IPDID=151402
    E_EAU_IENNDS_DNF=151403
    E_EAU_IENNDS_DBIE=151404
    E_EAU_IENNDS_UNF=151405

    E_EAU_IENNDP_IU=151500
    E_EAU_IENNDP_IP=151501
    E_EAU_IENNDP_IPPID=151502
    E_EAU_IENNDP_UNF=151503
    E_EAU_IENNDP_PNF=151504
    E_EAU_IENNDP_DNF=151505
    E_EAU_IENNDP_DBIE=151506

    E_EAU_IENNWG_IU=151600
    E_EAU_IENNWG_IP=151601
    E_EAU_IENNWG_IPWID=151602
    E_EAU_IENNWG_WNF=151603
    E_EAU_IENNWG_DBIE=151604
    E_EAU_IENNWG_UNF=151605

    E_EAU_IENNDB_IU=151700
    E_EAU_IENNDB_IP=151701
    E_EAU_IENNDB_IPBID=151702
    E_EAU_IENNDB_BNF=151703
    E_EAU_IENNDB_DBIE=151704
    E_EAU_IENNDB_UNF=151705

    E_EAU_IENNC_IU=151800
    E_EAU_IENNC_IP=151801
    E_EAU_IENNC_IPCID=151802
    E_EAU_IENNC_CNF=151803
    E_EAU_IENNC_DBIE=151804
    E_EAU_IENNC_UNF=151805

    E_EAU_IEIDPI_IUID=151900
    E_EAU_IEIDPI_IP=151901
    E_EAU_IEIDPI_IPDID=151902
    E_EAU_IEIDPI_IPDATE=151903
    E_EAU_IEIDPI_IPDBT=151904
    E_EAU_IEIDPI_IPDISC=151905
    E_EAU_IEIDPI_IIDBT=151906
    E_EAU_IEIDPI_IIDISC=151907
    E_EAU_IEIDPI_DBIE=151908
    E_EAU_IEIDPI_UNF=151909
    E_EAU_IEIDPI_DNF=151910

    E_EAU_IENNSS_IU=152000
    E_EAU_IENNSS_IP=152001
    E_EAU_IENNSS_IPNID=152002
    E_EAU_IENNSS_IPTID=152003
    E_EAU_IENNSS_UNF=152004
    E_EAU_IENNSS_NNF=152005
    E_EAU_IENNSS_TNF=152006
    E_EAU_IENNSS_DBIIE=152007
    E_EAU_IENNSS_DBPIE=152008

# events api user_responses

    E_EAUR_PEVRP_IUID=160000 #: process_event_response invalid uid
    E_EAUR_PEVRP_IDT=160001 #: process_event_response invalid date
    E_EAUR_PEVRP_IDAT=160002 #: process_event_response data is not dict
    E_EAUR_PEVRP_EVNF=160003 #: process_event_response event not found

    E_EAUR_PEVRPUEIDI_IRD=160100 #: _process_event_response_user_event_intervention_datapoint_identification data is not dict
    E_EAUR_PEVRPUEIDI_IIDP=160101 #: _process_event_response_user_event_intervention_datapoint_identification invalid identified data parameter
    E_EAUR_PEVRPUEIDI_IMSP=160102 #: _process_event_response_user_event_intervention_datapoint_identification invalid missing data parameter
    E_EAUR_PEVRPUEIDI_IIDI=160103 #: _process_event_response_user_event_intervention_datapoint_identification invalid identified item type
    E_EAUR_PEVRPUEIDI_IDPI=160104 #: _process_event_response_user_event_intervention_datapoint_identification invalid datapoint item parameter
    E_EAUR_PEVRPUEIDI_IPI=160105 #: _process_event_response_user_event_intervention_datapoint_identification invalid position item parameter
    E_EAUR_PEVRPUEIDI_ILI=160106 #: _process_event_response_user_event_intervention_datapoint_identification invalid length item parameter
    E_EAUR_PEVRPUEIDI_IMSI=160107 #: _process_event_response_user_event_intervention_datapoint_identification invalid missing item

# events api summary

    E_EAS_GUEGSD_IUID=170000 #: get_user_event_graph_summary_data invalid uid
    E_EAS_GUEGSD_IDATE=170001 #: get_user_event_graph_summary_data invalid date

    E_EAS_GGSDUENNSS_NPNF=170100 #: _generate_graph_summary_data_UENNSS nid parameter not found.
    E_EAS_GGSDUENNSS_INID=170101 #: _generate_graph_summary_data_UENNSS invalid nid parameter.
    E_EAS_GGSDUENNSS_NIDNF=170102 #: _generate_graph_summary_data_UENNSS snapshot not found.

