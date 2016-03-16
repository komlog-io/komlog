from komfig import logger
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.auth import exceptions as authexcept
from komlibs.events import exceptions as eventexcept
from komlibs.interface.websocket.protocol.v1 import status
from komlibs.interface.websocket.protocol.v1.model import response as modresp

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
    OperationValidationException,
    ResponseValidationException,
)

RESOURCE_NOT_FOUND_STATUS_EXCEPTION_LIST=(
    gestexcept.UserNotFoundException,
    gestexcept.AgentNotFoundException,
    gestexcept.DatasourceNotFoundException,
)

class ExceptionHandler:
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        try:
            resp=self.f(*args, **kwargs)
            return resp if resp else modresp.Response(status=status.MESSAGE_EXECUTION_ERROR)
        except PROTOCOL_ERROR_STATUS_EXCEPTION_LIST as e:
            return modresp.Response(status=status.PROTOCOL_ERROR, reason='protocol error', error=e.error)
        except MESSAGE_EXECUTION_DENIED_STATUS_EXCEPTION_LIST as e:
            return modresp.Response(status=status.MESSAGE_EXECUTION_DENIED,reason='msg exec denied',  error=e.error)
        except RESOURCE_NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            return modresp.Response(status=status.RESOURCE_NOT_FOUND, reason='resource not found', error=e.error)
        except MESSAGE_EXECUTION_ERROR_STATUS_EXCEPTION_LIST as e:
            return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, reason='msg exec error', error=e.error)
        except Exception as e:
            logger.logger.debug('WEBSOCKET Response non treated Exception: '+str(e))
            error=getattr(e,'error',-1)
            return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, error=error)

