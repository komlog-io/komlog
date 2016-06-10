import time
import traceback
from komlog.komfig import logging
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.events import exceptions as eventexcept
from komlog.komlibs.interface.websocket.protocol.v1 import status
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.model import response as modresp

class WebSocketProtocolException(Exception):
    def __init__(self, error):
        self.error=error

    def __str__(self):
        return str(self.__class__)

class BadParametersException(WebSocketProtocolException):
    def __init__(self, error):
        super(BadParametersException,self).__init__(error=error)

class ResponseValidationException(WebSocketProtocolException):
    def __init__(self, error):
        super(ResponseValidationException,self).__init__(error=error)

class MessageValidationException(WebSocketProtocolException):
    def __init__(self, error):
        super(MessageValidationException,self).__init__(error=error)

class OperationValidationException(WebSocketProtocolException):
    def __init__(self, error):
        super(OperationValidationException,self).__init__(error=error)

PROTOCOL_ERROR_STATUS_EXCEPTION_LIST=(
    BadParametersException,
    MessageValidationException,
    gestexcept.BadParametersException,
)

MESSAGE_EXECUTION_DENIED_STATUS_EXCEPTION_LIST=(
    authexcept.AuthException,
)

MESSAGE_EXECUTION_ERROR_STATUS_EXCEPTION_LIST=(
    gestexcept.DatasourceUploadContentException,
    gestexcept.DatapointCreationException,
    gestexcept.DatapointStoreValueException,
    OperationValidationException,
    ResponseValidationException,
)

RESOURCE_NOT_FOUND_STATUS_EXCEPTION_LIST=(
    gestexcept.UserNotFoundException,
    gestexcept.AgentNotFoundException,
    gestexcept.DatasourceNotFoundException,
)

SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST = (
    cassexcept.CassandraException,
)

class ExceptionHandler:
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        init=time.time()
        try:
            resp=self.f(*args, **kwargs)
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__name__,resp.error.name,str(init),str(end))))
            resp.error=resp.error.value
            return resp
        except PROTOCOL_ERROR_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,e.error.name,str(init),str(end))))
            return modresp.Response(status=status.PROTOCOL_ERROR, reason='protocol error', error=e.error.value)
        except MESSAGE_EXECUTION_DENIED_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,e.error.name,str(init),str(end))))
            return modresp.Response(status=status.MESSAGE_EXECUTION_DENIED,reason='msg exec denied',  error=e.error.value)
        except RESOURCE_NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,e.error.name,str(init),str(end))))
            return modresp.Response(status=status.RESOURCE_NOT_FOUND, reason='resource not found', error=e.error.value)
        except MESSAGE_EXECUTION_ERROR_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,e.error.name,str(init),str(end))))
            return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, reason='msg exec error', error=e.error.value)
        except SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,e.error.name,str(init),str(end))))
            return modresp.Response(status=status.SERVICE_UNAVAILABLE, reason='service temporarily unavailable', error=e.error.value)
        except Exception as e:
            logging.logger.error('WEBSOCKET Response non treated Exception in: '+'.'.join((self.f.__module__,self.f.__qualname__)))
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            error=getattr(e,'error',Errors.UNKNOWN)
            end=time.time()
            logging.c_logger.info(','.join((self.f.__module__+'.'+self.f.__qualname__,error.name,str(init),str(end))))
            return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, error=error.value)

