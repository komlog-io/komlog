import traceback
from cassandra import (DriverException, RequestExecutionException, Unavailable, Timeout,
    ReadTimeout, WriteTimeout, CoordinationFailure, ReadFailure, WriteFailure, FunctionFailure,
    RequestValidationException, ConfigurationException, AlreadyExists, InvalidRequest,
    Unauthorized, AuthenticationFailed, OperationTimedOut, UnsupportedOperation)
from cassandra.cluster import (NoHostAvailable, UserTypeDoesNotExist, QueryExhausted)
from komlog.komcass.errors import Errors
from komlog.komfig import logging

class KomcassException(Exception):
    def __init__(self, error):
        self.error=error

    def __str__(self):
        return str(self.__class__)

class CassandraException(KomcassException):
    def __init__(self, error):
        super().__init__(error=error)

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, *args, **kwargs):
        try:
            return self.f(*args, **kwargs)
        except NoHostAvailable:
            error=Errors.E_KCE_EH_NHA
            raise CassandraException(error=error)
        except UserTypeDoesNotExist:
            error=Errors.E_KCE_EH_UST
            raise CassandraException(error=error)
        except QueryExhausted:
            error=Errors.E_KCE_EH_QEX
            raise CassandraException(error=error)
        except UnsupportedOperation:
            error=Errors.E_KCE_EH_USO
            raise CassandraException(error=error)
        except OperationTimedOut:
            error=Errors.E_KCE_EH_OTOUT
            raise CassandraException(error=error)
        except AuthenticationFailed:
            error=Errors.E_KCE_EH_AUF
            raise CassandraException(error=error)
        except Unauthorized:
            error=Errors.E_KCE_EH_UNAU
            raise CassandraException(error=error)
        except InvalidRequest:
            error=Errors.E_KCE_EH_INV
            raise CassandraException(error=error)
        except AlreadyExists:
            error=Errors.E_KCE_EH_AEE
            raise CassandraException(error=error)
        except ConfigurationException:
            error=Errors.E_KCE_EH_CFG
            raise CassandraException(error=error)
        except RequestValidationException:
            error=Errors.E_KCE_EH_RVE
            raise CassandraException(error=error)
        except FunctionFailure:
            error=Errors.E_KCE_EH_FFL
            raise CassandraException(error=error)
        except WriteFailure:
            error=Errors.E_KCE_EH_WFL
            raise CassandraException(error=error)
        except ReadFailure:
            error=Errors.E_KCE_EH_RFL
            raise CassandraException(error=error)
        except CoordinationFailure:
            error=Errors.E_KCE_EH_CFL
            raise CassandraException(error=error)
        except WriteTimeout:
            error=Errors.E_KCE_EH_WTOUT
            raise CassandraException(error=error)
        except ReadTimeout:
            error=Errors.E_KCE_EH_RTOUT
            raise CassandraException(error=error)
        except Timeout:
            error=Errors.E_KCE_EH_TOUT
            raise CassandraException(error=error)
        except Unavailable:
            error=Errors.E_KCE_EH_UNA
            raise CassandraException(error=error)
        except RequestExecutionException:
            error=Errors.E_KCE_EH_REE
            raise CassandraException(error=error)
        except DriverException:
            error=Errors.E_KCE_EH_DRE
            raise CassandraException(error=error)
        except:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            raise

