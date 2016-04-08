from komlog.komfig import logging
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.events import exceptions as eventexcept
from komlog.komlibs.interface.web import status
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import webmodel

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
    gestexcept.ChallengeGenerationException,
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

NOT_ALLOWED_STATUS_EXCEPTION_LIST=(
    gestexcept.WidgetUnsupportedOperationException,
)

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        try:
            response=self.f(*args, **kwargs)
            return response if response else webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, error=Errors.UNKNOWN.value)
        except BAD_PARAMETERS_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error.value}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_BAD_PARAMETERS, data=data, error=e.error.value)
        except ACCESS_DENIED_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error.value}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED, data=data, error=e.error.value)
        except NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error.value}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND, data=data, error=e.error.value)
        except NOT_ALLOWED_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error.value}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_ALLOWED, data=data, error=e.error.value)
        except INTERNAL_ERROR_STATUS_EXCEPTION_LIST as e:
            data={'error':e.error.value}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, data=data, error=e.error.value)
        except Exception as e:
            logging.logger.debug('WEB Response non treated Exception: '+str(type(e))+str(e))
            error=getattr(e,'error',Errors.UNKNOWN.value)
            data={'error':error}
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, data=data, error=error)

