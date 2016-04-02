from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket.protocol.v1 import errors, exceptions

class Response:
    def __init__(self, status, error=None, reason=None):
        self._status=None
        self.error=error
        self.reason=reason
        self.status=status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if args.is_valid_int(value):
            self._status=value
        else:
            raise exceptions.ResponseValidationException(error=errors.E_IWSPV1MR_RESP_IS)

