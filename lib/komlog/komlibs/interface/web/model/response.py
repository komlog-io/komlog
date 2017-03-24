from komlog.komlibs.interface.web.errors import Errors

class WebInterfaceResponse(object):
    def __init__(self, status, error=Errors.OK, data=None):
        self.status=status
        self.error=error
        self.data=data
        self._imc_messages={'routed':{},'unrouted':[]}

    @property
    def imc_messages(self):
        return self._imc_messages

    @imc_messages.setter
    def imc_messages(self, value):
        raise TypeError

    def add_imc_message(self, msg, dest=None):
        if dest is not None:
            try:
                self._imc_messages['routed'][dest].append(msg)
            except KeyError:
                self._imc_messages['routed'][dest]=[msg]
        else:
            self._imc_messages['unrouted'].append(msg)
        return True

