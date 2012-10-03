"""
API to access DB 

"""
import datetime
from komdb import schema
from komdb import connection
from komdb import exceptions
from komdb.config import states,types


session = connection.Session()

class User(object):
    def __init__(self, username):
        try: self.__db_user = session.query(schema.User).filter_by(username=username).first()
        except:
            raise
        else:
            if self.__db_user is not None:
                self.__agents = None
                self.uid = self.__db_user.uid
                self.username = self.__db_user.username
                self.__password = self.__db_user.password
                self.datefrom = self.__db_user.datefrom
                self.state = self.__db_user.state
                self.type = self.__db_user.type
            else:
                raise exceptions.NotFoundUserError()
    
    def __eq__(self, user):
        return self.uid == user.uid

    def validate(self, password):
        return  self.__password == password

    def changePassword(self, old, new):
        if self.validate(old) is True:
            try:
                self.__db_user.password = new
                session.commit()
            except:
                return False
            else:
                self.__password = new
                return True

    def setType(self, type):
        try:
            self.__db_user.type = type
            session.commit()
        except:
            return False
        else:
            self.type = type
            return True

    def setState(self, state):
        try:
            self.__db_user.state = state
            session.commit()
        except:
            return False
        else:
            self.state = state
            return True

    def delete(self):
        if self.__db_user is not None:
            try:
                session.delete(self.__db_user)
                session.commit()
            except:
                session.rollback()
                return False
            return True
        else:
            return False 

    def getInfo(self):
        info = {}
        info['state'] = self.state
        info['type'] = self.type
        info['username'] = self.username
        info['datefrom'] = self.datefrom
        return info

    def getAgents(self):
        if self.__agents is None:
            agents = []
            aids = []
            try:
                for agent in self.__db_user.agents:
                    aids.append(agent.aid)
                for aid in aids:
                    agent = Agent(aid)
                    agents.append(agent)
                self.__agents = agents
            except:
                pass
        return self.__agents


class Agent(object):
    def __init__(self, aid):
        try: self.__db_agent = session.query(schema.Agent).filter_by(aid=aid).first()
        except: 
            raise
        else:
            if self.__db_agent is not None:
                self.__datasources = None
                self.__user = None
                self.uid = self.__db_agent.uid
                self.aid = self.__db_agent.aid
                self.agentname = self.__db_agent.agentname
                self.__password = self.__db_agent.password
                self.datefrom = self.__db_agent.datefrom
                self.state = self.__db_agent.state
                self.type = self.__db_agent.type
            else:
                raise exceptions.NotFoundAgentError()

    def __eq__(self, agent):
        return self.aid == agent.aid

    def validate(self, password):
        return self.__password == password

    def setState(self, state):
        try:
            self.__db_agent.state=state
            session.commit()
        except:
            return False
        else:
            self.state = state
            return True

    def setType(self, type):
        try:
            self.__db_agent.type=type
            session.commit()
        except:
            return False
        else:
            self.type = type
            return True

    def delete(self):
        if self.__db_agent is not None:
            try:
                session.delete(self.__db_agent)
                session.commit()
            except:
                session.rollback()
                return False
            return True
        else:
            return False 

    def getInfo(self):
        info = {}
        info['state'] = self.state
        info['type'] = self.type
        info['agentname'] = self.agentname
        info['datefrom'] = self.datefrom
        return info

    def getDatasources(self):
        if self.__datasources is None:
            datasources = []
            dids = []
            try:
                for datasource in self.__db_agent.datasources:
                    dids.append(datasource.did)
                for did in dids:
                    datasource = Datasource(did)
                    datasources.append(datasource)
                self.__datasources = datasources
            except:
                pass
        return self.__datasources

    def getUser(self):
        if self.__user is None:
            self.__user = User(self.uid)
        return self.__user

#####################################################
# CLASS DATASOURCE
#####################################################

class Datasource(object):
    def __init__(self, did):
        try: self.__db_datasource = session.query(schema.Datasource).filter_by(did=did).first()
        except: self.did = -1
        else:
            if self.__db_datasource is not None:
                self.__datapoints = None
                self.__samples = None
                self.__agent = None
                self.__config = None
                self.aid = self.__db_datasource.aid
                self.did = self.__db_datasource.did
                self.datasourcename = self.__db_datasource.datasourcename
                self.datefrom = self.__db_datasource.datefrom
                self.state = self.__db_datasource.state
                self.type = self.__db_datasource.type
            else:
                self.did = 0

    def __eq__(self, datasource):
        return self.did == datasource.did

    def setState(self, state):
        try:
            self.__db_datasource.state=state
            session.commit()
        except:
            return False
        else:
            self.state = state
            return True

    def setType(self, type):
        try:
            self.__db_datasource.type=type
            session.commit()
        except:
            return False
        else:
            self.type = type
            return True

    def delete(self):
        if self.__db_datasource is not None:
            try:
                session.delete(self.__db_datasource)
                session.commit()
            except:
                session.rollback()
                return False
            return True
        else:
            return False 

    def getInfo(self):
        info = {}
        info['state'] = self.state
        info['type'] = self.type
        info['datapointname'] = self.datasourcename
        info['datefrom'] = self.datefrom
        return info

    def getDatapoints(self):
        if self.__datapoints is None:
            datapoints = []
            pids = []
            try:
                for datapoint in self.__db_datasource.datapoints:
                    pids.append(datapoint.pid)
                for pid in pids:
                    datapoint = Datapoint(pid)
                    datapoints.append(datapoint)
                self.__datapoints = datapoints
            except:
                pass
        return self.__datapoints

    def getSamples(self, limit=25):
        if self.__samples is None:
            samples = []
            sids = []
            try:
                for sample in session.query(schema.Sample).filter_by(did=self.did).limit(limit):
                    sids.append(sample.sid)
                for sid in sids:
                    sample = Sample(sid)
                    samples.append(sample)
                self.__samples = samples
            except:
                pass
        return self.__samples

    def getAgent(self):
        if self.__agent is None:
            self.__agent = Agent(self.aid)
        return self.__agent
    
    def getConfig(self):
        if self.__config is None:
            try:
                self.__config = self.__db_datasource.config
            except:
                pass
        return self.__config
            


###############################################
# CLASS DATAPOINTS
###############################################


class Datapoint(object):
    def __init__(self, pid):
        try:    self.__db_datapoint = session.query(schema.Datapoint).filter_by(pid=pid).first()
        except: self.pid = -1
        else:
            if self.__db_datapoint is not None:
                self.__datasource = None
                self.did = self.__db_datapoint.did
                self.pid = self.__db_datapoint.pid
                self.datapointname = self.__db_datapoint.datapointname
                self.fieldnumber = self.__db_datapoint.fieldnumber
                self.datefrom = self.__db_datapoint.datefrom
                self.state = self.__db_datapoint.state
                self.type = self.__db_datapoint.type
            else:
                self.pid = 0

    def __eq__(self, datapoint):
        return self.pid == datapoint.pid

    def setState(self, state):
        try:
            self.__db_datapoint.state=state
            session.commit()
        except:
            return False
        else:
            self.state = state
            return True

    def setType(self, type):
        try:
            self.__db_datapoint.type=type
            session.commit()
        except:
            return False
        else:
            self.type = type
            return True

    def delete(self):
        if self.__db_datapoint is not None:
            try:
                session.delete(self.__db_datapoint)
                session.commit()
            except:
                session.rollback()
                return False
            return True
        else:
            return False 

    def getInfo(self):
        info = {}
        info['state'] = self.state
        info['type'] = self.type
        info['datapointname'] = self.datapointname
        info['datefrom'] = self.datefrom
        return info
    
    def getDatasource(self):
        if self.__datasource == None:
            self.__datasource = Datasource(self.did)
        return self.__datasource



###############################################
# CLASS SAMPLE
###############################################


class Sample(object):
    def __init__(self, sid):
        try:  self.__db_sample = session.query(schema.Sample).filter_by(sid=sid).first()
        except: self.sid = -1
        else:
            if self.__db_sample is not None:
                self.__datasource = None
                self.did = self.__db_sample.did
                self.sid = self.__db_sample.sid
                self.samplename = self.__db_sample.samplename
                self.dategenerated = self.__db_sample.dategenerated
                self.datereceived = self.__db_sample.datereceived
                self.size = self.__db_sample.size
                self.state = self.__db_sample.state
                self.type = self.__db_sample.type
            else:
                self.sid = 0

    def __eq__(self, sample):
        return self.sid == sample.sid

    def setState(self, state):
        try:
            self.__db_sample.state=state
            session.commit()
        except:
            return False
        else:
            self.state = state
            return True

    def setType(self, type):
        try:
            self.__db_sample.type=type
            session.commit()
        except:
            return False
        else:
            self.type = type
            return True

    def delete(self):
        if self.__db_sample is not None:
            try:
                session.delete(self.__db_sample)
                session.commit()
            except:
                session.rollback()
                return False
            return True
        else:
            return False 

    def getInfo(self):
        info = {}
        info['state'] = self.state
        info['type'] = self.type
        info['samplename'] = self.datapointname
        info['dategenerated'] = self.dategenerated
        info['datereceived'] = self.datereceived
        info['size'] = self.size
        return info
    
    def getDatasource(self):
        if self.__datasource == None:
            self.__datasource = Datasource(self.did)
        return self.__datasource


""" Functions used to create elements on DB """

def create_user(username, password, state=states.STATE_VALUE_USER_ACTIVE, type=types.TYPE_VALUE_USER_DEFAULT):
    """ Create a new user on database """
    try:
        user = User(username)
    except exceptions.NotFoundUserError:
        now = datetime.datetime.utcnow()
        user = schema.User(username, password, now, state, type)
        session.add(user)
        session.commit()
        uid = user.uid
        session.close()
        return uid
    except:
        session.rollback()
        return -1
    else:
        session.close()
        raise exceptions.AlreadyExistingUserError()

def create_agent(username, agentname, password, state=states.STATE_VALUE_AGENT_ACTIVE, type=types.TYPE_VALUE_AGENT_DEFAULT):
    """ Create a new agent on database associated to a given user """ 
    try:
        tmp_user = User(username)
    except exceptions.NotFoundUserError:
        return -1
    except:
        return -1
    else:
        for agent in tmp_user.getAgents():
            if agent.password == password:
                raise exceptions.AlreadyExistingAgentError()
        now = datetime.datetime.utcnow()
        agent = schema.Agent(tmp_user.uid, agentname, password, now, state, type)
        session.add(agent)
        session.commit()
        aid = agent.aid
        session.close()
        return aid

def create_datasource(aid, datasourcename, state=states.STATE_VALUE_DATASOURCE_ACTIVE, type=types.TYPE_VALUE_DATASOURCE_DEFAULT):
    """ Create a new datasource on database associated to a given user-agent """
    try:
        tmp_agent = Agent(aid)
    except exceptions.NotFoundAgentError:
        return -1
    except:
        return -1
    now = datetime.datetime.utcnow()
    datasource = schema.Datasource(tmp_agent.aid, datasourcename, now, state, type)
    session.add(datasource)
    session.commit()
    did = datasource.did
    session.close()
    return did

def create_sample(did, date_generated, state=states.STATE_VALUE_SAMPLE_INITIAL, type=types.TYPE_VALUE_SAMPLE_DEFAULT):
    """
    This function registers a new sample asociated to a datasource passed in the arguments
    """
    try:
        ds = Datasource(did)
    except exceptions.NotFoundDatasourceError:
        return -1
    except:
        return -1
    now = datetime.datetime.utcnow()
    sample = schema.Sample(ds.did, "NoName", date_generated, now, 0,state, type)
    session.add(sample)
    session.commit()
    sid = sample.sid
    session.close()
    return sid

""" Functions used to delete objects from database (intended for testing purposes only)"""

def delete_user(uid):
    db_user = session.query(schema.User).filter_by(uid=uid).first()
    user_object = User(db_user.username)       
    user_object.delete()
    return True

def delete_agent(aid):
    agent_object = Agent(aid)
    agent_object.delete()
    return True

def delete_datasource(did):
    ds_object = Datasource(did)
    ds_object.delete()
    return True

def delete_datapoint(pid):
    dp_object = Datapoint(pid)
    dp_object.delete()
    return True

def delete_sample(sid):
    sample_object = Sample(sid)
    sample_object.delete()
    return True

