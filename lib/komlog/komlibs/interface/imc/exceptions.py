import time
import json
import traceback
from komlog.komfig import logging
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.events import exceptions as eventexcept
from komlog.komlibs.interface.imc import status
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.imc.model import responses
from komlog.komlibs.interface.websocket import exceptions as wsexcept

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
    wsexcept.MessageValidationException,
)

SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST = (
    cassexcept.CassandraException,
)

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        init=time.time()
        log = {
            'func':'.'.join((self.f.__module__,self.f.__qualname__)),
            'ts':init
        }
        try:
            resp=self.f(*args, **kwargs)
            end=time.time()
            log['error']=resp.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return resp
        except BAD_PARAMETERS_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_BAD_PARAMETERS,error=e.error)
        except ACCESS_DENIED_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_ACCESS_DENIED,error=e.error)
        except NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except INTERNAL_ERROR_STATUS_EXCEPTION_LIST as e:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR,error=e.error)
        except SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST as e:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_SERVICE_UNAVAILABLE,error=e.error)
        except Exception as e:
            logging.logger.error('IMC Response non treated Exception in: '+'.'.join((self.f.__module__,self.f.__qualname__)))
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            error=getattr(e,'error',Errors.UNKNOWN)
            end=time.time()
            log['error']=error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR,error=error)

