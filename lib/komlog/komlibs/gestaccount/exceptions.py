class GestaccountException(Exception):
    def __init__(self, error, extra=None):
        self.error = error
        self.extra = extra

    def __str__(self):
        return str(self.__class__)

class AgentCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class AgentNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class AgentAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class UserNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class UserAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class EmailAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class UserConfirmationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class UserCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class UserUnsupportedOperationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class InvalidPasswordException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceDataNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceVariableNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceMapNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceUploadContentException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceUpdateException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceNoveltyDetectorException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceTextSummaryException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointDataNotFoundException(GestaccountException):
    def __init__(self, error, last_date=None):
        self.last_date=last_date
        super().__init__(error=error)

class DatapointNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointUpdateException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointDTreeTrainingSetEmptyException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointDTreeNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointDTreeGenerationException(GestaccountException):
    def __init__(self, error, extra):
        super().__init__(error=error, extra=extra)

class DatapointUnsupportedOperationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class BadParametersException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class WidgetCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class WidgetNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class WidgetAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class WidgetTypeNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class WidgetUnsupportedOperationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class AddDatapointToWidgetException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DeleteDatapointFromWidgetException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DashboardNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DashboardCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DashboardUpdateException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class SnapshotNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class SnapshotCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class CircleCreationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class CircleNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class CircleUpdateException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class CircleAddMemberException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class CircleDeleteMemberException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class InvitationNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class InvitationProcessException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class ForgetRequestNotFoundException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class ForgetRequestException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class ChallengeGenerationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class ChallengeValidationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatasourceHashGenerationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class DatapointStoreValueException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class UpdateOperationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

