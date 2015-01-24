from komfig import logger
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.auth import exceptions as authexcept
from komlibs.interface.imc import status
from komlibs.interface.imc.model import responses

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, **kwargs):
        try:
            response=self.f(**kwargs)
            return response
        except authexcept.AuthException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.BadParametersException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_BAD_PARAMETERS,error=e.error)
        except gestexcept.UserNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.AgentNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.WidgetNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DashboardNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.AgentCreationException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR,error=e.error)
        except gestexcept.UserConfirmationException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR,error=e.error)
        except gestexcept.DatasourceNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatasourceDataNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatasourceMapNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatapointDataNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.DatapointNotFoundException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_NOT_FOUND,error=e.error)
        except gestexcept.UserAlreadyExistsException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.AgentAlreadyExistsException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.InvalidPasswordException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_ACCESS_DENIED,error=e.error)
        except gestexcept.DatasourceUploadContentException as e:
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR,error=e.error)
        except Exception as e:
            logger.logger.debug('IMC Response Exception: '+str(e))
            return responses.ImcInterfaceResponse(status=status.IMC_STATUS_INTERNAL_ERROR)


class BadParametersException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return str(self.__class__)

