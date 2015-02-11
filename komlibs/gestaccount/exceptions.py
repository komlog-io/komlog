class GestaccountException(Exception):
    def __init__(self, error=None):
        self.error=error

    def __str__(self):
        return str(self.__class__)

class AgentCreationException(GestaccountException):
    def __init__(self):
        super(AgentCreationException,self).__init__()

class AgentNotFoundException(GestaccountException):
    def __init__(self):
        super(AgentNotFoundException,self).__init__()

class AgentAlreadyExistsException(GestaccountException):
    def __init__(self):
        super(AgentAlreadyExistsException,self).__init__()

class UserNotFoundException(GestaccountException):
    def __init__(self):
        super(UserNotFoundException,self).__init__()

class UserAlreadyExistsException(GestaccountException):
    def __init__(self):
        super(UserAlreadyExistsException,self).__init__()

class EmailAlreadyExistsException(GestaccountException):
    def __init__(self):
        super(EmailAlreadyExistsException,self).__init__()

class UserConfirmationException(GestaccountException):
    def __init__(self):
        super(UserConfirmationException,self).__init__()
    
class UserCreationException(GestaccountException):
    def __init__(self):
        super(UserCreationException,self).__init__()

class InvalidPasswordException(GestaccountException):
    def __init__(self):
        super(InvalidPasswordException,self).__init__()

class DatasourceCreationException(GestaccountException):
    def __init__(self):
        super(DatasourceCreationException,self).__init__()

class DatasourceNotFoundException(GestaccountException):
    def __init__(self):
        super(DatasourceNotFoundException,self).__init__()

class DatasourceDataNotFoundException(GestaccountException):
    def __init__(self):
        super(DatasourceDataNotFoundException,self).__init__()

class DatasourceVariableNotFoundException(GestaccountException):
    def __init__(self):
        super(DatasourceVariableNotFoundException,self).__init__()

class DatasourceMapNotFoundException(GestaccountException):
    def __init__(self):
        super(DatasourceMapNotFoundException,self).__init__()

class DatasourceUploadContentException(GestaccountException):
    def __init__(self):
        super(DatasourceUploadContentException,self).__init__()

class DatasourceUpdateException(GestaccountException):
    def __init__(self):
        super(DatasourceUpdateException,self).__init__()

class DatapointDataNotFoundException(GestaccountException):
    def __init__(self, last_date=None):
        self.last_date=last_date
        super(DatapointDataNotFoundException,self).__init__()

class DatapointNotFoundException(GestaccountException):
    def __init__(self):
        super(DatapointNotFoundException,self).__init__()

class DatapointUpdateException(GestaccountException):
    def __init__(self):
        super(DatapointUpdateException,self).__init__()

class DatapointCreationException(GestaccountException):
    def __init__(self):
        super(DatapointCreationException,self).__init__()

class DatapointDTreeTrainingSetEmptyException(GestaccountException):
    def __init__(self):
        super(DatapointDTreeTrainingSetEmptyException,self).__init__()

class DatapointDTreeNotFoundException(GestaccountException):
    def __init__(self):
        super(DatapointDTreeNotFoundException,self).__init__()

class VariableMatchesExistingDatapointException(GestaccountException):
    def __init__(self):
        super(VariableMatchesExistingDatapointException,self).__init__()

class BadParametersException(GestaccountException):
    def __init__(self):
        super(BadParametersException,self).__init__()

class WidgetCreationException(GestaccountException):
    def __init__(self):
        super(WidgetCreationException,self).__init__()

class WidgetNotFoundException(GestaccountException):
    def __init__(self):
        super(WidgetNotFoundException,self).__init__()

class WidgetAlreadyExistsException(GestaccountException):
    def __init__(self):
        super(WidgetAlreadyExistsException,self).__init__()

class WidgetTypeNotFoundException(GestaccountException):
    def __init__(self):
        super(WidgetTypeNotFoundException,self).__init__()

class WidgetUnsupportedOperationException(GestaccountException):
    def __init__(self):
        super(WidgetUnsupportedOperationException,self).__init__()

class AddDatapointToWidgetException(GestaccountException):
    def __init__(self):
        super(AddDatapointToWidgetException,self).__init__()

class DeleteDatapointFromWidgetException(GestaccountException):
    def __init__(self):
        super(DeleteDatapointFromWidgetException,self).__init__()

class DashboardNotFoundException(GestaccountException):
    def __init__(self):
        super(DashboardNotFoundException,self).__init__()

class DashboardCreationException(GestaccountException):
    def __init__(self):
        super(DashboardCreationException,self).__init__()

class DashboardUpdateException(GestaccountException):
    def __init__(self):
        super(DashboardUpdateException,self).__init__()

