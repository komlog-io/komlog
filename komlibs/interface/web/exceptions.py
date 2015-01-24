from komfig import logger
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.auth import exceptions as authexcept
from komlibs.interface.web import status
from komlibs.interface.web.model import webmodel

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, **kwargs):
        try:
            response=self.f(**kwargs)
            return response if response else webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR)
        except authexcept.AuthException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.BadParametersException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_BAD_PARAMETERS,error=e.error)
        except gestexcept.UserNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.AgentNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.WidgetNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DashboardNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.AgentCreationException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=e.error)
        except gestexcept.UserConfirmationException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=e.error)
        except gestexcept.DatasourceNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatasourceMapNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatapointDataNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatapointNotFoundException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.UserAlreadyExistsException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.AgentAlreadyExistsException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.InvalidPasswordException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.DatasourceUploadContentException as e:
            return webmodel.WebInterfaceResponse(status=status.WEB_STATUS_INTERNAL_ERROR,error=e.error)


class BadParametersException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return str(self.__class__)

