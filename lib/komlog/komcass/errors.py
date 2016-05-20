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

The range reserved for Errors.in this module is 300000 - 349999

'''

from enum import Enum

class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

#komcass exceptions

    E_KCE_EH_DRE    = 300000    #: DriverException
    E_KCE_EH_REE    = 300001    #: RequestExecutionException
    E_KCE_EH_UNA    = 300002    #: Unavailable
    E_KCE_EH_TOUT   = 300003    #: Timeout
    E_KCE_EH_RTOUT  = 300004    #: ReadTimeout
    E_KCE_EH_WTOUT  = 300005    #: WriteTimeout
    E_KCE_EH_CFL    = 300006    #: CoordinationFailure
    E_KCE_EH_RFL    = 300007    #: ReadFailure
    E_KCE_EH_WFL    = 300008    #: WriteFailure
    E_KCE_EH_FFL    = 300009    #: FunctionFailure
    E_KCE_EH_RVE    = 300010    #: RequestValidationException
    E_KCE_EH_CFG    = 300011    #: ConfigurationException
    E_KCE_EH_AEE    = 300012    #: AlreadyExists
    E_KCE_EH_INV    = 300013    #: InvalidRequest
    E_KCE_EH_UNAU   = 300014    #: Unauthorized
    E_KCE_EH_AUF    = 300015    #: AuthenticationFailed
    E_KCE_EH_OTOUT  = 300016    #: OperationTimedOut
    E_KCE_EH_USO    = 300017    #: UnsupportedOperation
    E_KCE_EH_NHA    = 300018    #: NoHostAvailable
    E_KCE_EH_UST    = 300019    #: UserTypeDoesNotExist
    E_KCE_EH_QEX    = 300020    #: QueryExhausted
