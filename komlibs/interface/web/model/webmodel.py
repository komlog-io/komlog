
class WebInterfaceResponse(object):
    def __init__(self, status, error=None, data=None):
        self.status=status
        self.error=error
        self.data=data
