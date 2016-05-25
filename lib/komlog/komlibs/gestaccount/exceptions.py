class GestaccountException(Exception):
    def __init__(self, error):
        self.error=error

    def __str__(self):
        return str(self.__class__)

class AgentCreationException(GestaccountException):
    def __init__(self, error):
        super(AgentCreationException,self).__init__(error=error)

class AgentNotFoundException(GestaccountException):
    def __init__(self, error):
        super(AgentNotFoundException,self).__init__(error=error)

class AgentAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super(AgentAlreadyExistsException,self).__init__(error=error)

class UserNotFoundException(GestaccountException):
    def __init__(self, error):
        super(UserNotFoundException,self).__init__(error=error)

class UserAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super(UserAlreadyExistsException,self).__init__(error=error)

class EmailAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super(EmailAlreadyExistsException,self).__init__(error=error)

class UserConfirmationException(GestaccountException):
    def __init__(self, error):
        super(UserConfirmationException,self).__init__(error=error)
    
class UserCreationException(GestaccountException):
    def __init__(self, error):
        super(UserCreationException,self).__init__(error=error)

class InvalidPasswordException(GestaccountException):
    def __init__(self, error):
        super(InvalidPasswordException,self).__init__(error=error)

class DatasourceCreationException(GestaccountException):
    def __init__(self, error):
        super(DatasourceCreationException,self).__init__(error=error)

class DatasourceNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DatasourceNotFoundException,self).__init__(error=error)

class DatasourceDataNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DatasourceDataNotFoundException,self).__init__(error=error)

class DatasourceVariableNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DatasourceVariableNotFoundException,self).__init__(error=error)

class DatasourceMapNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DatasourceMapNotFoundException,self).__init__(error=error)

class DatasourceUploadContentException(GestaccountException):
    def __init__(self, error):
        super(DatasourceUploadContentException,self).__init__(error=error)

class DatasourceUpdateException(GestaccountException):
    def __init__(self, error):
        super(DatasourceUpdateException,self).__init__(error=error)

class DatasourceNoveltyDetectorException(GestaccountException):
    def __init__(self, error):
        super(DatasourceNoveltyDetectorException,self).__init__(error=error)

class DatasourceTextSummaryException(GestaccountException):
    def __init__(self, error):
        super(DatasourceTextSummaryException,self).__init__(error=error)

class DatapointDataNotFoundException(GestaccountException):
    def __init__(self, error, last_date=None):
        self.last_date=last_date
        super(DatapointDataNotFoundException,self).__init__(error=error)

class DatapointNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DatapointNotFoundException,self).__init__(error=error)

class DatapointUpdateException(GestaccountException):
    def __init__(self, error):
        super(DatapointUpdateException,self).__init__(error=error)

class DatapointCreationException(GestaccountException):
    def __init__(self, error):
        super(DatapointCreationException,self).__init__(error=error)

class DatapointDTreeTrainingSetEmptyException(GestaccountException):
    def __init__(self, error):
        super(DatapointDTreeTrainingSetEmptyException,self).__init__(error=error)

class DatapointDTreeNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DatapointDTreeNotFoundException,self).__init__(error=error)

class DatapointUnsupportedOperationException(GestaccountException):
    def __init__(self, error):
        super().__init__(error=error)

class BadParametersException(GestaccountException):
    def __init__(self, error):
        super(BadParametersException,self).__init__(error=error)

class WidgetCreationException(GestaccountException):
    def __init__(self, error):
        super(WidgetCreationException,self).__init__(error=error)

class WidgetNotFoundException(GestaccountException):
    def __init__(self, error):
        super(WidgetNotFoundException,self).__init__(error=error)

class WidgetAlreadyExistsException(GestaccountException):
    def __init__(self, error):
        super(WidgetAlreadyExistsException,self).__init__(error=error)

class WidgetTypeNotFoundException(GestaccountException):
    def __init__(self, error):
        super(WidgetTypeNotFoundException,self).__init__(error=error)

class WidgetUnsupportedOperationException(GestaccountException):
    def __init__(self, error):
        super(WidgetUnsupportedOperationException,self).__init__(error=error)

class AddDatapointToWidgetException(GestaccountException):
    def __init__(self, error):
        super(AddDatapointToWidgetException,self).__init__(error=error)

class DeleteDatapointFromWidgetException(GestaccountException):
    def __init__(self, error):
        super(DeleteDatapointFromWidgetException,self).__init__(error=error)

class DashboardNotFoundException(GestaccountException):
    def __init__(self, error):
        super(DashboardNotFoundException,self).__init__(error=error)

class DashboardCreationException(GestaccountException):
    def __init__(self, error):
        super(DashboardCreationException,self).__init__(error=error)

class DashboardUpdateException(GestaccountException):
    def __init__(self, error):
        super(DashboardUpdateException,self).__init__(error=error)

class SnapshotNotFoundException(GestaccountException):
    def __init__(self, error):
        super(SnapshotNotFoundException,self).__init__(error=error)

class SnapshotCreationException(GestaccountException):
    def __init__(self, error):
        super(SnapshotCreationException,self).__init__(error=error)

class CircleCreationException(GestaccountException):
    def __init__(self, error):
        super(CircleCreationException,self).__init__(error=error)

class CircleNotFoundException(GestaccountException):
    def __init__(self, error):
        super(CircleNotFoundException,self).__init__(error=error)

class CircleUpdateException(GestaccountException):
    def __init__(self, error):
        super(CircleUpdateException,self).__init__(error=error)

class CircleAddMemberException(GestaccountException):
    def __init__(self, error):
        super(CircleAddMemberException,self).__init__(error=error)

class CircleDeleteMemberException(GestaccountException):
    def __init__(self, error):
        super(CircleDeleteMemberException,self).__init__(error=error)

class InvitationNotFoundException(GestaccountException):
    def __init__(self, error):
        super(InvitationNotFoundException,self).__init__(error=error)

class InvitationProcessException(GestaccountException):
    def __init__(self, error):
        super(InvitationProcessException,self).__init__(error=error)

class ForgetRequestNotFoundException(GestaccountException):
    def __init__(self, error):
        super(ForgetRequestNotFoundException,self).__init__(error=error)

class ForgetRequestException(GestaccountException):
    def __init__(self, error):
        super(ForgetRequestException,self).__init__(error=error)

class ChallengeGenerationException(GestaccountException):
    def __init__(self, error):
        super(ChallengeGenerationException,self).__init__(error=error)

class ChallengeValidationException(GestaccountException):
    def __init__(self, error):
        super(ChallengeValidationException,self).__init__(error=error)

class DatasourceHashGenerationException(GestaccountException):
    def __init__(self, error):
        super(DatasourceHashGenerationException,self).__init__(error=error)

