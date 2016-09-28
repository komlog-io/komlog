import time
import traceback
from komlog.komfig import logging
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.events import exceptions as eventexcept
from komlog.komlibs.interface.web import status
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.interface.web.model import response

class BadParametersException(Exception):
    def __init__(self, error):
        self.error=error

    def __str__(self):
        return str(self.__class__)

BAD_PARAMETERS_STATUS_EXCEPTION_LIST=(
    BadParametersException,
)

NOT_ALLOWED_STATUS_EXCEPTION_LIST=(
    gestexcept.UserUnsupportedOperationException,
    gestexcept.WidgetUnsupportedOperationException,
    authexcept.IntervalBoundsException,
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
    gestexcept.BadParametersException,
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
    eventexcept.BadParametersException,
    eventexcept.UserEventCreationException,
)

SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST = (
    cassexcept.CassandraException,
)

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        init=time.time()
        try:
            logging.logger.debug('START processing: '+self.f.__module__+'.'+self.f.__name__)
            resp=self.f(*args, **kwargs)
            logging.logger.debug('END processing: '+self.f.__module__+'.'+self.f.__name__)
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__name__,Errors.OK.name,str(init),str(end))))
            resp.error=resp.error.value
            return resp
        except BAD_PARAMETERS_STATUS_EXCEPTION_LIST as e:
            error=e.error
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_BAD_PARAMETERS, data=data, error=error.value)
        except NOT_ALLOWED_STATUS_EXCEPTION_LIST as e:
            error=e.error
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_NOT_ALLOWED, data=data, error=error.value)
        except ACCESS_DENIED_STATUS_EXCEPTION_LIST as e:
            error=e.error
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED, data=data, error=error.value)
        except NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            error=e.error
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND, data=data, error=error.value)
        except INTERNAL_ERROR_STATUS_EXCEPTION_LIST as e:
            error=e.error
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, data=data, error=error.value)
        except SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST as e:
            error=e.error
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_SERVICE_UNAVAILABLE, data=data, error=error.value)
        except Exception as e:
            logging.logger.error('WEB Response non treated Exception in: '+'.'.join((self.f.__module__,self.f.__qualname__)))
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            error=getattr(e,'error',Errors.UNKNOWN)
            data={'error':error.value}
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return response.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR, data=data, error=error.value)

