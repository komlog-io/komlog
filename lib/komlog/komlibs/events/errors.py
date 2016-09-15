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

    E_EAU_IEIDPI_IUID       = 151900 #: invalid uid
    E_EAU_IEIDPI_IP         = 151901 #: invalid parameters
    E_EAU_IEIDPI_IPPID      = 151902 #: invalid pid
    E_EAU_IEIDPI_IPDID      = 151903 #: invalid did
    E_EAU_IEIDPI_IPDATES    = 151904 #: invalid dates
    E_EAU_IEIDPI_IIDATE     = 151905 #: invalid item date
    E_EAU_IEIDPI_UNF        = 151906 #: user not found
    E_EAU_IEIDPI_DPNF       = 151907 #: datapoint not found
    E_EAU_IEIDPI_DPHNDID    = 151908 #: datapoint has no associated did
    E_EAU_IEIDPI_IDID       = 151909 #: datapoint did is not equal as parameters did
    E_EAU_IEIDPI_NODATES    = 151910 #: no dates received
    E_EAU_IEIDPI_DSNF       = 151911 #: datasource not found

    E_EAU_IENNSS_IU         = 152000
    E_EAU_IENNSS_IP         = 152001
    E_EAU_IENNSS_IPNID      = 152002
    E_EAU_IENNSS_IPTID      = 152003
    E_EAU_IENNSS_UNF        = 152004
    E_EAU_IENNSS_NNF        = 152005
    E_EAU_IENNSS_TNF        = 152006
    E_EAU_IENNSS_DBIIE      = 152007
    E_EAU_IENNSS_DBPIE      = 152008

# events api user_responses

    E_EAUR_PEVRP_IUID       = 160000 #: invalid uid
    E_EAUR_PEVRP_IDT        = 160001 #: invalid date
    E_EAUR_PEVRP_EVNF       = 160002 #: event not found
    E_EAUR_PEVRP_IEVT       = 160003 #: invalid event type

    E_EAUR_PEVRPUEIDI_IEVT  = 160100 #: invalid event type
    E_EAUR_PEVRPUEIDI_IRD   = 160101 #: data is not dict
    E_EAUR_PEVRPUEIDI_IDFNF = 160102 #: identified not found
    E_EAUR_PEVRPUEIDI_IDFTI = 160103 #: identified type invalid
    E_EAUR_PEVRPUEIDI_IIDI  = 160104 #: invalid identified item type
    E_EAUR_PEVRPUEIDI_ISEQI = 160105 #: invalid sequence item parameter
    E_EAUR_PEVRPUEIDI_IPI   = 160106 #: invalid position item parameter
    E_EAUR_PEVRPUEIDI_ILI   = 160107 #: invalid length item parameter

# events api summary

    E_EAS_GUEDS_IUID        = 170000 #: invalid uid
    E_EAS_GUEDS_IDATE       = 170001 #: invalid date

    E_EAS_GDSUENNSS_NPNF   = 170100 #: nid parameter not found.
    E_EAS_GDSUENNSS_INID   = 170101 #: invalid nid parameter.
    E_EAS_GDSUENNSS_NIDNF  = 170102 #: snapshot not found.

    E_EAS_GDSUEIDPI_IDID   = 170200 #: invalid did parameter
    E_EAS_GDSUEIDPI_IDATES = 170201 #: invalid dates parameter
    E_EAS_GDSUEIDPI_DSVNF  = 170202 #: datasource variables not found
    E_EAS_GDSUEIDPI_DSDNF  = 170203 #: datasource data not found

