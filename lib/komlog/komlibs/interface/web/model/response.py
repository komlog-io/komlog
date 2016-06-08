class WebInterfaceResponse(object):
    def __init__(self, status, error=0, data=None):
        self.status=status
        self.error=error
        self.data=data
