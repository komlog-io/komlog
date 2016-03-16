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

The range reserved for errors in this module is 200000 - 250000 

'''

# interface websocket api (we use v1 by default in api entry point)

E_IWSA_PM_IVA   = 200000      #: process_message invalid version or action received
E_IWSA_PM_UPV   = 200001      #: process_message unsupported protocol version
E_IWSA_PM_IPSP  = 200002      #: process_message invalid passport

# interface websocket protocol v1 api

E_IWSPV1A_PM_IA = 210000      #: unsupported action

# interface websocket protocol v1 processing message

E_IWSPV1PM_PSDD_IURI     = 210100      #: uri is not a datasource
E_IWSPV1PM_PSDD_ECDS     = 210101      #: error creating datasource
E_IWSPV1PM_PSDD_EUR      = 210102      #: exception updating ds resources
E_IWSPV1PM_PSDD_FUR      = 210103      #: fail updating ds resources
E_IWSPV1PM_PSDD_ESC      = 210104      #: error storing ds content

# interface websocket protocol v1 model message

E_IWSPV1MM_SDDM_IMT      = 220000      #: PostDatasourceDataMessage. message format error or 
                                       #: not v action or payload fields found
E_IWSPV1MM_SDDM_IA       = 220001      #: SendDsDataMessage. invalid message action
E_IWSPV1MM_SDDM_IV       = 220002      #: SendDsDataMessage. invalid message version
E_IWSPV1MM_SDDM_IPL      = 220003      #: SendDsDataMessage. invalid message payload

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

#interface websocket protocol v1 processing operation

E_IWSPV1PO_ROA_IOT       = 250000      #: request_operation_actions. invalid operation type
E_IWSPV1PO_ROA_ONF       = 250001      #: request_operation_actions. operation not found

