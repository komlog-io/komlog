'''
In this file we declare the different web interfaces that
can be accessed in the system
'''

class Interface:
    def __init__(self, value):
        self.value=value

class User_AgentCreation(Interface):
    def __init__(self):
        value='/user/agentcreation/'
        super().__init__(value)

class User_DatasourceCreation(Interface):
    def __init__(self):
        value='/user/dscreation/'
        super().__init__(value)

class User_DatapointCreation(Interface):
    def __init__(self):
        value='/user/dpcreation/'
        super().__init__(value)

class User_WidgetCreation(Interface):
    def __init__(self):
        value='/user/wgcreation/'
        super().__init__(value)

class User_DashboardCreation(Interface):
    def __init__(self):
        value='/user/dbcreation/'
        super().__init__(value)

class User_CircleCreation(Interface):
    def __init__(self):
        value='/user/circlecreation/'
        super().__init__(value)

class User_SnapshotCreation(Interface):
    def __init__(self):
        value='/user/snapshotcreation/'
        super().__init__(value)

class User_AddMemberToCircle(Interface):
    def __init__(self, cid):
        value='/user/addmembertocircle/'+cid.hex
        super().__init__(value)

class User_PostDatasourceDataDaily(Interface):
    def __init__(self, did=None):
        if did:
            value='/user/daily/postdsdata/'+did.hex
        else:
            value='/user/daily/postdsdata/'
        super().__init__(value)

class User_PostDatapointDataDaily(Interface):
    def __init__(self, pid=None):
        if pid:
            value='/user/daily/postdpdata/'+pid.hex
        else:
            value='/user/daily/postdpdata/'
        super().__init__(value)

class User_DataRetrievalMinTimestamp(Interface):
    def __init__(self):
        value='/user/dataretrievalmints/'
        super().__init__(value)

class Agent_DatasourceCreation(Interface):
    def __init__(self, aid):
        value='/agent/dscreation/'+aid.hex
        super().__init__(value)

class Agent_DatapointCreation(Interface):
    def __init__(self, aid):
        value='/agent/dpcreation/'+aid.hex
        super().__init__(value)

class Datasource_DatapointCreation(Interface):
    def __init__(self, did):
        value='/ds/dpcreation/'+did.hex
        super().__init__(value)

