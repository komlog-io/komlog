from komlog.komlibs.interface.imc.errors import Errors

class ImcInterfaceResponse:
    def __init__(self, status, error=Errors.OK, message_type=None, message_params=None ):
        self.status=status
        self.error=error
        self.message_type=message_type
        self.message_params=message_params
        self._routed_messages={}
        self._unrouted_messages=[]

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

