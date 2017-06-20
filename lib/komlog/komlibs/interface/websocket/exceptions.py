import time
import json
import traceback
from komlog.komfig import logging
from komlog.komcass import exceptions as cassexcept
from komlog.komlibs.general.validation import arguments
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.passport import AgentPassport
from komlog.komlibs.events import exceptions as eventexcept
from komlog.komlibs.interface.websocket import status
from komlog.komlibs.interface.websocket.errors import Errors
from komlog.komlibs.interface.websocket.model import response as modresp

class WebSocketProtocolException(Exception):
    def __init__(self, error):
        self.error=error

    def __str__(self):
        return str(self.__class__)

class BadParametersException(WebSocketProtocolException):
    def __init__(self, error):
        super().__init__(error=error)

class ResponseValidationException(WebSocketProtocolException):
    def __init__(self, error):
        super().__init__(error=error)

class MessageValidationException(WebSocketProtocolException):
    def __init__(self, error):
        super().__init__(error=error)

class OperationValidationException(WebSocketProtocolException):
    def __init__(self, error):
        super().__init__(error=error)

class OperationExecutionException(WebSocketProtocolException):
    def __init__(self, error):
        super().__init__(error=error)

PROTOCOL_ERROR_STATUS_EXCEPTION_LIST=(
    BadParametersException,
    MessageValidationException,
)

MESSAGE_EXECUTION_DENIED_STATUS_EXCEPTION_LIST=(
    authexcept.AuthException,
)

MESSAGE_EXECUTION_ERROR_STATUS_EXCEPTION_LIST=(
    gestexcept.BadParametersException,
    gestexcept.DatasourceUploadContentException,
    gestexcept.DatapointCreationException,
    gestexcept.DatapointStoreValueException,
    OperationValidationException,
    OperationExecutionException,
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
        if 'passport' in kwargs and isinstance(kwargs['passport'],AgentPassport):
            uid = kwargs['passport'].uid.hex
            aid = kwargs['passport'].aid.hex
            sid = kwargs['passport'].sid.hex
        else:
            uid = None
            aid = None
            sid = None
        log = {
            'func':'.'.join((self.f.__module__,self.f.__qualname__)),
            'uid':uid,
            'aid':uid,
            'sid':sid,
            'ts':init
        }
        try:
            resp=self.f(*args, **kwargs)
            end=time.time()
            log['error']=resp.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            return resp
        except PROTOCOL_ERROR_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            irt = kwargs['message']['seq'] if 'message' in kwargs and 'seq' in kwargs['message'] and arguments.is_valid_message_sequence(kwargs['message']['seq']) else None
            v = kwargs['message']['v'] if 'message' in kwargs and 'v' in kwargs['message'] and arguments.is_valid_int(kwargs['message']['v']) else 0
            ws_res = modresp.GenericResponse(status=status.PROTOCOL_ERROR, reason='protocol error', error=e.error, irt=irt, v=v)
            result = modresp.WSocketIfaceResponse(status=status.PROTOCOL_ERROR, error=e.error)
            result.add_ws_message(ws_res)
            return result
        except MESSAGE_EXECUTION_DENIED_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            irt = kwargs['message']['seq'] if 'message' in kwargs and 'seq' in kwargs['message'] and arguments.is_valid_message_sequence(kwargs['message']['seq']) else None
            v = kwargs['message']['v'] if 'message' in kwargs and 'v' in kwargs['message'] and arguments.is_valid_int(kwargs['message']['v']) else 0
            ws_res = modresp.GenericResponse(status=status.MESSAGE_EXECUTION_DENIED,reason='msg exec denied',  error=e.error, irt=irt, v=v)
            result = modresp.WSocketIfaceResponse(status=status.MESSAGE_EXECUTION_DENIED, error=e.error)
            result.add_ws_message(ws_res)
            return result
        except RESOURCE_NOT_FOUND_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            irt = kwargs['message']['seq'] if 'message' in kwargs and 'seq' in kwargs['message'] and arguments.is_valid_message_sequence(kwargs['message']['seq']) else None
            v = kwargs['message']['v'] if 'message' in kwargs and 'v' in kwargs['message'] and arguments.is_valid_int(kwargs['message']['v']) else 0
            ws_res = modresp.GenericResponse(status=status.RESOURCE_NOT_FOUND, reason='resource not found', error=e.error, irt=irt, v=v)
            result = modresp.WSocketIfaceResponse(status=status.RESOURCE_NOT_FOUND, error=e.error)
            result.add_ws_message(ws_res)
            return result
        except MESSAGE_EXECUTION_ERROR_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            irt = kwargs['message']['seq'] if 'message' in kwargs and 'seq' in kwargs['message'] and arguments.is_valid_message_sequence(kwargs['message']['seq']) else None
            v = kwargs['message']['v'] if 'message' in kwargs and 'v' in kwargs['message'] and arguments.is_valid_int(kwargs['message']['v']) else 0
            ws_res = modresp.GenericResponse(status=status.MESSAGE_EXECUTION_ERROR, reason='msg exec error', error=e.error, irt=irt, v=v)
            result = modresp.WSocketIfaceResponse(status=status.MESSAGE_EXECUTION_ERROR, error=e.error)
            result.add_ws_message(ws_res)
            return result
        except SERVICE_UNAVAILABLE_STATUS_EXCEPTION_LIST as e:
            end=time.time()
            log['error']=e.error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            irt = kwargs['message']['seq'] if 'message' in kwargs and 'seq' in kwargs['message'] and arguments.is_valid_message_sequence(kwargs['message']['seq']) else None
            v = kwargs['message']['v'] if 'message' in kwargs and 'v' in kwargs['message'] and arguments.is_valid_int(kwargs['message']['v']) else 0
            ws_res = modresp.GenericResponse(status=status.SERVICE_UNAVAILABLE, reason='service temporarily unavailable', error=e.error, irt=irt, v=v)
            result = modresp.WSocketIfaceResponse(status=status.SERVICE_UNAVAILABLE, error=e.error)
            result.add_ws_message(ws_res)
            return result
        except Exception as e:
            logging.logger.error('WEBSOCKET Response non treated Exception in: '+'.'.join((self.f.__module__,self.f.__qualname__)))
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            error=getattr(e,'error',Errors.UNKNOWN)
            end=time.time()
            log['error']=error.name
            log['duration']=end-init
            logging.c_logger.info(json.dumps(log))
            irt = kwargs['message']['seq'] if 'message' in kwargs and 'seq' in kwargs['message'] and arguments.is_valid_message_sequence(kwargs['message']['seq']) else None
            v = kwargs['message']['v'] if 'message' in kwargs and 'v' in kwargs['message'] and arguments.is_valid_int(kwargs['message']['v']) else 0
            ws_res = modresp.GenericResponse(status=status.MESSAGE_EXECUTION_ERROR, error=error, irt=irt, v=v)
            result = modresp.WSocketIfaceResponse(status=status.MESSAGE_EXECUTION_ERROR, error=error)
            result.add_ws_message(ws_res)
            return result

