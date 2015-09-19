class EventsException(Exception):
    def __init__(self, error):
        self.error=error

    def __str__(self):
        return str(self.__class__)

class BadParametersException(EventsException):
    def __init__(self, error):
        super(BadParametersException,self).__init__(error=error)

class EventNotFoundException(EventsException):
    def __init__(self, error):
        super(EventNotFoundException,self).__init__(error=error)

