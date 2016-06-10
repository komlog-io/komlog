from komlog.komlibs.interface.web.errors import Errors

class WebInterfaceResponse(object):
    def __init__(self, status, error=Errors.OK, data=None):
        self.status=status
        self.error=error
        self.data=data
