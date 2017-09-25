class AIException(Exception):

    def __init__(self, error, extra):
        self.error = error
        self.extra = extra

    def __str__(self):
        return str(self.__class__)

class DTreeGenerationException(AIException):
    def __init__(self, error, extra=None):
        super().__init__(error=error, extra=extra)
