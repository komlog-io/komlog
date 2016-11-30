'''
In this file we define the different error codes that will be
added to the protocol responses, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for Errors.in this module is 200000 - 250000 

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

# interface websocket protocol v1 api

    E_IWSPV1A_PM_IA = 200000      #: unsupported action

# interface websocket protocol v1 processing message

    E_IWSPV1PM_PSDSD_IURI   = 201100    #: uri is not a datasource
    E_IWSPV1PM_PSDSD_ECDS   = 201101    #: error creating datasource

    E_IWSPV1PM_PSDPD_IURI   = 201200    #: uri is not a datapoint
    E_IWSPV1PM_PSDPD_ECDP   = 201201    #: error creating datapoint

    E_IWSPV1PM_PSMTD_IUC    = 201300    #: invalid uri content 
    E_IWSPV1PM_PSMTD_ONAOU  = 201301    #: operation not allowed on uri
    E_IWSPV1PM_PSMTD_ECDS   = 201302    #: error creating datasources
    E_IWSPV1PM_PSMTD_ECDP   = 201303    #: error creating datapoints
    E_IWSPV1PM_PSMTD_NDSOE  = 201304    #: new datasource operation error
    E_IWSPV1PM_PSMTD_NDSDSTE= 201305    #: new datasource data store error
    E_IWSPV1PM_PSMTD_NUDPOE = 201306    #: new user datapoint operation error
    E_IWSPV1PM_PSMTD_DSDSTE = 201307    #: datasource data store error
    E_IWSPV1PM_PSMTD_UCNV   = 201308    #: uri content not valid for this uri type

    E_IWSPV1PM_PHTU_UNF     = 201400    #: process_hook_to_uri: uri not found
    E_IWSPV1PM_PHTU_ONA     = 201401    #: process_hook_to_uri: operation not allowed on this uri

    E_IWSPV1PM_PUHFU_UNF    = 201500    #: process_unhook_from_uri: uri not found
    E_IWSPV1PM_PUHFU_ONA    = 201501    #: process_unhook_from_uri:operation not allowed on this uri

    E_IWSPV1PM_PRDI_UNF     = 201600    #: process_request_data_interval: uri not found
    E_IWSPV1PM_PRDI_ONA     = 201601    #: process_request_data_interval: operation not allowed on this uri
    E_IWSPV1PM_PRDI_ANA     = 201602    #: process_request_data_interval:access to range not allowed
    E_IWSPV1PM_PRDI_ALP     = 201603    #: process_request_data_interval:access to range limited partially

# interface websocket protocol v1 model message

    E_IWSPV1MM_SDSD_IURI    = 202000      #: SendDsData. invalid uri
    E_IWSPV1MM_SDSD_ITS     = 202001      #: SendDsData. invalid ts
    E_IWSPV1MM_SDSD_ICNT    = 202002      #: SendDsData. invalid content
    E_IWSPV1MM_SDSD_ELFD    = 202003      #: SendDsData. error loading from dict

    E_IWSPV1MM_SDPD_IURI    = 202100      #: SendDpData. invalid uri
    E_IWSPV1MM_SDPD_ITS     = 202101      #: SendDpData. invalid ts
    E_IWSPV1MM_SDPD_ICNT    = 202102      #: SendDpData. invalid content
    E_IWSPV1MM_SDPD_ELFD    = 202103      #: SendDpData. error loading from dict

    E_IWSPV1MM_SMTD_IURIS   = 202200      #: SendMultiData. invalid uris
    E_IWSPV1MM_SMTD_ITS     = 202201      #: SendMultiData. invalid ts
    E_IWSPV1MM_SMTD_ELFD    = 202203      #: SendMultiData. error loading from dict

    E_IWSPV1MM_HTU_IURI     = 202300      #: HookToUri. invalid uri
    E_IWSPV1MM_HTU_ELFD     = 202303      #: HookToUri. error loading from dict

    E_IWSPV1MM_UHFU_IURI    = 202400      #: UnHookFromUri. invalid uri
    E_IWSPV1MM_UHFU_ELFD    = 202403      #: UnHookFromUri. error loading from dict

    E_IWSPV1MM_RQDT_IURI    = 202500      #: RequestData. invalid uri
    E_IWSPV1MM_RQDT_ISTART  = 202501      #: RequestData. invalid start
    E_IWSPV1MM_RQDT_IEND    = 202502      #: RequestData. invalid end
    E_IWSPV1MM_RQDT_ELFD    = 202503      #: RequestData. error loading from dict
    E_IWSPV1MM_RQDT_ECOIN   = 202504      #: RequestData. count or interval needed
    E_IWSPV1MM_RQDT_ICOUNT  = 202505      #: RequestData. invalid count

    E_IWSPV1MM_SDI_IURI     = 202600      #: SendDataInterval. invalid uri
    E_IWSPV1MM_SDI_ISTART   = 202601      #: SendDataInterval. invalid start
    E_IWSPV1MM_SDI_IEND     = 202602      #: SendDataInterval. invalid end
    E_IWSPV1MM_SDI_IDATA    = 202603      #: SendDataInterval. invalid data
    E_IWSPV1MM_SDI_ELFD     = 202604      #: SendDataInterval. error loading from dict

# interface websocket protocol v1 model response

    E_IWSPV1MR_RESP_IS       = 203000      #: Response. response status type error

# interface websocket protocol v1 model operation

    E_IWSPV1MO_WSIO_IC       = 204000      #: WSIFaceOperation. invalid class.
    E_IWSPV1MO_WSIO_OIDAI    = 204001      #: WSIFaceOperation. oid already set. op mutation disallowed
    E_IWSPV1MO_WSIO_IOID     = 204002      #: WSIFaceOperation. invalid oid type.
    E_IWSPV1MO_WSIO_PMNA     = 204003      #: WSIFaceOperation. params modification not allowed


    E_IWSPV1MO_NDSO_IUT      = 204100      #: NewDatasourceOperation. invalid uid
    E_IWSPV1MO_NDSO_IAT      = 204101      #: NewDatasourceOperation. invalid aid
    E_IWSPV1MO_NDSO_IDT      = 204102      #: NewDatasourceOperation. invalid did

    E_IWSPV1MO_NUDPO_IUT     = 204200      #: NewUserDatapointOperation. invalid uid
    E_IWSPV1MO_NUDPO_IAT     = 204201      #: NewUserDatapointOperation. invalid aid
    E_IWSPV1MO_NUDPO_IPT     = 204202      #: NewUserDatapointOperation. invalid pid

    E_IWSPV1MO_DSDSTO_IDID   = 204300      #: DatasourceDataStoredOperation. invalid did
    E_IWSPV1MO_DSDSTO_IDATE  = 204301      #: DatasourceDataStoredOperation. invalid date
    E_IWSPV1MO_DSDSTO_IUID   = 204302      #: DatasourceDataStoredOperation. invalid uid

    E_IWSPV1MO_DPDSTO_IPID   = 204400      #: DatapointDataStoredOperation. invalid pid
    E_IWSPV1MO_DPDSTO_IDATE  = 204401      #: DatapointDataStoredOperation. invalid date
    E_IWSPV1MO_DPDSTO_IUID   = 204402      #: DatapointDataStoredOperation. invalid uid

#interface websocket protocol v1 processing operation

    E_IWSPV1PO_ROA_IOT       = 205000      #: request_operation_actions. invalid operation type
    E_IWSPV1PO_ROA_ONF       = 205001      #: request_operation_actions. operation not found

    E_IWSPV1PO_PONDS_EUR     = 205100      #: process_operation_new_datasource. error updating res.

    E_IWSPV1PO_PONUDP_EUR    = 205200      #: process_operation_new_user_dp. error updating res.

