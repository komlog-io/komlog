from komlog.komfig import logger
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.events import exceptions as eventexcept
from komlog.komlibs.interface.imc import status
from komlog.komlibs.interface.imc.model import responses

class BadParametersException(Exception):
    def __init__(self, error=None):
        self.error=error

    def __str__(self):
        return str(self.__class__)


BAD_PARAMETERS_STATUS_EXCEPTION_LIST=(
    BadParametersException,
    gestexcept.BadParametersException,
    eventexcept.BadParametersException,
)

ACCESS_DENIED_STATUS_EXCEPTION_LIST=(
    authexcept.AuthException,
    gestexcept.UserAlreadyExistsException,
    gestexcept.AgentAlreadyExistsException,
    gestexcept.InvalidPasswordException,
)

NOT_FOUND_STATUS_EXCEPTION_LIST=(
    gestexcept.UserNotFoundException,
    gestexcept.AgentNotFoundException,
    gestexcept.WidgetNotFoundException,
    gestexcept.DashboardNotFoundException,
    gestexcept.SnapshotNotFoundException,
    gestexcept.CircleNotFoundException,
    gestexcept.DatasourceNotFoundException,
    gestexcept.DatasourceDataNotFoundException,
    gestexcept.DatasourceMapNotFoundException,
    gestexcept.DatapointDataNotFoundException,
    gestexcept.DatapointNotFoundException,
    eventexcept.EventNotFoundException,
)

INTERNAL_ERROR_STATUS_EXCEPTION_LIST=(
    gestexcept.AgentCreationException,
    gestexcept.WidgetCreationException,
    gestexcept.UserConfirmationException,
    gestexcept.DashboardCreationException,
    gestexcept.SnapshotCreationException,
    gestexcept.CircleCreationException,
    gestexcept.DashboardUpdateException,
    gestexcept.CircleUpdateException,
    gestexcept.AddDatapointToWidgetException,
    gestexcept.DeleteDatapointFromWidgetException,
    gestexcept.DatasourceUploadContentException,
    gestexcept.CircleAddMemberException,
    gestexcept.CircleDeleteMemberException,
    eventexcept.UserEventCreationException,
)

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, **kwargs):
        try:
            response=self.f(**kwargs)
            return response
        except BAD_PARAMETERS_STATUS_EXCEPTION_LIST as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_BAD_PARAMETERS,error=e.error)
        except ACCESS_DENIED_STATUS_EXCEPTION_LIST as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_ACCESS_DENIED,error=e.error)
        except NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except INTERNAL_ERROR_STATUS_EXCEPTION_LIST as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR,error=e.error)
        except Exception as e:
            logger.logger.debug('IMC Response Exception: '+str(e))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR)

