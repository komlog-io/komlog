
class AgentCreationException(Exception):
    def __init__(self):
        pass

class AgentNotFoundException(Exception):
    def __init__(self):
        pass

class UserNotFoundException(Exception):
    def __init__(self):
        pass

class UserAlreadyExistsException(Exception):
    def __init__(self):
        pass

class UserCreationException(Exception):
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

class DatapointNotFoundException(Exception):
    def __init__(self):
        pass

class DatapointUpdateException(Exception):
    def __init__(self):
        pass

class DatapointCreationException(Exception):
    def __init__(self, last_date):
        self.last_date=last_date

class BadParametersException(Exception):
    def __init__(self):
        pass

class GraphNotFoundException(Exception):
    def __init__(self):
        pass

class GraphCreationException(Exception):
    def __init__(self):
        pass

