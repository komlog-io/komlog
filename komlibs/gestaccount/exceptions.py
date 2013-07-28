
class AgentCreationException(Exception):
    def __init__(self):
        pass

class AgentNotFoundException(Exception):
    def __init__(self):
        pass

class UserNotFoundException(Exception):
    def __init__(self):
        pass

class DatasourceCreationException(Exception):
    def __init__(self):
        pass

class DatasourceNotFoundException(Exception):
    def __init__(self):
        pass

class DatasourceUploadContentException(Exception):
    def __init__(self):
        pass

class DatasourceUpdateException(Exception):
    def __init__(self):
        pass

class DatapointDataNotFoundException(Exception):
    def __init__(self, last_date):
        self.last_date=last_date

class DatapointCreationException(Exception):
    def __init__(self, last_date):
        self.last_date=last_date

class BadParametersException(Exception):
    def __init__(self):
        pass
