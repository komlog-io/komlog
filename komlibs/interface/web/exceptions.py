from komfig import logger
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.auth import exceptions as authexcept
from komlibs.events import exceptions as eventexcept
from komlibs.interface.web import status
from komlibs.interface.web.model import webmodel

class BadParametersException(Exception):
    def __init__(self, error):
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
    gestexcept.ChallengeValidationException,
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
    gestexcept.ChallengeGenerationException,
)

NOT_ALLOWED_STATUS_EXCEPTION_LIST=(
    gestexcept.WidgetUnsupportedOperationException,
)

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        try:
            response=self.f(*args, **kwargs)
            return response if response else webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
        except BAD_PARAMETERS_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_BAD_PARAMETERS, data=data, error=e.error)
        except ACCESS_DENIED_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED, data=data, error=e.error)
        except NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND, data=data, error=e.error)
        except NOT_ALLOWED_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_ALLOWED, data=data, error=e.error)
        except INTERNAL_ERROR_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, data=data, error=e.error)
        except Exception as e:
            logger.logger.debug('WEB Response non treated Exception: '+str(type(e))+str(e))
            error=getattr(e,'error',-1)
            data={'error':error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, data=data, error=-1)

