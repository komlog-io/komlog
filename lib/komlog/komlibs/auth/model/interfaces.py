'''
In this file we declare the different web interfaces that
can be accessed in the system
'''

class Interface:
    def __init__(self, value):
        self.value=value

class User_AgentCreation(Interface):
    def __init__(self):
        value='user.creation.agent'
        super().__init__(value)

class User_DatasourceCreation(Interface):
    def __init__(self):
        value='user.creation.datasource'
        super().__init__(value)

class User_DatapointCreation(Interface):
    def __init__(self):
        value='user.creation.datapoint'
        super().__init__(value)

class User_WidgetCreation(Interface):
    def __init__(self):
        value='user.creation.widget'
        super().__init__(value)

class User_DashboardCreation(Interface):
    def __init__(self):
        value='user.creation.dashboard'
        super().__init__(value)

class User_CircleCreation(Interface):
    def __init__(self):
        value='user.creation.circle'
        super().__init__(value)

class User_SnapshotCreation(Interface):
    def __init__(self):
        value='user.creation.snapshot'
        super().__init__(value)

class User_AddMemberToCircle(Interface):
    def __init__(self, cid):
        value='user.add.circle.member.'+cid.hex
        super().__init__(value)

class User_PostDatasourceDataDaily(Interface):
    def __init__(self, did=None):
        if did:
            value='daily.user.add.data.datasource.'+did.hex
        else:
            value='daily.user.add.data.datasource'
        super().__init__(value)

class User_PostDatapointDataDaily(Interface):
    def __init__(self, pid=None):
        if pid:
            value='daily.user.add.data.datapoint.'+pid.hex
        else:
            value='daily.user.add.data.datapoint'
        super().__init__(value)

class User_DataRetrievalMinTimestamp(Interface):
    def __init__(self):
        value='user.get.data.min_ts'
        super().__init__(value)

class Agent_DatasourceCreation(Interface):
    def __init__(self, aid):
        value='agent.creation.datasource.'+aid.hex
        super().__init__(value)

class Agent_DatapointCreation(Interface):
    def __init__(self, aid):
        value='agent.creation.datapoint.'+aid.hex
        super().__init__(value)

class Datasource_DatapointCreation(Interface):
    def __init__(self, did):
        value='datasource.creation.datapoint.'+did.hex
        super().__init__(value)

