from komlog.komlibs.interface.web.errors import Errors

class WebInterfaceResponse(object):
    def __init__(self, status, error=Errors.OK, data=None):
        self.status=status
        self.error=error
        self.data=data
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

