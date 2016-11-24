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

# interface websocket api (we use v1 by default in api entry point)

    E_IWSA_PM_IVA   = 200000      #: process_message invalid version or action received
    E_IWSA_PM_UPV   = 200001      #: process_message unsupported protocol version
    E_IWSA_PM_IPSP  = 200002      #: process_message invalid passport

# interface websocket protocol v1 api

    E_IWSPV1A_PM_IA = 210000      #: unsupported action

# interface websocket protocol v1 processing message

    E_IWSPV1PM_PSDSD_IURI   = 210100    #: uri is not a datasource
    E_IWSPV1PM_PSDSD_ECDS   = 210101    #: error creating datasource

    E_IWSPV1PM_PSDPD_IURI   = 210200    #: uri is not a datapoint
    E_IWSPV1PM_PSDPD_ECDP   = 210201    #: error creating datapoint

    E_IWSPV1PM_PSMTD_IUC    = 210300    #: invalid uri content 
    E_IWSPV1PM_PSMTD_ONAOU  = 210301    #: operation not allowed on uri
    E_IWSPV1PM_PSMTD_ECDS   = 210302    #: error creating datasources
    E_IWSPV1PM_PSMTD_ECDP   = 210303    #: error creating datapoints
    E_IWSPV1PM_PSMTD_NDSOE  = 210304    #: new datasource operation error
    E_IWSPV1PM_PSMTD_NDSDSTE= 210305    #: new datasource data store error
    E_IWSPV1PM_PSMTD_NUDPOE = 210306    #: new user datapoint operation error
    E_IWSPV1PM_PSMTD_DSDSTE = 210307    #: datasource data store error
    E_IWSPV1PM_PSMTD_UCNV   = 210308    #: uri content not valid for this uri type

    E_IWSPV1PM_PHTU_UNF     = 210400    #: process_hook_to_uri: uri not found
    E_IWSPV1PM_PHTU_ONA     = 210401    #: process_hook_to_uri: operation not allowed on this uri

    E_IWSPV1PM_PUHFU_UNF    = 210500    #: process_unhook_from_uri: uri not found
    E_IWSPV1PM_PUHFU_ONA    = 210501    #: process_unhook_from_uri:operation not allowed on this uri

    E_IWSPV1PM_PRDI_UNF     = 210600    #: process_request_data_interval: uri not found
    E_IWSPV1PM_PRDI_ONA     = 210601    #: process_request_data_interval: operation not allowed on this uri
    E_IWSPV1PM_PRDI_ANA     = 210602    #: process_request_data_interval:access to range not allowed
    E_IWSPV1PM_PRDI_ALP     = 210603    #: process_request_data_interval:access to range limited partially

# interface websocket protocol v1 model message

    E_IWSPV1MM_SDSD_IURI    = 220000      #: SendDsData. invalid uri
    E_IWSPV1MM_SDSD_ITS     = 220001      #: SendDsData. invalid ts
    E_IWSPV1MM_SDSD_ICNT    = 220002      #: SendDsData. invalid content
    E_IWSPV1MM_SDSD_ELFD    = 220003      #: SendDsData. error loading from dict

    E_IWSPV1MM_SDPD_IURI    = 220100      #: SendDpData. invalid uri
    E_IWSPV1MM_SDPD_ITS     = 220101      #: SendDpData. invalid ts
    E_IWSPV1MM_SDPD_ICNT    = 220102      #: SendDpData. invalid content
    E_IWSPV1MM_SDPD_ELFD    = 220103      #: SendDpData. error loading from dict

    E_IWSPV1MM_SMTD_IURIS   = 220200      #: SendMultiData. invalid uris
    E_IWSPV1MM_SMTD_ITS     = 220201      #: SendMultiData. invalid ts
    E_IWSPV1MM_SMTD_ELFD    = 220203      #: SendMultiData. error loading from dict

    E_IWSPV1MM_HTU_IURI     = 220300      #: HookToUri. invalid uri
    E_IWSPV1MM_HTU_ELFD     = 220303      #: HookToUri. error loading from dict

    E_IWSPV1MM_UHFU_IURI    = 220400      #: UnHookFromUri. invalid uri
    E_IWSPV1MM_UHFU_ELFD    = 220403      #: UnHookFromUri. error loading from dict

    E_IWSPV1MM_RQDT_IURI    = 220500      #: RequestData. invalid uri
    E_IWSPV1MM_RQDT_ISTART  = 220501      #: RequestData. invalid start
    E_IWSPV1MM_RQDT_IEND    = 220502      #: RequestData. invalid end
    E_IWSPV1MM_RQDT_ELFD    = 220503      #: RequestData. error loading from dict
    E_IWSPV1MM_RQDT_ECOIN   = 220504      #: RequestData. count or interval needed
    E_IWSPV1MM_RQDT_ICOUNT  = 220505      #: RequestData. invalid count

    E_IWSPV1MM_SDI_IURI     = 220600      #: SendDataInterval. invalid uri
    E_IWSPV1MM_SDI_ISTART   = 220601      #: SendDataInterval. invalid start
    E_IWSPV1MM_SDI_IEND     = 220602      #: SendDataInterval. invalid end
    E_IWSPV1MM_SDI_IDATA    = 220603      #: SendDataInterval. invalid data
    E_IWSPV1MM_SDI_ELFD     = 220604      #: SendDataInterval. error loading from dict

# interface websocket protocol v1 model response

    E_IWSPV1MR_RESP_IS       = 230000      #: Response. response status type error

# interface websocket protocol v1 model operation

    E_IWSPV1MO_WSIO_IC       = 240000      #: WSIFaceOperation. invalid class.
    E_IWSPV1MO_WSIO_OIDAI    = 240001      #: WSIFaceOperation. oid already set. op mutation disallowed
    E_IWSPV1MO_WSIO_IOID     = 240002      #: WSIFaceOperation. invalid oid type.
    E_IWSPV1MO_WSIO_PMNA     = 240003      #: WSIFaceOperation. params modification not allowed


    E_IWSPV1MO_NDSO_IUT      = 240100      #: NewDatasourceOperation. invalid uid
    E_IWSPV1MO_NDSO_IAT      = 240101      #: NewDatasourceOperation. invalid aid
    E_IWSPV1MO_NDSO_IDT      = 240102      #: NewDatasourceOperation. invalid did

    E_IWSPV1MO_NUDPO_IUT     = 240200      #: NewUserDatapointOperation. invalid uid
    E_IWSPV1MO_NUDPO_IAT     = 240201      #: NewUserDatapointOperation. invalid aid
    E_IWSPV1MO_NUDPO_IPT     = 240202      #: NewUserDatapointOperation. invalid pid

    E_IWSPV1MO_DSDSTO_IDID   = 240300      #: DatasourceDataStoredOperation. invalid did
    E_IWSPV1MO_DSDSTO_IDATE  = 240301      #: DatasourceDataStoredOperation. invalid date
    E_IWSPV1MO_DSDSTO_IUID   = 240302      #: DatasourceDataStoredOperation. invalid uid

    E_IWSPV1MO_DPDSTO_IPID   = 240400      #: DatapointDataStoredOperation. invalid pid
    E_IWSPV1MO_DPDSTO_IDATE  = 240401      #: DatapointDataStoredOperation. invalid date
    E_IWSPV1MO_DPDSTO_IUID   = 240402      #: DatapointDataStoredOperation. invalid uid

#interface websocket protocol v1 processing operation

    E_IWSPV1PO_ROA_IOT       = 250000      #: request_operation_actions. invalid operation type
    E_IWSPV1PO_ROA_ONF       = 250001      #: request_operation_actions. operation not found

    E_IWSPV1PO_PONDS_EUR     = 250100      #: process_operation_new_datasource. error updating res.

    E_IWSPV1PO_PONUDP_EUR    = 250200      #: process_operation_new_user_dp. error updating res.

