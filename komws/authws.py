from komdb import api
from komdb import exceptions as dbex
from komws import exceptions as wsex

def authenticate(data, context):
    """
    The purpose of these functions is to authenticate the client who queries the web service
    """
    print "Auth Dispatch"
    globals()[context.lower()](data)

def wsupload_sample(data):
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
    print "Init wsupload_sample()"
    try:
        user = api.User(data.username)
        if user.validate(data.password):
            agents = user.getAgents()
            for agent in agents:
                if agent.validate(data.agentid):
                    datasources = agent.getDatasources()
                    for ds in datasources:
                        if ds.did == data.datasourceid:
                            print "AUTH OK"
                            return True
    except:
        print "AUTH ERROR"
        raise wsex.AuthenticationError
    else:
        print "AUTH ERROR"
        raise wsex.AuthenticationError

def wsdownload_config(data):
    """
    data:
            - username
            - password
            - agentid
    We need to:
        - authenticate user
        - authenticate agent
    """
    print "Init wsdownload_config()"
    try:
        user = api.User(data.username)
        if user.validate(data.password):
            agents = user.getAgents()
            for agent in agents:
                if agent.validate(data.agentid):
                    print "AUTH OK"
                    return True
    except:
        print "AUTH ERROR"
        raise wsex.AuthenticationError
    else:
        print "AUTH ERROR"
        raise wsex.AuthenticationError



