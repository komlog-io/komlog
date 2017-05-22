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

The range reserved for Errors.in this module is 350000 - 400000 

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

# interface websocket api

    E_IWSA_PM_IVA   = 350000      #: process_message invalid version or action received
    E_IWSA_PM_UPV   = 350001      #: process_message unsupported protocol version
    E_IWSA_PM_IPSP  = 350002      #: process_message invalid passport

# interface websocket model response

    E_IWSMR_PR_IS   = 351000      #: ProcessingResult. status type error

    E_IWSMR_GR_IV   = 351100      #: GenericResponse. invalid version
    E_IWSMR_GR_ISEQ = 351101      #: GenericResponse. invalid sequence
    E_IWSMR_GR_IS   = 351102      #: GenericResponse. invalid status
    E_IWSMR_GR_IIRT = 351103      #: GenericResponse. invalid in reply to

# komwebsock auth

    E_KWSKA_AA_AE   = 352000      #: agent_authenticated attribute error. Cookie must be None

