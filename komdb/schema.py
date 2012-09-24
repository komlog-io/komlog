from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class UserState(Base):
    __tablename__ = 'user_states'
        
    state = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, state, description):
        self.state = state
        self.description = description

class UserType(Base):
    __tablename__ = 'user_types'

    type = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, type, description):
        self.type = type
        self.description = description

class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    datefrom = Column(DateTime, index=True, nullable=False)
    
    state = Column(Integer, ForeignKey('user_states.state'))
    type = Column(Integer, ForeignKey('user_types.type'))

    agents = relationship("Agent", backref="user")

    def __init__(self, username, password, datefrom, state, type):
        self.username = username
        self.password = password
        self.datefrom = datefrom
        self.state = state
        self.type = type
        
    def __repr__(self):
        return "<User('%s', '%s', '%s', '%d','%d')>" % (self.username, self.password, self.datefrom, self.state, self.type)


class UserCapability(Base):
    __tablename__ = 'user_capabilities'

    state = Column(Integer, ForeignKey('user_states.state'), primary_key=True)
    type = Column(Integer, ForeignKey('user_types.type'), primary_key=True)
    key = Column(String, nullable=False, primary_key=True)
    value = Column(String)

    def __init__(self, state, type, key, value):
        self.state = state
        self.type = type
        self.key = key
        self.value = value

class AgentState(Base):
    __tablename__ = 'agent_states'

    state = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, state, description):
        self.state = state
        self.description = description

class AgentType(Base):
    __tablename__ = 'agent_types'

    type = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, type, description):
        self.type = type
        self.description = description

class Agent(Base):
    __tablename__ = 'agents'

    aid = Column(Integer, primary_key=True, autoincrement=True)
    agentname = Column(String)
    password = Column(String, nullable=False)
    datefrom = Column(DateTime)
    
    state = Column(Integer, ForeignKey('agent_states.state'))
    type = Column(Integer, ForeignKey('agent_types.type'))

    uid = Column(Integer, ForeignKey('users.uid'))

    datasources = relationship("Datasource", backref="agent")


    def __init__(self, uid, agentname, password, datefrom, state, type):
        self.uid = uid
        self.agentname = agentname
        self.password = password
        self.datefrom = datefrom
        self.state = state
        self.type = type

    def __repr__(self):
        return "<Agent('%d', '%s', '%s', '%s', '%d','%d')>" % (self.uid, self.agentname, self.password, self.datefrom, self.state, self.type)

class AgentCapability(Base):
    __tablename__ = 'agent_capabilities'

    state = Column(Integer, ForeignKey('agent_states.state'), primary_key=True)
    type = Column(Integer, ForeignKey('agent_types.type'), primary_key=True)
    key = Column(String, nullable=False, primary_key=True)
    value = Column(String)

    def __init__(self, state, type, key, value):
        self.state = state
        self.type = type
        self.key = key
        self.value = value

class DatasourceState(Base):
    __tablename__ = 'datasource_states'

    state = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, state, description):
        self.state = state
        self.description = description

class DatasourceType(Base):
    __tablename__ = 'datasource_types'

    type = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, type, description):
        self.type = type
        self.description = description

class DatasourceConfig(Base):
    __tablename__ = 'datasource_config'
    
    did = Column(Integer, ForeignKey('datasources.did'), primary_key=True)
    sec = Column(String)
    min = Column(String)
    hour = Column(String)
    dom = Column(String)
    mon = Column(String)
    dow = Column(String)
    command = Column(String)
    

class Datasource(Base):
    __tablename__ = 'datasources'

    did = Column(Integer, primary_key=True, autoincrement=True)
    datasourcename = Column(String)
    datefrom = Column(DateTime)

    state = Column(Integer, ForeignKey('datasource_states.state'))
    type = Column(Integer, ForeignKey('datasource_types.type'))

    aid = Column(Integer, ForeignKey('agents.aid'))

    datapoints= relationship("Datapoint", backref="datasource")
    samples = relationship("Sample", backref="datasource")
    config = relationship("DatasourceConfig", uselist=False, backref="datasource")


    def __init__(self, aid, datasourcename, datefrom, state, type):
        self.aid = aid
        self.datasourcename = datasourcename
        self.datefrom = datefrom
        self.state = state
        self.type = type

    def __repr__(self):
        return "<Datasource('%d', '%s', '%s', '%d','%d')>" % (self.aid, self.datasourcename, self.datefrom, self.state, self.type)

class DatasourceCapability(Base):
    __tablename__ = 'datasource_capabilities'

    state = Column(Integer, ForeignKey('datasource_states.state'), primary_key=True)
    type = Column(Integer, ForeignKey('datasource_types.type'), primary_key=True)
    key = Column(String, nullable=False, primary_key=True)
    value = Column(String)

    def __init__(self, state, type, key, value):
        self.state = state
        self.type = type
        self.key = key
        self.value = value

class DatapointState(Base):
    __tablename__ = 'datapoint_states'

    state = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, state, description):
        self.state = state
        self.description = description

class DatapointType(Base):
    __tablename__ = 'datapoint_types'

    type = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, type, description):
        self.type = type
        self.description = description

class Datapoint(Base):
    __tablename__ = 'datapoints'

    pid = Column(Integer, primary_key=True, autoincrement=True)
    datapointname = Column(String)
    fieldnumber = Column(Integer)
    datefrom = Column(DateTime)

    state = Column(Integer, ForeignKey('datapoint_states.state'))
    type = Column(Integer, ForeignKey('datapoint_types.type'))

    did = Column(Integer, ForeignKey('datasources.did'))

    def __init__(self, did, datapointname, fieldnumber, datefrom, state, type):
        self.did = did
        self.datapointname = datapointname
        self.fieldnumber = fieldnumber
        self.datefrom = datefrom
        self.state = state
        self.type = type

    def __repr__(self):
        return "<Datapoint('%d', '%s', '%d', '%s', '%d','%d')>" % (self.did, self.username, self.fieldnumber, self.datefrom, self.state, self.type)

class DatapointCapability(Base):
    __tablename__ = 'datapoint_capabilities'

    state = Column(Integer, ForeignKey('datapoint_states.state'), primary_key=True)
    type = Column(Integer, ForeignKey('datapoint_types.type'), primary_key=True)
    key = Column(String, nullable=False, primary_key=True)
    value = Column(String)

    def __init__(self, state, type, key, value):
        self.state = state
        self.type = type
        self.key = key
        self.value = value

class SampleState(Base):
    __tablename__ = 'sample_states'

    state = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, state, description):
        self.state = state
        self.description = description

class SampleType(Base):
    __tablename__ = 'sample_types'

    type = Column(Integer, primary_key=True)
    description = Column(String)

    def __init__(self, type, description):
        self.type = type
        self.description = description

class Sample(Base):
    __tablename__ = 'samples'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    samplename = Column(String)
    dategenerated = Column(DateTime)
    datereceived = Column(DateTime)
    size = Column(Integer)

    state = Column(Integer, ForeignKey('sample_states.state'))
    type = Column(Integer, ForeignKey('sample_types.type'))

    did = Column(Integer, ForeignKey('datasources.did'))

    def __init__(self, did, samplename, dategenerated, datereceived, size, state, type):
        self.did = did
        self.samplename = samplename
        self.dategenerated = dategenerated
        self.datereceived = datereceived
        self.size = size
        self.state = state
        self.type = type

    def __repr__(self):
        return "<Sample('%d', '%s', '%s', '%s', '%d', '%d','%d')>" % (self.did, self.username, self.dategenerated, self.datereceived, self.size, self.state, self.type)

class SampleCapability(Base):
    __tablename__ = 'sample_capabilities'

    state = Column(Integer, ForeignKey('sample_states.state'), primary_key=True)
    type = Column(Integer, ForeignKey('sample_types.type'), primary_key=True)
    key = Column(String, nullable=False, primary_key=True)
    value = Column(String)

    def __init__(self, state, type, key, value):
        self.state = state
        self.type = type
        self.key = key
        self.value = value

