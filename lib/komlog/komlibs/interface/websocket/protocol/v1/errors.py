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
    E_IWSPV1PM_PSDSD_EUR    = 210102    #: exception updating ds resources
    E_IWSPV1PM_PSDSD_FUR    = 210103    #: fail updating ds resources
    E_IWSPV1PM_PSDSD_ESC    = 210104    #: error storing ds content

    E_IWSPV1PM_PSDPD_IURI   = 210200    #: uri is not a datapoint
    E_IWSPV1PM_PSDPD_ECDP   = 210201    #: error creating datapoint
    E_IWSPV1PM_PSDPD_FPOR   = 210202    #: error procesing operation result

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

# interface websocket protocol v1 model message

    E_IWSPV1MM_SDSDM_IMT     = 220000      #: SendDsDataMessage. message format error or 
                                           #: not v action or payload fields found
    E_IWSPV1MM_SDSDM_IA      = 220001      #: SendDsDataMessage. invalid message action
    E_IWSPV1MM_SDSDM_IV      = 220002      #: SendDsDataMessage. invalid message version
    E_IWSPV1MM_SDSDM_IPL     = 220003      #: SendDsDataMessage. invalid message payload


    E_IWSPV1MM_SDPDM_IMT     = 220100      #: SendDpDataMessage. message format error or 
                                           #: not v action or payload fields found
    E_IWSPV1MM_SDPDM_IA      = 220101      #: SendDpDataMessage. invalid message action
    E_IWSPV1MM_SDPDM_IV      = 220102      #: SendDpDataMessage. invalid message version
    E_IWSPV1MM_SDPDM_IPL     = 220103      #: SendDpDataMessage. invalid message payload

    E_IWSPV1MM_SMTDM_IMT     = 220200      #: SendMultiDataMessage. message format error or 
                                           #: not v action or payload fields found
    E_IWSPV1MM_SMTDM_IA      = 220201      #: SendMultiDataMessage. invalid message action
    E_IWSPV1MM_SMTDM_IV      = 220202      #: SendMultiDataMessage. invalid message version
    E_IWSPV1MM_SMTDM_IPL     = 220203      #: SendMultiDataMessage. invalid message payload

    E_IWSPV1MM_HTUM_IMT      = 220300      #: HookToUriMessage. message format error
    E_IWSPV1MM_HTUM_IA       = 220301      #: HookToUriMessage. invalid message action
    E_IWSPV1MM_HTUM_IV       = 220302      #: HookToUriMessage. invalid message version
    E_IWSPV1MM_HTUM_IPL      = 220303      #: HookToUriMessage. invalid message payload

    E_IWSPV1MM_UHFUM_IMT     = 220400      #: UnHookFromUriMessage. message format error
    E_IWSPV1MM_UHFUM_IA      = 220401      #: UnHookFromUriMessage. invalid message action
    E_IWSPV1MM_UHFUM_IV      = 220402      #: UnHookFromUriMessage. invalid message version
    E_IWSPV1MM_UHFUM_IPL     = 220403      #: UnHookFromUriMessage. invalid message payload

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

#interface websocket protocol v1 processing operation

    E_IWSPV1PO_ROA_IOT       = 250000      #: request_operation_actions. invalid operation type
    E_IWSPV1PO_ROA_ONF       = 250001      #: request_operation_actions. operation not found

