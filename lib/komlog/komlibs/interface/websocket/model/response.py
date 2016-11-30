from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.errors import Errors

class Response:
    def __init__(self, status, error=Errors.OK, reason=None):
        self._status=None
        self.status=status
        self.error=error
        self.reason=reason
        self._routed_messages={}
        self._unrouted_messages=[]

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if args.is_valid_int(value):
            self._status=value
        else:
            raise exceptions.ResponseValidationException(error=Errors.E_IWSMR_RESP_IS)

    @property
    def routed_messages(self):
        return self._routed_messages

    @routed_messages.setter
    def routed_messages(self, value):
        raise TypeError

    @property
    def unrouted_messages(self):
        return self._unrouted_messages

    @unrouted_messages.setter
    def unrouted_messages(self, value):
        raise TypeError

    def add_message(self, msg, dest=None):
        if dest is not None:
            try:
                self._routed_messages[dest].append(msg)
            except KeyError:
                self._routed_messages[dest]=[msg]
        else:
            self._unrouted_messages.append(msg)
        return True

