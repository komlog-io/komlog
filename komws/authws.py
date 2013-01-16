from komdb import api
from komdb import exceptions as dbex
import exceptions as wsex

def authenticate(data, context, sql_session):
    """
    The purpose of these functions is to authenticate the client who queries the web service
    """
    globals()[context.lower()](data, sql_session)

def wsupload_sample(data, sql_session):
    """
    data:
            - username
            - password
            - agentid
            - datasourceid
            - date
            - filecontent
    We need to:
        - authenticate user
        - authenticate agent
        - confirm datasource belonging
    """
    try:
        user = api.User(username=data.username, session=sql_session)
        if user.validate(data.password):
            agents = user.getAgents(sql_session)
            for agent in agents:
                if agent.validate(data.agentid):
                    datasources = agent.getDatasources(sql_session)
                    for ds in datasources:
                        if int(ds.did) == int(data.datasourceid):
                            return True
    except Exception, e:
        raise wsex.AuthenticationError
    else:
        raise wsex.AuthenticationError

def wsdownload_config(data, sql_session):
    """
    data:
            - username
            - password
            - agentid
    We need to:
        - authenticate user
        - authenticate agent
    """
    try:
        user = api.User(username=data.username,session=sql_session)
        if user.validate(data.password):
            agents = user.getAgents(sql_session)
            for agent in agents:
                if agent.validate(data.agentid):
                    return True
            ''' If we get here, means agent not found. To make it simple, we create it. '''
            aid = api.create_agent(data.username, 'Agent '+data.agentid, data.agentid, sql_session)
            if aid>0:
                return True
            else:
                raise wsex.AuthenticationError
                
    except:
        raise wsex.AuthenticationError
    else:
        raise wsex.AuthenticationError



