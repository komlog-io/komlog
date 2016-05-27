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

from enum import Enum

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

    E_IWSPV1PM_PSDSD_IURI    = 210100      #: uri is not a datasource
    E_IWSPV1PM_PSDSD_ECDS    = 210101      #: error creating datasource
    E_IWSPV1PM_PSDSD_EUR     = 210102      #: exception updating ds resources
    E_IWSPV1PM_PSDSD_FUR     = 210103      #: fail updating ds resources
    E_IWSPV1PM_PSDSD_ESC     = 210104      #: error storing ds content

    E_IWSPV1PM_PSDPD_IURI    = 210200      #: uri is not a datapoint
    E_IWSPV1PM_PSDPD_ECDP    = 210201      #: error creating datapoint
    E_IWSPV1PM_PSDPD_FPOR    = 210202      #: error procesing operation result

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

#interface websocket protocol v1 processing operation

    E_IWSPV1PO_ROA_IOT       = 250000      #: request_operation_actions. invalid operation type
    E_IWSPV1PO_ROA_ONF       = 250001      #: request_operation_actions. operation not found

