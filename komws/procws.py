import exceptions as wsex
from komdb import api as dbapi
from komdb import exceptions as dbex
from komfs import api as fsapi
import os



def process(data, context, sql_session):
    """
    The purpose of these functions is to process the service call
    """
    return globals()[context.lower()](data, sql_session)

def wsupload_sample(data, dir, sql_session):
    """
    data:
            - username
            - password
            - agentid
            - datasourceid
            - date (date string in iso format)
            - filecontent
    We need to:
            - Copy the sample (filecontent) to the destfile
    """
    try:
        name = data.date+'_'+str(data.datasourceid)+'.pspl'
        dest_file = os.path.join(dir,name) 
        fsapi.create_sample(dest_file, data.filecontent)
    except Exception as e:
        print str(e)
        raise wsex.ProcessingError()
    else:
        return True

def wsdownload_config(data, sql_session):
    """
    data:
            - username
            - password
            - agentid
    We need to:
            - For each agent's datasource get its configuration
            - return all configuration to the agent            
    """
    configuration = []
    try:
        user = dbapi.User(username=data.username, session=sql_session)
        for agent in user.getAgents(sql_session):
            if agent.validate(data.agentid):
                datasources = agent.getDatasources(sql_session)
                for datasource in datasources:
                    ds_config = datasource.getConfig(sql_session)
                    configuration.append(ds_config)
    except Exception as e:
        raise wsex.ProcessingError()
    else:
        return configuration
    


